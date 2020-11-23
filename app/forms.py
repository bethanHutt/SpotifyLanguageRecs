import wtforms
import flask_wtf


class CountryForm(flask_wtf.FlaskForm):
    country = wtforms.SelectField('Choose a Country:')
    submit = wtforms.SubmitField('Generate Playlist')
