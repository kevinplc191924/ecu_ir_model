import pandas as pd
import pytest
from src.model import (
    InputsStart,
    InputsEnd,
    load_ir_table,
    load_expend_table,
    select_level,
    base_tax,
    calculate_start,
    calculate,
)
from src.utils import validate_deductible


# Fixtures (sample data for testing)
@pytest.fixture
def sample_ir_table():
    # Minimal progressive IR table for testing
    data = {
        "fraccion_basica": [0, 10000],
        "impuesto_base": [0, 100],
        "tarifa": [0.1, 0.2],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_expend_table():
    data = {"proyeccion": [1000, 500], "real": [1200, 600]}
    return pd.DataFrame(data)


# Tests for data loaders
def test_load_ir_table(tmp_path):
    csv_path = tmp_path / "tabla_ir.csv"  # Create a temporary CSV

    pd.DataFrame(
        {"fraccion_basica": [0], "impuesto_base": [0], "tarifa": [0.1]}
    ).to_csv(csv_path, index=False)

    df = load_ir_table(csv_path)

    assert "fraccion_basica" in df.columns
    assert df.iloc[0]["tarifa"] == 0.1


def test_load_expend_table(tmp_path):
    csv_path = tmp_path / "gastos.csv"
    pd.DataFrame({"proyeccion": [100], "real": [80]}).to_csv(csv_path, index=False)

    df = load_expend_table(csv_path)

    assert "proyeccion" in df.columns
    assert df.iloc[0]["real"] == 80


# Tests for validation of max deductible (decorator already applied in model.py)
# Decorate the loader for testing
validated_loader = validate_deductible(max_deductible=1500)(load_expend_table)


def test_validate_deductible_passes(tmp_path):
    csv_path = tmp_path / "gastos.csv"
    pd.DataFrame({"proyeccion": [1000, 500], "real": [800, 400]}).to_csv(
        csv_path, index=False
    )

    df = validated_loader(csv_path)  # use the decorated version
    assert df["proyeccion"].sum() == 1500  # passes because sum == limit


def test_validate_deductible_raises(tmp_path):
    csv_path = tmp_path / "gastos.csv"
    pd.DataFrame({"proyeccion": [1000, 1000], "real": [800, 400]}).to_csv(
        csv_path, index=False
    )

    with pytest.raises(ValueError):
        validated_loader(csv_path)  # should raise because sum = 2000 > 1500


# Tests for tax logic
def test_select_level(sample_ir_table):
    level = select_level(12000, sample_ir_table)
    assert level["fraccion_basica"] == 10000


def test_base_tax(sample_ir_table):
    result = base_tax(12000, sample_ir_table)
    expected = round((12000 - 10000) * 0.2 + 100, 2)  # 500.0

    assert result == expected


def test_calculate_start(sample_ir_table, sample_expend_table):
    inputs = InputsStart(
        income=20000, projections=sample_expend_table["proyeccion"].tolist()
    )
    result = calculate_start(inputs, sample_ir_table)

    assert "Impuesto proyectado anual" in result
    assert isinstance(result["Impuesto proyectado anual"], float)


def test_calculate(sample_ir_table, sample_expend_table):
    inputs = InputsEnd(
        income=20000,
        retentions=200,
        projections=sample_expend_table["proyeccion"].tolist(),
        real_values=sample_expend_table["real"].tolist(),
    )
    result = calculate(inputs, sample_ir_table)

    assert "Impuesto real anual" in result
    assert "Total a pagar" in result
    assert isinstance(result["Total a pagar"], float)
