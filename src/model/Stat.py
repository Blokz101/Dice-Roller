from typing import Optional, Callable


class Stat:

    def __init__(
        self,
        name: str = "",
        initial_value: int = 0,
        max_value: Optional[int] = None,
        modifier_formula: Optional[Callable[[], None]] = None,
    ):
        self.name: str = name
        self.current_value: int = initial_value
        self.max_value: Optional[int] = max_value
        self.modifier_formula: Optional[Callable[[], int]] = modifier_formula

    def modifier(self) -> Optional[int]:
        if self.modifier_formula is None:
            return None
        return self.modifier_formula()
