import asyncio
import websockets
import os
from urllib.parse import urlparse

hostName = "0.0.0.0"
hostPort = 80


async def echo(websocket, path):
	parse_result = None
	try:
		parse_result = urlparse("." + path)
	except Exception:
		raise ValueError('Fail to parse URL')

	file_path = os.path.abspath(parse_result.path)
	with open(file_path) as f:
		while True:
			f.seek(0, os.SEEK_SET)
			content = f.read()
			if content:
				await websocket.send(content)
			else:
				await asyncio.sleep(1)

start_server = websockets.serve(echo, hostName, hostPort)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
