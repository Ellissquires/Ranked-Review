import discord

def intro_embed():
    embed = discord.Embed().from_dict({
        "title": "Ranked Review | Welcome! 🙃",
        "description": """You have been added to the summoner database and will now appear on the leaderboard. Each week the leaderboard will update showing the statistics for the previous ranked week. The list of commands available for this bot are listed below.

                          1️⃣ `!add_summoner`

                          2️⃣ `!remove_summoner`

                          3️⃣ `!leaderboard`

                          3️⃣ `!display_summoners`
                          """,
        "color": 16580705
    })
    footer_text = "If you experience any problems with this bot please contact, <placeholder>"
    embed.set_footer(text=footer_text)

    return embed

def leaderboard_embed(leaderboard):
    embed = discord.Embed().from_dict({
        "title": "Ranked Review | Summoners",
        "description": leaderboard,
        "color": 16580705
    })
    footer_text = "If you experience any problems with this bot please contact Ellis"
    embed.set_footer(text=footer_text)

    return embed


