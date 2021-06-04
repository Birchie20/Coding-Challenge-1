import pytest
import data_requirements
from datetime import datetime as dt
import data_extraction
import data_requirements
import numpy as np

@pytest.fixture()
def dr():
    dr = data_requirements.DataRequirementsClient1()
    dr.get_data_requirements('report_1')
    return dr



def test_FileDataRequirements_Standard(dr):
    """Check that the file is formatting the data correctly"""
    
    fdr = data_requirements.FileDataRequirements()
    fdr.required_file_names = dr.required_file_names
    
    de = data_extraction.ExtractValidateDataCSV("Testing/Test_Data/Test_Data_0_Correct/")
    de.data_requirements = dr
    de.get_data()

    fdr.check_and_format_fields(de)
    assert de.data.commissions.date.dtype == np.dtype('datetime64[ns]')
    


def test_FileDataRequirements_MissingField(dr):
    """Check that an error is raised is fields are missing from files"""
    
    fdr = data_requirements.FileDataRequirements()
    fdr.required_file_names = dr.required_file_names
    
    de = data_extraction.ExtractValidateDataCSV("Testing/Test_Data/Test_Data_2_Missing_Field/")
    de.data_requirements = dr
    de.get_data()

    with pytest.raises(Exception) as exc_info:
        fdr.check_and_format_fields(de)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "The following columns were not present in the files shown: \norder_lines:\n\tproduct_id,\n\tquantity.\norders:\n\tvendor_id\n\n Please update and try again"



def test_FileDataRequirements_Missingcell(dr):
    """Check that an error is raised is cells are empty in file(s)"""
    
    fdr = data_requirements.FileDataRequirements()
    fdr.required_file_names = dr.required_file_names
    
    de = data_extraction.ExtractValidateDataCSV("Testing/Test_Data/Test_Data_3_Missing_Cell/")
    de.data_requirements = dr
    de.get_data()

    with pytest.raises(Exception) as exc_info:
        fdr.check_and_format_fields(de)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "The following files contained empty fields: \n\nproduct_promotions\n\n Please update and try again"


