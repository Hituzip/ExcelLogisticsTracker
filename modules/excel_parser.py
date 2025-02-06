import numpy as np
import pandas as pd


def parse_float(value) -> float:
    """Обрабатывает входные данные, преобразуя их в float."""
    if pd.isna(value):  # Проверка на NaN (работает с pandas и numpy)
        return 0.0
    if isinstance(value, str):
        return float(value.replace(',', '.')) if value.replace(',', '.').replace('.', '', 1).isdigit() else 0.0
    if np.issubdtype(type(value), np.number):  # Проверяем, является ли число numpy-типом
        return float(value)
    return 0.0