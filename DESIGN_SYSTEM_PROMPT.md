# SmartBid Control Tower - Design System Prompt for AI Assistants

**Copy and paste this entire prompt when asking Copilot or any AI assistant to maintain design consistency.**

---

## 🎨 MANDATORY DESIGN RULES

You are working on the **SmartBid Control Tower** RFP Automation System. This is a professional, enterprise-grade business application with a **nature-inspired olive/green color palette** that conveys trust, growth, and efficiency.

### ⚠️ CRITICAL REQUIREMENTS:
1. **ONLY use colors defined in this document** - Never introduce blue, purple, or bright colors
2. **ONLY use icons from `lucide-react`** - Never use other icon libraries
3. **Maintain the professional, corporate aesthetic** - No playful or consumer-app styling
4. **Follow the exact color naming conventions** defined in Tailwind config

---

## 📦 ICON LIBRARY

**Package:** `lucide-react` v0.294.0

### Import Pattern:
```jsx
import { IconName, AnotherIcon } from 'lucide-react';
```

### Icon Inventory by Category:

#### **Navigation & Layout:**
- `Menu` - Sidebar toggle
- `ChevronLeft` - Collapse sidebar
- `ChevronRight` - Expand sidebar
- `ChevronDown` - Dropdown indicators
- `ChevronUp` - Expand/collapse sections
- `ArrowLeft` - Back navigation

#### **Core Features:**
- `LayoutDashboard` - Dashboard navigation
- `FileText` - RFP documents, file references
- `Upload` - Submit/upload actions
- `Download` - Ingest/download actions
- `Mail` - Email inbox, notifications
- `BarChart3` - Analytics, charts
- `Package` - Products catalog
- `Shield` - Auditor, security, compliance

#### **Actions & Status:**
- `Search` - Search inputs
- `Filter` - Filter controls
- `Eye` - View/preview actions
- `CheckCircle` - Success, completed status
- `AlertCircle` - Warnings, important info
- `AlertTriangle` - Alerts, warnings
- `XCircle` - Errors, failed status
- `Check` - Confirmation, mark as done
- `X` - Close, dismiss

#### **Data Display:**
- `TrendingUp` - Positive trends, growth
- `Clock` - Time, processing duration
- `Target` - Goals, targets
- `DollarSign` - Pricing, financial
- `ArrowUpRight` - Increase, positive change
- `ArrowDownRight` - Decrease, negative change

#### **User & Collaboration:**
- `User` - User profile, account
- `Users` - Multiple users, team
- `Bell` - Notifications
- `LogOut` - Sign out action

#### **Utilities:**
- `Calendar` - Dates, deadlines
- `Paperclip` - Attachments
- `LinkIcon` (import as `Link as LinkIcon`) - URLs, links
- `Copy` - Copy to clipboard
- `Sparkles` - AI features, smart actions
- `Loader` - Loading states
- `Lock` - Authentication, security
- `Globe` - Web scraping, external sources
- `MessageSquare` - Chat, copilot
- `ExternalLink` - External links

#### **Icon Usage Guidelines:**
- **Size:** Use `size={18}` for normal UI, `size={22}` for sidebar icons, `size={14}` for small inline icons
- **Color:** Apply via className: `text-olive-400`, `text-neutral-600`, etc.

---

## 🎨 COLOR PALETTE - COMPLETE SPECIFICATION

### **PRIMARY COLOR (Olive Green) - #7D9645**
**Main brand identity color**

```jsx
primary-50: '#F5F7F0'    // Very light backgrounds, hover states
primary-100: '#E8EDD9'   // Light backgrounds, subtle highlights
primary-200: '#D1DBB3'   // Borders, dividers
primary-300: '#B5C488'   // Muted accents, disabled states
primary-400: '#98AD5D'   // Secondary interactive elements
primary-500: '#7D9645'   // ⭐ MAIN PRIMARY - buttons, active states, links
primary-600: '#637835'   // Button hover, dark accents
primary-700: '#4A5A28'   // Dark primary variant
primary-800: '#323D1C'   // Very dark accents
primary-900: '#1F2712'   // Darkest shade
DEFAULT: '#7D9645'       // When using just 'primary'
```

**Usage:**
- `bg-primary-600` - Primary buttons (NOT primary-500 for buttons)
- `text-primary-600` - Primary text, links
- `border-primary-300` - Input borders, card borders
- `ring-primary-500` - Focus rings
- `hover:bg-primary-700` - Button hover states
- `bg-primary-50` - Hover backgrounds for list items

---

### **OLIVE (Muted Olive) - #8B9068**
**Supporting color for backgrounds and sidebar**

