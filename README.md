JavaCode Test Task

This repository contains a Python application that implements a REST API for managing wallets. The API supports the following operations:

* Create a new wallet
* Get the balance of a wallet
* Deposit money into a wallet
* Withdraw money from a wallet

The application uses the FastAPI framework and a PostgreSQL database.

The application is designed to handle a high volume of requests (1000 RPS per wallet) in a concurrent environment. All requests are handled gracefully, and no request should go unhandled (50X error). The response format is maintained for inherently invalid requests, such as when the wallet does not exist, invalid JSON is provided, or there are insufficient funds.

The application runs in a Docker container, and the database also runs in a Docker container. The entire system can be brought up using Docker Compose. The application and database parameters can be configured without rebuilding the containers.

All endpoints are covered by tests.

How to run the application:

shell

docker-compose up --build

How to use the API:

* GET api/v1/wallets/: Get a list of all wallets.
* POST api/v1/wallets/: Create a new wallet.
* POST api/v1/wallets/{wallet_uuid}/operation: Deposit or withdraw money from a wallet.

Note: The wallet_uuid in the URL path is the UUID of the wallet.

Endpoints:

* GET api/v1/wallets: Get a list of all wallets.
* POST api/v1/wallets: Create a new wallet.
* GET api/v1/wallets/{wallet_uuid}: Get the balance of a wallet.
* POST api/v1/wallets/{wallet_uuid}/operation: Deposit or withdraw money from a wallet.

Request body for POST api/v1/wallets/{wallet_uuid}/operation:

JSON

{
  "operationType": "DEPOSIT" or "WITHDRAW",
  "amount": 1000
}
