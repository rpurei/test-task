from pymed import PubMed
from celery import Celery
import redis
from config import *

celery = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task()
def pubmed_query(query):
    if query:
        result = ''
        pubmed = PubMed(tool="MyTool", email="my@email.address")
        results = pubmed.query(query, max_results=500)
        for article in results:
           keywords = ''
           article_id = article.pubmed_id
           title = article.title
           if article.keywords:
               if None in article.keywords:
                   article.keywords.remove(None)
               keywords = '", "'.join(article.keywords)
           publication_date = article.publication_date
           abstract = article.abstract
           result += f'{article_id} - {publication_date} - {title}\nKeywords: "{keywords}"\n{abstract}\n'
        print(result)
        return result
