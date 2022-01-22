from __future__ import unicode_literals
import youtube_dl
import google
import logging

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_video(source, download=True, update_status=True):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './files/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': source.format,
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            source.update_status("DOWNLOADING")
            meta = ydl.extract_info(source.url, download=True)
            update = dict()
            logging.info(meta)
            update['url'] = meta['webpage_url']
            update['video_id'] = meta['id']
            update['author'] = meta['uploader']
            update['title'] = meta['title']
            update['thumbnail'] = meta['thumbnail']
            source.update(update)
            source.set_filename()
            source.set_filepath()
            source.set_filename_raw()
            source.set_filepath_raw()
            source.convert_to_raw()
    except:
        source.update_status("ERROR WHILE DOWNLOADING RAW FILE")
        raise
    #Save original audio file to GS before starting the conversion process
    try:
        source.upload_blob(format=source.format)
    except google.auth.exceptions.DefaultCredentialsError:
        source.update_status("MISSING_CREDENTIALS")
        raise
