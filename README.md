# Interpretación de bocetos

Dibuja un boceto y solicita una descripción en español de su contenido.

Adaptación académica de Juan José Hoyos (Jhuza), a partir del ejercicio compartido por Carlos Mario Correa. Interfaz basada en [Aurora](docs/guia-visual-aurora.md).

[Abrir app](https://drawrecog-appxrd8ntagtefe8amd93ih.streamlit.app/) · [Portafolio](https://jhginterfacesmultimodalesportfolio.streamlit.app/)

## Ejecutar

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Uso y alcance

Ajusta el grosor, dibuja un boceto, introduce tu clave de OpenAI y pulsa Interpretar boceto.

Necesita una clave de OpenAI. Un boceto ambiguo puede producir una interpretación incorrecta; contrástala con tu intención.

Consulta la [ficha de la experiencia](docs/EXPERIENCIA.md). Las credenciales se introducen en la sesión; no deben guardarse en el código.

## Verificación

Las pruebas de `tests/` comprueban controles, entradas vacías y resultados con servicios o modelos simulados. No certifican una respuesta de un servicio externo. Ejecutar con `python -m pytest tests -q` después de instalar pytest y las dependencias de la app.
