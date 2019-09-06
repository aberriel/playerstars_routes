"""Uniform api responses."""

from chalice import Response


def success_dict(data):
    """Retorna dict de sucesso com o data especificado."""
    return dict(status='success',
                data=data)


def error_dict(message):
    """Retorna dict de erro com o message especificado."""
    return dict(status='error',
                message=message)


def success(data=None):
    """Retorna sucesso com o data especificado."""
    return Response(success_dict(data), status_code=200)


def created(data=None):
    """Retorna criado com o data especificado."""
    return Response(success_dict(data), status_code=201)


def redirect(url):
    """Retorna redirect com o location especificado."""
    return Response(body=None, headers=dict(Location=url), status_code=302)


def bad_request(message):
    """Retorna bad request com o message especificado."""
    return Response(body=error_dict(message), status_code=400)


def not_found(message):
    """Retorna not found com o message especificado."""
    return Response(body=error_dict(message), status_code=404)


def server_error(message):
    """Retorna erro interno do servidor com o message especificado."""
    return Response(body=error_dict(message), status_code=500)
