from random import choice, randint
from typing import Optional
from aiohttp import request

from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, BadArgument, cooldown, BucketType
from discord.utils import get

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"], brief="Say Hi to Doob!")
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll", "rolldice"], brief="Roll some dice!")
    @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 40:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in  rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("Please roll a lower number of dice.", delete_after=10)

    @command(name="slap", brief="Slap a user, what did they do wrong to you?")
    @cooldown(1, 10, BucketType.user)
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}!")
        await ctx.send("Ouch!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("That user could not be found. :/", delete_after=10)

# Make Echo Patreon only, because I don't wanna make my bot just say anything. (which is why the print statement says who said it and what, but just as an extra safe measure [and a benefit for the people who give me money] this is going to be Patreon only.)
    @command(name="echo", aliases=["say"], brief="Make Doob say something!")
    @cooldown(1, 10, BucketType.user)
    async def echo_message(self, ctx, *, message):
        homeGuild = self.bot.get_guild(702352937980133386)
        patreonRole = get(homeGuild.roles, id=757041749716893739)  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if patreonRole in member.roles:
            await ctx.send(message)
            print(f"{ctx.author.name} used the Echo command and said {message}")
        else:
            await ctx.send("You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev>.")

    @command(name="fact", aliases=["dogfact", "facts"], brief="Learn a random fact about dogs!")
    @cooldown(3, 10, BucketType.user)
    async def dog_fact(self, ctx):
        URL = "https://some-random-api.ml/facts/dog"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title="Dog Fact!", description=data["fact"], colour=ctx.author.colour)
                embed.set_footer(text=f"{ctx.author} requested this fact!", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Dog fact API sent a {response.status} status.")

    @command(name="dog", aliases=["dogimage"], brief="See a random picture of a dog!")
    @cooldown(8, 10, BucketType.user)
    async def dog_image(self, ctx):
        URL = "https://some-random-api.ml/img/dog"

        random = randint(1,103)

        if random != 100 and random != 101 and random != 102:
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title="Dog Picture!", colour=ctx.author.colour)
                    embed.set_footer(text=f"{ctx.author} requested this picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url=data["link"])
                    await ctx.send(embed=embed)

        elif random == 100:
            embed = Embed(title="Lucky Dog Picture!", description="This is [Liquid Mendo](https://twitter.com/mendo)'s dog Koda!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 100 chance of getting this picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360")
            await ctx.send(embed=embed)

        elif random == 101:
            embed = Embed(title="Lucky Dog Picture!", description="There is a 1 in 100 chance of getting this picture!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url = "https://i.imgur.com/pzqRLdi.jpg")
            await ctx.send(embed=embed)

        elif random == 102:
            embed = Embed(title="Lucky Dog Picture!", description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 100 chance of getting this picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
            await ctx.send(embed=embed)

    @command(name="notanimposter", aliases=["nai", "amonguscrew", "crewmate"], brief="I SWEAR I SAW HIM VENT! He wasn't an imposter...")
    @cooldown(1, 4, BucketType.user)
    async def not_an_imposter(self, ctx, *, target: Optional[str]):
        target = target or ctx.author

        await ctx.send(f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was not An Impostor.　 。　.\n\n　　'　　　 1 Impostor remains 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 .")


    @command(name="animposter", aliases=["ai", "amongusimposter", "imposter"], brief="I SWEAR I SAW HIM VENT! He was an imposter. I knew it!!!")
    @cooldown(1, 4, BucketType.user)
    async def an_imposter(self, ctx, *, target: Optional[str]):
        target = target or ctx.author

        await ctx.send(f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was An Impostor.　 。　.\n\n　　'　　　 0 Impostor remains 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 .")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
