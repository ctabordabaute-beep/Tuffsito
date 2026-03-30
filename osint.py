import discord
from discord.ext import commands
import aiohttp

# --- CONFIGURACIÓN ---
APP_ID = "2055"
TOKEN_API = "53f2ddae1e69c2b290b81c6fc2936217"
BOT_TOKEN = "MTQ4ODA0ODIxMTU1NjgyNzE4OA.GXRkuu.gCz8zWqqih05BXesbME2Ej4xjJ8sP1ClVL3XhM"
# ---------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    # El estado que pediste
    await bot.change_presence(activity=discord.Game(name="Base de Datos"))
    print(f"✅ {bot.user.name} activo. Sin cooldown y listo para el doxx.")

@bot.command()
async def ve(ctx, cedula: str = None):
    if not cedula:
        return await ctx.send("🤡 Pon una cédula, no soy adivino.")

    if not cedula.isdigit():
        return await ctx.send("🚫 Solo números, mardito.")

    url = f"https://api.cedula.com.ve/api/v1?app_id={APP_ID}&token={TOKEN_API}&nacionalidad=V&cedula={cedula}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                # El truco del content_type=None para que no de error 200 de JSON
                res = await response.json(content_type=None)
                
                if res.get("error") is False:
                    d = res.get("data")
                    cne = d.get("cne", {})
                    
                    embed = discord.Embed(
                        title=f"💳 Datos de: {cedula}",
                        color=0x2b2d31
                    )
                    
                    # Limpiamos los nombres para que no salgan None
                    n1 = d.get('primer_nombre') or ""
                    n2 = d.get('segundo_nombre') or ""
                    a1 = d.get('primer_apellido') or ""
                    a2 = d.get('segundo_apellido') or ""
                    nombre_full = f"{n1} {n2} {a1} {a2}".strip().upper()

                    embed.add_field(name="👤 Nombre Completo", value=nombre_full or "SIN REGISTRO", inline=False)
                    embed.add_field(name="🆔 RIF", value=d.get('rif', 'N/A'), inline=True)
                    embed.add_field(name="📍 Estado", value=cne.get('estado', 'N/A'), inline=True)
                    embed.add_field(name="🏛️ Centro Electoral", value=cne.get('centro_electoral', 'No asignado'), inline=False)
                    
                    embed.set_footer(text="Xentury DB | Consulta Libre ⚡")
                    
                    await ctx.send(embed=embed)
                else:
                    error_msg = res.get('error_str', 'Cédula no encontrada')
                    await ctx.send(f"⚠️ **API dice:** {error_msg}")
                    
        except Exception as e:
            await ctx.send(f"🧨 Error técnico: `{e}`")

# Si quieres que el bot se salga de otros servers automáticamente, avísame.
bot.run(BOT_TOKEN)

