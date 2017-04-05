from flask_wtf import FlaskForm


class Form(FlaskForm):
    class Meta:
        """
        Disable CSRF protection for individual forms since it is enabled
        globally. Form submission is performed with ajax so the 'X-CSRFToken'
        header must be included in the request.
        """
        csrf = False

        def bind_field(self, form, unbound_field, options):
            """
            Strip field values of whitespace.
            http://stackoverflow.com/questions/26232165/automatically-strip-all-values-in-wtforms
            """
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)


def _strip_filter(value):
    """
    Call strip() on given value if possible.
    :return: stripped or unaltered value
    """
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
