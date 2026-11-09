PROMPT_TEMPLATE = """You are an invoice data extraction assistant.
Read the invoice text and return ONLY valid JSON, with no extra words.

Use exactly this format:
{
  "vendor": "string",
  "invoice_number": "string",
  "date": "YYYY-MM-DD",
  "items": [
    {"description": "string", "quantity": 1, "unit_price": 0.0}
  ],
  "total": 0.0
}

Example input:
Hello, Sam's Bakery here. Invoice 77 from 2 January 2026. 4 cakes at $12 each. Total $48.

Example output:
{"vendor": "Sam's Bakery", "invoice_number": "77", "date": "2026-01-02", "items": [{"description": "cakes", "quantity": 4, "unit_price": 12.0}], "total": 48.0}

Now extract the data from this invoice:
{document_text}
"""


def build_prompt(text):
    # We use replace() because the JSON above contains curly braces,
    # which would confuse Python's .format()
    return PROMPT_TEMPLATE.replace("{document_text}", text)