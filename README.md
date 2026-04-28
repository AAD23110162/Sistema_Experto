# Sistema_Experto

Sistema experto en Python con interfaz por terminal. Incluye tres ejemplos independientes:

- Diagnóstico médico para infecciones de garganta.
- Diagnóstico automotriz para fallas de batería.
- Aprobación de créditos bancarios.

## Ejecutar

```bash
python3 main.py
```

También puedes abrir cada caso directamente:

```bash
python3 medical.py
python3 automotive.py
python3 credit.py
```

Si prefieres, `main.py` muestra un menú para elegir cualquiera de los tres casos.

## Qué hace

El programa recopila hechos por medio de preguntas en consola, evalúa reglas de negocio y muestra:

- La base de hechos actual.
- La conclusión obtenida.
- La traza de reglas que se activaron.

## Extender

Para agregar un nuevo ejemplo, crea otro conjunto de reglas dentro de `main.py` siguiendo el mismo patrón de los tres escenarios actuales.