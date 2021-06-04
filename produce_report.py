import data_requirements
import data_extraction
import generate_data
from datetime import datetime as dt
import configuration

#report = 'report_1'
#client = 'Client1'
#file_path = 'data'
#data_base = None
#file_source = 'CSV'
#report_date = dt(2019,9,29)




def main():

    report_date = dt(2019,8,10)

    report = ProduceReport(configuration.report, report_date, configuration.client, configuration.file_source, file_path = configuration.file_path)
    report.produce_report()

    return report


class ProduceReport(object):
    """This is the top level class that oversee's the production of the report"""

    def __init__(self, report, report_date, client, file_source, file_path = None, data_base = None):
        self._report = report
        self._client = client
        self._file_source = file_source
        self._file_path = file_path
        self._data_base = data_base
        self._report_date = report_date
        
    
    def produce_report(self):
        """Top level method used to oversee the generation of the report requested"""
        
        
        report_data_requirements = data_requirements.DataRequirementsFactory(self._client)
        report_data_requirements_obj = report_data_requirements.create_data_retrieval_object()

        field_requirements_obj = data_requirements.FileDataRequirements()
        
        data = data_extraction.ExtractValidateDataFactory(self._file_source)
        data_obj = data.create_extract_validate_data_object(file_path = self._file_path)  # Can pass in multiple connection data via kwargs

        data_generator = generate_data.GenerateReportFactory(self._client, self._report)
        data_generator_obj = data_generator.create_report_generator_obj()

        #get output style generate class

        report = self.generate_report(report_data_requirements_obj, data_obj, field_requirements_obj, data_generator_obj)

        return report


    def generate_report(self, report_data_requirements_obj, data_obj, field_requirements_obj, data_generator_obj):
        """
        Inject all the objects needed to generate the report into this method and run their methods each in turn
        to generate the report(s) data
        """

        report_data_requirements_obj.get_data_requirements(self._report)
        
        data_obj.data_requirements = report_data_requirements_obj
        data_obj.get_data()

        field_requirements_obj.required_file_names = report_data_requirements_obj.required_file_names
        field_requirements_obj.check_and_format_fields(data_obj)

        report_data = data_generator_obj.produce_report_data(self._report_date, data_obj.data)

        return report_data


if __name__ == "__main__":
    main()