"""
    Helper functions for upload api
"""
import os
from flask import current_app


def parse_content_range(header):
    """
    Extracts the starting byte position and resource length.

    Content-Range = "Content-Range" ":" content-range-spec

    content-range-spec      = byte-content-range-spec
    byte-content-range-spec = bytes-unit SP
                              byte-range-resp-spec "/"
                              ( instance-length | "*" )
    byte-range-resp-spec    = (first-byte-pos "-" last-byte-pos)
                                  | "*"
    instance-length         = 1*DIGIT

    . The first 500 bytes:
        bytes 0-499/1234
    . The second 500 bytes:
        bytes 500-999/1234
    . All except for the first 500 bytes:
        bytes 500-1233/1234
    . The last 500 bytes:
        bytes 734-1233/1234

    :param header: the rhs of the content-range header
    :return: the first-byte-pos and instance-length
    """
    bytes_ = header.split(' ')[1]
    return int(bytes_.split('-')[0]), int(bytes_.split('/')[1])


def upload_exists(filename):
    return os.path.exists(
        os.path.join(current_app["UPLOAD_DIRECTORY"]),
        filename)
