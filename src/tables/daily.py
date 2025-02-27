import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Daily:
	date: str
	language: str
	solution: str


class DailyTable(table.Table):
	table = "daily"

	def get(self, language: str) -> Daily | None:
		data = self.fetchone("get", language)

		if data is None:
			return None

		return Daily(*data)

	def set(self, language: str, solution: str) -> Daily | None:
		try:
			data = self.fetchone("set", language, solution)
		except sqlite3.IntegrityError:
			return None

		if data is None:
			return None

		return Daily(*data)
