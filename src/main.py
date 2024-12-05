import server
import sys

def main() -> None:
	try:
		port = int(sys.argv[1])
	except:
		port = 3000

	app = server.Server(port)
	app.serve_forever()

if __name__ == "__main__":
	main()
