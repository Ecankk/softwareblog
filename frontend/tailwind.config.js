module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [ // 支持多个主题
      'lofi', 'dark', 'cupcake', 'light', 'dracula', 'valentine', 'forest', 'luxury'
    ],
  },
}
