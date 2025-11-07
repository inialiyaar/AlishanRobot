import time
from AlishanBot.__init__ import start_time

def get_uptime():
    current_time = time.time()
    seconds = current_time - start_time
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4 and seconds > 0:
        seconds, result = divmod(seconds, 60 if count < 2 else 24)
        time_list.append(f"{int(result)}{time_suffix_list[count]}")
        count += 1

    return ":".join(reversed(time_list))