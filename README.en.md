# Company Website Data Extraction Tool

**Language:** [日本語](README.md) | English (this file) | [Tiếng Việt](README.vi.md)

Crawls the official websites of 10 listed companies by following links, and uses a generative AI (LLM) to extract the **head office address, representative name, capital, and date of establishment**. It uses no per-site selectors; a keyword-based link ranking handles every site generically.

For the technology comparison and the Task B findings, see [report.en.md](report.en.md).

## Requirements

- Python 3.9+
- An API key for one LLM provider (Gemini / OpenAI / Anthropic), or a local Ollama

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium        # fallback for JS-rendered sites
cp .env.example .env
```

Edit `.env` to set the model and API key.

```
LLM_MODEL=gemini/gemini-3.1-flash-lite
LLM_FALLBACK_MODEL=            # optional: used when the primary model fails
GEMINI_API_KEY=xxxxxxxx
```

Example `LLM_MODEL` values (litellm format): `gemini/gemini-3.1-flash-lite`, `gpt-4o-mini` (`OPENAI_API_KEY`), `anthropic/claude-3-5-haiku-latest` (`ANTHROPIC_API_KEY`), `ollama/llama3.1` (no key needed).

> [!NOTE]
> Models get retired. If you see a `404`, switch to a model name that is currently available from the provider.

## Usage

```bash
# All 10 companies (run via CLI)
python src/main.py

# One company (filter by part of the name)
python src/main.py --only サカタ

# Visit more pages per company (when fields are missing)
python src/main.py --max-pages 6
```

### Run via Web UI (Streamlit - Option A)
You can use the web interface (supports English, Vietnamese, and Japanese) to extract companies interactively:
```bash
streamlit run src/app.py
```
The UI will automatically open at `http://localhost:8501`.

### Run Option B (Next.js + Firecrawl + Vercel AI SDK)
This is a separate project in the `next-app` directory. You must configure `FIRECRAWL_API_KEY` and `GEMINI_API_KEY` in `next-app/.env.local`.
```bash
cd next-app
npm install
npm run dev
```
A beautifully designed modern UI will run at `http://localhost:3000`.

The input is `input/companies.csv` (`name,url`).

### Task B (Indeed investigation)

```bash
python src/indeed_probe.py
```

Sends one request per approach (4 in total) and saves the results to `result/indeed_probe.json` plus screenshots. The "headed" step opens a real Chrome window; leave it open until it finishes.

### Tests

```bash
python -m pytest -q tests
```

## Output

| File | Contents |
|---|---|
| `result/companies.csv` | Extracted data (UTF-8 with BOM for Excel) plus model, tokens, cost, seconds |
| `result/companies.json` | Same, plus visited URLs and evidence-check results |
| `result/run_log.json` | Run totals: tokens, cost, time, and the model that actually answered |
| `result/indeed_probe.json` | Task B experiment results |

## How it works

1. Collect links from the top page and, if needed, from sub-pages (subdomains of the same registered domain are included).
2. Rank links by keywords such as 会社概要, 企業情報, corporate, profile.
3. Clean the text of the top pages and have the LLM extract JSON (`null` when absent; no guessing).
4. Check that each quoted evidence snippet really appears in the page, and normalise the founding date to `YYYY-MM`.
5. If any field is still missing, fill it from the next candidate page.

## Directory layout

```
├── input/companies.csv   # target companies
├── prompts/              # history of prompts used with generative AI
├── result/               # extracted data
├── src/                  # source code
├── tests/                # unit tests
├── README.md             # Japanese (required by the assignment)
├── README.en.md / README.vi.md
└── report.md / report.en.md / report.vi.md
```

## Known limitations

- The Gemini free tier is rate-limited (e.g. 15 requests/min). A `429` can leave some fields empty; re-run just that company with `--only`.
- Capital is kept as written in the source (e.g. `30,685百万円`); it is not converted to a single numeric unit.
- Correctness against the official sites must be verified separately (Appendix A of [report.en.md](report.en.md)).
- Do not commit `.env` (already in `.gitignore`).
