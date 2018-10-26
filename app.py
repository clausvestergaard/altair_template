from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
import markdown
from flask import Markup

from flask import request

import os
import json


# Based on https://github.com/miguelgrinberg/Flask-PageDown/tree/master/example


# IMPORT DATA
def import_data():
    file_path = f'{os.getcwd()}/obj/data.json'
    try:
        with open(file_path, 'rb') as f:
            _data = json.load(f)
        return _data
    except FileNotFoundError:
        print(f'Filen {file_path} findes ikke.')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
PageDown(app)


class PageDownFormExample(FlaskForm):
    textfield = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

class PageDownFormSubmit(FlaskForm):
    submit = SubmitField('Submit')




@app.route('/', methods=['GET', 'POST'])
def index():
    formsubmit = PageDownFormSubmit()
    form = {f'form{i}': PageDownFormExample(f'form{i}') for i in range(len(import_data()))}

    graph_data = import_data()
    for i in range(len(graph_data)):
        form[f'form{i}'].textfield.name = f'textfield_{i}'
    data = None
    text = []
    konklusion = None

    if formsubmit.validate_on_submit():

        for i in range(len(graph_data)):
                data = form
                text.append(Markup(markdown.markdown(data[f'form{i}'].textfield.data)))
    else:
        for i in range(len(graph_data)):
            form[f'form{i}'].textfield.data = (f'form{i}')

    return render_template('index_ite.html', form=form, data=data, graph_data=graph_data, text=text, konklusion=konklusion, formsubmit=formsubmit)


if __name__ == '__main__':
    app.run(debug=True)
