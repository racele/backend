import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Auth:
	token: str
	user_id: int


@dataclasses.dataclass
class Session:
	created_at: int
	last_used_at: int
	session_id: int
	user_id: int


class SessionTable(table.Table):
	table = "session"

	def clear(self, token: str, user_id: int) -> None:
		self.execute("clear", token, user_id)

	def create(self, user_id: int) -> Auth:
		while True:
			token = self.random(20)

			try:
				self.execute("create", token, user_id)
			except sqlite3.IntegrityError:
				continue

			return Auth(token, user_id)

	def delete(self, session_id: int, user_id: int) -> bool:
		cursor = self.execute("delete", session_id, user_id)
		return cursor.rowcount == 1

	def end(self, token: str) -> bool:
		cursor = self.execute("end", token)
		return cursor.rowcount == 1

	def list(self, user_id: int) -> list[Session]:
		rows = self.fetchall("list", user_id)
		return [Session(*row) for row in rows]

	def resolve(self, token: str) -> Auth | None:
		row = self.fetchone("resolve", token)

		if row is None:
			return None

		return Auth(*row)
