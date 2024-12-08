import http
import typing

import database
import endpoint


class Login(endpoint.Endpoint):
	method = http.HTTPMethod.POST
	path = "accounts/login"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		username = data.get("username")
		password = data.get("password")

		user = self.database.users.get(username)

		if user is None:
			return endpoint.error("invalid username")

		if not user.verify_password(password):
			return endpoint.error("invalid password")

		token = self.database.tokens.create(user.id)

		return endpoint.success({"token": token})


class Register(endpoint.Endpoint):
	method = http.HTTPMethod.POST
	path = "accounts/register"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		username = data.get("username")
		password = data.get("password")

		if len(username) < 3 or not username.isascii() or not username.isalpha():
			return endpoint.error("invalid username")

		if len(password) < 8 or not password.isascii() or not password.isalnum():
			return endpoint.error("invalid password")

		user = self.database.users.create(username, password)

		if user is None:
			return endpoint.error("username taken")

		token = self.database.tokens.create(user)

		return endpoint.success({"token": token}, http.HTTPStatus.CREATED)


class RenameUser(endpoint.Endpoint):
	method = http.HTTPMethod.PATCH
	path = "accounts/username"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error("invalid token")

		username = data.get("username")

		if len(username) < 3 or not username.isascii() or not username.isalpha():
			return endpoint.error("invalid username")

		if not self.database.users.rename(data.user, username):
			return endpoint.error("username taken")

		return endpoint.success({})
