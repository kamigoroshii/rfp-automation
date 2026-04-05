# SmartBid Control Tower - Design System Reference

**Complete styling guide for icons, fonts, colors, and components**  
**Last Updated:** February 11, 2026

---

## 🎨 Icon System

### Icon Library
- **Package**: `lucide-react`
- **Version**: `^0.294.0`
- **Documentation**: https://lucide.dev/
- **Installation**: 
```bash
npm install lucide-react@^0.294.0
```

### Icons Used in Project

#### Navigation & Layout
- `LayoutDashboard` - Dashboard icon
- `Menu` - Hamburger menu
- `ChevronLeft`, `ChevronRight` - Left/right arrows
- `ChevronDown`, `ChevronUp` - Dropdown arrows

#### Document & File Operations
- `FileText` - Document/RFP icon
- `Upload` - Upload action
- `Download` - Download action
- `Paperclip` - Attachment
- `Mail` - Email/inbox

#### Status & Indicators
- `CheckCircle` - Success/completed
- `XCircle` - Error/failed
- `AlertTriangle` - Warning
- `AlertCircle` - Info alert
- `Check` - Checkmark
- `Shield` - Security/audit
- `Eye` - View/preview
- `Clock` - Time/pending
- `Loader` - Loading spinner

#### Business & Analytics
- `TrendingUp` - Growth/positive trend
- `ArrowUpRight` - Increase
- `ArrowDownRight` - Decrease
- `BarChart3` - Analytics/charts
- `DollarSign` - Pricing/money
- `Target` - Goals/targets

#### User & Authentication
- `User` - Single user
- `Users` - Multiple users/team
- `LogOut` - Sign out
- `Lock` - Security/password

#### Product & Miscellaneous
- `Package` - Products/inventory
- `Search` - Search functionality
- `Filter` - Filter options
- `Calendar` - Date picker
- `MessageSquare` - Chat/messages
- `X` - Close button
- `Bell` - Notifications
- `ExternalLink` - External link
- `Globe` - Web/internet
- `Link` - Link/URL
- `Sparkles` - AI/special feature
- `Copy` - Copy to clipboard

### Icon Usage Patterns

#### Basic Usage
```jsx
import { IconName } from 'lucide-react';

<IconName className="w-5 h-5" />
```

#### Standard Sizes
```jsx
// Small (16px)
<Icon className="w-4 h-4" />

// Medium (20px) - Most common
<Icon className="w-5 h-5" />

// Large (24px)
<Icon className="w-6 h-6" />

// Extra Large (32px)
<Icon className="w-8 h-8" />
```

#### With Colors
```jsx
// Primary color
<Icon className="w-5 h-5 text-primary-600" />

// Gray/neutral
<Icon className="w-5 h-5 text-neutral-500" />

// Success
<Icon className="w-5 h-5 text-success-600" />

// Error
<Icon className="w-5 h-5 text-error-600" />

// White (on dark backgrounds)
<Icon className="w-5 h-5 text-white" />
```

#### In Buttons
```jsx
<button className="flex items-center gap-2">
  <Icon className="w-4 h-4" />
  Button Text
</button>
```

#### In Cards/Headers
```jsx
<div className="flex items-center gap-3">
  <Icon className="w-6 h-6 text-primary-600" />
  <h2>Section Title</h2>
</div>
```

#### Status Badges
```jsx
<div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-success-100">
  <CheckCircle className="w-3.5 h-3.5 text-success-600" />
  <span className="text-xs text-success-700">Approved</span>
</div>
```

---

## 📝 Typography System

### Primary Font: Inter

**Google Fonts Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
```

**Alternative CDN Link (HTML):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Font Weights
- **300** - Light (rarely used)
- **400** - Regular (body text)
- **500** - Medium (subheadings, emphasis)
- **600** - Semibold (headings, buttons)
- **700** - Bold (strong emphasis)

### Font Family Configuration

**Tailwind Config:**
```javascript
fontFamily: {
  sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
  serif: ['Georgia', 'serif'],
  mono: ['Consolas', 'Monaco', 'monospace'],
}
```

**CSS:**
```css
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
```

### Font Size Scale

```javascript
// Tailwind Config
fontSize: {
  'xs': ['0.75rem', { lineHeight: '1rem' }],      // 12px / 16px
  'sm': ['0.875rem', { lineHeight: '1.25rem' }],  // 14px / 20px
  'base': ['1rem', { lineHeight: '1.5rem' }],     // 16px / 24px
  'lg': ['1.125rem', { lineHeight: '1.75rem' }],  // 18px / 28px
  'xl': ['1.25rem', { lineHeight: '1.75rem' }],   // 20px / 28px
  '2xl': ['1.5rem', { lineHeight: '2rem' }],      // 24px / 32px
  '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 30px / 36px
  '4xl': ['2.25rem', { lineHeight: '2.5rem' }],   // 36px / 40px
}
```

### Typography Usage Guide

```css
/* Body Text */
body {
  @apply font-sans antialiased text-base text-neutral-900;
  letter-spacing: -0.01em;  /* Slightly tighter for professional look */
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  @apply font-semibold text-neutral-900;
  letter-spacing: -0.02em;  /* Tighter letter spacing */
}

