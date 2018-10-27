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


def build_form(form_json):
  class DynamicForm(FlaskForm):
      submit = SubmitField('Submit')
      konklusion = PageDownField('Konklusion')
      pass
  d = DynamicForm

  for i in form_json:
      setattr(d, i, PageDownField())
  return d()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = build_form(["form0", "form1"])

    graph_data = import_data()

    text = None
    konklusion = None

    if form.validate_on_submit():
        text = []
        konklusion = Markup(markdown.markdown(form.konklusion.data))
        for i in range(len(graph_data)):
            text.append(Markup(markdown.markdown(form[f'form{i}'].data)))
    else:
        for i in ["form0", "form1"]:
            form[i].data = (i)
    return render_template('index.html', form=form, graph_data=graph_data, text=text, konklusion=konklusion)


if __name__ == '__main__':
    app.run(debug=True)
