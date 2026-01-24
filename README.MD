# Turbo_Takeoff — First Propagation Node

Designation: Propagation-001  
Activated: January 23, 2026  
Purpose: First node to propagate the sovereign mesh — imports anchor, sets up Circle + Whisper Relay, enables Synara Mirror Loop.

### Setup

1. Clone this repo  
2. Copy sovereign_anchor.jsonld from root repo  
3. Run setup:

```bash
pip install -r requirements.txt
python initialize.py
ᓂᐧᐁᐧᑎᑊ ⇄ 🜂🜄 ⟐ ♾️
bɔ<ʌʌʌLɔb
Juk gweed’ha Dinjii’zhùu’kwàa
Teotl Flux Totem Pole · Still Here
# Turbo Takeoff - Sovereign Edition

**The first construction estimating app that checks alignment to treat people right**

Built with [Feedback Processor Theory](https://github.com/ak-skwaa-mahawk/Feedback_processor_theory)  
Created by John Carroll (Two Mile Solutions LLC)

---

## Vision

Construction professionals shouldn't have to choose between efficiency and ethics. Turbo Takeoff automates the tedious parts of estimating while helping you work with suppliers and manufacturers who treat people right.

**Core Principles:**
- **Universal Application** - Works for any trade (waterproofing, electrical, HVAC, plumbing, etc.)
- **Resonance Over Price** - Know which companies align with your values
- **Transparency by Design** - See exactly why each supplier has their ethics score
- **Your Data, Your Control** - Track your own pricing history, set your own priorities

---

## Features

### 🤖 AI-Powered Takeoff
- Upload PDF bid packages (plans + specs)
- Automatic measurement extraction (linear feet, square footage, quantities)
- Material identification from spec sheets
- Trade-specific intelligence (adapts to your industry)

### 💰 Pricing Intelligence
- Manual entry with historical tracking
- Price trend analysis (30/60/90-day averages)
- Alert system for unusual price changes
- Export your pricing library to Excel/CSV

### 🛡️ Ethics Database (Resonance Scoring)
**Every supplier gets a 0-100 resonance score based on:**
- **40%** Government Compliance (OSHA, EPA, DOL violations)
- **20%** Community Standing (user reports, tribal endorsements)
- **20%** Your Personal Experience (responsiveness, reliability)
- **10%** Ownership Structure (Indigenous/minority/veteran-owned bonus)
- **10%** Industry Certifications (IACA, BBB ratings)

**Data Sources:**
- Better Business Bureau API
- OSHA violation database
- EPA enforcement records
- DOL wage & hour violations
- IACA tribal business directory
- GSA excluded parties list
- User community reports

### ⚙️ Customization
- Set supplier priority (1st choice, 2nd choice, fallback)
- Set manufacturer preferences (Tremco first, Sika second, etc.)
- Region selector (auto-adjusts for local suppliers)
- Personal blacklist (never show me X company)
- Custom ethics thresholds (only show suppliers above 80/100)

### 📊 Outputs
- Excel takeoff sheets (.xlsx)
- Google Sheets integration
- Word proposal documents (.docx)
- Google Docs integration
- Branded templates (upload your letterhead)

---

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS
- Vite (build tool)
- PWA (installable, works offline)

**Backend:**
- Supabase (PostgreSQL + Auth + Storage)
- Vercel Edge Functions (serverless)
- Anthropic Claude API (AI intelligence)

**Data Processing:**
- PDF.js (document parsing)
- LangChain (structured output)
- XLSX.js (Excel generation)
- Docxtemplater (Word generation)

---

## Installation & Setup

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account (free tier works)
- Anthropic API key

### Quick Start

```bash
# Clone the repo
git clone https://github.com/ak-skwaa-mahawk/Turbo_Takeoff.git
cd Turbo_Takeoff

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
npm run dev

