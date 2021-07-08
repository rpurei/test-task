from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify
import pymysql
import redis
from config import *
from pymed import PubMed
import json
from forms import SearchForm


app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)

cache = redis.Redis(host='redis', port=6379)
conn = pymysql.connect(host=MYSQL_DATABASE_HOST, user=MYSQL_DATABASE_USER, passwd=MYSQL_DATABASE_PASSWORD,
                                 db=MYSQL_DATABASE_DB)
if conn:
    DB_CONNECTION = True
    conn.close()


def article_save(art_id, art_title, art_keywords, art_abstract, art_date):
    connection = None
    try:
        connection = pymysql.connect(host=MYSQL_DATABASE_HOST, user=MYSQL_DATABASE_USER, passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB)
        with connection:
            cursor = connection.cursor()
            cursor.callproc('insertarticle', (art_id, art_title, art_keywords, art_abstract, art_date,))
            connection.commit()
    except:
        DB_CONNECTION = False
    finally:
        pass
        #connection.close()


def result_handler(type, search_word, date_before='', date_after='', save=False):
    result = ''
    if not date_before:
        date_before = '1970-01-01'
    if not date_after:
        date_after = '3000-01-01'
    query = f'(("{date_before}"[Date - Create] : "{date_after}"[Date - Create])) AND {search_word})'
    pubmed = PubMed(tool="MyTool", email="my@email.address")
    results = pubmed.query(query, max_results=500)
    for article in results:
        keywords = ''
        if hasattr(article, 'keywords'):
            if None in article.keywords:
                article.keywords.remove(None)
            keywords = ', '.join(article.keywords)
        trunc_id = article.pubmed_id.split('\n')[0]
        if save:
            article_save(trunc_id, article.title, keywords, article.abstract, article.publication_date)
        if type == 'HTML':
            result += f'<h3>{trunc_id} - {article.publication_date} - {article.title}</h3><strong>Ключевые слова: </strong>{keywords}</br>{article.abstract}</br>'
        elif type == 'JSON':
            result += json.dumps({"id": str(article.pubmed_id), "pub_date": str(article.publication_date), "title": article.title, "keywords": keywords, "abstract": article.abstract})
    return result


@app.route('/', methods=['POST', 'GET'])
def index_view():
    search_result = ''
    search_word = ''
    date_before = ''
    date_after = ''
    form_search = SearchForm()
    if form_search.validate_on_submit():
        search_word = form_search.search_word.data
        date_before = str(form_search.date_before.data).replace("-", "/")
        date_after = str(form_search.date_after.data).replace("-", "/")
        search_result = result_handler('HTML', search_word, date_before, date_after, form_search.save_db.data)

    return render_template('index.html', search_result=search_result, form_search=form_search, search_word=search_word,
                           date_before=date_before, date_after=date_after, app_title = APP_NAME, db_con = DB_CONNECTION)


@app.route('/api/v1/word/<search_word>')
def search_view(search_word):
    if search_word:
        return jsonify(result_handler('JSON', search_word))


app.run(host='0.0.0.0', port=80)