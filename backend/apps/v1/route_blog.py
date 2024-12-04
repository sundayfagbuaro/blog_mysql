from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import  Jinja2Templates
from fastapi import Depends
from db.repository.blog import list_blogs, retrieve_blog
from sqlalchemy.orm import Session
from db.session import get_db
from typing import Optional

# Initialize and create an instance of Jinja2Templates
templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def home(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    print(dir(request))
    return templates.TemplateResponse("blogs/home.html",{"request": request, "blogs": blogs, "alert": alert})

@router.get("/app/blog/{id}")
def blog_details(request: Request, id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    context = {"request": request, "blog": blog}
    return templates.TemplateResponse("blogs/details.html", context=context)