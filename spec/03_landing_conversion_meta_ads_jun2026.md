# SPEC 03 — Landing de Conversión Meta Ads → WhatsApp (Junio 2026)

**Proyecto:** webluxe — Cuban Groove Peru  
**Fecha:** 2026-05-30  
**Agente:** designer  
**Estado:** Pendiente implementación  
**Stack:** Next.js 14 (App Router) + TypeScript + Tailwind CSS  

---

## Contexto

Landing page independiente del sitio Django, diseñada exclusivamente para recibir tráfico de Meta Ads (Instagram/Facebook Reels). El visitante ya consumió contenido audiovisual antes de llegar — necesita conversión directa, no storytelling.

**Objetivo primario:** Convertir visitantes en leads calificados por WhatsApp, guiándolos a encontrar el programa correcto mediante un wizard de 1–2 pasos.

**Sedes activas Junio 2026:** Lince y Surco únicamente.

---

## 1. Wireframe UX Completo

### Sección 1 — Hero (viewport completo, mobile-first)

```
┌─────────────────────────────────────────────────┐
│  [FOTO PROFESIONAL — fondo oscuro, overlay 50%]  │
│                                                   │
│  ┌── Logo Cuban Groove (top-center, 48px) ──┐    │
│  └───────────────────────────────────────────┘    │
│                                                   │
│         [Espacio flex grow]                       │
│                                                   │
│  ┌── CONTENIDO HERO (bottom-aligned, px-6) ──┐   │
│  │                                            │   │
│  │  ★★★★★  Más de 500 alumnos formados        │   │
│  │  [text-amber-400, text-sm, mb-4]           │   │
│  │                                            │   │
│  │  Encuentra el programa                     │   │
│  │  ideal para ti                             │   │
│  │  [text-white, text-4xl/5xl, font-bold]     │   │
│  │                                            │   │
│  │  Te ayudamos a descubrir cuál es           │   │
│  │  el mejor camino según tu experiencia.     │   │
│  │  [text-gray-300, text-base, mt-3]          │   │
│  │                                            │   │
│  │  [btn: EMPEZAR AHORA →]                    │   │
│  │  [bg-amber-500, text-black, w-full,        │   │
│  │   py-4, rounded-2xl, font-bold, text-lg]   │   │
│  │                                            │   │
│  └────────────────────────────────────────────┘   │
│  [pb-12]                                          │
└─────────────────────────────────────────────────┘

DESKTOP (lg:):
┌──────────────────────────────────────────────────────┐
│  [FOTO — full bleed, overlay gradient left]           │
│                                                       │
│  Logo (top-left, pl-16)        [espacio]              │
│                                                       │
│  ┌── max-w-lg, pl-16, pb-20 ──────────────────┐      │
│  │  ★★★★★ Más de 500 alumnos formados          │      │
│  │                                             │      │
│  │  Encuentra el programa                      │      │
│  │  ideal para ti                              │      │
│  │  [text-5xl/6xl, leading-tight]              │      │
│  │                                             │      │
│  │  Subtítulo [text-gray-300, text-lg]         │      │
│  │                                             │      │
│  │  [EMPEZAR AHORA →]  [w-auto, px-10]         │      │
│  └─────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────┘
```

### Sección 2 — Wizard de Recomendación

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-900, py-20, px-6]                      │
│                                                   │
│  ┌── Barra de progreso ──────────────────────┐   │
│  │  [bg-zinc-800, h-1, rounded-full]          │   │
│  │  [fill amber-500, transition-all 500ms]    │   │
│  │  Paso 1 de 2                               │   │
│  └────────────────────────────────────────────┘   │
│                                                   │
│  ¿Cuál es tu experiencia                            │
│  bailando salsa?                                  │
│  [text-white, text-2xl/3xl, font-bold, mb-8]      │
│                                                   │
│  ┌── CARDS OPCIONES (stack vertical mobile) ──┐   │
│  │                                             │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  Nunca he bailado                   │   │   │
│  │  │  [card: bg-zinc-800, border-zinc-700│   │   │
│  │  │   hover:border-amber-500,           │   │   │
│  │  │   p-5, rounded-2xl, cursor-pointer] │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  │  [gap-3 entre cards]                        │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  Menos de 6 meses                   │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  Entre 6 meses y 1 año              │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  Más de 1 año                       │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────┐   │   │
│  │  │  Prefiero clases privadas           │   │   │
│  │  └─────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘

PASO 2 (condicional, misma sección):
┌─────────────────────────────────────────────────┐
│  Barra progreso [100%]                            │
│  Paso 2 de 2                                      │
│                                                   │
│  ¿Qué te gustaría                                 │
│  trabajar?                                        │
│                                                   │
│  ┌─ card ─────────────────────────────────────┐   │
│  │  Mi baile en pareja                         │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─ card ─────────────────────────────────────┐   │
│  │  Mi estilo femenino                         │   │
│  └─────────────────────────────────────────────┘   │
│                                                   │
│  [← Volver]  [text-gray-400, text-sm]             │
└─────────────────────────────────────────────────┘
```

### Sección 3 — Resultado Personalizado

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-950, py-20, px-6]                      │
│                                                   │
│  Tu programa recomendado:                         │
│  [text-amber-400, text-sm, uppercase, tracking]   │
│                                                   │
│  ┌── TARJETA PROGRAMA (bg-zinc-900, rounded-3xl,──┐│
│  │   border border-amber-500/30, p-8)              ││
│  │                                                 ││
│  │  [Icono programa — 48px, amber]                 ││
│  │  SALSA CUBANA BÁSICO                            ││
│  │  [text-white, text-2xl, font-bold]              ││
│  │                                                 ││
│  │  Para quienes empiezan desde cero...            ││
│  │  [text-gray-400, text-sm, mb-6]                 ││
│  │                                                 ││
│  │  ✓ Fundamentos de movimiento cubano             ││
│  │  ✓ Trabajo de cadera y ritmo                    ││
│  │  ✓ Vocabulario básico de Casino                 ││
│  │  [text-gray-300, text-sm, gap-2]                ││
│  │                                                 ││
│  │  ─── SEPARATOR ────────────────────────         ││
│  │                                                 ││
│  │  SEDES DISPONIBLES                              ││
│  │  [text-gray-500, text-xs, uppercase]            ││
│  │                                                 ││
│  │  ┌─ Surco ──────────────────────────────┐      ││
│  │  │  📍 Surco        🗓 Lunes / Miércoles │      ││
│  │  │  🕐 7:00 pm – 8:30 pm    S/. 180/mes │      ││
│  │  │  🟢 Vacantes disponibles: 4           │      ││
│  │  └──────────────────────────────────────┘      ││
│  │  ┌─ Lince ──────────────────────────────┐      ││
│  │  │  📍 Lince        🗓 Martes / Jueves   │      ││
│  │  │  🕐 7:00 pm – 8:30 pm    S/. 180/mes │      ││
│  │  │  🟢 Vacantes disponibles: 3           │      ││
│  │  └──────────────────────────────────────┘      ││
│  │                                                 ││
│  │  [BTN: RESERVAR MI VACANTE → WhatsApp]          ││
│  │  [bg-green-500, text-white, w-full, py-4]       ││
│  │                                                 ││
│  │  🔒 Sin compromisos. Conversación directa.      ││
│  │  [text-gray-500, text-xs, text-center]          ││
│  └─────────────────────────────────────────────────┘│
│                                                   │
│  [BTN secundario: Volver a empezar]               │
│  [text-gray-500, text-sm, underline]              │
└─────────────────────────────────────────────────┘
```

