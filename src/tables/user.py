import dataclasses
import sqlite3

import table


@dataclasses.dataclass
class Auth:
	id: int
	password: str
	salt: str

	def verify(self, password: str) -> bool:
		hash = table.Table.hash(password, self.salt)
		return hash == self.password


@dataclasses.dataclass
class User:
	created_at: int
	id: int
	username: str


class UserTable(table.Table):
	table = "user"

	def auth(self, username: str) -> Auth | None:
		cursor = self.execute("auth", username)
		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return Auth(*data)

	def create(self, username: str, password: str) -> User | None:
		salt = self.random(10)
		hash = self.hash(password, salt)

		try:
			cursor = self.execute("create", hash, salt, username)
		except sqlite3.IntegrityError:
			return None

		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return User(*data)

	def get(self, user_id: int) -> User | None:
		cursor = self.execute("get", user_id)
		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return User(*data)

	def search(self, query: str) -> list[User]:
		cursor = self.execute("search", query)
		data: table.FetchAll = cursor.fetchall()

		return [User(*row) for row in data]

	def update(self, user_id: int, username: str | None, password: str | None) -> User | None:
		if password is None:
			salt = None
			hash = None
		else:
			salt = self.random(10)
			hash = self.hash(password, salt)

		try:
			cursor = self.execute("update", hash, salt, username, user_id)
		except sqlite3.IntegrityError:
			return None

		data: table.FetchOne = cursor.fetchone()

		if data is None:
			return None

		return User(*data)

	@staticmethod
	def verify_password(password: str) -> bool:
		return len(password) >= 8 and password.isascii() and password.isalnum()

	@staticmethod
	def verify_username(username: str) -> bool:
		return len(username) >= 3 and username.isascii() and username.isalpha()
