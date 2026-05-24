"""
Завдання 4 — візуалізація бінарної купи.

Бінарна купа зберігається як масив, де для вузла з індексом i:
  - лівий нащадок: 2i + 1
  - правий нащадок: 2i + 2

Беремо список значень, перетворюємо у min-heap через heapq.heapify,
потім будуємо дерево Node-ів за індексами масиву і малюємо.

Базовий код — з умови завдання (Node + add_edges + draw_tree),
адаптований під нашу задачу і з градієнтом кольору по глибині.
"""

import heapq
import math
import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    """Вузол дерева для візуалізації (з умови завдання)."""

    def __init__(self, key, color: str = "skyblue") -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_tree_from_heap(heap: list[int]) -> Node | None:
    """Конвертує масив-купу у дерево Node-ів за індексами 2i+1, 2i+2."""
    if not heap:
        return None

    nodes = [Node(v) for v in heap]
    for i, node in enumerate(nodes):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < len(nodes):
            node.left = nodes[left_idx]
        if right_idx < len(nodes):
            node.right = nodes[right_idx]

    return nodes[0]


def _depth_gradient(depth: int, max_depth: int) -> str:
    """Корінь — темно-синій, листя — світло-блакитний."""
    t = depth / max(max_depth, 1)
    # від (#0d47a1) до (#bbdefb)
    start = (0x0d, 0x47, 0xa1)
    end = (0xbb, 0xde, 0xfb)
    r = round(start[0] + (end[0] - start[0]) * t)
    g = round(start[1] + (end[1] - start[1]) * t)
    b = round(start[2] + (end[2] - start[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def assign_colors(root: Node | None, max_depth: int, depth: int = 0) -> None:
    if root is None:
        return
    root.color = _depth_gradient(depth, max_depth)
    assign_colors(root.left, max_depth, depth + 1)
    assign_colors(root.right, max_depth, depth + 1)


def add_edges(graph, node, pos, x: float = 0, y: float = 0, layer: int = 1):
    """Рекурсивно додає вузли та ребра, призначаючи координати (з умови)."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_heap(root: Node, filename: str, title: str = "Бінарна купа") -> None:
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(
        tree, pos=pos, ax=ax, labels=labels, arrows=False,
        node_size=1500, node_color=colors, font_size=11, font_weight="bold",
        edgecolors="#212121",
    )
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")


if __name__ == "__main__":
    values = [50, 30, 20, 15, 10, 8, 16, 4, 7, 9, 6, 5, 11, 12, 3]
    print(f"Початковий список:   {values}")

    heap = values[:]
    heapq.heapify(heap)
    print(f"Після heapify():      {heap}")
    print("  (мін-купа: корінь = найменше значення)")

    max_depth = int(math.log2(len(heap))) if heap else 0
    root = build_tree_from_heap(heap)
    if root is not None:
        assign_colors(root, max_depth)
        draw_heap(root, "heap.png", title="Мін-купа (корінь зверху)")
