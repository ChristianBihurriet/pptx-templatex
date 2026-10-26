# Tipos docentes: dam_oscuro

Generado desde las notas del PPTX; no editar a mano.

Origen SHA-256: `999161d5fe7dcfab9b7ea922d39d0240d0086122ff27f5566c8261de6ad09ba3`

## Contrato común

Devuelve solo JSON UTF-8. Raíz: `titulo` (texto no vacío), `diapositivas` (lista no vacía); `modulo` y `curso` son textos opcionales. No se admiten otras claves.

Cada diapositiva contiene `tipo` y los campos siguientes. Todos son cadenas, nunca null, objetos ni listas. Los obligatorios no pueden quedar vacíos. Un opcional omitido equivale a texto vacío.

Texto literal: sin Markdown ni HTML; no se ejecuta código. Usa \n para saltos y espacios para indentar. No uses controles salvo \n y \t, ni la sintaxis reservada {{ img:clave }} ni PPTGEN_METADATA. No uses claves duplicadas, NaN o Infinity.

Los máximos son bloqueantes; cuentan caracteres Unicode y líneas separadas por \n, no líneas visuales. Divide el contenido si excede un máximo. No hay truncado ni paginación automática.

## portada

Presentar el tema y orientar al alumnado al comienzo de la clase.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 100 | 2 | Texto del campo titulo. |
| subtitulo | string | no | 180 | 3 | Texto del campo subtitulo. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "portada",
      "titulo": "Herencia en Java",
      "subtitulo": "Compartir comportamiento entre clases relacionadas"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Texto literal; sin Markdown.
- Diseño fijo; revisar el ajuste visual en PowerPoint.

## pregunta

Plantear un problema cercano para construir intuición antes de la teoría.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 100 | 2 | Texto del campo titulo. |
| contenido | string | sí | 500 | 8 | Texto del campo contenido. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "pregunta",
      "titulo": "¿Dónde pondrías un comportamiento compartido?",
      "contenido": "Una aplicación de una clínica registra perros y gatos.\nAmbos tienen nombre y pueden comer.\nSi copiamos ese código en dos clases, ¿cuántos lugares debemos revisar cuando cambia?"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Texto literal; sin Markdown.
- Diseño fijo; revisar el ajuste visual en PowerPoint.

## definicion

Explicar un concepto y relacionarlo con un problema o ejemplo práctico.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 100 | 2 | Texto del campo titulo. |
| contenido | string | sí | 500 | 8 | Texto del campo contenido. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "definicion",
      "titulo": "Primero, recuerda qué es una clase",
      "contenido": "Una clase describe los datos y las operaciones de un tipo de objeto.\nUn método es una operación definida en esa clase.\nAquí usaremos un método que imprime un mensaje."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Texto literal; sin Markdown.
- Diseño fijo; revisar el ajuste visual en PowerPoint.

## codigo

Mostrar código legible y explicar su comportamiento sin ejecutarlo automáticamente.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 100 | 2 | Texto del campo titulo. |
| codigo | string | sí | 1400 | 18 | Texto del campo codigo. |
| lenguaje | string | no | 30 | 1 | Texto del campo lenguaje. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "codigo",
      "titulo": "Guarda este ejemplo como Main.java",
      "codigo": "class Animal {\n    void comer() {\n        System.out.println(\"El animal come\");\n    }\n}\n\nclass Perro extends Animal {}\n\npublic class Main {\n    public static void main(String[] args) {\n        Perro perro = new Perro();\n        perro.comer();\n    }\n}",
      "lenguaje": "java"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Texto literal; sin Markdown.
- Diseño fijo; revisar el ajuste visual en PowerPoint.

## explicacion