```jsx
olive-50: '#F8F9F5'     // ⭐ MAIN BACKGROUND COLOR for body
olive-100: '#EDEEE6'    // Card borders, subtle dividers
olive-200: '#D7DAC8'    // -
olive-300: '#BFC3A6'    // -
olive-400: '#A3A881'    // Sidebar inactive icons
olive-500: '#8B9068'    // -
olive-600: '#6F7454'    // -
olive-700: '#555841'    // -
olive-800: '#3B3E2E'    // ⭐ SIDEBAR BORDERS, active nav background
olive-900: '#25271D'    // ⭐ SIDEBAR BACKGROUND (dark)
```

**Usage:**
- `bg-olive-50` - Main content area background
- `bg-olive-900` - Sidebar background (dark mode)
- `bg-olive-800` - Active sidebar navigation item
- `border-olive-800` - Sidebar borders
- `border-olive-100` - White card borders
- `text-olive-300` - Sidebar inactive text
- `text-olive-400` - Sidebar inactive icons
- `text-olive-200` - Sidebar active icons

---

### **SAGE (Sage Green) - #7A8F7A**
**Subtle accent color**

```jsx
sage-50: '#F6F8F6'
sage-500: '#7A8F7A'     // Used for error states (unconventional but per design)
sage-900: '#1F241F'
```

**Usage:**
- `text-sage-500` - Subtle accents
- Currently mapped to error states in the system

---

### **ACCENT (Muted Gold) - #D4BA4F**
**Highlight and special accent color**

```jsx
accent-50: '#FEFDF8'
accent-100: '#FDF9E8'
accent-500: '#D4BA4F'   // Muted gold for special highlights
accent-900: '#3A3214'
```

**Usage:**
- Use sparingly for special badges, premium features
- `bg-accent-50` - Subtle highlight backgrounds

---

### **NEUTRAL (Grayscale) - Professional Grays**
**Core UI colors for text, borders, backgrounds**

```jsx
neutral-50: '#FAFAFA'    // Lightest background
neutral-100: '#F5F5F5'   // Light background
neutral-200: '#E5E5E5'   // Borders, dividers
neutral-300: '#D4D4D4'   // Input borders, inactive borders
neutral-400: '#A3A3A3'   // Placeholder text
neutral-500: '#737373'   // Secondary text
neutral-600: '#525252'   // Tertiary headings, labels
neutral-700: '#404040'   // Body text (alternative)
neutral-800: '#262626'   // Dark text
neutral-900: '#171717'   // Darkest text, headings
```

**Usage:**
- `text-neutral-900` - Primary headings
- `text-neutral-700` - Body text, secondary labels
- `text-neutral-600` - Tertiary text, table headers
- `text-neutral-500` - Light text, timestamps
- `text-neutral-400` - Placeholder text
- `border-neutral-200` - Header border, light dividers
- `border-neutral-300` - Input borders, button borders
- `bg-neutral-100` - Hover states on white backgrounds
- `bg-neutral-50` - Alternate row backgrounds

---

### **STATUS COLORS**

#### **Success (Green) - Same as Primary**
```jsx
success-500: '#7D9645'  // Success states use primary green
DEFAULT: '#7D9645'
```
**Usage:** `text-success`, `bg-success`, completed statuses, positive indicators

#### **Warning (Muted Olive)**
```jsx
warning-500: '#8B9068'  // Muted olive for warnings
DEFAULT: '#8B9068'
```
**Usage:** `bg-warning/10`, `text-warning`, warning badges, pending states

#### **Error (Sage)**
```jsx
error-500: '#7A8F7A'    // Sage olive for errors
DEFAULT: '#7A8F7A'
```
**Usage:** `text-error`, `bg-error`, failed states, required field indicators
**Note:** For destructive actions (like delete buttons), use `text-red-600` and `bg-red-50`

#### **Info (Primary)**
```jsx
info-500: '#7D9645'     // Info uses primary color
DEFAULT: '#7D9645'
```
**Usage:** `text-info`, `bg-info/10`, informational badges

---

### **TEXT COLORS (Semantic)**
```jsx
text-DEFAULT: '#262626'    // Primary text color
text-light: '#737373'      // Secondary text
text-lighter: '#A3A3A3'    // Tertiary text
```

**Usage:**
- `text-text` - Body text (same as neutral-800)
- `text-text-light` - Secondary labels, descriptions
- `text-text-lighter` - Timestamps, metadata

---

## 🏗️ COMPONENT STYLING GUIDELINES

