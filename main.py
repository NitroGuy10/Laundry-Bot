import config
import bot
import server

import asyncio
import multiprocessing

async def main():
    if not config.load_config():
        exit(1)
    
    # Start bot and server concurrently
    bot_task = asyncio.create_task(bot.start_bot())
    server_process = multiprocessing.Process(target=server.start_server)
    server_process.start()

    # Wait for the shutdown command from the bot
    await bot_task
    print("Bot has shut down.\nClosing server...")
    server_process.terminate()
    server_process.join()
    print("Server closed.\nWaiting a few seconds before exit...")
    await asyncio.sleep(3)  # The bot needs a moment to close properly
    print("All done!")

if __name__ == "__main__":
    asyncio.run(main())
