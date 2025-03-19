import http

import database
import endpoint
import response


class DeleteSession(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.DELETE
	path = "/users/@me/sessions/{session_id}"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()

		try:
			session_id = int(context.data["session_id"])
		except ValueError:
			return response.error("Invalid session")

		deleted = context.database.sessions.delete(session_id, auth.user_id)
		return response.deleted(deleted)


class ListSessions(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/sessions"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()
		sessions = context.database.sessions.list(auth.user_id)

		return response.success(sessions)
