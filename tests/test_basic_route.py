import pytest
from playerstars_routes.basic_route import BasicChaliceRoute


def test_abstract_methods():
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().make_post_request('data')
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().get_all_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().not_found_message()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().not_found_all_message()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().get_request_model()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().get_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().save_exception()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().post_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().make_put_request('data')
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().update_exception()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().put_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().delete_request_model()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().delete_interactor()
    assert str(exc.value) == 'Não foi implementado'
    with pytest.raises(NotImplementedError) as exc:
        BasicChaliceRoute().delete_not_found()
    assert str(exc.value) == 'Não foi implementado'
