from django.shortcuts import render, redirect, get_object_or_404
from .models import caja, parle, tipo_de_pieza, pieza
from django import forms
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

def hola(request):
    return render(request, 'index.html')

def listar_cajas(request, parle_id=None):
    cajas = caja.objects.all()
    Parle = None
    
    if parle_id:
        Parle = get_object_or_404(parle, id=parle_id)
        cajas = cajas.filter(id_parle=Parle)
    
    return render(request, 'caja/list.html', {
        'cajas': cajas,
        'parle_filtrado': Parle
    })

class CajaForm(forms.ModelForm):
    # Campos para nuevo Tipo_de_pieza
    nuevo_tipo_nombre = forms.CharField(
        max_length=200,
        required=False,
        label="Nombre del nuevo tipo de pieza"
    )
    nuevo_tipo_tipo = forms.CharField(
        max_length=200,
        required=False,
        label="Tipo del nuevo tipo de pieza"
    )
    
    # Campo para seleccionar Tipo_de_pieza existente
    tipo_existente = forms.ModelChoiceField(
        queryset=tipo_de_pieza.objects.all(),  # Nombres únicos
        required=False,
        label="Seleccionar tipo existente",
        widget=forms.Select(attrs={'class': 'mi-clase-css'})  # Opcional: estilos
    )

    parle = forms.ModelChoiceField(
        queryset=parle.objects.all().order_by('nombre'),  # Ordenados por nombre
        required=False,
        label="Seleccionar Parle"
    )

    class Meta:
        model = caja
        fields = ['nombre', 'id_parle', 'cant_piezas']

    def clean(self):
        cleaned_data = super().clean()
        nuevo_tipo_nombre = cleaned_data.get('nuevo_tipo_nombre')
        nuevo_tipo_tipo = cleaned_data.get('nuevo_tipo_tipo')
        tipo_existente = cleaned_data.get('tipo_existente')

        # Validar que se ingrese un tipo nuevo o se seleccione uno existente
        if not tipo_existente and (not nuevo_tipo_nombre or not nuevo_tipo_tipo):
            raise forms.ValidationError(
                "Debes seleccionar un tipo existente o ingresar uno nuevo."
            )

        return cleaned_data

    def save(self, commit=True):
        caja = super().save(commit=commit)
        tipo_existente = self.cleaned_data.get('tipo_existente')
        nuevo_tipo_nombre = self.cleaned_data.get('nuevo_tipo_nombre')
        nuevo_tipo_tipo = self.cleaned_data.get('nuevo_tipo_tipo')

        # Crear el Tipo_de_pieza según la opción elegida
        if tipo_existente:
            # Crear un nuevo tipo con los datos del existente (pero vinculado a la nueva caja)
            tipo_de_pieza.objects.create(
                nombre=tipo_existente.nombre,
                tipo=tipo_existente.tipo,
                id_caja=caja
            )
        else:
            # Crear un nuevo tipo con los datos ingresados
            tipo_de_pieza.objects.create(
                nombre=nuevo_tipo_nombre,
                tipo=nuevo_tipo_tipo,
                id_caja=caja
            )

        return caja

def registrarCaja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_caja')  # Redirige a una vista de listado
    else:
        form = CajaForm()
    
    return render(request, 'caja/create.html', {'form': form})

def eliminar_caja(request, id):
    if request.method == 'POST':
        Caja = get_object_or_404(caja, id=id)
        Caja.delete()
    return redirect('listar_caja')

class EditarCajaForm(forms.ModelForm):
    class Meta:
        model = caja
        fields = ['nombre', 'cant_piezas', 'id_parle']  # Campos a editar
        labels = {
            'id_parle': 'Parle asociado'  # Etiqueta más amigable
        }

def editar_caja(request, id):
    Caja = get_object_or_404(caja, id=id)  # Obtiene la caja a editar
    
    if request.method == 'POST':
        form = EditarCajaForm(request.POST, instance=Caja)
        if form.is_valid():
            form.save()
            return redirect('listar_caja')  # Redirige al listado
    else:
        form = EditarCajaForm(instance=Caja)  # Formulario con datos actuales
    
    return render(request, 'caja/edit.html', {'form': form, 'caja': Caja})

def contenido_caja(request, id):
    Caja = get_object_or_404(caja, id=id)  # Instancia
    piezas = Caja.piezas.all()  # Acceso correcto
    return render(request, 'pieza/list.html', {'caja': Caja, 'piezas': piezas})

class AgregarPiezaForm(forms.ModelForm):
    class Meta:
        model = pieza
        fields = ['codigo', 'nombre', 'tipo']  # Añade 'codigo'
        labels = {
            'codigo': 'Código Único'
        }

