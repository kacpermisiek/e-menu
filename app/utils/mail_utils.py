import datetime
import smtplib
from email.mime.text import MIMEText
from typing import Optional

from sqlalchemy.orm import Session

from app.db import get_session_constructor
from app.models.mail_pool import MailPool
from app.models.menu import MenuPosition
from app.models.user import User
from app.settings import settings
from app.utils.logger import get_logger

logger = get_logger("mail_utils")


def send_mail() -> None:
    session_maker = get_session_constructor(settings.database)
    with session_maker() as db:
        message, created, updated = create_message(db)
        if message:
            users_emails = [user.email for user in db.query(User).all()]
            msg = MIMEText(message)
            msg["Subject"] = "eMenu - Daily update"
            msg["From"] = settings.smtp_user

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(
                    settings.smtp_user, settings.smtp_password.get_secret_value()
                )
                smtp_server.sendmail(settings.smtp_user, users_emails, msg.as_string())
        else:
            logger.info("No new or updated positions, no mail sent")
    just_clear_mail_pool()


def create_message(db: Session):
    created, updated = get_created_and_updated_positions(db)
    if created or updated:
        message = prepare_mail_body(created, updated)
        return message, created, updated
    return None, None, None


def create_bullet_list(positions: list[MenuPosition]) -> str:
    return "\n".join([f"* {p.name} - {p.price} {settings.currency}" for p in positions])


def prepare_mail_body(
    created: Optional[list[MenuPosition]], updated: Optional[list[MenuPosition]]
) -> str:
    msg = "Hello,\n\nHere are some fresh menu positions:\n\n"

    if created:
        msg += f"New:\n{create_bullet_list(created)}\n"
    if updated:
        msg += f"Updated:\n{create_bullet_list(updated)}\n"
    msg += "Have a nice day!\n\neMenu team\n"

    return msg


def get_created_and_updated_positions(
    db: Session,
) -> tuple[list[MailPool], list[MailPool]]:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    today_pool = db.query(MailPool).filter(MailPool.date == yesterday)

    created_ids = [
        row.position_id for row in today_pool.filter(MailPool.updated == False).all()
    ]
    updated_ids = [
        row.position_id for row in today_pool.filter(MailPool.updated == True).all()
    ]

    created = db.query(MenuPosition).filter(MenuPosition.id.in_(created_ids)).all()
    updated = db.query(MenuPosition).filter(MenuPosition.id.in_(updated_ids)).all()

    for position in today_pool:
        db.delete(position)
    db.commit()
    return created, updated


def just_clear_mail_pool() -> None:
    session_maker = get_session_constructor(settings.database)
    with session_maker() as db:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        today_pool = db.query(MailPool).filter(MailPool.date < yesterday)
        for position in today_pool:
            db.delete(position)
        db.commit()
