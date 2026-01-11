import discord
import config
import util
import asyncio
import gpio

client = None

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polling_task = None
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Start the GPIO polling task
        if self.polling_task is None:
            self.polling_task = self.loop.create_task(gpio.poll_washer_pin(self))
            print('Started GPIO polling task')
    
    async def washer_done_notification(self):
        if config.get("silenced") == "false":
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name == "laundry":
                        await channel.send("Your laundry is done! 🧺✅")
                        return

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        if message.content == '!help':
            help_text = (
                "```"
                "Available commands:\n"
                "!ping - Responds with 'Pong!'\n"
                "!ip - Responds with the server's IP addresses (ifconfig output)\n"
                "!site - Provides the URL to access the web server\n"
                "!silence - Stop notifying on washer completion\n"
                "!unsilence - Resume notifying on washer completion\n"
                "!set_finished_timeout <seconds> - Set the finished timeout duration\n"
                "!shutdown - Shuts down the bot\n"
                "```"
            )
            await message.channel.send(help_text)

        
        if message.content == '!ping':
            await message.channel.send('Pong!')
        
        if message.content == '!ip':
            chunks = util.split_for_discord(f"Hostname: {util.get_hostname()}\n\n{util.get_ifconfig_output()}", True)
            for chunk in chunks:
                await message.channel.send(chunk)
        
        if message.content == "!site":
            await message.channel.send(f"http://{util.get_hostname()}:{config.get('port')}/")
        
        if message.content == "!silence":
            config.set("silenced", "true")
            await message.channel.send("Notifications silenced.")

        if message.content == "!unsilence":
            config.set("silenced", "false")
            await message.channel.send("Notifications unsilenced.")
        
        if message.content.startswith("!set_finished_timeout"):
            parts = message.content.split()
            if len(parts) == 2 and parts[1].isdigit():
                timeout_seconds = parts[1]
                try:
                    int(timeout_seconds)  # Ensure it's a valid integer
                    config.set("finished_timeout_seconds", timeout_seconds)
                    await message.channel.send(f"\"Finished\" timeout set to {timeout_seconds} seconds.")
                except ValueError:
                    await message.channel.send("Please provide a valid number of seconds.")
            else:
                await message.channel.send("Usage: !set_finished_timeout <seconds>")
    
        if message.content == '!shutdown':
            await message.channel.send('Shutting down...')
            await self.close()
    
    async def close(self):
        # Cancel the polling task before closing
        if self.polling_task is not None:
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                print('GPIO polling task cancelled')
        await super().close()

async def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    print("Starting Discord bot...")

    global client
    client = MyClient(intents=intents)
    token = config.get("discord_bot_token")

    await client.start(token)
