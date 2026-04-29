# Sistema Experto
Autor: Alejandro Aguirre Díaz

Descripcion: Sistema experto es un repositorio con 3 ejemplos de sistemas expertos. El proyecto está organizado por carpetas, una por cada ejemplo, y cada caso sigue la misma arquitectura básica de un sistema experto.

## Estructura General

La solución usa un motor común en [engine.py](engine.py) y tres ejemplos independientes:

- [medical/](medical) para diagnóstico médico.
- [automotive/](automotive) para diagnóstico automotriz.
- [credit/](credit) para aprobación de créditos.

Cada carpeta contiene los mismos componentes conceptuales:

- [adquisicion_de_conocimiento.py](medical/adquisicion_de_conocimiento.py) o equivalente: captura datos del usuario.
- [base_de_conocimiento.py](medical/base_de_conocimiento.py) o equivalente: define reglas y conclusiones.
- [base_de_hechos.py](medical/base_de_hechos.py) o equivalente: prepara los datos calculados del caso.
- [motor_de_inferencia.py](medical/motor_de_inferencia.py) o equivalente: aplica el motor común.
- [interfase_y_usuario.py](medical/interfase_y_usuario.py) o equivalente: presenta resultados al usuario.
- [main.py](medical/main.py) como punto de entrada del ejemplo.

## Propiedades Comunes

Todos los ejemplos comparten estas propiedades:

- Interfaz por terminal.
- Entrada interactiva guiada por preguntas.
- Base de hechos temporal para cada caso.
- Base de conocimiento con reglas tipo SI/ENTONCES.
- Motor de inferencia que encadena conclusiones.
- Mensajes de salida con explicación del resultado.
- Dependencias solo de la biblioteca estándar de Python.

## Casos Disponibles

### 1. Diagnóstico Médico

Objetivo: apoyar la identificación de una infección de garganta y sugerir tratamiento.

Propiedades:

- Captura temperatura, dolor de garganta, placas blancas y tos.
- Calcula un hecho derivado llamado `high_fever`.
- Usa reglas para distinguir entre infección por estreptococo e infección viral.
- Produce una recomendación de tratamiento como `Penicilina` o `Tratamiento sintomático e hidratación`.

Características:

- Simula un caso clásico de diagnóstico clínico.
- Tiene trazabilidad de reglas activadas.
- Incluye una explicación breve de por qué se llegó a la conclusión.

### 2. Diagnóstico Automotriz

Objetivo: ayudar a detectar una falla eléctrica básica en el vehículo.

Propiedades:

- Muestra una lista numerada de modelos y el usuario elige uno por número.
- Captura voltaje de batería, clic del arranque y parpadeo del tablero.
- Calcula un hecho derivado llamado `battery_low`.
- Usa reglas para identificar batería con bajo voltaje, batería descargada y una recomendación final.

Características:

- Enfocado en diagnóstico rápido para taller.
- Simplifica la entrada del modelo para evitar escritura libre.
- Recomienda una acción concreta: cambiar la batería y revisar el sistema de carga.

### 3. Aprobación de Créditos Bancarios

Objetivo: evaluar si una solicitud de crédito puede aprobarse según reglas básicas de riesgo.

Propiedades:

- Captura nombre del solicitante, ingresos, deudas y atrasos previos.
- Calcula hechos derivados como `debt_ratio`, `income_ok`, `debt_ok` y `no_late_payments`.
- Usa reglas para aprobar o rechazar la solicitud.
- Muestra la decisión final con justificación.

Características:

- Simula un flujo de análisis financiero sencillo.
- Permite ver cómo la proporción de deuda afecta la decisión.
- Es útil para explicar políticas de riesgo de forma didáctica.

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

## Qué Hace el Sistema

El sistema recopila hechos por medio de preguntas en consola, evalúa reglas de negocio y muestra:

- La base de hechos actual.
- La conclusión obtenida.
- La traza de reglas que se activaron.

## Extender

Para agregar un nuevo ejemplo, crea una nueva carpeta con la misma estructura. Cada carpeta debería incluir:

- Un archivo de adquisición de conocimiento.
- Un archivo de base de conocimiento.
- Un archivo de base de hechos.
- Un archivo de motor de inferencia.
- Un archivo de interfase y usuario.
- Un `main.py` propio.

Si deseas integrarlo al menú principal, añade su constructor en [main.py](main.py).

## Notas de desarrollo

- Los entry points dentro de cada carpeta están preparados para ejecutarse como scripts desde la raíz del proyecto (añaden dinámicamente la raíz al `sys.path`).
- El proyecto usa solo la biblioteca estándar de Python; no requiere `requirements.txt` por ahora.
- Recomendación: crear un entorno virtual y usar `python -m venv .venv` y `source .venv/bin/activate` antes de ejecutar.

Si quieres, puedo:

- Añadir tests unitarios (pytest) por carpeta.
- Crear un `requirements.txt` y un pequeño `Makefile` o `scripts/run.sh`.