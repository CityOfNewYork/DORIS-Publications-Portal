from flask.ext.sqlalchemy import SQLAlchemy
from marshmallow import Serializer, fields

db = SQLAlchemy()


class Document(db.Model):
	__tablename__ = 'document'
	__searchable__ = ['title', 'description', 'agency', 'category', 'type','docText']
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.Date, nullable=False)
	filename = db.Column(db.String(255), nullable=False)
	common_id = db.Column(db.Integer, default=None)
	section_id = db.Column(db.Integer, default=None)
	num_access = db.Column(db.Integer, default=0, nullable=False)
	agency = db.Column(db.Enum(
		'Aging',
		'Buildings',
		'Campaign Finance',
		'Children\'s Services',
		'City Council',
		'City Clerk',
		'City Planning',
		'Citywide Admin Svcs',
		'Civilian Complaint',
		'Comm - Police Corr',
		'Community Assistance',
		'Comptroller',
		'Conflicts of Interest',
		'Consumer Affairs',
		'Contracts',
		'Correction',
		'Criminal Justice Coordinator',
		'Cultural Affairs',
		'DOI - Investigation',
		'Design/Construction',
		'Disabilities',
		'District Atty, NY County',
		'Districting Commission',
		'Domestic Violence',
		'Economic Development',
		'Education, Dept. of',
		'Elections, Board of',
		'Emergency Mgmt.',
		'Employment',
		'Empowerment Zone',
		'Environmental - DEP',
		'Environmental - OEC',
		'Environmental - ECB',
		'Equal Employment',
		'Film/Theatre',
		'Finance',
		'Fire',
		'FISA',
		'Health and Mental Hyg.',
		'HealthStat',
		'Homeless Services',
		'Hospitals - HHC',
		'Housing - HPD',
		'Human Rights',
		'Human Rsrcs - HRA',
		'Immigrant Affairs',
		'Independent Budget',
		'Info. Tech. and Telecom.',
		'Intergovernmental',
		'International Affairs',
		'Judiciary Committee',
		'Juvenile Justice',
		'Labor Relations',
		'Landmarks',
		'Law Department',
		'Library - Brooklyn',
		'Library - New York',
		'Library - Queens',
		'Loft Board',
		'Management and Budget',
		'Mayor',
		'Metropolitan Transportation Authority',
		'NYCERS',
		'Operations',
		'Parks and Recreation',
		'Payroll Administration',
		'Police',
		'Police Pension Fund',
		'Probation',
		'Public Advocate',
		'Public Health',
		'Public Housing-NYCHA',
		'Records',
		'Rent Guidelines',
		'Sanitation',
		'School Construction',
		'Small Business Svcs',
		'Sports Commission',
		'Standards and Appeal',
		'Tax Appeals Tribunal',
		'Tax Commission',
		'Taxi and Limousine',
		'Transportation',
		'Trials and Hearings',
		'Veterans - Military',
		'Volunteer Center',
		'Voter Assistance',
		'Youth & Community'), nullable=False)
	category = db.Column(db.Enum(
		'Business and Consumers',
		'Cultural/Entertainment',
		'Education',
		'Environment',
		'Finance and Budget',
		'Government Policy',
		'Health',
		'Housing and Buildings',
		'Human Services',
		'Labor Relations',
		'Public Safety',
		'Recreation/Parks',
		'Sanitation',
		'Technology',
		'Transportation'), nullable=False)
	type = db.Column(db.Enum(
		'Annual Report',
		'Audit Report',
		'Bond Offering - Official Statements',
		'Budget Report',
		'Consultant Report',
		'Guide - Manual',
		'Hearing - Minutes',
		'Legislative Document',
		'Memoranda - Directive',
		'Press Release',
		'Serial Publication',
		'Staff Report',
		'Report'), nullable=False)
	url = db.Column(db.String(255), nullable=False)
	pub_or_foil = db.Column(db.Enum('Publication', 'FOIL'), nullable=False)
	docText = db.Column(db.UnicodeText(length=2**23))
	
# marshmallows go great with cereal, especially the small kind
class DocumentCereal(Serializer):
    class Meta:
        fields = ('id', 'title', 'description', 'date_created', 'filename', 'common_id', 'section_id', 'num_access', 'agency', 'category', 'type', 'url', 'pub_or_foil', 'docText')