Desarrollar una idea y concretarla con un ejemplo breve, sin convertirla en una lista de definiciones.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| contenido | string | sí | 360 | 8 | Explicación principal en frases cortas; introduce los términos antes de utilizarlos. |
| ejemplo | string | sí | 140 | 6 | Ejemplo corto, dato, expresión o fragmento; columna monoespaciada estrecha. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "explicacion",
      "titulo": "Una lista crece con los datos",
      "contenido": "ArrayList almacena elementos en orden y ajusta su capacidad interna.\nEl tamaño indica cuántos elementos contiene, no cuántos podría alojar.\nUsa el tipo genérico para que el compilador compruebe los valores.",
      "ejemplo": "List<String> nombres =\n    new ArrayList<>();\nnombres.add(\"Ana\");\nnombres.size(); // 1"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Ejemplo en Consolas 20 pt; recomienda no superar 22 caracteres por línea. No hay resaltado de sintaxis.

## problema

Crear una necesidad de aprendizaje a partir de una situación, su dificultad y una pregunta investigable.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| situacion | string | sí | 130 | 2 | Contexto cercano al alumnado, antes de introducir la solución. |
| problema | string | sí | 200 | 5 | Dificultad observable y consecuencias; no adelantes el mecanismo que la resuelve. |
| pregunta | string | sí | 110 | 4 | Pregunta concreta que orienta el razonamiento del grupo. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "problema",
      "titulo": "¿Por qué perdemos actualizaciones?",
      "situacion": "Dos hilos incrementan el mismo contador de peticiones.",
      "problema": "Cada hilo lee, suma y escribe.\nUna escritura puede sobrescribir el cálculo del otro hilo.",
      "pregunta": "¿Cómo protegerías la operación completa, no solo la variable?"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.

## codigo_explicado

Relacionar un fragmento de código legible con la explicación de sus decisiones y efectos.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| codigo | string | sí | 420 | 11 | Fragmento autocontenido, con indentación de espacios; evita líneas largas. |
| explicacion | string | sí | 200 | 7 | Explica el flujo y el motivo de las instrucciones; no repitas literalmente el código. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "codigo_explicado",
      "titulo": "Recuperar datos con JDBC",
      "codigo": "String sql = \"SELECT nombre FROM alumno\";\ntry (var st = cn.prepareStatement(sql);\n     var rs = st.executeQuery()) {\n    while (rs.next()) {\n        System.out.println(\n            rs.getString(\"nombre\"));\n    }\n}",
      "explicacion": "La conexión cn ya está abierta.\nEl statement ejecuta la consulta.\nnext() mueve el cursor.\ntry cierra los dos recursos, incluso si se lanza una excepción."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Código en Consolas 20 pt; recomienda hasta 40 caracteres por línea. No ejecuta ni colorea el código.

## codigo_resultado

Predecir la salida y contrastarla con la ejecución mental de un fragmento corto.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| lenguaje | string | no | 24 | 1 | Etiqueta de lenguaje o entorno, sin efecto en el motor. |
| codigo | string | sí | 330 | 5 | Programa o consulta breve; los datos de entrada deben quedar claros. |
| resultado | string | sí | 130 | 2 | Salida literal, sin mezclar explicaciones dentro del bloque de resultado. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "codigo_resultado",
      "titulo": "El orden importa en una lista",
      "lenguaje": "JAVA 21",
      "codigo": "var valores = new ArrayList<Integer>();\nvalores.add(10);\nvalores.add(0, 5);\nSystem.out.println(valores);",
      "resultado": "[5, 10]"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Código en Consolas 21 pt, hasta 65 columnas recomendadas; salida en Consolas 22 pt.

## comparacion

Contrastar dos conceptos siguiendo el mismo criterio y evitando falsas equivalencias.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| izquierda_titulo | string | sí | 42 | 2 | Nombre de la primera alternativa. |
| izquierda_contenido | string | sí | 210 | 6 | Características de la primera alternativa según un criterio común. |
| derecha_titulo | string | sí | 42 | 2 | Nombre de la segunda alternativa. |
| derecha_contenido | string | sí | 210 | 6 | Características comparables con las de la columna izquierda. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "comparacion",
      "titulo": "Herencia frente a composición",
      "izquierda_titulo": "Herencia: es un",
      "izquierda_contenido": "Una subclase especializa un tipo.\nComparte su contrato y puede redefinir comportamiento.\nEjemplo: Perro es un Animal.",
      "derecha_titulo": "Composición: tiene un",
      "derecha_contenido": "Un objeto colabora con otros objetos.\nDelega trabajo sin pertenecer a su jerarquía.\nEjemplo: Coche tiene un Motor."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.

