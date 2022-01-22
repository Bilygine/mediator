import os

#DB CONFIG

SOURCE_TABLE = "sources"
DB = "test"
DB_PORT = 28015

#SERVER CONFIG

HOSTNAME = "mediator"
PORT = 5000

#LOCAL CONFIG

FILE_STORAGE = os.environ.get("FILE_STORAGE", "/usr/src/app/files/")
