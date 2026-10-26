# Viabilidad: contratos dentro de las notas del PowerPoint

Investigación y prueba aislada del 26 de octubre de 2026. **Documento histórico:
el enfoque descrito ya está integrado en `pptgen`.** La guía vigente está en
[CREAR_PLANTILLAS.md](CREAR_PLANTILLAS.md). El cargador extrae los contratos de
las notas, calcula las páginas y genera los catálogos con `--documentar-tipos`.
La generación sanea una copia temporal y reconstruye las notas docentes con
relaciones nuevas antes de publicar el resultado. Los apartados siguientes
conservan las conclusiones y propuestas de la investigación original.

## Conclusión

Es viable que cada diapositiva modelo almacene su identidad, contrato y
documentación en sus notas, y que el PPTX sea la única fuente de definición de
tipos. Recomiendo JSON delimitado, extraído al cargar el tema, y dos salidas
derivadas: catálogo JSON normalizado y catálogo Markdown para la IA.

Hay una condición necesaria antes de usarlo en producción: **sanear las notas
antes de que el motor copie las páginas**. La versión instalada del copiador
conserva el texto de las notas mediante una copia incompleta de su parte XML.
Los metadatos podrían llegar al alumno, y no se puede dar por garantizada la
integridad de esas notas copiadas.

## 1. API disponible y visibilidad

