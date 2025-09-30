from pathlib import Path
import pandas as pd
import shutil

def read_data(path: Path):
    if path.suffix == ".csv":
        return pd.read_csv(path)
    else:                       # Excel
        return pd.read_excel(path)

DATA_DIR   = Path("./iBRF/Imbalanced_datasets")          # CSV files
CSV_FILES  = sorted(DATA_DIR.glob("*.csv"))
assert CSV_FILES, "No CSV found"


for f in CSV_FILES:
    df = read_data(f)
    target_col = df.columns[-1]
    no_classes = df[target_col].nunique()
    if (no_classes > 2):
        shutil.move(f, DATA_DIR / "multiclass")
    else:
        shutil.move(f, DATA_DIR / "binary")
    # print(f.stem, no_classes)