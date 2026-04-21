from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from app.models.user import User

router = APIRouter()

# 1. PUBLIC: Get all blogs
@router.get("/", response_model=List[BlogResponse])
def get_blogs(db: Session = Depends(deps.get_db), category: str = None):
    query = db.query(Blog)
    if category and category != "All":
        query = query.filter(Blog.category == category)
    return query.order_by(Blog.created_at.desc()).all()

# 2. ADMIN ONLY: Post a new blog (With Permission Check)
@router.post("/", response_model=BlogResponse)
def create_blog(
    blog_in: BlogCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    # --- PERMISSION CHECK ---
    if not current_user.can_post_blog:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account does not have permission to post blogs. Contact Root Admin."
        )

    # Combine names for the blog display
    full_name = f"{current_user.first_name} {current_user.last_name}"
    
    new_blog = Blog(
        **blog_in.model_dump(), 
        author_id=current_user.id, 
        author_name=full_name
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# 3. ADMIN ONLY: Update/Edit blog (With Permission Check)
@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int, 
    blog_in: BlogUpdate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    # --- PERMISSION CHECK ---
    if not current_user.can_edit_blog:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account does not have permission to edit blogs."
        )

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Optional: Only allow the original author OR a Super Admin to edit
    if blog.author_id != current_user.id and current_user.email != "admin@wysele.com":
         raise HTTPException(status_code=403, detail="You can only edit your own blogs.")

    update_data = blog_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(blog, field, value)
    
    db.commit()
    db.refresh(blog)
    return blog

# 4. ADMIN ONLY: Delete blog (Usually Root or Author only)
@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin)
):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Safety: Only the author or the Root Super Admin can delete
    if blog.author_id != current_user.id and current_user.email != "admin@wysele.com":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this blog.")

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}