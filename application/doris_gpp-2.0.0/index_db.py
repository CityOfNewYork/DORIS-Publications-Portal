import os
import MySQLdb
import time
import logging
from elasticsearch import Elasticsearch
# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
# add handlers to tracer
tracer.addHandler(logging.FileHandler('/tmp/out.sh'))

DB = MySQLdb.connect(host='localhost', user='root', passwd='')
C = DB.cursor()
URL = 'localhost'
INDEX = 'publications'
DOCTYPE = 'document'

es = Elasticsearch()


def indexDB():
	es.indices.delete(index=INDEX, ignore=[400, 404])
	es.indices.create(index=INDEX, body={
		"index": {
			"analysis": {
				"analyzer": {
					"gpp_analyzer": {
						"type": "snowball",
						"language": "English"
					}
				}
			},
            "refresh_interval": 60000
		}
	})

	index_time_start = time.clock()
	print "Start"
	es.indices.put_mapping(index=INDEX, doc_type=DOCTYPE, body={
		DOCTYPE: {
			'properties': {
				'id': {'type': 'integer'},
				'title': {'type': 'string',
						  'analyzer': 'gpp_analyzer',
						  'index': 'analyzed',
						  'fields': {
							  'raw': {
							  'type': 'string',
							  'index': 'not_analyzed'
							  }
						  }
				},
				'description':  {'type': 'string', 'analyzer': 'gpp_analyzer', 'index': 'analyzed'},
				'date_created': {'type': 'date'},
				'common_id':    {'type': 'integer'},
				'section_id':   {'type': 'integer'},
				'pub_or_foil':  {'type': 'string', 'index': 'no'},
				'agency':       {'type': 'string', 'index': 'not_analyzed'},
				'category':     {'type': 'string', 'index': 'not_analyzed'},
				'type':         {'type': 'string', 'index': 'not_analyzed'},
				'url':          {'type': 'string', 'index': 'no'},
				'docText': {'type': 'string', 'analyzer': 'gpp_analyzer', 'index': 'analyzed'},
				# 'file':           {
				#     'type': 'attachment',
				#     'analyzer': 'gpp_analyzer',
				#     'fields': {
				#         'file': {'analyzer': 'gpp_analyzer'}
				#     }
				# }
			}
		}
	})

	docs = Document.objects.all()

	for doc in docs:
		es.index(index=INDEX, doc_type=DOCTYPE, body={
			"id":           doc.id,
			"title":        doc.title,
			"description":  doc.description,
			"date_created": doc.date_created,
			"common_id":    doc.common_id,
			"section_id":   doc.section_id,
			"pub_or_foil":  doc.pub_or_foil,
			"agency":       doc.agency,
			"category":     doc.category,
			"type":         doc.type,
			"url":          doc.url,
			"docText":		doc.docText,
			# "file":         b64encoded
		})

	index_time_elapsed = time.clock() - index_time_start
	print "Completed in: %f seconds" %index_time_elapsed


if __name__ == "__main__":
	print "Indexing database..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_gpp.settings')
	from gpp.models import Document
	indexDB()