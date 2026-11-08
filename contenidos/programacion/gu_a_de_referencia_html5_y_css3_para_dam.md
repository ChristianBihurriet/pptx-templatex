# Guía de Referencia: HTML5 y CSS3 (Módulo: Lenguajes de Marcas)

Esta guía recopila los conceptos fundamentales de HTML y CSS necesarios para el ciclo de **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

---

## 1. Etiquetas Básicas de HTML

HTML (*HyperText Markup Language*) es el lenguaje estándar utilizado para estructurar el contenido de las páginas web.

### Estructura Mínima de un Documento

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Primera Página</title>
</head>
<body>
    <h1>¡Hola, Mundo!</h1>
    <p>Este es el contenido principal.</p>
</body>
</html>
```

### Etiquetas Principales de Texto y Enlaces

| Etiqueta | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `<h1>` a `<h6>` | Encabezados jerárquicos (`h1` es el más importante). | `<h1>Título Principal</h1>` |
| `<p>` | Párrafo de texto. | `<p>Texto explicativo...</p>` |
| `<a>` | Enlace (*hyperlink*). Usa el atributo `href`. | `<a href="https://google.com">Buscar</a>` |
| `<img>` | Imagen (etiqueta autocerrada). Usa `src` y `alt`. | `<img src="logo.png" alt="Logo de la empresa">` |
| `<span>` | Contenedor en línea (*inline*) para dar estilo o manipular texto. | `<span class="destacado">texto</span>` |
| `<div>` | Contenedor en bloque (*block*) para agrupar elementos. | `<div>...</div>` |

### Listas

#### Listas no ordenadas (`<ul>`)
```html
<ul>
    <li>Java</li>
    <li>HTML/CSS</li>
    <li>SQL</li>
</ul>
```

#### Listas ordenadas (`<ol>`)
```html
<ol>
    <li>Descargar repositorio</li>
    <li>Compilar código</li>
    <li>Ejecutar aplicación</li>
</ol>
```

---

## 2. HTML Semántico

El HTML semántico consiste en utilizar etiquetas que describen el **significado del contenido** tanto para los navegadores como para los motores de búsqueda y herramientas de accesibilidad.

### Estructura Visual vs. Semántica

En lugar de usar `<div>` para toda la estructura de la página, se utilizan las siguientes etiquetas nativas:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Blog Dev</title>
</head>
<body>

    <!-- Encabezado superior de la web -->
    <header>
        <h1>DevBlog DAM</h1>
        <nav>
            <ul>
                <li><a href="#inicio">Inicio</a></li>
                <li><a href="#articulos">Artículos</a></li>
            </ul>
        </nav>
    </header>

    <!-- Contenido principal exclusivo del documento -->
    <main>
        <section id="articulos">
            <article>
                <h2>Introducción a Lenguajes de Marcas</h2>
                <p>Publicado el <time datetime="2026-10-29">29 de Octubre</time></p>
                <p>Las marcas permiten estructurar información...</p>
            </article>
        </section>

        <!-- Barra lateral o contenido secundario -->
        <aside>
            <h3>Enlaces de interés</h3>
            <p>Documentación oficial de MDN.</p>
        </aside>
    </main>

    <!-- Pie de página -->
    <footer>
        <p>&copy; 2026 - Módulo Lenguajes de Marcas (1º DAM)</p>
    </footer>

</body>
</html>
```

---

## 3. Formularios en HTML

Los formularios permiten a los usuarios enviar información desde el cliente hacia el servidor (clave para el desarrollo backend).

### Contenedor Principal: `<form>`

* **`action`**: URL o endpoint a donde se enviarán los datos.
* **`method`**: Método HTTP (`GET` para consultas, `POST` para enviar datos sensibles o crear registros).

### Elementos Básicos de un Formulario

