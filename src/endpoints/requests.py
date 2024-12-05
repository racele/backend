import database
import endpoint
import typing

class AcceptRequest(endpoint.Endpoint):
	method = endpoint.Method.Post
	path = "requests/accept"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error(400, "invalid token")

		try:
			sender = int(data.get("sender"))
		except:
			return endpoint.error(400, "invalid sender")

		if not self.database.requests.accept(data.user, sender):
			return endpoint.error(400, "accepting the request failed")

		return endpoint.Result(200, {})

class CreateRequest(endpoint.Endpoint):
	method = endpoint.Method.Post
	path = "requests/create"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error(400, "invalid token")

		try:
			recipient = int(data.get("recipient"))
		except:
			return endpoint.error(400, "invalid recipient")

		if not self.database.requests.create(recipient, data.user):
			return endpoint.error(400, "creating the request failed")

		return endpoint.Result(200, {})

class DeclineRequest(endpoint.Endpoint):
	method = endpoint.Method.Post
	path = "requests/decline"

	@typing.override
	def run(self, data: database.RequestData) -> endpoint.Result:
		if data.user is None:
			return endpoint.error(400, "invalid token")

		try:
			sender = int(data.get("sender"))
		except:
			return endpoint.error(400, "invalid sender")

		if not self.database.requests.decline(data.user, sender):
			return endpoint.error(400, "declining the request failed")

		return endpoint.Result(200, {})
