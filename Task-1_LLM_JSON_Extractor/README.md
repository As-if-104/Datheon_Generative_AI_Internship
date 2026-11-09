# Task 1: Structured LLM Prompt Pipeline & JSON Extractor

## Goal
Extract structured data from unstructured invoice text using the Google Gemini API, and make sure the result is valid JSON by checking it with Pydantic.

## How it works
```
Invoice text (.txt) -> Prompt template -> Gemini API -> JSON reply -> Pydantic validation -> Saved JSON file
```

1. `main.py` reads every `.txt` file from the `data/` folder.
2. `src/prompts.py` fills a prompt template with the invoice text. The prompt contains the required JSON format and one few-shot example.
3. `src/extractor.py` sends the prompt to Gemini and asks for a JSON-only reply. It retries automatically if the server is busy (503 error).
4. `src/schema.py` defines the Pydantic models (`Invoice` and `LineItem`). The reply is validated against them, so wrong or missing fields raise an error.
5. Valid results are saved as JSON files in `output/`.

## Project structure
```
Task-1_LLM_JSON_Extractor/
├── data/              # 5 sample invoices (unstructured text)
├── src/
│   ├── prompts.py     # prompt template + few-shot example
│   ├── schema.py      # Pydantic models
│   └── extractor.py   # Gemini API call + validation
├── output/            # extracted JSON results
├── main.py            # runs the pipeline
├── .env               # API key (not uploaded to GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup
1. Create and activate a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
3. Get a free API key from Google AI Studio and create a `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Run:
   ```
   python main.py
   ```

## Sample data
Five invoices were written in different styles to test the pipeline:

| File | Style |
|---|---|
| `invoice_1.txt` | Casual message from a vendor |
| `invoice_2.txt` | Formal invoice with an item list |
| `invoice_3.txt` | Customer thank-you email |
| `invoice_4.txt` | Tax invoice with a day-month-year date (`02-11-2026`) |
| `invoice_5.txt` | Very short, informal lowercase message |

## Example
**Input** (`data/invoice_1.txt`)
```
Hi, this is Rahim from ABC Traders. Invoice #1042 dated 5 Nov 2026.
You bought 3 laptops at $500 each and 2 mice at $10 each.
Total amount due is $1,520.
```

**Output** (`output/invoice_1.json`)
```json
{
  "vendor": "ABC Traders",
  "invoice_number": "1042",
  "date": "2026-11-05",
  "items": [
    {"description": "laptops", "quantity": 3, "unit_price": 500.0},
    {"description": "mice", "quantity": 2, "unit_price": 10.0}
  ],
  "total": 1520.0
}
```

## Results
All 5 sample invoices were processed and saved as valid JSON in `output/`. Vendor names, invoice numbers, items and totals were checked by hand against the source text, and the item prices add up to each invoice total. Dates were converted to `YYYY-MM-DD` format.

## Notes
- Model used: `gemini-3.5-flash-lite`. The model name is set in one place (`MODEL` in `src/extractor.py`) because Google renames models often.
- Some models returned 503 "high demand" errors, so a retry loop was added.
- Switching to a lighter "flash-lite" model solved the overload problem and works well for this simple extraction task.
- The Pydantic schema checks field names and types. It does not check that the total equals the sum of the items.

## Possible improvements
- Add a check that the total matches the sum of the items.
- Add a second use case, such as resume parsing.