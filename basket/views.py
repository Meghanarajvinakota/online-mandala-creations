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
    return redirect(redirect_url)


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    # Function for removing items from basket
    try:
        basket = request.session.get('basket', {})

        basket.pop(item_id)
        request.session['basket'] = basket
        return redirect(reverse('view_basket'))
    except Exception as e:
        # This runs if user tries to remove an item that is not in the basket
        messages.error(request, "Oops, that didn't work, please try again.")
        return redirect(reverse('home'))
