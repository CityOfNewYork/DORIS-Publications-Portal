Government Publications Portal

Features

	Home Page
		- Search indexed records with simple search
		- Full-Text search that matches search entry with key words within each document of the records. If there is a match, record is displayed in the results page.
		- Filters (agency, category, type) that will narrow down the user's search results
		- Remove all filters button

	Results Page
		- View / Save button that lets the user view or save the attached pdf file, respectively
		- Search functionality included in the results page, so user does not have to revisit search page in order to search
		- List / Panel view of results
		- Results per page, users can view 10,20,50, or 100 results at a time
		- Sort by relevance, date, title, and agency
		- Pagination

	Publications Page
		- Previews pdf file for the user to read

How to install

Using a virtualenv, pip install requirements.txt

Download and run the schema dump on a MySQL server, adjust appconfig to connect to your database
In order to index the records using Whoosh, write a script that will iterate through the records and add those to your database in flask using SQLAlchemy.