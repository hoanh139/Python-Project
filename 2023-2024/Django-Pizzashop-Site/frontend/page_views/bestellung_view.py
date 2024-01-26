from django.views.generic import TemplateView


class BestellungView(TemplateView):
    template_name = 'pages/bestellung.html'
