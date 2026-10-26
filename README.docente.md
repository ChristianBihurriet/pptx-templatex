# Presentaciones docentes locales para DAM

`pptgen` convierte JSON docente en PowerPoints editables. **El PPTX del tema es
la única fuente de sus tipos, contratos y documentación**, mediante JSON en las
notas de cada diapositiva modelo. No hay un registro de campos fuera del PPTX.

Reutiliza `TemplateEngine`, `python-pptx` y `pptx-slide-copier`, conservando los
créditos de SpringMT y la licencia MIT. La CLI `pptx-templatex` sigue disponible.
No hay APIs, IA, bases de datos ni servicios: tras instalar las dependencias,
validar, documentar y generar funciona sin conexión.

## Instalar y utilizar

Python 3.10 o posterior, desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\pptgen.exe --listar-temas
.\.venv\Scripts\pptgen.exe --listar-tipos
.\.venv\Scripts\pptgen.exe contenidos/programacion/herencia.json --validar
.\.venv\Scripts\pptgen.exe contenidos/programacion/herencia.json --tema dam_oscuro --nombre "Herencia en Java"
```

Resultado: `salida/Herencia en Java.pptx`. Si existe, elige otro nombre o directorio;
no se sobrescribe. Para uso ordinario basta `pip install -e .`; `[dev]` añade pruebas
y lint. También puedes usar `python -m pptgen.cli`. En Linux/macOS activa
`.venv/bin/activate` y utiliza `pptgen`.

| Argumento | Uso |
| --- | --- |
| `contenido.json` | Obligatorio para generar o validar |
| `--tema` | `dam_oscuro` por defecto |
| `--nombre` | Nombre sin extensión; por defecto el nombre del archivo JSON |
| `--salida` | Directorio relativo al actual; `salida/` por defecto |
| `--validar` | Valida tema, notas, marcadores y contenido sin generar archivos |
| `--listar-temas` | Descubre temas locales e incluidos con el paquete |
| `--listar-tipos` | Valida el tema y lista sus campos; `*` significa obligatorio |
| `--documentar-tipos` | Genera `tipos_<tema>.md` y `tipos_<tema>.json` en `--salida` |

Los modos validar/listar/documentar son excluyentes. Documentar no requiere contenido
y regenera sus archivos derivados. Éxito devuelve 0; errores de datos/tema/archivo,
1; argumentos incorrectos, 2. Los nombres de salida no pueden contener rutas.

## Preparar contenido con cualquier chatbot

Regenera el catálogo del tema y adjúntalo junto a los prompts generales:

```powershell
.\.venv\Scripts\pptgen.exe --tema dam_oscuro --documentar-tipos --salida prompts
```

Entrega a la IA `prompts/profesor.md`, `prompts/formato_json.md`,
`prompts/tipos_dam_oscuro.md` y el contexto del módulo en `contexto/1dam/`.
El Markdown generado contiene campos, obligatoriedad, máximos, propósito,
restricciones y ejemplos validados. No edites manualmente los catálogos: cambia
las notas del PPTX y regenera. El JSON exportado tampoco se carga como registro.

El formato docente mantiene `titulo`, `modulo`, `curso` y `diapositivas`, con
`tipo` y campos de texto por diapositiva. Los contenidos existentes siguen siendo
válidos: los cuatro tipos originales conservan sus campos y máximos anteriores.

## Biblioteca de 20 composiciones

El tema incorpora explicaciones, comparación, código explicado y con resultado,
transformaciones, errores, procedimientos, tabla editable, flujo, relaciones de
clases, casos prácticos, advertencias, resumen, terminal y concepto visual.
Consulta [docs/BIBLIOTECA_DOCENTE.md](docs/BIBLIOTECA_DOCENTE.md) para elegir un
diseño, abrir las demostraciones y conocer qué revisión visual queda pendiente.

```powershell
.\.venv\Scripts\pptgen.exe contenidos/demostracion/biblioteca_dam.json --nombre "Biblioteca docente DAM - 20 tipos"
.\.venv\Scripts\pptgen.exe contenidos/demostracion/biblioteca_limites.json --nombre "Biblioteca docente DAM - limites"
```

El segundo archivo es una prueba sintética de límites, no una clase para impartir.
Si los resultados ya existen, utiliza otra carpeta con `--salida`.

## Editar o añadir un diseño

Sigue [docs/CREAR_PLANTILLAS.md](docs/CREAR_PLANTILLAS.md): incluye el procedimiento
exclusivamente desde PowerPoint y un bloque completo de ejemplo para sus notas.

El tema incluido usa `plantillas/dam_oscuro/docente_biblioteca.pptx`. Su `tema.json`
contiene solo el nombre del archivo; no contiene tipos ni contratos. Se conservan
`docente.pptx` (la versión anterior de cuatro diseños) y `plantilla.pptx` (anterior
a la migración). **Ninguno es el archivo activo del generador.** Edita
`docente_biblioteca.pptx`; las cuatro páginas originales se conservaron intactas.

Un tema nuevo puede contener solo `plantillas/mi_tema/plantilla.pptx`, sin JSON
externo. Si prefieres otro nombre de archivo, añade un `tema.json` mínimo con
`version: 1` y `plantilla`. Las carpetas locales prevalecen sobre las instaladas.

La generación usa una copia temporal sin notas de plantilla, copia las diapositivas
y reconstruye solo el texto docente exterior al bloque JSON. Verifica que no
queden delimitadores internos ni relaciones inválidas antes de publicar el PPTX.
No modifica el tema original ni distribuye sus contratos en las notas finales.

## Estructura

```text
pptgen/                     Extracción, validación, CLI, catálogo y generación
pptx_templatex/             Motor y CLI originales
plantillas/dam_oscuro/
  docente_biblioteca.pptx   20 diseños y contratos en notas: fuente de verdad
  tema.json                 Solo apunta a docente_biblioteca.pptx
