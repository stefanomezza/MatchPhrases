from MatchPhrases import MatchPhrases
from MatchNounChunks import MatchNounChunks
import logging
import cherrypy as http
from enum import Enum

'''
run.py - Launches a CherryPy server exposing the find_matches method of the MatchPhrases class.
The server is implemented through the CherryPy framework and accepts GET requests to the base_url/find_matches URI.
More details in the README.md file
'''


class Server(Enum):
    BASE = 0,
    NOUN_CHUNK = 1

# configuration of the server
config = {
    "server_port": 8080,
    "phrases_file": "phrases.txt",
    "number_of_threads": 10,
    "logging_level": logging.INFO,
    "server_type": Server.NOUN_CHUNK
}

# setup the logging
logger = logging.getLogger("Server")
logger.setLevel(config.get("logging_level")) 

# initializing server
logger.log(level=logging.INFO, msg="Initializing server")
http.config.update({'server.socket_port': config.get("server_port"),
                    'server.thread_pool': config.get("number_of_threads"),
                    'global': {
                        'engine.autoreload.on': False
                    }
                    })
try:
    # check which server to run
    if config.get("server_type") == Server.NOUN_CHUNK:
        mp_server = MatchNounChunks(config.get("phrases_file"))
    else:
        mp_server = MatchPhrases(config.get("phrases_file"))
    logger.log(level=logging.INFO, msg="Phrases loaded correctly! Server starting...")
    # starting server
    http.quickstart(mp_server)
    logger.log(level=logging.INFO, msg="Server started at 127.0.0.1:8080/")

except AssertionError:
    # the phrases file doesn't exist: critical failure
    logger.log(level=logging.CRITICAL,
               msg="ERROR: Phrases file '" + config.get("phrases_file") + "' not found. Server will shut down")
    exit(1)
