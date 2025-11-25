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
# === SOVEREIGN AUDIT TRAIL ===
AUDIT_LOG = OUTPUT_DIR / "ethics_audit.log"

def audit_log(event_type: str, category: str, entity: str, result: str, reason: str = ""):
    line = f"{datetime.now().isoformat()} | {event_type.ljust(7)} | {category.ljust(12} | {entity.ljust(20)} | {result.ljust(8)} | {reason}\n"
    with open(AUDIT_LOG, "a") as f:
        f.write(line)

# Log config at startup
def log_ethics_config():
    e = cfg["ethics"]
    audit_log("AUDIT", "config", "ethics_enabled", str(e["enabled"]))
    audit_log("AUDIT", "config", "mode", e.get("mode", "blacklist"))
    audit_log("AUDIT", "config", "strict_mode", str(e.get("strict_mode", False)))
    audit_log("AUDIT", "config", "emergency_mode", str(e["emergency_mode"]["active"]))
    if e["emergency_mode"]["active"]:
        audit_log("AUDIT", "config", "emergency_reason", e["emergency_mode"].get("reason", ""))

# Updated is_entity_allowed with full auditing
def is_entity_allowed(entity_name: str, entity_type: str, bypass_reason: str = "") -> bool:
    if not cfg["ethics"]["enabled"]:
        audit_log("CHECK", entity_type, entity_name, "ALLOWED", "ethics disabled")
        return True

    # Emergency mode
    if cfg["ethics"]["emergency_mode"]["active"]:
        audit_log("CHECK", entity_type, entity_name, "ALLOWED", f"EMERGENCY MODE: {cfg['ethics']['emergency_mode']['reason']}")
        return True

    name = entity_name.strip().split()[0] if entity_type == "manufacturer" else entity_name
    mode = cfg["ethics"].get("mode", "blacklist")

    # Manual bypass
    bypass_cfg = cfg["ethics"]["bypass"]
    if bypass_cfg["enabled"]:
        override_key = f"allow_{entity_type}_override"
        if bypass_cfg.get(override_key, False) and bypass_reason:
            audit_log("BYPASS", entity_type, entity_name, "ALLOWED", reason=bypass_reason)
            return True

    # Normal blade
    if mode == "blacklist":
        if name in BLACKLIST:
            audit_log("CHECK", entity_type, name, "BLOCKED", "in blacklist")
            if cfg["ethics"]["strict_mode"]:
                raise SystemExit(1)
            return False
        else:
            audit_log("CHECK", entity_type, name, "ALLOWED", "not blacklisted")
            return True

    elif mode == "whitelist":
        if name in WHITELIST:
            audit_log("CHECK", entity_type, name, "ALLOWED", "in Circle of Honor")
            return True
        else:
            audit_log("CHECK", entity_type, name, "REJECTED", "not in whitelist")
            if cfg["ethics"]["strict_mode"]:
                raise SystemExit(1)
            return False

# Final audit at end of bid
def finalize_audit(project_name: str, violations: int, overrides: int):
    status = "CLEAN" if violations == 0 and overrides == 0 else f"OVERRIDDEN ({overrides})" if overrides else f"VIOLATIONS ({violations})"
    audit_log("FINAL", "project", project_name, status)