prompts/                    Metodología, formato común y catálogos generados
contexto/1dam/              Conocimientos previos editables por módulo
contenidos/                 JSON docentes, incluido programacion/herencia.json
docs/CREAR_PLANTILLAS.md    Guía vigente de autoría en PowerPoint
salida/                     Archivos generados, excluidos de Git
tests/                     Pruebas originales y de integración
tools/                     Experimento histórico y utilidades de migración/diseño
```

Los contratos antiguos en `tema.json` se rechazan con un mensaje de migración;
no se mezclan con las notas. Para migrar otro tema hay una utilidad explícita
documentada en la guía. No hay migración silenciosa al ejecutar un comando normal.

## Pruebas y límites

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check pptgen tests
```

Los límites cuentan caracteres y saltos `\n`; no miden el ajuste visual. No hay
truncado, reducción de fuentes ni paginación automáticos. Desactiva el autoajuste
en PowerPoint y revisa el resultado antes de clase. Instala las fuentes necesarias
en el equipo que lo mostrará; no se incrustan automáticamente.

Se admiten cuadros de texto, formas sin agrupar y tablas fijas. Las imágenes y
conectores prediseñados pueden ser estáticos. No se generan listas de filas,
imágenes variables ni diagramas automáticos desde el contrato docente actual.
No se sustituyen marcadores en SmartArt, patrones, gráficos ni notas. Los párrafos
modificados usan un único formato de referencia; no se conservan estilos distintos
por palabra. El código es texto literal, sin resaltado ni ejecución.

Las notas docentes se conservan como texto plano; no se conserva su formato rico.
Las notas con formas o imágenes personalizadas se rechazan en lugar de descartarlas
silenciosamente. El bloque interno de metadatos no aparece en el archivo final.

La investigación original está en
[docs/PLANTILLAS_AUTODESCRIPTIVAS.md](docs/PLANTILLAS_AUTODESCRIPTIVAS.md), marcada
como antecedente histórico. La guía de autoría describe el sistema vigente.
