from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Preference, Article, Board
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserCreationForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tagger.ai import extract_tags  
from django.db.models import Q
import re

STOPWORDS = {"and", "the", "for", "of", "to", "in", "on", "with", "a", "an", "amp"}

def _keywords_from_prefs(user_preferences):
    tokens = set()
    for pref in user_preferences:
        title = (pref.title or "").lower()
        words = re.findall(r"[a-z0-9]+", title)
        for w in words:
            if len(w) >= 3 and w not in STOPWORDS:
                tokens.add(w)
    return tokens


@login_required(login_url='login')
def home(request):
    user = request.user
    user_preferences = user.preferences.all()
    query = request.GET.get("q")

    # Articles already saved
    saved_titles = Article.objects.filter(boards__user=user).values_list("title", flat=True)

    if query:
        articles = (
            Article.objects.filter(
                Q(preferences__title__icontains=query) |
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            )
            .exclude(boards__user=user)
            .exclude(title__in=saved_titles)
            .distinct()
        )
    else:
        # Build keywords from preferences
        keywords = _keywords_from_prefs(user_preferences)

        if keywords:
            q_obj = Q()
            for kw in keywords:
                q_obj |= Q(preferences__title__icontains=kw)

            articles = (
                Article.objects.filter(q_obj)
                .exclude(boards__user=user)
                .exclude(title__in=saved_titles)
                .distinct()
            )
        else:
            articles = Article.objects.exclude(boards__user=user).exclude(title__in=saved_titles)

    # Dedup by title
    seen_titles = set()
    unique_articles = []
    for article in articles:
        if article.title not in seen_titles:
            seen_titles.add(article.title)
            unique_articles.append(article)

    article_data = [
        {
            "title": article.title,
            "pic": article.pic,
            "link": article.link,
            "overview": article.overview,
            "id": article.a_id,
            "show_save": not article.boards.filter(user=user).exists(),
        }
        for article in unique_articles
    ]

    return render(request, "base/home.html", {"article_data": article_data, "query": query})


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', {'page': page})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('first-page')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.email 
            user.save()
            login(request, user)
            return redirect('welcome')  # Redirect to button details page after registration
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def firstPage(request):
    return render(request, 'base/first_page.html');

@login_required(login_url='login')
def welcomePage(request):
    name = request.user.name 
    context = {'name': name}
    return render(request, 'base/welcome.html', context)

@login_required(login_url='login')
def selectPreferences(request):
    # Hardcoded preference options
    hardcoded_prefs = [
        "Technology",
    "Science",
    "Health & Fitness",
    "Business & Finance",
    "Politics & Current Affairs",
    "Education & Learning",
    "History & Culture",
    "Travel & Adventure",
    "Food & Nutrition",
    "Sports",
    "Entertainment (Movies, TV, Music)",
    "Gaming",
    "Art & Design",
    "Literature & Books",
    "Environment & Sustainability",
    "Relationships & Lifestyle",
    "Self-Improvement & Productivity",
    "Fashion & Beauty",
    "Religion & Spirituality",
    "Startups & Entrepreneurship",
    "Law & Justice",
    "Opinion & Editorials",
    "Cryptocurrency & Blockchain",
    ]

    if request.method == 'POST':
        selected_titles = request.POST.getlist('preferences')

        # Clear existing preferences
        request.user.preferences.clear()

        for title in selected_titles:
            # Create or fetch Preference object for each title
            pref, _ = Preference.objects.get_or_create(title=title)
            request.user.preferences.add(pref)

        return redirect('button-details')

    # Fetch currently selected preferences by title
    user_selected = request.user.preferences.values_list("title", flat=True)

    context = {
        'preferences': hardcoded_prefs,   # send hardcoded list
        'user_selected': user_selected,   # send selected titles
    }
    return render(request, 'base/select_preferences.html', context)





