import database
import endpoint
import typing

class Login(endpoint.Endpoint):
	method = endpoint.Method.Post
	path = "accounts/login"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		username = data.get("username")
		password = data.get("password")

		user = self.database.users.get(username)

		if user is None:
			return endpoint.error(400, "invalid username")

		if not user.verify_password(password):
			return endpoint.error(400, "invalid password")

		token = self.database.tokens.create(user.id)

		return endpoint.Result(200, {"token": token})

class Register(endpoint.Endpoint):
	method = endpoint.Method.Post
	path = "accounts/register"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		username = data.get("username")
		password = data.get("password")

		if len(username) < 3 or not username.isascii() or not username.isalpha():
			return endpoint.error(400, "invalid username")

		if len(password) < 8 or not password.isascii() or not password.isalnum():
			return endpoint.error(400, "invalid password")

		user = self.database.users.create(username, password)

		if user is None:
			return endpoint.error(400, "username taken")

		token = self.database.tokens.create(user)

		return endpoint.Result(200, {"token": token})

class RenameUser(endpoint.Endpoint):
	method = endpoint.Method.Patch
	path = "accounts/username"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error(400, "invalid token")

		username = data.get("username")

		if len(username) < 3 or not username.isascii() or not username.isalpha():
			return endpoint.error(400, "invalid username")

		if not self.database.users.rename(data.user, username):
			return endpoint.error(400, "username taken")

		return endpoint.Result(200, {})
