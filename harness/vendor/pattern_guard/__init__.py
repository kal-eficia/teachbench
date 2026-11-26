"""Catch guessable answer patterns in multiple-choice and sort tasks."""
from .core import Finding, Report, analyse, plan_key, reorder_options
from .quiz import check_mcq, check_sort, fix_file, fix_mcq, fix_sort

__version__ = "1.0.0"
__all__ = ["Finding", "Report", "analyse", "plan_key", "reorder_options",
           "check_mcq", "check_sort", "fix_file", "fix_mcq", "fix_sort"]
