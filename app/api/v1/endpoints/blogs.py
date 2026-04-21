from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from urllib.parse import urlparse
from app.api import deps
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from app.models.user import User

router = APIRouter()

BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"}

def validate_image_url(url: Optional[str]):
    if not url:
        return
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Invalid image URL scheme.")
    if parsed.hostname in BLOCKED_HOSTS:
        raise HTTPException(status_code=400, detail="Invalid image URL host.")

# 1. PUBLIC: Get all blogs
@router.get("/", response_model=List[BlogResponse])
def get_blogs(db: Session = Depends(deps.get_db), category: str = None):
    query = db.query(Blog)
    if category and category != "All":
        query = query.filter(Blog.category == category)
    return query.order_by(Blog.created_at.desc()).all()

# 2. PUBLIC: Get single blog
@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(deps.get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# 3. ADMIN ONLY: Post a new blog
@router.post("/", response_model=BlogResponse)
def create_blog(
    blog_in: BlogCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    if not current_user.can_post_blog:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission to post blogs.")

    validate_image_url(blog_in.image_url)

    new_blog = Blog(
        **blog_in.model_dump(),
        author_id=current_user.id,
        author_name=f"{current_user.first_name} {current_user.last_name}"
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# 4. ADMIN ONLY: Update blog (author or SUPER_ADMIN)
@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int,
    blog_in: BlogUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    if not current_user.can_edit_blog:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission to edit blogs.")

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # A01: ownership check — only author or SUPER_ADMIN can edit
    if blog.author_id != current_user.id and current_user.role != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="You can only edit your own blogs.")

    if blog_in.image_url:
        validate_image_url(blog_in.image_url)

    for field, value in blog_in.model_dump(exclude_unset=True).items():
        setattr(blog, field, value)

    db.commit()
    db.refresh(blog)
    return blog

# 5. ADMIN ONLY: Delete blog (author or SUPER_ADMIN)
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # A01: ownership check — only author or SUPER_ADMIN can delete
    if blog.author_id != current_user.id and current_user.role != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this blog.")

    db.delete(blog)
    db.commit()
