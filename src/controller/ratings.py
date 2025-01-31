@app.post("/ratings")
def add_rating(rating: RatingSchema, db: Session = Depends(get_db)):
    new_rating = Rating(user_id=1, movie_id=rating.movie_id, rating=rating.rating)  # TODO: replace with authenticated user
    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}

@app.get("/ratings/user")
def get_user_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == 1).all()  # TODO: replace with authenticated user
    return ratings