import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Variable pour stocker les giveaways actifs
giveaways = {}

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} connecté!")
    await bot.tree.sync()
    print("✅ Commandes synchronisées!")

class ParticipateButton(discord.ui.Button):
    def __init__(self, giveaway_id):
        super().__init__(label="Participer ✨", style=discord.ButtonStyle.green)
        self.giveaway_id = giveaway_id

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        giveaway = giveaways.get(self.giveaway_id)
        
        if not giveaway:
            await interaction.response.send_message("❌ Ce giveaway n'existe plus!", ephemeral=True)
            return

        # Vérifier les conditions
        erreur = verifier_conditions(user, interaction.guild)
        
        if erreur:
            await interaction.response.send_message(f"❌ {erreur}", ephemeral=True)
            return

        # Ajouter le participant
        if user.id not in giveaway["participants"]:
            giveaway["participants"].add(user.id)
            await interaction.response.send_message(
                f"✅ Vous avez rejoint le giveaway! ({len(giveaway['participants'])} participants)",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Vous participez déjà! ({len(giveaway['participants'])} participants)",
                ephemeral=True
            )

class GiveawayView(discord.ui.View):
    def __init__(self, giveaway_id):
        super().__init__(timeout=None)
        self.add_item(ParticipateButton(giveaway_id))

def verifier_conditions(user: discord.Member, guild: discord.Guild) -> str:
    """Vérifie si l'utilisateur remplit toutes les conditions"""
    
    # Vérifier le statut /kurokami
    if user.activity is None or not any("kurokami" in str(act).lower() for act in user.activities if act):
        return "❌ Vous devez avoir le statut 'kurokami' activé!"
    
    # Vérifier si l'utilisateur est en vocal
    if user.voice is None:
        return "❌ Vous devez être connecté à un salon vocal!"
    
    # Vérifier si le salon vocal est public (pas AFK/private)
    voice_channel = user.voice.channel
    if voice_channel.category and "afk" in voice_channel.category.name.lower():
        return "❌ Vous ne pouvez pas participer depuis un salon AFK!"
    
    if voice_channel.name.lower().endswith("private") or "private" in voice_channel.name.lower():
        return "❌ Vous ne pouvez pas participer depuis un salon privé!"
    
    # Vérifier si l'utilisateur est muet (micro ou casque)
    if user.voice.self_mute or user.voice.self_deaf:
        return "❌ Vous ne pouvez pas participer si vous êtes muet ou sourdine!"
    
    return ""

@bot.tree.command(name="giveaway", description="Créer un giveaway")
@discord.app_commands.describe(
    duree="Durée en secondes (ex: 60 pour 1 minute)",
    gagnants="Nombre de gagnants",
    cadeau="Le cadeau à gagner"
)
async def giveaway(interaction: discord.Interaction, duree: int, gagnants: int, cadeau: str):
    """Crée un giveaway avec les conditions spécifiées"""
    
    # Créer l'ID du giveaway
    giveaway_id = f"{interaction.user.id}_{int(datetime.now().timestamp())}"
    
    # Initialiser les données du giveaway
    giveaways[giveaway_id] = {
        "participants": set(),
        "gagnants_count": gagnants,
        "cadeau": cadeau,
        "organisateur": interaction.user,
        "fin_time": datetime.now() + timedelta(seconds=duree)
    }
    
    # Créer l'embed
    embed = discord.Embed(
        title="🎁 GIVEAWAY 🎁",
        description=f"**Cadeau:** {cadeau}",
        color=discord.Color.gold(),
        timestamp=giveaways[giveaway_id]["fin_time"]
    )
    embed.add_field(name="👥 Participants", value="0", inline=True)
    embed.add_field(name="🏆 Gagnants", value=str(gagnants), inline=True)
    embed.add_field(name="⏱️ Fin", value=f"<t:{int(giveaways[giveaway_id]['fin_time'].timestamp())}:R>", inline=True)
    embed.set_footer(text=f"Organisé par {interaction.user.name}")
    
    # Envoyer le message avec le bouton
    view = GiveawayView(giveaway_id)
    message = await interaction.response.send_message(embed=embed, view=view)
    
    giveaways[giveaway_id]["message_id"] = message.id
    giveaways[giveaway_id]["channel_id"] = interaction.channel.id
    
    await interaction.followup.send(f"✅ Giveaway créé! Il se terminera dans {duree} secondes.", ephemeral=True)
    
    # Attendre la fin du giveaway
    await asyncio.sleep(duree)
    
    # Déterminer les gagnants
    participants = list(giveaways[giveaway_id]["participants"])
    
    if not participants:
        embed_fin = discord.Embed(
            title="🎁 GIVEAWAY TERMINÉ 🎁",
            description=f"**Cadeau:** {cadeau}\n\n❌ Pas de participant!",
            color=discord.Color.red()
        )
        channel = bot.get_channel(giveaways[giveaway_id]["channel_id"])
        await channel.send(embed=embed_fin)
    else:
        import random
        gagnants_ids = random.sample(participants, min(gagnants, len(participants)))
        gagnants_names = [f"<@{gid}>" for gid in gagnants_ids]
        
        embed_fin = discord.Embed(
            title="🎁 GIVEAWAY TERMINÉ 🎁",
            description=f"**Cadeau:** {cadeau}\n\n🏆 **Gagnants:** {', '.join(gagnants_names)}",
            color=discord.Color.green()
        )
        channel = bot.get_channel(giveaways[giveaway_id]["channel_id"])
        await channel.send(embed=embed_fin)
    
    # Nettoyer
    del giveaways[giveaway_id]

# Lancer le bot
bot.run("TON_TOKEN_ICI")