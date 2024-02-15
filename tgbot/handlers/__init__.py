from aiogram import Router
from . import commands
from . import admin
from . import user
from . import register

__all__ = ("router",)

main_router = Router(name=__name__)

main_router.include_routers(
    commands.router,
    register.router,
    admin.router,
    user.router,
)