## antes_despues

Mostrar qué cambia tras una refactorización o transformación y qué propiedad se conserva.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| antes_titulo | string | sí | 36 | 1 | Estado de partida o limitación inicial. |
| antes_contenido | string | sí | 230 | 7 | Código o texto del estado inicial. |
| despues_titulo | string | sí | 36 | 1 | Estado transformado o mejora conseguida. |
| despues_contenido | string | sí | 230 | 7 | Versión comparable con el estado inicial. |
| conclusion | string | no | 140 | 2 | Síntesis de la transformación y sus límites. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "antes_despues",
      "titulo": "Separar una decisión de su resultado",
      "antes_titulo": "Condición repetida",
      "antes_contenido": "if (edad >= 18) {\n    permitirAcceso();\n}\nif (edad >= 18) {\n    mostrarPanel();\n}",
      "despues_titulo": "Intención explícita",
      "despues_contenido": "boolean esMayor = edad >= 18;\nif (esMayor) {\n    permitirAcceso();\n    mostrarPanel();\n}",
      "conclusion": "El nombre expresa la intención; comprueba que agrupar las acciones conserva el comportamiento."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Ambos bloques usan Consolas 19 pt; hasta 33 caracteres por línea recomendados.

## error_correccion

Identificar un error concreto, explicar su causa y mostrar la corrección mínima.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| codigo_error | string | sí | 230 | 7 | Fragmento incorrecto, sin ambigüedad sobre la línea que falla. |
| codigo_correcto | string | sí | 230 | 7 | Corrección del mismo ejemplo, no un programa distinto. |
| explicacion | string | sí | 150 | 2 | Causa del error y principio que evita repetirlo. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "error_correccion",
      "titulo": "Un tipo incompatible no se convierte solo",
      "codigo_error": "String edadTexto = \"18\";\nint edad = edadTexto;\n// Error de compilación",
      "codigo_correcto": "String edadTexto = \"18\";\nint edad =\n    Integer.parseInt(edadTexto);",
      "explicacion": "String e int son tipos distintos. parseInt interpreta el texto y puede fallar si no representa un entero."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Código en Consolas 19 pt; hasta 34 caracteres por línea recomendados.

## pasos

Explicar un procedimiento de tres a cinco acciones secuenciales sin ocultar sus comprobaciones.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| paso_1 | string | sí | 120 | 2 | Acción 1: comienza con un verbo y describe un resultado verificable. |
| paso_2 | string | sí | 120 | 2 | Acción 2: comienza con un verbo y describe un resultado verificable. |
| paso_3 | string | sí | 120 | 2 | Acción 3: comienza con un verbo y describe un resultado verificable. |
| paso_4 | string | no | 120 | 2 | Acción 4: comienza con un verbo y describe un resultado verificable. |
| paso_5 | string | no | 120 | 2 | Acción 5: comienza con un verbo y describe un resultado verificable. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "pasos",
      "titulo": "De un cambio local a una entrega revisada",
      "paso_1": "Revisa los cambios con git diff y ejecuta las pruebas.",
      "paso_2": "Añade únicamente los archivos pertinentes con git add.",
      "paso_3": "Crea un commit con un mensaje que explique la intención.",
      "paso_4": "Publica la rama y abre una solicitud de integración.",
      "paso_5": "Comprueba la revisión y el resultado de CI antes de integrar."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Cinco filas fijas numeradas. Los pasos 1–3 son obligatorios; 4–5 son opcionales y dejan la fila vacía al omitirse.
- No cambia el número de filas ni renumera pasos. Para tres pasos deja vacíos ambos últimos; no omitas uno intermedio.

