import {Validator} from "jsonschema";

const submissionSubset = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "/Submission",
    "properties": {
        "creators": {
            "items": {
                "id": "/properties/creators/items",
                "type": "string"
            },
            "type": "array"
        },
        "date_published": {
            "pattern": "\\d{2}/\\d{2}/\\d{4}",
            "type": "string",
            "error": {
                "pattern": "This is not a valid date value."
            }
        },
        "description": {
            "maxLength": 200,
            "minLength": 100,
            "type": "string",
            "error": {
                "maxLength": "Please shorten your description to at most 200 characters.",
                "minLength": "Please lengthen your description to at least 100 characters."
            }
        },
        "end_date": {
            "pattern": "\\d{2}/\\d{2}/\\d{4}",
            "type": "string",
            "error": {
                "pattern": "This is not a valid date value."
            }
        },
        "files": {
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "maxLength": 64
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 3
                    }
                },
                "required": [
                    "name",
                    "title"
                ]
            },
            "type": "array",
            "minItems": 1
        },
        "start_date": {
            "pattern": "\\d{2}/\\d{2}/\\d{4}",
            "type": "string",
            "error": {
                "pattern": "This is not a valid date value."
            }
        },
        "subtitle": {
            "maxLength": 150,
            "type": "string",
            "error": {
                "maxLength": "Please shorten your subtitle to at most 150 characters."
            }
        },
        "title": {
            "maxLength": 150,
            "type": "string",
            "error": {
                "maxLength": "Please shorten your title to at most 150 characters."
            }
        },
        "year": {
            "minimum": 1600,
            "type": "integer",
            "error": {
                "minimum": "This year cannot be earlier than 1600."
            }
        },
        "year_type": {
            "type": "string"
        }
    },
    "required": [
        "files",
        "agency",
        "description",
        "title",
        "date_published",
        "subjects",
        "report_type",
        "year_type"
    ],
    "anyOf": [
        {
            "required": [
                "year"
            ]
        },
        {
            "required": [
                "end_date",
                "start_date"
            ]
        }
    ],
    "type": "object"
};

function validate_json(data, schema) {
    let v = new Validator();
    v.addSchema(schema, "/Submission");
    debugger;
}

export {validate_json, submissionSubset};
