from unittest.mock import MagicMock, patch
from chalicelib import (
    cancel_duel_route, end_duel, enter_duel, get_all_duel,
    get_all_player_duels, get_duel, get_duels_by_status_route,
    get_match_list, get_opponent_list_route, inform_invitation_timeout,
    post_duel, reject_duel_route, get_duel_details,
    get_opponent_teams_for_duel, get_random_duel, put_random_duel,
    delete_random_duel, post_random_duel
)
from playerstars_interactors import (
    CancelDuelException,
    CreateDuelException,
    EndDuelException,
    EnterDuelException,
    GetDuelResponseModel,
    GetMatchListResponseModel,
    GetOpponentCandidateListException,
    GetOpponentCandidateListResponseModel,
    GetOpponentTeamsResponseModel,
    GetPlayerDuelByStatusError,
    InformOpponentResponseTimeoutException,
    RejectDuelException,
    PostPreDuelException)
from tests.test_utils import jwt

import json


def make_get_match_list_mock():
    payload = {
        "player_id": "pl01",
        "member_type": "PLAYER",
        "console_id": "con02"
    }
    return MagicMock(current_request=MagicMock(
        json_body=payload, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_match_list', make_get_match_list_mock())
@patch('chalicelib.duel_route.GetMatchListInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list(client, resource, run):
    result = get_match_list()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_match_list', make_get_match_list_mock())
@patch('chalicelib.duel_route.GetMatchListInteractor.run',
       MagicMock(return_value=GetMatchListResponseModel([])))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list_not_found(client, resource):
    result = get_match_list()

    assert 'Nenhum match encontrado para o player' in result.body['message']
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "console": {
        "name": "Super Nintendo",
        "logo_path": "/images/ss.png",
        "tag_name": "nick#1",
        "games" : []
        },
    "game":{
        "name": "Sonic",
        "logo_path": "images/sonic.jpg",
        "consoles": []
        },
    "maximum_time": "00:50:00",
    "minimum_time": "00:10:00",
    "bet_size": 90,
    "star_type" : "RED_STAR",
    "challenged": "idahsiasia",
    "duel_type": "INDIVIDUAL",
    "member_type": "PLAYER"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_create_duel', make_post_mock_data())
@patch('chalicelib.duel_route.CreateDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_create_duel(client, resourcem, run):
    result = post_duel()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_create_duel', make_post_mock_data())
@patch('chalicelib.duel_route.CreateDuelInteractor.run',
       MagicMock(side_effect=CreateDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_create_duel_raises(client, resource):
    result = post_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_inform_invite_timeout_mock_data():
    payload = """{
        "duel_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))

@patch('chalicelib.duel_route.bp_inform_invite_timeout',
       make_inform_invite_timeout_mock_data())
@patch('chalicelib.duel_route.InformOpponentResponseTimeoutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_inform_invite_timeout(client, resource, run):
    result = inform_invitation_timeout()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.duel_route.bp_inform_invite_timeout',
       make_inform_invite_timeout_mock_data())
@patch('chalicelib.duel_route.InformOpponentResponseTimeoutInteractor.run',
       MagicMock(side_effect=InformOpponentResponseTimeoutException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_inform_invite_timeout_raises(client, resource):
    result = inform_invitation_timeout()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_enter_duel_mock_data():
    payload = """{
        "duel_id": "duelid123",
        "lambda_function_name": "function1",
        "time_to_finish": 18000,
        "aws_region": "us-east-1"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_enter_duel',
       make_enter_duel_mock_data())
@patch('chalicelib.duel_route.EnterDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel(client, resource, run):
    result = enter_duel()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_enter_duel',
       make_enter_duel_mock_data())
@patch('chalicelib.duel_route.EnterDuelInteractor.run',
       MagicMock(side_effect=EnterDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel_raises(client, resource):
    result = enter_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_profile_request():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel(client, resource, run):
    result = get_all_player_duels()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel_not_found(client, resource):
    result = get_all_player_duels()

    assert result.body['message'] == \
        'No duel found for the player ' \
        '8ad1635f-2263-4dda-879a-bd24b5d9732f'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_duel(client, resource, run):
    result = get_all_duel()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_duel(client, resource):
    result = get_all_duel()

    assert result.body['message'] == 'No duel found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel(client, resource, run):
    result = get_duel('1234')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_duel(client, resource):
    result = get_duel('123123')

    assert result.body['message'] == 'Duel not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status(client, resource, run):
    result = get_duels_by_status_route('lobby')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status_not_found(client, resource):
    result = get_duels_by_status_route('lobby')

    assert result.body['message'] == \
        "No duel found with status lobby for the player" \
        " 8ad1635f-2263-4dda-879a-bd24b5d9732f"
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run',
       MagicMock(side_effect=GetPlayerDuelByStatusError('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status_not_found_raises(client, resource):
    result = get_duels_by_status_route('lobby')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_opponent_list_request():
    payload = """{
        "console_id": "consoleid123",
        "game_id": "gameid123",
        "duel_member_type": "player"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_opponent_list_request())
@patch('chalicelib.duel_route.GetOpponentCandidateListInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_list(client, resource, run):
    result = get_opponent_list_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_opponent_list_request())
@patch('chalicelib.duel_route.GetOpponentCandidateListInteractor.run',
       MagicMock(return_value=GetOpponentCandidateListResponseModel([])))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_list_not_found(client, resource):
    result = get_opponent_list_route()
    assert result.body['message'] == "No opponent candidate found"
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_opponent_list_request())
@patch('chalicelib.duel_route.GetOpponentCandidateListInteractor.run',
       MagicMock(side_effect=GetOpponentCandidateListException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_list_raises(client, resource):
    result = get_opponent_list_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_reject_request():
    payload = """{
        "duel_id": "id1234"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.duel_route.bp_duel', make_post_reject_request())
@patch('chalicelib.duel_route.RejectDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_reject_duel(client, resource, run):
    result = reject_duel_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_post_reject_request())
@patch('chalicelib.duel_route.RejectDuelInteractor.run',
       MagicMock(side_effect=RejectDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def teste_reject_duel_raises(client, resource):
    result = reject_duel_route()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_end_duel_request():
    payload = """{
        "duel_id": "id1234",
        "result": "win",
        "image_base64": "iuasdiuhafiasjdiyhviuasd"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


def make_get_duel_detail_request():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.duel_route.bp_duel', make_end_duel_request())
@patch('chalicelib.duel_route.EndDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_end_duel(client, resource, run):
    result = end_duel()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.duel_route.bp_duel', make_end_duel_request())
@patch('chalicelib.duel_route.EndDuelInteractor.run',
       MagicMock(side_effect=EndDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_end_duel_raises(client, resource):
    result = end_duel()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_cancel_duel_request():
    payload = """{
        "duel_id": "id1234"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.duel_route.bp_cancel_duel', make_cancel_duel_request())
@patch('chalicelib.duel_route.CancelDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_cancel_duel(client, resource, run):
    result = cancel_duel_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.duel_route.bp_cancel_duel', make_cancel_duel_request())
@patch('chalicelib.duel_route.CancelDuelInteractor.run',
       MagicMock(side_effect=CancelDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_cancel_duel_raises(client, resource):
    result = cancel_duel_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


@patch('chalicelib.duel_route.bp_duel', make_get_duel_detail_request())
@patch('chalicelib.duel_route.GetDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_detail(client, resource, run):
    result = get_duel_details('id123')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.duel_route.bp_duel', make_get_duel_detail_request())
@patch('chalicelib.duel_route.GetDuelInteractor.run',
       return_value=GetDuelResponseModel(None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_detail_empty(client, resource, run):
    result = get_duel_details('id123')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404


@patch('chalicelib.duel_route.bp_duel', make_get_duel_detail_request())
@patch('chalicelib.duel_route.GetDuelInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_detail_raises(client, resource, run):
    result = get_duel_details('id123')
    run.assert_called_once()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.duel_route.GetOpponentTeamsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_teams_for_duel(client, resource, run):
    result = get_opponent_teams_for_duel()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.duel_route.GetOpponentTeamsInteractor.run',
       return_value=GetOpponentTeamsResponseModel([]))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_teams_for_duel_empty(client, resource, run):
    result = get_opponent_teams_for_duel()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert result.body['message'] == \
        'No team found to be opponent of that team id'


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.duel_route.GetOpponentTeamsInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_opponent_teams_for_duel_raises(client, resource, run):
    result = get_opponent_teams_for_duel()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_random_duel(client, resource, run):
    result = delete_random_duel("schrubles")
    assert result


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_random_duel(client, resource, run):
    result = get_random_duel('schrubles')
    assert result


data = {
    "star_amount": 5,
    "duel_type": "PLAYER",
    "game_entity_id": "a8b7c2e4-7d89-4a24-965b-7c201e4bbe37",
    "star_type": "GOLDEN_STAR"
}


def post_preduel_run():
    return MagicMock(), 'success'


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           json_body=data)))
@patch('chalicelib.duel_route.PostPreDuelInteractor.run',
       return_value=post_preduel_run)
@patch('boto3.resource')
@patch('boto3.client')
def test_post_random_duel(client, resource, run):
    result = post_random_duel()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


def post_preduel_run2():
    return MagicMock(), 'created'


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           json_body=data)))
@patch('chalicelib.duel_route.PostPreDuelInteractor.run',
       return_value=post_preduel_run2)
@patch('boto3.resource')
@patch('boto3.client')
def test_post_random_duel_created(client, resource, run):
    result = post_random_duel()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           json_body=data)))
@patch('chalicelib.duel_route.PostPreDuelInteractor.run',
       side_effect=PostPreDuelException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_random_duel_raises(client, resource, run):
    result = post_random_duel()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.duel_route.PutPreDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_random_duel(client, resource, run):
    result = put_random_duel('entity_id', 'status')
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.duel_route.PutPreDuelInteractor.run',
       side_effect=PostPreDuelException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_random_duel_raises(client, resource, run):
    result = put_random_duel('entity_id', 'status')
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'
