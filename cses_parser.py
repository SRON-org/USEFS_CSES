import yaml
import toml
import json
import os

def parse_cses_file(file_path: str) -> dict:
    """
    Parses a CSES file and returns a dictionary representing the data.
    """
    try:
        # 根据文件后缀判断格式
        _, ext = os.path.splitext(file_path)
        file_format = ext[1:].lower()

        with open(file_path, "r", encoding="utf-8") as f:
            if file_format == "yaml" or file_format == "yml":
                data = yaml.safe_load(f)
            elif file_format == "toml":
                data = toml.load(f)
            elif file_format == "json":
                data = json.load(f)
            else:
                raise ValueError("Invalid CSES file format: File extension must be yaml, toml, or json.")

        # CSES 数据校验
        if not isinstance(data, dict):
            raise ValueError("Invalid CSES file format: Root element must be a dictionary.")

        if 'version' not in data or 'subjects' not in data or 'schedules' not in data:
            raise ValueError("Invalid CSES file format: Missing 'version', 'subjects', or 'schedules' keys.")

        if data['version'] != 1:
            raise ValueError("Invalid CSES version.  Only version 1 is supported.")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"CSES file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse CSES file: {e}") from e
    except toml.TomlDecodeError as e:
        raise ValueError(f"Failed to parse CSES file: {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse CSES file: {e}") from e
    except ValueError as e:
        raise e  # 重新抛出数据校验异常
    except Exception as e:
        raise ValueError(f"Invalid CSES file format: {e}") from e