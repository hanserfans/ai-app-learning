"""JSON 文件与异常。默认更新 data/learning_records.json 演示文件。"""

import argparse
import json
from pathlib import Path


def save_records(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(records, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")


def load_records(path: Path) -> list[dict]:
    # 文件不存在时返回空记录；损坏的内容应暴露错误，避免静默丢数据。
    if not path.exists():
        return []
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("记录文件的最外层必须是列表")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("每条记录必须是对象")
        if not isinstance(record.get("topic"), str):
            raise ValueError("topic 必须是字符串")
        minutes = record.get("minutes")
        if type(minutes) is not int or minutes < 0:
            raise ValueError("minutes 必须是非负整数")
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_path = Path(__file__).resolve().parents[1] / "data" / "learning_records.json"
    parser.add_argument("--path", type=Path, default=default_path)
    args = parser.parse_args()
    # 这是固定演示数据：每次运行覆盖 --path 指向的演示文件。
    records = [{"topic": "Python 文件读写", "minutes": 30}]
    try:
        save_records(args.path, records)
        loaded = load_records(args.path)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"保存或读取失败：{error}")
        raise SystemExit(1) from error
    print(f"已保存并读取 {len(loaded)} 条记录：{args.path}")
    print(loaded)


if __name__ == "__main__":
    main()
