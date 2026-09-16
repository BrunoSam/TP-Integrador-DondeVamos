# Diagrama de clases

> Actualizado en TP1 con la implementación de la v1.

```mermaid
classDiagram

    class Lugar {
        -id: int
        -nombre: str
        -zona: str
        -categoria: str
        -puntuacion: float
        -horario_apertura: str
        -horario_cierre: str
        -costo: int
        +id() int
        +nombre() str
        +zona() str
        +categoria() str
        +puntuacion() float
        +horario_apertura() str
        +horario_cierre() str
        +costo() int
        +repr() str
    }

    class Catalogo {
        -lugares: list
        -salidas: list
        +cargar_desde_json(ruta) None
        +cargar_salidas_desde_json(ruta) None
        +buscar(nombre) Lugar
        +listar() list
        +listar_salidas() list
        +filtrar(categoria) list
    }

    class Salida {
        -id: int
        -nombre: str
        -participantes: list
        +id() int
        +nombre() str
        +participantes() list
        +repr() str
    }

    class Terminal {
        -catalogo: Catalogo
        +iniciar() None
    }

    Terminal --> Catalogo : usa
    Catalogo "1" o-- "*" Lugar : contiene
    Catalogo "1" o-- "*" Salida : contiene
```

La clase `Salida` se incorporó en la v1 en su versión mínima (id, nombre y lista de participantes), y se va a completar en etapas posteriores (fechas, presupuesto, lugares elegidos) cuando se implementen F4/F5.