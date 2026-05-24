"""
Завдання 1 — однозв'язний список.

Реалізовано:
  - reverse() — реверс in-place, змінюємо посилання між вузлами
  - merge_sort() — сортування злиттям (природне для linked list,
    бо не потребує random access як quicksort)
  - merge_two_sorted() — об'єднання двох відсортованих списків
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node | None = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    @classmethod
    def from_iterable(cls, values) -> LinkedList:
        ll = cls()
        for v in values:
            ll.append(v)
        return ll

    def append(self, value: int) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        node = self.head
        while node.next is not None:
            node = node.next
        node.next = new_node

    def to_list(self) -> list[int]:
        out = []
        node = self.head
        while node is not None:
            out.append(node.value)
            node = node.next
        return out

    def __str__(self) -> str:
        parts = []
        node = self.head
        while node is not None:
            parts.append(str(node.value))
            node = node.next
        parts.append("None")
        return " -> ".join(parts)

    # ---------- реверс ----------

    def reverse(self) -> None:
        """In-place реверс: ідемо вперед, перенаправляємо посилання назад."""
        prev = None
        curr = self.head
        while curr is not None:
            next_node = curr.next  # запам'ятовуємо куди йти далі
            curr.next = prev       # перевертаємо посилання
            prev = curr            # рухаємо prev вперед
            curr = next_node
        self.head = prev

    # ---------- сортування злиттям ----------

    def merge_sort(self) -> None:
        """In-place merge sort. Складність O(n log n), пам'ять O(log n) на стек."""
        self.head = _merge_sort(self.head)


def _merge_sort(head: Node | None) -> Node | None:
    if head is None or head.next is None:
        return head

    # розбиваємо посередині через slow/fast pointer
    mid = _split_middle(head)
    left = _merge_sort(head)
    right = _merge_sort(mid)
    return _merge_nodes(left, right)


def _split_middle(head: Node) -> Node | None:
    """Знаходимо середину і розриваємо. Повертаємо голову правої половини."""
    slow = head
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    mid = slow.next  # type: ignore[union-attr]
    slow.next = None  # type: ignore[union-attr]
    return mid


def _merge_nodes(a: Node | None, b: Node | None) -> Node | None:
    """Зливає два відсортовані ланцюжки в один. Стабільне злиття."""
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def merge_two_sorted(a: LinkedList, b: LinkedList) -> LinkedList:
    """Зовнішня функція: бере два відсортовані LinkedList, повертає новий."""
    result = LinkedList()
    result.head = _merge_nodes(a.head, b.head)
    return result


if __name__ == "__main__":
    print("Реверс:")
    ll = LinkedList.from_iterable([1, 2, 3, 4, 5])
    print(f"  до:    {ll}")
    ll.reverse()
    print(f"  після: {ll}")

    print("\nСортування злиттям:")
    ll = LinkedList.from_iterable([5, 2, 8, 1, 9, 3, 7, 4, 6])
    print(f"  до:    {ll}")
    ll.merge_sort()
    print(f"  після: {ll}")

    print("\nЗлиття двох відсортованих:")
    a = LinkedList.from_iterable([1, 4, 7, 10])
    b = LinkedList.from_iterable([2, 3, 8, 11, 15])
    print(f"  a:      {a}")
    print(f"  b:      {b}")
    merged = merge_two_sorted(a, b)
    print(f"  merged: {merged}")
