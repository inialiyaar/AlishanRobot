from AlishanBot.core.bot import Alishan, Assistant



_info = {
    "BOT_ID": None,
    "BOT_USERNAME": None,
    "BOT_FULL_NAME": None,
    "BOT_MENTION": None,
    "ASSISTANT_ID": None,
    "ASSISTANT_USERNAME": None,
    "ASSISTANT_FULL_NAME": None,
    "ASSISTANT_MENTION": None,
}


async def load_info():
    bot = await Alishan.get_me()
    assistant_user = await Assistant.get_me()

    bot_full_name = f"{bot.first_name or ''} {bot.last_name or ''}"
    assistant_full_name = f"{assistant_user.first_name or ''} {assistant_user.last_name or ''}"

    _info.update({
        "BOT_ID": bot.id,
        "BOT_USERNAME": bot.username,
        "BOT_FULL_NAME": bot_full_name,
        "BOT_MENTION": f'<a href="tg://user?id={bot.id}">{bot_full_name}</a>',
        "ASSISTANT_ID": assistant_user.id,
        "ASSISTANT_USERNAME": assistant_user.username,
        "ASSISTANT_FULL_NAME": assistant_full_name,
        "ASSISTANT_MENTION": f"<a href\"tg://user?id={assistant_user.id}\">{assistant_full_name}</a>",
    })


def get_info() -> dict:
    return _info


def get_bot_info() -> dict:
    return {
        "id": _info["BOT_ID"],
        "username": _info["BOT_USERNAME"],
        "fullname": _info["BOT_FULL_NAME"],
        "mention": _info["BOT_MENTION"],
    }


def get_assistant_info() -> dict:
    return {
        "id": _info["ASSISTANT_ID"],
        "username": _info["ASSISTANT_USERNAME"],
        "fullname": _info["ASSISTANT_FULL_NAME"],
        "mention": _info["ASSISTANT_MENTION"],
    }