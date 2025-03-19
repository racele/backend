import http

import database
import endpoint
import response


class AuthorizeUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.POST
	path = "/users/authorize"
	query = ["password", "username"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		password = context.data["password"]
		username = context.data["username"]

		access = context.database.users.access(username)

		if access is None:
			return response.error("Invalid username")

		if not access.verify(password):
			return response.error("Invalid password")

		auth = context.database.sessions.create(access.user_id)

		return response.success(auth)


class CreateUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.POST
	path = "/users"
	query = ["password", "username"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		password = context.data["password"]
		username = context.data["username"]

		if not context.database.users.verify_username(username):
			return response.error("Invalid username")

		if not context.database.users.verify_password(password):
			return response.error("Invalid password")

		user = context.database.users.create(password, username)

		if user is None:
			return response.error("Username is already taken")

		return response.success(user, http.HTTPStatus.CREATED)


class GetUser(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/users/{user_id}"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		try:
			user_id = int(context.data["user_id"])
		except ValueError:
			return response.error("Invalid user")

		user = context.database.users.get(user_id)

		if user is None:
			return response.error("Invalid user")

		return response.success(user)


class SearchUsers(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/users"
	query = ["query"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		query = context.data["query"]
		users = context.database.users.search(query)

		return response.success(users)


class UpdateUser(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.PATCH
	path = "/users/@me"
	query = ["password?", "username?"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()

		password = context.data.get("password")
		username = context.data.get("username")

		if username is not None and not context.database.users.verify_username(username):
			return response.error("Invalid username")

		if password is not None and not context.database.users.verify_password(password):
			return response.error("Invalid password")

		user = context.database.users.update(password, auth.user_id, username)

		if user is None:
			return response.error("Username is already taken")

		if password is not None:
			context.database.sessions.clear(auth.token, auth.user_id)

		return response.success(user)
