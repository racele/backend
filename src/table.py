import functools
import hashlib
import random
import sqlite3
import string
import typing

type FetchAll = list[tuple[typing.Any, ...]]
type FetchOne = None | tuple[typing.Any, ...]


@functools.cache
def queries(table: str) -> dict[str, str]:
	with open(f"sql/{table}.sql") as file:
		content = file.read()

	queries: dict[str, str] = {}

	for query in content.split("\n\n"):
		head, *tail = query.splitlines()
		queries[head.removeprefix("-- ")] = " ".join(tail)

	return queries


class Table:
	table: str

	def __init__(self, connection: sqlite3.Connection) -> None:
		self.connection = connection

	def execute(self, method: str, *parameters: object) -> sqlite3.Cursor:
		return self.connection.execute(queries(self.table)[method], parameters)

	@staticmethod
	def hash(input: str, salt: str) -> str:
		return hashlib.sha1((input + salt).encode()).hexdigest()

	@staticmethod
	def random(count: int) -> str:
		return "".join(random.sample(string.ascii_letters, count))
