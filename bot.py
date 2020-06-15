from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from ranked_stats import RankedStats
from pymongo import MongoClient
from tabulate import tabulate

import helpers
import os

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RIOT_TOKEN = os.getenv('RIOT_TOKEN')
MONGO_PASS = os.getenv('MONGO_PASS')


class RankedReview(commands.Bot):

    def __init__(self, discord_token, riot_token, guild, cpre):
        self.discord_token = discord_token
        self.guild = guild
        self.connection_url = f"mongodb+srv://test:{MONGO_PASS}@rankedreview-aphq3.mongodb.net/test"
        self.stat_engine = RankedStats(riot_token, "euw1")
        super().__init__(command_prefix=cpre)

    def init(self):
        cluster = MongoClient(self.connection_url)
        db = cluster["RankedReview"]
        self.ranked_collection = db["SummonerRankedData"]
        self.run(self.discord_token)

    async def on_ready(self):
        guild = get(self.guilds, name=self.guild)
        print(f'{self.user} is connected to the following server:\n'
              f'{guild.name}(id: {guild.id})')

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

    async def save_summoner(self, ctx, summoner_name):
        ranked_stats = self.stat_engine.fetch_ranked_stats(summoner_name)
        print(ranked_stats)
        solo_stats = next(q for q in ranked_stats if q["queueType"] == "RANKED_SOLO_5x5")

        if self.ranked_collection.find_one({"Summoner": solo_stats["summonerName"]}):
            await ctx.send("Summoner already added, you can view the leaderboard with the command `!leaderboard`")
        else:
            summoner_ranked_record = {
                "Summoner": solo_stats["summonerName"],
                "Rank": solo_stats["tier"] + " " + solo_stats["rank"],
                "LP": solo_stats["leaguePoints"],
                "Wins": solo_stats["wins"],
                "Losses": solo_stats["losses"]
            }
            self.ranked_collection.insert_one(summoner_ranked_record)
            print(f"Creating summoner record for {summoner_name}")
            embed = helpers.intro_embed()
            await ctx.send(embed=embed)

    async def delete_summoner(self, ctx, summoner_name):
        self.ranked_collection.delete_many({"Summoner": summoner_name})
        await ctx.send(f"{summoner_name} has been removed.")

    async def display_summoners(self, ctx):
        data = list(self.ranked_collection.find({}, {'_id': 0}))

        if not data:
            await ctx.send("No summoners to display, you can add one with the `!add_summoner <summoner>` command")
            return

        header = data[0].keys()
        rows = [x.values() for x in data]
        table = tabulate(rows, header, tablefmt="simple")
        leaderboard = f"```{table}```"
        embed = helpers.leaderboard_embed(leaderboard)
        await ctx.send(embed=embed)


bot = RankedReview(DISCORD_TOKEN, RIOT_TOKEN, GUILD, "!")

@bot.command(name="add_summoner", help="Adds a summoner to the database")
async def add_summoner(ctx, summoner_name):
    await bot.save_summoner(ctx, summoner_name)

@bot.command(name="remove_summoner", help="Removes a summoner from the database")
async def remove_summoner(ctx, summoner_name):
    await bot.delete_summoner(ctx, summoner_name)

@bot.command(name="leaderboard", help="Displays the current leaderboard")
async def leaderboard(ctx, summoner_name):
    pass

@bot.command(name="display_summoners", help="Displays the summoners currently saved")
async def display_summoners(ctx):
    await bot.display_summoners(ctx)

bot.init()
