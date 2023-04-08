# Create virtual environment and install Django
mkdir myproject
cd myproject
python3 -m venv venv
source venv/bin/activate
pip install django

# Create models for Blog post and user in Django and create migrations
python manage.py startapp blog
python manage.py makemigrations
python manage.py migrate

# Implement CRUD functionality for Blog post
## Views ##
from django.shortcuts import render
from .models import Blog

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = Blog.objects.get(pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def blog_create(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BlogForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Save the blog data to the database:
            form.save()
            # Redirect to blog list view:
            return redirect('blog_list')
    else:
        # Create an empty form instance:
        form = BlogForm()
    return render(request, 'blog_create.html', {'form': form})

def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BlogForm(request.POST, instance=blog)
        # Check if the form is valid:
        if form.is_valid():
            # Save the updated blog data to the database:
            form.save()
            # Redirect to blog list view:
            return redirect('blog_list')
    else:
        # Create a form instance with pre-populated data:
        form = BlogForm(instance=blog)
    return render(request, 'blog_update.html', {'form': form})

def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blog_list')

## URLs ##
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/update/', views.blog_update, name='blog_update'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]

## Forms ##
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'author')

# Implement user authentication and authorization using Django built-in authentication system
python manage.py createsuperuser
## Follow prompts to create superuser

## Views ##
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

def login_view(request):
    if request.method == 'POST':
        # Create an instance of built-in form with data from request:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user:
            user = form.get_user()
            login(request, user)
            return redirect('blog_list')
    else:
        # Create an empty form instance:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

## URLs ##
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

## Templates ##
<!-- login.html -->
{% extends 'base.html' %}
{% block content %}
  <h2>Login</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
  </form>
{% endblock %}

## Decorators ##
from django.contrib.auth.decorators import login_required

@login_required
def blog_create(request):
    ...

# Build frontend using React library for displaying blogs and interacting with API
## Install dependancies ##
npx create-react-app client
cd client
npm install axios react-router-dom

## Create Components ##
### App.js ###
import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import BlogList from './components/BlogList';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={BlogList} />
      </Switch>
    </Router>
  );
}

export default App;

### BlogList.js ###
import React, { Component } from 'react';
import axios from 'axios';

class BlogList extends Component {
  state = {
    blogs: []
  };

  componentDidMount() {
    axios.get('/api/blogs')
      .then(res => {
        const blogs = res.data;
        this.setState({ blogs });
      });
  }

  render() {
    return (
      <div>
        <h2>Blog List</h2>
        <ul>
          {this.state.blogs.map(blog => <li key={blog.id}>{blog.title}</li>)}
        </ul>
      </div>
    );
  }
}

export default BlogList;

### Routing ###
## Create urls.py file in blog app ##
from django.urls import path
from .views import BlogListView

urlpatterns = [
    path('api/blogs/', BlogListView.as_view())
]

## Update views.py to accept API requests ##
from django.views.generic import ListView
from .models import Blog
from django.http import JsonResponse

class BlogListView(ListView):
  model = Blog
  template_name = 'blog_list.html'
  queryset = Blog.objects.all()

  def get(self, request, *args, **kwargs):
    blogs = list(Blog.objects.values())
    return JsonResponse(blogs, safe=False)

## Update settings.py to accept React requests ##
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
] 
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
] 

## Update template to host react app ##
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <title>My Blog</title>
  </head>
  <body>
    <div id="root"></div>
    <script src="{% static 'main.js' %}"></script>
  </body>
</html> 

## Build react app ##
npm run build
cp -r build/ ../static/ 

## Create django views and linking ##
### Create home view and template ###
## views.py
from django.shortcuts import render
from blog.models import Blog

def home(request):
    return render(request, 'home.html', {'blogs': Blog.objects.all()})

## urls.py
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]

## home.html
{% extends 'base.html' %}
{% block content %}
  <h2>Blog List</h2>
  <ul>
  {% for blog in blogs %}
    <li><a href="{% url 'blog_detail' blog.pk %}">{{ blog.title }}</a></li>
  {% empty %}
    <li>No blog posts yet.</li>
  {% endfor %}
  </ul>
{% endblock %}

