import discord
import responses
import settings
import datetime


async def send_message (message, user_message):
    try:
        response = responses.get_response(user_message)
        await message.channel.send(response)
    
    except Exception as e:
        print(e)

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        pozdrav = 'Yay online sam, vreme ukljucenja: ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        await client.get_channel(int(settings.hodnik)).send(pozdrav)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content).lower()
        channel = str(message.channel) ### ako se poruka pise na drugom kanalu
        general_channel = client.get_channel(settings.hodnik)

        if user_message == 'bot_version':
            myEmbed = discord.Embed(title = 'Trenutna verzija', description = 'Trenutna verzija bota je v1.3', color=0x95eb34 )
            myEmbed.add_field(name='Verzija:', value ='v1.3')
            myEmbed.add_field(name='Datum zadnjeg update:',value='30.11.2023. godine')
            myEmbed.set_footer(text='Uskoro nove stvari! Stay tuned!')
            myEmbed.set_author(name='Bole')
            await client.get_channel(int(settings.hodnik)).send(embed=myEmbed) 

        elif user_message == 'cls':
            await message.delete()
        else:
            await send_message(message, user_message)

    client.run(settings.token)