def agregar_pieza(request, id):
    Caja = get_object_or_404(caja, id=id)
    piezas = Caja.piezas.all()  # Usando el related_name
    
    if request.method == 'POST':
        form = AgregarPiezaForm(request.POST)
        if form.is_valid():
            nueva_pieza = form.save(commit=False)
            nueva_pieza.id_caja = Caja  # Asigna la caja automáticamente
            nueva_pieza.save()
            return redirect('contenido_caja', id=id)  # Recarga la página
    else:
        form = AgregarPiezaForm()
    
    return render(request, 'caja/create.html', {
        'caja': Caja,
        'piezas': piezas,
        'form': form
    })

def eliminar_pieza(request, id):
    Pieza = get_object_or_404(pieza, id=id)
    caja_id = Pieza.id_caja.id  # Guardamos el ID de la caja antes de eliminar
    
    if request.method == 'POST':
        Pieza.delete()
    
    return redirect('contenido_caja', id=caja_id)

class EditarPiezaForm(forms.ModelForm):
    class Meta:
        model = pieza
        fields = ['codigo', 'nombre', 'tipo']  # Campos editables
        labels = {
            'codigo': 'Código Único',
            'nombre': 'Nombre',
            'tipo': 'Tipo de Pieza'
        }

def editar_pieza(request, id):
    # Obtiene la pieza a editar
    Pieza = get_object_or_404(pieza, id=id)
    
    if request.method == 'POST':
        # Procesa el formulario con los datos actualizados
        form = EditarPiezaForm(request.POST, instance=Pieza)
        if form.is_valid():
            form.save()
            return redirect('contenido_caja', id=Pieza.id_caja.id)  # Redirige a la caja
    else:
        # Muestra el formulario con los datos actuales de la pieza
        form = EditarPiezaForm(instance=Pieza)
    
    return render(request, 'pieza/edit.html', {
        'form': form,
        'pieza': Pieza
    })

def parles_dashboard(request):
    Parles = parle.objects.all()
    return render(request, 'parles/dashboard.html', {'parles': Parles})

def crear_parle(request):
    if request.method == 'POST':
        # Obtener el último Parle
        ultimo_parle = parle.objects.order_by('-id').first()
        
        # Calcular posición
        if ultimo_parle:
            nueva_x = ultimo_parle.pos_x + ultimo_parle.ancho + 20  # 20px de separación
            nueva_y = ultimo_parle.pos_y
        else:
            nueva_x = 50  # Posición inicial X
            nueva_y = 50  # Posición inicial Y
        
        # Crear Parle
        nuevo_parle = parle.objects.create(
            pos_x=nueva_x,
            pos_y=nueva_y,
            ancho=200,
            alto=150
        )
        
        return JsonResponse({
            'id': nuevo_parle.id,
            'nombre': nuevo_parle.nombre,
            'pos_x': nuevo_parle.pos_x,
            'pos_y': nuevo_parle.pos_y,
            'ancho': nuevo_parle.ancho,
            'alto': nuevo_parle.alto
        })
    return redirect('parles_dashboard')

@require_http_methods(["POST"])
def actualizar_parle(request, id):
    Parle = get_object_or_404(parle, id=id)
    data = json.loads(request.body)
    
    if 'x' in data and 'y' in data:
        Parle.pos_x = data['x']
        Parle.pos_y = data['y']
    
    if 'width' in data and 'height' in data:
        Parle.ancho = data['width']
        Parle.alto = data['height']
    
    Parle.save()  # <-- ¡Aquí estaba el error! (Parle, no parle)
    return JsonResponse({'status': 'success'})

def eliminar_parle(request, id):
    if request.method == 'POST':
        Parle = parle.objects.get(id=id)
        Parle.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@require_http_methods(["POST"])
def actualizar_parle(request, id):
    Parle = get_object_or_404(parle, id=id)
    data = json.loads(request.body)
    
    # Actualizar posición
    if 'x' in data and 'y' in data:
        Parle.pos_x = data['x']
        Parle.pos_y = data['y']
    
    # Actualizar tamaño
    if 'width' in data and 'height' in data:
        Parle.ancho = data['width']
        Parle.alto = data['height']
    
    parle.save()
    return JsonResponse({'status': 'success'})

@require_http_methods(["POST"])
def actualizar_nombre_parle(request, id):
    Parle = get_object_or_404(parle, id=id)
    try:
        data = json.loads(request.body)
        nuevo_nombre = data.get('nombre', '').strip()
        
        if not nuevo_nombre:
            return JsonResponse({'status': 'error', 'message': 'Nombre vacío'}, status=400)
        
        Parle.nombre = nuevo_nombre
        Parle.save()
        return JsonResponse({'status': 'success', 'nombre': Parle.nombre})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)