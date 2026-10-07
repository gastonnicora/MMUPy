# MMUPy 1.0.1

## Descripción

MMUPy es una aplicación gráfica para simular algoritmos de reemplazo de páginas en memoria.

La aplicación permite seleccionar la cantidad de marcos físicos, ingresar una secuencia de referencias y ejecutar los algoritmos FIFO, FIFO2, LRU y ÓPTIMO.

## Estructura

- `core/`: lógica de la simulación, memoria, páginas, cola, algoritmos y registro histórico.
- `gui/`: interfaz gráfica desarrollada con PySide6.
- `main.py`: punto de entrada de la aplicación.

## Algoritmos

### FIFO

Reemplaza la página que lleva más tiempo dentro de la cola.

### FIFO2

Implementa la estrategia de segunda oportunidad utilizando el bit de referencia.

### LRU

Reemplaza la página que lleva más tiempo sin ser utilizada.

### ÓPTIMO

Selecciona la página cuyo próximo uso se encuentra más alejado en la secuencia de referencias.

## Referencias modificadas

Una referencia terminada en `M` representa una escritura. Por ejemplo:

```text
1 2 3M 4 1 2M
```

Cuando existen referencias modificadas, el simulador contempla un marco reservado para representar la operación correspondiente.

## Instalación

Instalar las dependencias con:

```text
pip install -r requirements.txt
```

## Ejecución

Ejecutar:

```text
python main.py
```

## Refactorización

La refactorización mantiene la representación visual original de la cola, la tabla de simulación y el historial.

Los cambios se concentran en la organización interna del código, la documentación, el manejo de tipos, la eliminación de argumentos mutables por defecto y la simplificación de operaciones repetidas.

No se modificó la estructura visual de los widgets.
