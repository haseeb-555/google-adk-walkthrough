# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CityForm(FlaskForm):
    city = StringField("City", validators=[
        DataRequired(message="City name cannot be empty."),
        Length(max=20, message="City name cannot exceed 20 characters.")
    ])
    submit = SubmitField("Submit")
