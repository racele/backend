import sys

import server


def main() -> None:
	try:
		port = int(sys.argv[1])
	except IndexError:
		port = 3000
	except ValueError:
		sys.exit("port is not an integer")

	try:
		app = server.Server(port)
	except OverflowError:
		sys.exit("port is out of range")

	app.serve_forever()


if __name__ == "__main__":
	main()
