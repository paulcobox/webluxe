---
name: project-landing-nextjs-jun2026
description: Landing de conversión Meta Ads → WhatsApp para Junio 2026, proyecto Next.js separado del Django
metadata:
  type: project
---

## Landing Next.js Meta Ads — Junio 2026

**Estado:** Spec entregado (03_landing_conversion_meta_ads_jun2026.md)
**Proyecto:** Separado del Django webluxe — nuevo repositorio Next.js 14

### Decisiones de diseño clave
- Dark mode (#0a0a0a base) + acentos ámbar/dorado (#f59e0b, #d97706)
- Tipografía: Inter via Google Fonts
- Mobile-first, inspiración Apple/Stripe/Airbnb
- Sin navbar/footer complejo — landing aislada

### Wizard UX (state machine)
- Paso 1: experiencia de baile (5 opciones)
- Paso 2 condicional: ¿qué trabajar? (solo si >6 meses)
- Resultados: 4 programas posibles
- Barra de progreso visual entre pasos

### CTA principal
- WhatsApp con mensaje pre-llenado dinámico
- Número: +51991337159
- Pattern URL: `https://wa.me/51991337159?text=...`

### Arquitectura de datos
- Todo editable en `/data/config.ts` sin tocar JSX
- Estructura: programs[], sedes[], testimonials[], faqs[], benefits[], gallery[]

### Sedes Junio 2026
- Lince y Surco únicamente

**Why:** Landing independiente para tráfico de pago Meta Ads, desacoplada del Django para poder deployar en Vercel y medir conversiones de forma aislada.
**How to apply:** Cualquier modificación futura debe mantener el data layer en config.ts separado del JSX, y el wizard como state machine pura sin side effects.
