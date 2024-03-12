import datetime
from http import HTTPStatus
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.mail_pool import MailPool
from app.models.menu import MenuPosition


def when_user_create_new_menu_position(test_client, position_name: str = "test_menu"):
    res = test_client.post(
        "/api/admin/menu/menu_position",
        json={
            "name": position_name,
            "price": 10.0,
            "description": "test_description",
            "preparation_time": 10,
            "is_vegan": False,
        },
    )
    assert res.status_code == HTTPStatus.CREATED

    return res.json()["id"]


def then_position_at_pool_should_be_x_times(db_api, position_id, x=1):
    position = db_api.query(MailPool).filter(MailPool.position_id == position_id).all()
    assert len(position) == x


def then_mail_pool_should_meet_expectations(
    db_api: Session, position_id: int, updated: bool, expected_date: datetime.date
):
    position = (
        db_api.query(MailPool)
        .filter(MailPool.position_id == position_id, MailPool.updated == updated)
        .filter(MailPool.date == expected_date)
        .filter(MailPool.updated == updated)
        .one_or_none()
    )
    assert position is not None


def test_new_menu_position_should_be_added_to_mail_pool(db_api, admin_cli):
    position_id = when_user_create_new_menu_position(admin_cli)

    then_position_at_pool_should_be_x_times(db_api, position_id)
    then_mail_pool_should_meet_expectations(
        db_api, position_id, updated=False, expected_date=datetime.date.today()
    )


def when_position_with_old_creation_date(db_api: Session) -> MenuPosition:
    position = MenuPosition(
        name="test_menu",
        price=10.0,
        description="test_description",
        preparation_time=10,
        is_vegan=False,
        created_at=datetime.datetime(2021, 1, 1),
        updated_at=datetime.datetime(2021, 1, 1),
    )
    db_api.add(position)
    db_api.commit()
    return position


def when_create_and_update_dates_are_from_yesterday(db_api, position_id):
    position = db_api.get(MenuPosition, position_id)
    position.created_at = datetime.datetime.now() - datetime.timedelta(days=1)
    position.updated_at = datetime.datetime.now() - datetime.timedelta(days=1)
    db_api.commit()


def when_user_edit_position(
    test_client, position_id, body: Optional[dict[str, Any]] = None
):
    if body is None:
        body = {"name": "test_menu2"}
    res = test_client.patch(
        f"/api/admin/menu/menu_position/{position_id}",
        json=body,
    )
    assert res.status_code == HTTPStatus.OK


def when_user_edit_position_yesterday(
    db_api: Session, test_client, position_id, body: Optional[dict[str, Any]] = None
):
    when_user_edit_position(test_client, position_id, body)
    mail_position = (
        db_api.query(MailPool)
        .filter(MailPool.position_id == position_id)
        .filter(MailPool.date == datetime.date.today())
        .one_or_none()
    )
    mail_position.date = datetime.date.today() - datetime.timedelta(days=1)
    db_api.commit()


def test_updated_menu_position_should_be_added_to_mail_pool(db_api, admin_cli):
    position = when_position_with_old_creation_date(db_api)
    when_user_edit_position(admin_cli, position.id)

    then_position_at_pool_should_be_x_times(db_api, position.id, x=1)


def test_updated_menu_twice_should_not_add_to_mail_pool_twice(db_api, admin_cli):
    position = when_position_with_old_creation_date(db_api)
    when_user_edit_position(admin_cli, position.id)
    when_user_edit_position(admin_cli, position.id)

    then_position_at_pool_should_be_x_times(db_api, position.id, x=1)


def test_updated_menu_twice_in_other_dates_should_add_to_mail_pool_twice(
    db_api, admin_cli
):
    position = when_position_with_old_creation_date(db_api)
    when_user_edit_position_yesterday(db_api, admin_cli, position.id)

    when_user_edit_position(admin_cli, position.id, body={"name": "test_menu3"})

    then_position_at_pool_should_be_x_times(db_api, position.id, x=2)


def deleted_menu_position_should_be_also_deleted_from_mail_pool(db_api, test_client):
    position_id = when_user_create_new_menu_position(test_client)

    test_client.delete(f"/api/admin/menu/menu_position/{position_id}")

    then_position_at_pool_should_be_x_times(db_api, position_id, x=0)


def test_deleted_menu_position_should_be_also_deleted_if_was_updated_yesterday(
    db_api, admin_cli
):
    position = when_position_with_old_creation_date(db_api)
    when_user_edit_position_yesterday(db_api, admin_cli, position.id)

    admin_cli.delete(f"/api/admin/menu/menu_position/{position.id}")

    then_position_at_pool_should_be_x_times(db_api, position.id, x=0)


def test_deleted_menu_positions_should_remove_all_of_mail_pool_records(
    db_api, admin_cli
):
    position = when_position_with_old_creation_date(db_api)
    when_user_edit_position_yesterday(db_api, admin_cli, position.id)
    when_user_edit_position(admin_cli, position.id, body={"name": "test_menu3"})

    admin_cli.delete(f"/api/admin/menu/menu_position/{position.id}")

    then_position_at_pool_should_be_x_times(db_api, position.id, x=0)


def test_created_menu_positions_should_be_added_to_mail_pool(db_api, admin_cli):
    position_ids = [
        when_user_create_new_menu_position(admin_cli, str(x)) for x in range(10)
    ]

    for position_id in position_ids:
        then_position_at_pool_should_be_x_times(db_api, position_id, x=1)
