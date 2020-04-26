from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User

# HTML Pages
def index(request):
    allPosts = Post.objects.all()
    params = {'allPosts': allPosts}
    return render(request, 'home/index.html', params)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        message = request.POST['message']
        if len(name)<4 or len(mobile)<10 or len(email)<5 or len(message)<4:
            messages.error(request, 'Please fill correct information')
        else:
            contact = Contact(name=name, mobile=mobile, email=email, message=message)
            contact.save()
            messages.success(request, 'Your message has been successfully sent.')
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query) > 75:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
        
    if allPosts.count() == 0:        
        messages.warning(request, 'No search reasults found. please refine your query.')
    params = {'allPosts': allPosts, 'query': query}   
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        psw = request.POST['psw']
        repsw = request.POST['repsw']

        if psw != repsw:
            messages.warning(request, 'Re-password not matched. Try again.')
            return redirect('Home')

        if not mobile.isnumeric():
            messages.error(request, 'Please enter valid mobile number')
            return redirect('Home')
        
        if len(mobile) != 10:
            messages.warning(request, 'Mobile number contain only 10 digits.')
            return redirect('Home')

        myuser = User.objects.create_user(mobile, email, psw)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Congratulations! Your iCoder account has been registred successfully.')
        return redirect('Home')
    else:
        messages.warning(request, 'Please fill valid information.')
        return redirect('Home')

    return render(request, 'home/index.html')


def handleLogin(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        
        user = authenticate(username=mobile, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have Successfully Loged In')
            return redirect('Home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('Home')
    else:
        messages.warning(request, 'Please fill valid information.')
        return redirect('Home')

    return render(request, 'home/index.html')


def handleLogout(request):
    logout(request)
    messages.info(request, 'Logout Successfully. Thanks for spending some quality time with the Web site today')
    return redirect('Home')