export const metadata = {
  title: 'Nocturne Dining - AI Recommender',
  description: 'AI Dining Concierge',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        {/* Tailwind CDN for perfect Stitch Fidelity */}
        <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
        
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;900&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
        
        {/* Injecting the exact Stitch Tailwind Config */}
        <script id="tailwind-config" dangerouslySetInnerHTML={{
          __html: `
            tailwind.config = {
              darkMode: "class",
              theme: {
                extend: {
                  "colors": {
                    "surface": "#131313",
                    "on-surface": "#e5e2e1",
                    "primary": "#ffb3b1",
                    "primary-container": "#ff535a",
                    "on-primary-container": "#5b000e",
                    "secondary": "#ffb59c",
                    "secondary-container": "#8e2c01",
                    "tertiary": "#ffb5a0",
                    "tertiary-container": "#ff5625",
                    "surface-variant": "#353534",
                    "on-surface-variant": "#e4bebc",
                    "surface-container": "#201f1f",
                    "surface-container-high": "#2a2a2a",
                    "surface-container-lowest": "#0e0e0e",
                    "background": "#131313",
                    "on-background": "#e5e2e1",
                    "primary-fixed-dim": "#ffb3b1",
                  },
                  "fontFamily": {
                    "body-md": ["Inter"],
                    "body-lg": ["Inter"],
                    "label-sm": ["Inter"],
                    "label-md": ["Inter"],
                    "headline-md": ["Outfit"],
                    "headline-lg": ["Outfit"],
                    "headline-lg-mobile": ["Outfit"],
                    "display-lg": ["Outfit"]
                  }
                }
              }
            }
          `
        }} />

        <style dangerouslySetInnerHTML={{
          __html: `
            .glass-panel {
                background: rgba(26, 26, 26, 0.6);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            .text-gradient {
                background: linear-gradient(135deg, #ffb3b1, #ff535a);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .btn-glow {
                box-shadow: 0 0 15px rgba(226, 55, 68, 0.4);
            }
          `
        }} />
      </head>
      <body className="bg-background text-on-background min-h-screen overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
        {children}
      </body>
    </html>
  )
}
