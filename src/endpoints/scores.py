import http

import database
import endpoint
import response


class CreateScore(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.POST
	path = "/users/@me/scores"
	query = ["date?", "guesses", "solution", "time"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		user_id = context.get_user_id()

		date = context.data.get("date")
		solution = context.data["solution"]

		try:
			guesses = int(context.data["guesses"])
		except ValueError:
			return response.error("Invalid guesses")

		try:
			time = int(context.data["time"])
		except ValueError:
			return response.error("Invalid time")

		score = context.database.scores.create(date, guesses, solution, time, user_id)

		if score is None:
			return response.error("Score already exists for this date")

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
