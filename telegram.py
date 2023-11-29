from telethon import TelegramClient, events
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import asyncio
import os

# 配置
api_id = '18138452'  # Telegram API ID
api_hash = '42f89bf956575caa848bd97b0e774fe9'  # Telegram API Hash
bot_token = '5854334680:AAGJnVrAXVhRO3BnfBUza2vy_DtpmLtxw4I'  # Bot Token
save_path = '/cc'  # 文件保存路径

# Telegram 客户端初始化
client = TelegramClient('session', api_id, api_hash)

async def download_media(message):
    if message.photo or message.video:
        file_path = os.path.join(save_path, message.file.name)
        await message.download_media(file=file_path)
        print(f"文件已下载：{file_path}")

@client.on(events.NewMessage)
async def handler(event):
    await download_media(event.message)

# Telegram Bot 处理器
def start(update, context):
    update.message.reply_text('发送Telegram群组或频道链接。')

def handle_link(update, context):
    url = update.message.text
    asyncio.run(client.start())
    asyncio.create_task(client.get_entity(url))
    update.message.reply_text('开始监控频道或群组。')

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()