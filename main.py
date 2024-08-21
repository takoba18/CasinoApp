from pathlib import Path

from core import CasinoCore

if __name__ == "__main__":
    input_dir = Path("/data")
    input_file_name = "transactions.txt"
    output_file_name = "results.txt"
    casino_core = CasinoCore(input_dir=input_dir, input_file_name=input_file_name, output_file_name=output_file_name,
                             verbose=False)
    casino_core()
