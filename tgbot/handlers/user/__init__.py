from aiogram import Router, F
from aiogram.enums.chat_type import ChatType

from tgbot.filters.role import IsRegisteredFilter

from . import search
from . import query

__all__ = ("router",)

router = Router(name=__name__)
router.message.filter(IsRegisteredFilter(), F.chat.type.in_({ChatType.PRIVATE}))
router.callback_query.filter(
    IsRegisteredFilter(),
    F.message.chat.type.in_({ChatType.PRIVATE}),
)

router.include_routers(
    search.router,
    query.router,
)
