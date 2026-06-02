from dataclasses import dataclass
import pandas as pd
from pathlib import Path
from src.utils import validate_deductible

max_deductible = 12081.0  # Change this to the applicable value


# Store the information in dataclasses
@dataclass
class InputsStart:
    """
    Container for initial (projected) inputs.

    Parameters
    ----------
    income : float
        Information pre-process: estimated annual income.
    projections : list of float
        Information pre-process: estimated deductible expenses by category.
    """

    income: float  # Information pre-process: estimated
    projections: list[float]  # Information pre-process: estimated


@dataclass
class InputsEnd:
    """
    Container for final (real) inputs.

    Parameters
    ----------
    income : float
        Information post-process: real annual income.
    retentions : float
        Information post-process: real tax retentions already applied.
    projections : list of float
        Information pre-process: estimated deductible expenses by category.
    real_values : list of float
        Information post-process: real deductible expenses by category.
    """

    income: float  # Information post-process: real
    retentions: float  # Information post-process: real
    projections: list[float]  # Information pre-process: estimated
    real_values: list[float]  # Information post-process: real


# Functions to load external data: ir_table and expenditures
def load_ir_table(path_csv: str | Path) -> pd.DataFrame:
    """
    Load and sort the progressive income tax (IR) table.

    Parameters
    ----------
    path_csv : str or Path
        Path to the CSV file containing the IR table.

    Returns
    -------
    pd.DataFrame
        DataFrame sorted by `fraccion_basica`.
    """
    path = Path(path_csv)  # Ensure it's a Path object
    if not path.exists():
        raise FileNotFoundError(f"IR table not found at {path}")
    df = pd.read_csv(path)
    df = df.sort_values("fraccion_basica")
    return df


@validate_deductible(max_deductible)
def load_expend_table(path_csv: str | Path) -> pd.DataFrame:
    """
    Load the expenditure table.

    Parameters
    ----------
    path_csv : str or Path
        Path to the CSV file containing expenditures.

    Returns
    -------
    pd.DataFrame
        DataFrame with expenditure projections and real values.
    """
    path = Path(path_csv)
    if not path.exists():
        raise FileNotFoundError(f"Expenditure table not found at {path}")
    return pd.read_csv(path)


# Related functions to get the values of interest
def select_level(base: float, ir_table: pd.DataFrame) -> pd.Series:
    """
    Select the tax bracket corresponding to a given base.

    Parameters
    ----------
    base : float
        Taxable base amount.
    ir_table : pd.DataFrame
        Progressive IR table.

    Returns
    -------
    pd.Series
        Row of the IR table corresponding to the applicable bracket.
    """
    idx = ir_table[ir_table["fraccion_basica"] <= base].index.max()
    return ir_table.loc[idx]


def base_tax(base: float, ir_table: pd.DataFrame) -> float:
    """
    Calculate the tax for a given base using the IR table.

    Parameters
    ----------
    base : float
        Taxable base amount.
    ir_table : pd.DataFrame
        Progressive IR table.

    Returns
    -------
    float
        Tax amount rounded to two decimals.
    """
    level = select_level(base, ir_table)  # Using previous logic
    excess = max(base - level["fraccion_basica"], 0)  # Non-negative filter just in case
    tax = float(
        excess * level["tarifa"] + level["impuesto_base"]
    )  # Casting the result as float to get the number only
    return round(tax, 2)


def calculate_start(inputs: InputsStart, ir_table: pd.DataFrame) -> dict[str, float]:
    """
    Calculate projected tax values.

    Parameters
    ----------
    inputs : InputsStart
        Initial inputs with income and projected expenses.
    ir_table : pd.DataFrame
        Progressive IR table.

    Returns
    -------
    dict of str to float
        Dictionary with projected annual tax and monthly retention.
    """
    total_proj = sum(inputs.projections)
    proj_base = max(inputs.income - total_proj, 0)
    tax_proj = base_tax(proj_base, ir_table)  # Using previous logic

    return {
        "Impuesto proyectado anual": tax_proj,
        "Retención proyectada mensual": round(tax_proj / 12, 2),
    }


def calculate(inputs: InputsEnd, ir_table: pd.DataFrame) -> dict[str, float]:
    """
    Calculate real tax values and compare with projections.

    Parameters
    ----------
    inputs : InputsEnd
        Final inputs with income, retentions, projections, and real expenses.
    ir_table : pd.DataFrame
        Progressive IR table.

    Returns
    -------
    dict of str to float
        Dictionary with projected and real bases, taxes, retentions,
        total payable, and difference between real and projected tax.
    """
    total_proj = sum(inputs.projections)
    total_real = sum(inputs.real_values)

    proj_base = max(inputs.income - total_proj, 0)
    real_base = max(inputs.income - total_real, 0)

    tax_proj = base_tax(proj_base, ir_table)  # Using previous logic
    tax_real = base_tax(real_base, ir_table)

    total_tax = round(tax_real - inputs.retentions, 2)

    return {
        "Base imponible proyectada": proj_base,
        "Base imponible real": real_base,
        "Impuesto proyectado anual": tax_proj,
        "Impuesto real anual": tax_real,
        "Retenciones acumuladas": inputs.retentions,
        "Total a pagar": total_tax,
    }
