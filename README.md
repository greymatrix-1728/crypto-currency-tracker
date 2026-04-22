
# 🪙 Crypto Hunter

A cryptocurrency tracking web application built with React. Track live prices, market caps, and historical charts for the top 100 cryptocurrencies — powered by the CoinGecko API.

![React](https://img.shields.io/badge/React-17.0.2-61DAFB?style=flat&logo=react)
![Material UI](https://img.shields.io/badge/Material--UI-4.12.3-0081CB?style=flat&logo=mui)
![Chart.js](https://img.shields.io/badge/Chart.js-3.5.1-FF6384?style=flat&logo=chartdotjs)
![CoinGecko API](https://img.shields.io/badge/API-CoinGecko-8DC647?style=flat)

---

## 🌐 Live Demo

🔗 [View Live App](#) -https://storied-pika-0cfc7b.netlify.app/

---

## 📸 Preview

![Homepage Preview](public/banner2.jpg)

---

## ✨ Features

- 📊 **Live Prices** — Top 100 cryptocurrencies ranked by market cap
- 🔍 **Search** — Filter coins by name or symbol in real time
- 💱 **Currency Toggle** — Switch between USD ($) and INR (₹)
- 🎠 **Trending Carousel** — Auto-scrolling strip of top trending coins
- 📈 **Historical Chart** — Interactive price chart per coin (24h, 30d, 3m, 1y)
- 📱 **Responsive** — Works on desktop and mobile

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| React 17 | Core UI library |
| React Router DOM v5 | Client-side routing |
| Material-UI v4 | UI components & styling |
| Axios | API requests |
| Chart.js + react-chartjs-2 | Historical price charts |
| react-alice-carousel | Trending coins carousel |
| html-react-parser | Render HTML from API descriptions |
| CoinGecko API | Cryptocurrency data source |

---

## 🚀 Getting Started

### Prerequisites

- Node.js v14 or higher
- npm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/crypto-tracker.git
   cd crypto-tracker
   ```

2. **Install dependencies**
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Fix ajv compatibility (Node v18+)**
   ```bash
   npm install ajv@8 --legacy-peer-deps
   ```

4. **Add your CoinGecko API key**

   Get a free Demo API key from [coingecko.com/en/api](https://www.coingecko.com/en/api) and add it to `src/config/api.js`:
   ```js
   const API_KEY = "your_api_key_here";
   ```

5. **Start the development server**
   ```bash
   npm start
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📁 Project Structure

```
src/
├── index.js                   # App entry point
├── CryptoContext.js            # Global state (currency, symbol)
├── App.js                      # Routes setup
├── config/
│   ├── api.js                  # CoinGecko API URLs
│   └── data.js                 # Chart time range options
├── Pages/
│   ├── HomePage.js             # Route: /
│   └── CoinPage.js             # Route: /coins/:id
└── components/
    ├── Header.js               # Navigation bar
    ├── CoinsTable.js           # Searchable coins table
    ├── CoinInfo.js             # Historical price chart
    ├── SelectButton.js         # Chart time range button
    └── Banner/
        ├── Banner.js           # Hero section
        └── Carousel.js         # Trending coins strip
```

---

## 📦 Deployment

### Build for production
```bash
npm run build
```

This creates an optimised `build/` folder ready for deployment.

### Deploy to Netlify (Drag & Drop)
1. Run `npm run build`
2. Go to [netlify.com/drop](https://app.netlify.com/drop)
3. Drag and drop the `build/` folder
4. Get your live URL instantly ✅

### Deploy via GitHub + Netlify (Auto-deploy)
1. Push this repo to GitHub
2. Go to [netlify.com](https://netlify.com) → Add new site → Import from Git
3. Select your repo
4. Set build command: `npm run build`
5. Set publish directory: `build`
6. Click Deploy 🚀

---

## 🔑 Environment Notes

The CoinGecko Demo API key is stored in `src/config/api.js`. For production apps, consider moving it to a `.env` file:

```env
REACT_APP_COINGECKO_API_KEY=your_key_here
```

Then reference it in code as `process.env.REACT_APP_COINGECKO_API_KEY`.

---

## 📄 License

MIT © ajet

---

## 🙏 Acknowledgements

- [CoinGecko](https://www.coingecko.com/) for the free cryptocurrency API
- [Material-UI](https://mui.com/) for the component library
- [Chart.js](https://www.chartjs.org/) for the charting library
