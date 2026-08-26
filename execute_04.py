import sys
import os
import hashlib
import ast
import subprocess

REPO = r'c:\Users\User10\Documents\MRV\yuvi\QuantForge'
script_path = os.path.join(REPO, 'output', 'research_discovery', 'H01_EQUITY_VOLATILITY_ASYMMETRY', 'run_h01_equity_v1.py')
sys.path.append(os.path.dirname(script_path))
import run_h01_equity_v1

print("--- Pre-Launch Assertions ---")
# 1. Protocol/runtime
assert run_h01_equity_v1.PROTOCOL_VERSION == '1.3.0', "PROTOCOL_VERSION != 1.3.0"
print("1. Protocol/runtime: PASS")

# 2. Universe
assert run_h01_equity_v1.CELLS[0][0] == 'EQBROAD_L1', "Cell 0 not EQBROAD_L1"
assert run_h01_equity_v1.CELLS[0][3] == [('sp', 'HPD'), ('NYA', 'HTML')], "EQBROAD_L1 markets != sp, NYA"
assert run_h01_equity_v1.CELLS[1] == ('EQBROAD_L2', 'CONTEMPORARY', 'broad', [('SP500', 'FRED'), ('DJIA', 'FRED')]), "EQBROAD_L2 changed"
assert run_h01_equity_v1.CELLS[2] == ('EQTECH_L1', 'HISTORICAL', 'tech', [('NASDAQ100', 'FRED'), ('NASDAQCOM', 'FRED')]), "EQTECH_L1 changed"
assert run_h01_equity_v1.CELLS[3] == ('EQTECH_L2', 'CONTEMPORARY', 'tech', [('NASDAQ100', 'FRED'), ('NASDAQCOM', 'FRED')]), "EQTECH_L2 changed"
print("2. Universe: PASS")

# 3. NYA Preflight
nya_win = ('1982-04-21', '2002-10-01')
nya_data = run_h01_equity_v1.load_nya(nya_win)
assert nya_data['n_rows'] == 5163, f"NYA row count = {nya_data['n_rows']}"
assert nya_data['dates'][0] == '1982-04-21', "NYA first date wrong"
assert nya_data['dates'][-1] == '2002-09-30', "NYA last date wrong"
assert all(c > 0 for c in nya_data['closes']), "NYA has nonpositive closes"
print("3. NYA Preflight: PASS")

# 4. Source Identity
expected_shas = {
    'sp_historical.csv': 'dd35661826279d786c3acec08446e7f0c99137b6a349ad367461851b61148bd8',
    'NYA_DATA.html': '367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f',
    'fred_SP500.csv': '4b6c37f3477a4f3454009e500eb1b4d7844b38b0aaad10097b5fe6a5f8ae0db7',
    'fred_DJIA.csv': '6a274816b3ed64956346c10dc8decb5eb585155ac16af410cd2306048d290ee2',
    'fred_NASDAQCOM.csv': '377af7dec4b1a01486cc9e2db48fbe0538e024d58ed258eedbd01e98494358d6',
    'fred_NASDAQ100.csv': '1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f'
}
assert run_h01_equity_v1.FINGERPRINTS == expected_shas, "FINGERPRINTS mismatch"
print("4. Source Identity: PASS")

# 5. Validation Artifact
val_path = os.path.join(REPO, 'data', 'PER_MARKET_VALIDATION.csv')
assert os.path.exists(val_path), "PER_MARKET_VALIDATION.csv missing"
print("5. Validation Artifact: PASS")

# 6. No legacy dependency
with open(script_path, 'r', encoding='utf-8') as f:
    src_code = f.read()

tree = ast.parse(src_code)
class StringLiteralChecker(ast.NodeVisitor):
    def __init__(self):
        self.found = False
    def visit_Str(self, node):
        if 'front_sp.csv' in node.s:
            self.found = True
        self.generic_visit(node)
    def visit_Constant(self, node):
        if isinstance(node.value, str) and 'front_sp.csv' in node.value:
            self.found = True
        self.generic_visit(node)
    def visit_Expr(self, node):
        # Ignore top level docstrings or class/function docstrings
        # AST represents docstrings as Expr(Constant(str)) as the first stmt
        pass # To be safe we'll just check all constants except docstrings, but actually
             # we can just use ast.walk and skip docstrings

checker = StringLiteralChecker()
# A simpler way: collect all active strings in the AST
def get_active_strings(node):
    strings = []
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
        # skip docstring
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, (ast.Str, ast.Constant)):
            body = body[1:]
        for stmt in body:
            strings.extend(get_active_strings(stmt))
    elif isinstance(node, ast.AST):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.append(node.value)
        elif isinstance(node, ast.Str): # Python < 3.8
            strings.append(node.s)
        for child in ast.iter_child_nodes(node):
            strings.extend(get_active_strings(child))
    return strings

active_strings = get_active_strings(tree)
assert not any('front_sp.csv' in s for s in active_strings), "Executable front_sp.csv string found"

print("6. No legacy dependency: PASS")
print("ALL PRE-FLIGHT ASSERTIONS PASSED")
