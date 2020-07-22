from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class usermessage(db.Model):
    __tablename__ = 'user_active_log'
    id = db.Column(db.String(50), primary_key=True)
    user_name = db.Column(db.String(50))
    message = db.Column(db.Text)
    date = db.Column(db.TIMESTAMP)

    def __init__(self
                 , id
                 , user_id
                 , message
                 , date
                 ):
        self.id = id
        self.user_id = user_name
        self.message = message
        self.date = date


if __name__ == '__main__':
    manager.run()
