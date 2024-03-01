from django.shortcuts import render

# Create your views here.
def index(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/index.html', context=context_dict)
    return response

def about(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/about.html', context=context_dict)
    return response