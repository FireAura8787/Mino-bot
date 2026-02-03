from flask import Flask
from threading import Thread
import discord
from discord import app_commands
from discord.ext import commands
import os

# 1. Mini site pour Render (pour pas que le bot s'endorme)
app = Flask('')
@app.route('/')
def home():
    return "Mino est en vie !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Setup du Bot
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronise les commandes slash (/)
        await self.tree.sync()
        print(f"Commandes slash synchronisées pour {self.user}")

bot = MyBot()

# --- COMMANDES SLASH ---

@bot.tree.command(name="config", description="Configurer le serveur")
@app_commands.describe(nom_du_serv="Change le nom de la config", salon_bienvenue="ID du salon de bienvenue")
async def config(interaction: discord.Interaction, nom_du_serv: str, salon_bienvenue: str):
    await interaction.response.send_message(f"✅ Config mise à jour !\n**Nom :** {nom_du_serv}\n**Salon :** {salon_bienvenue}", ephemeral=True)

@bot.tree.command(name="cv", description="Prendre des nouvelles de Mino")
async def cv_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Cv mon pote, ett toi ?")

# --- LANCEMENT SECURISE ---
if __name__ == "__main__":
    keep_alive()
    # On récupère le token caché dans les paramètres de Render
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Erreur : Le DISCORD_TOKEN n'est pas configuré dans Render !")
