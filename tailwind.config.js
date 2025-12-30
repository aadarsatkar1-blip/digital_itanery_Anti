/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./itanery_app/templates/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        gold: '#d4af37',
        ocean: '#0ea5e9',
      },
    },
  },
  plugins: [],
}
