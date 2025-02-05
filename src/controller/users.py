from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

# @router.post("/register")
# async def register(user: UserRegister, db: Session = Depends(get_db)):
#     hashed_password = pwd_context.hash(user.password)
#     db_user = User(username=user.username, password_hash=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "User registered successfully"}

# @router.post("/login")
# async def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     return {"message": "Login successful"}
