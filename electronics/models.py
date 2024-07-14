from django.db import models
from django.contrib import admin


class Contact(models.Model):
    email = models.EmailField(max_length=100, unique=True, verbose_name="Почта")
    country = models.CharField(verbose_name="Страна", max_length=50)
    city = models.CharField(verbose_name="Город", max_length=50)
    street = models.CharField(verbose_name="Улица", max_length=50)
    house = models.PositiveSmallIntegerField(verbose_name="Дом")

    def __str__(self) -> str:
        return f"{self.email}, {self.country}, {self.city}, {self.street}, {self.house}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = [
            "id",
        ]


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование", unique=True)
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateTimeField(verbose_name="Дата выхода на рынок")

    def __str__(self) -> str:
        return f"{self.title} {self.model}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = [
            "id",
            "release_date",
        ]


class Factory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    created_at = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.contact}"

    class Meta:
        verbose_name = "Фабрика"
        verbose_name_plural = "Фабрики"
        ordering = [
            "id",
            "name",
        ]


class Network(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    supplier = models.ForeignKey(
        Factory, on_delete=models.CASCADE, verbose_name="Поставщик"
    )
    debt = models.PositiveIntegerField(verbose_name="Задолженность", default=0)
    created_at = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.contact}"

    class Meta:
        verbose_name = "Розничная сеть"
        verbose_name_plural = "Розничные сети"
        ordering = [
            "id",
            "name",
        ]


class Seller(models.Model):
    class SupplierChoice(models.TextChoices):
        FACTORY = "1", "Фабрика"
        NETWORK = "2", "Розничная сеть"

    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    supplier_choice = models.CharField(
        choices=SupplierChoice.choices,
        default=SupplierChoice.NETWORK,
        verbose_name="Поставщик",
    )
    supplier_factory = models.ForeignKey(
        Factory,
        on_delete=models.CASCADE,
        verbose_name="Поставщик (фабрика)",
        blank=True,
        null=True,
    )
    supplier_network = models.ForeignKey(
        Network,
        on_delete=models.CASCADE,
        verbose_name="Поставщик (розничная сеть)",
        blank=True,
        null=True,
    )
    debt = models.PositiveIntegerField(verbose_name="Задолженность", default=0)
    created_at = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.contact}"
    
    @admin.display(description="Поставщик")
    def supplier_display(self):
        if self.supplier_choice == "1":
            supplier = f"фабрика {self.supplier_factory}"
        else:
            supplier = f"сеть {self.supplier_network}"
        return supplier 

    class Meta:
        verbose_name = "Предпрениматель"
        verbose_name_plural = "Предпрениматели"
        ordering = [
            "id",
            "name",
        ]


class Prod_fact(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    factory = models.ForeignKey(
        Factory, on_delete=models.CASCADE, verbose_name="Фабрика"
    )


class Prod_net(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    network = models.ForeignKey(Network, on_delete=models.CASCADE, verbose_name="Сеть")


class Prod_sell(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, verbose_name="Предпрениматель"
    )