## tabla

Explicar datos o correspondencias mediante una tabla nativa editable de estructura constante.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| encabezado_1 | string | sí | 32 | 2 | Cabecera de la columna 1. |
| encabezado_2 | string | sí | 32 | 2 | Cabecera de la columna 2. |
| encabezado_3 | string | sí | 32 | 2 | Cabecera de la columna 3. |
| fila_1_col_1 | string | sí | 42 | 2 | Texto de la fila 1, columna 1; dos líneas como máximo. |
| fila_1_col_2 | string | sí | 42 | 2 | Texto de la fila 1, columna 2; dos líneas como máximo. |
| fila_1_col_3 | string | sí | 42 | 2 | Texto de la fila 1, columna 3; dos líneas como máximo. |
| fila_2_col_1 | string | sí | 42 | 2 | Texto de la fila 2, columna 1; dos líneas como máximo. |
| fila_2_col_2 | string | sí | 42 | 2 | Texto de la fila 2, columna 2; dos líneas como máximo. |
| fila_2_col_3 | string | sí | 42 | 2 | Texto de la fila 2, columna 3; dos líneas como máximo. |
| fila_3_col_1 | string | sí | 42 | 2 | Texto de la fila 3, columna 1; dos líneas como máximo. |
| fila_3_col_2 | string | sí | 42 | 2 | Texto de la fila 3, columna 2; dos líneas como máximo. |
| fila_3_col_3 | string | sí | 42 | 2 | Texto de la fila 3, columna 3; dos líneas como máximo. |
| fila_4_col_1 | string | sí | 42 | 2 | Texto de la fila 4, columna 1; dos líneas como máximo. |
| fila_4_col_2 | string | sí | 42 | 2 | Texto de la fila 4, columna 2; dos líneas como máximo. |
| fila_4_col_3 | string | sí | 42 | 2 | Texto de la fila 4, columna 3; dos líneas como máximo. |
| nota | string | no | 100 | 1 | Aclaración de lectura, no una fila adicional. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "tabla",
      "titulo": "Una clave foránea relaciona filas",
      "encabezado_1": "Columna",
      "encabezado_2": "Tipo SQL",
      "encabezado_3": "Restricción",
      "fila_1_col_1": "id",
      "fila_1_col_2": "INTEGER",
      "fila_1_col_3": "PRIMARY KEY",
      "fila_2_col_1": "alumno_id",
      "fila_2_col_2": "INTEGER",
      "fila_2_col_3": "FK a alumno(id)",
      "fila_3_col_1": "curso_id",
      "fila_3_col_2": "INTEGER",
      "fila_3_col_3": "FK a curso(id)",
      "fila_4_col_1": "nota",
      "fila_4_col_2": "DECIMAL(4,2)",
      "fila_4_col_3": "CHECK entre 0 y 10",
      "nota": "Ejemplo de una tabla matricula: cada clave foránea referencia una clave de otra tabla."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Tabla fija de tres columnas, una cabecera y cuatro filas de datos. Todas las celdas son campos de texto obligatorios.
- No admite listas JSON, inserción de filas ni celdas combinadas. Celdas Aptos 20 pt; recomienda hasta 26 caracteres por línea.

## diagrama_flujo

Representar una secuencia lineal de cuatro etapas con cajas y conectores nativos editables.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| contexto | string | no | 140 | 2 | Entrada o contexto necesario para interpretar el proceso. |
| etapa_1 | string | sí | 26 | 2 | Nombre y resultado breve de la etapa 1. |
| etapa_2 | string | sí | 26 | 2 | Nombre y resultado breve de la etapa 2. |
| etapa_3 | string | sí | 26 | 2 | Nombre y resultado breve de la etapa 3. |
| etapa_4 | string | sí | 26 | 2 | Nombre y resultado breve de la etapa 4. |
| conclusion | string | no | 160 | 2 | Idea final sobre el flujo, sus dependencias o su resultado. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "diagrama_flujo",
      "titulo": "Del fuente al programa en ejecución",
      "contexto": "El compilador y la máquina virtual cumplen funciones distintas.",
      "etapa_1": "Fuente\n.java",
      "etapa_2": "Compilar\njavac",
      "etapa_3": "Bytecode\n.class",
      "etapa_4": "Ejecutar\nJVM",
      "conclusion": "Compilar comprueba y transforma el fuente; ejecutar pone en marcha el bytecode."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Cuatro etapas obligatorias y tres flechas izquierda → derecha. No admite decisiones, bucles ni topología variable.