```html
<form action="/registro" method="POST">
    
    <!-- Campo de Texto -->
    <div>
        <label for="nombre">Nombre completo:</label>
        <input type="text" id="nombre" name="nombre" placeholder="Ej: Ana Gómez" required>
    </div>

    <!-- Campo de Correo Electrónico -->
    <div>
        <label for="email">Correo electrónico:</label>
        <input type="email" id="email" name="email" required>
    </div>

    <!-- Campo de Contraseña -->
    <div>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" minlength="8" required>
    </div>

    <!-- Menú Desplegable (<select>) -->
    <div>
        <label for="curso">Curso escolar:</label>
        <select id="curso" name="curso">
            <option value="dam1">1º DAM</option>
            <option value="dam2">2º DAM</option>
            <option value="daw1">1º DAW</option>
        </select>
    </div>

    <!-- Área de Texto Multilínea -->
    <div>
        <label for="comentario">Comentarios:</label>
        <textarea id="comentario" name="comentario" rows="4"></textarea>
    </div>

    <!-- Botón de Envío -->
    <button type="submit">Guardar Registro</button>

</form>
```

> **Nota clave para Backend:** El atributo `name` en los `<input>` es el nombre de la clave que recibirá la petición HTTP en el servidor (ej: `request.getParameter("nombre")`).

---

## 4. Introducción a CSS

CSS (*Cascading Style Sheets*) se encarga del estilo visual de los documentos HTML.

### 4.1. Vinculación recomendada (Hoja de Estilos Externa)

En la sección `<head>` de tu documento HTML, añade:

```html
<link rel="stylesheet" href="estilos.css">
```

### 4.2. Sintaxis de una Regla CSS

```css
selector {
    propiedad: valor;
    propiedad2: valor2;
}
```

### 4.3. Selectores Básicos

1. **Selector de Etiqueta**: Afecta a todos los elementos del mismo tipo.
   ```css
   h1 {
       color: #1a365d;
       font-family: Arial, sans-serif;
   }
   ```

2. **Selector de Clase (`.`)**: Reutilizable en múltiples elementos.
   ```css
   .campo-formulario {
       border: 1px solid #cbd5e0;
       border-radius: 4px;
   }
   ```

3. **Selector de ID (`#`)**: Único por elemento en la página.
   ```css
   #boton-login {
       background-color: #2b6cb0;
       color: white;
   }
   ```

### 4.4. El Modelo de Caja (*Box Model*)

Cada elemento HTML renderizado es una caja rectangular compuesta por 4 áreas:

* **Content**: El contenido real (texto, imagen, inputs).
* **Padding**: Espacio **interior** entre el contenido y el borde.
* **Border**: El borde visible que rodea el padding.
* **Margin**: Espacio **exterior** entre la caja y los demás elementos colindantes.

```css
.tarjeta {
    width: 300px;           /* Ancho del contenido */
    padding: 16px;          /* Espacio interno */
    border: 2px solid #ccc; /* Borde visible */
    margin: 20px;           /* Separación externa */
}
```

---

## 5. Ejemplo Completo Integrado

### HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Acceso al Sistema</title>
    <link rel="stylesheet" href="estilos.css">
</head>
<body>

    <main class="contenedor">
        <form action="/login" method="POST" class="form-login">
            <h2>Iniciar Sesión</h2>

            <div class="grupo-campo">
                <label for="usuario">Usuario:</label>
                <input type="text" id="usuario" name="usuario" class="campo" required>
            </div>

            <div class="grupo-campo">
                <label for="clave">Contraseña:</label>
                <input type="password" id="clave" name="clave" class="campo" required>
            </div>

            <button type="submit" id="btn-entrar">Acceder</button>
        </form>
    </main>

</body>
</html>
```

### CSS (`estilos.css`)

```css
/* Reset básico de márgenes */
body {
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f7fafc;
}

/* Centrado del contenedor */
.contenedor {
    width: 350px;
    margin: 50px auto;
}

/* Estilo de la tarjeta de formulario */
.form-login {
    background-color: #ffffff;
    padding: 24px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

.form-login h2 {
    margin-top: 0;
    color: #2d3748;
    text-align: center;
}

/* Agrupación de campos */
.grupo-campo {
    margin-bottom: 16px;
}

.grupo-campo label {
    display: block;
    margin-bottom: 6px;
    color: #4a5568;
    font-weight: 600;
}

.campo {
    width: 100%;
    padding: 8px;
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    box-sizing: border-box; /* Incluye padding en el width total */
}

/* Botón principal */
#btn-entrar {
    width: 100%;
    padding: 10px;
    background-color: #3182ce;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
}

#btn-entrar:hover {
    background-color: #2b6cb0;
}
```