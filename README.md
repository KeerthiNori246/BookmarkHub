# BookmarkHub
BookmarkHub is a Pinterest-inspired web application focused on helping readers discover articles online instead of images. It is designed for users to find interesting articles, save and organize them into boards, and build a personal profile that reflects their reading taste. Profiles allow users to showcase their saved articles to others, explore what other users are reading, and get inspiration based on different reading interests. With personalized feeds, AI-powered recommendations, and social features, BookmarkHub makes reading and sharing articles engaging and easy.

## How it works:
* Users create an account and set their reading preferences.
* A personalized feed of articles is then generated.
* Articles can be organized into boards from this home page, just like on Pinterest—saving an article essentially means adding it to one of your boards.
* The personalized feed dynamically adapts based on what you save.

## Cool feature – Bookmarklet:
* You can drag a special "Bookmarklet" button to your browser’s bookmarks bar.
* While browsing the web, click it to instantly save any article to your BookmarkHub boards.

## AI-powered personalization:
* The feed is fine-tuned using KeyBERT, which analyzes saved articles to recommend similar ones.

## Social aspect:
* Each user has a profile that showcases their saved articles, making it a way to share your reading taste.
* You can explore others’ profiles to discover what they’re reading too.

## Tech stack:
* Built with Django as the backend framework.

## Running Instructions:
```bash
# Clone the repo
git clone https://github.com/KeerthiNori246/BookmarkHub.git

# Install Django
pip install django

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver

# Open in browser: http://127.0.0.1:8000/
