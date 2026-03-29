import telebot
import json
import os
from langdetect import detect

# ================== CONFIGURACIÓN ==================
TOKEN = "8524030812:AAH-AZHw08ExviYynse2k4xhgGbN5PbFkj8"
ADMIN_ID = 965059504

bot = telebot.TeleBot(TOKEN)

BLOCKED_FILE = "blocked_users.json"
RESPONSES_FILE = "responses.json"

def load_blocked():
if os.path.exists(BLOCKED_FILE):
with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
return set(json.load(f))
return set()

def save_blocked(blocked_set):
with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
json.dump(list(blocked_set), f)

def load_responses():
if os.path.exists(RESPONSES_FILE):
with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
return json.load(f)
# Respuestas iniciales (tus 6 originales + las 2 que confirmaste, en ES e inglés)
return {
"hola cómo estás?": "hola amor😘",
"cómo estás?": "bien y tu? ♥️",
"me puedes dar info?": "tengo videos de todo tipo a la venta y en la subscripción de mi onlyfans, podemos hacer sexting y esas cositas… aquí tienes mis links si quieres mirar 😍 linktr.ee/lizrainbow",
"quiero info por favor?": "amor mira mis links ahí puedes encontrar todo de mi linktr.ee/lizrainbow",
"eres guapa?": "♥️♥️♥️",
"quiero comprar algo?": "amor aquí tienes mis tiendas y otras cositas que te encantarán lizrainbow.manyvids.com",
"me puedes mandar fotos?": "amor mis fotos hot y desnudas desde 50€ están hechas para que las mires una y otra vez y te pongas durísimo pensando en mí 😘 quiero que seas tú quien tenga lo más rico y privado… ¿quieres un pack especial o fotos custom solo para ti? dime qué te gusta y te mando lo que más te excite 🔥 linktr.ee/lizrainbow",
"tienes onlyfans?": "en onlyfans tienes todo mi contenido exclusivo amor 😘 pero si quieres algo más directo y personal te ofrezco los precios especiales porque quiero que seas tú quien me tenga: videos y fotos desde 50€, sexting desde 60€ 💦 también puedo hacerte custom videos solo para ti 😈 ¿quieres entrar o prefieres comprar directo conmigo ahora para que sea más íntimo y caliente? linktr.ee/lizrainbow",

"hello how are you?": "hi love 😘",
"how are you?": "good and you? ♥️",
"can you give me info?": "i have all kinds of videos for sale and in my onlyfans subscription, we can do sexting and those naughty things… here are my links if you want to check them out 😍 linktr.ee/lizrainbow",
"i want some info please?": "baby check my links, there you can find everything about me linktr.ee/lizrainbow",
"are you hot?": "♥️♥️♥️",
"i want to buy something?": "baby here are my stores and other things you’re gonna love lizrainbow.manyvids.com",
"can you send me photos?": "baby my hot nude photos start from 50€ and are made so you can look at them again and again and get rock hard thinking about me 😘 i want you to be the one who gets the hottest and most private stuff… do you want a special pack or custom photos just for you? tell me what you like and i’ll send you exactly what turns you on the most 🔥 linktr.ee/lizrainbow",
"do you have onlyfans?": "on onlyfans you have all my exclusive content baby 😘 but if you want something more direct and personal i offer you special prices because i want you to have me: videos and photos from 50€, sexting from 60€ 💦 i can also make custom videos just for you 😈 do you want to subscribe or prefer to buy directly from me right now so it’s more intimate and hot? linktr.ee/lizrainbow",
}

def save_responses(responses_dict):
with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
json.dump(responses_dict, f, ensure_ascii=False, indent=4)

blocked_users = load_blocked()
respuestas = load_responses()

# Mensajes genéricos
GENERIC_MSG_ES = "Hola, en este momento no estoy pero miraré tu mensaje lo antes posible o puedes enviarme un email a lizrainbowx@gmail.com"
GENERIC_MSG_EN = "Hi, I'm not available right now but I'll check your message as soon as possible or you can email me at lizrainbowx@gmail.com"

# ================== COMANDOS ==================
@bot.message_handler(commands=['start'])
def start(message):
if message.chat.type != 'private': return
bot.reply_to(message, "👋 ¡Bienvenido! Bot listo. Usa /add para añadir nuevas preguntas y respuestas.")

