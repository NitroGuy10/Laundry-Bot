import config
import bot
import server

import asyncio

async def main():
    if not config.load_config():
        exit(1)
    
    bot_task = asyncio.create_task(bot.start_bot())
    server_task = asyncio.create_task(server.start_server())

    await bot_task
    await asyncio.sleep(3)  # Let the bot shut down gracefully
    server_task.cancel()

    print("Exiting...")

if __name__ == "__main__":
    asyncio.run(main())
