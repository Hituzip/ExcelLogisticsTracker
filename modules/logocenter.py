import os
from typing import Union
import pandas as pd

from modules.excel_parser import parse_float


def logocenter_column_sum(file: Union[str, os.PathLike], column: str) -> float:
    """Суммирует данные в указанном столбце Excel."""
    df = pd.read_excel(file, usecols=column)
    return sum(map(parse_float, df.values.flatten()))  # Преобразуем в одномерный массив