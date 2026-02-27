import pandas as pd

from dtw_lab.lab1 import encode_categorical_vars, read_csv_from_google_drive


def test_encode_categorical_vars_with_mock_dataset():
    df = pd.DataFrame({
        "Battery_Size": ["AAA", "AA", "C", "D"],
        "Discharge_Speed": ["Slow", "Medium", "Fast", "Slow"],
        "Manufacturer": ["A", "B", "C", "A"]
    })

    encoded_df = encode_categorical_vars(df)

    assert encoded_df["Battery_Size"].tolist() == [1, 2, 3, 4]
    assert encoded_df["Discharge_Speed"].tolist() == [1, 2, 3, 1]
    assert all(col in encoded_df.columns for col in ["Manufacturer_A", "Manufacturer_B", "Manufacturer_C"])


def test_read_csv_from_google_drive_mocks_requests_get(mocker):
    file_id = "fake_file_id"
    expected_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    fake_csv = "Battery_Size,Discharge_Speed\nAAA,Slow\nAA,Medium\n"

    mock_get = mocker.patch("dtw_lab.lab1.requests.get")
    mock_get.return_value.content = fake_csv.encode("utf-8")

    result_df = read_csv_from_google_drive(file_id)

    assert result_df.shape == (2, 2)
    assert result_df["Battery_Size"].tolist() == ["AAA", "AA"]
    assert result_df["Discharge_Speed"].tolist() == ["Slow", "Medium"]
    assert mock_get.called
    mock_get.assert_called_once_with(expected_url)