from io import BytesIO

from aiogram import Router, F
from aiogram.types import Message

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Column, Start

from tgbot.handlers.admin.states.menu import AdminMenuSG
from tgbot.handlers.admin.states.admins import AdminSG
from tgbot.handlers.admin.states.users import UserSG
from tgbot.filters.dialog.role import IsSudoFilter
from tgbot.filters.role import IsSudoFilter as IsSudoFilter_
from tgbot.services.l10n_dialog import L10NFormat
from tgbot.services.repository import Repo

router = Router(name=__name__)


admin_menu_dialog = Dialog(
    Window(
        L10NFormat("admin-start-text"),
        Column(
            Start(
                L10NFormat("admin-button-list-admins"),
                id="admin_lst",
                state=AdminSG.lst,
                when=IsSudoFilter(),
            ),
            Start(
                L10NFormat("admin-button-list-users"),
                id="user_lst",
                state=UserSG.lst,
            ),
        ),
        Cancel(L10NFormat("admin-button-close")),
        state=AdminMenuSG.main,
    ),
)


# router.include_routers(admin_menu_dialog)
