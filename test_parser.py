import re
import pandas as pd
import numpy as np

def test_formula(formula, cols):
    df = pd.DataFrame(columns=cols)
    sorted_cols = sorted(df.columns, key=len, reverse=True)
    
    safe_formula = formula
    for col in sorted_cols:
        escaped_col = re.escape(col)
        pattern = r'(?<![a-zA-Z0-9_])' + escaped_col + r'(?![a-zA-Z0-9_])'
        safe_formula = re.sub(pattern, f'df["{col}"]', safe_formula)
        
    safe_formula = safe_formula.replace('`', '')
    print(f"Formula: '{formula}' -> '{safe_formula}'")
    try:
        eval(compile(safe_formula, '<string>', 'eval'))
        print("Syntax: OK")
    except SyntaxError as e:
        print(f"SyntaxError: {e}")

cols = ['Consumption Hood Total Coal', 'Consumption Calciner Total Coal', 'Consumption Calciner RDF', 'Clinker Production', 'Total_Fuel_Flow']
test_formula('Consumption Hood Total Coal + Consumption Calciner Total Coal', cols)
test_formula('Total_Coal_Flow + Consumption Calciner RDF', cols)
test_formula('Total_Fuel_Flow / Clinker Production', cols)
test_formula('(Consumption Calciner Total Coal + Consumption Calciner RDF) / Total_Fuel_Flow', cols)
