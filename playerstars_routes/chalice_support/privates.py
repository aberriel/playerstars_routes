from .auth import cors, cupauth


def private(method):
    return dict(methods=[method], cors=cors, authorizer=cupauth)


def private_get():
    return private('GET')


def private_put():
    return private('PUT')


def private_post():
    return private('POST')


def private_delete():
    return private('DELETE')
