from django.urls import path
from . import views

urlpatterns = [
    path('home',views.homepage,name="home"),
    path('',views.register,name="register"),
    path('login',views.loginpage,name="login"),
    path('logout',views.logouts,name="logout"),
    path('profile/<int:id>',views.profile,name="profile"),
    path('createprofile',views.createprofile,name="createprofile"),
    path('comment/<int:id>',views.makecomment,name="comment"),
    path('temp/<int:id>',views.temp,name="temp"),
    path('follow/<int:id>/<int:pk>',views.follow,name="follow"),
    path('editpost/<int:id>',views.editpost,name="editpost"),
    path('deletepost/<int:id>',views.deletepost,name="deletepost"),
    path('editcomment/<int:id>',views.editcomment,name="editcomment"),
    path('deletecomment/<int:id>',views.deletecomment,name="deletecomment"),
    path('editprofile/<int:id>',views.editprofile,name="editprofile"),
    path('follower',views.follower,name="follower"),
    path('following',views.following,name="following"),

]

