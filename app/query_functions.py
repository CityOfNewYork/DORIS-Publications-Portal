from flask import jsonify
from models import Document, DocumentCereal
import json
import time

def process_query(search, agencies_selected, categories_selected, types_selected, fulltext_checked):
    """
    Retrieves search results based on search value and selected filters
    :param search: user input query
    :param agencies_selected: user-selected agencies from 'Filter' / 'Refine Search'
    :param categories_selected: user-selected categories from 'Filter' / 'Refine Search'
    :param types_selected: user-selected types from 'Filter' / 'Refine Search'
    :return: finalized results of the query, and the time it takes to execute this function
    """
    process_time_start = time.clock()

    search = normalize(search)

    #initialize query or search based on user input
    if search:
        if fulltext_checked:
            results = Document.query.whoosh_search(search, fields=('docText',))
        else:
            results = Document.query.whoosh_search(search, fields=('title', 'description', 'agency', 'category', 'type'))
    else:
        results = Document.query

    if agencies_selected:
        results = results.filter(Document.agency.in_(agencies_selected))

    if categories_selected:
        results = results.filter(Document.category.in_(categories_selected))

    if types_selected:
        results = results.filter(Document.type.in_(types_selected))

#     serialized = jsonify({"results": DocumentCereal(final_filter, many=True).data})
#     res = json.loads(serialized.data)['results']
        
    process_time_elapsed = format((time.clock() - process_time_start), '.3f')
    
    return results.all(), process_time_elapsed
#     return res, process_time_elapsed


def sort_search(results, sort_method):
    """
    Sorts results of current set
    :param results: query results list
    :param sort_method: how to sort results
    :return: sorted results
    """
    sort_by = { "Relevance": results,
                "Date: Newest": sorted(results, key=lambda r: r.date_created, reverse=True),
                "Date: Oldest": sorted(results, key=lambda r: r.date_created),
                "Title: A - Z": sorted(results, key=lambda r: r.title),
                "Title: Z - A": sorted(results, key=lambda r: r.title, reverse=True),
                "Agency: A - Z": sorted(results, key=lambda r: r.agency),
                "Agency: Z - A": sorted(results, key=lambda r: r.agency, reverse=True)}

    return sort_by[sort_method]


def sort_search_json(results, sort_method):
    """
    Sorts results of current set
    :param results: query results json object
    :param sort_method: how to sort results
    :return: sorted results json
    """
    pass


def normalize(_input):
    """
    Standardizes passed value by removing unnecessary characters and words
    :param _input: string to be normalized
    :return: normalized value
    """
    #remove stop words
    stop_words = []

    #remove stop characters
    stop_chars = ['?', '"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',  "--", '.']
    for char in stop_chars:
        _input = _input.replace(char, '')

    return _input