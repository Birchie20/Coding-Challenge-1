import pytest
from datetime import datetime as dt
import produce_report


def test_ProduceReport_Standard():
    """Checks that a report is produced and is correct using input which should work"""

    pr = produce_report.ProduceReport('report_1', 
                                      dt(2019,9,29), 
                                      'Client1', 
                                      'CSV', 
                                      file_path = "Testing/Test_Data/Test_Data_0_Correct/")

    assert pr.produce_report() == {"customers": 5,
                                   'items': 1544,
                                   'total_discount_amount': 12999485.95,
                                   'discount_rate_avg': 0.18,
                                   'order_total_avg': 12515188.46,
                                   'commissions': {'total': 8248738.27,
                                                   'order_average': 1649747.65,
                                                   'promotions': {"1": 0.0,
                                                                  "2": 0.0,
                                                                  "3": 0.0,
                                                                  "4": 0.0,
                                                                  "5": 0.0
                                                                  }
                                                   }
                                   }




def test_ProduceReport_promos():
    """Checks that a report is produced and is correct using input which should generate promotions values"""

    pr = produce_report.ProduceReport('report_1', 
                                    dt(2019,8,12), 
                                    'Client1', 
                                    'CSV', 
                                    file_path = "Testing/Test_Data/Test_Data_0_Correct/")
    
    test = pr.produce_report()
    test_1 = 1

    assert pr.produce_report() == {"customers": 10,
                                   'items': 3482,
                                   'total_discount_amount': 22125711.15,
                                   'discount_rate_avg': 0.13,
                                   'order_total_avg': 16750783.60,
                                   'commissions': {'total': 22513046.63,
                                                   'order_average': 2251304.66,
                                                   'promotions': {"1": 15424.10,
                                                                  "2": 0.0,
                                                                  "3": 0.0,
                                                                  "4": 0.0,
                                                                  "5": 61254.21
                                                                  }
                                                   }
                                   }