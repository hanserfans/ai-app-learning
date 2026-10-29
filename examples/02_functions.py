"""函数：参数、返回值、默认参数和类型提示。"""


def summarize_minutes(minutes: list[int], target: int = 180) -> dict:
    """返回学习统计；空列表有效，负数记录无效。"""
    if any(value < 0 for value in minutes):
        raise ValueError("学习分钟数不能为负数")
    total = sum(minutes)
    return {
        "total": total,
        "average": round(total / len(minutes), 1) if minutes else 0,
        "target_met": total >= target,
    }


def main():
    result = summarize_minutes([30, 45, 60], target=120)
    print(f"总计 {result['total']} 分钟，是否达标：{result['target_met']}")
    print("空记录：", summarize_minutes([]))
    try:
        summarize_minutes([30, -5])
    except ValueError as error:
        print(f"输入有误：{error}")


if __name__ == "__main__":
    main()
