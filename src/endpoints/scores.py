import http

import database
import endpoint
import response


class CreateScore(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.POST
	path = "/users/@me/scores"
	query = ["attempts", "date?", "time"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		date = context.data.get("date")
		user_id = context.get_user_id()

		try:
			attempts = int(context.data["attempts"])
		except ValueError:
			return response.error("invalid attempts")

		try:
			time = int(context.data["time"])
		except ValueError:
			return response.error("invalid time")

		score = context.database.scores.create(attempts, date, time, user_id)

		if score is None:
			return response.error("score already exists for this date")

		return response.success(score, http.HTTPStatus.CREATED)


class ListDaily(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/scores/daily"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()
		scores = context.database.scores.daily(user_id)

		return response.success(scores)


class ListPractice(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/scores/practice"
	query = []

	@staticmethod
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()
		scores = context.database.scores.practice(user_id)

		return response.success(scores)
