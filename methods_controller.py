from flask import Flask, request
from flask_cors import CORS
from youtubedl import *
from objects.Source import Source
import rethinkdb_functions
import threading
import traceback
import logging
    
def create_new_source(url):
    """
    DISALLOW DUPLICATE IMPLEMENTATION
    """
    """
    END OF DUPLICATE IMPLEMENTATION
    """
    source = Source(url=url)
    source.verify_url()
    if source.url == "Invalid URL":
        return "Invalid URL"
    ret = source.create_into_db()
    ret['source_id'] = source.id
    thread = threading.Thread(target=download_new_source, kwargs={'source': source})
    thread.start()
    ###
    ###Create a second thread to start download, and return the confirmation of source creation
    ###
    
    return ret

def download_new_source(source):
    """
    YOUTUBE IMPLEMENTATION
    """
    download_video(source, download=True)
    """
    END OF YOUTUBE IMPLEMENTATION
    """
    try:
        source.upload_blob()
        source.update_status("DOWNLOADED")
    except:
        source.download = "ERROR"
        source.update_status("ERROR WHILE PUSHING TO GOOGLE STORAGE")
        logging.info(source.url, source.file_name, source.file_name_raw)
        raise

def update_existing_source(request):
    source_id = request.args.get('source_id')
    return "Not Implemented yet"


def delete_source(source_id):
    source = Source(id=source_id)
    source.update_status("DELETING")
    ret = source.delete_from_db()
    ret['source_id'] = source.id
    return ret


