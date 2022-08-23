from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Profile,Post,Comment,Followers
from django.http import HttpResponseRedirect
from .forms import PostForm,CommentForm,ProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request,"register.html",{'form':form})

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/home')
    return render(request,"login.html")


def logouts(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def homepage(request):
    post=Post.objects.all().order_by('-created')
    profile=User.objects.all()
    
    if request.method =='POST':
        if 'image' in request.FILES:
            posts=Post.objects.create(
                creator=request.user,
                text=request.POST.get('text'),
                image=request.FILES.get('image')
            )
            posts.save()
            return redirect('/home')
        elif 'like' in request.POST:
            postl=Post.objects.get(id=request.POST.get('like'))
            if request.user in postl.likers.all():
                print('remove')
                postl.likers.remove(request.user)
            else:
                print('add')
                postl.likers.add(request.user)
        else:
             posts=Post.objects.create(
                creator=request.user,
                text=request.POST.get('text'),
            )
             posts.save()
             return redirect('/home')   
    return render(request,"home.html",{'profiles':profile,'Post':post})

@login_required(login_url='/login')
def profile(request,id):
    profile=User.objects.get(id=id)
    post=Post.objects.filter(creator=profile).order_by('-created')
    if request.method =='POST':
        if 'like' in request.POST:
            postl=Post.objects.get(id=request.POST.get('like'))
            if request.user in postl.likers.all():
                print('remove')
                postl.likers.remove(request.user)
            else:
                print('add')
                postl.likers.add(request.user)

    return render(request,"profile.html",{'profiles':profile,'Post':post})

@login_required(login_url='/login')
def createprofile(request):
    if request.method == 'POST':
        if 'profile_pic' in request.FILES and 'cover_pic' in request.FILES:
            bio=request.POST.get('bio')
            location=request.POST.get('location')
            profile_pic=request.FILES.get('profile_pic')
            cover_pic=request.FILES.get('cover_pic')
            profile=Profile.objects.create(
                username=request.user,
                bio=bio,
                location=location,
                profile_pic=profile_pic,
                cover_pic=cover_pic
            )
            profile.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif 'profile_pic' in request.FILES and 'cover_pic' not in request.FILES:
            bio=request.POST.get('bio')
            location=request.POST.get('location')
            profile_pic=request.FILES.get('profile_pic')
            
            profile=Profile.objects.create(
                username=request.user,
                bio=bio,
                location=location,
                profile_pic=profile_pic,
                
            )
            profile.save()
            return redirect(request.META['HTTP_REFERER'])
        elif 'profile_pic' not in request.FILES and 'cover_pic' not in request.FILES:
            bio=request.POST.get('bio')
            location=request.POST.get('location')
            
            profile=Profile.objects.create(
                username=request.user,
                bio=bio,
                location=location,
            )
            profile.save()
            return redirect(request.META['HTTP_REFERER'])
    return render(request,"createprofile.html")

@login_required(login_url='/login')
def makecomment(request,id):
    post=Post.objects.get(id=id)
    comment=Comment.objects.filter(posts=post).order_by('-created')
    if request.method == 'POST' and 'like' not in request.POST and 'childcomment' not in request.POST:
        contents=Comment.objects.create(
            commenter=request.user,
            posts=post,
            content=request.POST.get('comment')
        )
        contents.save()
    elif 'childcomment' in request.POST:
        parent=Comment.objects.get(id=request.POST.get('childcomment'))
        contents=Comment.objects.create(
            commenter=request.user,
            posts=post,
            parent=parent,
            content=request.POST.get('comment')
        )
        contents.save()
    elif 'like' in request.POST:
            postl=Post.objects.get(id=request.POST.get('like'))
            if request.user in postl.likers.all():
                print('remove')
                postl.likers.remove(request.user)
            else:
                print('add')
                postl.likers.add(request.user)
            
    return render(request,"comment.html",{'p':post,'comment':comment})

@login_required(login_url='/login')
def follow(request,id,pk):
    follow=Followers.objects.get(id=pk)
    user=request.user
    follow_user=User.objects.get(id=id)
    print(follow)
    if request.user in follow.follower.all():
        follow.follower.remove(request.user)
        for i in user.followers_set.all():
            i.following.remove(follow_user)
        print('remove')
    else:
        follow.follower.add(request.user)
        print(user.followers_set.all())
        if not(len(user.followers_set.all())):
            print('success')
            f=Followers.objects.create(
                user=request.user
            )
            f.save()
        for i in user.followers_set.all():
            i.following.add(follow_user)      
            print('add',request.user,follow_user)
        return redirect(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def editpost(request,id):
    p=Post.objects.get(id=id)
    form=PostForm(instance=p)
    if request.method =='POST':
        form=PostForm(request.POST,request.FILES,instance=p)
        if form.is_valid():
            form.save()
        return redirect(request.META['HTTP_REFERER'])    
    return render(request,"editpost.html",{'form':form})

@login_required(login_url='/login')
def editcomment(request,id):
    c=Comment.objects.get(id=id)
    form=CommentForm(instance=c)
    if request.method=='POST':
        form=CommentForm(request.POST,instance=c)
        if form.is_valid():
            form.save()
        return redirect(request.META['HTTP_REFERER'])
    return render(request,"editpost.html",{'form':form})
    
@login_required(login_url='/login')
def editprofile(request,id):
    p=Profile.objects.get(id=id)
    form=ProfileForm(instance=p)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=p)
        if form.is_valid():
            form.save()
            print('hey')
    return render(request,"editprofile.html",{'form':form})

    
@login_required(login_url='/login')
def deletepost(request,id):
    p=Post.objects.get(id=id)
    p.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def deletecomment(request,id):
    c=Comment.objects.get(id=id)
    c.delete()
    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='/login')
def temp(request,id):
    follower=User.objects.get(id=id)
    user=request.user
    f=Followers.objects.create(
        user=follower
    )
    if f:
        follow=Followers.objects.filter(user=follower)
        for f in follow:
            f.follower.add(request.user)
        for i in user.followers_set.all():
             i.following.add(follower)
        f.save()
        return redirect(request.META['HTTP_REFERER'])
    return render(request,"temp.html")


@login_required(login_url='/login')
def follower(request):
    user=request.user
    follower=Followers.objects.get(user=user)
    return render(request,"follower.html",{'follower':follower})

@login_required(login_url='/login')
def following(request):
    user=request.user
    follower=Followers.objects.get(user=user)
    return render(request,"following.html",{'follower':follower})