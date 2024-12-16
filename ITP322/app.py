from flask import Flask, render_template, flash, redirect, url_for, request
import requests
import os
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY') or 'BREVO_API_KEY'
    BREVO_API_URL = "https://api.sendinblue.com/v3/smtp/email"


app = Flask(__name__)
app.config.from_object(Config)

# Registration form
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')


def send_confirmation_email(name, email):
    headers = {
        'accept': 'application/json',
        'api-key': app.config['BREVO_API_KEY'],
        'content-type': 'application/json',
    }
    data = {
        "sender": {"name": "Event Setter", "email": "oliquianomark111@gmail.com"},
        "to": [{"email": email, "name": name}],
        "subject": "Event Registration Confirmation",
        "htmlContent": f"<h1>Event Name: {name}</h1><p>Your event is successfully registered.</p>"
    }
    response = requests.post(app.config['BREVO_API_URL'], headers=headers, json=data)
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        response = send_confirmation_email(name, email)
        if response.status_code == 201:
            flash('A confirmation email has been sent to you.', 'success')
        else:
            flash('Failed to send confirmation email. Please try again later.', 'danger')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
