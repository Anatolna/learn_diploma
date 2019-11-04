from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Inputform(FlaskForm):
    domain = StringField('Введите домен', validators=[DataRequired()],
                         render_kw={'class': 'form_control'})
    submit = SubmitField('Поехали', render_kw={'class': 'btn btn-success'})
