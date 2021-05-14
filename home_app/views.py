from django.shortcuts import render, redirect
from .models import Task
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RegisterPage(FormView):
    template_name = 'home_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True      # didin't work
    success_url = reverse_lazy('home_app:tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):     # an already logged in user will be redirected
        if self.request.user.is_authenticated:
            return redirect('home_app:tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'home_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True   # an already logged in user will be redirected

    def get_success_url(self):
        return reverse_lazy('home_app:tasks')

# Create your views here.
class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' # custom name
    # task_list.html is the template
    def get_context_data(self, **kwargs):               # for showing only logged in users list
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) # context_object_name
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context
    

class DetailTask(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'home_app/task.html' # custom name and path

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ('title', 'description', 'complete')
    success_url = reverse_lazy('home_app:tasks') # only works when you submit the form
    # task_form.html is the template

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ('title', 'description', 'complete')
    success_url = reverse_lazy('home_app:tasks')
    def get(self, *args, **kwargs):
        print(self.request.user.id)     # User class
        # print(Task.objects.filter(user=self.request.user.id))
        print('hello')
        return super(TaskUpdate, self).get(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task' # custom name
    success_url = reverse_lazy('home_app:tasks')