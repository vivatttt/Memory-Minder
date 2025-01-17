from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from backend.app.db.connection import get_session
from backend.app.utils.authorization import check_if_user_authorized
from frontend.bot.main_menu.handlers import show_unauthorized
from frontend.bot.main_menu.states import AuthorizationForm
from shared.utils.exception import UnknownUpdateTypeError


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async for session in get_session():
            data["session"] = session
            return await handler(event, data)


class AuthorizationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session = data["session"]
    
        if event.message:
            event_msg = event.message
            user_id = event_msg.from_user.id
        elif event.callback_query:
            event_msg = event.callback_query
            user_id = event_msg.from_user.id
        else:
            raise UnknownUpdateTypeError

        user_authorised = await check_if_user_authorized(id_=user_id, session=session)

        fsm_context = data.get('state')
        state = await fsm_context.get_state()

        if not user_authorised and isinstance(fsm_context, FSMContext) and state != AuthorizationForm.name_filled:
            await fsm_context.set_state(AuthorizationForm.waiting_for_name)
            return await show_unauthorized(event.message, fsm_context)
        return await handler(event, data)