@bot.message_handler(commands=['id'])
def get_user_id(message):
if message.chat.type != 'private': return
bot.reply_to(message, f"🔢 Tu ID es: <b>{message.from_user.id}</b>", parse_mode="HTML")

# AÑADIR nueva pregunta/respuesta
@bot.message_handler(commands=['add'])
def add_response(message):
if message.chat.type != 'private' or message.from_user.id != ADMIN_ID:
return
try:
# Formato: /add "pregunta?" "respuesta"
parts = message.text.split('"')
if len(parts) < 4:
bot.reply_to(message, "❌ Uso correcto:\n/add \"pregunta exacta?\" \"respuesta completa\"\nEjemplo: /add \"me puedes mandar mas fotos?\" \"claro amor aquí tienes...\"")
return
pregunta = parts[1].strip().lower()
respuesta = parts[3].strip()
respuestas[pregunta] = respuesta
save_responses(respuestas)
bot.reply_to(message, f"✅ Añadido correctamente:\nPregunta: {pregunta}\nRespuesta: {respuesta}")
except:
bot.reply_to(message, "❌ Error en el formato. Usa comillas dobles.")

# LISTAR todas las preguntas/respuestas
@bot.message_handler(commands=['list'])
def list_responses(message):
if message.chat.type != 'private' or message.from_user.id != ADMIN_ID:
return
if not respuestas:
bot.reply_to(message, "No hay respuestas configuradas.")
return
texto = "📋 **Preguntas y respuestas actuales:**\n\n"
for p, r in respuestas.items():
texto += f"❓ `{p}`\n→ {r}\n\n"
bot.reply_to(message, texto, parse_mode="Markdown")

# ELIMINAR una pregunta
@bot.message_handler(commands=['del'])
def del_response(message):
if message.chat.type != 'private' or message.from_user.id != ADMIN_ID:
return
try:
parts = message.text.split('"')
if len(parts) < 2:
bot.reply_to(message, "❌ Uso: /del \"pregunta exacta?\"")
return
pregunta = parts[1].strip().lower()
if pregunta in respuestas:
del respuestas[pregunta]
save_responses(respuestas)
bot.reply_to(message, f"✅ Pregunta eliminada: {pregunta}")
else:
bot.reply_to(message, "❌ Esa pregunta no existe.")
except:
bot.reply_to(message, "❌ Error en el formato.")

# Comandos de bloqueo (igual que antes)
@bot.message_handler(commands=['block', 'unblock', 'list_blocked'])
def admin_block(message):
# (código de bloqueo igual que en la versión anterior - lo mantengo funcional)
if message.chat.type != 'private' or message.from_user.id != ADMIN_ID: return
cmd = message.text.split()[0][1:]
if cmd == 'block':
try:
uid = int(message.text.split()[1])
blocked_users.add(uid)
save_blocked(blocked_users)
bot.reply_to(message, f"✅ Bloqueado {uid}")
except:
bot.reply_to(message, "Uso: /block <id>")
elif cmd == 'unblock':
try:
uid = int(message.text.split()[1])
blocked_users.discard(uid)
save_blocked(blocked_users)
bot.reply_to(message, f"✅ Desbloqueado {uid}")
except:
bot.reply_to(message, "Uso: /unblock <id>")
elif cmd == 'list_blocked':
bot.reply_to(message, "Bloqueados: " + ", ".join(map(str, blocked_users)) if blocked_users else "Ninguno")

# ================== RESPUESTAS AUTOMÁTICAS ==================
@bot.message_handler(func=lambda m: True)
def responder(message):
if message.chat.type != 'private': return
if message.from_user.id in blocked_users: return

texto = message.text.strip().lower()

try:
lang = detect(texto)
except:
lang = 'es'

# Coincidencia exacta
for pregunta, respuesta in respuestas.items():
if texto == pregunta:
bot.reply_to(message, respuesta)
return

# Genérico según idioma
if lang == 'en':
bot.reply_to(message, GENERIC_MSG_EN)
else:
bot.reply_to(message, GENERIC_MSG_ES)

# ================== INICIAR ==================
print("✅ Bot iniciado - Ahora puedes añadir respuestas desde Telegram con /add")
bot.infinity_polling()