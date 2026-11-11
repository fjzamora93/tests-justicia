/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        ink: '#242a24',
        paper: '#f5f4ed',
        forest: '#2f664c',
        citron: '#d4ef6a',
        coral: '#e88769',
      },
    },
  },
  plugins: [],
};