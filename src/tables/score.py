import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Score:
	date: str | None
	guesses: int
	solution: str
	time: int
	user_id: int


class ScoreTable(table.Table):
	table = "score"

	def create(self, date: str | None, guesses: int, solution: str, time: int, user_id: int) -> Score | None:
		try:
			data = self.fetchone("create", date, guesses, solution, time, user_id)
		except sqlite3.IntegrityError:
			return None

		if data is None:
			return None

		return Score(*data)

	def daily(self, user_id: int) -> list[Score]:
		data = self.fetchall("daily", user_id)
		return [Score(*row) for row in data]

	def practice(self, user_id: int) -> list[Score]:
		data = self.fetchall("practice", user_id)
		return [Score(*row) for row in data]
