import asyncio

async def start_server():
    while True:
        print("Server is running...")
        await asyncio.sleep(2)  # Simulate server activity

