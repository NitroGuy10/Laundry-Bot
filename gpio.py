
import random
import asyncio

import bot


def get_washer_pin_status() -> bool:
    return random.choice([True, False])


async def poll_washer_pin(client) -> None:
    seconds_low = 0
    running = False

    while True:
        pin_status = get_washer_pin_status()
        if pin_status == True:
            running = True
            seconds_low = 0
        else:
            if running == True:
                seconds_low += 1
                if seconds_low >= int(bot.config.get("finished_timeout_seconds")):
                    await client.washer_done_notification()
                    running = False
                    seconds_low = 0
        
        print(f"Washer pin status: {pin_status}")
        print(f"Seconds low: {seconds_low}")
        await asyncio.sleep(1)  # Poll every second
