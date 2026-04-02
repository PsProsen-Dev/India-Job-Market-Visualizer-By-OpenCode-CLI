# India Job Market Visualizer

A research tool that visualizes Indian occupations from PLFS (Periodic Labour Force Survey) data. Inspired by [Karpathy's US Job Market Visualizer](https://karpathy.ai/jobs/).

## About

This tool visualizes **occupations** from India's labour market data:
- Data source: PLFS (Periodic Labour Force Survey) from MOSPI
- Occupation codes: NCO 2015 (National Classification of Occupations)
- Metrics: Employment count, salary, growth outlook, education, AI exposure

## Features

- **Treemap Visualization**: Rectangle area proportional to employment
- **Color Layers**: Toggle between Growth Outlook, Median Salary, Education, AI Exposure
- **AI Exposure Scoring**: LLM-powered analysis for each occupation (adapted for India context)
- **Interactive**: Hover for details, click for more info

## Quick Start

### Prerequisites
- Python 3.9+
- OpenRouter API key (for AI scoring) - optional, fallback scoring available

### Installation

```bash
# Clone the repo
git clone https://github.com/PsProsen-Dev/India-Job-Market-Visualizer-By-OpenCode-CLI
cd India-Job-Market-Visualizer-By-OpenCode-CLI

# Install dependencies
pip install pandas numpy httpx python-dotenv
```

### Generate Data

1. **Aggregate PLFS data** (if you have raw data):
```bash
python scripts/aggregate_plfs.py
```

2. **Score AI exposure** (optional - fallback available):
```bash
# Create .env file with your API key
echo "OPENROUTER_API_KEY=your_key_here" > .env
python scripts/score.py

# OR use fallback scoring (no API needed)
python scripts/score_fallback.py
```

3. **Build site data**:
```bash
python scripts/build_site_data.py
```

### View Locally

```bash
cd site
python -m http.server 8000
# Open http://localhost:8000
```

## File Structure

```
India-Job-Market-Visualizer-By-OpenCode-CLI/
├── scripts/
│   ├── nco_mapping.py       # NCO 2015 occupation codes
│   ├── aggregate_plfs.py    # Aggregate PLFS data to occupations
│   ├── score.py             # AI exposure scoring (LLM)
│   ├── score_fallback.py    # AI exposure scoring (fallback)
│   └── build_site_data.py   # Build data.json for visualization
├── data/
│   ├── india_occupations_stats.json   # Full occupation statistics
│   ├── occupations.json               # Occupation list
│   ├── occupations.csv                 # CSV with metrics
│   └── india_scores.json              # AI exposure scores
├── site/
│   ├── index.html          # Main visualization (treemap)
│   └── data.json           # Compact data for frontend
├── README.md
└── .env.example             # Environment variables template
```

## Data Pipeline

1. **PLFS Raw Data** → Aggregate by NCO code → `india_occupations_stats.json`
2. **Scoring** → LLM analysis or fallback heuristics → `india_scores.json`
3. **Build** → Merge stats + scores → `site/data.json`
4. **Visualize** → Treemap in browser

## Technologies

- **Frontend**: Pure HTML/JS (no framework)
- **Backend**: Python scripts for data processing
- **AI**: OpenRouter API (Gemini Flash) for scoring (optional)
- **Data**: PLFS survey micro-data

## India-Specific Considerations

- Uses NCO 2015 occupation codes (not SOC like US)
- Salary in INR (₹) per month
- Categories: Professionals, Technicians, Service Workers, Agriculture, etc.
- Female workforce percentage included
- Urban/Rural distribution

## Known Limitations

- PLFS data may have sampling limitations
- AI exposure scores are rough estimates (LLM or heuristics)
- Occupation descriptions are basic (no detailed scraping)
- Growth outlook is estimated based on category trends

## Credits

- Inspired by [Andrej Karpathy](https://karpathy.ai/) and his [US Job Market Visualizer](https://karpathy.ai/jobs/)
- Data from [MOSPI](https://www.mospi.gov.in/) PLFS survey
- Occupation codes from [NCO 2015](https://dge.gov.in/dge/hi/nco-2015)

## License

MIT License - Feel free to use and modify!