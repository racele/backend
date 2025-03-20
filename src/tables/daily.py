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
		row = self.fetchone("get", language)

		if row is None:
			return None

		return Daily(*row)

	def set(self, language: str, solution: str) -> Daily | None:
		try:
			row = self.fetchone("set", language, solution)
		except sqlite3.IntegrityError:
			return None

		if row is None:
			return None

		return Daily(*row)
