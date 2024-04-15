import starlette.status as status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core import settings
from routes import users

# init fastapi server
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0",
)

# routes
app.include_router(
    router=users,
    prefix=settings.API_V1_STR,
)

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
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
        url="/docs",
        status_code=status.HTTP_302_FOUND,
    )


# run script
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
