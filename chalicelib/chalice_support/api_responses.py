"""Uniform api responses."""

from chalice import Response


def success_dict(data):
    """Returns success dict with specified data."""
    return dict(status='success',
                data=data)


def error_dict(message):
    """Returns error dict with specified message."""
    return dict(status='error',
                message=message)


def success(data=None):
    """Returns success response with specified data."""
    return Response(success_dict(data), status_code=200)


def created(data=None):
    """Returns 'Created with Success' response with created data."""
    return Response(success_dict(data), status_code=201)


def redirect(url):
    """Returns redirect response with location to redirect."""
    return Response(body=None, headers=dict(Location=url), status_code=302)


def bad_request(message):
    """Returns 'Bad Request' error with details on message."""
    return Response(body=error_dict(message), status_code=400)


def not_found(message):
    """Returns 'Not Found' error with details on message."""
    return Response(body=error_dict(message), status_code=404)


def server_error(message):
    """Returns internal server error with details on message."""
    return Response(body=error_dict(message), status_code=500)


def success_partial(data, range_units, range_from, range_to, range_total):
    """Retorna partial content."""
    range_data = f"{range_units} {range_from}-{range_to}/{range_total}"
    headers = {"Content-Range": range_data}
    return Response(success_dict(data), status_code=206, headers=headers)


def unauthorized(message):
    """Retorna unauthorized com o message especificado."""
    return Response(body=error_dict(message), status_code=401)
