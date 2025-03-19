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
		data = self.fetchone("accept", recipient_id, sender_id)

		if data is None:
			return None

		return Request(*data)

	def accepted(self, user_id: int) -> list[Request]:
		data = self.fetchall("accepted", user_id)
		return [Request(*row) for row in data]

	def create(self, recipient_id: int, sender_id: int) -> Request | None:
		try:
			data = self.fetchone("create", recipient_id, sender_id)
		except sqlite3.IntegrityError:
			return None

		if data is None:
			return None

		return Request(*data)

	def delete(self, recipient_id: int, sender_id: int) -> bool:
		cursor = self.execute("delete", recipient_id, sender_id)
		return cursor.rowcount == 1

	def exists(self, recipient_id: int, sender_id: int) -> bool:
		data = self.fetchone("exists", recipient_id, sender_id)

		if data is None:
			return False

		return data[0] == 1

	def received(self, user_id: int) -> list[Request]:
		data = self.fetchall("received", user_id)
		return [Request(*row) for row in data]

	def sent(self, user_id: int) -> list[Request]:
		data = self.fetchall("sent", user_id)
		return [Request(*row) for row in data]
