from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired, Length(min=5, max=40)])
    submit = SubmitField('/search')
