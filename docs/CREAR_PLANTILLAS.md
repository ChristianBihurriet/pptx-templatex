# Crear tipos exclusivamente desde PowerPoint

Guía vigente tras la integración de plantillas autodescriptivas. La definición
de un tipo vive en las **notas del presentador de su diapositiva modelo**.
El PPTX contiene diseño, campos, límites, ejemplo y propósito didáctico.
No hay que modificar Python ni registrar campos en `tema.json`.

## Qué archivo abrir

El tema `dam_oscuro` usa **`plantillas/dam_oscuro/docente_biblioteca.pptx`**. El `tema.json`
de esa carpeta solo apunta al archivo activo:

```json
{"version": 1, "plantilla": "docente_biblioteca.pptx"}
```

Las antiguas `plantilla.pptx` y `docente.pptx` no están activas: se conservan las
versiones previas, sin sobrescribirlas. Para crear otro tema, copia
el archivo activo a `plantillas/mi_tema/plantilla.pptx`; en esa convención no
necesitas `tema.json`. Si utilizas otro nombre, añade solo ese puntero de archivo.
Los temas se buscan primero en el directorio de trabajo y después en el paquete.

## 1. Diseñar una diapositiva modelo

Abre el PPTX activo en PowerPoint. Puedes duplicar una página existente y
cambiar su distribución. Usa cuadros de texto, formas con texto sin agrupar,
tablas nativas de tamaño fijo, imágenes estáticas y conectores prediseñados.
Mantén todos los campos variables directamente en la diapositiva.

Para un diseño de comparación, coloca cinco cuadros:

```text
                       {{ titulo }}

{{ izquierda_titulo }}             {{ derecha_titulo }}
{{ izquierda_contenido }}          {{ derecha_contenido }}
```

La distribución `comparacion` ya viene incluida en la biblioteca de 20 tipos:
consulta [BIBLIOTECA_DOCENTE.md](BIBLIOTECA_DOCENTE.md). El ejemplo siguiente
ilustra el procedimiento de autoría; para añadir otra distribución, utiliza un
nombre nuevo (por ejemplo, `comparacion_personal`) tanto en el contrato como en
su ejemplo. No añadas una segunda página con el mismo `tipo`.

El texto fijo, colores, tamaños, fondos y fuentes se diseñan en PowerPoint.
Usa un formato uniforme por párrafo variable: el motor reconstruye cada párrafo
modificado con un solo formato de referencia y no conserva estilos por palabra.
Elige «No autoajustar» para que PowerPoint no reduzca las fuentes del diseño.

### Marcadores y nombres

- `{{ titulo }}` y `{{titulo}}` son válidos. Mantén cada marcador en un solo
  párrafo; puede estar partido en segmentos de formato, pero no en párrafos.
- Nombres de temas, tipos, campos y marcadores: `[a-z][a-z0-9_]*`, sin tildes,
  mayúsculas ni guiones medios. Los valores y títulos visibles sí admiten tildes.
- El nombre del cuadro en el panel de selección no registra el campo; importa
  únicamente el marcador escrito y su correspondencia en las notas.
- Cada campo, incluso opcional, debe tener su marcador en la página. Puede
  repetirse el marcador; dos campos no pueden compartirlo.
- `tipo` es un nombre de campo reservado. Los marcadores globales
  `{{ titulo_clase }}`, `{{ modulo }}` y `{{ curso }}` proceden de la raíz del JSON
  y no se declaran en `campos`. El título de la clase no rellena automáticamente
  el título propio de cada diapositiva.
- No se admiten marcadores con rutas/índices, como `{{ user.name }}`, ni de
  imágenes `{{ img:foto }}` o filas variables `{{ rows.campo }}` en el contrato docente.

## 2. Abrir y editar las notas

En la vista normal de PowerPoint, abre el panel **Notas** que aparece debajo de
la diapositiva. Pega el siguiente bloque completo como texto; los delimitadores
también se incluyen. No lo pegues en un cuadro de la diapositiva ni en el patrón.
Las notas no se ven en la proyección normal, pero sí en la vista del moderador.

Al duplicar una diapositiva, cambia su `tipo`: el programa rechaza duplicados.
El orden de páginas puede cambiar libremente: la posición se calcula al cargar.
No escribas una clave `pagina`, ni uses el título visible como identificador.

Este bloque está en el formato implementado y documenta el ejemplo de comparación:

