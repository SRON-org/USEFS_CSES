import argparse
import yaml
import cses_parser
import usefs_builder
from USEFS import USEFS_YamlParser, USEFS_TomlParser, USEFS_JsonParser, new  # 导入所有 parser
import os
from datetime import date

def convert_cses_to_usefs(cses_file: str, usefs_file: str, from_date: str = None,
                         usefs_format: str = "yaml"):
    """
    Converts a CSES file to a USEFS file.

    Args:
        cses_file (str): Path to the CSES file.
        usefs_file (str): Path to the output USEFS file.
        from_date (str, optional): Start date for the schedule (YYYY-MM-DD). Defaults to None (auto-detect).
        usefs_format (str, optional): Format for the USEFS file (yaml, toml, json). Defaults to "yaml".
    """
    try:
        # 1. 自动检测开学日期
        if from_date is None:
            from_date = _auto_detect_from_date()

        # 2. 根据 CSES 文件后缀推断 CSES 格式
        _, cses_ext = os.path.splitext(cses_file)
        cses_format = cses_ext[1:].lower()
        if cses_format not in ("yaml", "toml", "json"):
            raise ValueError(
                "Invalid CSES file format. File extension must be yaml, toml, or json.")

        # 3. 解析 CSES 文件 # 3. 解析 CSES 文件
        cses_data = cses_parser.parse_cses_file(cses_file)

        # 4. 构建 USEFS 数据
        usefs_data = usefs_builder.build_usefs_data(cses_data, from_date)

        # 5. 创建一个新的 USEFS 文件
        # 根据 usefs_file 的后缀来决定新建文件的格式
        _, usefs_ext = os.path.splitext(usefs_file)
        target_usefs_format = usefs_ext[1:].lower()
        if target_usefs_format not in ("yaml", "toml", "json"):
            raise ValueError(
                "Invalid USEFS file format. File extension must be yaml, toml, or json.")

        new_usefs_file = new(usefs_file)

        # 6. 根据 USEFS 目标文件格式选择对应的 Parser 并加载文件
        if target_usefs_format == "yaml":
            usefs_parser = USEFS_YamlParser(new_usefs_file)
        elif target_usefs_format == "toml":
            usefs_parser = USEFS_TomlParser(new_usefs_file)
        elif target_usefs_format == "json":
            usefs_parser = USEFS_JsonParser(new_usefs_file)
        else:
            raise ValueError("Invalid USEFS format. Must be yaml, toml, or json.")

        # 7. 设置 data 和相关属性
        usefs_parser.data = usefs_data
        usefs_parser.version = usefs_data['version']
        usefs_parser.items = usefs_data['items']
        usefs_parser.collections = usefs_data['collections']

        # 8. 保存文件
        usefs_parser.save_to_file(new_usefs_file)

        print(f"Successfully converted {cses_file} to {usefs_file} in {target_usefs_format} format.")

    except ValueError as e:
        raise  # 重新抛出，让调用者处理
    except Exception as e:
        raise  # 重新抛出，让调用者处理


def _auto_detect_from_date() -> str:
    """
    Automatically detects the 'from_date' based on the current date.
    """
    today = date.today()
    current_year = today.year

    september_first = date(current_year, 9, 1)

    if today < september_first:
        # 今年还没有到 9 月 1 日，使用去年的 9 月 1 日
        from_date = date(current_year - 1, 9, 1).strftime("%Y-%m-%d")
    else:
        # 今年已经过了 9 月 1 日，使用今年的 9 月 1 日
        from_date = september_first.strftime("%Y-%m-%d")

    return from_date

def main():
    parser = argparse.ArgumentParser(description="Convert CSES format to USEFS format.")
    parser.add_argument("cses_file", help="Path to the CSES file.")
    parser.add_argument("usefs_file", help="Path to the output USEFS file.")
    parser.add_argument("--from_date", help="Start date for the schedule (YYYY-MM-DD)", default=None) # 允许为空
    args = parser.parse_args()

    try:
        # 现在 `convert_cses_to_usefs` 函数根据输出文件扩展名确定 USEFS 格式
        convert_cses_to_usefs(args.cses_file, args.usefs_file, args.from_date)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()