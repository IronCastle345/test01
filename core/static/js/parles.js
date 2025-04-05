document.addEventListener('DOMContentLoaded', () => {
    const parleMap = document.getElementById('parle-map'); 
    // Inicializar interact.js en los Parles existentes
    document.querySelectorAll('.parle-box').forEach(element => {
        addInteractions(element);
        applyParleStyles(element);
    });

    function applyParleStyles(element) {
        element.style.position = 'absolute';
        element.style.left = `${element.dataset.x}px`;
        element.style.top = `${element.dataset.y}px`;
        element.style.width = `${element.dataset.width}px`;
        element.style.height = `${element.dataset.height}px`;
    }

    // Crear elemento HTML para un parle
    function createParleElement(parle) {
        const div = document.createElement('div');
        div.className = 'parle-box';
        div.setAttribute('data-id', parle.id);
        
        // Posición y tamaño desde el backend
        div.style.left = `${parle.pos_x}px`;
        div.style.top = `${parle.pos_y}px`;
        div.style.width = `${parle.ancho}px`;
        div.style.height = `${parle.alto}px`;
        
        // Contenido
        div.innerHTML = `
            <h5>${parle.nombre}</h5>
            <p>Cajas: ${parle.cant_cajas}</p>
            <button class="btn btn-sm btn-success view-boxes">Ver Cajas</button>
            <button class="btn btn-sm btn-danger delete-parle">Eliminar</button>
        `;
        
        parleMap.appendChild(div);
        addInteractions(div);
    }

    // Añadir interacciones (arrastrar, redimensionar)
    function addInteractions(element) {
        interact(element)
            .draggable({
                inertia: false,
                modifiers: [
                    interact.modifiers.restrictRect({
                        restriction: 'parent',
                        endOnly: true
                    })
                ],
                listeners: {
                    move(event) {
                        const target = event.target;
                        const x = (parseFloat(target.style.left) || 0) + event.dx;
                        const y = (parseFloat(target.style.top) || 0) + event.dy;
                        target.style.left = `${x}px`;
                        target.style.top = `${y}px`;
                        updateParlePosition(target.dataset.id, x, y);
                    }
                }
            })
            .resizable({
                edges: { 
                    left: '.resize-left', 
                    right: '.resize-right', 
                    bottom: '.resize-bottom', 
                    top: '.resize-top' 
                },
                modifiers: [
                    interact.modifiers.restrictSize({
                        min: { width: 100, height: 80 }
                    })
                ],
                listeners: {
                    move(event) {
                        const target = event.target;
                        target.style.width = `${event.rect.width}px`;
                        target.style.height = `${event.rect.height}px`;
                        updateParleSize(target.dataset.id, event.rect.width, event.rect.height);
                    }
                }
            });
    
        // Añadir handles de redimensionado táctiles
        const resizeHandles = `
            <div class="resize-handle resize-left"></div>
            <div class="resize-handle resize-right"></div>
            <div class="resize-handle resize-bottom"></div>
            <div class="resize-handle resize-top"></div>
        `;
        element.insertAdjacentHTML('beforeend', resizeHandles);
    }

    // Función updateParlePosition
    function updateParlePosition(id, x, y) {
        fetch(`/parles/${id}/actualizar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ x, y }), // Envía x, y como números
        });
    }

    // Función updateParleSize
    function updateParleSize(id, width, height) {
        fetch(`/parles/${id}/actualizar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ width, height }), // Envía width, height como números
        });
    }

    // Crear nuevo parle
    document.getElementById('add-parle').addEventListener('click', () => {
        fetch('/parles/crear/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(parle => createParleElement(parle));
    });

    // Eliminar parle
    parleMap.addEventListener('click', (e) => {
        if (e.target.classList.contains('view-boxes')) {
            const parleDiv = e.target.closest('.parle-box');
            const parleId = parleDiv.dataset.id;
            window.location.href = `/cajas/parle/${parleId}/`;
        }

        if (e.target.classList.contains('delete-parle')) {
            const parleDiv = e.target.closest('.parle-box');
            const parleId = parleDiv.dataset.id;
            fetch(`/parles/${parleId}/eliminar/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(() => parleDiv.remove());
        }
    });

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('delete-parle')) {
            const parleDiv = e.target.closest('.parle-box');
            const parleId = parleDiv.dataset.id;
            fetch(`/parles/${parleId}/eliminar/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(() => parleDiv.remove());
        }
    });
});

document.querySelectorAll('.parle-box').forEach(element => {
    interact(element)
        .draggable({
            inertia: false,
            modifiers: [
                interact.modifiers.restrictRect({
                    restriction: 'parent',
                    endOnly: true
                })
            ],
            listeners: {
                start(event) {
                    event.target.classList.add('dragging');
                },
                move(event) {
                    const target = event.target;
                    const x = (parseFloat(target.style.left) || 0) + event.dx;
                    const y = (parseFloat(target.style.top) || 0) + event.dy;
                    
                    target.style.left = `${x}px`;
                    target.style.top = `${y}px`;
                    
                    // Actualizar con debounce
                    updatePositionDebounced(target.dataset.id, x, y);
                },
                end(event) {
                    event.target.classList.remove('dragging');
                }
            }
        })
        .resizable({
            edges: { left: true, right: true, bottom: true, top: true },
            modifiers: [
                interact.modifiers.restrictSize({
                    min: { width: 100, height: 80 }
                })
            ],
            listeners: {
                start(event) {
                    event.target.classList.add('resizing');
                },
                move(event) {
                    const target = event.target;
                    target.style.width = `${event.rect.width}px`;
                    target.style.height = `${event.rect.height}px`;
                    
                    // Actualizar con debounce
                    updateSizeDebounced(target.dataset.id, event.rect.width, event.rect.height);
                },
                end(event) {
                    event.target.classList.remove('resizing');
                }
            }
        });
});

  function debounce(func, timeout = 1000) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const updatePositionDebounced = debounce((id, x, y) => {
    updateParlePosition(id, x, y);
});

const updateSizeDebounced = debounce((id, width, height) => {
    updateParleSize(id, width, height);
});

document.addEventListener('dblclick', (e) => {
    if (e.target.classList.contains('editable-nombre')) {
        const element = e.target;
        const originalText = element.textContent;
        const parleId = element.dataset.id;

        // Crear input editable
        const input = document.createElement('input');
        input.type = 'text';
        input.value = originalText;
        input.style.width = '100%';
        
        // Reemplazar h5 por el input
        element.replaceWith(input);
        input.focus();

        // Guardar al perder el focus o presionar Enter
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                guardarNombre();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // Evitar comportamiento por defecto
                guardarNombre();
            }
        });
        
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        // Modificar la función guardarNombre
        function guardarNombre() {
            const nuevoNombre = input.value.trim();
            
            if (nuevoNombre && nuevoNombre !== originalText) {
                fetch(`/parles/${parleId}/actualizar-nombre/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'), // Token desde la cookie
                    },
                    credentials: 'include', // ¡Añade esta línea!
                    body: JSON.stringify({ nombre: nuevoNombre }),
                })
                .then(response => {
                    if (!response.ok) throw new Error('Error en la respuesta');
                    return response.json();
                })
                .then(data => {
                    element.textContent = data.nombre; // Actualizar el texto
                    input.replaceWith(element); // Restaurar el elemento h5
                })
                .catch(error => {
                    console.error('Error:', error);
                    input.replaceWith(element); // Revertir cambios si hay error
                });
            } else {
                input.replaceWith(element);
            }
        }
        }
    }
)

