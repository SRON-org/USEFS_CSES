def build_usefs_data(cses_data: dict, from_date: str) -> dict:
    """
    Builds USEFS data from CSES data.
    """
    usefs_data = {
        "version": 1,
        "items": [],  # CSES 中没有独立的 item，所以为空
        "collections": []
    }

    for schedule in cses_data["schedules"]:
        collection = build_collection(schedule, cses_data["subjects"], from_date) # 传递开学日期，这对于解析单双周起到了很NB的作用
        usefs_data["collections"].append(collection)

    return usefs_data


def build_collection(schedule: dict, subjects: list, from_date: str) -> dict:
    """
    Builds a USEFS collection from a CSES schedule.
    """
    day_map = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }

    enable_day = schedule["enable_day"]
    enable = day_map.get(enable_day) # 获取星期几
    if not enable:
        raise ValueError(f"Invalid enable_day value: {enable_day}.  Must be between 1 and 7.")

    cycle = schedule["weeks"]
    if cycle not in ["all", "odd", "even"]:
        raise ValueError(f"Invalid weeks value: {cycle}. Must be 'all', 'odd', or 'even'.")

    if cycle == "all":
        cycle = "every" 

    collection = {
        "collection_name": schedule["name"],
        "enable": enable,
        "cycle": cycle,
        "importance": 1,
        "from_date": from_date, 
        "content": []
    }

    for class_data in schedule["classes"]:
        item = build_item(class_data, subjects)
        collection["content"].append(item)

    return collection


def build_item(class_data: dict, subjects: list) -> dict:
    """
    Builds a USEFS item from a CSES class.
    """
    subject_name = class_data["subject"]
    subject = next((s for s in subjects if s["name"] == subject_name), None)
    if not subject:
        raise ValueError(f"Subject with name '{subject_name}' not found.")


    start_time = class_data["start_time"]
    end_time = class_data["end_time"]

    # duration计算
    start_datetime = datetime.strptime(start_time, "%H:%M:%S")
    end_datetime = datetime.strptime(end_time, "%H:%M:%S")
    duration_timedelta = end_datetime - start_datetime
    duration_minutes = int(duration_timedelta.total_seconds() / 60) # 转换为分钟

    item = {
        "name": subject["name"],
        "short_name": subject.get("simplified_name", subject["name"]), # 优先使用 simplified_name
        "from_time": start_time[:5],  # USEFS 只需要 HH:MM 这真的太简洁了
        "duration": f"{duration_minutes}m",
        "note": f"授课教师: {subject.get('teacher', '未知')}",
        "tags": ["学习", subject["name"], "课程"],
        "properties": {
            "teacher": subject.get("teacher"),
            "room": subject.get("room")
        }
    }

    # 去除None这样代表啥都没有的值
    item["properties"] = {k: v for k, v in item["properties"].items() if v is not None}
    item = {k: v for k, v in item.items() if v is not None}


    return item

from datetime import datetime