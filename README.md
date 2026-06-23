# Sentiment Classifier

A lightweight Python tool that classifies text as **positive**, **negative**, or **neutral** using the [Anthropic Claude API](https://www.anthropic.com). Designed for batch processing CSV files.

---

## Project Structure

```
sentiment-classifier/
├── classifier.py      # Core classification logic (reusable module)
├── run.py             # CLI runner for batch CSV processing
├── sample_data.csv    # Example input file
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # You are here
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/sentiment-classifier.git
cd sentiment-classifier
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."     # macOS/Linux
set ANTHROPIC_API_KEY=sk-ant-...          # Windows CMD
$env:ANTHROPIC_API_KEY="sk-ant-..."       # Windows PowerShell
```

> Never commit your API key. The `.gitignore` excludes `.env` files.

---

## Usage

### Classify a CSV file

```bash
python run.py --input sample_data.csv --text-col text --output results.csv
```

| Argument | Default | Description |
|---|---|---|
| `--input` | *(required)* | Path to your input CSV |
| `--text-col` | `text` | Column name containing the text to classify |
| `--output` | `results.csv` | Where to save results |
| `--delay` | `0.2` | Seconds between API calls (rate limiting) |

### Use as a Python module

```python
from classifier import classify_text, classify_batch

# Single text
result = classify_text("I love this product!")
print(result)
# {'sentiment': 'positive', 'confidence': 0.97, 'reason': 'Strong positive language used.'}

# Batch
results = classify_batch(["Great!", "Terrible.", "It arrived."])
for r in results:
    print(r["sentiment"], r["confidence"])
```

---

## Output Format

The output CSV contains all original columns plus three new ones:

| Column | Description |
|---|---|
| `sentiment` | `positive`, `negative`, or `neutral` |
| `confidence` | Float from 0.0 to 1.0 |
| `reason` | One-sentence explanation |

---

## Customisation

- **Change the model**: Edit `classifier.py` and swap `claude-haiku-4-5-20251001` for another Claude model.
- **Change labels**: Edit `SYSTEM_PROMPT` in `classifier.py` to use your own categories (e.g. `urgent`, `not urgent`).
- **Add more columns**: Extend the `result` dict in `classify_text()` to return extra fields.

---

## Pushing to GitHub

```bash
git init
git add .
git commit -m "Initial commit: sentiment classifier"
git remote add origin https://github.com/YOUR_USERNAME/sentiment-classifier.git
git push -u origin main
```

---

## License

MIT
