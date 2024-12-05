import table

class TokenTable(table.Table):
	name = "token"

	def create(self, user: int) -> str:
		while True:
			token = table.randstr(20)

			try:
				self.execute("create", token, user)
			except:
				continue
			else:
				return token

	def resolve(self, token: str) -> int | None:
		cursor = self.execute("resolve", token)
		data = cursor.fetchone()

		if data is None:
			return None

		return data[0]
