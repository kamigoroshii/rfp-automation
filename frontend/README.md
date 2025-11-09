# RFP Automation System - Frontend

Modern React-based frontend for the RFP Automation System with a beautiful olive green theme.

## Features

- 📊 **Dashboard**: Overview of system performance and recent RFPs
- 📋 **RFP List**: Browse and filter all RFPs with status tracking
- 🔍 **RFP Details**: Comprehensive view of specifications, matches, and pricing
- 📤 **Submit RFP**: Easy submission via URL or PDF upload
- 📈 **Analytics**: Performance metrics and trends visualization
- 📦 **Products**: Product catalog browser

## Tech Stack

- **React 18** - UI framework
- **React Router** - Navigation
- **Vite** - Build tool
- **Tailwind CSS** - Styling with olive green theme
- **Chart.js** - Data visualization
- **Axios** - API client
- **date-fns** - Date formatting
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The app will run on http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout/           # Layout components (Header, Sidebar)
│   ├── pages/                # Page components
│   │   ├── Dashboard.jsx
│   │   ├── RFPList.jsx
│   │   ├── RFPDetail.jsx
│   │   ├── SubmitRFP.jsx
│   │   ├── Analytics.jsx
│   │   └── Products.jsx
│   ├── services/             # API and data services
│   │   ├── api.js            # API client with mock/real data toggle
│   │   └── mockData.js       # Mock data for development
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── public/                   # Static assets
├── index.html                # HTML template
├── package.json              # Dependencies
├── vite.config.js            # Vite configuration
└── tailwind.config.js        # Tailwind configuration
```

## Features in Detail

### Mock Data Mode

The frontend includes comprehensive mock data and can run fully functional without a backend:

- Set `USE_MOCK_DATA = true` in `src/services/api.js` (default)
- All API calls return realistic sample data
- Simulates network delays for authentic experience

### Olive Green Theme

Custom color palette defined in `tailwind.config.js`:
- Primary: #556B2F (Dark Olive Green)
- Accent: #9ACD32 (Yellow Green)
- Success: #228B22 (Forest Green)
- Warning: #DAA520 (Goldenrod)
- Background: #F5F5DC (Beige)

### Real-time Updates

- Auto-refresh RFP list every 30 seconds
- Toast notifications for status changes
- Deadline alerts for urgent RFPs (< 48 hours)

## API Integration

To connect to the real backend:

1. Set `USE_MOCK_DATA = false` in `src/services/api.js`
2. Ensure backend is running on http://localhost:8000
3. API proxy is configured in `vite.config.js`

### API Endpoints Used

- `GET /api/rfp/list` - Get all RFPs
- `GET /api/rfp/:id` - Get RFP details
- `POST /api/rfp/submit` - Submit new RFP
- `POST /api/rfp/:id/feedback` - Submit feedback
- `GET /api/analytics/dashboard` - Get analytics
- `GET /api/products/search` - Search products

## Development

### Available Scripts

- `npm run dev` - Start dev server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Style

- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS for styling
- Keep components small and focused

## Building for Production

```bash
npm run build
```

Production build will be in `dist/` directory.

## Docker Deployment

Frontend can be containerized with nginx:

```dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Contributing

1. Follow the existing code structure
2. Maintain the olive green theme
3. Test with both mock and real data
4. Ensure responsive design works on all screen sizes

## License

Copyright 2025 EyTech - All Rights Reserved
