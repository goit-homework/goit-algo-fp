"""
Завдання 3 — алгоритм Дейкстри з бінарною купою.

Знаходимо найкоротші відстані від вибраної стартової вершини
до всіх інших у зваженому неорієнтованому графі.

Класична Дейкстра без купи — O(V²). З бінарною купою (heapq) —
O((V + E) log V). Купа дозволяє швидко вибирати наступну вершину
з мінімальною відстанню.

Граф — невелика умовна "мережа міст України" (вершини = міста,
ребра з вагами = умовна довжина шляху в км).
"""

import heapq
import math

import matplotlib.pyplot as plt
import networkx as nx


# умовний зважений граф (міста, ребро = (сусід, вага))
GRAPH: dict[str, list[tuple[str, int]]] = {
    "Київ":     [("Житомир", 140), ("Чернігів", 150), ("Черкаси", 190), ("Полтава", 350)],
    "Житомир":  [("Київ", 140), ("Львів", 470), ("Вінниця", 130)],
    "Львів":    [("Житомир", 470), ("Тернопіль", 130), ("Ужгород", 260)],
    "Тернопіль":[("Львів", 130), ("Вінниця", 230)],
    "Вінниця":  [("Житомир", 130), ("Тернопіль", 230), ("Одеса", 430)],
    "Одеса":    [("Вінниця", 430), ("Миколаїв", 130), ("Херсон", 200)],
    "Миколаїв": [("Одеса", 130), ("Херсон", 70), ("Кропивницький", 180)],
    "Кропивницький":[("Миколаїв", 180), ("Черкаси", 130), ("Дніпро", 250)],
    "Черкаси":  [("Київ", 190), ("Кропивницький", 130), ("Полтава", 220)],
    "Полтава":  [("Київ", 350), ("Черкаси", 220), ("Харків", 140), ("Дніпро", 180)],
    "Харків":   [("Полтава", 140), ("Дніпро", 220)],
    "Дніпро":   [("Полтава", 180), ("Харків", 220), ("Запоріжжя", 80), ("Кропивницький", 250)],
    "Запоріжжя":[("Дніпро", 80), ("Херсон", 280)],
    "Херсон":   [("Одеса", 200), ("Миколаїв", 70), ("Запоріжжя", 280)],
    "Чернігів": [("Київ", 150)],
    "Ужгород":  [("Львів", 260)],
}


def dijkstra(graph: dict[str, list[tuple[str, int]]], source: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """
    Повертає (distances, previous):
      distances[v] — найкоротша відстань source -> v
      previous[v] — попередня вершина на найкоротшому шляху

    Алгоритм:
      1. Усі відстані = ∞, окрім source = 0.
      2. Купа стартує з (0, source).
      3. Беремо вершину з мінімальною відстанню, релаксуємо її сусідів.
      4. Повторюємо доки купа не пуста.
    """
    distances: dict[str, float] = {v: math.inf for v in graph}
    previous: dict[str, str | None] = {v: None for v in graph}
    distances[source] = 0

    heap: list[tuple[float, str]] = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        # стандартний lazy-delete трюк: ігноруємо застарілі записи у купі
        if current_dist > distances[u]:
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, previous


def reconstruct_path(previous: dict[str, str | None], target: str) -> list[str]:
    """Збираємо шлях від source до target, ідучи назад по previous[]."""
    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path


def visualize(graph: dict, source: str, distances: dict, previous: dict, filename: str) -> None:
    g = nx.Graph()
    for u, neighbors in graph.items():
        for v, w in neighbors:
            g.add_edge(u, v, weight=w)

    pos = nx.spring_layout(g, seed=42, k=1.5)

    # ребра що входять у дерево найкоротших шляхів
    shortest_edges = set()
    for v, prev in previous.items():
        if prev is not None:
            shortest_edges.add(frozenset({prev, v}))

    edges_in_tree = [(u, v) for u, v in g.edges() if frozenset({u, v}) in shortest_edges]
    edges_other = [(u, v) for u, v in g.edges() if frozenset({u, v}) not in shortest_edges]

    fig, ax = plt.subplots(figsize=(12, 8))

    # звичайні ребра
    nx.draw_networkx_edges(g, pos, edgelist=edges_other, ax=ax, edge_color="#bdbdbd", width=1)
    # ребра дерева — товщі і яскравіші
    nx.draw_networkx_edges(g, pos, edgelist=edges_in_tree, ax=ax, edge_color="#d32f2f", width=2.5)

    # вузли (source виділяємо окремо)
    node_colors = ["#ffc107" if v == source else "#90caf9" for v in g.nodes()]
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color=node_colors, node_size=1300, edgecolors="#424242")

    # підписи: місто + відстань
    labels = {v: f"{v}\n({int(distances[v])} км)" for v in g.nodes()}
    nx.draw_networkx_labels(g, pos, labels=labels, ax=ax, font_size=8)

    # ваги на ребрах
    edge_weights = {(u, v): d["weight"] for u, v, d in g.edges(data=True)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights, ax=ax, font_size=7, label_pos=0.5)

    ax.set_title(f"Найкоротші шляхи від '{source}' (червоні ребра = дерево Дейкстри)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")


if __name__ == "__main__":
    source = "Київ"
    distances, previous = dijkstra(GRAPH, source)

    print(f"Найкоротші відстані від '{source}':")
    print("-" * 50)
    for city in sorted(distances, key=lambda c: distances[c]):
        path = reconstruct_path(previous, city)
        path_str = " -> ".join(path)
        print(f"  {city:<14} {int(distances[city]):>4} км   шлях: {path_str}")

    print()
    visualize(GRAPH, source, distances, previous, "dijkstra.png")
