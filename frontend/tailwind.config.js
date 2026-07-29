/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#ea580c',
          light: '#fb923c',
          dark: '#9a3412',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out forwards',
        'slide-up': 'slideUp 0.5s ease-out forwards',
        'slide-in-right': 'slideInRight 0.4s ease-out forwards',
        'score-reveal': 'scoreReveal 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards',
        'progress-fill': 'progressFill 0.8s ease-out forwards',
        'spin': 'spin 0.7s linear infinite',
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}
