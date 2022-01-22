import uuid
import time
import sox
import os
import requests
import rethinkdb_functions
from google.cloud import storage
import logging
import config


class Source(object):
    """
    Source object to use from Rethinkdb
    If id is not provided, a uuid will be generated randomly
    """
    def __init__(self, url="", audio_format="mp3", download="", id=None, title="", author="", thumbnail=""):
        
        self.url = url
        self.format = audio_format
        self.download = download
        self.title = title
        self.author = author
        self.thumbnail = thumbnail
        self.registered_at = int(time.time())
        self.status = "WAITING"
        if id == None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    @staticmethod
    def from_dict(source):
        """
        Create a Source object from a dict
        """
        id = source.get('id', None)
        url = source.get('url')
        format = source.get('format', 'mp3')
        download = source.get('download')
        title = source.get('title')
        author = source.get('author')
        thumbnail = source.get('thumbnail')

        return Source(id=id,
            url=url,
            download=download,
            title=title,
            author=author,
            thumbnail=thumbnail,
            )

    @staticmethod
    def from_db(source_id):
        return self.from_dict(self.get_from_db(source_id))

    def to_dict(self):
        """
        Return the Source object in a dict form
        """
        ret = dict()
        ret['id'] = self.id
        ret['url'] = self.url
        if self.format != None:
            ret['format'] = self.format
        ret['download'] = self.download
        ret['title'] = self.title
        ret['author'] = self.author
        ret['thumbnail'] = self.thumbnail
        ret['registered_at'] = self.registered_at
        ret['status'] = self.status
        return ret

    def get_from_db(self, source_id):
        return rethinkdb_functions.get_source(source_id)

    def create_into_db(self):
        return rethinkdb_functions.create_source(self)

    def update_in_db(self):
        return rethinkdb_functions.update_source(self)

    def delete_from_db(self):
        return rethinkdb_functions.delete_source(self)

    def update(self, body={}):
        """
        Takes a dict body argument and update the Source object properties according to it
        You cannot update id
        """
        self.url = body.get('url', self.url)
        self.format = body.get('format', self.format)
        self.download = body.get('download', self.download)
        self.title = body.get('title', self.title)
        self.author = body.get('author', self.author)
        self.thumbnail = body.get('thumbnail', self.thumbnail)
        self.video_id = body.get('video_id', "")
        self.status = body.get('status', self.status)
        return self.update_in_db()

    def update_status(self, new_status):
        """
        Take a string and put it in a dict before sending it to update method
        """
        body = dict()
        body['status'] = new_status
        return self.update(body)

    def set_filename(self):
        """
        Set filename according to this template <video_id>.<format>
        """
        self.file_name_base = str(self.video_id)
        self.file_name = str(self.video_id) + "." + self.format

    def set_filepath(self):
        if hasattr(self, 'file_name'):
            self.file_path = config.FILE_STORAGE + self.file_name
        else:
            self.set_filename()
            self.set_filepath()

    def convert_to_raw(self):
        """
        Convert downloaded audio file into raw file
        """
        self.update_status("CONVERTING")
        audio_file = sox.Transformer()
        audio_file.convert(samplerate=16000,
                            n_channels=1,
                            bitdepth=16,)
        audio_file.build(self.file_path, self.file_path_raw)

    def set_filename_raw(self):
        if hasattr(self, 'file_name_base'):
            self.file_name_raw = self.file_name_base + ".raw"
        else:
            self.set_filename()
            self.set_filename_raw()    

    def set_filepath_raw(self):
        if hasattr(self, 'file_name_raw'):
            self.file_path_raw = config.FILE_STORAGE + self.file_name_raw
        else:
            self.set_filename_raw()
            self.set_filepath_raw()

    def upload_blob(self, format="raw"):
        """
        Uploads a file to the bucket
        """
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(os.environ['BUCKET_NAME'])
        if format == 'raw':
            file_to_upload = self.file_name_raw
            path_to_upload = self.file_path_raw
        else:
            file_to_upload = self.file_name
            path_to_upload = self.file_path
        blob = bucket.blob("fr/" + file_to_upload)
        self.update_status("UPLOADING_TO_GS")
        blob.upload_from_filename(path_to_upload)
        logging.info('File {} uploaded to {}.'.format(
            file_to_upload,
            "fr/" + file_to_upload))
        self.download = "gs://" + os.environ['BUCKET_NAME'] + "/fr/" + self.file_name_raw
        self.update()

    def verify_url(self):
        """
        Check if URL return 404. If it does, self.url becomes "Invalid URL"
        """
        try:
            r = requests.get(self.url)
            if r.status_code == 404:
                self.url = "Invalid URL"
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            self.url = "Invalid URL"

    def __str__(self):
        return self.url + "\n" + str(self.title) + "\n" + str(self.author)


