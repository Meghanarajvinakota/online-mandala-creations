from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from courses.models import Course

# Create your views here.

def view_basket(request):
    """ A view that renders the basket contents page """

    return render(request, 'basket/basket.html')

def add_to_basket(request, item_id):

    # Function for adding items to the basket
    course = get_object_or_404(Course, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url', reverse('view_basket'))
    basket = request.session.get('basket', {})

    # checks if item is already in basket
    if item_id in list(basket.keys()):
        messages.error(request, f'{course.name} is already in your basket!')
    else:
        basket[item_id] = quantity
        messages.success(request, f'{course.name} was added to your basket')

    request.session['basket'] = basket
    print(request.session['basket'])
    return redirect(redirect_url)
