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
	def __init__(self, auth: str | None, data: dict[str, str], database: Database) -> None:
		self.data = data
		self.user = None

		if auth is not None:
			parts = auth.split()

			if len(parts) == 2 and parts[0].lower() == "bearer":
				self.user = database.tokens.resolve(parts[1])

	def get(self, parameter: str) -> str:
		return self.data.get(parameter, "").strip()
