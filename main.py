BB84# === SOVEREIGN ETHICS ENGINE — FINAL INTEGRATION ===
def load_ethics_lists():
    """Load blacklist/whitelist once at startup"""
    blacklist = set()
    whitelist = set()
    if os.path.exists(cfg["ethics"]["blacklist_file"]):
        blacklist = set(yaml.safe_load(open(cfg["ethics"]["blacklist_file"])) or [])
    if os.path.exists(cfg["ethics"]["whitelist_file"]):
        whitelist = set(yaml.safe_load(open(cfg["ethics"]["whitelist_file"])) or [])
    return blacklist, whitelist

BLACKLIST, WHITELIST = load_ethics_lists()

def ethics_violation_log(entity: str, type_: str, project: str):
    """Log every blocked attempt"""
    if cfg["ethics"].get("log_violations", True):
        log_path = OUTPUT_DIR / "ethics_violations.log"
        with open(log_path, "a") as f:
            f.write(f"{datetime.now().isoformat()} | BLOCKED | {type_} | {entity} | {project}\n")

def is_entity_allowed(entity_name: str, entity_type: str) -> bool:
    """The vhitzee blade — single source of truth"""
    if not cfg["ethics"]["enabled"]:
        return True

    mode = cfg["ethics"].get("mode", "blacklist")
    strict = cfg["ethics"].get("strict_mode", False)

    # Normalize name
    name = entity_name.strip().split()[0] if entity_type == "manufacturer" else entity_name

    if mode == "blacklist":
        if name in BLACKLIST:
            ethics_violation_log(name, entity_type, project_key)
            click.echo(f"   VHITZEE BLADE: {name} BLOCKED ({entity_type} blacklisted)")
            return False
        return True

    elif mode == "whitelist":
        allowed = name in WHITELIST
        if not allowed:
            ethics_violation_log(name, entity_type, project_key)
            if strict:
                click.echo(f"   VHITZEE BLADE: {name} REJECTED — not in Circle of Honor (strict mode)")
                click.echo("   Bid halted. Only the worthy eat.")
                raise SystemExit(1)  # hard stop
            else:
                click.echo(f"   VHITZEE BLADE: {name} excluded — not in whitelist")
        return allowed

# === REBUILT build_line_items WITH ETHICS FUSED ===
def build_line_items(takeoff: dict, region: str, project_key: str):
    priority_mfr = cfg["manufacturers_priority"][0]
    active_suppliers = [s for s in cfg["suppliers"] if s.get("active", True)]
    items = []

    # Sealant line
    if takeoff["sealant_linear_feet"] > 0:
        if not is_entity_allowed(priority_mfr, "manufacturer"):
            click.echo(f"   → Skipping sealant — {priority_mfr} not allowed")
        else:
            supplier_allowed = False
            price = 18.42
            for s in active_suppliers:
                if is_entity_allowed(s["name"], "supplier"):
                    price = scrape_price(s, "Tremco Vulkem 45SSL", region)
                    supplier_allowed = True
                    break
            if not supplier_allowed:
                click.echo("   → No clean supplier found for sealant — using fallback price")
            
            qty = takeoff["sealant_linear_feet"]
            labor_hrs = qty / cfg["labor"]["productivity"]["sealant_lf_per_hour"]
            labor_rate = cfg["labor"]["rates"]["Sealant Installer"]
            items.append({
                "desc": f"{priority_mfr} Vulkem 45SSL Sealant",
                "qty": qty, "unit": "LF", "mat_price": price,
                "labor_hours": round(labor_hrs, 1), "labor_rate": labor_rate,
                "line_total": qty * price + labor_hrs * labor_rate,
                "ethics_status": "CLEAN"
            })

    # Deck coating line
    if takeoff["deck_coating_sf"] > 0:
        if not is_entity_allowed(priority_mfr, "manufacturer"):
            click.echo(f"   → Skipping deck coating — {priority_mfr} not allowed")
        else:
            supplier_allowed = False
            price = 4.87
            for s in active_suppliers:
                if is_entity_allowed(s["name"], "supplier"):
                    price = scrape_price(s, "Tremco Spectrem 2", region)
                    supplier_allowed = True
                    break
            if not supplier_allowed:
                click.echo("   → No clean supplier found for deck coating")
            
            qty = takeoff["deck_coating_sf"]
            labor_hrs = qty / cfg["labor"]["productivity"]["deck_coating_sf_per_hour"]
            labor_rate = cfg["labor"]["rates"]["Deck Coating Foreman"]
            items.append({
                "desc": f"{priority_mfr} Spectrem 2 Deck Coating",
                "qty": qty, "unit": "SF", "mat_price": price,
                "labor_hours": round(labor_hrs, 1), "labor_rate": labor_rate,
                "line_total": qty * price + labor_hrs * labor_rate,
                "ethics_status": "CLEAN"
            })

    # Subs — only invite Circle of Honor
    if cfg["subcontractors"]["enabled"]:
        for sub in APPROVED_SUBS:
            if is_entity_allowed(sub["name"], "subcontractor"):
                # invite logic here
                pass
            else:
                click.echo(f"   → Sub {sub['name']} BLOCKED by vhitzee blade")

    return items
def is_entity_allowed(entity_name: str, entity_type: str, bypass_reason: str = "") -> bool:
    if not cfg["ethics"]["enabled"]:
        return True

    # Emergency mode = warnings only, never blocks
    if cfg["ethics"]["emergency_mode"]["active"]:
        click.echo(f"   EMERGENCY MODE: {entity_name} allowed ({cfg['ethics']['emergency_mode']['reason']})")
        return True

    # Manual bypass per category
    bypass_cfg = cfg["ethics"]["bypass"]
    if bypass_cfg["enabled"]:
        override_key = f"allow_{entity_type}_override"
        if bypass_cfg.get(override_key, False):
            reason = bypass_reason or "manual override"
            click.echo(f"   SOVEREIGN OVERRIDE: {entity_name} allowed — {reason}")
            return True

    # Normal ethics blade (only runs if no override)
    name = entity_name.strip().split()[0] if entity_type == "manufacturer" else entity_name
    mode = cfg["ethics"].get("mode", "blacklist")

    if mode == "blacklist":
        if name in BLACKLIST:
            msg = f"   VHITZEE BLADE: {name} BLOCKED (blacklisted)"
            if cfg["ethics"]["strict_mode"]:
                click.echo(msg)
                raise SystemExit(1)
            else:
                click.echo(msg + " — continuing (non-strict)")
                return False
        return True

    elif mode == "whitelist":
        if name not in WHITELIST:
            msg = f"   VHITZEE BLADE: {name} REJECTED — not in Circle of Honor"
            if cfg["ethics"]["strict_mode"]:
                click.echo(msg)
                raise SystemExit(1)
            else:
                click.echo(msg + " — continuing (non-strict)")
                return False
        return True

    return True