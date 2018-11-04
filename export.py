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
        Basically just validating input and appending dictionaries to the list 'exporting'.

        Parameters
        ----------
        type : str
            Either 'figur' if Altair chart or 'tabel' if table.
        data : str
            Data represented as a string. Json if the data represents an Altair chart or in HTML if the data
            represents a table.


        Examples
        --------
        >>> ED = ExportingData()
        >>> ED.add_data(data_type='figur', data_values=chart_cars.to_json())
        >>> ED.add_data(data_type='tabel', data_values=cars.head().to_html(classes='table is-striped is-hoverable')
        """

        self.validate_input(data_type, data_values)

        _data = {'type': data_type, 'data': data_values}
        self.exporting.append(_data)
        return self

    def save_data(self):
        self.validate_output()
        with open(self.file_path, 'w') as f:
            json.dump(self.exporting, f)

    def validate_input(self, data_type, data_values) -> bool:
        try:
            assert isinstance(data_type, str)
            assert isinstance(data_values, str)
        except AssertionError:
            raise TypeError('Both data_type and data_values have to be of type str. '
                            f'Input was data_type: {type(data_type)} and data_values: {type(data_values)}.')

    def validate_output(self):
        try:
            assert isinstance(self.exporting, list)
            assert all([isinstance(i, dict) for i in self.exporting])
        except AssertionError:
            raise TypeError('exporting has to be a list of dictionaries.')
