import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0"))
AUTO_ROLE_ID = int(os.getenv("AUTO_ROLE_ID", "0"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Бот {bot.user} успешно запущен и готов к работе!")


@bot.event
async def on_member_join(member: discord.Member):
    if AUTO_ROLE_ID:
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            try:
                await member.add_roles(role, reason="Автовыдача роли при входе")
            except discord.Forbidden:
                print(f"Недостаточно прав для выдачи роли {AUTO_ROLE_ID} пользователю {member}")
            except discord.HTTPException as e:
                print(f"Ошибка Discord API при выдаче роли: {e}")

    if WELCOME_CHANNEL_ID:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            try:
                embed = discord.Embed(
                    title="Добро пожаловать на сервер! 🎉",
                    description=f"Привет, {member.mention}! Мы рады видеть тебя на **{member.guild.name}**.",
                    color=discord.Color.green()
                )
                if member.avatar:
                    embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text=f"Теперь нас {member.guild.member_count} участников!")
                await channel.send(embed=embed)
            except Exception as e:
                print(f"Ошибка при отправке приветствия: {e}")


if not TOKEN:
    raise RuntimeError("Не задан токен бота в переменных окружения (DISCORD_TOKEN или BOT_TOKEN)!")

bot.run(TOKEN)
