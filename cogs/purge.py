from discord.ext import commands
import asyncio

class Cleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        messages = []
        async for message in ctx.channel.history(limit=amount + 1):
            if (ctx.channel.permissions_for(ctx.guild.me).manage_messages
                and not message.pinned):
                messages.append(message)

        messages_to_delete = messages[1:]

        if len(messages_to_delete) < amount:
            prompt = await ctx.send(f"Found only {len(messages_to_delete)} messages. Proceed with deletion? (y/n)",
                                    delete_after=10)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["y", "n"]

            try:
                reply = await self.bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await prompt.edit(content="Timed out. No messages deleted.", delete_after=5)
                return

            if reply.content.lower() != "y":
                await prompt.edit(content="Deletion cancelled.", delete_after=5)
                await reply.delete(delay=5)
                await prompt.delete(delay=5)
                return

        await ctx.channel.delete_messages(messages_to_delete)
        confirmation = await ctx.send(f"Deleted {len(messages_to_delete)} messages.", delete_after=3)

async def setup(bot):
    await bot.add_cog(Cleaner(bot))