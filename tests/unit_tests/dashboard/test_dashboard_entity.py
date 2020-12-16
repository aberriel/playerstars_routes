from chalicelib.dashboard.dashboard_entity import DashboardEntity


def test_dashboard_entity():
    dbe = DashboardEntity('cid')
    assert dbe.entity_id == 'cid'
    json_data = dbe.to_json()
    assert json_data == {'entity_id': 'cid'}
    ldbe = DashboardEntity.from_json(json_data)
    assert ldbe.entity_id == 'cid'
