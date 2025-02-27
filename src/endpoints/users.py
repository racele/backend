import http
import typing

import database
import endpoint
import response


class AuthorizeUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.POST
	path = "/users/authorize"
	query = ["password", "username"]

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		password = context.data["password"]
		username = context.data["username"]

		auth = context.database.users.auth(username)

		if auth is None:
			return response.error("invalid username")

		if not auth.verify(password):
			return response.error("invalid password")

		token = context.database.sessions.create(auth.id)

		return response.success({"token": token})


class CreateUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.POST
	path = "/users"
	query = ["password", "username"]

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		password = context.data["password"]
		username = context.data["username"]

		if not context.database.users.verify_username(username):
			return response.error("invalid username")

		if not context.database.users.verify_password(password):
			return response.error("invalid password")

		user = context.database.users.create(username, password)

		if user is None:
			return response.error("username is already taken")

		return response.success(user, http.HTTPStatus.CREATED)


class GetSelf(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()

		user = context.database.users.get(user_id)

		if user is None:
			return response.error("invalid user")

		return response.success(user)


class GetUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/users/{user_id}"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		try:
			user_id = int(context.data["user_id"])
		except ValueError:
			return response.error("invalid user")

		user = context.database.users.get(user_id)

		if user is None:
			return response.error("invalid user")

		return response.success(user)


class SearchUsers(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/users"
	query = ["query"]

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		query = context.data["query"]
		users = context.database.users.search(query)

		return response.success(users)


class UpdateSelf(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.PATCH
	path = "/users/@me"
	query = ["password?", "username?"]

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		token = context.get_token()
		user_id = context.get_user_id()

		password = context.data.get("password")
		username = context.data.get("username")

		if username is not None and not context.database.users.verify_username(username):
			return response.error("invalid username")

		if password is not None and not context.database.users.verify_password(password):
			return response.error("invalid password")

		user = context.database.users.update(user_id, username, password)

		if user is None:
			return response.error("username is already taken")

		if password is not None:
			context.database.sessions.clear(user_id, token)

		return response.success(user)
