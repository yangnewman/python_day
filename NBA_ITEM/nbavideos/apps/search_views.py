from flask import jsonify, Blueprint, redirect, request, render_template, url_for
from apps.models import db, Nba

search_blue = Blueprint('nba', __name__)


# @search_blue.route('/', methods=['GET'])
# def nba_index():
#     return redirect(url_for('nba.index'))
#
#
# @search_blue.route('/hello/', methods=['GET'])
# def hello():
#     return 'hello'


# @search_blue.route('/get_search/', methods=['GET'])
# def get_search():
#     sql = 'select * from nba order by time desc limit 9;'
#     # sql = 'select * from nba;'
#     db_obj = db.session.execute(sql)
#     db_all = db_obj.fetchall()
#     result= []
#     for item in db_all:
#         nba_item = {}
#         nba_item['title'] = item[1]
#         nba_item['image'] = item[2]
#         nba_item['time'] = item[3]
#         nba_item['url'] = item[4]
#         result.append(nba_item)
#     return jsonify({'code':200, 'video':result})


# @search_blue.route('/get_all/', methods=['GET'])
# def get_all():
#     sql = 'select * from nba;'
#     # sql = 'select * from nba;'
#     db_obj = db.session.execute(sql)
#     db_all = db_obj.fetchall()
#     if len(db_all) > 120:
#         sql = 'select * from nba order by time desc limit 120;'
#         # sql = 'select * from nba;'
#         db_obj = db.session.execute(sql)
#         db_all = db_obj.fetchall()
#     result = []
#     for item in db_all:
#         nba_item = {}
#         nba_item['title'] = item[1]
#         nba_item['image'] = item[2]
#         nba_item['time'] = item[3]
#         nba_item['url'] = item[4]
#         result.append(nba_item)
#     return jsonify({'code': 200, 'video': result})


@search_blue.route('/index/', methods=['get'])
def index():
    # page定义当前页码
    page = int(request.args.get('page', 1))
    # per_page定义每页显示的条数
    per_page = int(request.args.get('per_page', 12))
    # 是个对象paginate:<flask_sqlalchemy.Pagination object>
    # paginate = Nba.query.order_by('-s_id').paginate(page, per_page, error_out=False)
    # 必要步骤
    paginate = Nba.query.order_by('time desc').paginate(page, per_page, error_out=False)
    # 获取全部学生对象
    videos = paginate.items
    return render_template('show-page.html', paginate=paginate, videos=videos)


@search_blue.route('/get_search/<input>/', methods=['get'])
def get_search(input):
    # page定义当前页码
    page = int(request.args.get('page', 1))
    # per_page定义每页显示的条数
    per_page = int(request.args.get('per_page', 12))
    # 是个对象paginate:<flask_sqlalchemy.Pagination object>
    # paginate = Nba.query.order_by('-s_id').paginate(page, per_page, error_out=False)
    # 必要步骤
    paginate = Nba.query.filter(Nba.title.like('%{}%'.format(str(input)))).order_by('time desc').paginate(page, per_page, error_out=False)
    # 获取全部学生对象
    videos = paginate.items

    return render_template('search-page.html', paginate=paginate, search_data=input)





