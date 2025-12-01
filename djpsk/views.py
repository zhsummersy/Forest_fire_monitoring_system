from django.shortcuts import render, HttpResponse
from home.models import *
from django.contrib import messages
from blog.models import Post
from django.shortcuts import redirect




def show_home_page(request):
	cats=Category.objects.all()
	images = Image.objects.all()
	data = {'images':images,'cats':cats}
	return render(request,"home/home.html",data)

# Create your views here.
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)

        if len(name)<2 or len(email)<5 or len(content)<3:
            messages.error(request, "Please fill the form Correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, ": Sent, Thank You.")
    return render(request,'home/contact.html')



def search(request):
    #前端input,name=''
    query = request.GET['query']
    if len(query)>78:
        allPosts = []
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,": No search result found. Please refine your query.")
    params={'allPosts': allPosts, 'query':query}
    return render(request,'home/search.html',params)
   # return HttpResponse('This is search')


