from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SearchField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя:", validators=[DataRequired()])
    email = StringField("Электронная почта:", validators=[Email()])
    password = StringField("Пароль:", validators=[InputRequired()])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField("Электронная почта:", validators=[Email()])
    password = StringField("Пароль:", validators=[InputRequired()])
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):
    search = SearchField("Поиск по названию:")
    categories = SelectField("Поиск по категории:")
    submit = SubmitField("Найти")
