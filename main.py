import starlette.status as status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core import SQLModel, engine, settings
from routes import auth, artisan

# init fastapi server
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
)

# routes
app.include_router(
    router=auth,
    prefix=settings.API_V1_STR,
)
app.include_router(
    router=artisan,
    prefix=settings.API_V1_STR,
)

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# redirect to docs on hitting root endpoint
@app.get(path="/", status_code=302)
async def root():
    """
    Redirects incoming GET requests to the API documentation page.
    """

    # Redirecting to the API documentation page using a 302 status code
    return RedirectResponse(
        url="/redoc",
        status_code=status.HTTP_302_FOUND,
    )


def main():
    import uvicorn

    # start db engine
    SQLModel.metadata.create_all(engine)

    # run application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# run script
if __name__ == "__main__":
    main()
