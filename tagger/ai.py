# tagger/ai.py
from keybert import KeyBERT

kw_model = KeyBERT('all-mpnet-base-v2')  # Better quality model

# Smart keyword set (simplified from your JS version)
SMART_KEYWORDS = set([
    'technology', 'tech', 'AI', 'artificial intelligence', 'science', 'space', 'nasa',
        'animals', 'zoology', 'biology', 'lion', 'tiger', 'finance', 'stocks', 'investment',
        'health', 'medicine', 'covid', 'mental health', 'nutrition', 'fitness', 'environment',
        'climate', 'ecology', 'education', 'university', 'school', 'history', 'politics', 'election', 'music', 'art', 'culture', 'travel', 'food', 'cooking', 'recipes', 'lifestyle', 'fashion',
        'sports', 'football', 'basketball', 'cricket', 'gaming', 'video games', 'movies', 'cinema', 'tv shows', 'series', 'books', 'literature', 'writing', 'photography', 'design', 'programming', 'coding', 'web development', 'software',
        'television', 'streaming', 'podcasts', 'comics', 'anime', 'manga', 'comedy', 'humor', 'political satire', 'social media', 'internet culture', 'memes', 'cryptocurrency', 'blockchain', 'data science', 'machine learning', 'big data', 'cloud computing', 'cybersecurity', 'privacy',
        'science', 'technology', 'engineering', 'mathematics', 'artificial intelligence', 'machine learning', 'space', 'astronomy', 'history', 'philosophy', 'psychology', 'sociology', 'education', 'e-learning',
        'politics', 'world news', 'local news', 'elections', 'government', 'policy', 'law', 'legal news', 'war', 'conflict', 'economics', 'crime', 'justice',
        'personal finance', 'stock market', 'cryptocurrency', 'investing', 'real estate', 'startups', 'entrepreneurship', 'business news', 'economy', 'trade', 'marketing', 'sales', 'leadership', 'management',
        'gadgets', 'tech reviews', 'apps', 'software', 'programming', 'coding', 'web development', 'cybersecurity', 'cloud computing', 'mobile', 'android', 'ios', 'big data',
        'health', 'mental health', 'nutrition', 'fitness', 'exercise', 'diseases', 'medicine', 'medical breakthroughs', 'women\'s health', 'men\'s health', 'healthcare', 'yoga', 'mindfulness', 'sleep', 'lifestyle',
        'climate change', 'renewable energy', 'pollution', 'conservation', 'wildlife', 'biodiversity', 'sustainability', 'sustainable living', 'natural disasters',
        'literature', 'books', 'visual arts', 'performing arts', 'theater', 'dance', 'culture', 'cultural commentary', 'museums', 'exhibitions',
        'movies', 'cinema', 'tv shows', 'series', 'music', 'albums', 'celebrities', 'gossip', 'awards', 'pop culture', 'streaming', 'netflix', 'prime video',
        'gaming', 'video games', 'esports', 'game reviews', 'walkthroughs', 'tournaments', 'mobile games', 'game development',
        'travel', 'destinations', 'food', 'recipes', 'home decor', 'fashion', 'style', 'beauty', 'grooming', 'diy', 'crafts', 'photography', 'gardening', 'pets',
        'automotive', 'cars', 'electric vehicles', 'car reviews', 'public transport', 'mobility', 'bikes', 'scooters', 
        'career', 'jobs', 'resume', 'job hunting', 'freelancing', 'remote work', 'work culture', 'productivity', 'time management',
        'social media', 'tiktok', 'instagram', 'youtube', 'memes', 'viral content', 'internet culture', 'online communities', 'reddit', 'discord',
        'relationships', 'dating', 'family', 'parenting', 'self-help', 'life advice', 'personal growth',
        'backpacking', 'solo travel', 'travel hacks', 'hidden gems', 'cultural etiquette', 'adventure',
        'product reviews', 'buying guides', 'online shopping', 'e-commerce', 'deals', 'discounts'
])

STOPWORDS = set([
    'the','and','to','of','in','a','for','is','on','with','that','this','by','an',
    'as','it','from','at','be','are','was','or','which','but','we','can','has','have',
    'why', 'not', 'all', 'if', 'so', 'do', 'you', 'your', 'they', 'their', 'he', 'she',
    'him', 'her', 'my', 'me', 'us', 'our', 'what', 'who', 'when', 'where', 'how', 'does', 'the','and','to','of','in','a','for','is','on','with','that','this','by','an',
        'as','it','from','at','be','are','was','or','which','but','we','can','has','have', 'why', 'not', 'all', 'if', 'so', 'do', 'you', 'your', 'they', 'their', 'he', 'she', 'him', 'her', 'my', 'me', 'us', 'our', 'what', 'who', 'when', 'where', 'how', 'does'
])

def extract_top_words(text, n=5):
    import re
    from collections import Counter

    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [word for word, _ in Counter(filtered).most_common(n)]

def match_smart_keywords(text):
    text_lower = text.lower()
    return [kw for kw in SMART_KEYWORDS if kw in text_lower]

def extract_tags(title, description=''):
    combined_text = f"{title} {description}"

    # 1. KeyBERT extraction
    keywords = kw_model.extract_keywords(
        combined_text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=10
    )
    keybert_tags = [kw for kw, score in keywords if score >= 0.45]

    # 2. Smart matching
    smart_tags = match_smart_keywords(combined_text)

    # 3. Top words
    top_words = extract_top_words(combined_text)

    # 4. Merge & dedupe
    all_tags = list(set(keybert_tags + smart_tags + top_words))
    return all_tags