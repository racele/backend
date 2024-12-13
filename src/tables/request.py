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

	def accept(self, recipient_id: int, sender_id: int) -> bool:
		cursor = self.execute("accept", recipient_id, sender_id)
		return cursor.rowcount == 1

	def accepted(self, user_id: int) -> list[Request]:
		cursor = self.execute("accepted", user_id)
		data: table.FetchAll = cursor.fetchall()

		return [Request(*row) for row in data]

	def create(self, recipient_id: int, sender_id: int) -> Request | None:
		try:
			cursor = self.execute("create", recipient_id, sender_id)
		except sqlite3.IntegrityError:
			return None

		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return Request(*data)

	def delete(self, recipient_id: int, sender_id: int) -> bool:
		cursor = self.execute("delete", recipient_id, sender_id)
		return cursor.rowcount == 1

	def exists(self, recipient_id: int, sender_id: int) -> bool:
		cursor = self.execute("exists", recipient_id, sender_id)
		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return False

		return data[0] == 1

	def received(self, user_id: int) -> list[Request]:
		cursor = self.execute("received", user_id)
		data: table.FetchAll = cursor.fetchall()

		return [Request(*row) for row in data]

	def sent(self, user_id: int) -> list[Request]:
		cursor = self.execute("sent", user_id)
		data: table.FetchAll = cursor.fetchall()

		return [Request(*row) for row in data]
