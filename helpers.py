import discord

def intro_embed():
    embed = discord.Embed().from_dict({
        "title": "Ranked Review | Welcome! 🙃",
        "description": """You have been added to the summoner database and will now appear on the leaderboard. Each week the leaderboard will update showing the statistics for the previous ranked week. The list of commands available for this bot are listed below.

                          1️⃣ `!add_summoner`

                          2️⃣ `!leaderboard`

                          3️⃣ `!remove_summoner`
                          """,
        "color": 16580705
    })
    footer_text = "If you experience any problems with this bot please contact, <placeholder>"
    embed.set_footer(text=footer_text)

    return embed