### Sección 4 — Beneficios

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-900, py-20, px-6]                      │
│                                                   │
│  Por qué elegir Cuban Groove                      │
│  [text-white, text-2xl, font-bold, text-center]   │
│                                                   │
│  MOBILE: grid 2 columnas, gap-4                   │
│  ┌──────────┐  ┌──────────┐                       │
│  │   🎵     │  │   👤     │                       │
│  │ Desde    │  │ Sin      │                       │
│  │ cero     │  │ pareja   │                       │
│  └──────────┘  └──────────┘                       │
│  ┌──────────┐  ┌──────────┐                       │
│  │   🏆     │  │   🇨🇺     │                       │
│  │ Profes   │  │ Cultura  │                       │
│  │ especial │  │ auténtica│                       │
│  └──────────┘  └──────────┘                       │
│  ┌──────────┐  ┌──────────┐                       │
│  │   😊     │  │   🎓     │                       │
│  │ Ambiente │  │ Técnica  │                       │
│  │ amigable │  │ y social │                       │
│  └──────────┘  └──────────┘                       │
│                                                   │
│  DESKTOP: grid 3 columnas                         │
└─────────────────────────────────────────────────┘
```

### Sección 5 — Testimonios

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-950, py-20, overflow-hidden]           │
│                                                   │
│  Lo que dicen nuestros alumnos                    │
│  [text-center, text-white, text-2xl, mb-10]       │
│                                                   │
│  ← [SLIDER HORIZONTAL — snap-x] →                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────┐  │
│  │ [Foto 80px]  │ │ [Foto 80px]  │ │ ...      │  │
│  │ Nombre       │ │ Nombre       │ │          │  │
│  │ Profesión    │ │ Profesión    │ │          │  │
│  │              │ │              │ │          │  │
│  │ "Texto del   │ │ "Texto del   │ │          │  │
│  │  testimonio" │ │  testimonio" │ │          │  │
│  │              │ │              │ │          │  │
│  │ ★★★★★        │ │ ★★★★★        │ │          │  │
│  └──────────────┘ └──────────────┘ └──────────┘  │
│  [Dots de navegación — amber]                     │
└─────────────────────────────────────────────────┘
```

### Sección 6 — Galería

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-900, py-20, px-4]                      │
│                                                   │
│  Nuestras clases                                  │
│  [text-center, text-white, text-2xl, mb-8]        │
│                                                   │
│  MOBILE: columns-2, gap-2                         │
│  ┌─────┐ ┌─────┐                                  │
│  │ img │ │ img │  ← break-inside-avoid            │
│  │tall │ │     │                                  │
│  │     │ │ img │                                  │
│  │     │ │wide │                                  │
│  └─────┘ └─────┘                                  │
│                                                   │
│  DESKTOP: columns-3                               │
└─────────────────────────────────────────────────┘
```

### Sección 7 — FAQ Accordion

```
┌─────────────────────────────────────────────────┐
│  [bg-zinc-950, py-20, px-6]                      │
│                                                   │
│  Preguntas frecuentes                             │
│  [text-center, text-white, text-2xl, mb-10]       │
│                                                   │
│  ┌── ITEM FAQ ──────────────────────────────┐    │
│  │  ¿Necesito venir con pareja?    [+ / −]   │    │
│  └───────────────────────────────────────────┘    │
│  [border-b border-zinc-800]                       │
│  ┌── ITEM FAQ (expanded) ───────────────────┐    │
│  │  ¿Puedo empezar desde cero?    [−]        │    │
│  │                                           │    │
│  │  Sí, la mayoría de nuestros alumnos...    │    │
│  │  [text-gray-400, text-sm, pb-4]           │    │
│  └───────────────────────────────────────────┘    │
│  [...3 preguntas más]                             │
└─────────────────────────────────────────────────┘
```

### Sección 8 — CTA Final

```
┌─────────────────────────────────────────────────┐
│  [bg-amber-500, py-24, px-6, text-center]        │
│                                                   │
│  Tu próxima versión                               │
│  comienza aquí.                                   │
│  [text-black, text-3xl/4xl, font-bold]            │
│                                                   │
│  Reserva tu vacante para Junio 2026.              │
│  [text-black/70, text-base, mt-4, mb-8]           │
│                                                   │
│  [BTN: 💬 Hablar por WhatsApp]                    │
│  [bg-black, text-white, w-full/auto,              │
│   py-4, px-10, rounded-2xl, font-bold]            │
│                                                   │
│  Instagram | TikTok | YouTube  [links grises]     │
└─────────────────────────────────────────────────┘
```

---

## 2. Arquitectura de Componentes

```
/src
  /app
    page.tsx                    → Orquesta secciones, import data config
    layout.tsx                  → Metadata, fonts, Google Analytics/GTM/Pixel
    globals.css                 → Tailwind base + custom scroll-snap

  /components
    /landing
      Hero.tsx                  → props: title, subtitle, ctaLabel, stats{count,label}
      Wizard.tsx                → state machine, emite: {program, step}; contiene WizardStep
      WizardStep.tsx            → props: question, options[]{id,label,icon?}, onSelect(id)
      ProgressBar.tsx           → props: current, total
      ProgramResult.tsx         → props: program(ProgramConfig), onReset; genera URL WhatsApp
      Benefits.tsx              → props: items[]{icon, title, description}
      Testimonials.tsx          → props: items[]{name, role, text, photo?}; CSS snap scroll
      Gallery.tsx               → props: images[]{src, alt, aspectRatio?}; CSS columns
      FAQ.tsx                   → props: items[]{question, answer}; useState accordion
      FinalCTA.tsx              → props: title, subtitle, whatsappNumber

    /ui
      Button.tsx                → variant: 'primary'|'secondary'|'ghost', size, fullWidth
      Card.tsx                  → variant: 'option'|'result'|'benefit'|'testimony'
      Badge.tsx                 → props: children, variant: 'stars'|'info'|'warning'
      Icon.tsx                  → wrapper para Lucide icons con size/color
      SectionTitle.tsx          → props: eyebrow?, title, subtitle?; variants de color

  /data
    config.ts                   → SOURCE OF TRUTH: todos los datos editables

  /lib
    whatsapp.ts                 → buildWhatsAppUrl(phone, program, sede) → string
    analytics.ts                → helpers GTM dataLayer push

  /types
    index.ts                    → ProgramConfig, SedeConfig, TestimonialConfig, etc.
```

### Relaciones clave

```
page.tsx
  ├── Hero          (lee: siteConfig.stats)
  ├── Wizard        (lee: wizardConfig, emite: selectedProgram)
  │     └── WizardStep (x2 pasos)
  │           └── ProgressBar
  ├── ProgramResult (recibe: selectedProgram, lee: programs[selected])
  ├── Benefits      (lee: benefitsConfig)
  ├── Testimonials  (lee: testimonialsConfig)
  ├── Gallery       (lee: galleryConfig)
  ├── FAQ           (lee: faqConfig)
  └── FinalCTA      (lee: siteConfig.whatsapp)
```

---

## 3. Configuración Editable — /data/config.ts

```typescript
// /data/config.ts
// ============================================================
// EDITAR ESTE ARCHIVO para actualizar precios, horarios,
// vacantes, testimonios, sin tocar ningún componente JSX.
// ============================================================

