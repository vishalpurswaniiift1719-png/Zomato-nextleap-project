---
name: Nocturne Dining
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#ffb59c'
  on-secondary: '#5c1a00'
  secondary-container: '#8e2c01'
  on-secondary-container: '#ffaa8d'
  tertiary: '#ffb5a0'
  on-tertiary: '#601400'
  tertiary-container: '#ff5625'
  on-tertiary-container: '#541100'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdbcf'
  secondary-fixed-dim: '#ffb59c'
  on-secondary-fixed: '#380c00'
  on-secondary-fixed-variant: '#822800'
  tertiary-fixed: '#ffdbd1'
  tertiary-fixed-dim: '#ffb5a0'
  on-tertiary-fixed: '#3b0900'
  on-tertiary-fixed-variant: '#872000'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 24px
  gutter: 16px
  sidebar-width: 280px
---

## Brand & Style

The design system establishes a high-end, nocturnal atmosphere for culinary exploration. It targets a sophisticated audience seeking curated dining experiences through an AI lens. 

The aesthetic is **Premium Modern with Glassmorphism**. It utilizes deep obsidian surfaces to create a sense of exclusivity, while "glowing" interactive elements provide a sense of AI-driven energy. The UI relies on depth, translucency, and vibrant light-leaks to evoke the feeling of a modern city at night—sophisticated, energetic, and technologically advanced.

## Colors

The palette is rooted in an ultra-dark **Obsidian (#0D0D0D)** base to provide maximum contrast for the vibrant accents. 

- **Primary (Zomato Red):** Used for critical actions, branding, and core AI indicators.
- **Secondary (Warm Coral):** Provides a softer alternative for secondary tags and supplementary information.
- **Tertiary (Neon Orange):** Reserved for high-energy highlights and gradient stop points.
- **Neutral:** A range of deep charcoals and greys used to define structure without breaking the dark-mode immersion.

Glass surfaces use a semi-transparent white stroke to define edges against the dark background, ensuring clarity despite the low-contrast environment.

## Typography

This design system uses a dual-font strategy to balance character with utility. 

**Outfit** is used for headings and display text. Its geometric construction feels modern and high-end, fitting the "premium" brand promise. 
**Inter** is used for all body text, inputs, and labels. Its high legibility and systematic feel complement the AI-driven nature of the product, ensuring that complex restaurant data remains easy to digest.

Text colors should primarily stay in the White and Off-white range to maintain high contrast against the obsidian background. Use opacity (e.g., 60% white) rather than grey hex codes for secondary text to maintain the "glass" look.

## Layout & Spacing

The layout follows a **fluid grid** model with generous safe areas to maintain a premium, "breathable" feel. 

- **Desktop:** 12-column grid with a fixed sidebar for navigation. Content is centered in a container with a max-width of 1440px.
- **Mobile:** 4-column grid with 16px margins. Bottom navigation or a sleek hamburger menu is used to maximize vertical screen real estate for imagery.

Vertical spacing should follow an 8px rhythm. Use larger gaps (48px+) between major sections to emphasize the minimalist, editorial style of the restaurant listings.

## Elevation & Depth

Hierarchy is established through **Glassmorphism** rather than traditional drop shadows.

- **Level 0 (Base):** #0D0D0D.
- **Level 1 (Surface):** #1A1A1A with a subtle 1px border (`rgba(255,255,255,0.05)`).
- **Level 2 (Glass Cards):** Background `rgba(26, 26, 26, 0.6)` with a `backdrop-filter: blur(12px)`.
- **Level 3 (Popovers/Modals):** Background `rgba(30, 30, 30, 0.8)` with a `backdrop-filter: blur(20px)` and a soft outer glow in the primary color (low opacity).

Interaction is indicated by "inner glows" or increased border brightness rather than moving the element "higher" on the Z-axis.

## Shapes

The design system uses a **Rounded** shape language to feel approachable yet sleek. 

Standard components (Cards, Inputs) use a 0.5rem (8px) radius. Larger containers like Modals or Hero cards should use 1rem (16px) or 1.5rem (24px) to create a soft, high-end feel. Interactive elements like "AI Recommend" buttons or filter chips should use pill-shaped (full-round) corners to distinguish them from structural content.

## Components

### Buttons
- **Primary:** Gradient background (Vibrant Red to Coral) with a `box-shadow: 0 0 15px rgba(226, 55, 68, 0.4)`. Text is bold white.
- **Secondary:** Glass background with a 1px white stroke at 20% opacity.
- **AI Action:** Features a subtle animated pulse effect or a shifting gradient border to signify "processing."

### Glass Cards
Cards are the primary container for restaurant listings. They feature a background blur of 10-15px, a thin top-down highlight border, and high-quality imagery that bleeds to the top edges.

### Vibrant Badges
Used for ratings, price levels, or cuisine types. These use semi-transparent versions of the accent colors (e.g., `rgba(226, 55, 68, 0.2)`) with a high-saturation text color to pop against the dark backgrounds.

### Inputs
Sleek, dark fields with #1A1A1A backgrounds. On focus, the border transitions to a primary red glow. Icons should be used within the fields (e.g., search or location pin) to minimize visual clutter.

### Sidebar Navigation
A fixed-position element with a semi-transparent background. Active states are indicated by a vertical "glow bar" on the left and a subtle shift in text weight.