

from flask import Flask

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.models import db
from apps.search_views import search_blue

app = Flask(__name__)

app.register_blueprint(blueprint=search_blue, url_prefix='/nba/')

app.config['SECRET_KEY']= 'sadjahfgkjn2'
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/crawler01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)

# 配置migrate
migrate = Migrate(app=app, db=db)

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

