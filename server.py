import random
from datetime import datetime
import modal
import creds


def gen_card_urls():
    url = "https://ssimeonoff.github.io/cards-list"
    preludes = [f"P0{i+1}" if i < 9 else f"P{i+1}" for i in range(35)]

    cards = [
        f"{i+1}" if i >= 99 else f"0{i+1}" if i >= 9 else f"00{i+1}"
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

    venus_corps = {
        "CORP13": "Aphrodite",
        "CORP14": "Celestic",
        "CORP15": "Manutech",
        "CORP16": "Morning Star Inc.",
        "CORP17": "Viron"
    }

    merged_corps = {**corps, **venus_corps}

    prelude_cards = ["P36", "P37", "P38", "P39", "P40", "P41", "P42"]

    venus_cards = [
        f"{i}" for i in range(213, 262)
    ]

    final_cards = cards + prelude_cards

    choices = (
        random.sample(list(corps), 2)
        + random.sample(preludes, 4)
        + random.sample(final_cards, 10)
    )

    venus_choices = (
        random.sample(list(merged_corps), 2)
        + random.sample(preludes, 4)
        + random.sample(final_cards + venus_cards, 10)
    )

    final_url = f'{url}#{"#".join(choices)}'
    venus_url = f'{url}#{"#".join(venus_choices)}'

    return {
        'base': final_url,
        'venus': venus_url,
        'base_corps': list(
            map(lambda x: corps.get(x), [x for x in choices if x.startswith("CORP")])
        ),
        'venus_corps': list(
            map(lambda x: merged_corps.get(x), [x for x in venus_choices if x.startswith("CORP")])
        )
    }

discord_image = modal.Image.debian_slim().pip_install("discord")
stub = modal.Stub("tm-hand-bot")


@stub.function(schedule=modal.Cron("0 15 * * *"), image=discord_image)
def run_bot():
    import discord

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        base_channel = client.get_channel(creds.BASE_CHANNEL)
        venus_channel = client.get_channel(creds.VENUS_CHANNEL)
        
        data = gen_card_urls()

        board = random.sample(["Tharsis", "Elysium", "Hellas"], 1)
        order = random.sample(["first", "second"], 1)
        

        base_message = f'{data["venus"]}: {data["venus_corps"][1]} vs. {data["venus_corps"][0]} on {board[0]}, going {order[0]}'
        venus_message = print(f'{data["base"]}: {data["base_corps"][1]} vs. {data["base_corps"][0]} on {board[0]}, going {order[0]}')

        await base_channel.create_thread(
            name=base_message,
            content=data["base"]
        )

        await venus_channel.create_thread(
            name=venus_message,
            content=data["venus"]
        )        

    client.run(creds.DISCORD_TOKEN)


if __name__ == "__main__":
    stub.deploy("tm-hand-bot")
    
