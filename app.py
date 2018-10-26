from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
import markdown
from flask import Markup

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
    tekstfelt1 = PageDownField('Enter your markdown')
    tekstfelt2 = PageDownField('Enter your markdown')
    konklusion = PageDownField('Angiv eventuel konklusion')

    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PageDownFormExample()
    graph_data = import_data()
    data = None
    text = None
    konklusion = None

    if form.validate_on_submit():
        data = form
        text = [Markup(markdown.markdown(data.tekstfelt1.data)),
                Markup(markdown.markdown(data.tekstfelt2.data))]
        konklusion = Markup(markdown.markdown(data.konklusion.data))
    else:

        form.tekstfelt1.data = ('# This is demo #1 of Flask-PageDown\n'
                                '**Markdown** is rendered on the fly in the '
                                '<i>preview area below</i>!')
        form.tekstfelt2.data = ('# This is demo #2 of Flask-PageDown\nThe '
                                '*preview* is rendered separately from the '
                                '*input*, and in this case it is located above.')
        form.konklusion.data = ('Skriv din *konklusion*')
    return render_template('index.html', form=form, data=data, graph_data=graph_data, text=text, konklusion=konklusion)


if __name__ == '__main__':
    app.run(debug=True)
