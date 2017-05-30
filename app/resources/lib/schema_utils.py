import os
import json
import jsonschema
from flask import current_app


# https://github.com/Julian/jsonschema/issues/119

# Custom validators
def _required(validator, required, instance, schema):
    '''Validate 'required' properties.'''
    if not validator.is_type(instance, 'object'):
        return

    for index, requirement in enumerate(required):
        if requirement not in instance:
            error = jsonschema.ValidationError(
                '{0!r} is a required property'.format(requirement)
            )
            error.schema_path.append(index)
            yield error


# Construct validator as extension of Json Schema Draft 3.
Validator = jsonschema.validators.extend(
    validator=jsonschema.validators.Draft3Validator,
    validators={
        'required': _required
    }
)


def validate_json(data, schema_path, schema_name):
    errors = {}
    with open(os.path.join(
            current_app.config['SCHEMAS_DIRECTORY'],
            schema_path,
            ".".join((schema_name, 'json'))), 'r') as fp:
        resolver = jsonschema.RefResolver(
            'file://' + os.path.join(current_app.config['SCHEMAS_DIRECTORY'], schema_path), None)
        validator = Validator(json.load(fp), resolver=resolver)
        for error in validator.iter_errors(data):
            # get property name
            if error.schema_path[0] == "anyOf":
                for value in error.validator_value:
                    for property_name in value["required"]:
                        if not data.get(property_name):
                            errors[property_name] = ["This field is required."]
                continue
            elif error.schema_path[0] == "required":
                property_name = error.validator_value[error.schema_path[1]]
            else:
                property_name = error.path[0]
            # get error message
            if error.schema_path[0] == "required":
                message = "This field is required"
            elif error.schema.get('error') is not None:
                message = error.schema['error'].get(error.validator, error.message)
            else:
                message = error.message
            # append error message
            if errors.get(property_name) is not None:
                errors[property_name].append(message)
            else:
                errors[property_name] = [message]
    return errors
