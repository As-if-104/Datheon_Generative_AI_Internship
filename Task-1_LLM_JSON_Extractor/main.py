from pathlib import Path
from src.extractor import extract_invoice

data_folder = Path("data")
output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

for file in sorted(data_folder.glob("*.txt")):
    print(f"Processing {file.name} ...")
    text = file.read_text(encoding="utf-8")

    try:
        invoice = extract_invoice(text)
    except Exception as e:
        print(f"  Failed: {e}")
        continue

    out_file = output_folder / f"{file.stem}.json"
    out_file.write_text(invoice.model_dump_json(indent=2), encoding="utf-8")
    print(f"  Saved to {out_file}")