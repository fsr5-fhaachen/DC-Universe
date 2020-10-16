import discord
import os
import typing

from discord.ext import commands


class ManualGroups( commands.Cog, name='ManualGroups' ):
    def __init__(self, bot): 
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.guild_command_channel_id = os.getenv(
            'GUILD_COMMAND_CHANNEL' 
        )
        if isinstance( self.guild_command_channel_id, str ) :
            self.guild_command_channel_id = int(
                self.guild_command_channel_id 
            )
        
        self.guild_roles_channel_id = os.getenv(
            'GUILD_ROLES_CHANNEL' 
        )
        if isinstance( self.guild_roles_channel_id, str ) :
            self.guild_roles_channel_id = int(
                self.guild_roles_channel_id 
            )
        
        self.guild_announcement_channel_id = os.getenv(
            'GUILD_ANNOUNCEMENTS_CHANNEL'
        )
        if isinstance( self.guild_announcement_channel_id, str ) :
            self.guild_announcement_channel_id = int(
                self.guild_announcement_channel_id
            )

        self.guild_inf_role_id = os.getenv(
            'GUILD_INF_ROLE' 
        )
        if isinstance( self.guild_inf_role_id, str ) :
            self.guild_inf_role_id = int(
                self.guild_inf_role_id 
            )

        self.guild_wi_role_id = os.getenv(
            'GUILD_WI_ROLE' 
        )
        if isinstance( self.guild_wi_role_id, str ) :
            self.guild_wi_role_id = int(
                self.guild_wi_role_id 
            )

        self.guild_et_role_id = os.getenv(
            'GUILD_ET_ROLE' 
        )
        if isinstance( self.guild_et_role_id, str ) :
            self.guild_et_role_id = int(
                self.guild_et_role_id 
            )

        self.guild_mcd_role_id = os.getenv(
            'GUILD_MCD_ROLE' 
        )
        if isinstance( self.guild_mcd_role_id, str ) :
            self.guild_mcd_role_id = int(
                self.guild_mcd_role_id
            )
        
        self.guild_command_message_id = 0


    @commands.command(aliases=['studiengang', 'sg'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def studyProgram(self, ctx, active: typing.Optional[str]):
        if active:
            active = active.lower()

        # in general we does not care whether a message was already send or not

        # post message with content
        if active == 'start':
            if self.guild_command_message_id > 0:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es existiert bereits eine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
                return

            if self.guild_announcement_channel_id > 0 :
                guild_announcement_channel = self.bot.get_channel(
                    self.guild_announcement_channel_id
                )

                if guild_announcement_channel :
                    announcement_message = await guild_announcement_channel.send(
                        'Hallo @everyone,\n' + 
                        'Ab sofort könnt ihr euch eurem Studiengang zuordnen! Dies passiert indem du auf diese Nachricht reagierst.\n' +
                        'Die entsprechenden Buchstaben sind wie folgt zu verstehen:\n' +
                        ':regional_indicator_i: - INF\n' +
                        ':regional_indicator_w: - WI\n' +
                        ':regional_indicator_e: - ET\n' +
                        ':regional_indicator_m: - MCD' 
                    )
                    await announcement_message.add_reaction('🇮')
                    await announcement_message.add_reaction('🇼')
                    await announcement_message.add_reaction('🇪')
                    await announcement_message.add_reaction('🇲')
                    if announcement_message:
                        self.guild_command_message_id = guild_announcement_channel.last_message_id

        if active == 'stopp':
            if self.guild_command_message_id == 0:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es existiert keine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
            
            else :
                channel = self.bot.get_channel( self.guild_announcement_channel_id )
                msg = await channel.fetch_message( self.guild_command_message_id )
                await msg.delete()


    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return
        
        guild_announcement_channel = self.bot.get_channel(
            self.guild_announcement_channel_id
        )
        # await guild_announcement_channel.send('Soweit so gut')

        if self.guild_command_message_id > 0 and self.guild_command_message_id == payload.message_id:
            role = 0

            if payload.emoji.name == '🇮':
                role = self.guild_inf_role_id

            elif payload.emoji.name == '🇼':
                role = self.guild_wi_role_id

            elif payload.emoji.name == '🇪':
                role = self.guild_et_role_id

            elif payload.emoji.name == '🇲':
                role = self.guild_mcd_role_id

            else:
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                user = discord.Member
                user.id = payload.user_id
                await message.remove_reaction(payload.emoji, user)
                return

            if role > 0:
                userId = payload.user_id
                userDiscord = self.bot.get_guild.get_member(userId)
                await userDiscord.add_roles( role )
            else:
                channel = self.bot.get_channel(payload.channel_id)
                user = await self.bot.fetch_user(payload.user_id)
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = f'Etwas ist schief gelaufen.'
                )
                await channel.send ( user.mention, embed=embed )

def setup( bot ):
    bot.add_cog( ManualGroups( bot ) )
