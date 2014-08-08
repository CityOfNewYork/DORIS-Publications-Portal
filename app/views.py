import os
from app import app
from flask import Flask, render_template, request, flash, url_for, redirect, make_response, session, abort, jsonify
from forms import SearchForm
from models import db, Document# , DocumentCereal
from query_functions import process_query, sort_search
from index_database import index_document, add_sample_entries, index_city_record
from flask.ext.paginate import Pagination
from flask.ext.mail import Message
from . import mail


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    session['sort']= 'Relevance'
    session['fulltext'] = None
    session['num_results'] = 10
    session['list_view'] = 0
    session['page'] = 1
    return render_template("index.html", form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():

    #Set initial session variables
    if 'sort' not in session:
        session['sort'] = 'Relevance'
    if 'length' not in session:
        session['length'] = 0
    if 'fulltext' not in session:
        session['fulltext'] = None
    if 'num_results' not in session:
        session['num_results'] = 10
    if 'list_view' not in session:
        session['list_view'] = 0
    if 'page' not in session:
        session['page'] = 1
    
    #On POST request
    if request.method == 'POST':
    
        #POST - Search
        if request.form['btn'] == "Search":
            session['search'] = request.form.get('user_input')
            session['agencies'] = request.form.getlist('agency[]')
            session['categories'] = request.form.getlist('category[]')
            session['types'] = request.form.getlist('type[]')
            session['fulltext'] = request.form.get('fulltext')
            
        #POST - Refine Search
        if request.form['btn'] == "Refine / Search":
            if request.form.get('user_input'):
                session['search'] = request.form.get('user_input')
            session['agencies'] = request.form.getlist('agency[]')
            session['categories'] = request.form.getlist('category[]')
            session['types'] = request.form.getlist('type[]')
            session['fulltext'] = request.form.get('fulltext')
            
        session['page'] = 1

    #On GET Request
    if request.method == 'GET':
        
        #GET - Sort
        if request.args.get('sort'):
            session['sort'] = request.args.get('sort')

        #GET - Num Results
        if request.args.get('num_results'):
            session['num_results'] = request.args.get('num_results')
            session['page'] = 1
            
        #GET - List view
        if request.args.get('list_view'):
            session['list_view'] = request.args.get('list_view')
            
    #retrieve results
    res, time = process_query(session['search'], session['agencies'], session['categories'], session['types'], session['fulltext'])
    res = sort_search(res, session['sort'])
    session['length'] = len(res)
    
    #initiate pagination
    session['page'] = int(request.args.get('page', session['page']))
        
    pagination = Pagination(page=session['page'], total=session['length'], per_page=int(session['num_results']), css_framework="boostrap3")
    start = session['page'] * int(session['num_results']) - int(session['num_results'])
    res = res[start : start + int(session['num_results']) ]

    # if len(session['search']) > 30:
#         session['search'] = session['search'][:30] + '...'
     
    #RENDER!
    return render_template("results.html", 
                            start=start,
                            search=session['search'], 
                            results=res, 
                            time=time, 
                            length=session['length'], 
                            method='post', 
                            sort_method=session['sort'], 
                            pagination=pagination,
                            fulltext=session['fulltext'],
                            num_results=int(session['num_results']),
                            list_view=int(session['list_view']),
                            page_num=session['page'])


@app.route('/publication/<int:id><title>', methods=['GET'])
def publication(id,title):
    document = Document.query.filter(Document.id == id).first()
    document_title = document.title
    document_url = document.url
    # document.num_access += 1
    # db.session.commit()
    # response = make_response(url)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=%s.pdf' % document.filename
    # return response
    return render_template("publication.html", document_title=document_title, document_url=document_url)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/email', methods=['POST'])
def email():

    #On POST request
    if request.method == 'POST':
    
        if request.form['send_email'] and request.form['feedback_msg']:
            message = request.form['feedback_msg']
            name = request.form['name']
            email = request.form['email']
            msg = Message(subject='GPP Feedback',
                          body='Name: ' + name + '\n' + 'Email: ' + email + '\n' + 'Message: ' + message,
                          sender=os.environ.get('DEFAULT_MAIL_SENDER'),
                          recipients=[os.environ.get('FEEDBACK_RECIPIENT')])
        try:                                                
            mail.send(msg)
        except UnboundLocalError:
            return redirect(redirect_url())
                              
    return redirect(redirect_url())


@app.errorhandler(404)
def page_not_found(e):
    url = redirect_url()
    return render_template('404.html',url=url), 404