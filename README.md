Good day, dear applicant. This task is aimed at assessing your actual level in Python development, so please treat it as if you were working on a project. Complete it honestly and showcase your skills to the maximum. Good luck!

Write an application that accepts a REST request of the following type:
POST api/v1/wallets/<WALLETUUID>/operation
{
  operationType: DEPOSIT or WITHDRAW,
  amount: 1000
}
Then, implement the logic to update the balance in the database. There should also be a way to retrieve the wallet balance:
GET api/v1/wallets/{WALLETUUID}
Stack:(FastAPI / Flask / Django) & PostgreSQL
Migrations for the database should be created using Liquibase (optional).
Pay special attention to issues when working in a concurrent environment (1000 RPS per wallet). No request should go unhandled (50X error).
Ensure that the response format is maintained for inherently invalid requests, such as when the wallet does not exist, invalid JSON is provided, or there are insufficient funds.
The application should run in a Docker container, and the database should too. The entire system should be brought up using Docker Compose.
Provide the ability to configure various application and database parameters without rebuilding the containers.
Endpoints should be covered by tests.
Upload the completed task to GitHub and provide the link.
Address any questions regarding the task independently, at your discretion.

// docker-compose up --build
