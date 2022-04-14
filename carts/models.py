from django.db import models
from accounts.models import Account
from store.models import Product, Variation


class Cart(models.Model):
    cart_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_user)


class CartItem(models.Model):
    variations = models.ManyToManyField(Variation, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)

    # const totalPrice = cart.reduce(
    #   (acc, cur) => acc + cur.quantity * cur.product.price,
    #   0
    # );
    #
    # const totalTax = totalPrice * 0.03;
    # const grandTotal = totalPrice + totalTax;
    # console.log("grandtoal", grandTotal);
