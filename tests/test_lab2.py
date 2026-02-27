from src.dtw_lab.lab2 import get_statistic
import pandas as pd
import pytest
from dtw_lab.lab1 import calculate_statistic, encode_categorical_vars

def test_calculate_statistic():
    df = pd.DataFrame({"Charge_Left_Percentage": [39, 60, 30, 30, 41]})
    assert calculate_statistic("mean", df["Charge_Left_Percentage"]) == 40
    assert calculate_statistic("median", df["Charge_Left_Percentage"]) == 39
    assert calculate_statistic("mode", df["Charge_Left_Percentage"]) == 30

def test_encode_categorical_vars():
    df = pd.DataFrame({
        "Battery_Size": ["AAA", "AA", "C", "D"],
        "Discharge_Speed": ["Slow", "Medium", "Fast", "Slow"],
        "Manufacturer": ["A", "B", "C", "A"]
    })
    encoded_df = encode_categorical_vars(df)
    assert encoded_df["Battery_Size"].tolist() == [1, 2, 3, 4]
    assert encoded_df["Discharge_Speed"].tolist() == [1, 2, 3, 1]
    assert all(col in encoded_df.columns for col in ["Manufacturer_A", "Manufacturer_B", "Manufacturer_C"]) 