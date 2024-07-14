from typing import Any
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from electronics.models import Contact, Factory, Network, Product, Seller


class CityFilter(SimpleListFilter):
    title = _("Город")
    parameter_name = "contact"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        contact_ids = model_admin.get_queryset(request).all().values("contact")
        queryset = Contact.objects.filter(id__in = contact_ids).order_by("city").distinct("city")
        return queryset.values_list("city", "city")

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            contacts = Contact.objects.filter(city = self.value())
            queryset = queryset.filter(contact__id__in = contacts)
            return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "model", "release_date")


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "created_at")
    list_filter = [CityFilter]


@admin.action(description="Очистить задолженности у выбранных")
def set_debt_to_zero(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "supplier", "created_at", "debt")
    actions = [set_debt_to_zero]
    list_filter = [CityFilter]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "supplier_display", "created_at", "debt")
    actions = [set_debt_to_zero]
    list_filter = [CityFilter]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house")