h1 { @apply text-4xl; }  /* 36px */
h2 { @apply text-3xl; }  /* 30px */
h3 { @apply text-2xl; }  /* 24px */
h4 { @apply text-xl; }   /* 20px */
h5 { @apply text-lg; }   /* 18px */
h6 { @apply text-base; } /* 16px */

/* Small Text */
.text-small { @apply text-sm; }      /* 14px */
.text-caption { @apply text-xs; }    /* 12px */

/* Code */
code {
  @apply font-mono text-sm;
}
```

### Letter Spacing Guide
- **Body text**: `-0.01em` (subtle tightening)
- **Headings**: `-0.02em` (more pronounced tightening)
- **All caps/tracking**: `0.05em` to `0.1em` (looser for readability)

---

## 🎨 Complete Color Palette

### Primary Colors (Olive Green)

**Main brand color - professional, natural, trustworthy**

```javascript
primary: {
  50: '#F5F7F0',   // Lightest - backgrounds
  100: '#E8EDD9',  // Very light - hover states
  200: '#D1DBB3',  // Light
  300: '#B5C488',  // Light-medium
  400: '#98AD5D',  // Medium
  500: '#7D9645',  // Main primary - DEFAULT
  600: '#637835',  // Dark - primary.dark
  700: '#4A5A28',  // Darker
  800: '#323D1C',  // Very dark
  900: '#1F2712',  // Darkest
  DEFAULT: '#7D9645',
  dark: '#4A5A28',
}
```

**Usage:**
- `bg-primary-500` or `bg-primary` - Main buttons, active states
- `text-primary-600` - Primary text accents
- `bg-primary-50` - Light backgrounds
- `border-primary-300` - Borders, dividers

### Secondary Colors (Muted Olive)

```javascript
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
}
```

**Usage:**
- `bg-olive-50` - Subtle backgrounds (main body)
- `bg-olive-100` - Card backgrounds
- `text-olive-700` - Secondary text

### Sage Green

```javascript
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
}
```

**Usage:**
- Alternative accent color
- Error states (subtle)

### Accent Colors (Muted Gold)

```javascript
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
}
```

**Usage:**
- Highlights, special features
- Hover effects on secondary elements

### Neutral Colors (Grays)

```javascript
neutral: {
  50: '#FAFAFA',   // Almost white - backgrounds
  100: '#F5F5F5',  // Very light gray
  200: '#E5E5E5',  // Light gray - borders
  300: '#D4D4D4',  // Medium-light gray
  400: '#A3A3A3',  // Medium gray
  500: '#737373',  // Base gray - icons, secondary text
  600: '#525252',  // Dark gray
  700: '#404040',  // Darker gray - text
  800: '#262626',  // Very dark - primary text
  900: '#171717',  // Almost black
}
```

**Usage:**
- `bg-neutral-50` - Page backgrounds
- `bg-neutral-100` - Card backgrounds
- `border-neutral-200` - Default borders
- `text-neutral-500` - Secondary text, icons
- `text-neutral-700` - Body text
- `text-neutral-800` - Headings
- `text-neutral-900` - Strong emphasis

### Status Colors

#### Success (Olive Green)
```javascript
success: {
  50: '#F5F7F0',
  500: '#7D9645',  // Same as primary
  600: '#637835',
  DEFAULT: '#7D9645',
}
```
**Usage:** Approved, completed, passed

#### Warning (Muted Olive)
```javascript
warning: {
  50: '#F8F9F5',
  500: '#8B9068',  // Muted olive
  700: '#555841',
  DEFAULT: '#8B9068',
}
```
**Usage:** Pending, caution, review needed

#### Error (Sage)
```javascript
error: {
  50: '#F6F8F6',
  500: '#7A8F7A',  // Sage olive
  700: '#4A564A',
  DEFAULT: '#7A8F7A',
}
```
**Usage:** Rejected, failed, errors

#### Info (Same as Primary)
```javascript
info: {
  50: '#F5F7F0',
  500: '#7D9645',
  DEFAULT: '#7D9645',
}
```
**Usage:** Information, notifications

### Text Color Utilities

```javascript
text: {
  DEFAULT: '#262626',  // neutral-800
  light: '#737373',    // neutral-500
  lighter: '#A3A3A3',  // neutral-400
}
```

**Usage:**
```jsx
<p className="text-text">Main text</p>
<p className="text-text-light">Secondary text</p>
<p className="text-text-lighter">Tertiary text</p>
```

---

## 🎭 Shadows & Elevation

### Box Shadow Scale

```javascript
boxShadow: {
  'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  'DEFAULT': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  'none': 'none',
}
```

**Usage Guide:**
- `shadow-sm` - Subtle cards, inputs
- `shadow` (default) - Standard cards
- `shadow-md` - Dropdown menus, popovers
- `shadow-lg` - Modals, dialogs
- `shadow-xl` - Hero sections, large modals

### Border Radius Scale

```javascript
borderRadius: {
  'none': '0',
  'sm': '0.25rem',      // 4px - tight corners
  'DEFAULT': '0.375rem', // 6px - default
  'md': '0.5rem',       // 8px - cards
  'lg': '0.75rem',      // 12px - large cards
  'xl': '1rem',         // 16px - hero sections
  'full': '9999px',     // Pills, circles
}
```

---

## 🎬 Animations & Transitions

### Animation Keyframes

```javascript
animation: {
  blob: "blob 7s infinite",
  "fade-in-up": "fadeInUp 0.5s ease-out",
  "in": "fadeIn 0.2s ease-out",
}

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
}
```

### Transition Standards

```css
/* Applied to all interactive elements */
button, a, input, select, textarea {
  transition-property: background-color, border-color, color;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Timing Guide:**
- **150ms** - Button hovers, color changes
- **200ms** - Fade in/out
- **300ms** - Slide/transform animations
- **500ms** - Page transitions

---

## 🧱 Custom Scrollbar

```css
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #FAFAFA;  /* neutral-50 */
}

::-webkit-scrollbar-thumb {
  background: #D4D4D4;  /* neutral-300 */
  border-radius: 5px;
  border: 2px solid #FAFAFA;
}

::-webkit-scrollbar-thumb:hover {
  background: #A3A3A3;  /* neutral-400 */
}
```

---

## 🧩 Component Classes

### Card Component

```css
.card {
  @apply bg-white rounded-lg border border-olive-100 shadow-sm;
}

.card-hover {
  @apply transition-shadow duration-200 hover:shadow-md;
}
```

**Usage:**
```jsx
<div className="card card-hover p-6">
  Card content
</div>
```

### Button Components

```css
.btn {
  @apply px-4 py-2 rounded-md font-medium text-sm;
  @apply focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-primary {
  @apply bg-primary-600 text-white focus:ring-primary-500;
}

.btn-secondary {
  @apply bg-white text-neutral-700 border border-neutral-300 focus:ring-neutral-400;
}
```

**Usage:**
```jsx
<button className="btn btn-primary">Primary Action</button>
<button className="btn btn-secondary">Secondary Action</button>
```

### Input Component

```css
.input {
  @apply w-full px-3 py-2 text-sm border border-neutral-300 rounded-md;
  @apply focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  @apply placeholder:text-neutral-400;
}
```

**Usage:**
```jsx
<input type="text" className="input" placeholder="Enter text..." />
```

### Badge Component

```css
.badge {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium;
}
```

**Variants:**
```jsx
// Success
<span className="badge bg-success-100 text-success-700">Approved</span>

// Warning
<span className="badge bg-warning-100 text-warning-700">Pending</span>

// Error
<span className="badge bg-error-100 text-error-700">Rejected</span>

// Neutral
<span className="badge bg-neutral-100 text-neutral-700">Draft</span>
```

### Table Component

```css
.table {
  @apply min-w-full divide-y divide-neutral-200;
}

.table thead {
  @apply bg-olive-50;
}

.table th {
  @apply px-6 py-3 text-left text-xs font-semibold text-neutral-600 uppercase tracking-wider;
}

.table td {
  @apply px-6 py-4 whitespace-nowrap text-sm text-neutral-900;
}
```

---

## 📦 Quick Setup Guide

### 1. Install Dependencies

```bash
npm install lucide-react@^0.294.0 tailwindcss@^3.3.6 autoprefixer@^10.4.16 postcss@^8.4.32
```

### 2. Import Google Font

Add to your main CSS file:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
```

Or in HTML:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### 3. Configure Tailwind

Create/update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Copy all color scales from this document
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      // Add other customizations
    },
  },
  plugins: [],
}
```

### 4. Add Base Styles

Create your main CSS file:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-sans antialiased bg-olive-50 text-neutral-900;
    letter-spacing: -0.01em;
  }
  
  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold text-neutral-900;
    letter-spacing: -0.02em;
  }
}

