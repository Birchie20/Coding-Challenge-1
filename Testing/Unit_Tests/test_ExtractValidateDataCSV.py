import pytest
import data_requirements
import data_extraction
import pandas as pd
from pandas.util.testing import assert_frame_equal 

@pytest.fixture()
def dr():
    dr = data_requirements.DataRequirementsClient1()
    dr.get_data_requirements('report_1')
    return dr


def test_ExtractValidateDataCSV_CorrectData(dr):
    de = data_extraction.ExtractValidateDataCSV("Testing/Test_Data/Test_Data_0_Correct/")
    de.data_requirements = dr
    de.get_data()
    assert_frame_equal(de.data.commissions, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/commissions.csv"))
    assert_frame_equal(de.data.order_lines, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/order_lines.csv"))
    assert_frame_equal(de.data.orders, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/orders.csv"))
    assert_frame_equal(de.data.product_promotions, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/product_promotions.csv"))
    assert_frame_equal(de.data.products, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/products.csv"))
    assert_frame_equal(de.data.promotions, pd.read_csv("Testing/Test_Data/Test_Data_0_Correct/promotions.csv"))


def test_ExtractValidateDataCSV_MissingFile(dr):
    de = data_extraction.ExtractValidateDataCSV("Testing/Test_Data/Test_Data_1_Missing_File/")
    de.data_requirements = dr
    with pytest.raises(Exception) as exc_info:
        de.get_data()
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "Could not find the following required files in csv format:\n\ncommissions\n\nPlease ensure they are present and retry"

