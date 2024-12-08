import http.server
import json
import urllib.parse

import database
import endpoint
import endpoints.endpoints


class RequestHandler(http.server.BaseHTTPRequestHandler):
	protocol_version = "HTTP/1.1"

	def do_PATCH(self) -> None:
		self.respond(http.HTTPMethod.PATCH)

	def do_POST(self) -> None:
		self.respond(http.HTTPMethod.POST)

	def respond(self, method: http.HTTPMethod) -> None:
		result = self.run(method)
		response = json.dumps(result.response).encode()

		self.send_response(result.code)
		self.send_header("Content-Type", "application/json")
		self.send_header("Content-Length", str(len(response)))
		self.end_headers()

		self.wfile.write(response)

	def run(self, method: http.HTTPMethod) -> endpoint.Result:
		if not isinstance(self.server, Server):
			return endpoint.error("invalid server", http.HTTPStatus.INTERNAL_SERVER_ERROR)

		try:
			length = int(self.headers["Content-Length"])
		except Exception:
			length = 0

		query = self.rfile.read(length).decode()
		parsed = dict(urllib.parse.parse_qsl(query))
		data = database.RequestData(parsed, self.server.database)

		url = urllib.parse.urlparse(self.path)
		path = url.path.strip("/")

		for handler in self.server.endpoints:
			if handler.method == method and handler.path == path:
				return handler.run(data)
		else:
			return endpoint.error("invalid endpoint", http.HTTPStatus.NOT_FOUND)


class Server(http.server.HTTPServer):
	def __init__(self, port: int) -> None:
		super().__init__(("0.0.0.0", port), RequestHandler)

		self.database = database.Database()
		self.endpoints = endpoints.endpoints.collect(self.database)
