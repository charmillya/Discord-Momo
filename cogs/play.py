import nextcord
import asyncio
from nextcord.ext import commands

class cPlay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="play",
        description="I play a music of your choice!",
    )   
    async def play(
        self,
        inter: nextcord.Interaction,
        song: str = nextcord.SlashOption(
            name="song",
            description="The song you want to play!"
        ),
        ):
        user = inter.user
        if not user.voice:
            await inter.response.send_message("You need to be **in a voice channel** to use this command!")
        else:
            voice_channel = user.voice.channel
            vc = await self.bot.join_voice_channel(voice_channel)
            player = vc.create_ffmpeg_player(f'{song}')
            player.start()
            await inter.response.send_message(f"Playing {song} in {voice_channel}")
            while not player.is_done():
                await asyncio.sleep(1)
            player.stop()
            await vc.disconnect()

        
def setup(bot: commands.Bot):
    bot.add_cog(cPlay(bot))