import type {
  SiteConfig,
  ProgramConfig,
  BenefitItem,
  TestimonialItem,
  GalleryImage,
  FAQItem,
  WizardConfig,
} from '@/types';

// ─── CONFIGURACIÓN GLOBAL ───────────────────────────────────
export const siteConfig: SiteConfig = {
  name: 'Cuban Groove Perú',
  whatsappNumber: '51991337159',
  stats: {
    count: '500+',
    label: 'alumnos formados',
  },
  hero: {
    title: 'Comienza tu formación en Salsa Cubana',
    subtitle:
      'Responde unas preguntas y te recomendaremos el programa más adecuado para tu nivel.',
    ctaLabel: 'Empezar ahora',
    // Reemplazar con URL de imagen real (Cloudinary, S3, etc.)
    heroImageUrl: 'https://images.unsplash.com/photo-1545959570-a94084071b5d?w=1200',
  },
  social: {
    instagram: 'https://www.instagram.com/cubangroove/',
    tiktok: 'https://www.tiktok.com/@cubangrooveperu',
    youtube: 'https://www.youtube.com/@CubanGroovePeru',
  },
  finalCta: {
    title: 'Tu próxima versión comienza aquí.',
    subtitle: 'Reserva tu vacante para Junio 2026.',
    btnLabel: 'Hablar por WhatsApp',
  },
};

// ─── SEDES DISPONIBLES ──────────────────────────────────────
export const sedesConfig = {
  surco: {
    id: 'surco',
    name: 'Surco',
    address: 'Santiago de Surco, Lima',
  },
  lince: {
    id: 'lince',
    name: 'Lince',
    address: 'Lince, Lima',
  },
} as const;

export type SedeId = keyof typeof sedesConfig;

// ─── PROGRAMAS ──────────────────────────────────────────────
export const programsConfig: Record<string, ProgramConfig> = {
  basico: {
    id: 'basico',
    name: 'Salsa Cubana Básico',
    icon: 'music',
    tagline: 'El punto de partida perfecto para tu viaje cubano',
    description:
      'Para quienes no tienen experiencia previa o quieren reforzar fundamentos. Aprenderás a moverte con ritmo, coordinar cuerpo y pasos, y entrar al mundo del Casino.',
    benefits: [
      'Fundamentos de movimiento cubano',
      'Trabajo de cadera y ritmo desde cero',
      'Vocabulario básico de Casino en pareja',
      'Ambiente relajado y de apoyo',
    ],
    sedes: [
      {
        sedeId: 'surco',
        schedule: 'Lunes y Miércoles',
        time: '7:00 pm – 8:30 pm',
        price: 'S/. 180 / mes',
        vacantes: 4, // ← EDITAR para actualizar disponibilidad
      },
      {
        sedeId: 'lince',
        schedule: 'Martes y Jueves',
        time: '7:00 pm – 8:30 pm',
        price: 'S/. 180 / mes',
        vacantes: 3,
      },
    ],
    whatsappMessage: (sede: string) =>
      `Hola 👋 Vi la publicidad de Cuban Groove y me gustaría recibir información sobre el programa Salsa Cubana Básico en la sede ${sede}.`,
  },

  intermedio: {
    id: 'intermedio',
    name: 'Salsa Cubana Intermedio',
    icon: 'zap',
    tagline: 'Lleva tu baile al siguiente nivel',
    description:
      'Para bailarines con mínimo 6 meses de experiencia que quieren profundizar en técnica, conexión musical y vocabulario avanzado de Casino.',
    benefits: [
      'Técnica avanzada de movimiento cubano',
      'Musicalidad y fraseo musical',
      'Conexión y lead/follow en pareja',
      'Vocabulario avanzado de Casino y Rueda',
    ],
    sedes: [
      {
        sedeId: 'surco',
        schedule: 'Lunes y Miércoles',
        time: '8:30 pm – 10:00 pm',
        price: 'S/. 200 / mes',
        vacantes: 5,
      },
      {
        sedeId: 'lince',
        schedule: 'Martes y Jueves',
        time: '8:30 pm – 10:00 pm',
        price: 'S/. 200 / mes',
        vacantes: 2,
      },
    ],
    whatsappMessage: (sede: string) =>
      `Hola 👋 Vi la publicidad de Cuban Groove y me gustaría recibir información sobre el programa Salsa Cubana Intermedio en la sede ${sede}.`,
  },

  ladyStyle: {
    id: 'ladyStyle',
    name: 'Lady Style Cubano',
    icon: 'sparkles',
    tagline: 'Técnica femenina, expresión y flow',
    description:
      'Exclusivo para mujeres con mínimo 6 meses de experiencia. Trabajo profundo de técnica femenina cubana, expresión corporal, flow y presencia escénica.',
    benefits: [
      'Técnica femenina cubana auténtica',
      'Trabajo de expresión y musicalidad',
      'Flow, sensualidad y presencia escénica',
      'Comunidad de mujeres que se apoyan',
    ],
    sedes: [
      {
        sedeId: 'surco',
        schedule: 'Sábados',
        time: '10:00 am – 11:30 am',
        price: 'S/. 180 / mes',
        vacantes: 6,
      },
      {
        sedeId: 'lince',
        schedule: 'Sábados',
        time: '11:30 am – 1:00 pm',
        price: 'S/. 180 / mes',
        vacantes: 4,
      },
    ],
    whatsappMessage: (sede: string) =>
      `Hola 👋 Vi la publicidad de Cuban Groove y me gustaría recibir información sobre el programa Lady Style Cubano en la sede ${sede}.`,
  },

  privadas: {
    id: 'privadas',
    name: 'Clases Privadas',
    icon: 'user',
    tagline: 'Atención 100% personalizada para ti',
    description:
      'Para cualquier nivel. Avanza al doble de velocidad con atención individualizada. Horarios flexibles adaptados a tu disponibilidad.',
    benefits: [
      'Progreso personalizado a tu ritmo',
      'Horarios totalmente flexibles',
      'Corrección técnica inmediata',
      'Metodología adaptada a tus objetivos',
    ],
    sedes: [
      {
        sedeId: 'surco',
        schedule: 'A coordinar',
        time: 'Horario flexible',
        price: 'Consultar precio',
        vacantes: null, // null = "Disponible" sin número
      },
      {
        sedeId: 'lince',
        schedule: 'A coordinar',
        time: 'Horario flexible',
        price: 'Consultar precio',
        vacantes: null,
      },
    ],
    whatsappMessage: (sede: string) =>
      `Hola 👋 Vi la publicidad de Cuban Groove y me gustaría recibir información sobre Clases Privadas en la sede ${sede}.`,
  },
};

// ─── WIZARD ─────────────────────────────────────────────────
export const wizardConfig: WizardConfig = {
  steps: [
    {
      id: 'experience',
      question: '¿Cuál es tu experiencia\nbailando salsa?',
      options: [
        { id: 'never', label: 'Nunca he bailado', result: 'basico' },
        { id: 'less6m', label: 'Menos de 6 meses', result: 'basico' },
        { id: '6m_1y', label: 'Entre 6 meses y 1 año', nextStep: 'style' },
        { id: 'more1y', label: 'Más de 1 año', nextStep: 'style' },
        { id: 'private', label: 'Prefiero clases privadas', result: 'privadas' },
      ],
    },
    {
      id: 'style',
      question: '¿Qué te gustaría\ntrabaj ar?',
      options: [
        { id: 'pareja', label: 'Mi baile en pareja', result: 'intermedio' },
        { id: 'femenino', label: 'Mi estilo femenino', result: 'ladyStyle' },
      ],
    },
  ],
};

