## Government Publications Portal

### About

This application was built under the direction of Joel Castillo by three 
talented interns from the NYU Polytechnic School of Engineering, Alan Chen, 
Alvi Kabir, and Panagis (Peter) Alisandratos using Python and the Django Framework. 

We currently use the following packages in our application:
- Django 1.6.6
- django-endless-pagination 2.0
- ecdsa 0.11
- elasticsearch 1.2.0
- MySQL-python 1.2.5
- paramiko 1.15.1
- pycrypto 2.6.1
- requests 2.3.0
- urllib3 1.9

We are also making use of MySQL Community Edition (v 5.1) to house our database.

### Features

- Basic Search – The default search will comb through the database searching 
document titles, descriptions, agencies, types, and categories to give you the 
best possible results.
- Advanced Search – You can filter your results By Agency, Category, and Type 
to make the search even faster and targeted.
- Sorting – All searches can be sorted by Agency, Category, Type, and Relevance.
- Dynamic Pagination – Allows users to view 10, 20, 50, or 100 results per page.
- Embedded PDFs – To make it easier to view the documents, the files are 
embedded in the results page, allowing the user to view their document without 
manually saving to their computer.

### Upcoming Features

- Full Text Search – Full text search will be available for all documents in 
the near future, making it even easier to find the right document.
- Relevancy Scores – A percentage based score of how relevant a result is to 
your original search query.
- CSV Export – Users will be able to export their search results to a CSV file 
for manipulation in a program such as Microsoft Excel.
- API – Allows other applications to take advantage of our database of documents 
and display them in unique ways to users.

### Getting Involved

We are launching this product as a beta so that we can get your input. Please
use our feedback form or Github issues to submit new requests and bug reports.
We would also encourage you to send any improvements on our code. Clone our 
repository and show us what you can do with our codebase to make it even better.

### Acknowledgements

Special thanks to our four talented interns
(Alan Chen, Alvi Kabir, Brandon Tang, and Panagis Alisandratos), Jeff Merrit, Steve Bezman, Prince Gupta, and Anand Krishnan.
