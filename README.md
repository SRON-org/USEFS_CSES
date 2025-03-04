<div align="center">

<image src="https://github.com/user-attachments/assets/9e91bfd4-4448-4668-bede-6eafb0b42888" height="86"/>

# USEFS_CSES

Convert CSES v1 to USEF Schema v1

#### [Main Repo](https://github.com/SRON-org/USEFS)

</div>

## 介绍

USEFS_ICS 是一个简单的 Python 程序，旨在将使用 CSES v1（通用的课程表交换格式）的 YAML、TOML 或 JSON 格式文件**完美地**转换为标准 USEFS（通用日程计划表交换格式架构） 的 YAML、TOML 或 JSON 格式文件，允许使用者将课表表导入至日程表、提醒事项、辅助计划和电子课程表等时间管理类产品。

## 特性

*   **单向转换**: 解析 CSES v1 文件，输出标准有效的 USEFS 格式文件。
*   **自动填充起始日期**: CSES v1 不支持保存开学日期，此工具支持指定或自动猜测开学日期以填充 ```from_date``` 关键字，用于计算单、双周。
