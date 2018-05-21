from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ..models import Item
from ..forms import ItemForm

__all__ = (
    'item_add',
)


@login_required
def item_add(request):
    if not request.user.is_authenticated:
        return redirect('members:login')

    if request.method == 'POST':
        item_name = request.POST['name']
        item_purchase_url = request.POST['purchase_url']
        item_price = request.POST['price']
        item_category = request.POST['category']
        item_img = request.POST['img']
        item_public_visibility = request.POST['public_visibility']
        if item_public_visibility == 'on':
            item_public_visibility = True
        else:
            item_public_visibility = False
        Item.objects.create(
            user=request.user,
            name=item_name,
            purchase_url=item_purchase_url,
            price=item_price,
            category=item_category,
            img=item_img,
            public_visibility=item_public_visibility,
        )
        return redirect('items:my-item-list')

        # form = ItemForm(request.POST, request.FILES)
        # if form.is_valid():
        #     item = form.save(commit=False)
        #     item.user = request.user
        #     item.save()

    # else:
    #     form = ItemForm()
    #
    # context = {
    #     'form': form,
    # }
    # return render(request, 'items/my_item/item_search.html', context)
