from telethon import TelegramClient, events
from telethon.sync import TelegramClient
from telegram.ext import Updater, CommandHandler, Filters
import asyncio
import os

# 配置
api_id = '18138452'  # 替换为您的Telegram API ID
api_hash = '42f89bf956575caa848bd97b0e774fe9'  # 替换为您的Telegram API Hash
bot_token = '5854334680:AAGJnVrAXVhRO3BnfBUza2vy_DtpmLtxw4I'  # 替换为您的Bot Token
save_path = '/cc'  # 替换为保存文件的路径

# 初始化Telegram客户端
client = TelegramClient('session_name', api_id, api_hash)

# 下载媒体文件的异步函数
async def download_media(message):
    if message.photo or message.video:
        file_path = os.path.join(save_path, message.file.name)
        await message.download_media(file=file_path)
        print(f'文件已下载：{file_path}')

# 处理新消息的事件
@client.on(events.NewMessage)
async def handler(event):
    await download_media(event.message)

# Telegram机器人的命令处理器
def start(update, context):
    update.message.reply_text('发送Telegram群组或频道链接。')

def handle_link(update, context):
    url = update.message.text
    asyncio.run(client.start())
    asyncio.create_task(client.get_entity(url))
    update.message.reply_text('开始监控频道或群组。')

# 主函数，设置和运行Telegram机器人
def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()