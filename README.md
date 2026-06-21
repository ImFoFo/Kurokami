# 🎮 Kurokami - Bot Discord

Un bot Discord avec des commandes de giveaway (tirages au sort) avec conditions spécifiques.

## 🎯 Fonctionnalités

### Commande `/giveaway`
Crée un giveaway (tirage au sort) avec les conditions suivantes:

**Paramètres:**
- `duree` - Durée en secondes (ex: 60 pour 1 minute)
- `gagnants` - Nombre de gagnants
- `cadeau` - Le cadeau à gagner

**Conditions pour participer:**
- ✅ Être connecté à un salon vocal **public**
- ✅ Avoir le statut **"kurokami"** activé
- ✅ **Ne pas être muet** (micro et casque actifs)
- ❌ Pas de salons AFK
- ❌ Pas de salons privés

**Bouton "Participer":**
- Clique sur le bouton pour rejoindre
- Le compteur de participants s'affiche
- À la fin, les gagnants sont tirés au sort automatiquement

## 📦 Installation

1. Clone ce dépôt
```bash
git clone https://github.com/ImFoFo/Kurokami.git
cd Kurokami
```

2. Installe les dépendances
```bash
pip install -r requirements.txt
```

3. Obtiens ton token Discord
- Va sur [Discord Developer Portal](https://discord.com/developers/applications)
- Crée une nouvelle application
- Va dans "Bot" et clique "Add Bot"
- Copie le token

4. Ajoute ton token dans `main.py`
```python
bot.run("TON_TOKEN_ICI")  # Remplace par ton vrai token
```

5. Lance le bot
```bash
python main.py
```

## 🚀 Utilisation

```
/giveaway duree:60 gagnants:3 cadeau:Steam Gift Card
```

Cela créera un giveaway de 1 minute avec 3 gagnants!

## ⚙️ Configuration du bot Discord

1. Va sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Sélectionne ton application
3. Va dans "OAuth2 > URL Generator"
4. Sélectionne les scopes: `bot` et `applications.commands`
5. Sélectionne les permissions:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
6. Copie l'URL générée et ouvre-la pour inviter le bot sur ton serveur

## 📝 Licence

MIT

## 👤 Auteur

ImFoFo

---

**Besoin d'aide ?** Crée une issue! 🎯
