import os
import sys
from io import StringIO
from typing import Dict


def validate_csv(csv: str):
    if csv and not os.path.exists(csv):
        csv = StringIO(csv)

    return csv


def write_csv(objects: Dict, filename: str):
    try:
        import pandas as pd

        df = pd.DataFrame(objects)
        df.to_csv(filename)
    except ImportError:
        pass

    try:
        import csv

        with open(filename, "w", encoding="utf8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=objects[0].keys())
            writer.writeheader()
            writer.writerows(objects)
    except ImportError:
        print("`pandas` or `csv` module are required to use `write_csv` function.")
        sys.exit(1)
