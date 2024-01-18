from django.shortcuts import render, redirect

from . models import Category, Product, Comment
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def store(request):

    all_products = Product.objects.all()

    context = {'my_products':all_products}

    return render(request, 'store/store.html', context)



def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}



def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)
    
    paginator = Paginator(products, 15)  # Show 15 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'store/list-category.html', {'category':category, 'products':products, "page_obj": page_obj})



def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)
    
    comments = Comment.objects.filter(listing=product)

    context = {'product': product, 'comments': comments}

    return render(request, 'store/product-info.html', context)


@login_required(redirect_field_name='account/my-login')
def createsubmit(request):
    if request.method == "POST":
        listing = Product()
        listing.user = request.user
        listing.title = request.POST.get('title')
        listing.brand = request.POST.get('brand')
        listing.description = request.POST.get('description')
        listing.price = request.POST.get('price')
        category_name = request.POST.get('category')
        category_instance, created = Category.objects.get_or_create(name=category_name)
        category_instance.save()
        listing.category = category_instance
        listing.image = request.POST.get('filename')
        listing.save()
        return redirect('store')
    else:
       
        return render(request, 'store/store.html')


@login_required(login_url='account/my-login')
def cmntsubmit(request, listingid):
    if request.method == 'POST':
        comnt = request.POST.get('comment')
        comment = Comment()
        comment.user = request.user.username
        comment.comment = comnt
        comment.comment_listingid = listingid
        product = get_object_or_404(Product, id=listingid)
        comment.listing = product
        comment.save()
        url = reverse('product-info', kwargs={'product_slug': product.slug})
        return redirect(url)
    else:
        return redirect(url)
    



def create(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, "store/create.html", context)
