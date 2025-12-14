from sqlalchemy.orm import Session
from apps.anatomy import Page, SocialMediaUser, Post

class DatabaseGateway:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, payload: dict):
        """
        Input Format:
        {
            "flag": 0 or 1,
            "page_id": "str" (Required for Flag 0),
            "data": {...} (Required for Flag 1)
        }
        """
        flag = payload.get("flag")
        
        # --- FLAG 0: RETRIEVE FROM DB ---
        if flag == 0:
            page_alias = payload.get("page_id")
            print(f"[Part A] Checking DB for: {page_alias}")
            
            # Query the DB
            page = self.db.query(Page).filter(Page.page_alias == page_alias).first()
            
            if page:
                return {"status": "found", "data": {
                    "name": page.name,
                    "industry": page.industry,
                    "followers": page.follower_count,
                    "description": page.description
                }}
            else:
                return {"status": "not_found"}

        # --- FLAG 1: INSERT INTO DB ---
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
            
            # 2. Add Employees (Iterate list)
            for emp in data.get("employees", []):
                new_emp = SocialMediaUser(page_id=new_page.id, name=emp["name"])
                self.db.add(new_emp)
                
            # 3. Add Posts
            for post in data.get("posts", []):
                new_post = Post(page_id=new_page.id, content=post["content"])
                self.db.add(new_post)
                
            self.db.commit()
            return {"status": "success", "message": "Data inserted successfully"}
            
        else:
            return {"status": "error", "message": "Invalid Flag"}
def format_scraper_result(raw_data: dict, page_alias: str) -> dict:
    print("[Part C] Formatting merged Apify data...")

    # 1. Map Metadata (Same as before)
    formatted_data = {
        "page_alias": page_alias,
        "linkedin_internal_id": str(raw_data.get("companyId")),
        "name": raw_data.get("companyName") or f"Unknown ({page_alias})",
        "description": raw_data.get("description") or raw_data.get("tagline", ""),
        "website_url": raw_data.get("websiteUrl"),
        "industry": raw_data.get("industry"),
        "follower_count": raw_data.get("followerCount") or 0,
        "head_count": raw_data.get("employeeCount") or 0,
        "profile_picture_url": raw_data.get("logoResolutionResult") or raw_data.get("originalCoverImage"),
        "specialties": raw_data.get("specialities", []),
        "employees": [],
        "posts": []
    }
    
    raw_posts = raw_data.get("posts_data", [])
    
    for post in raw_posts:
        content = post.get("text") or post.get("content") or post.get("commentary") or ""
        
        if content:
            formatted_data["posts"].append({"content": content[:500]}) 

    return {
        "flag": 1,
        "data": formatted_data
    }