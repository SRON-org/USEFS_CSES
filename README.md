<div align="center">

<image src="https://github.com/user-attachments/assets/9e91bfd4-4448-4668-bede-6eafb0b42888" height="86"/>
<image src="http://m.qpic.cn/psc?/V51UyG6T2hLdbN0oEgHl3fEkH73KqJt7/TmEUgtj9EK6.7V8ajmQrEEsEylM*52lTktZHLze*PTbMCd2wg4o5kkEyKNVsVL9UM5xK4GLClF.TOL*ty*FnqAuxBQmobbAoJ.gYMo62EQY!/mnull&bo=wADAAAAAAAADByI!&rf=photolist&t=5" height="86"/>

# USEFS_CSES

Convert CSES v1 to USEF Schema v1

#### [Main Repo](https://github.com/SRON-org/USEFS)

</div>

## 介绍

USEFS_CSES 是一个简单的 Python 程序，旨在将使用 CSES v1（通用的课程表交换格式）的文件**完美地**转换为标准 USEFS（通用日程计划表交换格式架构） 的 YAML、TOML 或 JSON 格式文件，允许使用者将课表表导入至日程表、提醒事项、辅助计划和电子课程表等时间管理类产品。

## 特性

*   **单向转换**: 解析 CSES v1 文件，输出标准有效的 USEFS 格式文件。
*   **自动填充起始日期**: CSES v1 不支持保存开学日期，此工具支持指定或自动猜测开学日期以填充 ```from_date``` 关键字，用于计算单、双周。
*   **简单灵活地使用**: 可以在命令行中使用，也可以在 Python 中调用。这些仅需简单的 _一行代码_ 即可完成。
*   **完整兼容**：处理单双周课表，允许将 CSES 的部分 USEFS 标准未收录的原生关键字和自定义关键字转换为自定义关键字。

## 安装

请使用以下代码从 **PyPI** 安装最新版本的 ```USEFS_CSES``` ：
```bash
pip install USEFS_CSES
```

## 用法
### 命令行

1.  **基本用法：**

    ```bash
    USEFS_CSES <cses_file> <usefs_file>
    ```

    *   `<cses_file>`:  CSES 源文件路径.
    *   `<usefs_file>`:  USEFS 目标文件路径 (根据文件扩展名决定格式：YAML, TOML, 或 JSON).

2.  **指定开学日期 (可选)：**

    ```bash
    USEFS_CSES <cses_file> <usefs_file> --from_date YYYY-MM-DD
    ```

    *   `--from_date`:  指定开学日期，格式为 `YYYY-MM-DD`。  如果没有指定，程序会自动根据当前时段检测。

**示例：**

```bash
USEFS_CSES cses.yaml output.json  # 将 CSES 的 YAML 格式转换为 USEFS 的 JSON 格式
USEFS_CSES cses.yaml output.yaml --from_date 2025-09-01  # 转换并指定开学日期
```

### 代码调用

1.  **导入 `convert_cses_to_usefs` 函数：**

    ```python
    from USEFS_CSES.ToUSEFS import convert_cses_to_usefs
    ```

2.  **调用函数：**

    ```python
    try:
        convert_cses_to_usefs("cses.yaml", "schedule.yaml")
    except ValueError as e:
        print(f"Conversion failed: {e}")
    ```

    *   `convert_cses_to_usefs(cses_file, usefs_file, from_date=None)`
        *   `cses_file`:  CSES 源文件路径.
        *   `usefs_file`:  USEFS 目标文件路径 (文件扩展名决定格式).
        *   `from_date`:  可选，开学日期字符串 (YYYY-MM-DD)。

    **注意：**
    通过修改 `usefs_file` 的文件扩展名来指定目标 USEFS 文件的格式 (.yaml, .toml, .json)。

## 文件格式

*   **CSES 源文件：** 可以是 YAML、TOML 或 JSON 格式。程序会根据文件扩展名自动检测。
*   **USEFS 目标文件：**  通过目标文件名（`usefs_file`）的扩展名来指定格式，可以是 YAML (`.yaml` 或 `.yml`)、TOML (`.toml`) 或 JSON (`.json`)。

## 示例

你可以在本仓库的 ```examples``` 文件夹中找到相关示例文件：

* ```CSES2USEFS.example.py``` : 使用 Python 调用此工具的示例，运行后将会将目录下的示例 CSES 标准格式 ```cses.yaml``` 文件转换为 JSON、YAML 和 TOML 格式的 USEFS 文件。

* ```usefs_from_cses.json``` : 转换后的 JSON 格式的 USEFS 文件示例。

* ```usefs_from_cses.yaml``` : 转换后的 YAML 格式的 USEFS 文件示例。

* ```usefs_from_cses.toml``` : 转换后的 TOML 格式的 USEFS 文件示例。

## 关于 CSES[^1]
[SmartTeachCN/CSES](https://github.com/SmartTeachCN/CSES) （The Course Schedule Exchange Schema）是一个由 SmartTeach 团队研发的**新一代通用课程表交换格式**，用于在不同软件之间交换课程表。遵循 MIT License，它被设计为简单易用，可以轻松转换为其他格式。

> [!Important]
>
> 本工具所有代码中均未使用到来自 SmartTeachCN 团队的，有关 CSES 的任何官方工具或脚本。USEFS 与 CSES 及其所属团队不存在任何商业联系。

[^1]: 本版介绍部分摘自其原有仓库的 README.md 文件。你可以查看其仓库来了解有关于 CSES 标准的更多详细信息。
