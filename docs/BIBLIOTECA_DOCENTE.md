# Biblioteca docente DAM: 20 composiciones

## Archivos y fuente de verdad

- **Plantilla activa:** `plantillas/dam_oscuro/docente_biblioteca.pptx`.
- `tema.json` solo selecciona ese archivo; no registra contratos.
- Versiones anteriores conservadas: `docente.pptx` (cuatro tipos autodescriptivos)
  y `plantilla.pptx` (antes de la migración). No se sobrescribieron.
- Catálogos derivados: `prompts/tipos_dam_oscuro.md` y `.json`.
- Demostración: `salida/Biblioteca docente DAM - 20 tipos.pptx`.
- Prueba sintética: `salida/Biblioteca docente DAM - limites.pptx`.

Los resultados de `salida/` están excluidos de Git; pueden regenerarse desde los
JSON versionables de `contenidos/demostracion/`. Los contratos solo se editan en
las notas de la plantilla activa, nunca en los catálogos ni en esos contenidos.
No se han cambiado el motor ni los módulos Python de `pptgen` para añadir diseños.

## Elegir una composición

| Tipo | Uso y distribución |
| --- | --- |
| `portada` | Presentar el tema con título y subtítulo; original conservado. |
| `pregunta` | Activar una necesidad de aprendizaje con una pregunta y contexto; original conservado. |
| `definicion` | Precisar un concepto ya motivado, con explicación amplia; original conservado. |
| `codigo` | Fragmento de código a ancho completo; original conservado. |
| `explicacion` | Explicación principal amplia y ejemplo breve en una tarjeta lateral monoespaciada. |
| `problema` | Situación arriba; dificultad y pregunta guía en dos paneles inferiores diferenciados. |
| `codigo_explicado` | Código en el panel izquierdo, más ancho; razonamiento y decisiones a la derecha. |
| `codigo_resultado` | Código corto arriba y salida esperada en una banda independiente debajo. |
| `comparacion` | Dos columnas equilibradas, cada una con título y características comparables. |
| `antes_despues` | Dos estados monoespaciados, una flecha de transformación y una síntesis inferior. |
| `error_correccion` | Fragmento incorrecto en rojo, corrección en verde y explicación de la causa debajo. |
| `pasos` | Línea de procedimiento vertical con cinco filas numeradas; tres obligatorias y dos opcionales. |
| `tabla` | Tabla nativa de tres columnas y cuatro filas de datos, además de su cabecera; nota inferior opcional. |
| `diagrama_flujo` | Cuatro cajas horizontales conectadas por tres flechas, con contexto y conclusión opcionales. |
| `relaciones_clases` | Una clase base arriba y dos especializaciones debajo, conectadas hacia la base. |
| `caso_practico` | Contexto en columna lateral; requisitos y objetivo verificable en el espacio principal. |
| `advertencia` | Señal de aviso nativa y tres bloques: error habitual, motivo y recomendación. |
| `resumen` | Tres ideas conectadas a la izquierda y un principio destacado a la derecha. |
| `terminal` | Consola a ancho completo; comandos y salida claramente separados, con aclaración opcional. |
| `concepto_visual` | Concepto central destacado, explicación breve y tres tarjetas de apoyo visual. |

Las composiciones no dependen del tema de la clase: sus ejemplos abarcan Java,
POO, concurrencia, JDBC, Git, SQL, normalización y lenguajes de marcas, pero los
campos admiten otros contenidos. La jerarquía de `relaciones_clases` sí tiene un
significado fijo: herencia; no debe reutilizarse para representar composición.

Los campos, límites exactos, obligatoriedad, propósitos, restricciones y ejemplos
válidos están en el **catálogo generado**, no en una segunda tabla contractual
mantenida a mano en este documento.

## Generar las muestras y documentar los tipos

Desde la raíz del proyecto, con el entorno instalado:

```powershell
.\.venv\Scripts\pptgen.exe --listar-tipos
.\.venv\Scripts\pptgen.exe --documentar-tipos --salida prompts
.\.venv\Scripts\pptgen.exe contenidos/demostracion/biblioteca_dam.json --validar
.\.venv\Scripts\pptgen.exe contenidos/demostracion/biblioteca_dam.json --nombre "Biblioteca docente DAM - 20 tipos"
.\.venv\Scripts\pptgen.exe contenidos/demostracion/biblioteca_limites.json --nombre "Biblioteca docente DAM - limites"
```

Si un resultado ya existe, el generador no lo sobrescribe: cambia el nombre o
utiliza, por ejemplo, `--salida salida/revision_2`. La demostración contiene datos
en **todos** los campos, también los opcionales, para evaluar las composiciones.
La prueba de límites usa texto sintético y alcanza simultáneamente los máximos
de caracteres y saltos de cada campo; comprueba el contrato, no la corrección
didáctica ni el ajuste de cualquier texto posible. Si cambias los límites del
PPTX, esa muestra deberá actualizarse; las pruebas detectan su desfase.

