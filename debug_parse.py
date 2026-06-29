import sys
sys.path.insert(0, 'backend')
import importlib, data_processor
importlib.reload(data_processor)
from data_processor import load_data

with open(r'C:\Users\ranja\projects\projects office\EDA\VOLT\2026-01-15_2026-05-15_1m1.csv', 'rb') as f:
    content = f.read()

df = load_data(content, '2026-01-15_2026-05-15_1m1.csv')
print(f"Rows: {len(df)}, Cols: {len(df.columns)}")
print()
print("First 6 columns (should all have real values now):")
for c in df.columns[:6]:
    nan_count = df[c].isna().sum()
    zero_count = (df[c] == 0).sum() if c != 'timestamp' else 0
    first_val = df[c].iloc[0]
    nonzero_pct = 0
    if c != 'timestamp':
        nonzero_count = ((df[c] != 0) & (df[c].notna())).sum()
        nonzero_pct = round(nonzero_count / len(df) * 100, 1)
    print(f"  {c}: NaN={nan_count}, zeros={zero_count}, nonzero%={nonzero_pct}%, first={first_val}")
