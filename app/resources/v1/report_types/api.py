from flask_restful import Resource
from app.resources.lib import api_response

# TODO: use db object
from collections import namedtuple

ReportType = namedtuple("ReportType", ["text", "value"])


class ReportTypesAPI(Resource):
    def get(self):
        return api_response.success([
            {
                "text": type_.text,
                "value": type_.value
            } for type_ in [
                ReportType("Adjudications / Decisions", "adjudications_decisions"),
                ReportType("Audit Report", "audit_report"),
                ReportType("Brochures", "brochures"),
                ReportType("Budget / Finance", "budget_finance"),
                ReportType("Bulletins", "bulletins"),
                ReportType("Calendars", "calendars"),
                ReportType("Data / Statistics", "data_statistics"),
                ReportType("Directives", "directives"),
                ReportType("Environmental Impact Statements - Draft", "environmental_impact_statements_draft"),
                ReportType("Environmental Impact Statements - Final", "environmental_impact_statements_final"),
                ReportType("Executive Orders", "executive_orders"),
                ReportType("Guides", "guides"),
                ReportType("Laws / Legislation", "laws_legislation"),
                ReportType("Manuals / Directories", "manuals_directories"),
                ReportType("Minutes", "minutes"),
                ReportType("Newsletters / Other Serial Publications", "newletters"),
                ReportType("Other", "other"),
                ReportType("Plans", "plans"),
                ReportType("Press Releases", "press_releases"),
                ReportType("Proceedings", "proceedings"),
                ReportType("Reports - Annual", "reports_annual"),
                ReportType("Reports - Biennial", "reports_biennial"),
                ReportType("Reports - Monthly", "reports_monthly"),
                ReportType("Reports - Weekly", "reports_weekly"),
                ReportType("Reports - Other (Consultant/Staff)", "reports_other"),
                ReportType("Studies", "studies"),
            ]
        ])
