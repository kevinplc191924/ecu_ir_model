# Ecuador IR model (2025)

Automated Income Tax (Impuesto a la Renta, IR) calculator for Ecuador, built in Python.

This project provides a modular system to:

- Load the Ecuadorian progressive IR table from CSV.
- Process projected and real expenses by category.
- Calculate taxable base, projected tax, real tax, and final balance.
- Run simulations in Jupyter notebooks or via a command‑line interface (CLI).

---

## 📂 Project Structure

```text
ecu_ir_model/  # Root folder project
    data/
        - gastos_proy.csv        # Projected expenses per category (start)
        - gastos.csv             # Projected and real expenses per category (end)
        - gastos_second_case.csv # Expenses to simulate negative tax
        - tabla_ir.csv           # Applicable personal income tax table (2025)
    notebooks/
        - ir_application.ipynb  # Use-cases and Spanish explanation
    src/
        - cli.py   # CLI script to calculate the tax (end of the year)
        - model.py # Functions and logic to calculate the tax (start and end of the year)
    test/
        - test_model.py
        - test_cli.py
    README.md
    requirements.txt
    setup.py # File to auto-install the project as a package
```

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/ecu_ir_model.git
cd ecu_ir_model
pip install -r requirements.txt
```

Install as a package in editable mode `-e` to use the functions from `src/model.py` and further modifications across the folder structure:

```bash
pip install -e .
```

---

## 🚀 Usage

1. **Jupyter Notebook**

Open the notebook in `notebooks/ir_application.ipynb` to run simulations interactively. **An explanation of the process in Spanish is included.**

Example snippet to run from the root:

```python
from src.model import InputsEnd, load_ir_table, load_expend_table, calculate

# Load data
ir_table = load_ir_table("data/tabla_ir.csv")
expend_table = load_expend_table("data/gastos.csv")

# Define inputs
inputs = InputsEnd(
    income=20000.0,
    retentions=225.90,
    projections=expend_table["proyeccion"].tolist(),
    real_values=expend_table["real"].tolist()
)

# Calculate results
print(calculate(inputs, ir_table))
```

2. **Command Line Interface (CLI)**

Run the CLI script with `income` and `retentions` as arguments (`--prety` shows the result as a table):

```bash
python src/cli.py 20000 225.90 --pretty
```

```powershell
python .\src\cli.py 20000 225.90 --pretty
```

Example result:

```text
Valores
Base imponible proyectada           15000.0
Base imponible real                 15600.0
Impuesto proyectado                   225.9
Impuesto real                         285.9
Retenciones                           225.9
Total a pagar                          60.0
Diferencia entre real y proyectado     60.0
```

---

## 📖 Notes

- The project uses NumPy-style docstrings for clarity and maintainability.
- Data files (`tabla_ir.csv`, `gastos.csv`, `gastos_second_case.csv` `gastos_proy.csv`) must follow the expected schema (see examples in `data/`).

---