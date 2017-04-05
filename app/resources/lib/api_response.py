"""
    JSend-compliant JSON responses (https://labs.omniti.com/labs/jsend)

"""
from flask import jsonify


def success(data=None, status_code=200):
    """
    All went well, and (usually) some data was returned.

    Required keys:
        status - Should always be set to "success".
        data - Acts as the wrapper for any data returned by the API call.
               If the call returns no data, data should be set to null.

    Examples:

        GET /posts
        {
            "status": "success",
            "data": {
                "posts": [
                    { "id": 1, "title" : "A blog post" },
                    { "id": 2, "title" : "Another blog post" },
                ]
            }
        }

        GET /post/2
        {
            "status": "success",
            "data": {
                "post": { "id": 2, "title" : "Another blog post" }
            }
        }

        DELETE /post/2
        {
            "status": "success",
            "data": null
        }
    """
    return _response('success', status_code, data=data)


def fail(data, status_code=200):
    """
    There was a problem with the data submitted, or
    some pre-condition of the API call wasn't satisfied.

    Required keys:
        status - Should always be set to "fail".
        data - Provides the wrapper for the details of why the request failed.
               If the reasons for failure correspond to POST values, the response
               object's keys SHOULD correspond to those POST values.

    Example:
        POST /post
        {
            "status": "fail",
            "data": { "title": "This field is required" }
        }
    """
    return _response('fail', status_code, data=data)


def error(message: str, code: int=None, data=None):
    """
    An error occurred in processing the request, i.e. an exception was thrown.
    Response status code: 500

    Required Keys:
        status - Should always be set to "error".
        message -  A meaningful, end-user-readable (or at the least log-worthy)
                   message, explaining what went wrong.

    Optional Keys:
        code - A numeric code corresponding to the error, if applicable.
        data - A generic container for any other information about the error,
               i.e. the conditions that caused the error, stack traces, etc.

    Example:
        GET /posts
        {
            "status": "error",
            "message": "Unable to communicate with database"
        }
    """
    keys = {"message": message}
    for key, val in {"code": code, "data": data}.items():
        if val is not None:
            keys[key] = val
    return _response('error', 500, **keys)


def _response(status, status_code, **kwargs):
    response = jsonify({
        'status': status,
        **kwargs
    })
    response.status_code = status_code
    return response
