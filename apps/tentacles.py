from apify_client import ApifyClient
from apps.CONSTANTS import APIFY as APIFY_TOKEN

# ---------------- CONFIGURATION ----------------
APIFY_TOKEN = APIFY_TOKEN
ACTOR_ID = "dev_fusion~linkedin-company-scraper" 
ACTOR_POSTS = "apimaestro~linkedin-company-posts"
# -----------------------------------------------
def get_linkedin_data(page_alias: str):
    print(f"[-] Fetching Data for: {page_alias}...")
    client = ApifyClient(APIFY_TOKEN)
    
    # --- 1. FETCH METADATA ---
    print(f"    [1/2] Requesting Metadata ({ACTOR_ID})...")
    meta_input = { "profileUrls": [f"https://www.linkedin.com/company/{page_alias}"] }
    
    metadata = {}
    try:
        run_meta = client.actor(ACTOR_ID).call(run_input=meta_input)
        dataset_meta = client.dataset(run_meta["defaultDatasetId"]).list_items().items
        if dataset_meta:
            metadata = dataset_meta[0]
            print("    [+] Metadata received.")
    except Exception as e:
        print(f"    [!] Metadata Error: {e}")

    # --- 2. FETCH POSTS ---
    print(f"    [2/2] Requesting Posts ({ACTOR_POSTS})...")
   
    posts_input = { 
        "linkedinUrl": f"https://www.linkedin.com/company/{page_alias}", 
        "company_name": page_alias,
        "resultsCount": 15  # Limit to 15 posts
    }
    
    posts_list = []
    try:
        run_posts = client.actor(ACTOR_POSTS).call(run_input=posts_input)
        dataset_posts = client.dataset(run_posts["defaultDatasetId"]).list_items().items
        if dataset_posts:
            posts_list = dataset_posts
            print(f"    [+] {len(posts_list)} Posts received.")
        else:
            print("    [!] No posts found.")
    except Exception as e:
        print(f"    [!] Posts Error: {e}")

    # --- 3. MERGE RESULTS ---
    metadata["posts_data"] = posts_list 
    
    return metadata

# --- TEST---
if __name__ == "__main__":
    res = get_linkedin_data("deepsolv")
    import json
    print(json.dumps(res, indent=4))