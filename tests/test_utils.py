import os
from quantcast_cli.utils import temp_csv_file


def test_temp_csv_file_creates_file_with_correct_data():
    test_data = "column1,column2\nvalue1,value2"
    with temp_csv_file(test_data) as temp_file:
        assert os.path.exists(temp_file.name), "Temporary file does not exist."
        with open(temp_file.name, "r") as file:
            content = file.read()
            assert content == test_data, "File content does not match expected data."


def test_temp_csv_file_creates_csv_file():
    test_data = "header1,header2\nrow1data1,row1data2"
    with temp_csv_file(test_data) as temp_file:
        assert temp_file.name.endswith(".csv"), "File does not have a .csv extension."


def test_temp_csv_file_deletes_file_after_exit():
    with temp_csv_file("sample_data") as temp_file:
        temp_file_path = temp_file.name
    assert not os.path.exists(temp_file_path), "Temporary file was not deleted."


def test_temp_csv_file_with_error_inside_context():
    test_data = "this,is,test,data"
    try:
        with temp_csv_file(test_data) as temp_file:
            temp_file_path = temp_file.name
            raise Exception("Simulation Fake Error")
    except Exception:
        pass

    assert not os.path.exists(
        temp_file_path
    ), "Temporary file was not deleted after an error inside the context."
