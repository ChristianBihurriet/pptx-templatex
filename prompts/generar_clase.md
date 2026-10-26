# Preparar una clase con una IA externa al programa

Regenera primero el catálogo del tema que vas a utilizar:

```bash
pptgen --tema dam_oscuro --documentar-tipos --salida prompts
```

Adjunta manualmente `profesor.md`, `formato_json.md`, el catálogo generado
`tipos_<tema>.md` y el archivo de contexto del módulo que corresponda.
El catálogo se extrae del PPTX y documenta sus tipos, campos y límites;
`tema.json` no contiene contratos. Regénéralo después de editar la plantilla.
Sustituye los siguientes datos al pedir la clase:

> Prepara una clase teórica sobre [TEMA], para [CURSO], módulo [MÓDULO], de
> [DURACIÓN] minutos. Objetivos: [OBJETIVOS]. Conocimientos previos confirmados:
> los del archivo de contexto adjunto. No asumas conocimientos adicionales.
> Respeta la metodología de profesor.md, el contrato común de formato_json.md
> y los contratos y ejemplos del catálogo tipos_<tema>.md adjunto.
> Empieza por una situación real, formula preguntas para construir intuición y
> desarrolla cada concepto antes de usarlo. Incluye ejemplos Java ejecutables,
> explica su resultado y los errores frecuentes con los tipos disponibles.
> Devuelve solo el JSON de la presentación teórica. Separa los ejercicios en
> otro documento si los pido después. Revisa los límites de cada campo antes
> de entregar. No incluyas decisiones visuales.

Guarda la respuesta como `contenidos/<modulo>/<tema>.json`. Comprueba localmente:

```bash
pptgen contenidos/programacion/herencia.json --validar
pptgen contenidos/programacion/herencia.json --nombre "Herencia en Java"
```

Revisa el contenido y la presentación en PowerPoint antes de clase. Actualiza el
contexto de conocimientos previos solo después de confirmar qué se ha trabajado.
