import logging

import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.schema import schema

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Create the FastAPI app
app = FastAPI()

# Include the GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def read_root():
    return {"message": "Welcome to the GraphQL API. Go to /graphql to verify."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
