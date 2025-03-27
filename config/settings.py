import os

DISCORD_TOKEN = os.environ.get("tokenDiscord")
stream = 'http://localhost:5000/stream'
instructions = 'http://localhost:5000/instructions'
clear = 'http://localhost:5000/clear'
file_search = 'http://localhost:5000/file-search'
remove_historique = 'http://localhost:5000/remove_historique'

model = "gpt-4o"

api_key = os.environ.get("tokenGPT")
