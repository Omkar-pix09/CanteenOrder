// CanteenOrder — Shared JS Utilities

// ── CART MANAGEMENT (localStorage) ──
const Cart = {
  get() { return JSON.parse(localStorage.getItem('co_cart') || '[]'); },
  set(items) { localStorage.setItem('co_cart', JSON.stringify(items)); Cart.updateBadge(); },
  add(item) {
    const cart = Cart.get();
    const existing = cart.find(i => i.id === item.id);
    if (existing) existing.qty++;
    else cart.push({ ...item, qty: 1 });
    Cart.set(cart);
    Toast.show(`${item.emoji || '🍽'} ${item.name} added!`, 'success');
  },
  remove(itemId) {
    Cart.set(Cart.get().filter(i => i.id !== itemId));
  },
  updateQty(itemId, qty) {
    const cart = Cart.get();
    const item = cart.find(i => i.id === itemId);
    if (item) { if (qty <= 0) Cart.remove(itemId); else { item.qty = qty; Cart.set(cart); } }
  },
  clear() { Cart.set([]); },
  total() { return Cart.get().reduce((s, i) => s + i.price * i.qty, 0); },
  count() { return Cart.get().reduce((s, i) => s + i.qty, 0); },
  updateBadge() {
    const cnt = Cart.count();
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = cnt;
      el.style.display = cnt ? 'flex' : 'none';
    });
  }
};

// ── TOAST NOTIFICATIONS ──
const Toast = {
  container: null,
  init() {
    if (!document.getElementById('toast-container')) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById('toast-container');
    }
  },
  show(msg, type = 'default', duration = 3000) {
    if (!this.container) this.init();
    const icons = { success: '✓', error: '✕', warning: '⚠', default: 'ℹ' };
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<span style="font-size:16px">${icons[type] || icons.default}</span> ${msg}`;
    this.container.appendChild(t);
    setTimeout(() => {
      t.style.animation = 'fadeOut 0.3s ease forwards';
      setTimeout(() => t.remove(), 300);
    }, duration);
  }
};

// ── API HELPER ──
const API = {
  async get(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  async post(url, data) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },
  async put(url, data) {
    const res = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  }
};

// ── FORMAT HELPERS ──
const fmt = {
  currency: (n) => `₹${Number(n).toFixed(0)}`,
  time: (iso) => new Date(iso).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }),
  date: (iso) => new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }),
  stars: (r) => '★'.repeat(Math.round(r)) + '☆'.repeat(5 - Math.round(r)),
};

// ── STATUS HELPERS ──
const statusLabel = { placed: 'Order Placed', confirmed: 'Confirmed', cooking: 'Being Cooked', ready: 'Ready for Pickup', delivered: 'Delivered' };
const statusIcon  = { placed: '📋', confirmed: '✅', cooking: '👨‍🍳', ready: '🔔', delivered: '🎉' };

// ── COUNTDOWN TIMER ──
function startCountdown(seconds, el) {
  let remaining = seconds * 60;
  const tick = () => {
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    el.textContent = `${m}:${s.toString().padStart(2, '0')}`;
    if (remaining-- > 0) setTimeout(tick, 1000);
    else el.textContent = 'Ready!';
  };
  tick();
}

// ── POINTS METER ANIMATION ──
function animatePoints(el, target, max = 500) {
  const pct = Math.min((target / max) * 100, 100);
  el.style.width = '0%';
  setTimeout(() => {
    el.style.transition = 'width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)';
    el.style.width = pct + '%';
  }, 100);
}

// ── USER SESSION ──
const User = {
  async get() {
    try { return await API.get('/api/user'); } catch { return null; }
  },
  async refreshHeader() {
    const u = await this.get();
    if (!u) return;
    document.querySelectorAll('.nav-wallet').forEach(el => el.textContent = fmt.currency(u.wallet));
    document.querySelectorAll('.nav-points').forEach(el => el.textContent = `${u.points} pts`);
    document.querySelectorAll('.user-name').forEach(el => el.textContent = u.name);
  }
};

// Init on load
document.addEventListener('DOMContentLoaded', () => {
  Toast.init();
  Cart.updateBadge();
  User.refreshHeader();
});
