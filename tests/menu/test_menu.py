import uuid
from http import HTTPStatus

from app.models.menu import Menu
from tests.menu.fixtures import hundred_menus


def test_get_menu_should_return_ok_message(test_client):
    res = test_client.get("/api/menu")
    assert res.status_code == HTTPStatus.OK, res.text


def test_get_menu_should_return_empty_list_when_there_is_no_menus(test_client):
    res = test_client.get("/api/menu")
    assert res.json() == []


def test_create_new_menu_should_return_created_message(test_client, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)
    assert res.status_code == HTTPStatus.CREATED, res.text


def test_create_new_menu_should_create_new_record_in_db(test_client, db_api, json_basic_menu):
    res = test_client.post("/api/admin/menu", json=json_basic_menu)

    menu = db_api.query(Menu).get(res.json()["id"])
    assert menu is not None


def test_get_menu_should_return_list_of_enums(test_client, hundred_menus):
    res = test_client.get("/api/menu")
    assert len(res.json()) == 100


def test_get_not_existing_menu_should_return_not_found(test_client):
    res = test_client.get(f"/api/menu/{uuid.uuid4()}")
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