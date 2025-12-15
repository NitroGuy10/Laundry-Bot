import discord
import config

client = None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        if message.content == '!ping':
            await message.channel.send('Pong!')
        
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
