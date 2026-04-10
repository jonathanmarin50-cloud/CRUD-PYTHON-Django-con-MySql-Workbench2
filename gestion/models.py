"""
Modelos de la aplicación de gestión de pedidos.
Aquí definimos la estructura de nuestra base de datos (las tablas), los campos 
que tendrá cada una y las relaciones entre ellas.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# ============================================================
#  MODELO: CLIENTE
# ============================================================
class Cliente(models.Model):
    """
    Representa a los compradores del sistema.
    Explicación: Esta es una tabla independiente que guarda los datos personales de cada cliente.
    """
    nombre = models.CharField(max_length=150, verbose_name="Nombre completo")
    correo = models.EmailField(unique=True, verbose_name="Correo electrónico")
    direccion = models.TextField(verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    
    # auto_now_add: Se pone la fecha actual automáticamente al crear el registro.
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre'] # Ordenar alfabéticamente por nombre de forma predeterminada.

    def __str__(self):
        """Cómo se muestra el objeto cuando lo imprimimos o lo vemos en el Admin."""
        return self.nombre


# ============================================================
#  MODELO: PRODUCTO
# ============================================================
class Producto(models.Model):
    """
    Representa los artículos que se venden.
    Regla de negocio: Usamos DecimalField para el precio para evitar errores de redondeo matemáticos.
    """
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Precio unitario",
        validators=[MinValueValidator(Decimal('0.01'))] # El precio no puede ser cero ni negativo.
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock disponible"
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"


# ============================================================
#  MODELO: PEDIDO
# ============================================================
class Pedido(models.Model):
    """
    Representa la 'cabecera' de una venta.
    Concepto clave: El ForeignKey conecta este pedido con un Cliente específico (Relación 1 a Muchos).
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]

    # ForeignKey: Crea el vínculo con la tabla de Clientes.
    # on_delete=models.PROTECT: Impide borrar el cliente si tiene pedidos, protegiendo la integridad de datos.
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,  
        related_name='pedidos',
        verbose_name="Cliente"
    )
    fecha = models.DateField(verbose_name="Fecha del pedido")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        verbose_name="Estado"
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha'] # Los más recientes aparecen primero.

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"

    def total(self):
        """
        Método de lógica de negocio:
        Calcula el total general del pedido sumando todos los subtotales de sus productos.
        """
        return sum(detalle.subtotal for detalle in self.detalles.all())


# ============================================================
#  MODELO: DETALLE DE PEDIDO
# ============================================================
class DetallePedido(models.Model):
    """
    Esta es la tabla de 'detalle' o 'renglón' del pedido.
    Explica que un pedido puede tener muchos productos. Aquí guardamos la cantidad de cada uno.
    """
    # Vincula este detalle con un pedido padre.
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE, # Si borro el pedido padre, se borran sus detalles automáticamente.
        related_name='detalles',
        verbose_name="Pedido"
    )
    # Vincula este detalle con un producto del inventario.
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles',
        verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad",
        validators=[MinValueValidator(1)] # Debe comprar al menos 1.
    )
    # editable=False: El usuario no lo escribe, se calcula por código automáticamente.
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2,
        editable=False,
        default=Decimal('0.00'),
        verbose_name="Subtotal"
    )

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedido"

    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para automatizar cálculos.
        Calculamos el subtotal (precio * cantidad) justo antes de guardar en MySQL.
        """
        self.subtotal = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} = ${self.subtotal}"
