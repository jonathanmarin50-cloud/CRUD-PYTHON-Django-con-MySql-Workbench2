"""
Formularios de la aplicación de gestión de pedidos.
Django usa estos archivos para generar automáticamente el código HTML de los 
formularios y validar que los datos ingresados por el usuario sean correctos.
"""
from django import forms
from .models import Cliente, Producto, Pedido, DetallePedido


# ============================================================
#  FORMULARIO: CLIENTE
# ============================================================
class ClienteForm(forms.ModelForm):
    """
    Formulario vinculado al modelo Cliente.
    Se usa tanto para CREAR como para EDITAR clientes.
    """
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'direccion', 'telefono']
        # Los 'widgets' definen la apariencia (CSS) de cada campo en el navegador.
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nombre completo del cliente'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: 300 123 4567'
            }),
        }

    def clean_telefono(self):
        """
        Validación personalizada para el teléfono.
        Lógica: El sistema no acepta números muy cortos.
        """
        telefono = self.cleaned_data.get('telefono', '')
        if len(telefono.strip()) < 7:
            raise forms.ValidationError("El teléfono debe tener al menos 7 dígitos.")
        return telefono


# ============================================================
#  FORMULARIO: PRODUCTO
# ============================================================
class ProductoForm(forms.ModelForm):
    """Formulario para gestionar el inventario de productos."""
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nombre del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0', 'placeholder': '0'
            }),
        }

    def clean_stock(self):
        """Regla de negocio: No permitimos que el stock sea negativo."""
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock


# ============================================================
#  FORMULARIO: PEDIDO
# ============================================================
class PedidoForm(forms.ModelForm):
    """Formulario para la cabecera del pedido (Cliente y Fecha)."""
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
#  FORMULARIO: DETALLE DE PEDIDO
# ============================================================
class DetallePedidoForm(forms.ModelForm):
    """Formulario para elegir productos y cantidades dentro de un pedido."""
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select', 'id': 'id_producto'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '1', 'id': 'id_cantidad', 'placeholder': '1'
            }),
        }

    def clean(self):
        """
        Validación avanzada de Lógica de Negocio:
        Verifica que el usuario no intente vender más productos de los que existen en stock.
        """
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            if cantidad > producto.stock:
                # Si no hay stock, lanzamos un error que se mostrará en rojo en la web.
                raise forms.ValidationError(
                    f"¡Error! Solo quedan {producto.stock} unidades de '{producto.nombre}' en el inventario."
                )
        return cleaned_data
