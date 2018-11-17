from flask import Flask, render_template, Markup, request
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
from markdown import markdown

import os
import json


# IMPORT DATA
def import_data():
    file_path = f'{os.getcwd()}/obj/data.json'
    try:
        with open(file_path, 'rb') as f:
            _data = json.load(f)
        if import_data_validate(_data, file_path):
            return _data

    except FileNotFoundError:
        print(f'The file {file_path} does not exists.')


def import_data_validate(_data, file_path) -> bool:
    try:
        assert isinstance(_data, list)
    except AssertionError:
        print(f'The file {file_path} is not in a valid format.')
        return False
    return True


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
PageDown(app)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def build_form(data_json):
    class DynamicForm(FlaskForm):
        submit = SubmitField('Submit')
        conclusion = PageDownField('Conclusion')
        pass

    d = DynamicForm

    for i in data_json:
        setattr(d, i, PageDownField())
    return d()


@app.route('/', methods=['GET', 'POST'])
def index():
    # Import data.
    graph_data = import_data()

    # Initialize form and fields.
    form_fields = [f'form{i}' for i in range(len(graph_data))]
    form = build_form(form_fields)
    text = None
    conclusion = None

    if form.validate_on_submit():
        text = []
        for i in range(len(graph_data)):
            text.append(Markup(markdown(form[f'form{i}'].data)))
        conclusion = Markup(markdown(form.conclusion.data))
        shutdown_server()
    else:
        for idx, i in enumerate(form_fields):
            if not graph_data[idx]["text"]:
                graph_data[idx]["text"] = 'Default text'
            form[i].data = graph_data[idx]["text"]
    return render_template('index.html', form=form, graph_data=graph_data, text=text, conclusion=conclusion,
                           form_fields=form_fields)


if __name__ == '__main__':
    app.run(debug=True)
