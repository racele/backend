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
		data = self.fetchone("auth", username)

		if data is None:
			return None

		return Auth(*data)

	def create(self, username: str, password: str) -> User | None:
		salt = self.random(10)
		hash = self.hash(password, salt)

		try:
			data = self.fetchone("create", hash, salt, username)
		except sqlite3.IntegrityError:
			return None

		if data is None:
			return None

		return User(*data)

	def get(self, user_id: int) -> User | None:
		data = self.fetchone("get", user_id)

		if data is None:
			return None

		return User(*data)

	def search(self, query: str) -> list[User]:
		data = self.fetchall("search", query)
		return [User(*row) for row in data]

	def update(self, user_id: int, username: str | None, password: str | None) -> User | None:
		if password is None:
			salt = None
			hash = None
		else:
			salt = self.random(10)
			hash = self.hash(password, salt)

		try:
			data = self.fetchone("update", hash, salt, username, user_id)
		except sqlite3.IntegrityError:
			return None

		if data is None:
			return None

		return User(*data)

	@staticmethod
	def verify_password(password: str) -> bool:
		return len(password) >= 8 and password.isascii() and password.isalnum()

	@staticmethod
	def verify_username(username: str) -> bool:
		return len(username) >= 3 and username.isascii() and username.isalpha()
