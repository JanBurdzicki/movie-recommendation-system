# @app.get("/movies/{movie_id}")
# def get_movie(movie_id: int, db: Session = Depends(get_db)):
#     movie = db.query(Movie).filter(Movie.id == movie_id).first()
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return movie

# @app.get("/movies/search")
# def search_movies(query: str, db: Session = Depends(get_db)):
#     movies = db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).all()
#     return movies