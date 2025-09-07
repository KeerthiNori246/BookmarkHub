from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstPage, name='first-page'),
    path('home/', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('welcome/', views.welcomePage, name='welcome'),
    path('select-preferences', views.selectPreferences, name='select-preferences'),
    path('profile/<str:name>/', views.profilePage, name='profile'),
    path('edit-profile', views.editProfile, name='edit-profile'),
    path('button-details', views.buttonDetails, name='button-details'),
    path('save-article/', views.saveArticle, name='save-article'),
    path('board-add-confirmation/<str:name>/', views.boardAddConfirmation, name='board-add-confirmation'),
    path('create-board', views.createBoard, name='create-board'),
    path('board-list/<str:name>/', views.boardList, name='board-list'),
    path('article-list/<int:pk>/', views.articleList, name='article-list'),
]