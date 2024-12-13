import sqlite3

import tables.request
import tables.session
import tables.user


class Database:
	def __init__(self) -> None:
		connection = sqlite3.connect(":memory:")

		self.requests = tables.request.RequestTable(connection)
		self.sessions = tables.session.SessionTable(connection)
		self.users = tables.user.UserTable(connection)

		with open("sql/init.sql") as file:
			script = file.read()

		connection.executescript(script)


class Context:
	def __init__(self, data: dict[str, str], database: Database) -> None:
		self.data = data
		self.database = database

		self.token = None
		self.user_id = None

	def get_token(self) -> str:
		if self.token is None:
			raise ValueError("missing token")

		return self.token

	def get_user_id(self) -> int:
		if self.user_id is None:
			raise ValueError("missing user_id")

		return self.user_id

	def set_token(self, token: str) -> None:
		self.token = token
		self.user_id = self.database.sessions.resolve(token)
