"""
Завдання 5 — візуалізація обходів бінарного дерева (DFS та BFS).

Обходи реалізовані **ітеративно**, без рекурсії, як вимагає умова:
  - DFS — через стек (LIFO),
  - BFS — через чергу (FIFO).

Колір кожного вузла відповідає його порядку відвідування — від
темного (перший) до світлого (останній). Це візуально показує
послідовність обходу: око бачить градієнт що іде по дереву.
"""

import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color: str = "skyblue") -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x: float = 0, y: float = 0, layer: int = 1):
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


# ---------- генерація кольорів ----------

def order_color(idx: int, total: int) -> str:
    """
    Колір для idx-того вузла. idx=0 — темний, idx=total-1 — світлий.
    Використовуємо інтерполяцію в RGB між двома точками.
    """
    if total <= 1:
        return "#1296F0"
    t = idx / (total - 1)
    # від темно-синього до світло-блакитного
    start = (0x0a, 0x2c, 0x6b)
    end = (0xb3, 0xe5, 0xfc)
    r = round(start[0] + (end[0] - start[0]) * t)
    g = round(start[1] + (end[1] - start[1]) * t)
    b = round(start[2] + (end[2] - start[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------- обходи ----------

def dfs_iterative(root: Node) -> list[Node]:
    """DFS через стек. Кладемо правого спочатку, щоб лівий брався першим."""
    if root is None:
        return []
    stack: list[Node] = [root]
    order: list[Node] = []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def bfs_iterative(root: Node) -> list[Node]:
    """BFS через чергу. Класичний level-by-level."""
    if root is None:
        return []
    queue: deque[Node] = deque([root])
    order: list[Node] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


# ---------- візуалізація ----------

def paint_by_order(visit_order: list[Node]) -> None:
    """Фарбуємо вузли за порядком відвідування."""
    total = len(visit_order)
    for i, node in enumerate(visit_order):
        node.color = order_color(i, total)


def draw_traversal(root: Node, filename: str, title: str) -> None:
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(
        tree, pos=pos, ax=ax, labels=labels, arrows=False,
        node_size=1500, node_color=colors, font_size=11, font_weight="bold",
        font_color="white", edgecolors="#212121",
    )
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  графік збережено: {filename}")


def build_sample_tree() -> Node:
    r"""
    Будуємо дерево достатньо великим щоб бачити різницю DFS vs BFS.
            1
          /   \
         2     3
        / \   / \
       4   5 6   7
      / \
     8   9
    """
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    root.left.left.left = Node(8)
    root.left.left.right = Node(9)
    return root


if __name__ == "__main__":
    # DFS
    root = build_sample_tree()
    dfs_order = dfs_iterative(root)
    print(f"DFS порядок: {[n.val for n in dfs_order]}")
    paint_by_order(dfs_order)
    draw_traversal(root, "dfs.png", title="DFS (стек) — від темного до світлого")

    # BFS — будуємо дерево заново, щоб мати свіжі вузли без кольорів від DFS
    root = build_sample_tree()
    bfs_order = bfs_iterative(root)
    print(f"BFS порядок: {[n.val for n in bfs_order]}")
    paint_by_order(bfs_order)
    draw_traversal(root, "bfs.png", title="BFS (черга) — від темного до світлого")
