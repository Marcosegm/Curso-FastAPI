from fastapi import  FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.security import HTTPBearer
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)



class User(BaseModel):
    email: str
    password: str


   

# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'  
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'  
    }
]

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("   <h1>hola mundo </h1>   ")

@app.post("/login", tags=["auth"])
def login(user: User):
    if (user.email == "admin" and user.password == "admin"):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200 ,content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})

