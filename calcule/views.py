from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from calcule.calculations import (
    calculate_cpi_cost,
    calculate_book_weight,
    get_shipping_cost,
    calculate_order,
    country_zone,
)


def index(request):
    return render(request, 'index.html')


def cpi_book_price_calculator(request):
    if request.method == 'POST':
        total_pages = int(request.POST['total_pages'])
        color_pages = int(request.POST['color_pages'])
        cover_type = request.POST.get('cover_type', 'Soft Cover').strip().title()
        copies = int(request.POST['copies'])

        if total_pages <= 0 or color_pages < 0 or copies <= 0:
            return render(
                request,
                'index.html',
                {
                    'calculator': 'cpi_book_price',
                    'invalid_input': True,
                    'total_pages': total_pages,
                    'color_pages': color_pages,
                    'cover_type': cover_type,
                    'copies': copies,
                }
            )

        result = calculate_cpi_cost(total_pages, color_pages, copies, cover_type)
        return render(
            request,
            'index.html',
            {
                'calculator': 'cpi_book_price',
                'show_result': True,
                'result': result,
                'total_pages': total_pages,
                'color_pages': color_pages,
                'cover_type': cover_type,
                'copies': copies,
            }
        )
    return render(request, 'index.html', {'calculator': 'cpi_book_price'})


def shipping_calculator(request):
    country_list = sorted(set(name.title() for name in country_zone.keys()))

    if request.method == 'POST':
        page_count = int(request.POST['page_count'])
        cover_type = request.POST['cover_type']
        copies = int(request.POST['copies'])
        country = request.POST['country'].strip()

        if page_count <= 0 or copies <= 0:
            return render(
                request,
                'index.html',
                {
                    'calculator': 'shipping',
                    'invalid_input': True,
                    'page_count': page_count,
                    'cover_type': cover_type,
                    'copies': copies,
                    'country': country,
                    'country_list': country_list,
                }
            )

        total_weight_kg = calculate_book_weight(page_count, cover_type) * copies
        zone = country_zone.get(country)
        if zone:
            cost = get_shipping_cost(total_weight_kg, zone)
            return render(
                request,
                'index.html',
                {
                    'calculator': 'shipping',
                    'show_result': True,
                    'result': {
                        'country': country,
                        'copies': copies,
                        'total_weight': round(total_weight_kg, 3),
                        'shipping_cost': cost if cost else 'Not Available',
                    },
                    'page_count': page_count,
                    'cover_type': cover_type,
                    'copies': copies,
                    'country': country,
                    'country_list': country_list,
                }
            )
        return render(
            request,
            'index.html',
            {
                'calculator': 'shipping',
                'show_result': True,
                'result': {
                    'country': country,
                    'copies': copies,
                    'total_weight': round(total_weight_kg, 3),
                    'shipping_cost': 'Not Available',
                },
                'page_count': page_count,
                'cover_type': cover_type,
                'copies': copies,
                'country': country,
                'country_list': country_list,
            }
        )

    return render(request, 'index.html', {'calculator': 'shipping', 'country_list': country_list})


from django.shortcuts import render

# Add this function to pass the country list from the calculations.py file
def get_country_list():
    return list(country_zone.keys())

def order_calculator(request):
    country_list = get_country_list()

    if request.method == 'POST':
        total_pages = int(request.POST['total_pages'])
        color_pages = int(request.POST['color_pages'])
        cover_type = request.POST.get('cover_type', 'Soft')  # Default to "Soft"
        copies = int(request.POST['copies'])
        country = request.POST['country']

        if cover_type == "Soft":
            cover_type = "Soft Cover"
        elif cover_type == "Hard":
            cover_type = "Hard Cover"

        if total_pages <= 0 or color_pages < 0 or copies <= 0:
            return render(
                request,
                'index.html',
                {
                    'calculator': 'order',
                    'invalid_input': True,
                    'total_pages': total_pages,
                    'color_pages': color_pages,
                    'cover_type': cover_type,
                    'copies': copies,
                    'country': country,
                    'country_list': country_list  # Pass the country list to the template
                }
            )

        result = calculate_order(total_pages, color_pages, copies, cover_type, country)
        return render(
            request,
            'index.html',
            {
                'calculator': 'order',
                'show_result': True,
                'result': result,
                'total_pages': total_pages,
                'color_pages': color_pages,
                'cover_type': cover_type,
                'copies': copies,
                'country': country,
                'country_list': country_list  # Pass the country list to the template
            }
        )
    return render(request, 'index.html', {'calculator': 'order', 'country_list': country_list})

def weight_calculator(request):
    if request.method == 'POST':
        total_pages = int(request.POST.get('total_pages', 0))
        color_pages = int(request.POST.get('color_pages', 0))
        cover_type = request.POST.get('cover_type', 'Soft Cover').strip().title()
        copies = int(request.POST.get('copies', 1))

        if cover_type not in ['Soft Cover', 'Hard Cover']:
            cover_type = 'Soft Cover'

        try:
            # Calculate the total weight of the book (including cover)
            total_book_weight_kg = calculate_book_weight(total_pages, cover_type)

            # Calculate the weight of the cover
            cover_weight_kg = calculate_book_weight(0, cover_type)

            # Calculate B&W pages weight only if color_pages is less than total_pages
            if color_pages > 0:
                bw_pages_weight = calculate_book_weight(total_pages - color_pages, cover_type) - cover_weight_kg
                color_pages_weight = calculate_book_weight(color_pages, cover_type) - cover_weight_kg
            else:
                bw_pages_weight = calculate_book_weight(total_pages, cover_type) - cover_weight_kg
                color_pages_weight = 0.0

            # Multiply by the number of copies
            total_weight_all_books_kg = total_book_weight_kg * copies

            # Prepare the context dictionary
            context = {
                'calculator': 'weight',
                'show_result': True,
                'result': {
                    'cover_weight': round(cover_weight_kg, 3),
                    'bw_pages_weight': round(bw_pages_weight, 3),
                    'color_pages_weight': round(color_pages_weight, 3),
                    'total_weight': round(total_weight_all_books_kg, 3),
                },
                'total_pages': total_pages,
                'color_pages': color_pages,
                'cover_type': cover_type,
                'copies': copies,
            }
        except ValueError as e:
            context = {
                'calculator': 'weight',
                'invalid_input': True,
                'error_message': str(e),
                'total_pages': total_pages,
                'color_pages': color_pages,
                'cover_type': cover_type,
                'copies': copies,
            }
        return render(request, 'index.html', context)

    return render(request, 'index.html', {'calculator': 'weight'})
