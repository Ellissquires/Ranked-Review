import os

from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from ranked_stats import RankedStats
import helpers
import ranked_stats

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_TOKEN = os.getenv('RIOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGO_PASS = os.getenv('MONGO_PASS')
REGION = "euw1"

# mongo_url = f"mongodb+srv://test:{MONGO_PASS}@rankedreview-aphq3.mongodb.net/test"


class RankedReview(commands.Bot):

    def __init__(self, discord_token, riot_token, region, server, cpre):
        self.discord_token = discord_token
        self.server = server
        self.stat_engine = RankedStats(riot_token, region)
        super().__init__(command_prefix=cpre)

    def init(self):
        self.run(self.discord_token)

    async def on_ready(self):
        guild = get(self.guilds, name=self.server)
        print(f'{self.user} is connected to the following server:\n'
              f'{guild.name}(id: {guild.id})')

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise


bot = RankedReview(DISCORD_TOKEN, RIOT_TOKEN, REGION, GUILD, "!")
stats = ranked_stats.RankedStats(RIOT_TOKEN, REGION)

@bot.command(name="add_summoner", help="Adds a summoner to the database")
async def add_summoner(ctx, summoner_name):
    # Fetch summoner stats
    embed = helpers.intro_embed()
    await ctx.send(embed=embed)

@bot.command(name="leaderboard", help="Displays the current leaderboard")
async def add_summoner(ctx, summoner_name):
    pass

bot.init()
