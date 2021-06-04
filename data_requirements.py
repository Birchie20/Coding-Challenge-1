from datetime import datetime as dt
import pandas as pd


class DataRequirements(object):
    """
    Used as the base class from which individual client classes can inherit in order to establish
    which files are required in order to run reports for the client in question

    Depending upon whether reports are standard accross clients or or not you may wish to change
    this implementation and use another.
    """
    def __init__(self):
        self._required_file_names = None
        self._report_requirements = None
    
    def get_data_requirements(self, report):
        """
        Used to determine which data files are required to generate the report(s) requested by the user
        """

        if isinstance(report, str):
            try:
                self._required_file_names = self._report_requirements[report]
            except:
                raise ValueError(f"{report} does not exist for this client")
        else:
            raise ValueError(f"Report requested must be entered either as a string")

        
       
    @property
    def required_file_names(self):
        return self._required_file_names


class DataRequirementsClient1(DataRequirements):
    """
    Class stores all the data files that are required per report for Client1

    If the data requirements change at all then you will need to update the collections in this class
    to reflect the updated data requirements.
    """   

    def __init__(self):
        self._required_file_names = None
        self._report_requirements = {'report_1': ('commissions',
                                                'order_lines', 
                                                'orders', 
                                                'product_promotions', 
                                                'products', 
                                                'promotions')
                                    }

        





class DataRequirementsFactory(object):
    """Used to determine which classes are needed to generate files"""

    def __init__(self, client):
        self._client = client


    def create_data_retrieval_object(self):
        """
        Uses conditions to determine which data retrieval object to create
        """

        if self._client == 'Client1':
            return DataRequirementsClient1()
        else:
            raise ValueError(f"The client you are running the report for ({self.client}) is not recognised - please contact the helpdesk")


class FileDataRequirements(object):
    """
    Used to validate that the data files ingested all have the required columns present

    If the data requirements vary by client, or the list gets too long 
    then you may need to think about using a design pattern 
    to better allow for this
    """
    
    field_requirements = {'commissions': {'date': dt,
                                         'vendor_id': int,
                                         'rate': float},
                          'order_lines': {'order_id': int, 
                                          'product_id': int, 
                                          'product_description':str, 
                                          'product_price':float,
                                          'product_vat_rate': float,
                                          'discount_rate': float,
                                          'quantity': int,
                                          'full_price_amount': float,
                                          'discounted_amount': float,
                                          'vat_amount': float,
                                          'total_amount': float}, 
                          'orders': {'id':int,
                                     'created_at': dt,
                                     'vendor_id': int,
                                     'customer_id': int}, 
                          'product_promotions': {'date': dt,
                                                 'product_id': int,
                                                 'promotion_id': int}, 
                          'products': {'id': int,
                                       'description': str}, 
                          'promotions':  {'id':int,
                                          'description': str}
        }

    def __init__(self):
        self._required_file_names = None
        self._data = None


    def check_and_format_fields(self, data_obj):       
        """
        Performs the check on the fields present in the files against those that we need in order to produce
        the report(s)

        Also formats the columns of each file ready for processing

        Better error handling could be implemented using pandas built in error handling with more time and
        if neccessary
        """

        self._data_obj = data_obj

        
        missing_fields_dict = {}
        null_entries_list= []
        for file in self._required_file_names:
            fields_present = list(getattr(data_obj.data, file).columns)
            missing_fields = [field for field in self.field_requirements[file].keys() if field not in fields_present]
            if missing_fields:
                missing_fields_dict[file] = missing_fields
            else:
                try:
                    getattr(data_obj.data, file).astype({k:v for k, v in self.field_requirements[file].items() if isinstance(v, (str, int, float))})  # Format the data columns where str, int or float
                except:
                    raise ValueError(f"Unable to format data to correct format in file {file}")
                datetime_field_list = [k for k,v in self.field_requirements[file].items() if v == dt]
                if datetime_field_list:
                    try:
                        getattr(data_obj.data, file)[datetime_field_list] = getattr(data_obj.data, file)[datetime_field_list].apply(pd.to_datetime)
                    except:
                        raise ValueError(f"Unable to cast an entry in a date field to a date in file {file}")
                nulls = getattr(data_obj.data, file).isnull().sum().sum()
                if nulls > 0:
                    null_entries_list.append(file)
                        

        if missing_fields_dict:
            error_field_strings = {k:k+':\n\t'+',\n\t'.join(missing_fields_dict[k]) for k in missing_fields_dict.keys()}
            error_field_string = '.\n'.join(error_field_strings.values())
            raise ValueError(f"The following columns were not present in the files shown: \n{error_field_string}\n\n Please update and try again")
        
        if null_entries_list:
            null_file_string = '\n'.join(null_entries_list)
            raise ValueError(f"The following files contained empty fields: \n\n{null_file_string}\n\n Please update and try again")

    @property
    def required_file_names(self):
        return self._required_file_names

    @required_file_names.setter
    def required_file_names(self, new_required_file_names):
        self._required_file_names = new_required_file_names

