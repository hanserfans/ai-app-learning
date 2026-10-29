"""变量、列表、字典、条件和循环：运行后打印一周学习统计。"""


def main():
    learner = "Python 初学者"
    minutes = [30, 45, 0, 60, 25, 40, 20]
    target_minutes = 180
    total = 0

    for day, value in enumerate(minutes, start=1):
        total += value
        if value > 0:
            print(f"第 {day} 天：学习 {value} 分钟")
        else:
            print(f"第 {day} 天：休息")

    summary = {
        "learner": learner,
        "total_minutes": total,
        "average_minutes": round(total / len(minutes), 1),
        "target_met": total >= target_minutes,
    }
    print(summary)


if __name__ == "__main__":
    main()
