from aiogram import Router
from . import register

__all__ = ("router",)

router = Router(name=__name__)

router.include_routers(
    register.router,
)
