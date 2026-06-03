# Handoff — Landing de Conversión Meta Ads
**Proyecto:** Cuban Groove Perú  
**Fecha:** 2026-05-31  
**Estado:** Implementado, pendiente de prueba en producción

---

## ¿Qué se construyó?

Una landing page de conversión standalone dentro del proyecto Django existente, diseñada para recibir tráfico de Meta Ads (Instagram / Facebook Reels). No reemplaza ni modifica el sitio principal.

### URL de acceso
| Entorno | URL |
|---|---|
| Desarrollo local | `http://localhost:8000/promo/` |
| Producción | `https://cubangrooveperu.com/promo/` |

---

## Archivos creados / modificados

| Archivo | Acción | Descripción |
|---|---|---|
| `templates/landing/meta_ads_jun2026.html` | Creado | Template standalone (sin navbar ni footer del sitio) |
| `content_site/views.py` | Modificado | Agregada clase `LandingMetaAdsJun2026View` |
| `content_site/urls.py` | Modificado | Agregada ruta `/promo/` → `name='landing_meta_ads'` |
| `spec/03_landing_conversion_meta_ads_jun2026.md` | Creado | Spec de diseño completo (wireframes, arquitectura, CRO) |

---

## Arquitectura de la landing

### Flujo de conversión
```
[Meta Ad / Reel]
      ↓
[HERO — viewport completo]
  Foto profesional + logo real + social proof + botón "Empezar ahora"
      ↓
[WIZARD — 1 o 2 pasos]
  Paso 1: ¿Cuál es tu experiencia bailando salsa?
    → "Nunca / menos de 6 meses"  → Salsa Cubana Básico
    → "Clases privadas"           → Clases Privadas
    → "6 meses a 1 año / +1 año"  → Paso 2
  Paso 2: ¿Qué te gustaría trabajar?
    → "Mi baile en pareja"  → Salsa Cubana Intermedio
    → "Mi estilo femenino"  → Lady Style Cubano
      ↓
[RESULTADO — tarjeta con programa recomendado]
  Nombre, tagline, descripción, beneficios, horarios por sede
      ↓
[FORMULARIO DE LEAD]
  Nombre · Apellido · Celular * · Email (opcional) · Sede (Surco / Lince)
  Submit → POST /create-lead/ (AJAX, misma vista del sitio principal)
      ↓
[WHATSAPP — abre automáticamente]
  Mensaje pre-llenado: "Hola 👋 Vi la publicidad de Cuban Groove y me gustaría
  recibir información sobre el programa [PROGRAMA] en la sede [SEDE]."
      ↓
[Secciones de confianza]
  Beneficios → Testimonios → Galería → FAQ → CTA Final
```

### Secciones de la página
| # | Sección | Propósito |
|---|---|---|
| 1 | Hero | Primer impacto, único CTA visible |
| 2 | Wizard | Guiar al usuario a su programa correcto |
| 3 | Resultado + Form | Mostrar programa + capturar datos antes de WA |
| 4 | Beneficios | Grid 2×3 con íconos Bootstrap Icons |
| 5 | Testimonios | Slider horizontal scroll-snap |
| 6 | Galería | Masonry CSS columns (sin JS extra) |
| 7 | FAQ | Accordion con aria-expanded accesible |
| 8 | CTA Final | Bloque naranja con botón WhatsApp |

---

## Stack técnico

- **Framework:** Django 5.0 (mismo del proyecto, sin dependencias nuevas)
- **Frontend:** Bootstrap 5 + Bootstrap Icons + FontAwesome (ya instalados)
- **Fuentes:** Nunito + Heebo (ya cargadas en el proyecto)
- **JS:** Vanilla JavaScript (sin librerías adicionales)
- **Lead capture:** Reutiliza el endpoint `/create-lead/` existente
- **reCAPTCHA:** v3, cargado al fondo (`defer`) para no bloquear render

---

## Paleta de colores (alineada con la marca)

| Variable CSS | Valor | Uso |
|---|---|---|
| `--cg-primary` | `#ff6a09` | Naranja — color oficial Cuban Groove |
| `--cg-primary-dk` | `#e05500` | Hover de botones naranja |
| `--cg-dark` | `#181d38` | Azul marino oscuro — secciones alternas |
| `--cg-dark-card` | `#1e2440` | Fondo de tarjetas |
| `--cg-dark-deep` | `#0f1220` | Fondo de página base |
| `--cg-dark-border` | `#2a3060` | Bordes sobre fondos oscuros |
| `--cg-green` | `#16a34a` | Color WhatsApp |

---

## Cómo editar contenido (sin tocar HTML)

Todo el contenido editable está centralizado en la clase `LandingMetaAdsJun2026View` dentro de `content_site/views.py`.

