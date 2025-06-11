/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Keep this set to 'class' for theme toggling
  content: [
    './templates/**/*.html', // Make sure your Django templates are scanned
  ],
  theme: {
    extend: {
      backgroundImage: {
        'custom-gradient': `
          radial-gradient(ellipse at top, rgba(30, 41, 59, 0.8), transparent),
          radial-gradient(ellipse at bottom, rgba(15, 23, 42, 0.8), transparent)
        `,
      },
      backgroundColor: {
        'custom-base': '#0f172a',
      },
      colors: {
        // --- Application-wide Backgrounds & Text ---
        // These are your main base colors for the entire app
        'app-background': {
          light: '#ffffff', // Pure white for light mode main background
          dark: '#0a0a0a',   // neutral-950 for dark mode main background
        },
        'app-text': {
          light: '#1f2937', // A slightly darker gray for main text (gray-800)
          dark: '#e5e7eb',   // A very light gray for main text (neutral-200)
        },

        // --- Code Block Specific Colors (as per your image) ---
        'code-block': {
          // The background of the entire code block container (slightly lighter in dark mode)
          outer: {
            light: '#f9fafb', // gray-50 or gray-100 for the outer container
            dark: '#171717',  // neutral-900 for the outer container in dark mode
          },
          // The background of the actual code area
          inner: {
            light: '#ffffff', // white for the inner code area
            dark: '#0a0a0a',   // neutral-950 for the inner code area
          },
          // Border for the code block
          border: {
            light: '#e5e7eb', // gray-200
            dark: '#404040',  // neutral-600 or neutral-700
          },
          // Text color within the code block (default unhighlighted text)
          text: {
            light: '#1f2937', // gray-800
            dark: '#f5f5f5',  // neutral-100
          },
          // Color for the '$' prompt and unhovered copy icon
          prompt: {
            light: '#6b7280', // gray-500
            dark: '#a3a3a3',  // neutral-400
          },
          // Color for the code block header text (e.g., "Python")
          header: {
            light: '#4b5563', // gray-700
            dark: '#d4d4d4',  // neutral-300
          },
        
        },

        // --- Accent Colors (e.g., for buttons, links, etc.) ---
        'accent': {
          DEFAULT: { // Default accent color (e.g., for general buttons)
            light: '#3b82f6', // blue-500
            dark: '#60a5fa',  // blue-400
          },
          hover: {
            light: '#2563eb', // blue-600
            dark: '#3b82f6',  // blue-500
          },
        },

        // --- Syntax Highlighting Colors ---
        // These are examples. You'd typically map these to your highlight.js/Prism.js theme.
        // Or, if you control it via CSS, use these for your custom classes.
        'syntax-keyword': {
          light: '#8b5cf6', // purple-500
          dark: '#c084fc',  // purple-400
        },
        'syntax-function': {
          light: '#ef4444', // red-500
          dark: '#f87171',  // red-400
        },
        'syntax-string': {
          light: '#22c55e', // green-500
          dark: '#4ade80',  // green-400
        },
        'syntax-comment': {
          light: '#9ca3af', // gray-400
          dark: '#6b7280',  // neutral-500
        },
        'syntax-type': {
          light: '#f97316', // orange-500
          dark: '#fb923c',  // orange-400
        },
        // ... add more as needed for your highlighter's tokens
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'), // Ensure this is still included
  ],
};