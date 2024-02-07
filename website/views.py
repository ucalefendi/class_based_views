from typing import Any
from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView,RedirectView
from . models import Post
from django.db.models import F

# Create your views here.

class Ex2view(TemplateView):
    """
    TemplateResponseMixin
    Provides a mechanism to construct a Templateresponse,given suitable contex.
    Attributes:
    """
    template_name = 'ex2.html'
    # template_engine = The NAME of a template engine to use for template loading template. (Jinja2,Genshi)
    #response_class = Custom template loading or custom context object instantiation
    #content_type = Default Django uses 'txt/html'

    """
    get_context_data(**kwargs) i a method inherited from ContextMixin
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.get(id=1)
        context['daata'] = 'Context data for ex2'
        return context
    

class PostPreloadTaskView(RedirectView):

    #url='http://youtube.com/veryacademy'

    pattern_name = 'website:singlepost'

    def get_redirect_url(self,*args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'])
        post.update(count=F('count')+1)
        

        return super().get_redirect_url(*args,**kwargs)
    
class SinglePostView(TemplateView):
    template_name = 'ex4.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_object_or_404(Post,pk=self.kwargs.get('pk'))
        return context
    
          

