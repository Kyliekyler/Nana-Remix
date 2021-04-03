import os
import time
from pathlib import Path

from PIL import Image
from pyrogram import filters
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError
from youtube_dl.utils import DownloadError
from youtube_dl.utils import ExtractorError
from youtube_dl.utils import GeoRestrictedError
from youtube_dl.utils import MaxDownloadsReached
from youtube_dl.utils import PostProcessingError
from youtube_dl.utils import UnavailableVideoError
from youtube_dl.utils import XAttrMetadataError

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply
from nana.plugins.downloads import progressdl

__MODULE__ = 'YouTube'
__HELP__ = """
download, convert music from youtube!

──「 **Download video** 」──
-> `ytdl (url)`
Download youtube video (mp4)

──「 **Convert to music** 」──
-> `ytmusic (url)`
Download youtube music, and then send to tg as music.
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('ytdl', COMMAND_PREFIXES),
)
async def youtube_download(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edit_or_reply(message, text='missing [url] parameter!!')
        return
    url = args[1]
    opts = {
        'format': 'bestvideo+bestaudio',
        'addmetadata': True,
        'key': 'FFmpegMetadata',
        'writethumbnail': True,
        'prefer_ffmpeg': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
        ],
        'outtmpl': '%(id)s.mp4',
        'logtostderr': False,
        'quiet': True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await edit_or_reply(message, text=f'`{str(DE)}`')
        return
    except ContentTooShortError:
        await edit_or_reply(
            message,
            text='`The download content was too short.`',
        )
        return
    except GeoRestrictedError:
        await edit_or_reply(
            message,
            text='`Video is not available.`',
        )
        return
    except MaxDownloadsReached:
        await edit_or_reply(
            message,
            text='`Max-downloads limit has been reached.`',
        )
        return
    except PostProcessingError:
        await edit_or_reply(
            message, text='`There was an error during post processing.`',
        )
        return
    except UnavailableVideoError:
        await edit_or_reply(
            message, text='`Media is not available in the requested format.`',
        )
        return
    except XAttrMetadataError as XAME:
        await edit_or_reply(
            message,
            text=f'`{XAME.code}: {XAME.msg}\n{XAME.reason}`',
        )
        return
    except ExtractorError:
        await edit_or_reply(
            message, text='`There was an error during info extraction.`',
        )
        return
    thumbnail = Path(f"{ytdl_data['thumbnails'][-1]['filename']}")
    im = Image.open(Path(thumbnail)).convert("RGB")
    width, height = im.size
    im = im.resize((width // 6, height // 6))
    im.save(Path(f"{ytdl_data['id']}.jpeg"))
    os.remove(thumbnail)
    thumbnail = Path(f"{ytdl_data['id']}.jpeg")
    c_time = time.time()
    caption = f"<a href={url}>{ytdl_data['title']}</a>"
    try:
        await message.reply_video(
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            duration=ytdl_data['duration'],
            caption=caption,
            thumb=thumbnail,
            width=ytdl_data['width'],
            height=ytdl_data['height'],
            parse_mode="HTML",
            progress=lambda d, t: client.loop.create_task(
                progressdl(d, t, message, c_time, 'Uploading...'),
            ),
        ),
    except FileNotFoundError:
        await message.reply_video(
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            duration=ytdl_data['duration'],
            caption=caption,
            width=ytdl_data['width'],
            height=ytdl_data['height'],
            parse_mode="HTML",
            progress=lambda d, t: client.loop.create_task(
                progressdl(d, t, message, c_time, 'Uploading...'),
            ),
        ),
        pass
    os.remove(f"{ytdl_data['id']}.mp4")
    if thumbnail:
        os.remove(thumbnail)
    await message.delete()


@app.on_message(
    filters.user(AdminSettings) & filters.command('ytmusic', COMMAND_PREFIXES),
)
async def youtube_music(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edit_or_reply(message, text='missing [url] parameter!')
        return
    url = args[1]
    opts = {
        'format': 'bestaudio',
        'addmetadata': True,
        'key': 'FFmpegMetadata',
        'writethumbnail': True,
        'prefer_ffmpeg': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
        ],
        'outtmpl': '%(id)s.mp3',
        'quiet': True,
        'logtostderr': False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await edit_or_reply(message, text=f'`{str(DE)}`')
        return
    except ContentTooShortError:
        await edit_or_reply(
            message,
            text='`The download content was too short.`',
        )
        return
    except GeoRestrictedError:
        await edit_or_reply(
            message,
            text='`Video is not available.`',
        )
        return
    except MaxDownloadsReached:
        await edit_or_reply(
            message,
            text='`Max-downloads limit has been reached.`',
        )
        return
    except PostProcessingError:
        await edit_or_reply(
            message, text='`There was an error during post processing.`',
        )
        return
    except UnavailableVideoError:
        await edit_or_reply(
            message, text='`Media is not available in the requested format.`',
        )
        return
    except XAttrMetadataError as XAME:
        await edit_or_reply(
            message,
            text=f'`{XAME.code}: {XAME.msg}\n{XAME.reason}`',
        )
        return
    except ExtractorError:
        await edit_or_reply(
            message, text='`There was an error during info extraction.`',
        )
        return
    thumbnail = Path(f"{ytdl_data['thumbnails'][-1]['filename']}")
    im = Image.open(Path(thumbnail)).convert("RGB")
    width, height = im.size
    im = im.resize((width // 6, height // 6))
    im.save(Path(f"{ytdl_data['id']}.jpeg"))
    os.remove(thumbnail)
    thumbnail = Path(f"{ytdl_data['id']}.jpeg")
    c_time = time.time()
    caption = f"<a href={url}>{ytdl_data['title']}</a>"
    try:
        await message.reply_audio(
            f"{ytdl_data['id']}.mp3",
            duration=ytdl_data['duration'],
            caption=caption,
            thumb=thumbnail,
            parse_mode="HTML",
            progress=lambda d, t: client.loop.create_task(
                progressdl(d, t, message, c_time, 'Uploading...'),
            ),
        ),
    except FileNotFoundError:
        await message.reply_audio(
            f"{ytdl_data['id']}.mp3",
            duration=ytdl_data['duration'],
            caption=caption,
            parse_mode="HTML",
            progress=lambda d, t: client.loop.create_task(
                progressdl(d, t, message, c_time, 'Uploading...'),
            ),
        ),
    os.remove(f"{ytdl_data['id']}.mp3")
    if thumbnail:
        os.remove(thumbnail)
    await message.delete()
