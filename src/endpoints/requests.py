import http
import typing

import database
import endpoint
import response


class AcceptRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.PUT
	path = "/users/@me/requests/{sender_id}/accept"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		recipient_id = context.get_user_id()

		try:
			sender_id = int(context.data["sender_id"])
		except ValueError:
			return response.error("invalid sender")

		accepted = context.database.requests.accept(recipient_id, sender_id)
		return response.success({"accepted": accepted})


class CreateRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.POST
	path = "/users/@me/requests"
	query = ["recipient_id"]

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		sender_id = context.get_user_id()

		try:
			recipient_id = int(context.data["recipient_id"])
		except ValueError:
			return response.error("invalid recipient")

		if recipient_id == sender_id:
			return response.error("cannot send a request to yourself")

		if context.database.requests.exists(recipient_id, sender_id):
			return response.error("request already exists")

		request = context.database.requests.create(recipient_id, sender_id)

		if request is None:
			return response.error("invalid recipient")

		return response.success(vars(request), http.HTTPStatus.CREATED)


class DeleteRequest(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.DELETE
	path = "/users/@me/requests/{user_id}"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		own_id = context.get_user_id()

		try:
			user_id = int(context.data["user_id"])
		except ValueError:
			return response.error("invalid user")

		deleted = context.database.requests.delete(own_id, user_id)
		return response.success({"deleted": deleted})


class GetAccepted(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/requests/accepted"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()

		requests = context.database.requests.accepted(user_id)
		dicts = [vars(request) for request in requests]

		return response.success(dicts)


class GetReceived(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/requests/received"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()

		requests = context.database.requests.received(user_id)
		dicts = [vars(request) for request in requests]

		return response.success(dicts)


class GetSent(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/requests/sent"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()

		requests = context.database.requests.sent(user_id)
		dicts = [vars(request) for request in requests]

		return response.success(dicts)
