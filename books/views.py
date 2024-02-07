from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import F
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import AddForm
from . models import Books
from django.utils import timezone
# Create your views here.








""" class AddBookView(FormView):

    template_name = 'add.html'
    form_class = AddForm
    success_url = '/books/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
     """

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self,request,*args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(),self.get_login_url(),
                                    self.redirect_field_name())
        if not self.has_permission():
            return redirect('/books')
        return super(UserAccessMixin,self).dispatch(self,*args, **kwargs)

class BookEditView(UserAccessMixin,PermissionRequiredMixin):


    raise_exception = False
    permission_required = 'books.schange_books'
    permission_denied_message = '/books/'

    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'



class AddBookView(CreateView):
    model = Books
    # fields = ['title']
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'

    def get_initial(self,*args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['title'] = 'Enter title'
        return initial
    
    
    




# class IndexView(TemplateView):
#     template_name = "home.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Books.objects.all()
#         return context



class IndexView(ListView):

    model = Books
    template_name = "home.html"
    context_object_name = "books"
    paginate_by = 4

    # queryset = Books.objects.all()[:2]

    def get_queryset(self):
        queryset = Books.objects.all()
        return queryset
        
class GenreView(ListView):

    model = Books
    template_name = "book-detail.html"
    context_object_name = "book"
    paginate_by = 2 #Pagination-over-write

    def get_queryset(self,*args,**kwargs):
        return Books.objects.filter(genre__icontains=self.kwargs.get('genre'))
            

    




class BookDetailView(DetailView):

    model = Books
    template_name = 'book_detail.html'
    context_object_name = 'book'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Books.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count') + 1)

        context['time'] = timezone.now()
        return context

