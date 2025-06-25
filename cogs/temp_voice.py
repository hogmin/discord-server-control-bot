from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

class TemporaryVC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}
        self.cleanup_task.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.name.lower() == "join to create":
            guild = after.channel.guild
            category = await guild.create_category(f"{member.name}'s category")
            vc = await category.create_voice_channel(f"{member.name} channel")
            self.active_channels[vc.id] = {
                "channel": vc,
                "category": category,
                "last_active": datetime.now(timezone.utc)
            }
            await member.move_to(vc)

        # Handle leaving a temp VC
        if before.channel and before.channel.id in self.active_channels:
            if len(before.channel.members) == 0:
                self.active_channels[before.channel.id]["last_active"] = datetime.now(timezone.utc)

    @tasks.loop(seconds=10)
    async def cleanup_task(self):
        now = datetime.now(timezone.utc)
        to_delete = []
        print(now, to_delete)
        for vc_id, info in self.active_channels.items():
            vc = info["channel"]
            if len(vc.members) == 0 and now - info["last_active"] > timedelta(seconds=30):
                to_delete.append(vc_id)
        for vc_id in to_delete:
            info = self.active_channels.pop(vc_id)
            await info["channel"].delete()
            await info["category"].delete()

async def setup(bot):
    await bot.add_cog(TemporaryVC(bot))
