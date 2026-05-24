"""
Завдання 6 — вибір їжі з найбільшою сумарною калорійністю в межах
бюджету (класична задача про рюкзак, 0/1 knapsack).

Реалізовано два підходи:
  - greedy_algorithm: жадібний за відношенням calories/cost
  - dynamic_programming: 0/1 knapsack через DP-таблицю (гарантовано оптимум)
"""


items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Сортуємо страви за спаданням відношення calories/cost і додаємо
    в кошик доки вистачає бюджету. Це 0/1 — кожну страву беремо
    максимум раз.

    Жадібний підхід не дає гарантії оптимуму для 0/1 knapsack —
    він буде оптимальним для дробового варіанту (коли можна брати
    частину страви), але для цілих штук іноді програє DP.

    Складність: O(n log n) на сортування + O(n) на обхід.
    """
    sorted_items = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen: list[str] = []
    spent = 0
    calories = 0
    for name, attrs in sorted_items:
        if spent + attrs["cost"] <= budget:
            chosen.append(name)
            spent += attrs["cost"]
            calories += attrs["calories"]

    return chosen, spent, calories


def dynamic_programming(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Класичний 0/1 knapsack через DP-таблицю.

    dp[i][b] = максимум калорій, що можна набрати, використовуючи
              перші i страв і бюджет b.

    Рекурентність:
      dp[i][b] = max(
          dp[i-1][b],                                           # не беремо i-ту
          dp[i-1][b - cost_i] + calories_i  якщо cost_i <= b    # беремо i-ту
      )

    Складність: O(n × budget) часу і пам'яті.
    """
    names = list(items.keys())
    n = len(names)

    # dp[i][b] — оптимальні калорії для перших i страв і бюджету b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            # варіант 1: не беремо i-ту страву
            dp[i][b] = dp[i - 1][b]
            # варіант 2: беремо, якщо влізає
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)

    # відновлюємо набір страв, ідучи назад по таблиці
    chosen: list[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            # i-ту страву взяли
            chosen.append(names[i - 1])
            b -= items[names[i - 1]]["cost"]

    chosen.reverse()
    spent = sum(items[name]["cost"] for name in chosen)
    return chosen, spent, dp[n][budget]


def print_result(label: str, chosen: list[str], spent: int, calories: int, budget: int) -> None:
    print(f"  {label}:")
    print(f"    обрано:  {chosen}")
    print(f"    витрачено: {spent} / {budget}")
    print(f"    калорій:   {calories}")


if __name__ == "__main__":
    print("Меню:")
    for name, attrs in items.items():
        ratio = attrs["calories"] / attrs["cost"]
        print(f"  {name:<10} cost={attrs['cost']:>3}  cal={attrs['calories']:>4}  ratio={ratio:.1f}")

    print()
    for budget in [50, 80, 100, 150]:
        print(f"Бюджет: {budget}")
        print("-" * 50)
        g_chosen, g_spent, g_cal = greedy_algorithm(items, budget)
        d_chosen, d_spent, d_cal = dynamic_programming(items, budget)
        print_result("greedy", g_chosen, g_spent, g_cal, budget)
        print_result("dp    ", d_chosen, d_spent, d_cal, budget)
        if d_cal > g_cal:
            print(f"    *** DP набрав на {d_cal - g_cal} калорій більше ({(d_cal - g_cal) / g_cal * 100:.1f}%)")
        elif d_cal == g_cal:
            print("    збігаються")
        print()
