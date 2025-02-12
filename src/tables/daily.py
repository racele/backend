import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Daily:
	created_at: str
	solution: str


class DailyTable(table.Table):
	table = "daily"

	def get(self) -> Daily | None:
		cursor = self.execute("get")
		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return Daily(*data)

	def set(self, solution: str) -> Daily | None:
		try:
			cursor = self.execute("set", solution)
		except sqlite3.IntegrityError:
			return None

		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return Daily(*data)