### **Sidebar (Dark Olive)**
```jsx
// Container
className="bg-olive-900 border-r border-olive-800 shadow-xl"

// Toggle Button
className="bg-olive-800 border border-olive-700 hover:bg-olive-700 text-olive-100"

// Navigation Items (Inactive)
className="text-olive-300 hover:bg-olive-800/50 hover:text-white"

// Navigation Items (Active)
className="bg-olive-800 text-white shadow-md border-l-4 border-olive-400"

// Icons (Inactive)
className="text-olive-400 group-hover:text-olive-200"

// Icons (Active)
className="text-olive-200"

// System Status Section
className="border-t border-olive-800 bg-olive-900/50"
className="text-olive-400"  // Label text
className="text-olive-300"  // Section headers

// Online Indicator
className="bg-green-500"
className="animate-ping bg-green-400 opacity-75"
className="text-green-400"  // "Online" text
```

### **Header (White)**
```jsx
// Container
className="bg-white border-b border-neutral-200 shadow-sm"

// Logo Background
className="bg-gradient-to-br from-olive-600 to-olive-800"

// Logo Text
className="text-white font-bold"

// Heading
className="text-neutral-900 font-semibold"

// Subheading
className="text-neutral-500"

// Menu Button
className="text-neutral-600 hover:bg-neutral-100"

// Notification Badge (Unread Dot)
className="bg-error rounded-full ring-1 ring-white"

// User Avatar
className="bg-olive-100"  // Background
className="text-olive-700"  // Icon color

// User Name
className="text-neutral-700 font-medium"

// Divider
className="bg-neutral-200"
```

### **Main Content Area**
```jsx
// Background
className="bg-olive-50"  // Light olive wash

// Page Container
className="space-y-6"  // Vertical spacing

// Page Title
className="text-2xl font-semibold text-neutral-900"

// Page Description
className="text-sm text-neutral-600 mt-1"
```

### **Cards**
```jsx
// Standard Card
className="bg-white rounded-lg border border-olive-100 shadow-sm"

// Hoverable Card
className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"

// Card Header
className="border-b border-neutral-200 bg-neutral-50"

// Card Title
className="text-lg font-semibold text-neutral-900"

// Card Description
className="text-sm text-neutral-600"
```

### **Buttons**

#### Primary Button:
```jsx
className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 
           font-medium text-sm transition-colors duration-150"
```

#### Secondary Button:
```jsx
className="px-4 py-2 bg-white text-neutral-700 border border-neutral-300 rounded-md 
           hover:bg-neutral-50 focus:outline-none focus:ring-2 focus:ring-neutral-400 
           focus:ring-offset-2 font-medium text-sm transition-colors duration-150"
```

#### Destructive Button:
```jsx
className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 
           focus:outline-none focus:ring-2 focus:ring-red-500"
```

### **Form Inputs**
```jsx
// Text Input
className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-md 
           focus:outline-none focus:ring-2 focus:ring-primary-500 
           focus:border-transparent placeholder:text-neutral-400"

// Input with Icon (Add padding)
className="pl-10 pr-4 py-3 border-2 border-primary-300 rounded-lg 
           focus:ring-2 focus:ring-primary-600"

// Select Dropdown
className="px-4 py-2 border border-neutral-300 rounded-lg 
           focus:outline-none focus:ring-2 focus:ring-primary"

// Required Field Asterisk
className="text-error"
```

### **Badges**
```jsx
// Status Badge Base
className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium"

// Success Badge
className="bg-success/10 text-success border border-success/20"

// Warning Badge
className="bg-warning/10 text-warning border border-warning/20"

// Error Badge
className="bg-error/10 text-error border border-error/20"

// Info Badge
className="bg-primary/10 text-primary border border-primary/20"

// New Badge
className="bg-primary-100 text-primary-700 border border-primary-200"
```

### **Tables**
```jsx
// Table Header
className="bg-olive-50"

// Table Header Cell
className="px-6 py-3 text-left text-xs font-semibold text-neutral-600 
           uppercase tracking-wider"

// Table Cell
className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900"

// Table Row (Hover)
className="hover:bg-neutral-50 transition-colors"
```

### **Loading States**
```jsx
// Spinner
className="animate-spin rounded-full h-10 w-10 border-2 
           border-primary-200 border-t-primary-600"

// Loading Container
className="flex items-center justify-center h-96"
```

### **Dropdowns/Menus**
```jsx
// Dropdown Container
className="absolute top-12 right-0 w-80 bg-white border border-gray-200 
           rounded-lg shadow-xl z-50 animate-in fade-in slide-in-from-top-2"

// Dropdown Header
className="p-3 border-b border-gray-100 bg-gray-50 rounded-t-lg"

// Dropdown Item
className="px-4 py-3 hover:bg-primary-50 border-b border-gray-100 
           transition-colors"
```

