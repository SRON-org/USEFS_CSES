import sys
sys.path.append('..') 
from ToUSEFS import convert_cses_to_usefs

try:
    # 转换为 YAML 格式
    convert_cses_to_usefs("cses.yaml", "usefs_from_cses.yaml")

    # 转换为 TOML 格式
    convert_cses_to_usefs("cses.yaml", "usefs_from_cses.toml")

    # 转换为 JSON 格式
    convert_cses_to_usefs("cses.yaml", "usefs_from_cses.json")

except ValueError as e:
    print(f"Conversion failed: {e}")