```text
Recordatorio docente: explicar primero las dos alternativas con ejemplos.

[[PPTGEN_METADATA_JSON_V1]]
{
  "metadatos_version": 1,
  "contrato_version": 1,
  "tipo": "comparacion",
  "proposito": "Contrastar dos alternativas utilizando el mismo criterio.",
  "campos": {
    "titulo": {
      "tipo_dato": "string",
      "marcador": "titulo",
      "obligatorio": true,
      "max_caracteres": 80,
      "max_lineas": 2,
      "descripcion": "Criterio o pregunta que organiza la comparación."
    },
    "izquierda_titulo": {
      "tipo_dato": "string",
      "marcador": "izquierda_titulo",
      "obligatorio": true,
      "max_caracteres": 42,
      "max_lineas": 2
    },
    "izquierda_contenido": {
      "tipo_dato": "string",
      "marcador": "izquierda_contenido",
      "obligatorio": true,
      "max_caracteres": 210,
      "max_lineas": 6
    },
    "derecha_titulo": {
      "tipo_dato": "string",
      "marcador": "derecha_titulo",
      "obligatorio": true,
      "max_caracteres": 42,
      "max_lineas": 2
    },
    "derecha_contenido": {
      "tipo_dato": "string",
      "marcador": "derecha_contenido",
      "obligatorio": true,
      "max_caracteres": 210,
      "max_lineas": 6
    }
  },
  "ejemplo": {
    "tipo": "comparacion",
    "titulo": "Herencia y composición",
    "izquierda_titulo": "Es un",
    "izquierda_contenido": "Un perro es un animal.",
    "derecha_titulo": "Tiene un",
    "derecha_contenido": "Un coche tiene un motor."
  },
  "restricciones": ["Dos columnas fijas; no redistribuye el espacio automáticamente."]
}
[[/PPTGEN_METADATA_JSON_V1]]
```

El texto antes o después del bloque es una nota docente y se puede conservar en
la salida como texto plano. No uses los delimitadores ni `PPTGEN_METADATA` fuera
del bloque. El contrato es JSON estricto: comillas dobles rectas, sin comentarios,
sin comas finales, sin claves duplicadas, NaN o Infinity. Dentro de valores usa
`\n` para saltos. Para separar líneas del JSON en el panel utiliza Enter.

### Esquema aceptado, sin claves adicionales

| Nivel | Claves obligatorias | Claves opcionales |
| --- | --- | --- |
| Contrato | `metadatos_version`, `contrato_version`, `tipo`, `proposito`, `campos`, `ejemplo` | `restricciones` |
| Cada campo | `tipo_dato`, `marcador` | `obligatorio`, `max_caracteres`, `max_lineas`, `descripcion` |

`metadatos_version` solo admite el entero `1`. `contrato_version` es un entero
positivo de revisión del tipo; increméntalo al cambiar sus reglas o significado.
Cambiar solo el aspecto o reordenar páginas no exige otra versión contractual.
No se seleccionan versiones históricas desde el JSON docente actual.

`proposito` y las descripciones proporcionadas deben ser texto no vacío.
`restricciones` es una lista de textos no vacíos y describe condiciones, pero
no habilita funciones nuevas. `campos` debe ser un objeto no vacío.
`ejemplo` es una diapositiva completa del mismo tipo, con datos que pasan el
adaptador y sus límites; se valida al cargar el tema, no solo al documentarlo.

`tipo_dato` solo admite `string`. Si falta `obligatorio`, se considera `false`.
Un campo opcional omitido se vuelve texto vacío; el cuadro permanece en su sitio.
No se admite `null`, ni valores por defecto configurables. Los obligatorios deben
estar presentes y contener algo distinto de espacios.

Los máximos opcionales son enteros positivos y **bloquean** contenido excesivo;
no son consejos. Si se omiten, no hay máximo de esa clase. Se cuentan caracteres
Unicode y líneas separadas por `\n`, no anchuras ni líneas visuales. No hay
truncado, reducción de fuente o paginación automática. Prueba datos cerca de los
máximos y líneas largas antes de elegirlos.

## 3. Guardar, validar y regenerar el catálogo

