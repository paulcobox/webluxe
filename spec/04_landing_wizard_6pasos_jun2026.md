# SPEC 04 — Landing Wizard 6 Pasos (Rediseño)
**Proyecto:** Cuban Groove Perú  
**Fecha:** 2026-05-31  
**Estado:** Aprobado — pendiente implementación  
**Reemplaza:** spec/03 (wizard 2 pasos)  
**URL:** `/promo/`

---

## Concepto

Landing de conversión para tráfico de Meta Ads. Flujo tipo quiz/asesor que guía al usuario en 6 pasos, cada uno visible en **un solo viewport sin scroll**. Al final captura los datos del lead y abre WhatsApp con contexto completo del perfil.

---

## Decisiones de diseño globales

| Elemento | Decisión |
|---|---|
| Navbar | Solo logo — sin links de navegación, sin hamburguesa |
| Botón flotante WhatsApp | **Eliminado** — forzar uso del formulario |
| Fondo general | Blanco (#ffffff) — tema claro, igual al sitio |
| Color primario | `#ff6a09` naranja — marca Cuban Groove |
| Cada paso | Ocupa exactamente un viewport (no scroll) |
| Progreso | Barra horizontal + "Paso X de 6" en cada step |

---

## Datos de programas y horarios

| Programa | Sede | Día | Hora | Referencia |
|---|---|---|---|---|
| Salsa Cubana Básico | Surco | Miércoles | 8:30 pm – 10:00 pm | Cerca al Óvalo Higuereta |
| Salsa Cubana Básico | Lince | Viernes | 8:00 pm – 10:00 pm | A 1 cdra. de Plaza Vea de Risso |
| Salsa Cubana Intermedio | Surco | Martes | 8:00 pm – 10:00 pm | Cerca al Óvalo Higuereta |
| Lady Style Cubano | Lince | Sábados | 6:00 pm – 8:30 pm | A 1 cdra. de Plaza Vea de Risso |
| Clases Privadas | Surco / Lince / Domicilio | A coordinar | Horario flexible | — |

### Precio (igual para todos los programas)
**S/. 170 / mes**

---

## Beneficios por programa

### 🟢 Salsa Cubana Básico
- ✓ Aprende desde cero, paso a paso
- ✓ Fundamentos del movimiento
- ✓ Descubre los fundamentos del auténtico estilo cubano

### 🔵 Salsa Cubana Intermedio
- ✓ Amplía tu repertorio de movimientos y combinaciones
- ✓ Mejora tu musicalidad, fluidez y conexión al bailar
- ✓ Lleva tu salsa cubana al siguiente nivel

### 🟣 Lady Style Cubano
- ✓ Potencia tu estilo, elegancia y presencia escénica
- ✓ Desarrolla movimiento corporal, técnica y expresión femenina
- ✓ Gana seguridad y confianza al bailar

### 🔒 Clases Privadas
- ✓ Progreso personalizado a tu ritmo
- ✓ Horarios totalmente flexibles
- ✓ Corrección técnica inmediata
- ✓ Metodología adaptada a tus objetivos

---

## Card de inversión (aparece en Step 5 al elegir sede)

```
💰 Inversión mensual: S/. 170

✅ 4 sesiones al mes
✅ Formación progresiva
✅ Profesor especializado
✅ Feedback con video (análisis y correcciones)
✅ Dinámicas sociales guiadas
```

**Texto de acompañamiento:**
> ✨ Trabajamos paso a paso, con acompañamiento real, para que desarrolles
> coordinación, confianza y conexión con tu cuerpo desde la primera clase.

**Texto de cierre antes del botón WA:**
> Esta es una recomendación inicial. Tu asesor puede mostrarte más opciones
> y armar un paquete personalizado para ti.

---

## Lógica de recomendación (Step 0 + Step 2)

| Experiencia (Step 0) | Objetivo (Step 2) | Programa resultante |
|---|---|---|
| Nunca he bailado | Cualquiera | Salsa Cubana Básico |
| Menos de 6 meses | Cualquiera | Salsa Cubana Básico |
| 6 meses – 1 año o Más de 1 año | Aprender desde cero / ritmo | Salsa Cubana Básico |
| 6 meses – 1 año o Más de 1 año | Bailar en pareja / Casino | Salsa Cubana Intermedio |
| 6 meses – 1 año o Más de 1 año | Estilo y expresión femenina | Lady Style Cubano |
| 6 meses – 1 año o Más de 1 año | Formación técnico-profesional | Salsa Cubana Intermedio |
| Quiero clases privadas | — (salta Step 2) | Clases Privadas |

---

## Flujo completo — 6 pasos

### STEP 0 — Hero + Experiencia *(viewport 1)*

**Zona foto (fondo con overlay → gradiente a blanco):**
- ⭐⭐⭐⭐⭐ Más de 500 alumnos formados
- H1: "Comienza tu formación en Salsa Cubana"
- Subtítulo: "Descubriremos el programa ideal para tu nivel y objetivos."

**Panel blanco (parte inferior):**
- Pregunta: "¿Cuál es tu experiencia bailando salsa?"
- Opciones:
  - Nunca he bailado
  - Menos de 6 meses
  - Entre 6 meses y 1 año
  - Más de 1 año
  - Quiero clases privadas

**Guarda:** `exp` = `'basico'` | `'avanzado'` | `'privadas'`  
**Si `privadas`:** omite Step 2, pasa directo a Step 1 → Step 3 → Step 4 → Step 5

---

### STEP 1 — Edad *(viewport 2)*

- Progreso: Paso 2 de 6 · 33%
- Pregunta: "¿Cuántos años tienes?"
- Subtítulo: "Esto nos ayuda a personalizar mejor tu programa."
- Opciones: 18–24 / 25–34 / 35–44 / 45–54 / 55+

**Guarda:** `edad` (se incluye en nota del lead y mensaje al asesor)

---

### STEP 2 — Objetivo principal *(viewport 3)*

- Progreso: Paso 3 de 6 · 50%
- Pregunta: "¿Cuál es tu principal objetivo al aprender salsa?"
- Opciones con ícono + descripción:

| Ícono | Opción | Mapea a |
|---|---|---|
| 🎵 | Aprender desde cero y ganar ritmo y confianza | Básico |
| 👫 | Bailar en pareja, Casino y pasos sueltos | Intermedio |
| 💃 | Desarrollar mi estilo y expresión femenina | Lady Style |
| 🏆 | Formarme a nivel técnico-profesional | Intermedio |

**Aquí se calcula el programa final** (combinando `exp` + `objetivo`)

*Nota: Si `exp = 'privadas'`, este paso se omite.*

---

### STEP 3 — "¡Genial! Preparando tu programa..." *(viewport 4)*

- Progreso: Paso 4 de 6 · 67%
- Título: "🎉 ¡Genial! Estamos preparando tu programa personalizado..."
- Barra de carga animada (CSS, dura 3 segundos)
- Carrusel de testimonios (auto-avanza cada 3s):
  - Testimonio 1: María García — "Llegué sin saber nada y en 3 meses ya estaba en la pista..."
  - Testimonio 2: Carlos Mendoza — "La metodología es diferente a otras academias..."
  - Testimonio 3: Lucía Torres — "El Lady Style me cambió la vida..."
  - Testimonio 4: Rodrigo Paz — "Con las clases privadas avancé el doble de rápido..."
- Dots de navegación (●○○)
- Botón "Continuar →" aparece después de 3 segundos

---

### STEP 4 — Captura de datos *(viewport 5)*

- Progreso: Paso 5 de 6 · 83%
- Título: "Ya casi está 🙌"
- Subtítulo: "Un asesor revisará tu perfil y te contactará hoy mismo."
- Campos:
  - Nombre * (col-6)
  - Apellido * (col-6)
  - WhatsApp / Celular * (col-12, inputmode numeric)
  - Correo (opcional, col-12)
- Botón: "Ver mi programa recomendado →" (naranja)
- Microcopy: "🔒 Sin spam. Datos 100% seguros."

**Al submit:**
1. Validar campos requeridos
2. POST `/create-lead/` con:
   - Datos del formulario (nombre, apellido, teléfono, email)
   - `notes`: perfil completo del quiz (experiencia + edad + objetivo)
   - UTMs capturados de la URL
3. Si éxito → avanzar a Step 5

---

### STEP 5 — Resultado + Precio + CTA *(viewport 6)*

- Progreso: 100% ✓

**5a — Tarjeta del programa recomendado:**
- Badge de color por programa (verde/azul/morado/gris)
- Nombre del programa (grande)
- 3 bullets de beneficios específicos del programa
- Separador

**5b — Selector de sede/horario:**
- Título: "Elige tu horario:"
- Cards clicables por sede (según programa):
  - **Básico:** Surco (Mié 8:30–10pm · Cerca al Óvalo Higuereta) + Lince (Vie 8–10pm · 1 cdra. Plaza Vea Risso)
  - **Intermedio:** Surco (Mar 8–10pm · Cerca al Óvalo Higuereta) — solo una sede
  - **Lady Style:** Lince (Sáb 6–8:30pm · 1 cdra. Plaza Vea Risso) — solo una sede
  - **Privadas:** Surco · Lince · Domicilio

**5c — Card de inversión (aparece al seleccionar sede, con animación):**
```
💰 Inversión mensual: S/. 170
✅ 4 sesiones al mes
✅ Formación progresiva
✅ Profesor especializado
✅ Feedback con video (análisis y correcciones)
✅ Dinámicas sociales guiadas
```
Texto: "✨ Trabajamos paso a paso, con acompañamiento real, para que desarrolles coordinación, confianza y conexión con tu cuerpo desde la primera clase."

**5d — CTA WhatsApp:**
- Texto previo: "Esta es una recomendación inicial. Tu asesor puede mostrarte más opciones y armar un paquete personalizado para ti."
- Botón: "💬 Hablar con mi asesor ahora" (verde WhatsApp, ancho completo)
- Microcopy: "🔒 Sin compromisos."

---

## Mensaje WhatsApp (con contexto completo)

```
Hola 👋 Vi la publicidad de Cuban Groove.

Mi perfil:
• Experiencia: [respuesta step 0]
• Edad: [rango step 1]
• Objetivo: [respuesta step 2]
• Sede elegida: [Surco / Lince / Domicilio]

Programa sugerido: [nombre programa]
Mi nombre es [nombre] [apellido].

Me gustaría recibir información y hablar con un asesor.
```

---

## Estructura técnica

### Archivos a modificar

| Archivo | Cambio |
|---|---|
| `templates/landing/meta_ads_jun2026.html` | Reescritura completa del wizard (6 pasos), navbar solo-logo, sin botón WA flotante, carrusel testimonios, card de precio |
| `content_site/views.py` | Actualizar `PROGRAMS` con horarios/referencias/bullets reales. Actualizar `WIZARD_CONFIG` a 6 pasos |

### Variables de estado del wizard (JavaScript)

```javascript
wizardState = {
  currentStep: 0,           // 0–5
  exp: null,                // 'basico' | 'avanzado' | 'privadas'
  edad: null,               // '18-24' | '25-34' | ...
  objetivo: null,           // 'ritmo' | 'pareja' | 'femenino' | 'tecnico'
  programaFinal: null,      // calculado al terminar step 2
  sedeElegida: null,        // 'surco' | 'lince' | 'domicilio'
  nombre: null,             // del formulario
  apellido: null,
}
```

### Lógica de pasos por ruta

```
Ruta A (experiencia básica):
  Step 0 → Step 1 → Step 2 → Step 3 → Step 4 → Step 5

Ruta B (privadas):
  Step 0 → Step 1 → Step 3 → Step 4 → Step 5
  (omite Step 2 — objetivo no aplica para privadas)
```

### CSS — cada paso es un "screen"

```css
.cg-wizard-screen {
  min-height: 100svh;           /* ocupa viewport completo */
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1.5rem;
  background: white;
}

/* Step 0 es especial: tiene foto de fondo */
.cg-wizard-screen--hero {
  background: [foto] con overlay → blanco;
}
```

### Barra de progreso

| Step | Paso visible | % |
|---|---|---|
| 0 | Paso 1 de 6 | 17% |
| 1 | Paso 2 de 6 | 33% |
| 2 | Paso 3 de 6 | 50% |
| 3 | Paso 4 de 6 | 67% |
| 4 | Paso 5 de 6 | 83% |
| 5 | Completado | 100% |

---

## Tracking

| Evento | Cuándo |
|---|---|
| `wizard_start` | Al cargar la página |
| `wizard_step_complete` | Al completar cada step (con step number) |
| `lead_submitted` | Al enviar formulario exitosamente |
| `whatsapp_click` | Al hacer clic en botón WA del resultado |
| Meta Pixel `Lead` | Al enviar formulario |
| Meta Pixel `Contact` | Al hacer clic en WA |

---

## Paleta de colores

| Variable | Valor | Uso |
|---|---|---|
| `--cg-primary` | `#ff6a09` | Naranja marca — botones, progress, acentos |
| `--cg-primary-dk` | `#e05500` | Hover botones naranja |
| `--cg-green` | `#16a34a` | Botón WhatsApp |
| `--cg-border` | `#e5e7eb` | Bordes de cards y opciones |
| `--cg-text` | `#1f2937` | Texto principal |
| `--cg-muted` | `#6b7280` | Texto secundario |
| Badge Básico | `#16a34a` (verde) | Color identificador del programa |
| Badge Intermedio | `#2563eb` (azul) | Color identificador del programa |
| Badge Lady Style | `#7c3aed` (morado) | Color identificador del programa |
| Badge Privadas | `#374151` (gris) | Color identificador del programa |

---

*Spec generado el 2026-05-31. Aprobado por el usuario. Listo para implementación.*