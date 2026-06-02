from src.model import InputsEnd, load_ir_table, load_expend_table, calculate
from pathlib import Path
import pandas as pd
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Ecuador Income Tax (IR) Calculator")
    parser.add_argument("income", type=float, help="Annual income")
    parser.add_argument("retentions", type=float, help="Total retentions")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Format output as a table instead of raw dict"
    )
    
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    # Define project root relative to this file
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    # Paths to the required data
    path_ir = PROJECT_ROOT / "data" / "tabla_ir.csv"
    path_expend = PROJECT_ROOT / "data" / "gastos.csv"

    # Load tables
    ir_table = load_ir_table(path_ir)
    expend_table = load_expend_table(path_expend)

    # Build inputs
    inputs = InputsEnd(
        income=args.income,
        retentions=args.retentions,
        projections=expend_table["proyeccion"].tolist(),
        real_values=expend_table["real"].tolist()
    )

    # Calculate results
    result = calculate(inputs, ir_table)

    # Output
    if args.pretty:
        tb = pd.Series(result).to_frame(name="Valores")
        print(tb)
    else:
        print(result)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"Error: {e}")