### Create blog detail view and template ###
## views.py
def blog_detail(request, pk):
    blog = Blog.objects.get(pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

## urls.py
from django.urls import path
from .views import home, blog_detail

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', blog_detail, name='blog_detail')
]

## blog_detail.html
{% extends 'base.html' %}
{% block content %}
  <h2>{{ blog.title }}</h2>
  <p>{{ blog.author }} <small>{{ blog.date }}</small></p>
  <hr>
  {{ blog.content|safe }}
{% endblock %} 

## Update BlogList Component in App.js ##
import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import BlogList from './components/BlogList';
import BlogDetail from './components/BlogDetail';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={BlogList} />
        <Route exact path="/blogs/:id" component={BlogDetail} />
      </Switch>
    </Router>
  );
}

export default App;

## Create BlogDetail Component ##
### BlogDetail.js ###
import React, { Component } from 'react';
import axios from 'axios';

class BlogDetail extends Component {
  state = {
    blog: null
  };

  componentDidMount() {
    const { match: { params } } = this.props;
    axios.get(`/api/blogs/${params.id}/`)
      .then(res => {
        const blog = res.data;
        this.setState({ blog });
      });
  }

  render() {
    const { blog } = this.state;
    if (blog === null) return (<p>Loading ...</p>)
    return (
      <div>
        <h2>{blog.title}</h2>
        <p>{blog.author} <small>{blog.date}</small></p>
        <hr />
        <p>{blog.content}</p>
      </div>
    );
  }
}

export default BlogDetail;

## Create appropriate url ##
### Update urls.py in blog app ###
from django.urls import path
from .views import BlogListView, BlogDetailView

urlpatterns = [
    path('api/blogs/', BlogListView.as_view()),
    path('api/blogs/<int:pk>/', BlogDetailView.as_view()),
]

### Update views.py in blog app ###
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Blog

class BlogDetailView(DetailView):
  model = Blog
  template_name = 'blog_detail.html'
  queryset = Blog.objects.all()
  context_object_name = 'blog'

  def get(self, request, *args, **kwargs):
    blog = self.get_object()
    blog_dict = {
      'id': blog.id,
      'title': blog.title,
      'content': blog.content,
      'author': blog.author.username,
      'date': blog.date.strftime("%b %d %Y"),
    }
    return JsonResponse(blog_dict, safe=False)# Implement nested comments for better organization
## Models ##
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

## Views ##
def comment_create(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CommentForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Save the comment data to the database:
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.blog = blog
            new_comment.save()
            # Redirect to blog detail view:
            return redirect('blog_detail', pk=pk)
    else:
        # Create an empty form instance:
        form = CommentForm()
    return render(request, 'comment_create.html', {'form': form})

### Templates ###
<!-- comment_create.html -->
{% extends 'base.html' %}
{% block content %}
  <h2>New Comment</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
  </form>
{% endblock %}

<!-- blog_detail.html -->
{% extends 'base.html' %}
{% block content %}
  <h2>{{ blog.title }}</h2>
  <p>{{ blog.author }} <small>{{ blog.date }}</small></p>
  <hr>
  {{ blog.content|safe }}
  <hr>
  <h3>Comments:</h3>
  <ul>
    {% for comment in blog.comment_set.all %}
      <li>{{ comment.content }} - {{ comment.author }} - {{ comment.date }}</li>
      {% if comment.replies.all %}
        <ul>
          {% for reply in comment.replies.all %}
            <li>{{ reply.content }} - {{ reply.author }} - {{ reply.date }}</li>
          {% endfor %}
        </ul>
      {% endif %}
      <hr />
    {% endfor %}
    {% if not blog.comment_set.all %}
      <p>No comments so far.</p>
    {% endif %}
  </ul>
  {% if request.user.is_authenticated %}
    <a href="{% url 'comment_create' blog.pk %}">Add New Comment+</a>
  {% else %}
    <a href="{% url 'login' %}">Login to Add Comment</a>
  {% endif %}
{% endblock %}

#JOB_COMPLETE#