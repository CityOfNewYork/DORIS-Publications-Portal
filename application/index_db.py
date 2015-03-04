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

DB = MySQLdb.connect(
    host='localhost', user='index', passwd=os.environ['DB_NDX'], db='publications')
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
          "refresh_interval": 60000,
          "number_of_replicas": 0,
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
              'agency':       {'type': 'string', 'index': 'not_analyzed'},
              'category':     {'type': 'string', 'index': 'not_analyzed'},
              'type':         {'type': 'string', 'index': 'not_analyzed'},
              'url':          {'type': 'string', 'index': 'no'},
              'pub_or_foil':  {'type': 'string', 'index': 'no'},
              # 'docText': {'type': 'string', 'analyzer': 'gpp_analyzer', 'index': 'analyzed'},
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

  num_docs = C.execute("SELECT MAX(id) FROM document")
  num_docs = C.fetchone()
  print str(num_docs[0]) + " documents"

  for i in range(0,num_docs[0]/1000+1):
    print "Retrieving Documents " + str(i*1000) + " to " + str((i+1)*1000)
    docs = C.execute("SELECT * FROM document WHERE id <= %s AND id > %s" % (str((i+1)*1000), str(i*1000)))
    docs = C.fetchall()
    print "Documents Retrieved"

    for doc in docs:
      es.index(index=INDEX, doc_type=DOCTYPE, body={
          "id":           doc[0],
          "title":        doc[1],
          "description":  doc[2],
          "date_created": doc[3],
          "common_id":    doc[5],
          "section_id":   doc[6],
          "agency":       doc[8],
          "category":     doc[9],
          "type":         doc[10],
          "url":          doc[11],
          "pub_or_foil":	doc[12],
          #"docText":		doc[13],
          # "file":         b64encoded
      })

  index_time_elapsed = time.clock() - index_time_start
  print "Completed in: %f seconds" % index_time_elapsed


if __name__ == "__main__":
  print "Indexing initialized..."
  indexDB()
