import http.server
import json
import urllib.parse

import database
import endpoint
import endpoints.endpoints


class RequestHandler(http.server.BaseHTTPRequestHandler):
	def do_PATCH(self) -> None:
		self.run(http.HTTPMethod.PATCH)

	def do_POST(self) -> None:
		self.run(http.HTTPMethod.POST)

	def run(self, method: http.HTTPMethod) -> None:
		if not isinstance(self.server, Server):
			return

		try:
			length = int(self.headers["content-length"])
		except Exception:
			length = 0

		query = self.rfile.read(length).decode()
		parsed = dict(urllib.parse.parse_qsl(query))
		data = database.RequestData(parsed, self.server.database)

		url = urllib.parse.urlparse(self.path)
		path = url.path.strip("/")

		for handler in self.server.endpoints:
			if handler.method == method and handler.path == path:
				result = handler.run(data)
				break
		else:
			result = endpoint.error("invalid endpoint", http.HTTPStatus.NOT_FOUND)

		self.send_response(result.code)
		self.send_header("content-type", "application/json")
		self.end_headers()

		self.wfile.write(json.dumps(result.response).encode())


class Server(http.server.HTTPServer):
	def __init__(self, port: int) -> None:
		super().__init__(("0.0.0.0", port), RequestHandler)

		self.database = database.Database()
		self.endpoints = endpoints.endpoints.collect(self.database)