Verificado con `python-pptx 1.0.2` instalado y la
[documentación oficial de Slides y NotesSlide](https://python-pptx.readthedocs.io/en/latest/api/slides.html).

```python
from pptx import Presentation

prs = Presentation("plantilla.pptx")
slide = prs.slides[0]

# Lectura sin crear notas donde no las había:
if slide.has_notes_slide:
    frame = slide.notes_slide.notes_text_frame
    if frame is not None:
        texto = frame.text

# Escritura: acceder a notes_slide crea la página de notas si no existe.
frame = slide.notes_slide.notes_text_frame
if frame is None:
    raise ValueError("La página de notas no tiene el marcador de cuerpo.")
frame.text = "Notas docentes o metadatos delimitados"
prs.save("copia_con_notas.pptx")
```

`notes_text_frame` puede ser `None` si falta el marcador de cuerpo de notas.
El extractor debe tratar ese caso con un error claro y no escribir notas al
inspeccionar una plantilla. Guardar notas es una capacidad actual; su
interpretación como contrato es la propuesta nueva.

Las notas no aparecen sobre la diapositiva en la proyección normal. Sí se ven
en el panel de notas, la vista del moderador, impresiones con notas o el XML
interno del archivo. No son almacenamiento secreto ni cifrado. Ocultarlas de
la diapositiva no basta para excluirlas del PowerPoint distribuido.

### JSON frente a YAML

Ambos caben como texto. Recomiendo **JSON** porque ya usamos la biblioteca
estándar y el resto del sistema consume JSON. Evita añadir un parser y las
reglas adicionales de YAML. En producción se deben rechazar claves duplicadas,
NaN, Infinity y versiones desconocidas, igual que en el lector actual.

YAML resultaría algo más cómodo para descripciones extensas, pero requeriría
una dependencia, carga segura sin constructores de objetos y una política de
tipos explícita. No ofrece una ventaja suficiente para el piloto.

## 2. Qué hace realmente el copiador con las notas

Ruta actual: `TemplateEngine._copy_slide` delega en
`pptx_slide_copier.SlideCopier.copy_slide`. Se inspeccionó el código instalado
de `pptx-slide-copier 0.1.5`, en particular `_copy_part_rels` y
`_copy_rel_as_generic_part`.

El copiador no excluye `notesSlide`: copia su contenido como `Part` genérica,
pero no recorre las relaciones internas de esa parte. En la prueba:

| Archivo | Texto de metadatos | Relaciones desde cada página de notas |
| --- | --- | --- |
| Plantilla piloto guardada con la API | Presente | `notesMaster` y `slide` |
| Salida del motor sin saneamiento | Presente, en las dos copias | Ninguna |
| Salida saneada con notas docentes reconstruidas | Ausente | `notesMaster` y `slide` |

Se puede releer el texto de la salida sin sanear con `python-pptx`, pero eso no
demuestra fidelidad completa en PowerPoint. La prueba no abrió un visor gráfico
ni comprobó si PowerPoint repararía la copia incompleta. No conviene utilizar
esa salida como presentación final.

La conclusión está ligada a las versiones ensayadas: el proyecto permite
versiones posteriores mediante `>=`. Una futura integración necesita mantener
una prueba de regresión de copia y saneamiento para detectar cambios.

## 3. Identidad estable y metadatos propuestos

La identidad semántica sería el nombre actual `tipo`, por ejemplo `portada`.
Se guarda en las notas y se comparte entre temas. Al abrir el PPTX, se construye
el mapa `tipo → posición actual`; la posición solo es un dato derivado para
el motor, nunca la identidad del contrato.

La API expone `slide_id`, estable ante reordenaciones dentro de un archivo, pero
no es una identidad compartida entre temas ni debe usarse para enlazar contenido
docente. El nombre visible de una diapositiva y su título tampoco lo son.
Para esta arquitectura no hace falta un UUID adicional.

Reglas propuestas:

- Mantener `[a-z][a-z0-9_]*`, como en el contrato actual.
- Un único bloque de metadatos por página y un único registro por `tipo` en cada
  tema. Duplicar una página y dejar el mismo tipo debe provocar un error.
- Reordenar páginas conserva el tipo; el extractor recalcula `pagina`.
- Las páginas decorativas sin marcadores pueden ignorarse. En producción,
  una página con marcadores variables pero sin contrato debería provocar un
  error de autoría para detectar notas borradas accidentalmente.
- No renombrar un `tipo` publicado sin tratarlo como cambio incompatible.

### Bloque utilizado por el piloto

Se guarda en las notas de una **copia** de la portada existente. Puede coexistir
con notas del profesor fuera de los delimitadores. No utiliza cuadros invisibles
ni añade formas a la diapositiva.

```text
Recordatorio docente: presentar el problema antes de la teoría.

[[PPTGEN_METADATA_JSON_V1]]
{
  "metadatos_version": 1,
  "tipo": "portada",
  "contrato_version": 1,
  "proposito": "Presentar el tema y orientar al alumnado al comienzo de la clase.",
  "campos": {
    "titulo": {
      "tipo_dato": "string",
      "marcador": "titulo",
      "obligatorio": true,
      "max_caracteres": 100,
      "max_lineas": 2
    },
    "subtitulo": {
      "tipo_dato": "string",
      "marcador": "subtitulo",
      "max_caracteres": 180,
      "max_lineas": 3
    }
  },
  "ejemplo": {
    "tipo": "portada",
    "titulo": "Herencia en Java",
    "subtitulo": "Reutilización y especialización"
  },
  "restricciones": [
    "Texto literal; sin Markdown.",
    "Diseño fijo; no hay ajuste automático por contenido."
  ]
}
[[/PPTGEN_METADATA_JSON_V1]]
```

Este formato es experimental: no se puede pegar en el `tema.json` actual, cuyo
esquema cerrado lo rechazaría. En notas no tiene efecto sobre la CLI actual.

## 4. Extracción y contraste con los marcadores

El extractor futuro debe recorrer cada página y leer su bloque de notas,
validar el esquema completo y después recorrer los mismos cuadros y celdas que
el motor actual. No se deben buscar marcadores dentro del propio JSON de notas:
el conjunto a contrastar es el del contenido visual de la diapositiva.

Se mantienen las reglas actuales:

1. Marcadores completos dentro de un párrafo, aun si PowerPoint los divide en
   varios segmentos de formato.
2. Todo campo declarado tiene su marcador en la página, aunque sea opcional.
3. No hay marcadores desconocidos, mal formados ni compartidos por dos campos.
4. Los globales `titulo_clase`, `modulo` y `curso` no se declaran como campos.
5. Las tablas fijas se recorren por celdas; los grupos se rechazan. No se ofrecen
   marcadores en SmartArt, patrones o notas como contenido variable.
6. Las capacidades operativas siguen siendo las del adaptador: texto literal,
   sin imágenes por campo ni listas de filas. Un metadato no habilita capacidades.

El extractor del piloto comprueba marcadores, duplicados y versión 1, y produce
un catálogo sin leer `tema.json`. No es todavía un validador de esquema completo:
no incluye todas las comprobaciones de claves y tipos que requiere producción.
En el piloto se ignoran páginas no anotadas porque solo se prueba la portada;
esa tolerancia no debe convertirse en una migración silenciosa.

## 5. Arquitectura mínima con una sola fuente de verdad

```text
plantillas/<tema>/plantilla.pptx
    ├─ formas, cuadros y tablas → aspecto visual
    └─ notas delimitadas       → contrato y documentación
                  │
           extracción y validación
                  │
           catálogo en memoria
              ┌───┴───────────────────┐
              │                       │
      Theme normalizado       Markdown para la IA
              │               y JSON exportable
       adapt_content actual
              │
       src_page / replace_texts
              │
    copia temporal sin notas de plantilla
              │
       TemplateEngine actual
              │
    reconstruir solo notas docentes
              │
       verificar ausencia de metadatos
```

En la futura integración, `load_theme` mantendría su interfaz y devolvería el
mismo `Theme` que consume el adaptador. La normalización transforma `campos`
en sus reglas actuales, omitiendo anotaciones, y obtiene `pagina` de la posición
encontrada. No requiere cambiar `tipo` ni ningún campo del JSON docente.

No habría un catálogo contractual editable fuera del PPTX. `catalogo.json` y
el Markdown serían artefactos derivados, nunca fuentes alternativas. Para validar
y generar se extraería el catálogo del PPTX seleccionado en ese momento. Si se
usa caché, se comprueba SHA-256 del archivo fuente y versión del extractor;
una caché antigua no puede prevalecer sobre el PPTX.

Conservar `--tema dam_oscuro` es viable usando la convención
`plantillas/dam_oscuro/plantilla.pptx`. El nombre de carpeta selecciona el recurso;
no define tipos. El `tema.json` contractual desaparecería tras la migración,
no se mantendrían reglas paralelas contradictorias.

Durante una transición se podría conservar temporalmente el cargador antiguo
para temas sin metadatos, con diagnóstico explícito. Si un tema tiene metadatos
incompletos o inválidos, se debe fallar; no completar silenciosamente desde
`tema.json`. En el destino final, los tipos provienen exclusivamente del PPTX.

### Catálogo JSON y Markdown

El JSON derivado contendría versión del catálogo, huella de origen, tipos,
versiones de contrato, reglas y posiciones calculadas. Puede normalizarse al
modelo actual del validador; el archivo exportado sirve para inspección y otras
herramientas, sin obligar a leerlo como un segundo registro editable.

El Markdown deriva de ese mismo catálogo: propósito, campos `string`,
obligatoriedad, máximos y ejemplos. Los ejemplos se validan con `adapt_content`
antes de publicarlos. El contrato raíz y las restricciones de capacidades se
aportan desde el formato docente soportado, no se infieren de etiquetas libres.

`pptgen --documentar-tipos` seguiría siendo un comando futuro; el piloto lo
demuestra con una herramienta separada. No se ha añadido esa opción a la CLI.

## 6. Evitar que los metadatos lleguen a la salida

La estrategia probada es:

1. Extraer los contratos y las notas humanas de la plantilla fuente.
2. Crear una copia de trabajo, preservando el archivo del profesor.
3. Desconectar las páginas de notas de **todas** las diapositivas de esa copia,
   antes de que el motor la cargue como origen y destino. No basta con limpiar
   solo `template_prs`: `process` vuelve a abrir la ruta de plantilla.
4. Guardar la copia temporal y pasar su ruta a `TemplateEngine`.
5. Si se quieren conservar notas docentes, reconstruirlas después de generar,
   mediante la API pública, siguiendo el mapa de cada diapositiva generada a
   su página de origen. Esto crea sus relaciones correctas.
6. Guardar, reabrir y verificar todas las partes XML y relaciones del ZIP para
   comprobar que no queda el bloque. Ante fallo, no entregar el archivo final.

La API no expone una operación de alto nivel `delete_notes_slide`. El piloto
utiliza `slide.part.drop_rel` con `RT.NOTES_SLIDE`, una operación de empaquetado
de bajo nivel que debe encapsularse y probarse en la integración. Al guardar,
las partes de notas desconectadas y no alcanzables no se serializan.

No se recomienda quitar archivos ZIP a mano sin actualizar relaciones y tipos
de contenido. Tampoco basta con borrar un cuadro visible o establecer
`notes_text_frame.text = ""` en solo algunas notas.

El piloto conserva **texto plano** docente, no su formato, imágenes o composición
de la página de notas. Si se necesita preservar notas ricas, debe decidirse y
probarse por separado. La plantilla sigue conteniendo sus metadatos; se limpian
únicamente las copias para generación.

## 7. Opcionales, máximos y versiones

Se conservan las reglas actuales para no romper contenidos:

- `obligatorio` omitido equivale a `false`.
- Campo opcional omitido equivale a cadena vacía; no desaparece el cuadro.
- Todos los valores de campos son cadenas. Los obligatorios no pueden estar
  vacíos ni contener solo espacios. No se introducen valores por defecto nuevos.
- `max_caracteres` y `max_lineas` son máximos bloqueantes, enteros positivos;
  si faltan, no hay ese máximo. Se cuentan caracteres Unicode y líneas `\n`,
  no líneas visuales. No se introduce truncado, reducción de fuentes ni paginación.

Dos versiones tienen responsabilidades distintas:

| Versión propuesta | Significado |
| --- | --- |
| `metadatos_version` | Estructura del bloque, delimitación y reglas del extractor |
| `contrato_version` | Revisión semántica publicada de un tipo concreto |

El piloto admite exclusivamente `1` en ambos casos. En producción debe haber
una política explícita de versiones soportadas y rechazo claro de las futuras.
Cambiar colores, fuentes o posición de la página no cambia el contrato. Añadir
campos, cambiar obligatoriedad, significado o máximos exige revisar la versión
y calcular compatibilidad real, no confiar solo en el número.

El JSON docente actual no lleva versión y la propuesta inicial no se la añade:
se valida contra el contrato del tema seleccionado. Esto mantiene compatibilidad
de formato, pero no permite fijar desde un contenido antiguo una versión histórica
arbitraria. Para reproducibilidad se conservaría la versión del PPTX y su huella;
una selección de versiones desde el contenido sería otra decisión futura.

## 8. Compatibilidad entre temas visuales

Debe calcularse con los contratos extraídos, no comparando posiciones de página
o nombres de formas. El piloto no implementa aún este comparador.

Dos niveles útiles:

**Compatibilidad del documento concreto:** ejecutar el adaptador con el mismo
JSON y cada tema. Si ambos aceptan el contenido, puede generarse con los dos.
Esto no garantiza que todo otro contenido sea intercambiable ni que quepa igual.

**Compatibilidad de contratos A → B:** comprobar que B acepta cualquier documento
admitido por A, para el conjunto de tipos que se quiera comparar:

- B tiene todos esos tipos de A.
- B conoce todos los campos que admite A, aunque sean opcionales; el adaptador
  rechaza las claves desconocidas cuando sí aparecen en un documento.
- B no exige campos que A permita omitir.
- Los tipos de dato y el significado de los campos coinciden. El significado
  requiere revisión de autoría; no se demuestra mediante un hash.
- B no tiene máximos más estrictos para los mismos campos. Un máximo omitido
  equivale a infinito para esta comparación.
- Las capacidades y la semántica de vacío/valores por defecto son compatibles.

La dirección importa. Aceptar títulos de 100 caracteres en A y de 60 en B
no es compatible A → B, aunque un título concreto de 30 caracteres funcione.
Para intercambiabilidad total, comprobar ambas direcciones y el catálogo completo.

Se puede generar una firma canónica de campos y reglas normalizadas, excluyendo
página, nombre de marcador, diseño y descripciones. La igualdad da una comprobación
estructural rápida; cuando difieren, hace falta informar diferencias por tipo y
campo. Misma versión con reglas distintas debe señalarse como inconsistencia.
La compatibilidad visual sigue requiriendo revisar límites y resultado en PowerPoint.

## 9. Prueba de concepto ejecutada

Herramienta aislada: [tools/poc_notas_plantilla.py](../tools/poc_notas_plantilla.py).
Pruebas: [tests/test_poc_notas.py](../tests/test_poc_notas.py).

```powershell
.\.venv\Scripts\python.exe -m tools.poc_notas_plantilla
```

Produce una carpeta nueva `salida/poc_notas/` y rechaza sobrescribirla. Para repetir:

```powershell
.\.venv\Scripts\python.exe -m tools.poc_notas_plantilla --salida salida/poc_notas_otra_prueba
```

El arranque utiliza el contrato y la página de la portada existente para crear
una copia anotada: así no redefine manualmente sus reglas. **Después**, el
extractor lee solo esa copia del PPTX, genera el catálogo y adapta el contenido
con el modelo actual. Es una demostración del flujo, no la sustitución del
registro de temas de producción.

Artefactos:

| Archivo en `salida/poc_notas/` | Uso |
| --- | --- |
| `plantilla_con_metadatos.pptx` | Copia del tema actual; solo la portada tiene contrato en notas |
| `catalogo.json` | Contrato extraído, posición derivada y huella del PPTX |
| `catalogo_ia.md` | Ficha Markdown generada desde el mismo catálogo |
| `salida_sin_sanear_NO_DISTRIBUIR.pptx` | Evidencia experimental de fuga de metadatos e integridad incompleta de notas; no entregar |
| `plantilla_saneada_temporal.pptx` | Copia sin notas de plantilla utilizada para generar |
| `presentacion_limpia.pptx` | Dos portadas con distinto contenido y solo notas docentes reconstruidas |
| `informe.json` | Versiones instaladas y verificaciones observadas |

Resultados de la ejecución:

- Se escribieron y releyeron notas con JSON sin poner metadatos en las formas.
- La copia sin sanear conservó el texto del bloque, pero perdió las relaciones
  internas de sus notas. La copia limpia no contiene el delimitador ni la clave
  `contrato_version` en sus partes XML/relaciones.
- Se reutilizó el tipo dos veces, incluyendo una omisión válida de `subtitulo`.
- Las notas docentes limpias conservan el recordatorio y tienen relaciones
  `notesMaster` y `slide`. La plantilla original conserva su SHA-256.
- Las pruebas verifican identidad al mover la portada de página 1 a página 4,
  rechazo de tipos duplicados, bloques rotos y campos sin marcador correspondiente.
- La suite completa pasa: **153 pruebas**, incluidas las 143 anteriores.

Límites de la prueba: no modifica `pptgen`, `tema.json`, prompts ni la plantilla
original; no implementa la selección de temas por PPTX, un esquema exhaustivo,
un comparador de temas ni una migración. La editabilidad se comprueba a nivel de
objetos y reapertura; queda pendiente revisar manualmente el archivo en PowerPoint
y comprobar el flujo de editar sus notas allí y volver a extraerlas.

## Decisiones propuestas antes de migrar

Recomiendo validar este enfoque: JSON delimitado; `tipo` como identidad compartida;
una sola definición por tipo/tema; campos de texto y reglas actuales; catálogos
solo derivados; saneamiento obligatorio antes de copiar y reconstrucción posterior
de notas docentes en texto plano.

Con ese acuerdo, la siguiente tarea sería implementar el extractor de producción
con esquema completo, conectarlo a `load_theme`, añadir generación de catálogo y
comparación, y migrar los cuatro tipos existentes. El motor puede permanecer
intacto si la preparación y el saneamiento se realizan en el generador docente.
