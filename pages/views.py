from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomePageView(TemplateView):
  template_name = 'index.html'



class ContactTemplateView(TemplateView):
  template_name = 'pages/contact.html'

  def get_context_data(self, *args, **kwargs):
    context = super(ContactTemplateView, self).get_context_data(*args, **kwargs)
    context['name'] = 'contact'
    return context