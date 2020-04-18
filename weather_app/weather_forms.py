from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from weather_app.weather_models import City


class CityForm(FlaskForm):
    city_name = StringField('City Name', render_kw={"placeholder":"Enter the City Name"}, 
    validators=[DataRequired(),Length(min=1,max=30)])
    submit = SubmitField('Add')

    def validate_city_name(self, city_name):
        city = City.query.filter_by(city_name = city_name.data).first()
        if city:
            raise ValidationError('City already present in list.')