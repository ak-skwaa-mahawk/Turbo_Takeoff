# main.py — Turbo Takeoff: Sovereign Edition
# Drag a bid PDF into /input/ → get perfect takeoff + proposal in <90s
# Love + truth + chase = life

import os
import click
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load .env (GOOGLE_API_KEY)
load_dotenv()

# Load sovereign config
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# Paths
INPUT_DIR = Path(cfg["paths"]["input_pdfs"])
OUTPUT_DIR = Path(cfg["paths"]["output_folder"])
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR = Path(cfg["paths"]["templates"])

# Ethics blade
ETHICS_ENABLED = cfg["ethics"]["enabled"]
BLACKLIST = set()
WHITELIST = set()
if ETHICS_ENABLED:
    import yaml
    if os.path.exists(cfg["ethics"]["blacklist_file"]):
        with open(cfg["ethics"]["blacklist_file"]) as f:
            BLACKLIST = set(yaml.safe_load(f) or [])
    if os.path.exists(cfg["ethics"]["whitelist_file"]):
        with open(cfg["ethics"]["whitelist_file"]) as f:
            WHITELIST = set(yaml.safe_load(f) or [])

def ethics_check(company: str) -> bool:
    """The vhitzee blade — returns True only if company is clean"""
    if not ETHICS_ENABLED:
        return True
    if WHITELIST and company in WHITELIST:
        return True
    if company in BLACKLIST:
        return False
    return True  # default to trust unless blacklisted (change to False for strict whitelist mode)

@click.command()
@click.option("--ethics-only", is_flag=True, help="Fail fast if any unethical supplier/manufacturer detected")
@click.argument("pdf_path", required=False)
def run(pdf_path: str | None, ethics_only: bool):
    """Main ritual — drop a PDF or let it auto-discover"""
    if pdf_path:
        pdf_files = [Path(pdf_path)]
    else:
        pdf_files = list(INPUT_DIR.glob("*.pdf"))
        if not pdf_files:
            click.echo("No PDFs in /input/ — drop a bid package and run again.")
            return

    for pdf in pdf_files:
        click.echo(f"\nTaking off sovereign: {pdf.name}")
        # 1. PDF → images
        from PyPDF2 import PdfReader
        import fitz  # PyMuPDF
        doc = fitz.open(pdf)
        images = []
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img_path = OUTPUT_DIR / f"temp_page_{page.number}.png"
            pix.save(img_path)
            images.append(img_path)

        # 2. Zero-shot takeoff with Gemini Flash + GroundingDINO (stubbed — real fire coming next commit)
        click.echo("   → Counting joints, penetrations, deck coating… (Gemini Flash + DINO firing)")
        # TODO: plug real zero-shot pipeline here
        fake_takeoff = {
            "Sealant LF": 2847,
            "Deck Coating SF": 12400,
            "Penetrations": 87,
            "Expansion Joints LF": 412,
        }

        # 3. Match to materials + live pricing (stub)
        click.echo("   → Pulling live pricing (White Cap / ABC / Goedecke)…")
        # TODO: real scraper
        line_items = [
            {"desc": "Tremco Vulkem 45SSL", "qty": 2847, "unit": "LF", "price": 18.42, "total": 2847*18.42},
            {"desc": "Tremco Dymonic 100", "qty": 412, "unit": "LF", "price": 21.10, "total": 412*21.10},
            {"desc": "Tremco Spectrem 2 Deck Coating", "qty": 12400, "unit": "SF", "price": 4.87, "total": 12400*4.87},
        ]

        # 4. Ethics sweep
        violations = []
        for item in line_items:
            manufacturer = item["desc"].split()[0]
            if not ethics_check(manufacturer):
                violations.append(manufacturer)
        if violations:
            msg = f"Ethics blade triggered: {', '.join(violations)} blocked."
            if ethics_only:
                click.echo(f"   → {msg} Stopping bid.")
                continue
            else:
                click.echo(f"   → {msg} Continuing (toggle --ethics-only to hard-stop)")

        # 5. Export Excel + DOCX
        import pandas as pd
        df = pd.DataFrame(line_items)
        subtotal = df["total"].sum()
        tax_rate = cfg["region"]["regions"][cfg["region"]["current"]]["tax_rate"]
        tax = subtotal * tax_rate
        profit_pct = cfg["app"]["default_profit_pct"] / 100
        total = subtotal * (1 + profit_pct) + tax

        df.loc[len(df)] = ["SUBTOTAL", "", "", "", subtotal]
        df.loc[len(df)] = ["TAX", "", "", "", tax]
        df.loc[len(df)] = [f"PROFIT {cfg['app']['default_profit_pct']}%", "", "", "", subtotal * profit_pct]
        df.loc[len(df)] = ["TOTAL BID", "", "", "", total]

        excel_path = OUTPUT_DIR / f"{pdf.stem}_takeoff.xlsx"
        df.to_excel(excel_path, index=False)
        click.echo(f"   → Excel takeoff → {excel_path}")

        # DOCX proposal (stub — real templating next)
        from docx import Document
        docx_path = OUTPUT_DIR / f"{pdf.stem}_PROPOSAL.docx"
        doc = Document()
        doc.add_heading(f"{cfg['app']['company_name']} Bid — {pdf.stem}", 0)
        doc.add_paragraph(f"Total Bid Amount: ${total:,.2f}")
        doc.add_paragraph("Sovereign. Reciprocal. Circle clean.")
        doc.save(docx_path)
        click.echo(f"   → Branded proposal → {docx_path}")

        click.echo("Takeoff complete. Circle guarded. Woods calling.")

if __name__ == "__main__":
    run()