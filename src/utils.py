from functools import wraps
import pandas as pd
from typing import Callable

def validate_deductible(max_deductible: float):
    """
    Decorator to validate that projected expenses do not exceed a maximum deductible.

    Parameters
    ----------
    max_deductible : float
        Maximum allowable sum of projected expenses. If the sum of the
        `proyeccion` column in the loaded DataFrame exceeds this value,
        a ValueError is raised.

    Returns
    -------
    function
        A decorated loader function that returns a validated DataFrame.
        The DataFrame is returned unchanged if the condition is satisfied.

    Raises
    ------
    ValueError
        If the sum of projected expenses is greater than `max_deductible`.

    Notes
    -----
    - This decorator is intended to be applied to loader functions that
      return a DataFrame with a `proyeccion` column.
    - The validation occurs immediately after the DataFrame is loaded.
    - Using `functools.wraps` preserves the original function’s name and
      docstring for introspection and documentation tools.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            table = func(*args, **kwargs)
            total_proj = table["proyeccion"].sum()
            if total_proj <= max_deductible:
                return table
            else:
                raise ValueError(
                    f"The sum of projected values ({total_proj}) "
                    f"exceeds the maximum deductible ({max_deductible})."
                )
        return wrapper
    return decorator