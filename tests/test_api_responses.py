"""Testes para api_responses."""

from chalice import Response

from chalicelib.chalice_support.api_responses import (
    success, created, redirect, bad_request, not_found, server_error)


def test_all_responses():
    """Testa todos os responses."""
    response = success(dict(test=1))
    assert isinstance(response, Response)
    assert response.body.get('status') == 'success'
    assert response.body.get('data')['test'] == 1
    assert response.status_code == 200

    response = created(dict(test=1))
    assert isinstance(response, Response)
    assert response.body.get('status') == 'success'
    assert response.body.get('data')['test'] == 1
    assert response.status_code == 201

    response = redirect('dummy')
    assert isinstance(response, Response)
    assert 'Location' in response.headers
    assert response.headers.get('Location') == 'dummy'

    response = bad_request('bad dog!')
    assert response.body.get('status') == 'error'
    assert response.body.get('message') == 'bad dog!'
    assert response.status_code == 400

    response = not_found('cadê?')
    assert response.body.get('status') == 'error'
    assert response.body.get('message') == 'cadê?'
    assert response.status_code == 404

    response = server_error('oops!')
    assert response.body.get('status') == 'error'
    assert response.body.get('message') == 'oops!'
    assert response.status_code == 500