// ─── BENEFICIOS ─────────────────────────────────────────────
export const benefitsConfig: BenefitItem[] = [
  {
    icon: 'music',
    title: 'Aprende desde cero',
    description: 'No importa si nunca has bailado. Nuestro método te lleva paso a paso.',
  },
  {
    icon: 'users',
    title: 'Sin necesitar pareja',
    description: 'Vengas solo o acompañado, siempre tendrás con quién practicar.',
  },
  {
    icon: 'award',
    title: 'Profesores especializados',
    description: 'Formación cubana auténtica con instructores de alto nivel.',
  },
  {
    icon: 'globe',
    title: 'Cultura cubana auténtica',
    description: 'Más que pasos: ritmo, sabor, historia y conexión con la música.',
  },
  {
    icon: 'smile',
    title: 'Ambiente amigable',
    description: 'Clases en grupos pequeños donde todos se apoyan y se divierten.',
  },
  {
    icon: 'graduation-cap',
    title: 'Formación técnica y social',
    description: 'Desarrollas técnica, coordinación y habilidades sociales al mismo tiempo.',
  },
];

// ─── TESTIMONIOS ────────────────────────────────────────────
export const testimonialsConfig: TestimonialItem[] = [
  {
    name: 'María García',
    role: 'Alumna desde 2024',
    text: 'Llegué sin saber nada de baile y en 3 meses ya estaba en la pista. Los profesores son increíbles y el ambiente te hace querer volver cada semana.',
    stars: 5,
    // photo: '/testimonials/maria.jpg', // descomentar cuando tengas foto real
  },
  {
    name: 'Carlos Mendoza',
    role: 'Alumno intermedio',
    text: 'La metodología es diferente a otras academias. Se nota la formación cubana de verdad. Mi conexión musical mejoró muchísimo.',
    stars: 5,
  },
  {
    name: 'Lucía Torres',
    role: 'Lady Style Cubano',
    text: 'El Lady Style me cambió la vida. No solo bailas mejor — te ves y te sientes diferente. Recomendadísimo para mujeres.',
    stars: 5,
  },
  {
    name: 'Rodrigo Paz',
    role: 'Clases Privadas',
    text: 'Con las clases privadas avancé el doble de rápido. Tengo horario complicado y me adaptaron todo sin problema.',
    stars: 5,
  },
];

// ─── GALERÍA ────────────────────────────────────────────────
export const galleryConfig: GalleryImage[] = [
  {
    src: 'https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=600',
    alt: 'Clase de salsa cubana en Cuban Groove Perú',
  },
  {
    src: 'https://images.unsplash.com/photo-1518834107812-67b0b7c58434?w=600',
    alt: 'Alumnos practicando Casino en pareja',
  },
  {
    src: 'https://images.unsplash.com/photo-1545959570-a94084071b5d?w=600',
    alt: 'Lady Style Cubano — clase femenina',
  },
  {
    src: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600',
    alt: 'Show de baile cubano',
  },
  {
    src: 'https://images.unsplash.com/photo-1524594152303-9fd13543fe6e?w=600',
    alt: 'Clase grupal de salsa en Lima',
  },
  {
    src: 'https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?w=600',
    alt: 'Instructores Cuban Groove Perú',
  },
];

// ─── FAQ ────────────────────────────────────────────────────
export const faqConfig: FAQItem[] = [
  {
    question: '¿Necesito venir con pareja?',
    answer:
      'No. La gran mayoría de nuestros alumnos vienen solos. En clase rotamos constantemente para que todos practiquen con diferentes personas. Solo necesitas ganas de aprender.',
  },
  {
    question: '¿Puedo empezar desde cero?',
    answer:
      'Absolutamente. El programa Básico está diseñado exactamente para ti. No asumimos ningún conocimiento previo. Empezamos desde el primer paso y avanzamos a tu ritmo.',
  },
  {
    question: '¿Qué ropa debo usar?',
    answer:
      'Ropa cómoda con la que puedas moverte libremente. Para el calzado, preferiblemente zapatos con suela lisa (no de goma) para poder girar bien. No necesitas comprar nada especial al inicio.',
  },
  {
    question: '¿Cómo se realiza el pago?',
    answer:
      'Aceptamos pago mensual por transferencia bancaria, Yape o Plin. El pago se coordina directamente por WhatsApp antes de tu primera clase. No hay matrícula adicional.',
  },
  {
    question: '¿Qué pasa si falto a una clase?',
    answer:
      'Entendemos que la vida pasa. Si avisas con anticipación, coordinamos la forma de recuperar o ponerte al día. Nuestro objetivo es que sigas avanzando sin importar los contratiempos.',
  },
];
```

---

## 4. Types — /types/index.ts

```typescript
// /types/index.ts

export interface SiteConfig {
  name: string;
  whatsappNumber: string;
  stats: { count: string; label: string };
  hero: {
    title: string;
    subtitle: string;
    ctaLabel: string;
    heroImageUrl: string;
  };
  social: { instagram: string; tiktok: string; youtube: string };
  finalCta: { title: string; subtitle: string; btnLabel: string };
}

export interface SedeSchedule {
  sedeId: string;
  schedule: string;
  time: string;
  price: string;
  vacantes: number | null;
}

export interface ProgramConfig {
  id: string;
  name: string;
  icon: string;
  tagline: string;
  description: string;
  benefits: string[];
  sedes: SedeSchedule[];
  whatsappMessage: (sede: string) => string;
}

export interface WizardOption {
  id: string;
  label: string;
  result?: string;       // programa final (si no hay nextStep)
  nextStep?: string;     // id del siguiente step
}

export interface WizardStep {
  id: string;
  question: string;
  options: WizardOption[];
}

export interface WizardConfig {
  steps: WizardStep[];
}

export interface BenefitItem {
  icon: string;
  title: string;
  description: string;
}

export interface TestimonialItem {
  name: string;
  role: string;
  text: string;
  stars: number;
  photo?: string;
}

export interface GalleryImage {
  src: string;
  alt: string;
}

export interface FAQItem {
  question: string;
  answer: string;
}
```

---

## 5. Código de Componentes

### layout.tsx

```tsx
// /app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Cuban Groove Perú – Encuentra tu programa de baile ideal',
  description:
    'Clases de Salsa Cubana, Casino, Lady Style y Clases Privadas en Lima. Sedes en Surco y Lince. Junio 2026.',
  openGraph: {
    title: 'Cuban Groove Perú – Encuentra tu programa de baile ideal',
    description: 'Descubre el programa perfecto para tu nivel. Sedes en Surco y Lince.',
    locale: 'es_PE',
    type: 'website',
  },
  robots: { index: false, follow: false }, // landing de ads: no indexar
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es-PE" className={inter.variable}>
      <head>
        {/* Google Tag Manager — reemplazar GTM-XXXXXXX */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');`,
          }}
        />
        {/* Meta Pixel — reemplazar XXXXXXXXXXXXXXXXXX */}
        <script
          dangerouslySetInnerHTML={{
            __html: `!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'XXXXXXXXXXXXXXXXXX');
fbq('track', 'PageView');`,
          }}
        />
      </head>
      <body className="bg-zinc-950 font-sans antialiased">
        {/* GTM noscript */}
        <noscript>
          <iframe
            src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        {children}
      </body>
    </html>
  );
}
```

### globals.css

```css
/* /app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
  }

  body {
    @apply bg-zinc-950 text-white;
  }
}

@layer utilities {
  .snap-x-mandatory {
    scroll-snap-type: x mandatory;
  }
  .snap-start {
    scroll-snap-align: start;
  }
}

/* Animación fade-in suave para el wizard */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.35s ease-out forwards;
}
```

### page.tsx

```tsx
// /app/page.tsx
'use client';

