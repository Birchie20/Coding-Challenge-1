import pytest
import data_requirements
import data_extraction


def test_ExtractValidateDataFactory_csv():
    """Test that correct class produced when looking to load from a csv"""
    de = data_extraction.ExtractValidateDataFactory('csv')
    assert isinstance(de.create_extract_validate_data_object(file_path = 'Testing/Test_Data/Test_Data_0_Correct/'), data_extraction.ExtractValidateDataCSV)


def test_ExtractValidateDataFactory_no_file_path():
    """Test that error produced when looking to load from a csv and no file_path supplied"""
    de = data_extraction.ExtractValidateDataFactory('csv')
    with pytest.raises(Exception) as exc_info:
        de.create_extract_validate_data_object()
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "When reading in from csv files you must provide a file_path"

def test_ExtractValidateDataFactory_non_csv():
    """Test that error produced when looking to load from a non CSV source"""
    de = data_extraction.ExtractValidateDataFactory('xlxs')
    with pytest.raises(Exception) as exc_info:    
        de.create_extract_validate_data_object()
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "We can not currently cater for xlxs file types, please use csv format files"

    


