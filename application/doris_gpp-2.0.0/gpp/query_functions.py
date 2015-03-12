import MySQLdb
import time
import logging
import os
from elasticsearch import Elasticsearch
# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
# add handlers to tracer
tracer.addHandler(logging.FileHandler('/var/www/logs/query.log'))

INDEX = 'publications'
DOCTYPE = 'document'

host_params = {'host': os.environ['ELASTICSEARCH'], 'port':443, 'use_ssl':True}

es = Elasticsearch([host_params], use_ssl=True)


def get_url_by_id(id):
    result = es.search(index='publications', body={
        "query": {
            "match": {
                "id": id
            }
        }
    })
    return result['hits']['hits'][0][u'_source'][u'url']


def process_query(search, agencies_selected, categories_selected, types_selected, fulltext, start, num_results, sort_method):
    start_time = time.clock()
    result_list = []
    if search:
        if fulltext:
            query_list = [
                {
                    "match": {
                        "docText": search
                    }
                },
            ]
        else:
            query_list = [
                {
                    "multi_match": {
                        "query": search,
                        "fields": ["title", "description"],
                        "type": "best_fields",
                        "cutoff_frequency": 0.0001
                    },
                },
            ]
    else:
        query_list = []

    if agencies_selected:
        query_list.append({"in": {"agency": agencies_selected}, })

    if categories_selected:
        query_list.append({"in": {"category": categories_selected}, })

    if types_selected:
        query_list.append({"in": {"type": types_selected}, })

    sort_by = {"Relevance": {},
               "Date: Newest": {"date_created": {"order": "desc"}},
               "Date: Oldest": {"date_created": {"order": "asc"}},
               "Title: A - Z": {"title": {"order": "asc"}},
               "Title: Z - A": {"title": {"order": "desc"}},
               "Agency: A - Z": {"agency": {"order": "asc"}},
               "Agency: Z - A": {"agency": {"order": "desc"}}}

    results = es.search(index=INDEX, body={
        "from": start, "size": num_results,
        "query": {
            "bool": {
                "must": query_list
            }
        },
        "sort": sort_by[sort_method],
        "highlight": {
            "pre_tags": ["<span class = 'highlight'>"],
            "post_tags": ["</span>"],
            "fields": {
                "title": {"number_of_fragments": 0},
                "description": {"number_of_fragments": 0},
                "agency": {},
                "category": {},
                "type": {}
            }
        }
    })

    query_time = format((time.clock() - start_time), '.3f')
    rank = int(start)
    for result in results['hits']['hits']:
        rank += 1
        result[u'_source'][u'rank'] = rank
        if not fulltext:
            highlight(result, u'title')
            highlight(result, u'description')
            highlight(result, u'agency')
            highlight(result, u'category')
            highlight(result, u'type')
        result_list.append(result['_source'])

    return result_list, results['hits']['total'], query_time


def highlight(result, field):
    if field in result[u'highlight'].keys():
        result[u'_source'][field] = result[u'highlight'][field][0]



