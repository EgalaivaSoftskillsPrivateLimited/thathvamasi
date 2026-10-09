"""
Blogs API endpoints for Thathvamasi HR Consultancy
"""

from typing import Optional, List
import uuid
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.models.blog_model import Blog

router = APIRouter(tags=["blogs"])


class BlogCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    category: Optional[str] = Field("Talent Acquisition", max_length=100)
    author: Optional[str] = Field("THC Executive Desk", max_length=100)
    read_time: Optional[str] = Field("4 min read", max_length=50)
    excerpt: str = Field(..., min_length=10)
    content: str = Field(..., min_length=10)
    image: Optional[str] = Field("/images/team/thc_leadership.jpg")


@router.get("/")
async def list_blogs(
    db: AsyncSession = Depends(get_db)
):
    """
    List HR market insights and thought leadership articles
    """
    try:
        stmt = select(Blog).order_by(desc(Blog.created_at)).limit(50)
        res = await db.execute(stmt)
        blogs = res.scalars().all()

        if not blogs:
            # Return seeded defaults if database has no articles yet
            return {
                "success": True,
                "count": 0,
                "data": []
            }

        output = []
        for b in blogs:
            output.append({
                "id": str(b.id),
                "title": b.title,
                "slug": b.slug,
                "excerpt": b.excerpt,
                "content": b.content,
                "author": b.author_name,
                "categories": b.categories,
                "readTime": f"{b.read_time_minutes or 4} min read",
                "date": b.created_at.strftime("%b %d, %Y") if b.created_at else "",
                "image": b.og_image_url or "/images/team/thc_leadership.jpg"
            })

        return {
            "success": True,
            "count": len(output),
            "data": output
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blog posts: {str(e)}"
        )


@router.post("/")
async def create_blog(
    data: BlogCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new HR article from the Command Center
    """
    try:
        slug = data.title.lower().replace(" ", "-").replace("/", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-") + f"-{str(uuid.uuid4())[:6]}"

        blog = Blog(
            title=data.title.strip(),
            slug=slug,
            excerpt=data.excerpt.strip(),
            content=data.content.strip(),
            author_name=data.author.strip() if data.author else "THC Editorial Desk",
            categories=[data.category] if data.category else ["Executive Search"],
            is_published=True,
            read_time_minutes=4,
            og_image_url=data.image
        )
        db.add(blog)
        await db.commit()
        await db.refresh(blog)

        return {
            "success": True,
            "message": "Article published successfully",
            "data": {
                "id": str(blog.id),
                "title": blog.title,
                "slug": blog.slug,
                "author": blog.author_name,
                "date": blog.created_at.strftime("%b %d, %Y") if blog.created_at else ""
            }
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish article: {str(e)}"
        )