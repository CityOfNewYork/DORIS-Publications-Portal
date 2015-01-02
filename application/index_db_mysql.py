import os
import time
import logging
import MySQLdb
from elasticsearch import Elasticsearch
# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.DEBUG)
# add handlers to tracer
tracer.addHandler(logging.FileHandler('/tmp/out.sh'))

DB = MySQLdb.connect(host='localhost', user='index', passwd=os.environ['DB_PASS_INDEX'], db='publications')
C = DB.cursor()
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

	num_docs = C.execute("SELECT COUNT(*) FROM headless_document")
	num_docs = C.fetchone()
	print str(num_docs[0]) + " headless_documents"

	docs = C.execute("SELECT * FROM headless_document")
	docs = C.fetchall()

	for doc in docs:
		es.index(index=INDEX, doc_type=DOCTYPE, body={
			"id":           doc[0],
			"title":        doc[1],
			"description":  doc[2],
			"date_created": doc[3],
			"common_id":    doc[5],
			"section_id":   doc[6],
			"pub_or_foil":  doc[8],
			"agency":       doc[9],
			"category":     doc[10],
			"type":         doc[11],
			"url":          doc[12],
			"docText":		doc[13],
			# "file":         b64encoded
		})
		# print str(doc[0]) + " indexed"

	index_time_elapsed = time.clock() - index_time_start
	print "Completed in: %f seconds" %index_time_elapsed


if __name__ == "__main__":
	print "Indexing initialized..."
	indexDB()