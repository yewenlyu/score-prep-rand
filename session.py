import random


class PracticeSession:
    """Pure state model for a measure practice session. No UI dependency."""

    def __init__(self, total: int) -> None:
        if total < 1:
            raise ValueError("Total measures must be at least 1")
        self._total = total
        self._remaining: list[int] = list(range(1, total + 1))
        random.shuffle(self._remaining)
        self._practiced: list[int] = []

    @property
    def total(self) -> int:
        return self._total

    @property
    def remaining_count(self) -> int:
        return len(self._remaining)

    @property
    def is_complete(self) -> bool:
        return len(self._remaining) == 0

    @property
    def practiced(self) -> list[int]:
        return self._practiced

    def next_measure(self) -> int:
        """Pop and return the next random measure. Raises if session is complete."""
        if self.is_complete:
            raise StopIteration("All measures have been practiced")
        measure = self._remaining.pop()
        self._practiced.append(measure)
        return measure
