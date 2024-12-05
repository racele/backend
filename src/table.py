import functools
import random
import sqlite3
import string

@functools.cache
def queries(table: str) -> dict[str, str]:
	with open(f"sql/{table}.sql") as file:
		content = file.read()

	queries: dict[str, str] = {}

	for query in content.split("\n\n"):
		head, *tail = query.splitlines()
		queries[head.strip("- ")] = " ".join(tail)

	return queries

def randstr(count: int) -> str:
	return "".join(random.sample(string.ascii_letters, count))

class Table:
	name: str

	def __init__(self, connection: sqlite3.Connection) -> None:
		self.connection = connection

	def execute(self, method: str, *parameters: object) -> sqlite3.Cursor:
		return self.connection.execute(queries(self.name)[method], parameters)
