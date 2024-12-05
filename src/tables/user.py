import dataclasses
import hashlib
import table

@dataclasses.dataclass
class User:
	id: int
	password: str
	salt: str
	username: str

	def verify_password(self, password: str) -> bool:
		hash = hashlib.sha1((password + self.salt).encode()).hexdigest()
		return hash == self.password

class UserTable(table.Table):
	name = "user"

	def create(self, username: str, password: str) -> int | None:
		salt = table.randstr(10)
		hash = hashlib.sha1((password + salt).encode()).hexdigest()

		try:
			cursor = self.execute("create", hash, salt, username)
		except:
			return None
		else:
			return cursor.lastrowid

	def get(self, username: str) -> User | None:
		cursor = self.execute("get", username)
		data = cursor.fetchone()

		if data is None:
			return None

		return User(*data)

	def rename(self, user: int, username: str) -> bool:
		try:
			self.execute("rename", username, user)
		except:
			return False
		else:
			return True
