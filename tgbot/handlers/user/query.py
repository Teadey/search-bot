from aiogram import Router
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode

from fluent.runtime import FluentLocalization

from tgbot.handlers.user.states.search import SearchSG
from tgbot.services.repository import Repo

router = Router(name=__name__)


@router.message()
async def query_handler(
    m: Message, l10n: FluentLocalization, repo: Repo, dialog_manager: DialogManager
):
    await dialog_manager.start(
        SearchSG.search, data={"query": m.text}, mode=StartMode.RESET_STACK
    )
