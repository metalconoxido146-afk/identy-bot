import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
TOKEN="9271644583:AAFFo57yudH-d69TL0f4EuBnCf7pKTEBZIY"
user_choice={}
async def start(update, context):
 keyboard=[[InlineKeyboardButton("🔍 RUC",callback_data='RUC')]]
 markup=InlineKeyboardMarkup(keyboard)
 await update.message.reply_text("Bienvenido a IDenty PE",reply_markup=markup)
async def botones(update, context):
 query=update.callback_query
 await query.answer()
 user_choice[query.from_user.id]=query.data
 await query.edit_message_text("Enviame el RUC de 11 digitos. Ej: 20100017491")
async def recibir(update, context):
 texto=update.message.text.strip()
 if len(texto)!=11:
  await update.message.reply_text("Debe tener 11 digitos")
  return
 await update.message.reply_text(f"Buscando {texto}...")
 try:
  r=requests.get(f"https://dniruc.apisperu.com/api/v1/ruc/{texto}",timeout=15).json()
  if r.get('ruc'):
   msg=f"RUC: {r.get('ruc')}\nRazon: {r.get('razonSocial')}\nEstado: {r.get('estado')}\nDireccion: {r.get('direccion')}"
  else:
   msg=f"No encontrado"
  await update.message.reply_text(msg)
 except Exception as e:
  await update.message.reply_text(f"Error: {e}")
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(botones))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,recibir))
app.run_polling()
