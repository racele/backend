import http

import database
import endpoint
import response


class AcceptRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.PUT
	path = "/users/@me/requests/{sender_id}/accept"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()

		try:
			sender_id = int(context.data["sender_id"])
		except ValueError:
			return response.error("Invalid sender")

		request = context.database.requests.accept(auth.user_id, sender_id)

		if request is None:
			return response.error("Invalid sender")

		return response.success(request)


class CreateRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.POST
	path = "/users/@me/requests"
	query = ["recipient_id"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()

		try:
			recipient_id = int(context.data["recipient_id"])
		except ValueError:
			return response.error("Invalid recipient")

		if recipient_id == auth.user_id:
			return response.error("Cannot send a request to yourself")

		if context.database.requests.exists(recipient_id, auth.user_id):
			return response.error("Request already exists")

		request = context.database.requests.create(recipient_id, auth.user_id)

		if request is None:
			return response.error("Invalid recipient")

		return response.success(request, http.HTTPStatus.CREATED)


class DeleteRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.DELETE
	path = "/users/@me/requests/{user_id}"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()

		try:
			user_id = int(context.data["user_id"])
		except ValueError:
			return response.error("Invalid user")

		deleted = context.database.requests.delete(auth.user_id, user_id)
		return response.deleted(deleted)


class ListRequests(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/requests"
	query = ["status"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()
		status = context.data["status"]

		match status:
			case "accepted":
				requests = context.database.requests.accepted(auth.user_id)
			case "received":
				requests = context.database.requests.received(auth.user_id)
			case "sent":
				requests = context.database.requests.sent(auth.user_id)
			case _:
				return response.error("Invalid status")

		return response.success(requests)
