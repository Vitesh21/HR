from src.main import BlogGeneratorSystem
from src.config import Config

def main():
    try:
        # Initialize the blog generator system
        blog_system = BlogGeneratorSystem(Config.HUGGINGFACE_API_KEY)
        
        # Generate a blog post
        topic = "Remote Work Best Practices 2023"
        blog_content = blog_system.generate_blog(topic)
        
        print(blog_content)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()