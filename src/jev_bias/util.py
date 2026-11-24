from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def pmap(fn: Callable[[T], R], items: Iterable[T], workers: int = 8) -> list[R]:
    """Order-preserving threaded map; exceptions propagate."""
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, items))
