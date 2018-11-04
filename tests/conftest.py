import pytest
import pandas as pd
import altair as alt


@pytest.fixture(scope='session', name='raw_data')
def _raw_data() -> pd.DataFrame:
    _data = pd.DataFrame({
        'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
    })
    return _data


@pytest.fixture(scope='session', name='chart')
def _chart(raw_data):
    cht = alt.Chart(raw_data).mark_bar().encode(
        x='a',
        y='b'
    )
    return cht


@pytest.fixture(scope='session', name='exported_data')
def _exported_data(raw_data, chart) -> list:
    tbl = raw_data.head().to_html(classes='table is-striped is-hoverable')

    exp_data = [{'type': 'figur', 'data': chart.to_json()}, {'type': 'tabel', 'data': tbl}]
    return exp_data
