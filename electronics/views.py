from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from electronics.models import Factory, Network, Prod_fact, Prod_net, Prod_sell, Product
from electronics.paginators import ItemPaginator
from electronics.serializers import ProductSerializer

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = ItemPaginator

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            supplier = data.pop("supplier_choice")
            supplier_id = data.pop("supplier_id")
        except:
            raise ValidationError("supplier should be attached")
        instance = self.get_serializer(data=data)
        instance.is_valid(raise_exception=True)
        new_product = Product.objects.create(instance)
        match supplier:
            case "factory":
                supplier = Factory.objects.filter(id=supplier_id)
                if supplier.exists():
                    supplier = supplier.first()
                else:
                    raise ValidationError(
                        "supplier id does't match any factory supplier"
                    )
                prod_fact = Prod_fact.objects.create(
                    product=new_product, supplier=supplier
                )
                prod_fact.save()
            case "network":
                supplier = Network.objects.filter(id=supplier_id)
                if supplier.exists():
                    supplier = supplier.first()
                else:
                    raise ValidationError(
                        "supplier id doesn't match any network supplier"
                    )
                prod_net = Prod_net.objects.create(
                    product=new_product, supplier=supplier
                )
                prod_net.save()
            case "seller":
                supplier = Network.objects.filter(id=supplier_id)
                if supplier.exists():
                    supplier = supplier.first()
                else:
                    raise ValidationError(
                        "supplier id doesn't match any seller supplier"
                    )
                prod_sell = Prod_sell.objects.create(
                    product=new_product, supplier=supplier
                )
                prod_sell.save()
            case _:
                raise ValidationError("choise correct supplier")
        new_product.save()
