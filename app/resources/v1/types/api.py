from flask_restful import Resource
from app.resources.lib import api_response

# TODO: use db object
from collections import namedtuple

Type = namedtuple("Type", ["text", "value"])


class TypesAPI(Resource):
    def get(self):
        return api_response.success({
            [{
                "text": type_.text,
                "value": type_.value
            } for type_ in [
                Type("Adjunctions / Decisions", "adjunctions_decisions"),
                Type("Audit Report", "audit_report"),
                Type("Brochures", "brochures"),
                Type("Budget / Finance", "budget_finance"),
                Type("Bulletins", "bulletins"),
                Type("Calendars", "calendars"),
                Type("Data / Statistics", "data_statistics"),
                Type("Directives", "directives"),
                Type("Environmental impact statements", "environmental_impact_statements_draft"),
                Type("Environmental impact statements", "environmental_impact_statements_final"),
                Type("Executive Orders", "executive orders"),
                Type("Guides", "guides"),
                Type("Laws / Legislation", "laws_legislation"),
                Type("Manuals / Directories", "manuals_directories"),
                Type("Minutes", "minutes"),
                Type("Newsletters / Other Serial Publications", "newletters"),
                Type("Other", "other"),
                Type("Plans", "plans"),
                Type("Press Releases", "press_releases"),
                Type("Proceedings", "proceedings"),
                Type("Reports - Annual", "reports_annual"),
                Type("Reports - Biennial", "reports_biennial"),
                Type("Reports - Monthly", "reports_monthly"),
                Type("Reports - Weekly", "reports_weekly"),
                Type("Reports - Other (Consultant/Staff)", "reports_other"),
                Type("Studies", "studies"),
            ]]
        })
