from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre'
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre'
    )

    description = models.TextField(
        verbose_name='Descripción'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price'
    )

    is_active = models.BooleanField(
        default=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Categoría'
    )

    @classmethod
    def crear_con_categoria_default(
        cls,
        name,
        description,
        price
    ):
        categoria_default, _ = Category.objects.get_or_create(
            name='Sin categoría'
        )

        return cls.objects.create(
            name=name,
            description=description,
            price=price,
            category=categoria_default
        )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name