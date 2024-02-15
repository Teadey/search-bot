import logging

from aiogram import Router
from aiogram.types import Message

from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.input import TextInput

from fluent.runtime import FluentLocalization

from tgbot.config_reader import config
from tgbot.handlers.register.states.register import RegisterSG
from tgbot.services.l10n_dialog import L10NFormat
from tgbot.services.repository import Repo


router = Router(name=__name__)
logger = logging.getLogger(__name__)


def password_validate(password: str):
    if password != config.password.get_secret_value():
        raise ValueError


async def password_invalid(
    m: Message, _: TextInput, dilaog_manager: DialogManager, __: ValueError
):
    l10n: FluentLocalization = dilaog_manager.middleware_data["l10n"]
    await m.reply(l10n.format_value("register-password-invalid"))


async def register_handler(
    m: Message, _: TextInput, dilaog_manager: DialogManager, __: str
):
    repo: Repo = dilaog_manager.middleware_data["repo"]
    l10n: FluentLocalization = dilaog_manager.middleware_data["l10n"]

    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username,
    )
    await m.answer(l10n.format_value("register-password-success"))
    await dilaog_manager.done()


register_dialog = Dialog(
    Window(
        L10NFormat("register-password-request"),
        TextInput(
            id="password",
            type_factory=password_validate,
            on_success=register_handler,
            # on_error=password_invalid,
        ),
        state=RegisterSG.password,
    ),
)


router.include_routers(
    register_dialog,
)
