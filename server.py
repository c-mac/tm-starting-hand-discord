import random
import modal
import creds


def gen_card_urls(format: str):
    url = "https://ssimeonoff.github.io/cards-list"
    preludes = [f"P0{i + 1}" if i < 9 else f"P{i + 1}" for i in range(35)]

    cards = [
        f"{i + 1}" if i >= 99 else f"0{i + 1}" if i >= 9 else f"00{i + 1}"
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
        "CORP17": "Viron",
    }

    promo_corps = {
        "CORP36": "Arcadian Communities",
        "CORP37": "Recyclon",
        "CORP38": "Splice",
        "CORP39": "Astrodrill",
        "CORP40": "Pharmacy Union",
    }

    colonies_corps = {
        "CORP23": "Aridor",
        "CORP24": "Arklight",
        "CORP25": "Polyphemos",
        "CORP26": "Poseidon",
        "CORP27": "Storm Craft",
    }

    final_corps = corps

    prelude_cards = ["P36", "P37", "P38", "P39", "P40", "P41", "P42"]

    venus_cards = [f"{i}" for i in range(213, 262)]

    # X14 - X30 (31,32,33 are replacements of base cards)
    promo_cards = ["209", "210", "211", "212", *[f"X{i}" for i in range(14, 31)]]

    colonies_cards = [f"C{i}" if i > 9 else f"C0{i}" for i in range(50)]

    colonies = [
        "EUROPA",
        "TRITON",
        "CALLISTO",
        "CERES",
        "ENCELADUS",
        "TITAN",
        "MIRANDA",
        "GANYMEDE",
        "LUNA",
        "IO",
        "PLUTO",
    ]

    final_cards = cards + prelude_cards
    corp_choices = 2
    if format == "BPVC":
        # Remove deimos, mag field generators, and great dam -- replace with their promo equivalents below
        cards.remove("039")
        cards.remove("165")
        cards.remove("136")
        promo_cards += ["X31", "X32", "X33"]
        final_cards += promo_cards + colonies_cards + venus_cards
        final_corps = {**corps, **venus_corps, **promo_corps, **colonies_corps}

    choices = (
        random.sample(list(final_corps), corp_choices)
        + random.sample(preludes, 4)
        + random.sample(final_cards, 10)
    )

    if format == "BPVC":
        choices += random.sample(colonies, 5)

    final_url = f"{url}#{'#'.join(choices)}"

    return {
        "url": final_url,
        "corps": list(
            map(
                lambda x: final_corps.get(x),
                [x for x in choices if x.startswith("CORP")],
            )
        ),
    }


discord_image = modal.Image.debian_slim().pip_install("discord")
app = modal.App("tm-hand-bot")


@app.function(schedule=modal.Cron("0 15 * * *"), image=discord_image)
def run_bot():
    import discord

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        base_channel = client.get_channel(creds.BASE_CHANNEL)

        format = random.choice(["BP", "BPVC"])

        data = gen_card_urls(format)

        board = random.sample(["Tharsis", "Elysium", "Hellas"], 1)
        order = random.sample(["first", "second"], 1)

        base_message = f"{format}: {data['corps'][1]} vs. {data['corps'][0]} on {board[0]}, going {order[0]}"

        await base_channel.create_thread(name=base_message, content=data["url"])

    client.run(creds.DISCORD_TOKEN)


if __name__ == "__main__":
    app.deploy("tm-hand-bot")
    # format = random.choice(["BP", "BPVC"])
    # data = gen_card_urls(format)
    # print(data["url"])
