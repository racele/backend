import http.server
import json
import urllib.parse

import database
import endpoint
import gateway
import response


class RequestHandler(http.server.BaseHTTPRequestHandler):
	protocol_version = "HTTP/1.1"
	timeout = 3.0

	def do_DELETE(self) -> None:
		self.respond(http.HTTPMethod.DELETE)

	def do_GET(self) -> None:
		self.respond(http.HTTPMethod.GET)

	def do_HEAD(self) -> None:
		self.respond(http.HTTPMethod.HEAD)

	def do_OPTIONS(self) -> None:
		self.send_response(http.HTTPStatus.NO_CONTENT)
		self.send_header("Access-Control-Allow-Headers", "*")
		self.send_header("Access-Control-Allow-Methods", "*")
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()

	def do_PATCH(self) -> None:
		self.respond(http.HTTPMethod.PATCH)

	def do_POST(self) -> None:
		self.respond(http.HTTPMethod.POST)

	def do_PUT(self) -> None:
		self.respond(http.HTTPMethod.PUT)

	def respond(self, method: http.HTTPMethod) -> None:
		try:
			result = self.run(method)
		except TimeoutError:
			self.close_connection = True
			result = response.error("Request timed out", http.HTTPStatus.REQUEST_TIMEOUT)

		body = json.dumps(result.data, cls=response.Encoder).encode()

		self.send_response(result.code)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Content-Length", str(len(body)))
		self.send_header("Content-Type", "application/json")
		self.end_headers()

		if method != http.HTTPMethod.HEAD:
			self.wfile.write(body)

	def run(self, method: http.HTTPMethod) -> response.Response:
		if not isinstance(self.server, Server):
			return response.error("Invalid server", http.HTTPStatus.INTERNAL_SERVER_ERROR)

		if method == http.HTTPMethod.HEAD:
			method = http.HTTPMethod.GET

		url = urllib.parse.urlparse(self.path)
		path = url.path

		for handler in self.server.endpoints:
			data: dict[str, str] = {}

			if method != handler.method or not handler.parse_path(data, path):
				continue

			if method == http.HTTPMethod.GET:
				query = url.query
			else:
				try:
					length = max(int(self.headers.get("Content-Length", 0)), 0)
				except ValueError:
					length = 0

				query = self.rfile.read(length).decode()

			parsed = dict(urllib.parse.parse_qsl(query, True))
			result = handler.parse_query(data, parsed)

			if result is not None:
				return result

			context = database.Context(data, self.server.database, self.server.gateway)
			result = handler.parse_auth(context, self.headers.get("Authorization"))

			if result is not None:
				return result

			return handler.run(context)

		return response.error("Invalid endpoint", http.HTTPStatus.NOT_FOUND)


class Server(http.server.HTTPServer):
	def __init__(self, host: str, port: int) -> None:
		super().__init__((host, port), RequestHandler)

		self.database = database.Database()
		self.endpoints = endpoint.collect()
		self.gateway = gateway.Gateway()
