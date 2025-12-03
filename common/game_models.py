from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class GameState:
    secret_object: Optional[str] = None
    max_questions: int = 20
    num_questions_asked: int = 0
    history: List[Tuple[str, str]] = field(default_factory=list)
    winner: Optional[str] = None
    finished: bool = False


def parse_yes_no(text: str) -> Optional[str]:
    t = text.strip().lower()
    if t in {"y", "yes"}:
        return "yes"
    if t in {"n", "no"}:
        return "no"

    if "yes" in t and "no" not in t:
        return "yes"
    if "no" in t and "yes" not in t:
        return "no"

    return None


def parse_llm_guess(text: str) -> Optional[str]:
    """
    Extract guess from strings like 'GUESS: cat'.
    """
    if text.upper().startswith("GUESS:"):
        return text.split(":", 1)[1].strip()
    return None
