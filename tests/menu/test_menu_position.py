import uuid
from http import HTTPStatus

import pytest

from app.models.menu import Menu, MenuPosition
from app.utils.vars import MAX_INT_64
from tests.menu.fixtures import hundred_menu_positions


def test_create_menu_position_should_return_created_message(
    test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text


def test_create_menu_position_should_add_position_to_database(
    db_api, test_client, json_basic_menu_position
):
    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 0

    test_client.post("api/admin/menu/menu_position", json=json_basic_menu_position)

    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 1


def test_create_menu_position_with_the_same_name_should_raise_http_error(
    db_api, test_client, with_menu_position
):
    data = {
        "name": with_menu_position.name,
        "price": 100,
        "description": "Some description",
        "preparation_time": 123,
        "is_vegan": True,
    }
    res = test_client.post("api/admin/menu/menu_position", json=data)
    assert res.status_code == HTTPStatus.BAD_REQUEST, res.text


def test_create_menu_position_with_some_menu_should_add_position_to_database(
    db_api, test_client, with_menu
):
    data = {
        "name": "Some name",
        "price": 100,
        "description": "Some description",
        "preparation_time": 123,
        "is_vegan": True,
        "menus": [with_menu.id],
    }
    res = test_client.post("api/admin/menu/menu_position", json=data)
    assert res.status_code == HTTPStatus.CREATED, res.text
    menu_position = db_api.query(MenuPosition).first()
    assert len(menu_position.menus) == 1
    assert menu_position.menus[0].id == with_menu.id


def test_create_menu_position_should_add_position_with_proper_data(
    db_api, test_client, json_basic_menu_position
):
    test_client.post("api/admin/menu/menu_position", json=json_basic_menu_position)

    menu_position = db_api.query(MenuPosition).first()
    assert menu_position.name == json_basic_menu_position["name"]
    assert menu_position.price == json_basic_menu_position["price"]
    assert menu_position.description == json_basic_menu_position["description"]
    assert (
        menu_position.preparation_time == json_basic_menu_position["preparation_time"]
    )
    assert menu_position.is_vegan == json_basic_menu_position["is_vegan"]
    assert menu_position.id is not None
    assert menu_position.created_at is not None
    assert menu_position.updated_at is not None
    assert menu_position.created_at == menu_position.updated_at
    assert len(menu_position.menus) == 0
    assert menu_position.menus == []


def test_create_many_menu_positions_should_add_positions_to_database(
    db_api, test_client, json_basic_menu_position
):
    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 0

    for i in range(10):
        json_basic_menu_position["name"] = json_basic_menu_position["name"] + str(i)
        res = test_client.post(
            "api/admin/menu/menu_position", json=json_basic_menu_position
        )
        assert res.status_code == HTTPStatus.CREATED, res.text

    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 10


@pytest.mark.parametrize(
    "name, value",
    [
        ("name", 1),
        ("name", 1.0),
        ("name", ""),
        ("name", True),
        ("name", "a" * 256),
        ("price", "test"),
        ("price", MAX_INT_64 + 1),
        ("price", -1),
        ("price", -1.0),
        ("description", 1),
        ("description", 1.0),
        ("description", True),
        ("preparation_time", "test"),
        ("preparation_time", MAX_INT_64 + 1),
        ("preparation_time", -1),
        ("preparation_time", -1.0),
        ("is_vegan", "test"),
    ],
)
def test_create_menu_position_with_wrong_parameter_format_should_raise_http_error(
    test_client, json_basic_menu_position, name, value
):
    json_basic_menu_position[name] = value
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, res.text


def test_get_menu_positions_should_return_all_of_positions(
    db_api, test_client, hundred_menu_positions
):
    res = test_client.get("api/admin/menu/menu_position")
    assert res.status_code == HTTPStatus.OK, res.text

    menu_positions = res.json()
    assert len(menu_positions) == 100


def test_get_zero_menu_positions_should_return_empty_list(db_api, test_client):
    res = test_client.get("api/admin/menu/menu_position")
    assert res.status_code == HTTPStatus.OK, res.text

    menu_positions = res.json()
    assert menu_positions == []


def test_get_not_existing_menu_position_should_return_http_error(
    test_client,
):
    res = test_client.get(f"api/admin/menu/menu_position/6661")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_get_existing_menu_position_should_return_proper_position(
    db_api, test_client, json_basic_menu_position
):
    test_client.post("api/admin/menu/menu_position", json=json_basic_menu_position)

    menu_position = db_api.query(MenuPosition).first()
    res = test_client.get(f"api/admin/menu/menu_position/{menu_position.id}")
    assert res.status_code == HTTPStatus.OK, res.text

    menu_position_response = res.json()
    assert menu_position_response["id"] == menu_position.id
    assert menu_position_response["name"] == menu_position.name
    assert menu_position_response["price"] == menu_position.price
    assert menu_position_response["description"] == menu_position.description
    assert menu_position_response["preparation_time"] == menu_position.preparation_time
    assert menu_position_response["is_vegan"] == menu_position.is_vegan
    assert menu_position_response["created_at"] == menu_position.created_at.isoformat()
    assert menu_position_response["updated_at"] == menu_position.updated_at.isoformat()


@pytest.mark.parametrize(
    "menu_position_id",
    ["test", "test-test", "test_test", "deadbeefdeadbeefdeadbeefdead"],
)
def test_get_menu_position_with_wrong_format_of_id_should_raise_http_error(
    test_client, menu_position_id
):
    res = test_client.get(f"api/admin/menu/menu_position/{menu_position_id}")
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, res.text


@pytest.mark.parametrize(
    "name, new_value", [("name", "another_name"), ("price", 21.38)]
)
def test_patch_menu_position_should_return_proper_value_and_change_it_in_db(
    db_api, test_client, name, new_value, with_menu_position
):
    res = test_client.patch(
        f"api/admin/menu/menu_position/{with_menu_position.id}", json={name: new_value}
    )
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()[name] == new_value

    res = test_client.get(f"api/admin/menu/menu_position/{with_menu_position.id}")
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()[name] == new_value


def test_patch_menu_should_change_updated_at_parameter(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    res = test_client.get(f"api/admin/menu/menu_position/{position_id}")
    created_at = res.json()["created_at"]
    updated_at = res.json()["updated_at"]

    res = test_client.patch(
        f"api/admin/menu/menu_position/{position_id}", json={"name": "another_name"}
    )
    assert res.status_code == HTTPStatus.OK, res.text

    res = test_client.get(f"api/admin/menu/menu_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()["created_at"] == created_at
    assert res.json()["updated_at"] > updated_at


def test_patch_menu_position_without_data(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    res = test_client.patch(f"api/admin/menu/menu_position/{position_id}", json={})
    assert res.status_code == HTTPStatus.OK, res.text


def test_patch_menu_position_menus_should_update_info_in_menu(
    db_api, test_client, with_menu_with_position
):
    position_id = with_menu_with_position.positions[0].id
    data = {"menus": []}
    test_client.patch(f"api/admin/menu/menu_position/{position_id}", json=data)

    get_menu_resp = test_client.get(f"api/menu/{with_menu_with_position.id}")
    assert len(get_menu_resp.json()["positions"]) == 0


def test_patch_menu_position_menus_should_also_add_positions_in_menu(
    db_api, test_client, with_menu, with_menu_position
):
    data = {"menus": [with_menu.id]}
    test_client.patch(
        f"api/admin/menu/menu_position/{with_menu_position.id}", json=data
    )

    get_menu_resp = test_client.get(f"api/menu/{with_menu.id}")
    assert len(get_menu_resp.json()["positions"]) == 1


def test_patch_menu_position_with_wrong_id_should_raise_http_error(
    test_client, json_basic_menu_position
):
    res = test_client.patch(
        f"api/admin/menu/menu_position/123", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_update_menu_position_should_return_value_and_change_it_in_db(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    data = {
        "name": "another_name",
        "price": 21.38,
        "description": "another_description",
        "preparation_time": 20,
        "is_vegan": True,
        "menus": [],
    }

    res = test_client.put(f"api/admin/menu/menu_position/{position_id}", json=data)

    assert res.status_code == HTTPStatus.OK, res.text


def test_update_menu_position_without_all_parameters_should_raise_http_error(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    data = {
        "name": "another_name",
        "price": 21.38,
        "description": "another_description",
        "preparation_time": 20,
        "menus": [],
    }

    res = test_client.put(f"api/admin/menu/menu_position/{position_id}", json=data)

    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, res.text


def test_update_menu_position_with_wrong_id_should_raise_http_error(
    test_client, json_basic_menu_position
):
    res = test_client.put(
        f"api/admin/menu/menu_position/235235234",
        json=json_basic_menu_position | {"menus": []},
    )
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_update_menu_position_should_update_info_in_menu(
    db_api, test_client, with_menu_with_position
):
    position_id = with_menu_with_position.positions[0].id
    data = {
        "name": "another_name",
        "price": 21.38,
        "description": "another_description",
        "preparation_time": 20,
        "is_vegan": True,
        "menus": [with_menu_with_position.id],
    }
    res = test_client.put(f"api/admin/menu/menu_position/{position_id}", json=data)
    assert res.status_code == HTTPStatus.OK, res.text

    get_position_resp = test_client.get(f"api/admin/menu/menu_position/{position_id}")
    assert get_position_resp.json()["name"] == "another_name"

    get_menu_resp = test_client.get(f"api/menu/{with_menu_with_position.id}")
    assert get_menu_resp.json()["positions"][0]["name"] == "another_name"


def test_update_menu_position_menus_should_update_info_in_menu(
    db_api, test_client, with_menu_with_position
):
    position_id = with_menu_with_position.positions[0].id
    data = {
        "name": "another_name",
        "price": 21.38,
        "description": "another_description",
        "preparation_time": 20,
        "is_vegan": True,
        "menus": [],
    }
    res = test_client.put(f"api/admin/menu/menu_position/{position_id}", json=data)
    assert res.status_code == HTTPStatus.OK, res.text

    get_position_resp = test_client.get(f"api/admin/menu/menu_position/{position_id}")
    assert get_position_resp.json()["name"] == "another_name"

    get_menu_resp = test_client.get(f"api/menu/{with_menu_with_position.id}")
    assert len(get_menu_resp.json()["positions"]) == 0


def test_delete_menu_position_with_wrong_id_should_raise_http_error(
    test_client,
):
    res = test_client.delete(f"api/admin/menu/menu_position/12314523423423423")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_delete_menu_position_should_return_menu_position_parameters(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    res = test_client.delete(f"api/admin/menu/menu_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()["id"] == position_id
    assert res.json()["name"] == json_basic_menu_position["name"]
    assert res.json()["price"] == json_basic_menu_position["price"]
    assert res.json()["description"] == json_basic_menu_position["description"]
    assert (
        res.json()["preparation_time"] == json_basic_menu_position["preparation_time"]
    )
    assert res.json()["is_vegan"] == json_basic_menu_position["is_vegan"]
    assert res.json()["created_at"] == res.json()["updated_at"]
    assert res.json()["id"] is not None
    assert res.json()["created_at"] is not None
    assert res.json()["updated_at"] is not None
    assert res.json()["created_at"] == res.json()["updated_at"]


def test_delete_menu_position_should_remove_position_from_db(
    db_api, test_client, json_basic_menu_position
):
    res = test_client.post(
        "api/admin/menu/menu_position", json=json_basic_menu_position
    )
    assert res.status_code == HTTPStatus.CREATED, res.text
    position_id = res.json()["id"]

    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 1

    res = test_client.delete(f"api/admin/menu/menu_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text

    menu_positions = db_api.query(MenuPosition).all()
    assert len(menu_positions) == 0
