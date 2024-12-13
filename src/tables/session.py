import sqlite3

import table


class SessionTable(table.Table):
	table = "session"

	def clear(self, user_id: int, token: str) -> None:
		self.execute("clear", token, user_id)

	def create(self, user_id: int) -> str:
		while True:
			token = self.random(20)

			try:
				self.execute("create", token, user_id)
			except sqlite3.IntegrityError:
				continue

			return token

	def resolve(self, token: str) -> int | None:
		cursor = self.execute("resolve", token)
		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return data[0]