- Las cajas, textos y conectores están desagrupados. Para otro número de etapas diseña otro tipo en PowerPoint.

## relaciones_clases

Explicar una jerarquía pequeña: dos clases especializan una base común y comparten un contrato.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| clase_base | string | sí | 28 | 1 | Nombre de la clase base; sin lista de clases. |
| miembros_base | string | sí | 54 | 2 | Dos atributos u operaciones significativos de la clase base. |
| clase_izquierda | string | sí | 28 | 1 | Nombre de la clase izquierda; sin lista de clases. |
| miembros_izquierda | string | sí | 64 | 2 | Dos atributos u operaciones significativos de la clase izquierda. |
| clase_derecha | string | sí | 28 | 1 | Nombre de la clase derecha; sin lista de clases. |
| miembros_derecha | string | sí | 64 | 2 | Dos atributos u operaciones significativos de la clase derecha. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "relaciones_clases",
      "titulo": "Una base común, comportamientos distintos",
      "clase_base": "Animal",
      "miembros_base": "+ nombre: String\n+ emitirSonido(): void",
      "clase_izquierda": "Perro",
      "miembros_izquierda": "+ emitirSonido(): void\n+ traerPelota(): void",
      "clase_derecha": "Gato",
      "miembros_derecha": "+ emitirSonido(): void\n+ trepar(): void"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Jerarquía fija de tres clases: las dos inferiores heredan de la superior. Las flechas apuntan a la base.
- Esquema didáctico con flechas sólidas, no notación UML completa. No representa composición ni multiplicidades.
- Miembros en Consolas 18 pt: hasta 27 caracteres por línea en la base y 32 en las especializaciones. No genera cajas ni relaciones adicionales.

## caso_practico

Plantear una tarea aplicable con contexto, requisitos observables y un criterio de éxito.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| contexto | string | sí | 180 | 7 | Situación, usuarios y necesidad real; no presupongas tecnología no explicada. |
| requisitos | string | sí | 260 | 6 | Condiciones verificables separadas por saltos; no uses una lista JSON. |
| objetivo | string | sí | 90 | 2 | Qué podrá demostrarse al terminar, no una solución completa. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "caso_practico",
      "titulo": "Guardar pedidos sin perder sus líneas",
      "contexto": "Una tienda registra un pedido y sus líneas en tablas distintas.\nUn fallo no debe dejar medio pedido guardado.",
      "requisitos": "Insertar cabecera y líneas en una transacción.\nConfirmar solo si todas las operaciones terminan.\nDeshacer los cambios ante un error.\nCerrar los recursos JDBC.",
      "objetivo": "Demostrar que un fallo en una línea no deja datos parciales."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.

## advertencia

Prevenir un error frecuente explicando su causa y una práctica alternativa concreta.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| error | string | sí | 110 | 2 | Conducta o idea equivocada descrita sin culpabilizar al alumno. |
| motivo | string | sí | 110 | 2 | Consecuencia y causa técnica que justifican la advertencia. |
| recomendacion | string | sí | 110 | 2 | Acción concreta y realizable que evita el problema. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "advertencia",
      "titulo": "Capturar una excepción no es resolverla",
      "error": "Usar un catch vacío para que el programa continúe.",
      "motivo": "El fallo desaparece de la vista, pero el estado puede quedar incompleto y la causa sin registrar.",
      "recomendacion": "Captura solo lo que puedas tratar. Informa del contexto y conserva la causa al propagar."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.

