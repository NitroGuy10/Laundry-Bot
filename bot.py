import discord
import config
import util

client = None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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
                "!shutdown - Shuts down the bot"
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
        
        elif message.content == '!shutdown':
            await message.channel.send('Shutting down...')
            await self.close()

async def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    print("Starting Discord bot...")

    global client
    client = MyClient(intents=intents)
    token = config.get("discord_bot_token")
    await client.start(token)
