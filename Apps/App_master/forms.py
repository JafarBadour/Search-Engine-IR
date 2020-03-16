from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    query = StringField('Query for search :: please use normal text', validators=[DataRequired, Length(min=5, max=40)])
    submit = SubmitField('Search query')


class DocQuery(FlaskForm):
    query = StringField('Query for a doc please use the format (reut2-0DD/N.txt) for example reut2-000/1.txt', validators=[DataRequired, Length(min=5, max=40)])
    submit = SubmitField('Search Doc')

