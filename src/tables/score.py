import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Score:
	created_at: int
	date: str | None
	guesses: int
	solution: str
	time: int
	user_id: int


class ScoreTable(table.Table):
	table = "score"

	def create(self, date: str | None, guesses: int, solution: str, time: int, user_id: int) -> Score | None:
		try:
			row = self.fetchone("create", date, guesses, solution, time, user_id)
		except sqlite3.IntegrityError:
			return None

		if row is None:
			return None

		return Score(*row)

	def daily(self, user_id: int) -> list[Score]:
		rows = self.fetchall("daily", user_id)
		return [Score(*row) for row in rows]

	def practice(self, user_id: int) -> list[Score]:
		rows = self.fetchall("practice", user_id)
		return [Score(*row) for row in rows]
