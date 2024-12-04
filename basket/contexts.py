from django.shortcuts import get_object_or_404
from courses.models import Course

def basket_contents(request):

    # declare the basket items list
    basket_items = []
    total = 0
    course_count = 0
    basket = request.session.get('basket', {})

    # populate the basket list
    for item_id, quantity in basket.items():
        course = get_object_or_404(Course, pk=item_id)
        total += quantity * course.price
        course_count += quantity
        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'course': course,
        })

    grand_total = total

    # get the basket totals
    context = {
        'basket_items': basket_items,
        'total': total,
        'course_count': course_count,
        'grand_total': grand_total,
    }

    return context