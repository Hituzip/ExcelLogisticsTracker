import os
from typing import Union

import pandas as pd

from modules.excel_parser import parse_float


def dry_column_sum(file: Union[str, os.PathLike], columns: str) -> dict:
    df = pd.read_excel(file, dtype=str, usecols=columns)
    sd = {}
    for i, b in df.values:
        if i.startswith('Слябы'):
            i = "Слябы"
        if i in sd.keys():
            sd[i] += parse_float(b)
        else:
            sd[i] = parse_float(b)
    return sd