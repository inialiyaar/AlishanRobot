import re
from telethon import events
from AlishanBot.core.bot import Alishan
from AlishanBot.__init__ import BOT_USERNAME

def add_command(*command_names):
    if len(command_names) == 1 and isinstance(command_names[0], (list, tuple)):
        command_names = command_names[0]

    commands_pattern = "|".join(command_names)
    pattern = rf"(?i)^/({commands_pattern})(?:@{BOT_USERNAME})?(?:\s+(.*))?$"

    def decorator(func):
        @Alishan.on(events.NewMessage(pattern=pattern))
        async def wrapper(event):
            text = event.raw_text

            match = re.match(pattern, text, flags=re.I)
            if not match:
                return

            command_used = match.group(1).lower()
            args = match.group(2) or None

            await func(event, command_used, args)

        return wrapper

    return decorator


def callback_query(data):
    def decorator(func):
        Alishan.add_event_handler(
            func, events.CallbackQuery(data=data.encode() if isinstance(data, str) else data)
        )
        return func

    return decorator