/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        emerald: {
          400: '#10b981',
          500: '#059669',
          600: '#047857',
          900: '#065f46',
          950: '#064e3b',
        }
      }
    },
  },
  plugins: [],
}
