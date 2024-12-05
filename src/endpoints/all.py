import endpoint
import endpoints.accounts
import endpoints.requests

all: list[type[endpoint.Endpoint]] = [
	endpoints.accounts.Login,
	endpoints.accounts.Register,
	endpoints.accounts.RenameUser,
	endpoints.requests.AcceptRequest,
	endpoints.requests.CreateRequest,
	endpoints.requests.DeclineRequest,
]
