import pytest
import data_requirements






@pytest.fixture()
def dr():
    dr = data_requirements.DataRequirementsClient1()
    return dr


def test_GetDataRequirements_Standard(dr):
    """Checks that the file names are returns as required_file_names property """
    dr.get_data_requirements('report_1')

    assert dr.required_file_names == ('commissions',
                                      'order_lines', 
                                      'orders', 
                                      'product_promotions', 
                                      'products', 
                                      'promotions')

def test_GetDataRequirements_IncorrectReportName(dr):
    """Check that if report name is not recognised an exception error is raised"""
    with pytest.raises(Exception) as exc_info:
        dr.get_data_requirements('report_15')
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "report_15 does not exist for this client"



def test_GetDataRequirements_NonStringReportName(dr):
    """Check that if report name is not recognised an exception error is raised"""
    with pytest.raises(Exception) as exc_info:
        dr.get_data_requirements(15.45)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "Report requested must be entered either as a string"
