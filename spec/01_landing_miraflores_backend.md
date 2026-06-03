# SPEC 01 — Plan de Implementación Backend: Landing Miraflores Ads

**Proyecto:** webluxe — Cuban Groove Peru  
**Fecha:** 2026-05-30  
**Agente:** django-backend-specialist  
**Estado:** Pendiente implementación  
**Relacionado con:** `00_landing_miraflores_ads.md`

---

## Resumen

Plan de implementación backend para la landing page publicitaria de Miraflores. Consiste en 4 fases, sin migraciones de base de datos. Se agrega una nueva vista y una nueva URL en la app `courses`, reutilizando el endpoint `/create-lead/` de `leads` sin ninguna modificación.

---

## Archivos Afectados

| Archivo | Acción |
|---------|--------|
| `courses/views.py` | AGREGAR clase `MirafloresLandingAdsView` |
| `courses/urls.py` | AGREGAR import + 1 path |
| `templates/courses/landing_miraflores_ads.html` | CREAR (template mínimo de arranque) |
| `leads/views.py` | SIN CAMBIOS |
| `leads/models.py` | SIN CAMBIOS |
| Migraciones | NINGUNA |

---

## Fase B1 — Agregar `MirafloresLandingAdsView` en `courses/views.py`

**Archivo:** `courses/views.py`

**Qué hacer:**
Insertar la nueva clase `MirafloresLandingAdsView(TemplateView)` inmediatamente después de `MirafloresDetailTemplateView` (actualmente alrededor de la línea 157). La clase debe:

- Definir `template_name = 'courses/landing_miraflores_ads.html'`
- Implementar `get_context_data` que:
  1. Obtiene el objeto `Course` con `get_object_or_404(Course, slug='clases-de-salsa-en-miraflores')` → asignar a `course`
  2. Consulta cursos activos con `place__icontains='miraflores'`, excluyendo el `pk` del curso principal, ordenados por prioridad (Miraflores primero, luego alfabético) → asignar a `list_courses`
  3. Asigna `video_embed_url = ''` como placeholder
  4. Retorna contexto con las tres variables: `course`, `list_courses`, `video_embed_url`

**Por qué este orden:** La vista debe existir antes de registrarse en `urls.py`. Si se toca primero la URL, el servidor lanza `ImportError` al intentar resolver la clase.

**Imports necesarios:** No se requieren imports nuevos. `get_object_or_404`, `TemplateView`, `Course`, `Case`, `When`, `Value`, `IntegerField`, `Q` ya están presentes en el archivo.

**Bug a NO replicar:** La `MirafloresDetailTemplateView` existente filtra por `place__icontains='surco'` (bug confirmado). La nueva vista debe usar `place__icontains='miraflores'` correctamente.

**Validación:**
```bash
python manage.py check courses
```
Debe retornar 0 errores.

---

## Fase B2 — Registrar URL en `courses/urls.py`

**Archivo:** `courses/urls.py`

**Sub-paso 2a — Agregar el import:**
En la línea del import de views, agregar `MirafloresLandingAdsView` a la lista de clases importadas (misma línea que `MirafloresDetailTemplateView`).

**Sub-paso 2b — Agregar el path:**
Insertar la nueva URL **antes** del catch-all `clases-baile/<slug:course_slug>/` (que debe permanecer como último elemento):

```
path('landing/miraflores-baile/', MirafloresLandingAdsView.as_view(), name='landing_miraflores_ads'),
```

Posición recomendada: inmediatamente después de `clases-de-salsa-en-miraflores/`.

**Por qué este orden:** El patrón `<slug:course_slug>` es un catch-all de un segmento. El path `landing/miraflores-baile/` tiene dos segmentos y no colisiona, pero por convención del proyecto el slug-detail va siempre al final absoluto.

**Validación:**
```bash
python manage.py shell -c "from django.urls import reverse; print(reverse('landing_miraflores_ads'))"
```
Debe imprimir `/landing/miraflores-baile/` sin excepciones.

---

## Fase B3 — Crear template mínimo de arranque

**Archivo:** `templates/courses/landing_miraflores_ads.html`

**Qué hacer:**
Crear el archivo con estructura mínima que permita validar que la vista renderiza sin errores antes de que el frontend construya el template completo:
- Extender `_base.html`
- Referenciar `{{ course.title }}`, `{{ list_courses }}`, `{{ video_embed_url }}`
- Un bloque `{% for c in list_courses %}{{ c.title }}{% endfor %}` para confirmar que el queryset no produce errores

**Por qué este orden:** Sin el template, cualquier request a la URL retornará `TemplateDoesNotExist`. El template mínimo desbloquea la Fase B4 y el trabajo paralelo del agente frontend.

---

## Fase B4 — Smoke test end-to-end

**Qué verificar con el servidor corriendo:**

1. `GET /landing/miraflores-baile/` → HTTP 200
2. `{{ course.title }}` se renderiza (confirma que `get_object_or_404` encuentra el slug)
3. `list_courses` no incluye el curso principal (confirma exclusión por `pk`)
4. `list_courses` usa `place__icontains='miraflores'` y no `'surco'` (confirma que el bug no se replicó)
5. `GET /clases-de-salsa-en-miraflores/` → HTTP 200 (confirma que la página SEO existente no se rompió)

**Comandos:**
```bash
python manage.py runserver
# En otra terminal:
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/landing/miraflores-baile/
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/clases-de-salsa-en-miraflores/
```
Ambos deben retornar `200`.

---

## Riesgos Backend

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Replicar el bug `place__icontains='surco'` al copiar la vista existente | Alta | Verificar explícitamente en Fase B4, paso 4 |
| Path `landing/miraflores-baile/` colocado después del catch-all `<slug>` | Alta | Verificar posición en `urlpatterns` antes de guardar |
| Olvidar agregar `MirafloresLandingAdsView` al import de `urls.py` | Alta | El `manage.py check` de Fase B2 lo detecta antes de correr el servidor |
| Slug hardcodeado `'clases-de-salsa-en-miraflores'` eliminado del admin | Baja | Comportamiento esperado con `get_object_or_404` → HTTP 404 |
| Cache middleware sirviendo respuesta errónea de pruebas previas | Baja | `python manage.py clear_cache` si ocurre |

---

## Orden de Ejecución

```
B1 → B2 → B3 → B4
```

B3 puede ejecutarse en paralelo con B1 y B2 si el frontend ya comenzó su trabajo, pero B4 requiere las tres anteriores completas.

---

## Contexto para el Siguiente Agente

Una vez completadas las 4 fases backend, el agente `frontend-dev-specialist` puede construir el template completo en `templates/courses/landing_miraflores_ads.html` reemplazando el template mínimo de arranque. Ver spec `02_landing_miraflores_frontend.md` para el plan frontend detallado.
