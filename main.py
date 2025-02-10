# main.py

import discord
from discord.ext import commands
from discord_slash import SlashCommand
import os

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Ticketing command to create a new ticket
@slash.slash(name="create_ticket", description="Create a new support ticket")
async def create_ticket(ctx):
    guild = ctx.guild
    channel = await guild.create_text_channel(f'ticket-{ctx.author.name}')
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await channel.set_permissions(guild.default_role, read_messages=False)
    await channel.send(f"Hello {ctx.author.mention}, please describe your issue. A staff member will be with you shortly.")

# Close the ticket
@slash.slash(name="close_ticket", description="Close your support ticket")
async def close_ticket(ctx):
    ticket_channel = ctx.channel
    if ticket_channel.name.startswith("ticket-"):
        await ticket_channel.delete()
        await ctx.send("Your ticket has been closed.")
    else:
        await ctx.send("This command can only be used in ticket channels.")

# Add a staff member to the ticket
@slash.slash(name="add_staff", description="Add a staff member to the ticket")
async def add_staff(ctx, member: discord.Member):
    ticket_channel = ctx.channel
    if ticket_channel.name.startswith("ticket-"):
        await ticket_channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"Added {member.mention} to the ticket.")
    else:
        await ctx.send("This command can only be used in ticket channels.")

# Remove a staff member from the ticket
@slash.slash(name="remove_staff", description="Remove a staff member from the ticket")
async def remove_staff(ctx, member: discord.Member):
    ticket_channel = ctx.channel
    if ticket_channel.name.startswith("ticket-"):
        await ticket_channel.set_permissions(member, read_messages=False, send_messages=False)
        await ctx.send(f"Removed {member.mention} from the ticket.")
    else:
        await ctx.send("This command can only be used in ticket channels.")

# Respond to ticket (for staff)
@slash.slash(name="respond_ticket", description="Respond to the ticket")
async def respond_ticket(ctx, message: str):
    ticket_channel = ctx.channel
    if ticket_channel.name.startswith("ticket-"):
        await ticket_channel.send(f"Staff: {message}")
        await ctx.send("Your response has been sent to the ticket.")
    else:
        await ctx.send("This command can only be used in ticket channels.")

# Reopen a closed ticket
@slash.slash(name="reopen_ticket", description="Reopen a closed ticket")
async def reopen_ticket(ctx):
    guild = ctx.guild
    ticket_channel = await guild.create_text_channel(f'ticket-{ctx.author.name}')
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    await ticket_channel.send(f"Hello {ctx.author.mention}, your ticket has been reopened. Please describe your issue.")

# Start the bot
bot.run('YOUR_BOT_TOKEN')
