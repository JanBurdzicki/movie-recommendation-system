from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from model.utils import get_db
from model.utils import User
from model.utils import get_current_user, set_current_user

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/me", response_class=HTMLResponse)
async def read_user_me(request: Request):
    user_id = get_current_user()
    return templates.TemplateResponse("user_me.html", {"request": request, "user_id": user_id})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail=f"Username '{username}' already taken")

    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User '{username}' registered successfully"}

    # return templates.TemplateResponse("register_success.html", {"request": request, "user": user})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not pwd_context.verify(password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        # return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    set_current_user(db_user.id)

    return {"message": "Login successful"}
    # return templates.TemplateResponse("dashboard.html", {"request": request, "user": db_user})
