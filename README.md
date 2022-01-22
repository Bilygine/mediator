
# Create a folder "credentials" where you will put your google_credentials.json

In your docker-compose.yaml, add something like this

```
 volumes:
  - /path/to/local/credentials:/path/to/docker/credentials
 environment:
  - GOOGLE_APPLICATION_CREDENTIALS=/path/to/docker/credentials
```

# Exemple of a full docker-compose.yaml :

```
version: '3'
services:
    source:
        image: bilygine/bilygine-downloader
        ports:
            - "5000:5000"
        volumes:
            - ./downloader/credentials:/code/credentials
        environment:
            - GOOGLE_APPLICATION_CREDENTIALS=/code/credentials/bilygine_google_credentials.json
            - BUCKET_NAME=bilygine-audio
    db:
        image: rethinkdb
        ports:
            - "8080:8080"
            - "29015"
            - "28015"
        volumes:
            - ./rethinkdb:/data
    analyzer:
        image: bilygine/bilygine-analyzer
        ports:
          - "8123:8123"
        volumes:
            - ./analyzer/analyzer-core/conf:/analyzer/conf/
```

# USING RETHINKDB

## QUERY TO INDEX url KEY

```
r.db("test").table("source").indexCreate('url')
```

## QUERY TO GET ALL object with a specific url

```
r.db("test").table("source").getAll('https://www.youtube.com/watch?v=TzO0hWJn-Ac', {index:'url'})
```