from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode
from fluent.runtime import FluentLocalization

from tgbot.handlers.register.states.register import RegisterSG
from tgbot.services.repository import Repo

router = Router(name=__name__)


@router.message(Command("start"))
async def start_handler(
    m: Message, l10n: FluentLocalization, repo: Repo, dialog_manager: DialogManager
):
    if not await repo.get_user(m.from_user.id):
        await dialog_manager.start(RegisterSG.password, mode=StartMode.RESET_STACK)
        return

    await m.answer(l10n.format_value("user-start-text"))