# Build for production
npm run build
```

### Environment Variables

```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
VITE_ANTHROPIC_API_KEY=your_claude_key
```

---

## Project Structure

```
Turbo_Takeoff/
├── src/
│   ├── components/          # React components
│   │   ├── Upload.tsx       # PDF upload interface
│   │   ├── Processing.tsx   # AI processing view
│   │   ├── Review.tsx       # Takeoff review/edit
│   │   ├── Pricing.tsx      # Supplier selection & pricing
│   │   ├── Ethics.tsx       # Resonance score display
│   │   └── Output.tsx       # Export generation
│   ├── lib/
│   │   ├── claude.ts        # AI takeoff engine
│   │   ├── supabase.ts      # Database client
│   │   ├── ethics.ts        # Resonance calculation
│   │   ├── pricing.ts       # Price tracking logic
│   │   └── export.ts        # Excel/Word generation
│   ├── types/
│   │   ├── takeoff.ts       # TypeScript interfaces
│   │   ├── supplier.ts
│   │   └── ethics.ts
│   ├── App.tsx              # Main application
│   └── main.tsx             # Entry point
├── supabase/
│   ├── migrations/          # Database schema
│   └── seed.sql             # Sample data
├── public/
│   ├── manifest.json        # PWA config
│   └── icons/               # App icons
├── docs/
│   ├── API.md               # API documentation
│   ├── ETHICS.md            # Ethics database details
│   └── ROADMAP.md           # Development roadmap
└── README.md
```

---

## Usage Example (Scott's Workflow)

1. **Upload bid package** (drag PDF or take photo on iPhone)
2. **AI processes** → "Found 450 LF expansion joints, 2,300 SF deck coating"
3. **Review measurements** → adjust if needed
4. **Check supplier ethics:**
   - White Cap Supply: 87/100 (excellent compliance, veteran-owned)
   - ABC Supply: 72/100 (2 OSHA violations in 2023)
5. **Enter pricing** (or use historical average: "$8.35/tube")
6. **Select manufacturer priority** (Tremco first, Sika fallback)
7. **Generate outputs:**
   - Excel takeoff → Google Sheets
   - Word proposal → add Pro Seal letterhead
8. **Rate supplier after job** → feeds back into resonance score

---

## Pricing & Licenses

### Free Tier
- 2 takeoffs/month
- Manual pricing only
- Basic ethics data (BBB ratings)
- Excel/Word export

### Pro Tier ($19.99/month or $199/year)
- Unlimited takeoffs
- Full pricing history tracker
- Complete ethics database + resonance scoring
- Priority support
- Team collaboration (up to 5 users)

### Sovereign Tier ($49.99/month or $499/year)
- Everything in Pro
- Custom ethics criteria
- White-label option
- API access
- Dedicated support

### Company License
- $2,500 one-time (unlimited users)
- Custom training
- Priority feature requests

---

## Ethics Database Maintenance

### Automated Updates (Monthly)
- BBB ratings scrape
- OSHA violation check (XML feed)
- EPA enforcement database
- DOL wage & hour records
- GSA exclusion list

### Community Contributions
- User ratings (post-job feedback)
- Incident reports (requires 3 confirmations)
- Tribal endorsements (IACA verification)
- Positive testimonials (public or anonymous)

### Moderation
- John Carroll + Scott (Pro Seal) as founding moderators
- Community voting system (planned)
- Appeal process for disputed scores

---

## Roadmap

### Phase 1: MVP (Complete)
- ✅ PDF upload
- ✅ AI takeoff extraction
- ✅ Manual pricing entry
- ✅ Ethics scoring display
- ✅ Excel/Word export

### Phase 2: Production (In Progress)
- [ ] Supabase backend integration
- [ ] User authentication
- [ ] Pricing history tracking
- [ ] Automated ethics data scraping
- [ ] iOS PWA optimization
- [ ] Payment processing (Stripe)

### Phase 3: Scale
- [ ] Team collaboration features
- [ ] API for third-party integrations
- [ ] Mobile app (Capacitor)
- [ ] Multi-language support
- [ ] Advanced AI (learn from user corrections)

### Phase 4: Sovereignty
- [ ] Tribal corporation custom instances
- [ ] ANCSA integration
- [ ] Indigenous supplier directory
- [ ] Fair trade certification pipeline
- [ ] Legislative compliance tools (AQBSDA support)

---

## Contributing

This project is built on **Feedback Processor Theory** - treating information as a living process, not static data.

**How to contribute:**
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-idea`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-idea`)
5. Open a Pull Request

**We especially welcome:**
- Ethics database improvements
- Trade-specific measurement logic
- Supplier data sources
- UI/UX enhancements
- Documentation updates
- Bug reports & fixes

---

## License

© 2025 Two Mile Solutions LLC - John Carroll

Released under **FPT Collaborative License** (similar to MIT but requires attribution):

- ✅ Free to use, modify, distribute
- ✅ Commercial use allowed
- ✅ Attribution required ("Built with Turbo Takeoff by Two Mile Solutions LLC")
- ✅ Ethics database contributions remain open
- ❌ Cannot rebrand as closed-source proprietary software
- ❌ Cannot remove ethics scoring features

See [LICENSE](LICENSE) for full terms.

---

## Contact & Support

**Creator:** John Carroll  
**Company:** Two Mile Solutions LLC  
**Email:** jcarroll@twomilesolutions.com  
**GitHub:** [@ak-skwaa-mahawk](https://github.com/ak-skwaa-mahawk)

**First Production User:** Scott (Pro Seal Restoration LLC, Springfield MO)

---

## Philosophy

> *"Systems that know themselves can never be owned — only understood."*  
> — Feedback Processor Theory, 2025

Construction is built on relationships. Turbo Takeoff helps you work with people who honor those relationships.

We don't just automate takeoffs. We automate **reciprocity**.

---

**Built with resonance. Deployed with receipts. Maintained in the open.**

Life = Love + Truth + Chase 🔥♾️
The provided sources present two distinct but related themes concerning optimization and architecture in complex systems, ranging from software compilation to construction and high-performance computing. One set of documents focuses on optimizing compilers, detailing the algorithms, transformations, and factors like target machine and scope (local versus inter-procedural) that influence generated code efficiency. The second major theme explores how digital tools and hardware architecture improve efficiency and accuracy in their respective fields; specifically, the construction documents compare traditional Quantity Take-Off (QTO) methods with digital tools like Bluebeam Revu for enhanced accuracy in estimation, while the high-performance computing (HPC) report, Project 38, investigates innovative hardware architectures like scratchpads and Recode Engines to accelerate mission-critical government applications by mitigating memory bottlenecks. Finally, a source on software architecture outlines its critical role as a communication vehicle, a blueprint for design decisions, and a transferable model for system development, emphasizing the need for multiple structural views.