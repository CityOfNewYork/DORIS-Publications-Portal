from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from query_functions import process_query, get_url_by_id
from django.core.paginator import Paginator
from math import ceil
import logging

def index(request):
    # Clear the Session First

    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    context_dict = \
        {'agencies': ['Admin. Trials and Hearings', 'Aging', 'Buildings', 'Business Integrity Commission',
                      'Chief Medical Examiner', 'Children\'s Services', 'City Council', 'City Planning',
                      'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Comptroller',
                      'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Corrections',
                      'Criminal Justice', 'Cultural Affairs', 'Data Analytics', 'DCAS',
                      'Design/Construction', 'DOI - Investigation', 'DOITT', 'Domestic Violence', 'Education, Dept. of',
                      'Emergency Mgmt.', 'Environmental - DEP', 'Equal Employment', 'Finance', 'Fire',
                      'Health', 'Health and Mental Hyg.', 'Homeless Services', 'Housing - HPD',
                      'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget',
                      'International Affairs', 'Labor Relations', 'Landmarks',
                      'Law Department', 'Loft Board', 'Management and Budget', 'Mayor', 'Mayor\'s Fund',
                      'Media and Entertainment', 'NYC Service', 'NYCERS', 'Operations', 'Parks and Recreation',
                      'Police', 'Probation', 'Public Advocate', 'Public Design Commission', 'Records',
                      'Rent Guidelines Board', 'Sanitation', 'Small Business Svcs', 'Standards and Appeal',
                      'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings',
                      'Veteran\'s Affairs', 'Youth & Community'],
         'categories': ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment',
                        'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services',
                        'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology',
                        'Transportation'],
         'types': ['Actuarial Audit', 'Actuarial Audit Report', 'Annual Audit Report',
                   'Annual Claims Report', 'Annual Contracts Report', 'Annual Report',
                   'Audit', 'Audit Report', 'Bond Offering - Official Statements',
                   'Brochure', 'Budget Report', 'Cash Report', 'Consultant Report',
                   'Economic Notes', 'GAGAS Peer Review', 'Guide - Manual', 'Hearing - Minutes',
                   'Legislative Document', 'Memoranda - Directive', 'Organizational Chart',
                   'Policy Report', 'Press Release', 'Public Policy and Other', 'Report',
                   'Report - Annual', 'Report - Other', 'Serial Publication',
                   'Shareowner Initiatives', 'Staff Report'], }
    request.session.flush()
    return render_to_response('index.html', context_dict, context)


