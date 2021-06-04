from abc import ABC, abstractmethod
import pandas as pd
import os
from Utilities import Utilities, DictObjectView

class IExtractValidateData(ABC):

    @abstractmethod
    def get_data(self, data_requirements):
        """Interface Method"""




class ExtractValidateDataCSV(IExtractValidateData):
    """
    This class is responsible for getting the data provided in a CSV format, 
    validating it, loading it and making it available
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
        self._data_requirements = None
        self.utilities = Utilities()
        self._data = None
        
    def get_data(self):
        """
        Used to go and retrieve and validate the data provided in the directory specified by the user
        """
        
        with os.scandir(self.file_path) as collection_of_files:
            files_found = [file.name.split('.')[0] for file in collection_of_files 
                           if (file.name.split('.')[0].lower().strip() in self._data_requirements.required_file_names 
                           and file.name.endswith('.csv'))]

        self.check_missing_files(files_found)
        
        self._data = DictObjectView(self.read_in_files(files_found))
            


        
    def check_missing_files(self, files_found):
        """
        If there are one or more files missing then this is used to establish which files are missing
        and return an error message to the user.
        
        It will also check (and share with the user) if it appears the files have simply been provided
        in the incorrect format.
        """
        
        name_formatted_files_found = [file_name.lower().strip() for file_name in files_found]  # Need files_found elements formatted to compare
        missing_files = [file for file in self._data_requirements.required_file_names 
                         if file not in name_formatted_files_found]
        
        if missing_files:

            with os.scandir(self.file_path) as collection_of_files:
                files_no_format_check = [file.name.split('.')[0].lower().strip() 
                                         for file in collection_of_files 
                                         if file.name.split('.')[0].lower().strip() 
                                         in self._data_requirements.required_file_names]  # Check for files regardless of file format

            if len(files_no_format_check) > len(files_found):
                wrong_format_files = [file_name for file_name in files_no_format_check 
                                      if file_name not in name_formatted_files_found]
                if wrong_format_files:
                    missing_files = [file + f" (found but not in csv format)" 
                                     if file in wrong_format_files else file for file in missing_files ]

            missing_file_string = ',\n'.join(missing_files)

            raise ValueError(f"Could not find the following required files in csv format:\n\n{missing_file_string}\n\nPlease ensure they are present and retry")

        
    def read_in_files(self, files_found):
        """
        Used to read in the files into pandas dataframes
        """
        
        file_data_dict = {file.lower().strip():self.utilities.catch_exception(pd.read_csv, self.file_path + file + '.csv')
                          for file in files_found}
        
        load_fail_files = [k for k,v in file_data_dict.items() if not isinstance(v, pd.DataFrame)]
        
        if load_fail_files:
            load_fail_files_string = ',\n'.join(load_fail_files)
            raise ValueError(f"Unable to load the following files: \n\n{load_fail_files_string}\n\nPlease check the data format in these files")
            
        return file_data_dict


    @property
    def data(self):
        return self._data

    @property
    def data_requirements(self):
        return self._data_requirements

    @data_requirements.setter
    def data_requirements(self, new_data_requirements):
        self._data_requirements = new_data_requirements


class ExtractValidateDataFactory(object):
    """Used to determine which classes are needed to extract data"""

    def __init__(self, file_source):
        self._file_source = file_source


    def create_extract_validate_data_object(self, **kwargs):
        """
        Uses conditions to determine which data retrieval object to create
        """

        if self._file_source.lower() == 'csv':
            if 'file_path' not in kwargs:
                raise ValueError(f"When reading in from csv files you must provide a file_path")
            return ExtractValidateDataCSV(kwargs['file_path'])
        else:
            raise ValueError(f"We can not currently cater for {self._file_source} file types, please use csv format files")