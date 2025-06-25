from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_map = {}

    @commands.command(name='rr',
                      help='Create reaction roles for the current channel.')
    @commands.has_permissions(manage_roles=True)
    async def create_reaction_roles(self, ctx, *, message_text):
        author_top_role = ctx.author.top_role
        print(author_top_role)
        roles = [
            r for r in ctx.guild.roles
            if author_top_role.position > r.position > 2
        ]

        print(roles)
        roles = sorted(roles, key=lambda r: r.position, reverse=True)
        if not roles:
            await ctx.send("No available roles found.")
            return

        msg = await ctx.send(message_text)
        self.emoji_map[msg.id] = {}

        for i, role in enumerate(roles):
            emoji = f"{i + 1}\u20e3"
            self.emoji_map[msg.id][emoji] = role
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id not in self.emoji_map:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            return
        emoji = str(payload.emoji)
        role = self.emoji_map[payload.message_id].get(emoji)
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id not in self.emoji_map:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)
        role = self.emoji_map[payload.message_id].get(emoji)
        if role:
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
