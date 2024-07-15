from rest_framework import serializers

from electronics.models import Contact, Factory, Product, Seller
from electronics.validators import ReleaseDateValidator, SupplierValidator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            "id",
        ]
        validators = [ReleaseDateValidator(field="release_date")]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = [
            "id",
        ]


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = "__all__"


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        validators = [SupplierValidator(fields = ["supplier_choice", "supplier_factory", "supplier_network"])]
