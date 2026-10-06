"""
SQLAlchemy Blog models for Thathvamasi HR Consultancy
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text, ARRAY, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Blog(Base):
    """
    Blog post model
    """
    __tablename__ = "blogs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    
    # Author information
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    author_name = Column(String(255), nullable=False)
    author_bio = Column(Text, nullable=True)
    author_avatar = Column(String(500), nullable=True)
    
    # Categorization
    categories = Column(ARRAY(String), default=[], nullable=False)
    tags = Column(ARRAY(String), default=[], nullable=False)
    
    # Publication status
    is_published = Column(Boolean, default=False, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_keywords = Column(ARRAY(String), default=[], nullable=False)
    og_image_url = Column(String(500), nullable=True)
    canonical_url = Column(String(500), nullable=True)
    
    # Statistics
    view_count = Column(Integer, default=0, nullable=False)
    share_count = Column(Integer, default=0, nullable=False)
    comment_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    read_time_minutes = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    images = relationship("BlogImage", back_populates="blog", cascade="all, delete-orphan")
    comments = relationship("BlogComment", back_populates="blog", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_blogs_slug', 'slug', unique=True),
        Index('ix_blogs_is_published', 'is_published'),
        Index('ix_blogs_published_at', 'published_at'),
        Index('ix_blogs_is_featured', 'is_featured'),
        Index('ix_blogs_categories', 'categories', postgresql_using='gin'),
        Index('ix_blogs_tags', 'tags', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title[:50]}..., published={self.is_published})>"


class BlogImage(Base):
    """
    Blog image model
    """
    __tablename__ = "blog_images"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    
    # Image information
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_type = Column(String(50), nullable=False)  # jpg, png, gif, webp
    
    # Image properties
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    cloudinary_id = Column(String(255), nullable=True)
    
    # SEO and accessibility
    alt_text = Column(String(255), nullable=True)
    caption = Column(String(500), nullable=True)
    
    # Display properties
    is_featured = Column(Boolean, default=False, nullable=False)
    position = Column(Integer, default=0, nullable=False)  # For ordering images
    
    # Upload information
    uploaded_by = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    blog = relationship("Blog", back_populates="images")
    
    # Indexes
    __table_args__ = (
        Index('ix_blog_images_blog_id', 'blog_id'),
        Index('ix_blog_images_is_featured', 'is_featured'),
        Index('ix_blog_images_position', 'position'),
    )
    
    def __repr__(self):
        return f"<BlogImage(id={self.id}, blog_id={self.blog_id}, filename={self.original_filename[:30]}...)>"


class BlogComment(Base):
    """
    Blog comment model
    """
    __tablename__ = "blog_comments"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    
    # Comment information
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=False)
    author_website = Column(String(500), nullable=True)
    author_ip = Column(String(45), nullable=True)  # IPv6 compatible
    
    # Content
    content = Column(Text, nullable=False)
    
    # Status
    is_approved = Column(Boolean, default=False, nullable=False)
    is_spam = Column(Boolean, default=False, nullable=False)
    
    # Reply tracking
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("blog_comments.id"), nullable=True)
    depth = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    blog = relationship("Blog", back_populates="comments")
    parent = relationship("BlogComment", remote_side=[id], backref="replies")
    
    # Indexes
    __table_args__ = (
        Index('ix_blog_comments_blog_id', 'blog_id'),
        Index('ix_blog_comments_is_approved', 'is_approved'),
        Index('ix_blog_comments_created_at', 'created_at'),
        Index('ix_blog_comments_parent_comment_id', 'parent_comment_id'),
    )
    
    def __repr__(self):
        return f"<BlogComment(id={self.id}, blog_id={self.blog_id}, author={self.author_name})>"


class BlogCategory(Base):
    """
    Blog category model
    """
    __tablename__ = "blog_categories"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Category information
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Display properties
    icon = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    order = Column(Integer, default=0, nullable=False)
    
    # Statistics
    post_count = Column(Integer, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_blog_categories_slug', 'slug', unique=True),
        Index('ix_blog_categories_order', 'order'),
        Index('ix_blog_categories_is_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<BlogCategory(id={self.id}, name={self.name}, posts={self.post_count})>"


class BlogTag(Base):
    """
    Blog tag model
    """
    __tablename__ = "blog_tags"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Tag information
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    
    # Statistics
    post_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('ix_blog_tags_slug', 'slug', unique=True),
        Index('ix_blog_tags_post_count', 'post_count'),
    )
    
    def __repr__(self):
        return f"<BlogTag(id={self.id}, name={self.name}, posts={self.post_count})>"