## resumen

Cerrar una explicación con tres ideas conectadas y un principio transferible a otros problemas.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| idea_1 | string | sí | 120 | 3 | Idea clave 1, expresada como una afirmación comprensible. |
| idea_2 | string | sí | 120 | 3 | Idea clave 2, expresada como una afirmación comprensible. |
| idea_3 | string | sí | 120 | 3 | Idea clave 3, expresada como una afirmación comprensible. |
| recuerda | string | sí | 90 | 5 | Principio breve que conecta las tres ideas y orienta su aplicación. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "resumen",
      "titulo": "Normalizar es decidir dónde vive cada dato",
      "idea_1": "La clave identifica una fila; no basta con que un valor parezca único en los ejemplos.",
      "idea_2": "Las dependencias ayudan a detectar datos repetidos y anomalías de actualización.",
      "idea_3": "Descomponer exige conservar la información y comprobar cómo se reconstruirá mediante consultas.",
      "recuerda": "Cada hecho en su lugar, con claves que permitan relacionarlo."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.

## terminal

Leer una sesión de consola distinguiendo instrucciones escritas y respuestas de la herramienta.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| comandos | string | sí | 230 | 4 | Comandos en orden; incluye el prompt solo si ayuda a distinguir el entorno. |
| salida | string | sí | 260 | 4 | Salida representativa de los comandos, sin inventar resultados que contradigan el ejemplo. |
| nota | string | no | 110 | 1 | Aclaración sobre el estado previo o el entorno. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "terminal",
      "titulo": "Inspeccionar antes de confirmar cambios",
      "comandos": "git status --short\ngit diff --stat\ngit log -1 --oneline",
      "salida": " M src/Alumno.java\n src/Alumno.java | 2 +-\n8a3c120 Validar la nota antes de guardarla",
      "nota": "Salida ilustrativa de un repositorio local; los identificadores de commit dependen del historial."
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Comandos Consolas 20 pt y salida Consolas 19 pt; hasta 65 caracteres por línea recomendados. No se ejecutan comandos.

## concepto_visual

Fijar una idea central con tres anclajes visuales breves en lugar de un párrafo largo.

Versión del contrato: 1. Metadatos: 1.

| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |
| --- | --- | --- | --- | --- | --- |
| titulo | string | sí | 80 | 2 | Título breve que anticipa la idea de la diapositiva. |
| concepto | string | sí | 28 | 1 | Concepto o relación central, no una frase explicativa larga. |
| explicacion | string | sí | 130 | 2 | Explicación breve que conecta el concepto con sus tres apoyos. |
| apoyo_1 | string | sí | 44 | 2 | Apoyo visual 1: ejemplo, propiedad o consecuencia del concepto. |
| apoyo_2 | string | sí | 44 | 2 | Apoyo visual 2: ejemplo, propiedad o consecuencia del concepto. |
| apoyo_3 | string | sí | 44 | 2 | Apoyo visual 3: ejemplo, propiedad o consecuencia del concepto. |

Ejemplo válido completo:

```json
{
  "titulo": "Ejemplo de clase",
  "diapositivas": [
    {
      "tipo": "concepto_visual",
      "titulo": "Un documento, tres formas de estructurar datos",
      "concepto": "Estructura y significado",
      "explicacion": "La sintaxis organiza los datos; el contrato permite interpretarlos y comprobar si son válidos.",
      "apoyo_1": "HTML\nContenido y semántica",
      "apoyo_2": "XML\nElementos y atributos",
      "apoyo_3": "JSON\nObjetos y listas"
    }
  ]
}
```

Capacidades: campos de texto en un diseño fijo; sin listas, imágenes variables ni diagramas automáticos.

- Composición fija y texto literal. Divide el contenido en varias diapositivas si no cabe.
- Los máximos cuentan caracteres y saltos explícitos, no el ajuste visual. Revisa las líneas largas.
- Tres apoyos fijos de texto; no son imágenes variables ni una lista JSON.