def profilePage(request, name):
    user = get_object_or_404(User, name=name)
    can_edit = request.user == user
    user_data = {
        'name': user.name,
        'email': user.email,
        'description': user.description,
        'pfp': user.pfp.url if user.pfp else '',
    }
    context = {
        "user_data": user_data,
        "can_edit": can_edit,
        "profile_user": user,  # optional, in case you want to show username
    }
    return render(request, 'base/profile_page.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    form = UserForm(instance=user)  
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', name=user.name)  
    context = {'form': form}
    return render(request, 'base/edit-profile.html', context)

@login_required(login_url='login')
def buttonDetails(request):
    context = {}
    return render(request, 'base/button_details.html', context)

@login_required(login_url='login')
def saveArticle(request):
    user = request.user
    boards = Board.objects.filter(user=user)

    title = request.GET.get('title', '')
    overview = request.GET.get('desc', '')
    link = request.GET.get('url', '')
    pic = request.GET.get('img', '')

    context = {
        'boards': boards,
        'title': title,
        'overview': overview,
        'link': link,
        'pic': pic
    }

    return render(request, 'base/save_article.html', context)


@login_required(login_url='login')
def boardAddConfirmation(request, name):
    if request.method == 'POST':
        board_name = request.POST.get('board_name') or name

        try:
            board = Board.objects.get(name=board_name, user=request.user)
        except Board.DoesNotExist:
            return render(request, 'base/board_add_confirmation.html', {'error': 'Board not found'})

        title = request.POST.get('title')
        overview = request.POST.get('overview')
        link = request.POST.get('link')
        pic_url = request.POST.get('pic')

        article = Article.objects.create(
            title=title,
            overview=overview,
            link=link,
            pic = pic_url
        )
        article.boards.add(board)

        tags = extract_tags(title, overview)

        for tag in tags:
            preference, created = Preference.objects.get_or_create(title=tag)
            article.preferences.add(preference)
            request.user.preferences.add(preference)

        return render(request, 'base/board_add_confirmation.html', {
            'message': 'Article saved successfully!',
            'board': board
        })

    return redirect('save-article')

@login_required(login_url='login')
def createBoard(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        overview = request.POST.get('overview')
        link = request.POST.get('link')
        pic_url = request.POST.get("pic")

        if name:
            board = Board.objects.create(name=name, user=request.user)

            if title and overview and link:
                # Step 1: Create the article
                article = Article.objects.create(
                    title=title,
                    overview=overview,
                    link=link,
                    pic=pic_url 
                )
                article.boards.add(board)

                tags = extract_tags(title, overview)

                for tag in tags:
                    preference, created = Preference.objects.get_or_create(title=tag)
                    article.preferences.add(preference)
                    request.user.preferences.add(preference)

            return redirect('save-article')

    return render(request, 'base/create_board.html')

def boardList(request, name):
    user = get_object_or_404(User, name=name)
    boards = Board.objects.filter(user=user)
    board_data = [{'name': board.name, 'pk': board.pk} for board in boards]
    context = {
        'user': user,
        'board_data': board_data
    }
    return render(request, 'base/board_list.html', context)

def articleList(request, pk):
    board = get_object_or_404(Board, pk=pk)
    articles = Article.objects.filter(boards=board).distinct()

    # Preload all saved article titles for this user
    saved_titles = set()
    if request.user.is_authenticated:
        saved_titles = set(
            Article.objects.filter(boards__user=request.user)
            .values_list("title", flat=True)
        )

    article_data = []
    for article in articles:
        can_save = request.user.is_authenticated and article.title not in saved_titles

        article_data.append({
            'title': article.title,
            'pic': article.pic if article.pic else '',
            'overview': article.overview,
            'link': article.link,
            'id': article.pk,
            'can_save': can_save,
        })

    context = {
        'board': board,
        'article_data': article_data,
        'user_name': request.user.name if request.user.is_authenticated else None,
    }
    return render(request, 'base/article_list.html', context)