def results(request):
    context = RequestContext(request)
    if not request.session.get('num_results'):
        request.session['num_results'] = 10
    if not request.session.get('sort'):
        request.session['sort'] = 'Relevance'
    if not request.session.get('list_view'):
        request.session['list_view'] = 0
    if not request.session.get('start'):
        request.session['start'] = 0
    if not request.session.get('page'):
        request.session['page'] = 1

    # On GET Request
    if request.method == 'GET':
        request.session['page'] = 1
        request.session['start'] = 0
        if request.GET.get('btn') == 'Search':
            request.session['search'] = request.GET.get('user_input')
            request.session['agencies'] = request.GET.getlist('agency[]', None)
            request.session['categories'] = request.GET.getlist('category[]', None)
            request.session['types'] = request.GET.getlist('type[]', None)
            request.session['fulltext'] = request.GET.get('fulltext', False)

        # #POST - Refine Search
        if request.GET.get('btn') == 'Refine / Search':
            if request.GET.get('user_input'):
                request.session['search'] = request.GET.get('user_input')
            request.session['agencies'] = request.GET.getlist('agency[]')
            request.session['categories'] = request.GET.getlist('category[]')
            request.session['types'] = request.GET.getlist('type[]')
            request.session['fulltext'] = request.GET.get('fulltext', False)
        # GET - Sort
        request.session['sort'] = request.GET.get('sort', request.session.get('sort'))
        # GET - Num Results
        request.session['num_results'] = request.GET.get('num_results', request.session.get('num_results'))
        # GET - List view
        request.session['list_view'] = request.GET.get('list_view', request.session.get('list_view'))
        request.session['page'] = request.GET.get('page', request.session.get('page'))
        request.session['start'] = int(request.session['num_results']) * (int(request.session['page']) - 1)
    else:
        return HttpResponse(status=404)

    # Retrieve Results
    request.session['results_list'], results_length, \
    query_time = process_query(
        request.session.get('search'),
        request.session.get('agencies'),
        request.session.get('categories'),
        request.session.get('types'),
        request.session.get('fulltext'),
        request.session.get('start'),
        int(request.session.get('num_results')),
        request.session.get('sort'))

    request.session['length'] = results_length
    request.session['num_pages'] = int(ceil(request.session['length'] / float(request.session['num_results'])))

    # Session expires after 5 seconds
    # request.session.set_expiry(5)

    # initiate pagination
    paginator = Paginator(range(1, request.session['length'] + 1), request.session.get('num_results'))
    pag_res = paginator.page(request.session['page'])

    context_dict = {'results': request.session['results_list'],
                    'agencies': ['Admin. Trials and Hearings', 'Aging', 'Buildings', 'Business Integrity Commission',
                                 'Chief Medical Examiner', 'Children\'s Services', 'City Council', 'City Planning',
                                 'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Comptroller',
                                 'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Corrections',
                                 'Criminal Justice', 'Cultural Affairs', 'Data Analytics', 'DCAS',
                                 'Design/Construction', 'DOI - Investigation', 'DOITT', 'Domestic Violence', 'Education, Dept. of',
                                 'Emergency Mgmt.', 'Environmental - DEP', 'Equal Employment', 'Finance', 'Fire',
                                 'Health', 'Health and Mental Hyg.', 'Homeless Services', 'Housing - HPD',
                                 'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget',
                                 'International Affairs', 'Labor Relations', 'Landmarks',
                                 'Law Department', 'Loft Board', 'Management and Budget', 'Mayor', 'Mayor\'s Fund',
                                 'Media and Entertainment', 'NYC Service', 'NYCERS', 'Operations', 'Parks and Recreation',
                                 'Police', 'Probation', 'Public Advocate', 'Public Design Commission', 'Records',
                                 'Rent Guidelines Board', 'Sanitation', 'Small Business Svcs', 'Standards and Appeal',
                                 'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings',
                                 'Veteran\'s Affairs', 'Youth & Community'],
                    'categories': ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment',
                                   'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services',
                                   'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology',
                                   'Transportation'],
                    'types': ['Actuarial Audit', 'Actuarial Audit Report', 'Annual Audit Report',
                              'Annual Claims Report', 'Annual Contracts Report', 'Annual Report',
                              'Audit', 'Audit Report', 'Bond Offering - Official Statements',
                              'Brochure', 'Budget Report', 'Cash Report', 'Consultant Report',
                              'Economic Notes', 'GAGAS Peer Review', 'Guide - Manual', 'Hearing - Minutes',
                              'Legislative Document', 'Memoranda - Directive', 'Organizational Chart',
                              'Policy Report', 'Press Release', 'Public Policy and Other', 'Report',
                              'Report - Annual', 'Report - Other', 'Serial Publication',
                              'Shareowner Initiatives', 'Staff Report'],
                    'length': int(request.session.get('length')),
                    'search': str(request.session.get('search')),
                    'selected_agencies': str(request.session.get('agencies')),
                    'selected_categories': str(request.session.get('categories')),
                    'selected_types': str(request.session.get('types')),
                    'pag_res': pag_res,
                    'num_results': int(request.session.get('num_results')),
                    'time': query_time,
                    'sort_method': request.session.get('sort'),
                    'list_view': int(request.session.get('list_view')),
                    'records': range(1, request.session['length'] + 1)}

    print context_dict
    return render_to_response('results.html', context_dict, context)

def publication(request):
    context = RequestContext(request)
    document_url = request.POST['view']
    context_dict = {'document_url': document_url }
    return render_to_response('publication.html', context_dict, context)