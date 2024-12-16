import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY') or 'BREVO_API_KEY'
