import json
import os
import pathlib


class ExportingData():
    exporting = []
    data_Keys = ['type', 'data']
    directory_path = pathlib.Path(os.getcwd()).joinpath("obj")
    file_path = directory_path.joinpath("data.json")

    def __init__(self):
        try:
            assert os.path.isdir(self.directory_path)
        except AssertionError:
            print(f'The directory {self.directory_path} does not exist.')

    def add_data(self, data_type: str, data_values: str):
        """
        Function for adding data to the object prior to exporting the data and running the app.

        Parameters
        ----------
        type : str
            Either 'figur' if Altair chart or 'tabel' if table.
        data : str
            Data represented as a string. Json if the data represents an Altair chart or in HTML if the data
            represents a table.

        Returns
        -------
        dict

        Examples
        --------
        >>> ED = ExportingData()
        >>> ED.add_data(data_type='figur', data_values=chart_cars.to_json())
        >>> ED.add_data(data_type='tabel', data_values=cars.head().to_html(classes='table is-striped is-hoverable')
        >>> print(ED.exporting)
        [xxxx]
        """

        if self.validate_input(data_type, data_values):
            _data = {'type': data_type, 'data': data_values}
            self.exporting.append(_data)
        return self

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.exporting, f)

    def validate_input(self, data_type, data_values) -> bool:
        try:
            assert isinstance(data_type, str)
            assert isinstance(data_values, str)
        except AssertionError:
            print(
                f'Inputs to the method {ExportingData.__name__}.{ExportingData.add_data.__name__} have to be strings.')
            return False
        return True

    def validate_output(self):
        try:
            assert isinstance(self.exporting, list)
        except AssertionError:
            print("Error message.")
            return False

        try:
            assert all([isinstance(i, dict) for i in self.exporting])
        except AssertionError:
            print("Error message")
            return False
        return True