Para generar una clase con cualquier chatbot, proporciona tres entradas separadas:

1. `prompts/tipos_dam_oscuro.md` y `prompts/formato_json.md`: contratos y formato.
2. `prompts/profesor.md`: metodología pedagógica.
3. Tu temario y el contexto de conocimientos previos del módulo.

No adjuntes el JSON de estrés como ejemplo de una clase. No edites los catálogos:
se regeneran desde las notas. La guía de autoría está en
[CREAR_PLANTILLAS.md](CREAR_PLANTILLAS.md).

## Decisiones visuales y límites

- Fondo oscuro `101827`, paneles sobrios y acentos turquesa, azul, verde, rojo y
  ámbar según la función. Formato panorámico 16:9.
- Los nuevos diseños usan Aptos para explicación y Consolas para código, comandos
  y miembros de clases. Los bloques nuevos monoespaciados están entre 18 y 22 pt;
  las recomendaciones de columnas por línea están en sus notas y en el catálogo.
- Las cuatro diapositivas originales se conservan sin cambios visuales ni
  contractuales. El antiguo tipo `codigo` mantiene su fuente de 14 pt y sus
  límites previos por compatibilidad: para explicación en un aula, prioriza los
  nuevos bloques más grandes y divide ejemplos extensos.
- No se reduce la fuente para encajar contenido. Los máximos no garantizan que
  cualquier distribución de palabras quepa: una línea larga, una palabra ancha
  o una fuente sustituida requieren revisión. Las recomendaciones de columnas
  son documentación, no reglas nuevas del adaptador.
- Las tablas son nativas y las formas y conectores están desagrupados. Las flechas
  se anclan a sus cajas y apuntan al final del conector (`a:tailEnd`, según la
  [introducción de Microsoft a DrawingML, §5.8.5.4](https://download.microsoft.com/download/e/1/4/e14fb96f-83b8-4a2a-84db-7fa8acbe061a/Office%20Open%20XML%20Part%203%20-%20Primer.pdf)).
- No hay imágenes variables, filas dinámicas, diagramas generados por datos,
  ejecución de código ni resaltado de sintaxis. Todos los campos son cadenas.
- Omitir un opcional vacía su texto; no elimina el cuadro, la fila ni su número.
  En `pasos`, usa tres, cuatro o cinco pasos consecutivos desde el primero.
- Las notas de metadatos se excluyen del resultado; el generador verifica el
  paquete antes de publicarlo. Las notas docentes exteriores se conservan como
  texto plano, con las limitaciones ya documentadas.

## Verificación y revisión manual pendiente

Pruebas de aceptación en `tests/test_biblioteca_docente.py`:

- Veinte nombres únicos, notas válidas y coincidencia de todos los marcadores.
- Igualdad de XML y contratos de las cuatro páginas originales respecto a
  `docente.pptx`; el JSON de herencia sigue siendo válido.
- Ejemplos, obligatorios, opcionales y rechazo del exceso de caracteres o líneas
  en cada campo de cada tipo.
- Generación de los veinte tipos y de la prueba de límites, sin metadatos internos.
- Tabla nativa de 5 × 3 celdas, conectores anclados y orientados, modificación y
  reapertura de texto y celdas; todas las formas nuevas están dentro del lienzo.
- Inversión completa de las veinte páginas y generación con los mismos tipos.
- Catálogos sincronizados con el PPTX y sus veinte ejemplos Markdown válidos.

Resultado de la suite completa: **216 pruebas pasan**. Ruff pasa en `pptgen`,
`tests` y las utilidades de integración comprobadas. La integridad incluye ZIP,
XML y resolución de todos los destinos de relaciones internas y tipos de partes
de la plantilla y de la demostración. No se hizo push al repositorio.

Se intentó renderizar la demostración con PowerPoint en modo de lectura, sin
ventana de presentación. La automatización COM no pudo iniciarse en esta sesión:
`0x80070520` (sesión de inicio de sesión no disponible). No hay LibreOffice
disponible. **No se ha realizado una revisión visual fiable ni se afirma que
todos los textos estén libres de desbordamientos.** Las pruebas estructurales y
de editabilidad no sustituyen esa revisión.

Antes de usar la biblioteca en clase, abre ambas presentaciones en PowerPoint,
comprueba las fuentes, las flechas, la tabla y los textos cercanos a los límites.
Edita una celda y una caja, mueve un nodo, guarda y reabre la copia. Si un ejemplo
queda apretado, reduce su contenido o ajusta el diseño y sus límites en las notas;
después regenera el catálogo. No ejecutes `tools/crear_tema_demo.py`: reconstruye
solo los cuatro diseños antiguos y destruiría la biblioteca ampliada de destino.
