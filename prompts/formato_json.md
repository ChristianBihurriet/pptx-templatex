# Contrato común de contenido docente

Este documento define solo las reglas generales. **Los tipos, campos, máximos,
propósitos y ejemplos específicos proceden del catálogo generado del tema**.
Adjunta `tipos_<tema>.md`, obtenido mediante:

```text
pptgen --tema dam_oscuro --documentar-tipos --salida prompts
```

No inventes tipos ni campos y no deduzcas contratos de otro tema. El catálogo
proviene de las notas del PPTX, que es la única fuente de verdad. Si no se ha
adjuntado, solicítalo antes de redactar contenido dependiente de tipos.

Devuelve únicamente JSON válido UTF-8, sin bloques Markdown, comentarios ni
claves duplicadas. No uses NaN o Infinity. La raíz admite exclusivamente:

| Campo | Tipo | Obligatorio |
| --- | --- | --- |
| `titulo` | texto no vacío: título general de la clase | sí |
| `modulo` | texto: módulo | no |
| `curso` | texto: curso | no |
| `diapositivas` | lista no vacía de objetos en el orden de presentación | sí |

Cada diapositiva declara `tipo` y exclusivamente los campos de su ficha en el
catálogo. Todos sus valores son cadenas: nunca números, listas, objetos o `null`.
Los obligatorios no pueden estar vacíos ni contener solo espacios. Los opcionales
omitidos se sustituyen por texto vacío. El `titulo` general no es un valor por
defecto de un campo `titulo` de diapositiva.

Los máximos declarados son bloqueantes. Cuentan caracteres Unicode, incluyendo
espacios y saltos, y líneas separadas por `\n`. Un salto final cuenta otra línea.
Divide el contenido si excede un máximo. Las líneas visuales por ajuste de ancho
no se cuentan: evita líneas de código excesivamente largas.

El texto es literal: Markdown, HTML y etiquetas de formato no cambian estilos.
Los comentarios, multiplicaciones, asteriscos y llaves del código se conservan.
Usa `\n` para saltos y preferiblemente cuatro espacios para indentar; `\t` se
admite. No uses otros controles, incluidos `\r` y `\u000b`, ni caracteres XML
inválidos. No uses `{{ img:clave }}` ni el identificador `PPTGEN_METADATA`, reservados.
El código no se ejecuta. Un campo de lenguaje, si el tipo lo declara, es solo texto.

No incluyas coordenadas, tamaños, colores, rutas de salida, `src_page`,
`replace_texts` o notas en el contenido. La presentación visual pertenece al PPTX.
Las notas de autoría y el contrato interno no forman parte del JSON docente.

El catálogo incluye ejemplos completos validados. El archivo
`contenidos/programacion/herencia.json` es un ejemplo de clase para el tema incluido.
El nombre del archivo generado se elige por CLI, no mediante campos del contenido.