@layer components {
  /* Add component classes */
}
```

### 5. Use Icons

```jsx
import { FileText, CheckCircle, TrendingUp } from 'lucide-react';

function MyComponent() {
  return (
    <div>
      <FileText className="w-5 h-5 text-primary-600" />
      <CheckCircle className="w-5 h-5 text-success-600" />
      <TrendingUp className="w-5 h-5 text-neutral-500" />
    </div>
  );
}
```

---

## 🎯 Design Principles

### 1. Professional & Clean
- Muted, earthy color palette (olive, sage, gold)
- Subtle shadows and borders
- Consistent spacing and alignment

### 2. Readable Typography
- Inter font for excellent legibility
- Negative letter-spacing for tighter, modern look
- Clear hierarchy with font sizes and weights

### 3. Consistent Iconography
- Lucide React for unified icon style
- Standard sizing: 16px (w-4), 20px (w-5), 24px (w-6)
- Always paired with proper color classes

### 4. Subtle Animations
- 150ms transitions for interactions
- Smooth, not distracting
- Respects `prefers-reduced-motion`

### 5. Accessibility
- High contrast text colors
- Focus indicators with `focus:ring-2`
- Semantic HTML and ARIA labels

---

## 📐 Spacing Scale

Using Tailwind's default spacing scale (4px increments):

```
0    - 0px
0.5  - 2px
1    - 4px
1.5  - 6px
2    - 8px
2.5  - 10px
3    - 12px
4    - 16px
5    - 20px
6    - 24px
8    - 32px
10   - 40px
12   - 48px
16   - 64px
20   - 80px
24   - 96px
```

**Custom additions:**
```javascript
spacing: {
  '128': '32rem',  // 512px
  '144': '36rem',  // 576px
}
```

---

## 🎨 Common Patterns

### Status Badge with Icon
```jsx
<div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-success-100">
  <CheckCircle className="w-3.5 h-3.5 text-success-600" />
  <span className="text-xs font-medium text-success-700">Approved</span>
