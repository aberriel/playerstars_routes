import pytest
from playerstars_routes.basic_route import BasicRoute


def test_abstract_methods():
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().make_post_request('data')
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().get_all_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().not_found_message()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().not_found_all_message()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().get_request_model()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().get_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().save_exception()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().post_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().make_put_request('data')
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().update_exception()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().put_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().delete_request_model()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().delete_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicRoute().delete_not_found()
    assert str(exc.value) == 'Não foi implementado'
