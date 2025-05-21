from dotenv import load_dotenv
import os
load_dotenv()


SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

def configure_app(app): 
    app.config['HOST'] = '0.0.0.0'
    app.config['PORT'] = 5000
    app.config['DEBUG'] = True