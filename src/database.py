import sqlite3

import gateway
import tables.daily
import tables.request
import tables.score
import tables.session
import tables.user


class Database:
	def __init__(self) -> None:
		connection = sqlite3.connect(":memory:")
		connection.row_factory = sqlite3.Row

		self.dailies = tables.daily.DailyTable(connection)
		self.requests = tables.request.RequestTable(connection)
		self.scores = tables.score.ScoreTable(connection)
		self.sessions = tables.session.SessionTable(connection)
		self.users = tables.user.UserTable(connection)

		with open("sql/init.sql") as file:
			script = file.read()

		connection.executescript(script)


class Context:
	def __init__(self, data: dict[str, str], database: Database, gateway: gateway.Gateway) -> None:
		self.auth = None
		self.data = data
		self.database = database
		self.gateway = gateway

	def get_auth(self) -> tables.session.Auth:
		if self.auth is None:
			raise ValueError

		return self.auth

	def set_auth(self, token: str) -> None:
		self.auth = self.database.sessions.resolve(token)
