"""Mark short written answers against exam-style marking points. No model, no API."""
from .core import PointResult, Result, mark, normalise, stem

__version__ = "1.0.0"
__all__ = ["mark", "Result", "PointResult", "normalise", "stem"]
