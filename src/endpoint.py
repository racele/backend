import abc
import http
import importlib
import os

import database
import response


class Endpoint:
	auth: bool
	method: http.HTTPMethod
	path: str
	query: list[str]

	@classmethod
	def parse_auth(cls, context: database.Context, auth: str | None) -> response.Response | None:
		if not cls.auth:
			return None

		if auth is None:
			return response.error("missing authorization", http.HTTPStatus.UNAUTHORIZED)

		parts = auth.strip().split()

		if len(parts) != 2 or parts[0].lower() != "bearer":
			return response.error("invalid authorization format", http.HTTPStatus.UNAUTHORIZED)

		context.set_token(parts[1])

		if context.user_id is None:
			return response.error("invalid token", http.HTTPStatus.UNAUTHORIZED)

		return None

	@classmethod
	def parse_path(cls, data: dict[str, str], path: str) -> bool:
		expected_parts = cls.path.split("/")
		got_parts = path.split("/")

		if len(expected_parts) != len(got_parts):
			return False

		for expected, got in zip(expected_parts, got_parts):
			if expected.startswith("{") and expected.endswith("}") and not got.startswith("@"):
				key = expected.removeprefix("{").removesuffix("}")
				data[key] = got.strip()
			elif expected != got:
				return False

		return True

	@classmethod
	def parse_query(cls, data: dict[str, str], query: dict[str, str]) -> response.Response | None:
		for parameter in cls.query:
			name = parameter.removesuffix("?")
			optional = parameter.endswith("?")

			if name in query:
				data[name] = query[name].strip()
				del query[name]
			elif not optional:
				return response.error(f"missing parameter '{name}'")

		for name in data:
			if not data[name]:
				return response.error(f"empty parameter '{name}'")

		for name in query:
			return response.error(f"unknown parameter '{name}'")

		return None

	@staticmethod
	@abc.abstractmethod
	def run(context: database.Context) -> response.Response:
		pass


def collect() -> list[type[Endpoint]]:
	endpoints: list[type[Endpoint]] = []

	for file in os.listdir("src/endpoints"):
		if not file.endswith(".py"):
			continue

		name = file.removesuffix(".py")
		module = importlib.import_module(f"endpoints.{name}")

		for value in vars(module).values():
			if isinstance(value, type) and issubclass(value, Endpoint):
				endpoints.append(value)

	return endpoints