Guarda el PPTX en PowerPoint. Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\pptgen.exe --tema dam_oscuro --listar-tipos
.\.venv\Scripts\pptgen.exe --tema dam_oscuro --documentar-tipos --salida prompts
```

El primer comando valida los contratos contra los marcadores. Una página con
marcadores y sin contrato da error, aunque otras páginas sean válidas. Las páginas
estáticas sin marcadores ni contrato se ignoran. No se completan reglas desde
`tema.json`. Los grupos de formas se rechazan: desagrúpalos antes de guardar.

El segundo genera/regenera `prompts/tipos_dam_oscuro.md` y
`prompts/tipos_dam_oscuro.json`, con huella SHA-256 del PPTX. Son derivados:
**no los edites para cambiar reglas**. Validar y generar vuelve a leer el PPTX;
no usa una copia vieja del catálogo. El Markdown documenta el contrato común,
propósitos, campos, descripciones, límites, restricciones y ejemplos completos.

Entrega a cualquier chatbot ese Markdown junto a `prompts/formato_json.md`,
`prompts/profesor.md` y el contexto del módulo. No necesita saber Python ni
números de página. Regenera después de cada cambio de notas o diseño.

## 4. Crear el contenido de prueba y generar

Copia un ejemplo completo del catálogo generado a un JSON docente. El tipo
`comparacion` ya está disponible en el tema actual. Por ejemplo:

```json
{
  "titulo": "Relaciones entre clases",
  "modulo": "Programación",
  "curso": "1DAM",
  "diapositivas": [
    {
      "tipo": "comparacion",
      "titulo": "Herencia y composición",
      "izquierda_titulo": "Es un",
      "izquierda_contenido": "Un perro es un animal.",
      "derecha_titulo": "Tiene un",
      "derecha_contenido": "Un coche tiene un motor."
    }
  ]
}
```

Guárdalo como `contenidos/programacion/comparacion.json` y ejecuta:

```powershell
.\.venv\Scripts\pptgen.exe contenidos/programacion/comparacion.json --validar
.\.venv\Scripts\pptgen.exe contenidos/programacion/comparacion.json --nombre "Comparación de prueba"
```

Estos comandos funcionan con `comparacion` sin añadir otra página. Si has creado
un tipo nuevo, usa su nombre y sus campos en el JSON después de guardar el PPTX.
Repite el tipo con dos datos distintos para comprobar su reutilización. Si el
archivo de salida existe, elige otro nombre. Para ver todos los tipos juntos,
genera `contenidos/demostracion/biblioteca_dam.json`.

## 5. Comprobar la edición y las notas finales

Abre el resultado en PowerPoint. Edita el título, una celda si existe y una forma;
confirma que no es una sola imagen. Revisa fuentes, espacios, cortes y tamaño
del código. Guarda y reabre la copia. El equipo de destino debe tener las fuentes;
no se instalan ni incrustan automáticamente.

Revisa el panel de notas: no debe contener JSON, delimitadores ni documentación
interna. Solo el texto docente fuera del bloque se reconstruye. Antes de publicar
el archivo, el programa verifica las partes XML y relaciones de las notas;
si detecta metadatos internos o enlaces inválidos, no entrega el PPTX.

El tema original nunca se sanea ni se usa como archivo de salida. La copia
temporal se limpia antes de llamar al copiador, evitando su defecto con las notas.
Se conserva texto docente plano; las notas con formas o imágenes personalizadas
se rechazan y el formato rico del texto no se conserva.

## Límites y compatibilidad

No se sustituyen marcadores en grupos, SmartArt, notas, patrones ni gráficos.
Los diagramas de estructura fija pueden usar cajas y conectores desagrupados;
no se generan diagramas variables. Las imágenes variables y tablas de filas
variables existen en el motor original, pero aún no en el contrato docente.

Los tipos se identifican por nombre, no por título ni número de página. Para usar
el mismo contenido con dos temas, ambos deben reconocer sus tipos y campos y
aceptar sus máximos. Puedes validar el mismo archivo con cada `--tema`; eso no
demuestra intercambiabilidad de todos los documentos. No hay aún un comando
automático de comparación de contratos entre temas.

## Migrar otros temas antiguos, una sola vez

Los contratos antiguos en `tema.json` se rechazan de forma explícita. Para un
tema legado con un ejemplo de contenido para cada tipo:

```powershell
.\.venv\Scripts\python.exe -m tools.migrar_contratos_a_notas plantillas/mi_tema contenidos/mi_ejemplo.json salida/mi_tema_migrado.pptx
```

La utilidad crea un archivo nuevo sin sobrescribir la plantilla, añade contratos
y comprueba que las reglas normalizadas coinciden exactamente con las antiguas.
Copia el resultado a la carpeta del tema y elimina `tipos` de `tema.json`:
déjalo solo con `version` y `plantilla`, o elimina el JSON si el archivo se llama
`plantilla.pptx`. Revisa y mejora los textos de documentación en PowerPoint.

`tools/crear_tema_demo.py` es una utilidad de reconstrucción de los cuatro diseños
de demostración: lee sus contratos del PPTX activo, pero sobrescribe el diseño
de destino. No la uses después de añadir diseños personalizados. No es necesaria
para añadir ni registrar una página desde PowerPoint.
