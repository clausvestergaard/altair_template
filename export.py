import json
import os
import pathlib


class ExportingData():
    exporting = []
    data_Keys = "'type, 'data'"

    def add_data(self, type: str, data: str):
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
        >>> ED.add_data(type='figur', data=chart_cars.to_json())
        >>> ED.add_data(type='tabel', data=cars.head().to_html(classes='table is-striped is-hoverable')
        >>> print(ED.exporting)
        [xxxx]
        """

        #if self.validate_input(type, data):
        _data = {'type': type, 'data': data}
        self.exporting.append(_data)
        return self

    def save_data(self):
        path = f'{pathlib.Path(os.getcwd()).joinpath("obj/data.json")}'
        with open(path, 'w') as f:
            json.dump(self.exporting, f)

    #def validate_input(self, data) -> bool:
    #    try:
    #        assert isinstance(data, dict)
    #    except AssertionError:
    #        print("You have to add the data in the format of a dict with the following keys")
    #        return False

# isinstance(data, list)
# {k for d in LoD for k in d.keys()}
