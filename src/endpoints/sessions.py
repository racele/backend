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
		user_id = context.get_user_id()

		try:
			session_id = int(context.data["session_id"])
		except ValueError:
			return response.error("invalid session")

		deleted = context.database.sessions.delete(session_id, user_id)
		return response.success({"deleted": deleted})


class ListSessions(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/sessions"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()
		sessions = context.database.sessions.list(user_id)

		return response.success(sessions)
