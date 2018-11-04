from export import ExportingData


def test_add_data_method_populates_exporting_list(raw_data, chart):
    ED = ExportingData()
    ED.add_data(data_type='figur', data_values=chart.to_json())
    ED.add_data(data_type='tabel', data_values=raw_data.to_html())

    _keys = {k for i in ED.exporting for k in i.keys()}

    assert isinstance(ED.exporting, list)
    assert {'type', 'data'} == _keys

