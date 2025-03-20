import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Request:
	accepted_at: int | None
	created_at: int
	recipient_id: int
	sender_id: int


class RequestTable(table.Table):
	table = "request"

	def accept(self, recipient_id: int, sender_id: int) -> Request | None:
		row = self.fetchone("accept", recipient_id, sender_id)

		if row is None:
			return None

		return Request(*row)

	def accepted(self, user_id: int) -> list[Request]:
		rows = self.fetchall("accepted", user_id)
		return [Request(*row) for row in rows]

	def create(self, recipient_id: int, sender_id: int) -> Request | None:
		try:
			row = self.fetchone("create", recipient_id, sender_id)
		except sqlite3.IntegrityError:
			return None

		if row is None:
			return None

		return Request(*row)

	def delete(self, recipient_id: int, sender_id: int) -> bool:
		cursor = self.execute("delete", recipient_id, sender_id)
		return cursor.rowcount == 1

	def get(self, recipient_id: int, sender_id: int) -> Request | None:
		row = self.fetchone("get", recipient_id, sender_id)

		if row is None:
			return None

		return Request(*row)

	def received(self, user_id: int) -> list[Request]:
		rows = self.fetchall("received", user_id)
		return [Request(*row) for row in rows]

	def sent(self, user_id: int) -> list[Request]:
		rows = self.fetchall("sent", user_id)
		return [Request(*row) for row in rows]
