/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hell: {
          darkest: '#070709',
          black: '#0d0d12',
          card: '#14141c',
          cardHover: '#1c1c28',
          surface: '#1f202e',
          border: '#2e3042',
          borderLight: '#43465e',
          red: {
            DEFAULT: '#dc2626',
            hover: '#ef4444',
            dark: '#7f1d1d',
            glow: '#ff3333',
          },
          green: {
            DEFAULT: '#10b981',
            hover: '#34d399',
            dark: '#064e3b',
            acid: '#22c55e',
            glow: '#00ff87',
          },
          steel: {
            DEFAULT: '#94a3b8',
            dark: '#475569',
            light: '#cbd5e1',
            bright: '#f8fafc',
          }
        }
      },
      fontFamily: {
        gothic: ['"Cinzel Decorative"', 'Cinzel', 'Georgia', 'serif'],
        metal: ['"Metal Mania"', 'Impact', 'sans-serif'],
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'flame': '0 0 20px -3px rgba(220, 38, 38, 0.45), 0 0 8px -2px rgba(220, 38, 38, 0.6)',
        'flame-lg': '0 0 35px -5px rgba(220, 38, 38, 0.6), 0 0 15px -2px rgba(239, 68, 68, 0.8)',
        'acid': '0 0 20px -3px rgba(16, 185, 129, 0.45), 0 0 8px -2px rgba(16, 185, 129, 0.6)',
        'acid-lg': '0 0 35px -5px rgba(16, 185, 129, 0.6), 0 0 15px -2px rgba(52, 211, 153, 0.8)',
        'metal': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 10px 25px -5px rgba(0, 0, 0, 0.8)',
      },
      backgroundImage: {
        'hell-radial': 'radial-gradient(circle at top, rgba(220, 38, 38, 0.15), rgba(7, 7, 9, 0.95) 70%)',
        'toxic-radial': 'radial-gradient(circle at bottom right, rgba(16, 185, 129, 0.12), transparent 50%)',
        'metal-gradient': 'linear-gradient(180deg, rgba(30, 32, 45, 0.8) 0%, rgba(18, 18, 25, 0.95) 100%)',
      }
    },
  },
  plugins: [],
}

