# 🍽 CanteenOrder — College Canteen Pre-Order System

A real-world full-stack canteen management system built with **HTML, CSS, JavaScript (main), Python Flask, and Java**.

---

## 🚀 Quick Start (Run in 3 Steps)

### Step 1 — Install Python dependencies
```bash
pip install flask flask-socketio eventlet
```

### Step 2 — Run Flask server
```bash
python app.py
```
Open browser → **http://localhost:5000**

### Step 3 — (Optional) Run Java microservice
```bash
cd java/src/main/java/com/canteen
javac CanteenReportService.java
java com.canteen.CanteenReportService
```
Java service → **http://localhost:8080**

---

## 🔑 Demo Login Credentials

| Role    | Username  | Password   | Access |
|---------|-----------|------------|--------|
| Student | student1  | pass123    | Menu, Cart, Wallet, Orders |
| Admin   | admin     | admin123   | Dashboard, Reports, Stock |
| Kitchen | kitchen   | kitchen1   | Kitchen Display |

---

## 📁 Project Structure

```
CanteenOrder/
│
├── app.py                          ← Flask main app + Socket.io + REST API
├── requirements.txt                ← Python dependencies
│
├── templates/                      ← HTML pages (Jinja2)
│   ├── login.html                  ← Login page (student/admin/kitchen)
│   ├── menu.html                   ← Student menu with AI recommendations
│   ├── cart.html                   ← Cart with wallet payment + group order
│   ├── orders.html                 ← Live order tracking with countdown
│   ├── wallet.html                 ← Digital wallet + points/rewards
│   ├── rate.html                   ← Star rating system
│   ├── kitchen.html                ← Kitchen display board (dark mode)
│   ├── admin.html                  ← Admin dashboard with Chart.js
│   ├── menu_manager.html           ← Menu CRUD management
│   ├── stock.html                  ← Real-time stock toggle manager
│   └── reports.html                ← PDF report generation
│
├── static/
│   ├── css/
│   │   └── main.css                ← Complete design system (saffron + teal)
│   └── js/
│       └── utils.js                ← Shared JS (Cart, Toast, API, User)
│
└── java/
    └── src/main/java/com/canteen/
        └── CanteenReportService.java  ← Java PDF + email + token + scheduler
```

---

## ✨ Features Implemented

### JavaScript (Main Language)
- ✅ Live menu with real-time sold-out sync (Socket.io)
- ✅ Cart management (localStorage) with group order + split support
- ✅ Digital wallet one-tap checkout
- ✅ Token number display
- ✅ Live order status tracker (Placed → Confirmed → Cooking → Ready)
- ✅ Estimated wait time countdown
- ✅ Points meter animation
- ✅ Admin Chart.js dashboard (revenue, peak hours, top items, forecast)
- ✅ Star rating UI

### Python (Flask)
- ✅ REST API for all data operations
- ✅ Socket.io for real-time broadcast
- ✅ Kitchen queue optimizer
- ✅ Dynamic wait time predictor
- ✅ AI meal recommendation (time-of-day + order history based)
- ✅ Rating analytics engine
- ✅ Demand forecasting
- ✅ Stock state management

### Java (Microservice)
- ✅ Token number generator API
- ✅ Daily PDF sales report (text format, iText when jar added)
- ✅ Weekly email summary (JavaMail when configured)
- ✅ Tiffin subscription tracker
- ✅ Midnight token reset scheduler
- ✅ CORS-enabled REST endpoints

### HTML/CSS
- ✅ Mobile-responsive design
- ✅ Warm saffron + teal canteen theme
- ✅ Baloo 2 + Sora fonts (Indian aesthetic)
- ✅ Dark kitchen display
- ✅ Admin sidebar dashboard
- ✅ Bottom navigation for mobile
- ✅ Smooth animations + toast notifications

---

## 🛠 VS Code Tips

1. Install **Python extension** and **Live Server** extension
2. Open integrated terminal → run `python app.py`
3. Click the Flask URL in terminal (Ctrl+Click)
4. For Java: install **Extension Pack for Java**

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login | Login |
| GET | /api/menu | Get all menu items |
| GET | /api/recommendations | AI-based recommendations |
| POST | /api/order | Place order |
| PUT | /api/order/{id}/status | Update order status |
| GET | /api/orders | Get user's orders |
| GET | /api/orders/queue | Get kitchen queue |
| PUT | /api/menu/{id}/availability | Toggle item availability |
| POST | /api/wallet/topup | Add wallet balance |
| POST | /api/wallet/redeem | Redeem points |
| POST | /api/rate | Submit item ratings |
| GET | /api/analytics | Admin analytics data |
| GET | /api/forecast | Demand forecast |
| GET | /api/user | Get current user data |
| POST | /api/subscribe | Create tiffin subscription |
| POST | /api/group-cart | Create group cart |

---

## 🎓 Tech Stack Summary

| Technology | Version | Usage |
|------------|---------|-------|
| JavaScript | ES6+ | UI, Socket.io, Chart.js, LocalStorage |
| Python | 3.8+ | Flask REST API, Socket.io server, AI logic |
| Flask | 3.0 | Web framework |
| Flask-SocketIO | 5.3 | Real-time WebSocket events |
| Java | 11+ | Reports, Email, Token API, Scheduler |
| HTML5 | — | Semantic templates |
| CSS3 | — | Custom design system |
| Chart.js | 4.4 | Admin analytics charts |

---

Built with ❤️ for college canteen management
