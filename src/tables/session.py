import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Session:
	created_at: int
	id: int
	last_used_at: int | None
	user_id: int


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

	def delete(self, session_id: int, user_id: int) -> bool:
		cursor = self.execute("delete", session_id, user_id)
		return cursor.rowcount == 1

	def list(self, user_id: int) -> list[Session]:
		data = self.fetchall("list", user_id)
		return [Session(*row) for row in data]

	def resolve(self, token: str) -> int | None:
		data = self.fetchone("resolve", token)

		if data is None:
			return None

		return data[0]
