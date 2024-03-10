import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from app.db import get_session_constructor
from app.models.mail_pool import MailPool
from app.models.user import User
from app.settings import settings
from app.utils.logger import get_logger

logger = get_logger("mail_utils")


def send_mail() -> None:
    session_maker = get_session_constructor(settings.database)
    with session_maker() as db:
        message, created, updated = create_message(db)
        if message:
            users = db.query(User).all()
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.login(settings.user, settings.smtp_password)
                for user in users:
                    message["To"] = user.email
                    server.sendmail(settings.mail_from, user.email, message.as_string())
        else:
            logger.info("No new or updated positions, no mail sent")


def create_message(db: Session):
    created, updated = get_created_and_updated_positions(db)
    if created or updated:
        message = MIMEMultipart()
        message["From"] = settings.mail_from
        message["Subject"] = "eMenu - Daily update"
        message.attach(MIMEText(prepare_mail_body(created, updated), "plain"))
        return message, created, updated
    return None, None, None


def prepare_mail_body(creted, updated) -> str:
    created_bullet_list = "\n".join(
        [f"* {p.name} - {p.price} {settings.currency}" for p in creted]
    )
    updated_bullet_list = "\n".join(
        [f"* {p.name} - {p.price} {settings.currency}" for p in updated]
    )

    return (
        f"Hello,\n\n"
        f"Here are the new and updated menu positions:\n\n"
        f"New:\n"
        f"{created_bullet_list}\n"
        f"Updated:\n"
        f"{updated_bullet_list}\n\n"
        f"Have a nice day!"
        f"eMenu"
    )


def get_created_and_updated_positions(
    db: Session,
) -> tuple[list[MailPool], list[MailPool]]:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    today_pool = db.query(MailPool).filter(MailPool.date == yesterday)
    created = today_pool.filter(not MailPool.updated).all()
    updated = today_pool.filter(MailPool.updated).all()

    for position in today_pool:
        db.delete(position)
    db.commit()
    return created, updated


def just_clear_mail_pool() -> None:
    session_maker = get_session_constructor(settings.database)
    with session_maker() as db:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        today_pool = db.query(MailPool).filter(MailPool.date == yesterday)
        for position in today_pool:
            db.delete(position)
        db.commit()
