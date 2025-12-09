/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#F5F7F0',
          100: '#E8EDD9',
          200: '#D1DBB3',
          300: '#B5C488',
          400: '#98AD5D',
          500: '#7D9645',  // Main primary - olive green
          600: '#637835',
          700: '#4A5A28',
          800: '#323D1C',
          900: '#1F2712',
          DEFAULT: '#7D9645',
          dark: '#4A5A28',
        },
        olive: {
          50: '#F8F9F5',
          100: '#EDEEE6',
          200: '#D7DAC8',
          300: '#BFC3A6',
          400: '#A3A881',
          500: '#8B9068',  // Muted olive
          600: '#6F7454',
          700: '#555841',
          800: '#3B3E2E',
          900: '#25271D',
        },
        sage: {
          50: '#F6F8F6',
          100: '#E9EDE9',
          200: '#D3DBD3',
          300: '#B8C5B8',
          400: '#98AA98',
          500: '#7A8F7A',  // Sage green
          600: '#627262',
          700: '#4A564A',
          800: '#343C34',
          900: '#1F241F',
        },
        accent: {
          50: '#FEFDF8',
          100: '#FDF9E8',
          200: '#FAF2CC',
          300: '#F5E6A3',
          400: '#EDD977',
          500: '#D4BA4F',  // Muted gold
          600: '#B19A3E',
          700: '#88762F',
          800: '#5F5221',
          900: '#3A3214',
        },
        neutral: {
          50: '#FAFAFA',
          100: '#F5F5F5',
          200: '#E5E5E5',
          300: '#D4D4D4',
          400: '#A3A3A3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
        // Status colors using olive green variations
        success: {
          50: '#F5F7F0',
          100: '#E8EDD9',
          200: '#D1DBB3',
          300: '#B5C488',
          400: '#98AD5D',
          500: '#7D9645',  // Success - bright olive
          600: '#637835',
          700: '#4A5A28',
          800: '#323D1C',
          900: '#1F2712',
          DEFAULT: '#7D9645',
        },
        warning: {
          50: '#F8F9F5',
          100: '#EDEEE6',
          200: '#D7DAC8',
          300: '#BFC3A6',
          400: '#A3A881',
          500: '#8B9068',  // Warning - muted olive
          600: '#6F7454',
          700: '#555841',
          800: '#3B3E2E',
          900: '#25271D',
          DEFAULT: '#8B9068',
        },
        error: {
          50: '#F6F8F6',
          100: '#E9EDE9',
          200: '#D3DBD3',
          300: '#B8C5B8',
          400: '#98AA98',
          500: '#7A8F7A',  // Error - sage olive
          600: '#627262',
          700: '#4A564A',
          800: '#343C34',
          900: '#1F241F',
          DEFAULT: '#7A8F7A',
        },
        info: {
          50: '#F5F7F0',
          100: '#E8EDD9',
          200: '#D1DBB3',
          300: '#B5C488',
          400: '#98AD5D',
          500: '#7D9645',  // Info - same as primary
          600: '#637835',
          700: '#4A5A28',
          800: '#323D1C',
          900: '#1F2712',
          DEFAULT: '#7D9645',
        },
        // Text colors
        text: {
          DEFAULT: '#262626',
          light: '#737373',
          lighter: '#A3A3A3',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['Georgia', 'serif'],
        mono: ['Consolas', 'Monaco', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'DEFAULT': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'none': 'none',
      },
      borderRadius: {
        'none': '0',
        'sm': '0.25rem',
        'DEFAULT': '0.375rem',
        'md': '0.5rem',
        'lg': '0.75rem',
        'xl': '1rem',
        'full': '9999px',
      },
      animation: {
        blob: "blob 7s infinite",
        "fade-in-up": "fadeInUp 0.5s ease-out",
        "in": "fadeIn 0.2s ease-out",
      },
      keyframes: {
        blob: {
          "0%": {
            transform: "translate(0px, 0px) scale(1)",
          },
          "33%": {
            transform: "translate(30px, -50px) scale(1.1)",
          },
          "66%": {
            transform: "translate(-20px, 20px) scale(0.9)",
          },
          "100%": {
            transform: "translate(0px, 0px) scale(1)",
          },
        },
        fadeInUp: {
          "0%": {
            opacity: "0",
            transform: "translateY(20px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
    },
  },
  plugins: [],
}
