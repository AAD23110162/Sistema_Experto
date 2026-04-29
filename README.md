# Sistema_Experto

Sistema experto en Python con interfaz por terminal. El proyecto está organizado por carpetas, una por cada ejemplo:

- [medical/](medical) para diagnóstico médico.
- [automotive/](automotive) para diagnóstico automotriz.
- [credit/](credit) para aprobación de créditos.

Cada carpeta incluye un script por cada parte del sistema:

- [adquisicion_de_conocimiento.py](medical/adquisicion_de_conocimiento.py) o equivalente.
- [base_de_conocimiento.py](medical/base_de_conocimiento.py) o equivalente.
- [interfase_y_usuario.py](medical/interfase_y_usuario.py) o equivalente.
- [base_de_hechos.py](medical/base_de_hechos.py) o equivalente.
- [motor_de_inferencia.py](medical/motor_de_inferencia.py) o equivalente.
- [main.py](medical/main.py) como punto de entrada del ejemplo.

## Estructura General

- [engine.py](engine.py) contiene el motor común y las utilidades compartidas.
- [main.py](main.py) muestra un menú para elegir cualquiera de los tres casos.

## Casos Disponibles

- Diagnóstico médico para infecciones de garganta.
- Diagnóstico automotriz para fallas de batería.
- Aprobación de créditos bancarios.

## Ejecutar

Menú general:

```bash
python3 main.py
```

Ejecutar un caso directamente desde su carpeta:

```bash
python3 medical/main.py
python3 automotive/main.py
python3 credit/main.py
```

Ejemplos rápidos (puedes usar `printf` para simular respuestas):

```bash
# Caso médico: temperatura 40°C, dolor de garganta sí, placas sí, tos no
printf '40\ns\ns\nn\n' | python3 medical/main.py

# Automotriz: Ford Fiesta, 11.5V, arranque hace clic, tablero parpadea
printf 'Ford Fiesta\n11.5\ns\ns\n' | python3 automotive/main.py

# Crédito: Juan Pérez, ingresos 25000, deudas 5000, sin atrasos
printf 'Juan Pérez\n25000\n5000\nn\n' | python3 credit/main.py
```

## Qué Hace

El sistema recopila hechos por medio de preguntas en consola, evalúa reglas de negocio y muestra:

- La base de hechos actual.
- La conclusión obtenida.
- La traza de reglas que se activaron.

## Extender

Para agregar un nuevo ejemplo, crea una nueva carpeta con la misma estructura: adquisición, base de hechos, base de conocimiento, motor de inferencia, interfaz y usuario, y main. Si deseas integrarlo al menú principal, añade su constructor en [main.py](main.py).

## Notas de desarrollo

- Los entry points dentro de cada carpeta están preparados para ejecutarse como scripts desde la raíz del proyecto (añaden dinámicamente la raíz al `sys.path`).
- El proyecto usa solo la biblioteca estándar de Python; no requiere `requirements.txt` por ahora.
- Recomendación: crear un entorno virtual y usar `python -m venv .venv` y `source .venv/bin/activate` antes de ejecutar.

Si quieres, puedo:

- Añadir tests unitarios (pytest) por carpeta.
- Crear un `requirements.txt` y un pequeño `Makefile` o `scripts/run.sh`.