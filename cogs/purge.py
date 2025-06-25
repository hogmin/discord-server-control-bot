from discord.ext import commands

class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=2)

async def setup(bot):
    await bot.add_cog(Cleaner(bot))
