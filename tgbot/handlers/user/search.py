from typing import Any

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, Dialog, Window, StartMode, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Format, List, Const
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup, Back, Button, Next

from fluent.runtime import FluentLocalization

from tgbot.handlers.user.states.search import SearchSG
from tgbot.services.l10n_dialog import L10NFormat
from tgbot.services.repository import Repo

router = Router(name=__name__)


def dump_model(model: dict, none_value: Any = 0) -> dict:
    for k, v in model.items():
        if v is None:
            model[k] = none_value

    return model


async def search_addresses(dialog_manager: DialogManager, repo: Repo, **_):
    query = dialog_manager.dialog_data.get("query") or dialog_manager.start_data.get(
        "query"
    )
    dialog_manager.dialog_data["query"] = query

    res = await repo.search_address(query=query)
    return {"addresses": res, "query": query}


async def get_address(dialog_manager: DialogManager, **_):
    return dump_model(dialog_manager.dialog_data)


async def get_comments(dialog_manager: DialogManager, repo: Repo, **_):
    address_id = dialog_manager.dialog_data["address_id"]

    comments = await repo.list_comment(address_id=address_id)
    comments = [
        {
            "username": comment.username or comment.firstname,
            "text": comment.text,
            "date": comment.created_on.strftime("%d.%m.%y %H:%M"),
        }
        for comment in comments
    ]
    return {"comments": comments, **dialog_manager.dialog_data}


async def query_handler(
    m: Message, _: TextInput, dialog_manager: DialogManager, query: str
):
    await dialog_manager.start(
        SearchSG.search,
        data={"query": m.text},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def show_address(
    callback: CallbackQuery,
    select: Select,
    dialog_manager: DialogManager,
    address_id: str,
):
    repo: Repo = dialog_manager.middleware_data["repo"]
    l10n: FluentLocalization = dialog_manager.middleware_data["l10n"]

    address_info = await repo.get_address(int(address_id))
    if not address_info:
        await callback.answer(
            l10n.format_value("user-search-not-available"), show_alert=True
        )
        return

    dialog_manager.dialog_data.update(
        {
            "address_id": address_info.id,
            "tip": address_info.tip,
            "number": address_info.number,
            "place": address_info.place,
            "birka": address_info.birka,
            "comment": address_info.comment,
            "gps": address_info.gps,
            "copy_box_number": address_info.copy_box_number,
        }
    )
    await dialog_manager.next()


async def comment_handler(
    m: Message, _: TextInput, dialog_manager: DialogManager, comment: str
):
    repo: Repo = dialog_manager.middleware_data["repo"]
    address_id = dialog_manager.dialog_data["address_id"]

    await repo.add_comment(user_id=m.from_user.id, address_id=address_id, text=comment)
    await dialog_manager.back()


QUERY_INPUT = TextInput(
    id="query_input",
    on_success=query_handler,
)


search_dialog = Dialog(
    Window(
        L10NFormat("user-search-result", when=F["addresses"]),
        L10NFormat("user-search-not-found", when=~F["addresses"]),
        QUERY_INPUT,
        ScrollingGroup(
            Select(
                Format("{item[place]}"),
                id="addr",
                item_id_getter=lambda item: item.id,
                items="addresses",
                on_click=show_address,
            ),
            id="addr_sg",
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        getter=search_addresses,
        state=SearchSG.search,
    ),
    Window(
        L10NFormat("user-search-detail"),
        QUERY_INPUT,
        Next(L10NFormat("user-button-show-comments")),
        Back(L10NFormat("admin-button-back")),
        getter=get_address,
        state=SearchSG.detail,
    ),
    Window(
        L10NFormat("user-search-comments"),
        List(
            Format("[<i>{item[date]}</i>] <b>{item[username]}</b>: {item[text]}"),
            items="comments",
        ),
        Button(
            L10NFormat("user-button-refresh"),
            id="refresh",
        ),
        Next(L10NFormat("user-button-add-comment")),
        Back(L10NFormat("admin-button-back")),
        getter=get_comments,
        state=SearchSG.comment,
    ),
    Window(
        L10NFormat("user-comment-request"),
        TextInput(
            id="comment_input",
            on_success=comment_handler,
        ),
        Back(L10NFormat("admin-button-back")),
        getter=get_address,
        state=SearchSG.add_comment,
    ),
)


router.include_routers(
    search_dialog,
)
