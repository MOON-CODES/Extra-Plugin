import os
import time
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
from VIPMUSIC import app

TMP_DOWNLOAD_DIRECTORY = "tg-File/"
CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"

def upload_to_catbox(file_path):
    files = {'fileToUpload': open(file_path, 'rb')}
    data = {'reqtype': 'fileupload'}

    response = requests.post(CATBOX_UPLOAD_URL, files=files, data=data)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Failed to upload to Catbox: {response.status_code} {response.text}")

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

@bot.on_message(filters.command(["tgm", "tgt"]) & filters.reply)
async def catbox_upload(client, message):
    input_command = message.command[0]
    optional_title = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    
    reply_msg = message.reply_to_message
    
    if input_command == "tgm":
        if reply_msg.media:
            start_time = time.time()
            downloaded_file_name = await reply_msg.download(TMP_DOWNLOAD_DIRECTORY)
            if not downloaded_file_name:
                await message.reply("Not Supported Format Media!")
                return
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)

            try:
                media_url = upload_to_catbox(downloaded_file_name)
            except Exception as exc:
                await message.reply(f"ERROR: {str(exc)}")
                os.remove(downloaded_file_name)
            else:
                os.remove(downloaded_file_name)
                end_time = time.time()
                time_taken = round(end_time - start_time, 2)

                await message.reply(
                    f"➼ Uploaded to Catbox in {time_taken} seconds.\n\n➼ Copy Link : {media_url}",
                    disable_web_page_preview=True
                )

    elif input_command == "tgt":
        if reply_msg.text:
            page_content = reply_msg.text
            if reply_msg.media:
                downloaded_file_name = await reply_msg.download(TMP_DOWNLOAD_DIRECTORY)
                with open(downloaded_file_name, "rb") as fd:
                    file_content = fd.read().decode("utf-8")
                    page_content += "\n" + file_content
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")

            start_time = time.time()

            await message.reply(
                f"➼ Text has been processed and uploaded in {round(time.time() - start_time, 2)} seconds.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("➡ View Processed Text", url="https://catbox.moe/")]]
                )
            )

    else:
        await message.reply("Reply to a message to upload it to Catbox.")
__MODULE__ = "Tᴇʟᴇɢʀᴀᴘʜ"
