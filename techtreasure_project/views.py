from django.shortcuts import render

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = most_viewed

    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response
