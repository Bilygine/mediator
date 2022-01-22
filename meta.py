from youtubedl import download_video
from objects.Source import Source

source = Source(url="https://www.youtube.com/watch?v=lTTajzrSkCw")
download_video(source)