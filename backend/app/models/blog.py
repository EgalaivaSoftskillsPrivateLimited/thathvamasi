    
    """
Blog models for Thathvamasi HR Consultancy
"""

from typing import Optional, List
from datetime import date
from pydantic import Field, validator
from app.models.base import BaseDBModel
from app.utils.helpers import generate_slug


class BlogSEO(BaseDBModel):
    """
    Blog SEO metadata model
    """
    meta_title: Optional[str] = Field(None, max_length=60, description="SEO meta title (50-60 chars)")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description (150-160 chars)")
    meta_keywords: Optional[List[str]] = Field(default_factory=list, description="SEO keywords")
    og_image: Optional[str] = Field(None, description="Open Graph image URL")
    canonical_url: Optional[str] = Field(None, description="Canonical URL")


class BlogImage(BaseDBModel):
    """
    Blog image model
    """
    url: str = Field(..., description="Image URL")
    alt_text: Optional[str] = Field(None, description="Image alt text")
    caption: Optional[str] = Field(None, description="Image caption")
    width: Optional[int] = Field(None, description="Image width")
    height: Optional[int] = Field(None, description="Image height")


class BlogAuthor(BaseDBModel):
    """
    Blog author model
    """
    name: str = Field(..., min_length=2, max_length=100, description="Author name")
    email: Optional[str] = Field(None, description="Author email")
    bio: Optional[str] = Field(None, description="Author bio")
    avatar: Optional[str] = Field(None, description="Author avatar URL")


class Blog(BaseDBModel):
    """
    Complete blog model
    """
    title: str = Field(..., min_length=5, max_length=200, description="Blog title")
    slug: str = Field(..., description="URL slug (auto-generated)")
    excerpt: Optional[str] = Field(None, max_length=300, description="Short excerpt/summary")
    content: str = Field(..., description="Blog content (HTML/Markdown)")
    featured_image: Optional[BlogImage] = Field(None, description="Featured image")
    images: List[BlogImage] = Field(default_factory=list, description="Additional images")
    
    # Author information
    author: BlogAuthor
    
    # Categorization
    categories: List[str] = Field(default_factory=list, description="Blog categories")
    tags: List[str] = Field(default_factory=list, description="Blog tags")
    
    # Publication status
    is_published: bool = Field(default=False, description="Whether the blog is published")
    published_at: Optional[date] = Field(None, description="Publication date")
    is_featured: bool = Field(default=False, description="Whether the blog is featured")
    is_pinned: bool = Field(default=False, description="Whether the blog is pinned to top")
    
    # SEO
    seo: Optional[BlogSEO] = Field(None, description="SEO metadata")
    
    # Statistics
    view_count: int = Field(default=0, description="Number of views")
    share_count: int = Field(default=0, description="Number of shares")
    read_time_minutes: Optional[int] = Field(None, description="Estimated read time in minutes")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Top HR Trends in 2026",
                "slug": "top-hr-trends-in-2026",
                "excerpt": "Discover the latest HR trends shaping the future of work in 2026",
                "content": "<p>HR trends are evolving rapidly...</p>",
                "author": {
                    "name": "Thathvamasi HR",
                    "email": "content@thathvamasi.com"
                },
                "categories": ["HR Insights", "Trends"],
                "tags": ["HR Trends", "Future of Work", "2026"],
                "is_published": True,
                "published_at": "2026-10-05",
                "view_count": 150,
                "read_time_minutes": 5
            }
        }


class BlogCreate(BaseDBModel):
    """
    Model for creating a new blog
    """
    title: str = Field(..., min_length=5, max_length=200)
    excerpt: Optional[str] = Field(None, max_length=300)
    content: str = Field(...)
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    is_published: bool = Field(default=False)
    published_at: Optional[date] = None
    is_featured: bool = Field(default=False)
    is_pinned: bool = Field(default=False)
    author_name: Optional[str] = Field(None, description="Author name (defaults to logged in user)")
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    meta_keywords: Optional[List[str]] = Field(default_factory=list)
    
    @validator('slug', pre=True, always=True)
    def generate_slug_from_title(cls, v, values):
        if 'title' in values and values['title']:
            return generate_slug(values['title'])
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Top HR Trends in 2026",
                "excerpt": "Discover the latest HR trends...",
                "content": "HR trends are evolving rapidly...",
                "categories": ["HR Insights", "Trends"],
                "tags": ["HR Trends", "2026"],
                "is_published": True,
                "author_name": "Thathvamasi HR"
            }
        }


class BlogUpdate(BaseDBModel):
    """
    Model for updating a blog
    """
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    excerpt: Optional[str] = Field(None, max_length=300)
    content: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None
    published_at: Optional[date] = None
    is_featured: Optional[bool] = None
    is_pinned: Optional[bool] = None
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    meta_keywords: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Updated: Top HR Trends in 2026",
                "is_published": True,
                "meta_description": "Updated analysis of HR trends for 2026"
            }
        }


class BlogResponse(BaseDBModel):
    """
    Blog response model for API
    """
    blog: Blog
    success: bool = True
    message: Optional[str] = None


class BlogsListResponse(BaseDBModel):
    """
    List of blogs response model
    """
    blogs: List[Blog]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True


class BlogCategory(BaseDBModel):
    """
    Blog category model
    """
    name: str = Field(..., min_length=2, max_length=50, description="Category name")
    slug: str = Field(..., description="Category slug")
    description: Optional[str] = Field(None, description="Category description")
    post_count: int = Field(default=0, description="Number of posts in this category")
    is_active: bool = Field(default=True, description="Whether category is active")


class BlogTag(BaseDBModel):
    """
    Blog tag model
    """
    name: str = Field(..., min_length=2, max_length=50, description="Tag name")
    slug: str = Field(..., description="Tag slug")
    post_count: int = Field(default=0, description="Number of posts with this tag")


class BlogStats(BaseDBModel):
    """
    Blog statistics model
    """
    total_blogs: int
    published_blogs: int
    draft_blogs: int
    featured_blogs: int
    total_views: int
    total_shares: int
    categories_count: int
    tags_count: int
    avg_read_time: Optional[float] = None
    most_viewed_blog: Optional[str] = None
    most_viewed_count: Optional[int] = None


class BlogSearchResult(BaseDBModel):
    """
    Blog search result model
    """
    blogs: List[Blog]
    total: int
    query: Optional[str] = None
    filters: Optional[dict] = None
    success: bool = True