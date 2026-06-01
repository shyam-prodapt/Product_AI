export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#1a1a2e', 50: '#eeeef5', 900: '#0d0d17' },
        accent: { DEFAULT: '#e94560', light: '#ff6b80' },
        surface: { DEFAULT: '#16213e', light: '#1f2d4e' },
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
    },
  },
  plugins: [],
}

