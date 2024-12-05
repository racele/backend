import table

class RequestTable(table.Table):
	name = "request"

	def accept(self, recipient: int, sender: int) -> bool:
		cursor = self.execute("accept", recipient, sender)
		return cursor.rowcount == 1

	def create(self, recipient: int, sender: int) -> bool:
		if self.exists(recipient, sender):
			return False

		try:
			self.execute("create", recipient, sender)
		except:
			return False
		else:
			return True

	def decline(self, recipient: int, sender: int) -> bool:
		cursor = self.execute("decline", recipient, sender)
		return cursor.rowcount == 1

	def exists(self, recipient: int, sender: int) -> bool:
		cursor = self.execute("exists", recipient, sender)
		return cursor.fetchone()[0] == 1
