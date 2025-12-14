import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ----------------- CONFIGURATION -----------------
DEFAULT_URL = "mysql+pymysql://dev_user:password123@localhost/linkedin_insights_db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_URL)
Base = declarative_base()

# ----------------- MODELS -----------------
class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True, index=True)
    page_alias = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    industry = Column(String(255))
    follower_count = Column(Integer)
    description = Column(Text)
    head_count = Column(Integer, default=0)      
    profile_picture_url = Column(Text)            
    website_url = Column(String(500))            
    # Relationships
    posts = relationship("Post", back_populates="page")
    employees = relationship("SocialMediaUser", back_populates="page")

class SocialMediaUser(Base):
    __tablename__ = "social_media_users"
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id"))
    name = Column(String(255))
    page = relationship("Page", back_populates="employees")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id"))
    # Use Text with utf8mb4 collation support for Emojis
    content = Column(Text(collation='utf8mb4_unicode_ci')) 
    page = relationship("Page", back_populates="posts")

# ----------------- CONNECTION -----------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)