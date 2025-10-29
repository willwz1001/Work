#!/usr/bin/env python3
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from googletrans import Translator

# Load env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN tidak ditemukan. Isi di .env atau environment variable.")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Translator (googletrans 4.0.0-rc1)
translator = Translator()

# Simple persistence for per-chat auto flag
DATA_FILE = Path("chats.json")
if DATA_FILE.exists():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            chat_auto = json.load(f)
    except Exception:
        chat_auto = {}
else:
    chat_auto = {}

def save_state():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(chat_auto, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("Gagal menyimpan state: %s", e)

# Commands
def start(update, context):
    txt = (
        "Halo — saya bot terjemahan Indonesia <-> Thailand.\n\n"
        "Fitur:\n"
        "- Mendeteksi pesan berbahasa Indonesia atau Thai dan otomatis menerjemahkan ke bahasa sebaliknya.\n"
        "- Gunakan /auto_off untuk mematikan auto-translate di chat ini.\n"
        "- Gunakan /auto_on untuk menyalakan kembali.\n"
        "- Gunakan /status untuk melihat status auto-translate di chat.\n\n"
        "Catatan: Bot ini menerjemahkan hanya ketika terdeteksi bahasa 'id' atau 'th'."
    )
    update.message.reply_text(txt)

def status(update, context):
    chat_id = str(update.effective_chat.id)
    enabled = chat_auto.get(chat_id, True)
    update.message.reply_text(f"Auto-translate {'ON' if enabled else 'OFF'} untuk chat ini.")

def auto_on(update, context):
    chat_id = str(update.effective_chat.id)
    chat_auto[chat_id] = True
    save_state()
    update.message.reply_text("Auto-translate diaktifkan untuk chat ini.")

def auto_off(update, context):
    chat_id = str(update.effective_chat.id)
    chat_auto[chat_id] = False
    save_state()
    update.message.reply_text("Auto-translate dimatikan untuk chat ini.")

# Message handling
def handle_message(update, context):
    msg = update.effective_message
    if not msg or not msg.text:
        return

    # Ignore other bots
    if msg.from_user and msg.from_user.is_bot:
        return

    chat_id = str(update.effective_chat.id)
    enabled = chat_auto.get(chat_id, True)
    if not enabled:
        return

    text = msg.text.strip()
    if not text:
        return

    try:
        detected = translator.detect(text).lang
    except Exception as e:
        logger.warning("Gagal detect bahasa: %s", e)
        return

    # We only auto-translate between Indonesian (id) and Thai (th)
    target = None
    if detected == "id":
        target = "th"
    elif detected == "th":
        target = "id"
    else:
        # Not id or th -> skip auto-translation
        return

    try:
        translated = translator.translate(text, dest=target).text
    except Exception as e:
        logger.exception("Gagal translate: %s", e)
        return

    # reply with the translated text
    reply = f"Terjemahan ({detected} → {target}):\n{translated}"
    try:
        msg.reply_text(reply)
    except Exception:
        # Telegram sometimes blocks same-message replies; attempt send_message fallback
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def error_handler(update, context):
    logger.exception("Update caused error: %s", context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("auto_on", auto_on))
    dp.add_handler(CommandHandler("auto_off", auto_off))

    # messages
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    dp.add_error_handler(error_handler)

    logger.info("Bot started. Polling...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()