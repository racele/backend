import sqlite3

import tables.request
import tables.token
import tables.user


class Database:
	def __init__(self) -> None:
		connection = sqlite3.connect(":memory:")

		self.requests = tables.request.RequestTable(connection)
		self.tokens = tables.token.TokenTable(connection)
		self.users = tables.user.UserTable(connection)

		with open("sql/init.sql") as file:
			script = file.read()

		connection.executescript(script)


class RequestData:
	data: dict[str, str]
	user: int | None

	def __init__(self, data: dict[str, str], database: Database) -> None:
		self.data = data
		self.user = database.tokens.resolve(self.get("token"))

	def get(self, parameter: str) -> str:
		return self.data.get(parameter, "").strip()
