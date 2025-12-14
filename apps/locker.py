from sqlalchemy.orm import Session, joinedload
from apps.anatomy import Page, SocialMediaUser, Post

class DatabaseGateway:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, payload: dict):
        flag = payload.get("flag")
        
        # --- FLAG 0: RETRIEVE (Updated to fetch ALL data) ---
        if flag == 0:
            page_alias = payload.get("page_id")
            print(f"[Part A] Checking DB for: {page_alias}")
            page = self.db.query(Page).options(
                joinedload(Page.posts),
                joinedload(Page.employees)
            ).filter(Page.page_alias == page_alias).first()
            
            if page:
                return {"status": "found", "data": {
                    "page_alias": page.page_alias,
                    "linkedin_internal_id": page.page_alias, 
                    "name": page.name,
                    "description": page.description,
                    "website_url": page.industry,
                    "industry": page.industry,
                    "follower_count": page.follower_count,
                    "head_count": page.head_count,
                    
                    # Relationships
                    "posts": [{"content": p.content} for p in page.posts],
                    "employees": [{"name": e.name} for e in page.employees]
                }}
            else:
                return {"status": "not_found"}

        # --- FLAG 1: INSERT ---
        elif flag == 1:
            data = payload.get("data")
            print(f"[Part A] Inserting new data for: {data.get('page_alias')}")
            
            # 1. Create Page
            new_page = Page(
                page_alias=data["page_alias"],
                name=data["name"],
                industry=data["industry"],
                follower_count=data["follower_count"],
                description=data["description"]
            )
            self.db.add(new_page)
            self.db.commit()
            self.db.refresh(new_page)
            
            # 2. Add Posts 
            for post in data.get("posts", []):
               #Truncating larger content for MVP
                content_safe = post["content"][:3000] if post.get("content") else ""
                new_post = Post(page_id=new_page.id, content=content_safe)
                self.db.add(new_post)
                
            self.db.commit()
            return {"status": "success", "message": "Data inserted successfully"}
            
        else:
            return {"status": "error", "message": "Invalid Flag"}