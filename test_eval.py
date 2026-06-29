import pandas as pd
import re

df = pd.DataFrame({'a b': [1, 2], 'c d': [3, 4]})
formula='(a b + c d) / a b'
sorted_cols = sorted(df.columns, key=len, reverse=True)
safe_formula = formula
for col in sorted_cols:
    safe_formula = re.sub(r'(?<![a-zA-Z0-9_])' + re.escape(col) + r'(?![a-zA-Z0-9_])', f'df["{col}"]', safe_formula)
print("Safe formula:", safe_formula)
df['res'] = eval(safe_formula)
print("Result:\n", df['res'])