import { useState } from 'react';
import Hero from '@/components/landing/Hero';
import Wizard from '@/components/landing/Wizard';
import ProgramResult from '@/components/landing/ProgramResult';
import Benefits from '@/components/landing/Benefits';
import Testimonials from '@/components/landing/Testimonials';
import Gallery from '@/components/landing/Gallery';
import FAQ from '@/components/landing/FAQ';
import FinalCTA from '@/components/landing/FinalCTA';

import {
  siteConfig,
  programsConfig,
  benefitsConfig,
  testimonialsConfig,
  galleryConfig,
  faqConfig,
  wizardConfig,
} from '@/data/config';

export default function LandingPage() {
  const [selectedProgramId, setSelectedProgramId] = useState<string | null>(null);

  const selectedProgram = selectedProgramId ? programsConfig[selectedProgramId] : null;

  const handleWizardComplete = (programId: string) => {
    setSelectedProgramId(programId);
    // Scroll suave a la sección de resultado
    setTimeout(() => {
      document.getElementById('resultado')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleReset = () => {
    setSelectedProgramId(null);
    document.getElementById('wizard')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleHeroCTA = () => {
    document.getElementById('wizard')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <main>
      {/* S1 — Hero */}
      <Hero
        title={siteConfig.hero.title}
        subtitle={siteConfig.hero.subtitle}
        ctaLabel={siteConfig.hero.ctaLabel}
        heroImageUrl={siteConfig.hero.heroImageUrl}
        stats={siteConfig.stats}
        onCTA={handleHeroCTA}
      />

      {/* S2 — Wizard */}
      <section id="wizard" aria-label="Encuentra tu programa">
        <Wizard config={wizardConfig} onComplete={handleWizardComplete} />
      </section>

      {/* S3 — Resultado (visible solo cuando hay selección) */}
      {selectedProgram && (
        <section id="resultado" aria-label="Programa recomendado">
          <ProgramResult program={selectedProgram} onReset={handleReset} />
        </section>
      )}

      {/* S4 — Beneficios */}
      <Benefits items={benefitsConfig} />

      {/* S5 — Testimonios */}
      <Testimonials items={testimonialsConfig} />

      {/* S6 — Galería */}
      <Gallery images={galleryConfig} />

      {/* S7 — FAQ */}
      <FAQ items={faqConfig} />

      {/* S8 — CTA Final */}
      <FinalCTA
        title={siteConfig.finalCta.title}
        subtitle={siteConfig.finalCta.subtitle}
        btnLabel={siteConfig.finalCta.btnLabel}
        whatsappNumber={siteConfig.whatsappNumber}
        social={siteConfig.social}
      />
    </main>
  );
}
```

### Hero.tsx

```tsx
// /components/landing/Hero.tsx
'use client';

import Image from 'next/image';

interface HeroProps {
  title: string;
  subtitle: string;
  ctaLabel: string;
  heroImageUrl: string;
  stats: { count: string; label: string };
  onCTA: () => void;
}

export default function Hero({
  title,
  subtitle,
  ctaLabel,
  heroImageUrl,
  stats,
  onCTA,
}: HeroProps) {
  return (
    <section
      className="relative min-h-screen flex flex-col"
      aria-label="Sección principal"
    >
      {/* Imagen de fondo */}
      <div className="absolute inset-0 z-0">
        <Image
          src={heroImageUrl}
          alt="Clases de salsa cubana en Cuban Groove Perú"
          fill
          className="object-cover object-center"
          priority
          sizes="100vw"
        />
        {/* Overlay oscuro con gradiente hacia abajo */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/80" />
      </div>

      {/* Logo */}
      <div className="relative z-10 flex justify-center lg:justify-start pt-8 px-6 lg:px-16">
        <div className="text-white font-bold text-xl tracking-wide">
          {/* Reemplazar con <Image> cuando tengas el logo real */}
          <span className="text-amber-400">CUBAN</span> GROOVE
        </div>
      </div>

      {/* Contenido principal — alineado al fondo */}
      <div className="relative z-10 flex-1 flex flex-col justify-end">
        <div className="px-6 pb-12 lg:px-16 lg:pb-20 lg:max-w-2xl">

          {/* Social proof */}
          <div className="flex items-center gap-2 mb-5">
            <div className="flex text-amber-400">
              {[...Array(5)].map((_, i) => (
                <svg key={i} className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
            </div>
            <span className="text-gray-300 text-sm">
              Más de <strong className="text-white">{stats.count}</strong> {stats.label}
            </span>
          </div>

          {/* Título */}
          <h1 className="text-4xl lg:text-6xl font-bold text-white leading-tight mb-4">
            {title}
          </h1>

          {/* Subtítulo */}
          <p className="text-gray-300 text-base lg:text-lg mb-8 max-w-lg">
            {subtitle}
          </p>

          {/* CTA */}
          <button
            onClick={onCTA}
            className="w-full lg:w-auto bg-amber-500 hover:bg-amber-400 text-black font-bold text-lg py-4 px-10 rounded-2xl transition-all duration-200 hover:scale-105 active:scale-95 focus:outline-none focus:ring-4 focus:ring-amber-400/50"
            aria-label={ctaLabel}
          >
            {ctaLabel} →
          </button>
        </div>
      </div>
    </section>
  );
}
```

### Wizard.tsx

```tsx
// /components/landing/Wizard.tsx
'use client';

import { useState } from 'react';
import type { WizardConfig } from '@/types';
import WizardStep from './WizardStep';
import ProgressBar from './ProgressBar';

interface WizardProps {
  config: WizardConfig;
  onComplete: (programId: string) => void;
}

interface WizardState {
  currentStepId: string;
  history: string[]; // ids de steps visitados, para "volver"
}

export default function Wizard({ config, onComplete }: WizardProps) {
  const firstStepId = config.steps[0].id;

  const [state, setState] = useState<WizardState>({
    currentStepId: firstStepId,
    history: [],
  });

  const currentStep = config.steps.find((s) => s.id === state.currentStepId);

  if (!currentStep) return null;

  // Índice del paso actual para la barra de progreso
  const stepIndex = config.steps.findIndex((s) => s.id === state.currentStepId);
  const totalSteps = config.steps.length;

  const handleSelect = (optionId: string) => {
    const option = currentStep.options.find((o) => o.id === optionId);
    if (!option) return;

    if (option.result) {
      // Fin del wizard — tenemos resultado
      onComplete(option.result);
    } else if (option.nextStep) {
      // Navegar al siguiente paso
      setState((prev) => ({
        currentStepId: option.nextStep!,
        history: [...prev.history, prev.currentStepId],
      }));
    }
  };

  const handleBack = () => {
    if (state.history.length === 0) return;
    const previousStepId = state.history[state.history.length - 1];
    setState((prev) => ({
      currentStepId: previousStepId,
      history: prev.history.slice(0, -1),
    }));
  };

  return (
    <div className="bg-zinc-900 py-20 px-6">
      <div className="max-w-2xl mx-auto">

        {/* Barra de progreso */}
        <ProgressBar current={stepIndex + 1} total={totalSteps} />

        {/* Pregunta y opciones — key fuerza re-render + animación */}
        <div key={state.currentStepId} className="animate-fade-in-up">
          <WizardStep
            question={currentStep.question}
            options={currentStep.options}
            onSelect={handleSelect}
          />
        </div>

        {/* Botón volver */}
        {state.history.length > 0 && (
          <button
            onClick={handleBack}
            className="mt-8 text-gray-400 hover:text-white text-sm underline underline-offset-4 transition-colors"
          >
            ← Volver
          </button>
        )}
      </div>
    </div>
  );
}
```

### WizardStep.tsx

```tsx
// /components/landing/WizardStep.tsx
'use client';

import type { WizardOption } from '@/types';

interface WizardStepProps {
  question: string;
  options: WizardOption[];
  onSelect: (optionId: string) => void;
}

export default function WizardStep({ question, options, onSelect }: WizardStepProps) {
  return (
    <div>
      {/* Pregunta */}
      <h2 className="text-white text-2xl lg:text-3xl font-bold mb-8 whitespace-pre-line">
        {question}
      </h2>

      {/* Opciones como cards clicables */}
      <div className="flex flex-col gap-3" role="list">
        {options.map((option) => (
          <button
            key={option.id}
            onClick={() => onSelect(option.id)}
            className="
              group w-full text-left
              bg-zinc-800 border border-zinc-700
              hover:border-amber-500 hover:bg-zinc-700
              active:scale-[0.99]
              p-5 rounded-2xl
              transition-all duration-200
              focus:outline-none focus:ring-2 focus:ring-amber-500/50
            "
            role="listitem"
            aria-label={option.label}
          >
            <div className="flex items-center justify-between">
              <span className="text-white font-medium text-base group-hover:text-amber-400 transition-colors">
                {option.label}
              </span>
              <svg
                className="w-5 h-5 text-zinc-500 group-hover:text-amber-500 transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

### ProgressBar.tsx

```tsx
// /components/landing/ProgressBar.tsx

interface ProgressBarProps {
  current: number;
  total: number;
}

export default function ProgressBar({ current, total }: ProgressBarProps) {
  const percentage = Math.round((current / total) * 100);

  return (
    <div className="mb-10">
      <div className="flex justify-between items-center mb-2">
        <span className="text-gray-500 text-xs uppercase tracking-widest">
          Paso {current} de {total}
        </span>
        <span className="text-amber-400 text-xs font-medium">{percentage}%</span>
      </div>
      <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-amber-500 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={current}
          aria-valuemin={1}
          aria-valuemax={total}
        />
      </div>
    </div>
  );
}
```

### ProgramResult.tsx

```tsx
// /components/landing/ProgramResult.tsx
'use client';

import { useState } from 'react';
import type { ProgramConfig } from '@/types';
import { sedesConfig } from '@/data/config';
import { buildWhatsAppUrl } from '@/lib/whatsapp';

interface ProgramResultProps {
  program: ProgramConfig;
  onReset: () => void;
}

export default function ProgramResult({ program, onReset }: ProgramResultProps) {
  const [selectedSedeId, setSelectedSedeId] = useState<string | null>(null);

  const handleWhatsApp = (sedeId: string) => {
    const sede = sedesConfig[sedeId as keyof typeof sedesConfig];
    if (!sede) return;

    const message = program.whatsappMessage(sede.name);
    const url = buildWhatsAppUrl('51991337159', message);

    // Evento para Meta Pixel y GTM
    if (typeof window !== 'undefined') {
      (window as any).fbq?.('track', 'Contact', {
        content_name: program.name,
        content_category: sede.name,
      });
      (window as any).dataLayer?.push({
        event: 'whatsapp_click',
        program: program.id,
        sede: sedeId,
      });
    }

    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <section className="bg-zinc-950 py-20 px-6">
      <div className="max-w-2xl mx-auto">

        {/* Eyebrow */}
        <p className="text-amber-400 text-sm uppercase tracking-widest mb-4 animate-fade-in-up">
          Tu programa recomendado
        </p>

        {/* Tarjeta principal */}
        <div className="bg-zinc-900 border border-amber-500/30 rounded-3xl p-8 animate-fade-in-up">

          {/* Encabezado programa */}
          <div className="mb-6">
            <h2 className="text-white text-2xl lg:text-3xl font-bold mb-2">
              {program.name}
            </h2>
            <p className="text-amber-400 text-sm font-medium">{program.tagline}</p>
          </div>

          {/* Descripción */}
          <p className="text-gray-400 text-sm leading-relaxed mb-6">
            {program.description}
          </p>

          {/* Beneficios del programa */}
          <ul className="space-y-2 mb-8">
            {program.benefits.map((benefit, i) => (
              <li key={i} className="flex items-start gap-3 text-gray-300 text-sm">
                <svg
                  className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                {benefit}
              </li>
            ))}
          </ul>

          {/* Separador */}
          <div className="border-t border-zinc-800 mb-8" />

          {/* Sedes */}
          <p className="text-gray-500 text-xs uppercase tracking-widest mb-4">
            Sedes disponibles — Junio 2026
          </p>

          <div className="space-y-4">
            {program.sedes.map((sedeInfo) => {
              const sede = sedesConfig[sedeInfo.sedeId as keyof typeof sedesConfig];
              if (!sede) return null;
              const isSelected = selectedSedeId === sedeInfo.sedeId;

              return (
                <div
                  key={sedeInfo.sedeId}
                  className={`
                    rounded-2xl border p-5 transition-all duration-200
                    ${isSelected
                      ? 'border-amber-500 bg-amber-500/10'
                      : 'border-zinc-700 bg-zinc-800/50'
                    }
                  `}
                >
                  {/* Nombre sede */}
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-white font-semibold text-base">
                      📍 {sede.name}
                    </h3>
                    {sedeInfo.vacantes !== null && (
                      <span className={`
                        text-xs font-medium px-2 py-1 rounded-full
                        ${sedeInfo.vacantes <= 2
                          ? 'bg-red-500/20 text-red-400'
                          : 'bg-emerald-500/20 text-emerald-400'
                        }
                      `}>
                        {sedeInfo.vacantes <= 2
                          ? `¡Solo ${sedeInfo.vacantes} vacantes!`
                          : `${sedeInfo.vacantes} vacantes`
                        }
                      </span>
                    )}
                    {sedeInfo.vacantes === null && (
                      <span className="text-xs font-medium px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400">
                        Disponible
                      </span>
                    )}
                  </div>

                  {/* Detalles */}
                  <div className="grid grid-cols-2 gap-2 mb-4 text-sm text-gray-400">
                    <div>🗓 {sedeInfo.schedule}</div>
                    <div>🕐 {sedeInfo.time}</div>
                    <div className="col-span-2 text-white font-medium">{sedeInfo.price}</div>
                  </div>

                  {/* Botón WhatsApp por sede */}
                  <button
                    onClick={() => handleWhatsApp(sedeInfo.sedeId)}
                    className="
                      w-full flex items-center justify-center gap-2
                      bg-green-600 hover:bg-green-500
                      text-white font-bold text-sm
                      py-3 rounded-xl
                      transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]
                      focus:outline-none focus:ring-2 focus:ring-green-400/50
                    "
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                    </svg>
                    Reservar en {sede.name}
                  </button>
                </div>
              );
            })}
          </div>

          {/* Microcopy de confianza */}
          <p className="text-center text-gray-500 text-xs mt-6">
            🔒 Sin compromisos. Solo una conversación directa con nuestro equipo.
          </p>
        </div>

        {/* Volver a empezar */}
        <div className="text-center mt-6">
          <button
            onClick={onReset}
            className="text-gray-500 hover:text-white text-sm underline underline-offset-4 transition-colors"
          >
            Volver a empezar
          </button>
        </div>
      </div>
    </section>
  );
}
```

### Benefits.tsx

```tsx
// /components/landing/Benefits.tsx
import type { BenefitItem } from '@/types';

const ICON_MAP: Record<string, string> = {
  music: 'M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3',
  users: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75M9 7a4 4 0 110 8 4 4 0 010-8z',
  award: 'M12 15l-4-4m0 0l4-4m-4 4h12m-7 7a9 9 0 110-18 9 9 0 010 18z',
  globe: 'M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z',
  smile: 'M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z',
  'graduation-cap': 'M22 10v6M2 10l10-5 10 5-10 5-10-5zM6 12v5c3 3 9 3 12 0v-5',
};

interface BenefitsProps {
  items: BenefitItem[];
}

export default function Benefits({ items }: BenefitsProps) {
  return (
    <section className="bg-zinc-900 py-20 px-6" aria-label="Beneficios">
      <div className="max-w-4xl mx-auto">

        <h2 className="text-white text-2xl lg:text-3xl font-bold text-center mb-3">
          Por qué elegir Cuban Groove
        </h2>
        <p className="text-gray-400 text-center text-sm mb-12 max-w-md mx-auto">
          Más de 500 alumnos encontraron su camino aquí. Esto es lo que nos hace diferentes.
        </p>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item, i) => (
            <div
              key={i}
              className="bg-zinc-800 rounded-2xl p-6 flex flex-col items-center text-center hover:bg-zinc-700 transition-colors duration-200"
            >
              <div className="w-12 h-12 bg-amber-500/20 rounded-xl flex items-center justify-center mb-4">
                <svg
                  className="w-6 h-6 text-amber-400"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.5}
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d={ICON_MAP[item.icon] || ICON_MAP.music} />
                </svg>
              </div>
              <h3 className="text-white font-semibold text-sm mb-2">{item.title}</h3>
              <p className="text-gray-400 text-xs leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Testimonials.tsx

```tsx
// /components/landing/Testimonials.tsx
'use client';

import { useRef } from 'react';
import type { TestimonialItem } from '@/types';
import Image from 'next/image';

interface TestimonialsProps {
  items: TestimonialItem[];
}

export default function Testimonials({ items }: TestimonialsProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  return (
    <section className="bg-zinc-950 py-20 overflow-hidden" aria-label="Testimonios">
      <div className="max-w-4xl mx-auto">

        <h2 className="text-white text-2xl lg:text-3xl font-bold text-center px-6 mb-3">
          Lo que dicen nuestros alumnos
        </h2>
        <p className="text-gray-400 text-center text-sm px-6 mb-10">
          Personas reales. Resultados reales.
        </p>

        {/* Slider horizontal con CSS scroll snap */}
        <div
          ref={scrollRef}
          className="flex gap-4 overflow-x-auto pb-6 px-6 snap-x-mandatory scroll-smooth"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {items.map((item, i) => (
            <article
              key={i}
              className="
                snap-start flex-shrink-0
                w-[85vw] lg:w-80
                bg-zinc-900 border border-zinc-800
                rounded-2xl p-6
              "
            >
              {/* Stars */}
              <div className="flex gap-1 text-amber-400 mb-4">
                {[...Array(item.stars)].map((_, j) => (
                  <svg key={j} className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>

              {/* Texto */}
              <blockquote className="text-gray-300 text-sm leading-relaxed mb-6 italic">
                "{item.text}"
              </blockquote>

              {/* Autor */}
              <div className="flex items-center gap-3">
                {item.photo ? (
                  <div className="relative w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
                    <Image src={item.photo} alt={item.name} fill className="object-cover" />
                  </div>
                ) : (
                  <div className="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0">
                    <span className="text-amber-400 font-bold text-sm">
                      {item.name.charAt(0)}
                    </span>
                  </div>
                )}
                <div>
                  <p className="text-white font-semibold text-sm">{item.name}</p>
                  <p className="text-gray-500 text-xs">{item.role}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Gallery.tsx

```tsx
// /components/landing/Gallery.tsx
import Image from 'next/image';
import type { GalleryImage } from '@/types';

interface GalleryProps {
  images: GalleryImage[];
}

export default function Gallery({ images }: GalleryProps) {
  return (
    <section className="bg-zinc-900 py-20 px-4 lg:px-8" aria-label="Galería de clases">
      <div className="max-w-4xl mx-auto">

        <h2 className="text-white text-2xl lg:text-3xl font-bold text-center px-2 mb-3">
          Nuestras clases
        </h2>
        <p className="text-gray-400 text-center text-sm mb-10">
          Así se vive Cuban Groove Perú.
        </p>

        {/* Masonry con CSS columns */}
        <div className="columns-2 lg:columns-3 gap-3 space-y-3">
          {images.map((img, i) => (
            <div
              key={i}
              className="break-inside-avoid rounded-2xl overflow-hidden"
            >
              <Image
                src={img.src}
                alt={img.alt}
                width={600}
                height={400}
                className="w-full h-auto object-cover hover:scale-105 transition-transform duration-500"
                loading="lazy"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### FAQ.tsx

```tsx
// /components/landing/FAQ.tsx
'use client';

import { useState } from 'react';
import type { FAQItem } from '@/types';

interface FAQProps {
  items: FAQItem[];
}

export default function FAQ({ items }: FAQProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggle = (i: number) => {
    setOpenIndex(openIndex === i ? null : i);
  };

  return (
    <section className="bg-zinc-950 py-20 px-6" aria-label="Preguntas frecuentes">
      <div className="max-w-2xl mx-auto">

        <h2 className="text-white text-2xl lg:text-3xl font-bold text-center mb-10">
          Preguntas frecuentes
        </h2>

        <div className="divide-y divide-zinc-800">
          {items.map((item, i) => (
            <div key={i}>
              <button
                onClick={() => toggle(i)}
                className="
                  w-full flex items-center justify-between
                  py-5 text-left
                  focus:outline-none group
                "
                aria-expanded={openIndex === i}
              >
                <span className={`
                  font-medium text-sm lg:text-base pr-4 transition-colors
                  ${openIndex === i ? 'text-amber-400' : 'text-white group-hover:text-amber-400'}
                `}>
                  {item.question}
                </span>
                <svg
                  className={`
                    w-5 h-5 flex-shrink-0 text-gray-500
                    transition-transform duration-200
                    ${openIndex === i ? 'rotate-45 text-amber-400' : ''}
                  `}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </button>

              {/* Respuesta con animación */}
              <div
                className={`
                  overflow-hidden transition-all duration-300 ease-in-out
                  ${openIndex === i ? 'max-h-64 opacity-100' : 'max-h-0 opacity-0'}
                `}
              >
                <p className="text-gray-400 text-sm leading-relaxed pb-5">
                  {item.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### FinalCTA.tsx

```tsx
// /components/landing/FinalCTA.tsx
import { buildWhatsAppUrl } from '@/lib/whatsapp';

interface FinalCTAProps {
  title: string;
  subtitle: string;
  btnLabel: string;
  whatsappNumber: string;
  social: { instagram: string; tiktok: string; youtube: string };
}

export default function FinalCTA({
  title,
  subtitle,
  btnLabel,
  whatsappNumber,
  social,
}: FinalCTAProps) {
  const defaultMessage =
    'Hola 👋 Vi la publicidad de Cuban Groove y me gustaría recibir información sobre los programas disponibles.';

  const whatsappUrl = buildWhatsAppUrl(whatsappNumber, defaultMessage);

  return (
    <footer className="bg-amber-500 py-24 px-6 text-center" aria-label="Llamada a la acción final">
      <div className="max-w-2xl mx-auto">

        <h2 className="text-black text-3xl lg:text-4xl font-bold leading-tight mb-4">
          {title}
        </h2>

        <p className="text-black/70 text-base lg:text-lg mb-10">
          {subtitle}
        </p>

        <a
          href={whatsappUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="
            inline-flex items-center justify-center gap-3
            bg-black text-white
            font-bold text-lg
            py-4 px-10 rounded-2xl
            w-full lg:w-auto
            hover:bg-zinc-900
            transition-all duration-200 hover:scale-105 active:scale-95
            focus:outline-none focus:ring-4 focus:ring-black/30
          "
          onClick={() => {
            if (typeof window !== 'undefined') {
              (window as any).fbq?.('track', 'Contact');
              (window as any).dataLayer?.push({ event: 'final_cta_whatsapp' });
            }
          }}
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          {btnLabel}
        </a>

        {/* Redes sociales */}
        <div className="flex justify-center gap-6 mt-10">
          <a href={social.instagram} target="_blank" rel="noopener noreferrer"
            className="text-black/50 hover:text-black transition-colors text-sm font-medium">
            Instagram
          </a>
          <a href={social.tiktok} target="_blank" rel="noopener noreferrer"
            className="text-black/50 hover:text-black transition-colors text-sm font-medium">
            TikTok
          </a>
          <a href={social.youtube} target="_blank" rel="noopener noreferrer"
            className="text-black/50 hover:text-black transition-colors text-sm font-medium">
            YouTube
          </a>
        </div>
      </div>
    </footer>
  );
}
```

### /lib/whatsapp.ts

```typescript
// /lib/whatsapp.ts

/**
 * Construye la URL de WhatsApp con mensaje pre-llenado.
 * El número debe estar en formato internacional sin + ni espacios.
 * Ejemplo: '51991337159'
 */
export function buildWhatsAppUrl(phone: string, message: string): string {
  const encoded = encodeURIComponent(message);
  return `https://wa.me/${phone}?text=${encoded}`;
}
```

### tailwind.config.ts

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          gold: '#f59e0b',
          'gold-dark': '#d97706',
        },
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.35s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          from: { opacity: '0', transform: 'translateY(16px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### Comandos para crear el proyecto

```bash
# 1. Crear el proyecto Next.js
npx create-next-app@latest cubangroove-landing --typescript --tailwind --app --src-dir --import-alias "@/*"

# 2. Entrar al directorio
cd cubangroove-landing

# 3. Instalar dependencias adicionales (mínimas — el proyecto no necesita más)
# next/image está incluido en Next.js — no necesita instalación extra

# 4. Crear estructura de carpetas
mkdir -p src/components/landing
mkdir -p src/data
mkdir -p src/lib
mkdir -p src/types

# 5. Copiar archivos en este orden:
#    src/types/index.ts
#    src/data/config.ts
#    src/lib/whatsapp.ts
#    src/components/landing/*.tsx
#    src/app/globals.css
#    src/app/layout.tsx
#    src/app/page.tsx
#    tailwind.config.ts

# 6. Correr en desarrollo
npm run dev
```

---

## 6. Recomendaciones CRO

### Las 8 decisiones de diseño más importantes para Meta Ads → WhatsApp

**1. Wizard en lugar de formulario tradicional (impacto estimado: +35–50% conversión)**
El wizard elimina el "miedo al formulario". El usuario toma micro-decisiones simples (un clic por paso) en lugar de enfrentarse a un formulario con múltiples campos. Cada clic es un micro-compromiso que aumenta la probabilidad de completar el flujo. Patrón probado por Typeform, Airbnb Onboarding, y quizzes de BuzzFeed.

**2. WhatsApp como única CTA, sin formularios de captura**
Tráfico de Meta Ads tiene alta intención pero baja paciencia. El usuario viene de consumir video entretenido — el salto cognitivo a "llenar un formulario con mis datos" es enorme. WhatsApp es familiar, inmediato, y percibido como conversacional. Elimina la fricción del formulario y conecta al lead directamente con el equipo de ventas.

**3. Mensaje pre-llenado dinámico con programa y sede específica**
Un mensaje genérico ("Quiero información") genera respuestas lentas del equipo porque hay que cualificar al lead. El mensaje pre-llenado con `[PROGRAMA] en la sede [SEDE]` llega pre-cualificado, permite una respuesta inmediata y personalizada, y el lead siente que el proceso ya empezó.

**4. Urgencia real en vacantes (número específico, no "pocos cupos")**
"Vacantes disponibles: 4" convierte más que "Cupos limitados". La especificidad hace que la escasez sea creíble. Cuando el número llega a 2 o menos, el badge cambia a rojo ("¡Solo 2 vacantes!") — activando FOMO legítimo. Editar estos números cada semana en `config.ts` toma 2 minutos y puede subir conversiones 10–20%.

**5. Dark mode + paleta dorada = percepción premium que justifica el precio**
El usuario viene de Instagram/Reels donde el contenido de calidad es visual. Un fondo blanco con texto negro grita "web genérica". El fondo oscuro (#0a0a0a + zinc-900/950) con acentos ámbar/dorado comunica exclusividad, calidad, y coherencia con el mundo de la música y el baile. Esta percepción permite cobrar más y reduce el "¿por qué tan caro?".

**6. Hero en viewport completo con CTA único y visible sin scroll**
El 60–80% del tráfico móvil de Meta Ads rebota si no ve una acción clara en los primeros 3 segundos. Un solo botón ("Empezar ahora"), una foto de fondo emocional, y el social proof ("500+ alumnos") crean el contexto mínimo necesario para el clic. Sin menú, sin links secundarios, sin distracciones.

**7. Resultado personalizado como "prescripción de experto"**
Cuando el wizard termina, el usuario no ve "una opción más del catálogo" — ve "tu programa recomendado". El lenguaje prescriptivo ("Para quienes empiezan desde cero...") hace que el usuario sienta que el sistema lo entendió. Esto activa el principio de reciprocidad: alguien me ayudó a encontrar lo que necesito, yo en retribución tomo acción.

**8. robots noindex + Meta Pixel + GTM: tracking sin contaminar SEO**
Esta landing recibe tráfico de pago, no orgánico. Indexarla contamina el SEO del sitio principal. El `robots: noindex` es obligatorio. El Meta Pixel con evento `Contact` al hacer clic en WhatsApp permite crear audiencias similares y medir el costo por lead real desde Meta Ads Manager.

**Bonus — Métricas clave a medir desde el día 1:**
- CTR Hero → Wizard (objetivo: >70% de visitantes pasan al wizard)
- Completion rate del wizard (objetivo: >80% completan los pasos)
- Click WhatsApp desde resultado (objetivo: >40% hacen clic)
- Tiempo hasta primer mensaje en WhatsApp (objetivo: <5 min)
