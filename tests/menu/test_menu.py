import uuid
from http import HTTPStatus

from app.models.menu import Menu, MenuMenuPosition, MenuPosition
from tests.menu.fixtures import hundred_menu_positions, hundred_menus


def test_get_menu_should_return_ok_message(test_client):
    res = test_client.get("/api/menu")
    assert res.status_code == HTTPStatus.OK, res.text


def test_get_menu_should_return_empty_list_when_there_is_no_menus(test_client):
    res = test_client.get("/api/menu")
    assert res.json() == []


def test_create_new_menu_should_return_created_message(test_client, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text


def test_create_new_menu_should_create_new_record_in_db(
    test_client, db_api, json_basic_menu
):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)

    menu = db_api.get(Menu, res.json()["id"])
    assert menu is not None


def test_get_menu_should_return_list_of_enums(test_client, hundred_menus):
    res = test_client.get("/api/menu")
    assert len(res.json()) == 100


def test_get_not_existing_menu_should_return_not_found(test_client):
    res = test_client.get(f"/api/menu/123")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_get_menu_should_return_it_params(test_client, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text

    menu_id = res.json()["id"]

    res = test_client.get(f"/api/menu/{menu_id}")
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()["name"] == json_basic_menu["name"]


def test_patch_menu_should_return_ok_message(test_client, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text

    menu_id = res.json()["id"]

    res = test_client.patch(f"/api/admin/menu/{menu_id}", json={"name": "new_name"})
    assert res.status_code == HTTPStatus.OK, res.text


def test_patch_menu_should_update_record_in_db(test_client, db_api, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    menu_id = res.json()["id"]

    test_client.patch(f"/api/admin/menu/{menu_id}", json={"name": "new_name"})

    menu = db_api.get(Menu, menu_id)
    assert menu.name == "new_name"


def test_delete_menu_should_return_ok_message(test_client, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text

    menu_id = res.json()["id"]

    res = test_client.delete(f"/api/admin/menu/{menu_id}")
    assert res.status_code == HTTPStatus.OK, res.text


def test_delete_menu_should_delete_record_in_db(test_client, db_api, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text

    menu_id = res.json()["id"]

    res = test_client.delete(f"/api/admin/menu/{menu_id}")
    assert res.status_code == HTTPStatus.OK, res.text

    menu = db_api.get(Menu, menu_id)
    assert menu is None


def test_delete_menu_with_wrong_id_should_return_not_found(test_client):
    res = test_client.delete(f"/api/admin/menu/123")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_add_menu_position_to_menu_should_return_ok_message(
    test_client, json_basic_menu, with_menu_position
):
    menu_id = test_client.post("/api/admin/menu", json=json_basic_menu).json()["id"]

    res = test_client.post(
        f"/api/admin/menu/{menu_id}/add_position/{with_menu_position.id}"
    )
    assert res.status_code == HTTPStatus.OK, res.text


def test_add_menu_position_to_menu_should_add_it_in_db(
    test_client, db_api, with_menu_position, json_basic_menu
):
    menu_id = test_client.post("/api/admin/menu", json=json_basic_menu).json()["id"]

    test_client.post(f"/api/admin/menu/{menu_id}/add_position/{with_menu_position.id}")

    menu = db_api.get(Menu, menu_id)
    assert len(menu.positions) == 1
    assert menu.positions[0].id == with_menu_position.id

    menu_menu_position = (
        db_api.query(MenuMenuPosition)
        .filter_by(menu_id=menu_id, menu_position_id=with_menu_position.id)
        .first()
    )
    assert menu_menu_position is not None


def test_add_the_same_menu_position_to_menu_should_return_bad_request(
    test_client, json_basic_menu, with_menu_position
):
    menu_id = test_client.post("/api/admin/menu", json=json_basic_menu).json()["id"]

    test_client.post(f"/api/admin/menu/{menu_id}/add_position/{with_menu_position.id}")
    res = test_client.post(
        f"/api/admin/menu/{menu_id}/add_position/{with_menu_position.id}"
    )
    assert res.status_code == HTTPStatus.BAD_REQUEST, res.text


def test_add_not_existing_menu_position_to_menu_should_return_not_found(
    test_client, json_basic_menu
):
    menu_id = test_client.post("/api/admin/menu", json=json_basic_menu).json()["id"]

    res = test_client.post(f"/api/admin/menu/{menu_id}/add_position/123")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_add_menu_position_to_not_existing_menu_should_return_not_found(
    test_client, with_menu_position
):
    res = test_client.post(f"/api/admin/menu/123/add_position/{with_menu_position.id}")
    assert res.status_code == HTTPStatus.NOT_FOUND, res.text


def test_get_menu_positions_should_return_list_of_menu_positions(
    test_client, json_basic_menu, with_menu_position
):
    menu_id = test_client.post("/api/admin/menu", json=json_basic_menu).json()["id"]

    test_client.post(f"/api/admin/menu/{menu_id}/add_position/{with_menu_position.id}")

    res = test_client.get(f"/api/menu/{menu_id}")
    assert len(res.json()["positions"]) == 1

    position = res.json()["positions"][0]

    assert position["id"] == with_menu_position.id
    assert position["name"] == with_menu_position.name
    assert position["price"] == with_menu_position.price
    assert position["description"] == with_menu_position.description
    assert position["preparation_time"] == with_menu_position.preparation_time
    assert position["is_vegan"] == with_menu_position.is_vegan
    assert position["created_at"] is not None
    assert position["updated_at"] is not None


def test_add_menu_position_to_two_different_menus_should_return_ok_message_and_create_records_in_db(
    db_api, test_client, hundred_menus, hundred_menu_positions
):
    menu_id_1 = 1
    menu_id_2 = 2

    menu_position_id = 1

    res = test_client.post(
        f"/api/admin/menu/{menu_id_1}/add_position/{menu_position_id}"
    )
    assert res.status_code == HTTPStatus.OK, res.text

    res = test_client.post(
        f"/api/admin/menu/{menu_id_2}/add_position/{menu_position_id}"
    )
    assert res.status_code == HTTPStatus.OK, res.text

    menu_1 = db_api.get(Menu, menu_id_1)
    menu_2 = db_api.get(Menu, menu_id_2)

    assert len(menu_1.positions) == 1
    assert len(menu_2.positions) == 1
    assert menu_1.positions[0].id == menu_position_id
    assert menu_2.positions[0].id == menu_position_id

    menu_menu_position_1 = db_api.get(MenuPosition, menu_position_id)
    assert len(menu_menu_position_1.menus) == 2
    assert menu_menu_position_1.menus[0].id == menu_id_1
    assert menu_menu_position_1.menus[1].id == menu_id_2


def test_remove_position_from_menu_should_return_ok_message(
    test_client, with_menu_with_position
):
    menu_id = with_menu_with_position.id
    position_id = with_menu_with_position.positions[0].id
    res = test_client.post(f"/api/admin/menu/{menu_id}/remove_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text


def test_remove_position_from_menu_should_not_remove_position_from_db(
    db_api, test_client, with_menu_with_position
):
    menu_id = with_menu_with_position.id
    position_id = with_menu_with_position.positions[0].id
    test_client.post(f"/api/admin/menu/{menu_id}/remove_position/{position_id}")

    db_api.refresh(with_menu_with_position)
    position = db_api.get(MenuPosition, position_id)
    assert position is not None

    res = test_client.get(f"/api/admin/menu/menu_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text
    assert res.json()["id"] == position_id


def test_remove_position_from_db_should_remove_it_from_menu(
    test_client, db_api, with_menu_with_position
):
    menu_id = with_menu_with_position.id
    position_id = with_menu_with_position.positions[0].id

    menu = db_api.get(Menu, menu_id)
    assert len(menu.positions) == 1

    res = test_client.delete(f"/api/admin/menu/menu_position/{position_id}")
    assert res.status_code == HTTPStatus.OK, res.text

    res = test_client.get(f"/api/menu/{menu_id}")
    assert res.json()["positions"] == []

    db_api.refresh(menu)
    assert len(menu.positions) == 0
