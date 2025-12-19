"""Testing utilities."""

import shutil
import sys
from typing import Callable, Container, Dict, Optional

import pandas as pd
import pytest

try:
    import openpyxl
except ImportError:
    pass

try:
    import graphviz
except ImportError:
    pass


def requires_openpyxl(f: Callable):
    """Decorator that marks a test function to be skipped in openpyxl is not
    installed."""
    skipif = pytest.mark.skipif(
        "openpyxl" not in sys.modules, reason="requires openpyxl package"
    )
    return skipif(f)


def requires_graphviz(f: Optional[Callable] = None, python_only: bool = False):
    """Decorator that marks a test function to be skipped in graphviz is not
    installed."""

    def _decorator(f: Callable):
        graphviz_package_installed = "graphviz" in sys.modules
        dot_command_installed = shutil.which("dot") is not None

        if python_only:
            skip_condition = not graphviz_package_installed
        else:
            skip_condition = not (graphviz_package_installed and dot_command_installed)

        if not graphviz_package_installed:
            reason = "graphviz package not installed"
        elif not dot_command_installed:
            reason = "graphviz not installed. `dot` command not found"
        else:
            reason = "graphviz is installed"

        skipif = pytest.mark.skipif(skip_condition, reason=reason)
        return skipif(f)

    if f is None:
        return _decorator
    else:
        return _decorator(f)


def assert_dicts_equal(
    dict1: Dict, dict2: Dict, ignore_keys: Optional[Container[str]] = None
) -> None:
    """
    Check two dictionaries recursively for equivalence, optionally ignoring comparison
    between values of certain keys.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary
        ignore_keys (list): List of keys whose values should be ignored during comparison
    """
    ignore_keys = ignore_keys or ()

    # Check if the keys in both dictionaries match
    assert set(dict1.keys()) == set(dict2.keys())

    # Iterate over the keys in the dictionaries
    for key in dict1.keys():
        # Check if the key is in the list of keys to ignore
        if key in ignore_keys:
            continue

        # Check if the values for the key in both dictionaries are themselves
        # dictionaries
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            # Recursively check equivalence of the dictionaries
            assert_dicts_equal(dict1[key], dict2[key], ignore_keys)
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            for i in range(len(dict1[key])):
                item1 = dict1[key][i]
                item2 = dict2[key][i]

                if isinstance(item1, dict) and isinstance(item2, dict):
                    # Recursively check equivalence of the dictionaries
                    assert_dicts_equal(item1, item2, ignore_keys)
                else:
                    assert item1 == item2
        else:
            # Check equivalence of the values for the key in both dictionaries
            assert dict1[key] == dict2[key], f"Key: {key}"


def assert_dataframes_equal(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    ignore_columns: Optional[Container[str]] = None,
) -> None:
    """
    Check two dataframes for equivalence, optionally ignoring comparison between certain
    columns.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary
        ignore_columns (list): List of keys whose values should be ignored during comparison
    """
    ignore_columns = list(ignore_columns) or []

    df1 = df1.drop(columns=ignore_columns)
    df2 = df2.drop(columns=ignore_columns)

    assert df1.equals(df2)
