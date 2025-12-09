from AlishanBot.core.bot import Alishan, music
from AlishanBot.core.decorators import add_command
from AlishanBot.__init__ import BOT_MENTION, BOT_USERNAME, player_stats
from AlishanBot.modules.helper_funcs.uptime import get_uptime
from AlishanBot.modules.helper_funcs.ping import get_ping
from AlishanBot import config
from AlishanBot.utils.database import users, groups, sudo_users
from AlishanBot import config
from AlishanBot.modules.helper_funcs.system import get_system_stats
from AlishanBot.utils.database import greetings  
import time


@add_command("stats")
async def stats_handler(event, command, args):
    sender = await event.get_sender()
    if not sender:
        return
    if not sudo_users.find_one({"user_id": sender.id}) and sender.id != config.OWNER_ID:
        return
    start = time.time()
    msg = await event.reply("**Checking..**")
    end = time.time()
    latency = round((end - start) * 1000, 2)    
    ping = get_ping() 
    uptime = get_uptime()
    total_users = users.count_documents({})
    chats = groups.count_documents({})
    greetings_on = greetings.count_documents({})
    pytgcalls_ping = music.ping
    ram, cpu, disk = get_system_stats()
    playing = len(player_stats)
    await msg.delete()
    caption=f"<b>{BOT_MENTION}'s Stats:</b>\n<b>Py-Tgcalls:</b> {pytgcalls_ping}ms\n<b>Latency:</b> {latency}ms\n<b>Chats:</b> {chats}\n<b>Users:</b> {total_users}\n<b>Playing On:</b> {playing}\n<b>Custom Greetings:</b> {greetings_on}\n\n<b>System Stats:</b>\n<b>Server Ping:</b> {ping}\n<b>Uptime:</b> {uptime}\n<b>RAM:</b> {ram:.1f}%\n<b>CPU:</b> {cpu:.1f}%\n<b>Disk:</b> {disk:.1f}%"
    await event.reply(caption, parse_mode="html")
    