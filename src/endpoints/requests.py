import http
import typing

import database
import endpoint


class AcceptRequest(endpoint.Endpoint):
	method = http.HTTPMethod.POST
	path = "requests/accept"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error("invalid token", http.HTTPStatus.UNAUTHORIZED)

		try:
			sender = int(data.get("sender"))
		except Exception:
			return endpoint.error("invalid sender")

		if not self.database.requests.accept(data.user, sender):
			return endpoint.error("accepting the request failed")

		return endpoint.success({})


class CreateRequest(endpoint.Endpoint):
	method = http.HTTPMethod.POST
	path = "requests/create"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error("invalid token", http.HTTPStatus.UNAUTHORIZED)

		try:
			recipient = int(data.get("recipient"))
		except Exception:
			return endpoint.error("invalid recipient")

		if not self.database.requests.create(recipient, data.user):
			return endpoint.error("creating the request failed")

		return endpoint.success({}, http.HTTPStatus.CREATED)


class DeclineRequest(endpoint.Endpoint):
	method = http.HTTPMethod.POST
	path = "requests/decline"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error("invalid token", http.HTTPStatus.UNAUTHORIZED)

		try:
			sender = int(data.get("sender"))
		except Exception:
			return endpoint.error("invalid sender")

		if not self.database.requests.decline(data.user, sender):
			return endpoint.error("declining the request failed")

		return endpoint.success({})