### **Focus States**
```jsx
// Global Focus Outline
*:focus-visible {
  outline: 2px solid #637835;  /* primary-600 */
  outline-offset: 2px;
}
```

---

## 📏 SPACING & SIZING

### **Border Radius:**
- `rounded-sm` - 0.25rem (small elements)
- `rounded` / `rounded-md` - 0.375-0.5rem (default buttons, inputs)
- `rounded-lg` - 0.75rem (cards, containers)
- `rounded-xl` - 1rem (large cards)
- `rounded-full` - 9999px (avatars, badges, pills)

### **Shadows:**
- `shadow-sm` - Subtle card elevation
- `shadow-md` - Hover states, dropdowns
- `shadow-lg` - Modals, important overlays
- `shadow-xl` - Sidebar, major UI sections

### **Icon Sizes:**
- Small inline: `size={14}`
- Standard UI: `size={18}` or `size={20}`
- Sidebar/navigation: `size={22}`
- Large feature icons: `size={24}`

---

## 🎭 ANIMATION & TRANSITIONS

### **Standard Transition:**
```jsx
className="transition-colors duration-150"  // For color changes
className="transition-shadow duration-200"  // For elevation changes
className="transition-all duration-200"     // For multiple properties
```

### **Loading Animations:**
```jsx
className="animate-spin"         // Spinners
className="animate-ping"         // Notification dots
className="animate-in fade-in"   // Dropdown entrances
```

---

## 📋 COMMON PATTERNS

### **Search Bar:**
```jsx
<div className="relative">
  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-500" size={20} />
  <input
    type="text"
    placeholder="Search..."
    className="w-full pl-10 pr-4 py-2 border border-neutral-300 rounded-lg 
               focus:outline-none focus:ring-2 focus:ring-primary"
  />
</div>
```

### **Stat Card:**
```jsx
<div className="bg-white rounded-lg border border-olive-100 shadow-sm p-6">
  <div className="flex items-center justify-between">
    <IconComponent size={22} className="text-primary-600" />
    <span className="text-2xl font-bold text-neutral-900">42</span>
  </div>
  <p className="text-sm text-neutral-600 mt-2">Stat Label</p>
</div>
```

### **Notification Badge:**
```jsx
<div className="relative">
  <Bell size={18} />
  {hasUnread && (
    <span className="absolute top-0 right-0 w-2 h-2 bg-error rounded-full 
                     ring-1 ring-white"></span>
  )}
</div>
```

---

## ⚠️ WHAT NOT TO DO

❌ **Never use these colors:**
- Blue shades (except in rare external link cases)
- Purple, pink, or bright colors
- Neon or saturated colors
- Pure black (#000000) - use neutral-900 instead
- Pure white backgrounds without borders - always add subtle olive-100 borders

❌ **Never use these patterns:**
- Material Design components
- Bootstrap classes
- Other icon libraries (Font Awesome, Heroicons, etc.)
- Rounded corners > 1rem (except rounded-full)
- Heavy shadows or 3D effects

✅ **Always:**
- Use olive/green color family
- Import icons from `lucide-react`
- Add focus states with `focus:ring-2 focus:ring-primary-500`
- Use `transition-colors duration-150` for hover states
- Test with sidebar collapsed and expanded
- Ensure text has sufficient contrast (WCAG AA minimum)

---

## 🚀 QUICK REFERENCE

**Most Common Combinations:**

```jsx
// Primary CTA Button
className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"

// White Card
className="bg-white rounded-lg border border-olive-100 shadow-sm p-6"

// Section Heading
className="text-2xl font-semibold text-neutral-900"

// Body Text
className="text-sm text-neutral-600"

// Input Field
className="w-full px-3 py-2 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500"

// Success Badge
className="px-2.5 py-0.5 bg-success/10 text-success border border-success/20 rounded-md text-xs font-medium"

// Table Header
className="bg-olive-50 px-6 py-3 text-xs font-semibold text-neutral-600 uppercase"
```

---

## 📝 USAGE INSTRUCTIONS

When you receive this prompt, you MUST:

1. **Use ONLY these colors** - Never deviate from the palette
2. **Import icons from `lucide-react`** - Check the icon inventory above
3. **Follow component patterns exactly** - Copy the className patterns
4. **Maintain professional aesthetic** - Corporate, not consumer
5. **Test responsiveness** - Mobile, tablet, desktop
6. **Add proper focus states** - Accessibility first

**Before suggesting any code, ask yourself:**
- Is this color from the approved palette?
- Is this icon from lucide-react?
- Does this maintain the professional, olive/green theme?
- Have I included proper hover and focus states?

---

**End of Design System Prompt**

*Last Updated: January 23, 2026*
*Version: 1.0*