### Actualizar vacantes (hacer cada semana)
```python
# content_site/views.py → clase LandingMetaAdsJun2026View → PROGRAMS
'sedes': [
    {'id': 'surco', ..., 'vacantes': 4},   # ← cambiar este número
    {'id': 'lince', ..., 'vacantes': 3},   # ← cambiar este número
],
```
- Número `<= 2` → badge rojo "¡Solo X vacantes!" (urgencia)
- Número `> 2` → badge verde "X vacantes"
- `None` → badge verde "Disponible" (para clases privadas)

### Actualizar precios u horarios
```python
{'id': 'surco', 'schedule': 'Lunes y Miércoles', 'time': '7:00 pm – 8:30 pm', 'price': 'S/. 180 / mes', ...}
```

### Agregar sede nueva
1. Agregar objeto en `sedes` del programa correspondiente en `PROGRAMS`
2. No requiere cambios en el template

### Cambiar imagen del hero
```python
# En get_context_data():
'hero_image_url': 'URL_DE_LA_IMAGEN_REAL',
```

### Agregar testimonio
```python
# TESTIMONIALS
{'name': 'Nombre Apellido', 'role': 'Alumna desde 2025', 'text': '...', 'stars': 5},
```

### Cambiar imágenes de galería
```python
# GALLERY — reemplazar URLs de Unsplash con fotos reales
{'src': '/media/galeria/foto.jpg', 'alt': 'Descripción de la foto'},
```

---

## Tracking implementado

| Evento | Cuándo se dispara |
|---|---|
| `whatsapp_click` | Al hacer submit del formulario exitosamente |
| `final_cta_whatsapp` | Al hacer clic en el botón del CTA final |
| Meta Pixel `Contact` | En ambos eventos anteriores |
| Google Analytics | Cargado via gtag (ID: `G-14XVW4XNL5`) |
| UTMs | Capturados de la URL y guardados en `localStorage` → enviados al lead |

---

## Pendientes antes de producción

### 🔴 Críticos (hacer antes de lanzar la campaña)
- [ ] **Reemplazar imágenes de Unsplash** con fotos reales del estudio en `GALLERY` y `hero_image_url`
- [ ] **Agregar Meta Pixel ID** — buscar `GTM-XXXXXXX` y `XXXXXXXXXXXXXXXXXX` en el template y reemplazar con los IDs reales
- [ ] **Verificar el flujo completo** en móvil: Wizard → Form → Lead guardado → WhatsApp abierto
- [ ] **Probar con datos reales** en `/admin/leads/lead/` que los leads lleguen correctamente
- [ ] **Confirmar horarios y precios** actuales con el equipo antes de publicar

### 🟡 Importantes (primera semana)
- [ ] Agregar testimonios reales con nombres y fotos de alumnos actuales
- [ ] Reemplazar la foto del hero con una foto profesional del estudio/alumnos
- [ ] Actualizar vacantes cada semana en `PROGRAMS` (toma ~2 minutos)
- [ ] Configurar dominio o subdirectorio para la campaña (ej: `cubangrooveperu.com/promo/`)

### 🟢 Mejoras futuras
- [ ] Agregar Google Tag Manager (GTM) para centralizar todos los eventos de tracking
- [ ] A/B test: probar "Empezar ahora" vs "Descubrir mi programa"
- [ ] Agregar video testimonials cuando estén disponibles
- [ ] Crear variantes por mes (`meta_ads_jul2026.html`) actualizando fechas y vacantes
- [ ] Considerar una versión por sede (landing `/promo/surco/` vs `/promo/lince/`) para campañas segmentadas geográficamente

---

## Comandos útiles

```bash
# Activar entorno virtual
C:\apps\web_luxe_apps\myenv\Scripts\activate

# Levantar servidor de desarrollo
python manage.py runserver

# Verificar que no hay errores de código
python manage.py check

# Ver URL registrada
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','webluxe.settings'); django.setup(); from django.urls import reverse; print(reverse('landing_meta_ads'))"
```

---

## Contexto de diseño

La landing fue diseñada con el concepto **"Asesor Virtual"**:
- El visitante llega habiendo visto un Reel → ya tiene contexto visual
- No necesita storytelling → necesita encontrar su programa y contactar
- El wizard genera micro-compromisos (cada clic acerca al lead a convertir)
- El formulario captura datos **antes** del WhatsApp → el lead queda en la base de datos incluso si el visitante no continúa en WhatsApp
- El mensaje pre-llenado en WhatsApp llega pre-cualificado → el equipo responde más rápido y con contexto

---

*Documento generado el 2026-05-31. Actualizar cuando se realicen cambios en la landing.*
