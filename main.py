from fasthtml.common import *
from pathlib import Path
import frontmatter
import markdown
import re
from datetime import datetime

# Initialize the FastHTML app
app, rt = fast_app(
    pico=True,  # Use Pico CSS for default styling
    hdrs=[
        Link(rel="stylesheet", href="/assets/blog.css"),
        MarkdownJS(),  # For client-side rendering if needed
    ]
)

# Create a blog post component
def BlogPost(title, date, content, summary=None):
    return Div(
        H1(title, cls="post-title"),
        P(f"Published: {date.strftime('%B %d, %Y')}", cls="post-date"),
        P(summary, cls="post-summary") if summary else None,
        Div(Safe(content), cls="post-content"),
        cls="blog-post"
    )

# Route for the home page
@rt
def index():
    posts = []
    for post_file in sorted(Path("content").glob("*.md"), reverse=True):
        post = frontmatter.load(post_file)
        post_slug = post_file.stem
        posts.append({
            "title": post.get("title", "Untitled"),
            "date": post.get("date", datetime.now()),
            "summary": post.get("summary", ""),
            "slug": post_slug
        })
    
    return Titled(
        "My FastHTML Blog",
        Div(*(
            Article(
                # Change this line to use path format instead of query parameters
                H2(A(post["title"], href=f"/post/{post['slug']}")),
                P(f"Published: {post['date'].strftime('%B %d, %Y')}"),
                P(post["summary"]),
                A("Read more →", href=f"/post/{post['slug']}", cls="read-more"),
                cls="post-preview"
            ) for post in posts
        ), cls="post-list")
    )

# Route for individual blog posts
@rt
def post_page(slug: str):
    try:
        post_path = Path(f"content/{slug}.md")
        if not post_path.exists():
            return Titled("404 - Post Not Found", P("Sorry, that post doesn't exist."))
        
        post = frontmatter.load(post_path)
        content = markdown.markdown(post.content)
        
        return Titled(
            post.get("title", "Untitled Post"),
            BlogPost(
                post.get("title", "Untitled"),
                post.get("date", datetime.now()),
                content,
            ),
            Link("← Back to Home", href=index)
        )
    except Exception as e:
        return Titled("Error", P(f"Error loading post: {str(e)}"))

# Optional: Add About page
@rt
def about():
    return Titled(
        "About My Blog",
        P("This is a blog created with FastHTML and hosted on GitHub Pages."),
        Link("← Back to Home", href=index)
    )

if __name__ == "__main__":
    serve()
