from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)
if 'VCAP_SERVICES' in os.environ:
  import json
  vcap_services = json.loads(os.environ['VCAP_SERVICES'])
  mysql_srv = vcap_services['cleardb'][0]
  cred = mysql_srv['credentials']
  mysql_uri = "mysql+pymysql://"+cred['username']+":"+cred['password']+"@"+cred['hostname']+":"+cred['port']+"/"+cred['name']
  app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'

print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
