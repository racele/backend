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
		auth = context.get_auth()

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

		score = context.database.scores.create(date, guesses, solution, time, auth.user_id)

		if score is None:
			return response.error("Score already exists for this date")

		return response.success(score, http.HTTPStatus.CREATED)


class ListScores(endpoint.Endpoint):
	auth = True
	method = http.HTTPMethod.GET
	path = "/users/@me/scores"
	query = ["mode"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		auth = context.get_auth()
		mode = context.data["mode"]

		match mode:
			case "daily":
				scores = context.database.scores.daily(auth.user_id)
			case "practice":
				scores = context.database.scores.practice(auth.user_id)
			case _:
				return response.error("Invalid mode")

		return response.success(scores)
