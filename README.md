# India Jobs Market Visualizer 🇮🇳

A production-grade, Karpathy-style interactive treemap for India’s 2024–2025 tech job market.

Inspired by Andrej Karpathy’s [`karpathy/jobs`](https://github.com/karpathy/jobs) and the live US visualizer at <https://karpathy.ai/jobs/>. This version retargets the concept to India using a curated, auditable static dataset covering AI/ML demand, GCC growth, salaries, city concentration, remote readiness, and AI exposure.

## What it visualizes

- **Area** = approximate role demand / workforce weight
- **Color layer** = selectable metric:
  - AI Exposure
  - Hiring Growth
  - Salary
  - Demand Score
  - Remote Readiness
- **Hover tooltip** = role, category, city hubs, salary, growth, exposure rationale, and skills
- **Side ranking** = top roles for the selected metric
- **City panel** = Bengaluru, Hyderabad, Pune, Chennai, NCR, Mumbai and Tier-2 hub concentration
- **JobSpeak panel** = monthly 2025 hiring pulse

## Production features

- Static GitHub Pages-ready site
- No build step required
- No framework or runtime dependency
- CDN-free and tracking-free
- Responsive layout for desktop and mobile
- Accessible controls using native inputs
- Data isolated in `site/data.json`
- Single-file frontend in `site/index.html`

## Run locally

```bash
cd site
python -m http.server 8000
# open http://localhost:8000
```

## Deploy on GitHub Pages

1. Open repository **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`
4. Folder: `/site`
5. Save

Your visualizer will be served from the GitHub Pages URL for this repository.

## Repository structure

```text
site/
├── index.html   # Production static app
└── data.json    # India jobs market dataset
README.md
```

## Dataset methodology

This visualizer uses a curated market-intelligence dataset derived from the provided research brief and public labour-market signals. The role records include approximate demand weights, salary bands in INR LPA, 2025 hiring growth, heuristic demand score, remote readiness, AI exposure score, core city hubs, and skill tags.

The AI exposure score follows the spirit of the Karpathy rubric: digital, computer-mediated work scores higher because current AI systems act most directly on text, code, analysis, design and communication. A high exposure score means **AI will reshape the work**, not that the role will disappear.

## India context represented

- FY2025 tech industry revenue: about **$282.6B**
- FY2025 tech workforce: about **5.8M**
- FY2025 net new hires: about **126K**
- GCC workforce: about **2.4M**
- GCC centers: **1,700+**
- AI/ML hiring: recurring **25–54% YoY** growth signals in 2025
- Major hiring hubs: Bengaluru, Hyderabad, Pune, Chennai, Delhi NCR, Mumbai, and Tier-2 expansion cities

## Caveats

This is not an official economic forecast. It is a visual exploration tool, similar in spirit to the original Karpathy project. The numbers are approximate and intended for comparative visualization, not payroll planning, investment decisions, or policy conclusions.

## Credits

- Original concept: [Andrej Karpathy / jobs](https://github.com/karpathy/jobs)
- India market research: uploaded project brief covering NASSCOM, Naukri JobSpeak, GCC reports, salary guides, and AI workforce disruption context

## License

MIT
