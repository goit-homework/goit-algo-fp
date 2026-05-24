"""
Завдання 7 — імовірності суми двох кубиків методом Монте-Карло.

Кидаємо два чесні шестигранники велику кількість разів, рахуємо
скільки разів випала кожна можлива сума (від 2 до 12), отримуємо
експериментальні ймовірності. Порівнюємо з аналітичними.

Аналітичні значення (з умови):
  2:  1/36 (2.78%)
  3:  2/36 (5.56%)
  ...
  7:  6/36 (16.67%)  <-- максимум
  ...
  12: 1/36 (2.78%)
"""

import numpy as np
import matplotlib.pyplot as plt


N_TRIALS = 1_000_000
RNG_SEED = 42


# аналітичні (точні) ймовірності — кількість способів отримати кожну суму
ANALYTICAL_COUNTS = {
    2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
    8: 5, 9: 4, 10: 3, 11: 2, 12: 1,
}
TOTAL_OUTCOMES = 36
ANALYTICAL_PROB = {s: c / TOTAL_OUTCOMES for s, c in ANALYTICAL_COUNTS.items()}


def monte_carlo_dice(n_trials: int, rng: np.random.Generator) -> dict[int, float]:
    """
    n кидків двох кубиків. Повертає {сума: емпірична_ймовірність}.

    Векторизована версія через numpy — швидше за цикл у Python.
    """
    d1 = rng.integers(1, 7, n_trials)
    d2 = rng.integers(1, 7, n_trials)
    sums = d1 + d2

    counts = np.bincount(sums, minlength=13)
    probs = {s: counts[s] / n_trials for s in range(2, 13)}
    return probs


def print_table(empirical: dict[int, float]) -> None:
    print()
    print("=" * 60)
    print(f"  Результати Монте-Карло на {N_TRIALS:,} кидках")
    print("=" * 60)
    print(f"  {'сума':>4}  {'MC ймовірність':>16}  {'аналітично':>14}  {'похибка':>9}")
    print("  " + "-" * 56)
    for s in sorted(empirical):
        mc = empirical[s]
        analytical = ANALYTICAL_PROB[s]
        err = abs(mc - analytical)
        rel_err = err / analytical * 100
        bar = "*" * int(mc * 200)  # маленька діаграма прямо в таблиці
        print(
            f"  {s:>4}  {mc * 100:>13.4f}%   {analytical * 100:>12.4f}%   {rel_err:>6.2f}%  {bar}"
        )


def plot_results(empirical: dict[int, float], filename: str = "dice.png") -> None:
    sums = sorted(empirical)
    mc_values = [empirical[s] * 100 for s in sums]
    analytical_values = [ANALYTICAL_PROB[s] * 100 for s in sums]

    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.array(sums)
    width = 0.35

    bars_mc = ax.bar(x - width / 2, mc_values, width, label=f"Monte Carlo ({N_TRIALS:,} кидків)",
                     color="#1976d2", edgecolor="#0d47a1")
    bars_an = ax.bar(x + width / 2, analytical_values, width, label="Аналітично",
                     color="#f57c00", edgecolor="#bf360c")

    # підписи зверху стовпчиків
    for b in bars_mc:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + 0.1, f"{h:.2f}", ha="center", fontsize=8)
    for b in bars_an:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + 0.1, f"{h:.2f}", ha="center", fontsize=8, color="#bf360c")

    ax.set_xticks(sums)
    ax.set_xlabel("сума на двох кубиках")
    ax.set_ylabel("ймовірність, %")
    ax.set_title("Ймовірності суми двох кубиків: Monte Carlo vs аналітично")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")


if __name__ == "__main__":
    rng = np.random.default_rng(RNG_SEED)
    empirical = monte_carlo_dice(N_TRIALS, rng)

    print_table(empirical)

    total_abs_err = sum(abs(empirical[s] - ANALYTICAL_PROB[s]) for s in empirical)
    print()
    print(f"  Сумарна абсолютна похибка по всіх 11 сумах: {total_abs_err:.6f}")
    print(f"  Середня відносна похибка на одну суму: {total_abs_err / 11 * 100:.4f}%")

    plot_results(empirical)