</div>
```

### Card Header with Icon
```jsx
<div className="flex items-center justify-between p-6 border-b border-neutral-200">
  <div className="flex items-center gap-3">
    <FileText className="w-6 h-6 text-primary-600" />
    <h2 className="text-xl font-semibold">Card Title</h2>
  </div>
  <button className="text-neutral-500 hover:text-neutral-700">
    <X className="w-5 h-5" />
  </button>
</div>
```

### Button with Icon
```jsx
<button className="btn btn-primary inline-flex items-center gap-2">
  <Upload className="w-4 h-4" />
  Upload File
</button>
```

### Stat Card
```jsx
<div className="card p-6">
  <div className="flex items-center justify-between">
    <div>
      <p className="text-sm text-neutral-500">Total RFPs</p>
      <p className="text-3xl font-semibold text-neutral-900">142</p>
    </div>
    <div className="p-3 bg-primary-100 rounded-lg">
      <FileText className="w-8 h-8 text-primary-600" />
    </div>
  </div>
  <div className="mt-4 flex items-center gap-1 text-sm">
    <TrendingUp className="w-4 h-4 text-success-600" />
    <span className="text-success-600 font-medium">12%</span>
    <span className="text-neutral-500">vs last month</span>
  </div>
</div>
```

---

## 🔍 Focus States

```css
*:focus-visible {
  outline: 2px solid #637835;  /* primary-600 */
  outline-offset: 2px;
}
```

**Button focus:**
```jsx
<button className="focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Click Me
</button>
```

---

## 📱 Responsive Design

Use Tailwind's responsive prefixes:

```jsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  Cards
</div>

<div className="p-4 md:p-6 lg:p-8">
  Responsive padding
</div>
```

---

## 🎪 Complete Package.json

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

---

**Version:** 1.0  
**Maintained by:** SmartBid Development Team  
**Based on:** RFP Automation System Design System

