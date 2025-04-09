from fasthtml.common import *
from starlette.testclient import TestClient
from pathlib import Path
import shutil
import os

def generate_static_site():
    """Generate static HTML files from FastHTML app routes"""
    from main import app, index, post_page, about
    
    # Create directory for static files
    static_dir = Path("_static")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir(exist_ok=True)
    
    # Copy assets folder if it exists
    assets_dir = Path("assets")
    if assets_dir.exists():
        shutil.copytree(assets_dir, static_dir / "assets")
    
    # Initialize TestClient
    client = TestClient(app)
    
    # Generate index.html
    index_response = client.get("/")
    (static_dir / "index.html").write_text(index_response.text)
    
    # Generate about.html
    about_response = client.get("/about")
    (static_dir / "about.html").write_text(about_response.text)
    
    # Create posts directory
    posts_dir = static_dir / "post_page"
    posts_dir.mkdir(exist_ok=True)
    
    # Generate HTML for each blog post
    for post_file in Path("content").glob("*.md"):
        slug = post_file.stem
        post_response = client.get(f"/post_page?slug={slug}")
        post_dir = posts_dir / slug
        post_dir.mkdir(exist_ok=True)
        (post_dir / "index.html").write_text(post_response.text)
    
    print(f"Static site generated in {static_dir}")

if __name__ == "__main__":
    generate_static_site()
