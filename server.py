import modal
import random
from datetime import datetime
import creds

discord_image = modal.Image.debian_slim().pip_install("discord")
stub = modal.Stub()

@stub.function(schedule=modal.Cron('0 15 * * *'), image=discord_image)
def run_bot():
    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    print(f'client initiated: {client}')

    @client.event
    async def on_ready():
        channel = client.get_channel(creds.FORUM_CHANNEL)
        print(f'channel found: {channel}')

        url = "https://ssimeonoff.github.io/cards-list"
        preludes = [
            f'P0{i+1}' if i < 9 else
            f'P{i+1}' for i in range(35)
        ]

        cards = [
            f'{i+1}' if i >= 99 else
            f'0{i+1}' if i >= 9 else
            f'00{i+1}'
            for i in range(208)
        ]

        corps = {
            "CORP01": "Credicor",
            "CORP02": "Ecoline",
            "CORP03": "Helion",
            "CORP04": "Mining Guild",
            "CORP05": "IC",
            "CORP06": "Inventrix",
            "CORP07": "Phobolog",
            "CORP08": "Tharsis",
            "CORP09": "Thorgate",
            "CORP10": "UNMI",
            "CORP11": "Teractor",
            "CORP12": "Saturn",
            "CORP18": "Cheung Shing",
            "CORP19": "Point Luna",
            "CORP20": "Robinson",
            "CORP21": "Valley Trust",
            "CORP22": "Vitor",
        }

        prelude_cards = ["P36", "P37", "P38", "P39", "P40", "P41", "P42"]

        final_cards = cards + prelude_cards

        choices = random.sample(list(corps), 2) + random.sample(preludes, 4) + random.sample(final_cards, 10)

        chosen_corps = list(map(
            lambda x: corps.get(x),
            [x for x in choices if x.startswith("CORP")]
        ))
        
        final_url = f'{url}#{"#".join(choices)}'

        _, message = await channel.create_thread(
            name=f'{datetime.now().strftime("%B %d, %Y")}: {chosen_corps[1]} vs. {chosen_corps[0]}',
            content=f"""{final_url}

Rate this hand with the emojis below!"""
        )

        print(f'message created: ${message}')

        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')
        await message.add_reaction('3️⃣')
        await message.add_reaction('4️⃣')
        await message.add_reaction('5️⃣')
        await message.add_reaction('6️⃣')
        await message.add_reaction('7️⃣')
        await message.add_reaction('8️⃣')
        await message.add_reaction('9️⃣')
        await message.add_reaction('0️⃣')

    client.run(creds.DISCORD_TOKEN)

if __name__ == "__main__":
    stub.deploy("tm-hand-bot")

# run_bot()