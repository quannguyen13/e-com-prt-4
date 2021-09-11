import stripe 
from django.conf import settings
from .cart import Cart
from .forms import CheckoutForm
from django.contrib import messages

from django.shortcuts import redirect, render
from apps.order.ultilities import checkout


def cart_detail(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():    
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            charge = stripe.Charge.create(
                amount=int(cart.get_total_cost() * 100),
                currency='USD',
                description='you have been charged',
                source=stripe_token
            )
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            city = form.cleaned_data['city']
            
            order = checkout(request, first_name, last_name, email, address, zipcode, city, phone, cart.get_total_cost())

            cart.clear()

            return redirect('success')
    else:
        form = CheckoutForm()
            



    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)


    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    # return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

    return render(request, 'cart/cart.html', {
        # 'form': form,
         'stripe_pub_key': settings.STRIPE_PUB_KEY
    })

def success(request):
    return render(request, 'cart/success.html')