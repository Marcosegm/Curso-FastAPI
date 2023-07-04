from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credenciales)
        if data["email"] != "admin":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")


class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field( min_length= 5, max_length=15)
    overview: str = Field( min_length= 15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                'id': 1,
                'title': 'Mi pelicula',
                'overview': "Descripcion de la pelicula",
                'year': 2022,
                'rating': 9.8,
                'category': 'Acción'  
            }
        }

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

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)

@app.get("/movies/{id}",tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404,content=[])


@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item["category"] == category]
    return JSONResponse(content=data)

@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie( movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la películla"}, status_code=201)

@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int , movie: Movie ) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Se ha modificado la películla"}, status_code=200)

@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha eliminado la películla"}, status_code=200)
