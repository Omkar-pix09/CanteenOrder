"""
CanteenOrder - College Canteen Pre-Order System
Main Flask Application with Socket.io, REST API, AI features
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import random
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "canteen_secret_2024"
socketio = SocketIO(app, cors_allowed_origins="*")

MENU_ITEMS = [
    {"id": 1,  "name": "Vada Pav",       "price": 15, "category": "Snacks",    "emoji": "🫓", "available": True,  "cook_time": 3,  "rating": 4.5, "ratings_count": 120},
    {"id": 2,  "name": "Misal Pav",      "price": 45, "category": "Breakfast", "emoji": "🥘", "available": True,  "cook_time": 6,  "rating": 4.7, "ratings_count": 89},
    {"id": 3,  "name": "Pav Bhaji",      "price": 55, "category": "Meals",     "emoji": "🍛", "available": True,  "cook_time": 8,  "rating": 4.6, "ratings_count": 200},
    {"id": 4,  "name": "Masala Chai",    "price": 10, "category": "Drinks",    "emoji": "☕", "available": True,  "cook_time": 2,  "rating": 4.8, "ratings_count": 350},
    {"id": 5,  "name": "Samosa",         "price": 12, "category": "Snacks",    "emoji": "🥟", "available": True,  "cook_time": 2,  "rating": 4.4, "ratings_count": 180},
    {"id": 6,  "name": "Thali (Full)",   "price": 80, "category": "Meals",     "emoji": "🍱", "available": True,  "cook_time": 10, "rating": 4.9, "ratings_count": 150},
    {"id": 7,  "name": "Cold Coffee",    "price": 35, "category": "Drinks",    "emoji": "🧋", "available": True,  "cook_time": 3,  "rating": 4.3, "ratings_count": 95},
    {"id": 8,  "name": "Poha",           "price": 25, "category": "Breakfast", "emoji": "🍚", "available": True,  "cook_time": 5,  "rating": 4.6, "ratings_count": 110},
    {"id": 9,  "name": "Bread Omelette", "price": 30, "category": "Breakfast", "emoji": "🍳", "available": True,  "cook_time": 5,  "rating": 4.5, "ratings_count": 75},
    {"id": 10, "name": "Lassi",          "price": 25, "category": "Drinks",    "emoji": "🥛", "available": True,  "cook_time": 2,  "rating": 4.4, "ratings_count": 60},
    {"id": 11, "name": "Upma",           "price": 20, "category": "Breakfast", "emoji": "🫕", "available": True,  "cook_time": 6,  "rating": 4.2, "ratings_count": 55},
    {"id": 12, "name": "Paneer Frankie", "price": 50, "category": "Snacks",    "emoji": "🌯", "available": True,  "cook_time": 7,  "rating": 4.7, "ratings_count": 130},
]

USERS = {
    "student1": {"name": "Rahul Patil",   "password": "pass123", "role": "student", "wallet": 250, "points": 120, "order_history": []},
    "admin":    {"name": "Canteen Admin", "password": "admin123", "role": "admin",   "wallet": 0,   "points": 0,   "order_history": []},
    "kitchen":  {"name": "Kitchen Staff", "password": "kitchen1", "role": "kitchen", "wallet": 0,   "points": 0,   "order_history": []},
}

ORDERS = {}
TOKEN_COUNTER = [1]
SUBSCRIPTIONS = []
GROUP_CARTS = {}

SALES_DATA = {
    "today": {"revenue": 1240, "orders": 48, "items_sold": {"Vada Pav": 30, "Masala Chai": 45, "Thali (Full)": 12, "Pav Bhaji": 18, "Samosa": 22}},
    "peak_hours": {str(h): random.randint(2, 20) for h in range(8, 20)},
    "weekly": [850, 1100, 980, 1240, 1350, 800, 600],
}

def get_menu_item(item_id):
    return next((i for i in MENU_ITEMS if i["id"] == item_id), None)

def calculate_wait_time(order_items):
    queue_length = len([o for o in ORDERS.values() if o["status"] in ["confirmed", "cooking"]])
    max_cook = max((get_menu_item(i["id"])["cook_time"] for i in order_items if get_menu_item(i["id"])), default=5)
    return max_cook + (queue_length * 2)

def get_recommendations(username):
    hour = datetime.now().hour
    if 7 <= hour <= 10:
        preferred_cats = ["Breakfast", "Drinks"]
    elif 11 <= hour <= 14:
        preferred_cats = ["Meals", "Snacks"]
    else:
        preferred_cats = ["Snacks", "Drinks"]
    user_history = USERS.get(username, {}).get("order_history", [])
    ordered_ids = [item_id for order in user_history for item_id in order.get("item_ids", [])]
    freq = defaultdict(int)
    for iid in ordered_ids:
        freq[iid] += 1
    scored = []
    for item in MENU_ITEMS:
        if not item["available"]:
            continue
        score = item["rating"]
        if item["category"] in preferred_cats:
            score += 2
        score += freq.get(item["id"], 0) * 0.5
        scored.append((score, item))
    scored.sort(reverse=True)
    return [item for _, item in scored[:3]]

def generate_token():
    token = f"T{TOKEN_COUNTER[0]:03d}"
    TOKEN_COUNTER[0] += 1
    return token

def generate_order_id():
    return f"ORD{random.randint(10000,99999)}"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/menu")
def menu():
    if "username" not in session:
        return render_template("login.html")
    return render_template("menu.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/wallet")
def wallet():
    return render_template("wallet.html")

@app.route("/orders")
def my_orders():
    return render_template("orders.html")

@app.route("/rate/<order_id>")
def rate_order(order_id):
    return render_template("rate.html", order_id=order_id)

@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/menu-manager")
def menu_manager():
    return render_template("menu_manager.html")

@app.route("/admin/reports")
def reports():
    return render_template("reports.html")

@app.route("/admin/stock")
def stock_manager():
    return render_template("stock.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = USERS.get(username)
    if user and user["password"] == password:
        session["username"] = username
        return jsonify({"success": True, "role": user["role"], "name": user["name"]})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"success": True})

@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU_ITEMS)

@app.route("/api/recommendations", methods=["GET"])
def recommendations():
    username = session.get("username", "guest")
    recs = get_recommendations(username)
    return jsonify(recs)

@app.route("/api/order", methods=["POST"])
def place_order():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.json
    username = session["username"]
    user = USERS[username]
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "No items"}), 400
    total = sum(i["price"] * i["qty"] for i in items)
    use_wallet = data.get("use_wallet", False)
    if use_wallet:
        if user["wallet"] < total:
            return jsonify({"error": "Insufficient wallet balance"}), 400
        user["wallet"] -= total
    order_id = generate_order_id()
    token = generate_token()
    wait = calculate_wait_time(items)
    points_earned = int(total * 0.1)
    order = {
        "id": order_id, "token": token, "username": username,
        "items": items, "total": total, "status": "placed",
        "placed_at": datetime.now().isoformat(), "wait_time": wait,
        "paid_via": "wallet" if use_wallet else "counter",
        "points_earned": points_earned, "rating": None,
    }
    ORDERS[order_id] = order
    user["points"] = user.get("points", 0) + points_earned
    user["order_history"].append({"order_id": order_id, "item_ids": [{"id": i["id"]} for i in items]})
    SALES_DATA["today"]["revenue"] += total
    SALES_DATA["today"]["orders"] += 1
    hour = str(datetime.now().hour)
    SALES_DATA["peak_hours"][hour] = SALES_DATA["peak_hours"].get(hour, 0) + 1
    socketio.emit("new_order", order, room="kitchen")
    socketio.emit("order_update", {"order_id": order_id, "status": "placed", "token": token}, room=username)
    return jsonify({"success": True, "order": order})

@app.route("/api/order/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.json
    new_status = data.get("status")
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    order["status"] = new_status
    if new_status == "ready":
        order["ready_at"] = datetime.now().isoformat()
    socketio.emit("order_update", {"order_id": order_id, "status": new_status, "token": order["token"]}, broadcast=True)
    return jsonify({"success": True, "order": order})

@app.route("/api/orders", methods=["GET"])
def get_orders():
    username = session.get("username")
    user = USERS.get(username, {})
    if user.get("role") in ["admin", "kitchen"]:
        return jsonify(list(ORDERS.values()))
    return jsonify([o for o in ORDERS.values() if o["username"] == username])

@app.route("/api/orders/queue", methods=["GET"])
def get_queue():
    active = [o for o in ORDERS.values() if o["status"] in ["placed", "confirmed", "cooking"]]
    active.sort(key=lambda x: x["placed_at"])
    return jsonify(active)

@app.route("/api/menu/<int:item_id>/availability", methods=["PUT"])
def toggle_availability(item_id):
    item = get_menu_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    item["available"] = not item["available"]
    socketio.emit("menu_update", {"id": item_id, "available": item["available"]}, broadcast=True)
    return jsonify({"success": True, "item": item})

@app.route("/api/wallet/topup", methods=["POST"])
def topup_wallet():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Not logged in"}), 401
    amount = request.json.get("amount", 0)
    USERS[username]["wallet"] += amount
    return jsonify({"success": True, "balance": USERS[username]["wallet"]})

@app.route("/api/wallet/redeem", methods=["POST"])
def redeem_points():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Not logged in"}), 401
    user = USERS[username]
    points = request.json.get("points", 0)
    if user["points"] < points:
        return jsonify({"error": "Not enough points"}), 400
    rupees = points // 10
    user["points"] -= points
    user["wallet"] += rupees
    return jsonify({"success": True, "credited": rupees, "points_left": user["points"]})

@app.route("/api/rate", methods=["POST"])
def rate_item():
    data = request.json
    order_id = data.get("order_id")
    ratings = data.get("ratings", {})
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    order["rating"] = ratings
    for item_id_str, rating in ratings.items():
        item = get_menu_item(int(item_id_str))
        if item:
            total_r = item["rating"] * item["ratings_count"] + rating
            item["ratings_count"] += 1
            item["rating"] = round(total_r / item["ratings_count"], 1)
    return jsonify({"success": True})

@app.route("/api/analytics", methods=["GET"])
def analytics():
    return jsonify({
        "today": SALES_DATA["today"],
        "peak_hours": SALES_DATA["peak_hours"],
        "weekly": SALES_DATA["weekly"],
        "menu": MENU_ITEMS,
        "total_orders": len(ORDERS),
    })

@app.route("/api/forecast", methods=["GET"])
def forecast():
    items_sold = SALES_DATA["today"]["items_sold"]
    forecast_data = {name: int(count * 1.1) for name, count in items_sold.items()}
    return jsonify(forecast_data)

@app.route("/api/user", methods=["GET"])
def get_user():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Not logged in"}), 401
    u = USERS[username].copy()
    u.pop("password", None)
    u["username"] = username
    return jsonify(u)

@app.route("/api/subscribe", methods=["POST"])
def subscribe_tiffin():
    username = session.get("username")
    data = request.json
    sub = {
        "id": f"SUB{random.randint(1000,9999)}",
        "username": username,
        "items": data.get("items", []),
        "days": data.get("days", ["Mon","Tue","Wed","Thu","Fri"]),
        "time": data.get("time", "13:00"),
        "active": True,
        "created_at": datetime.now().isoformat(),
    }
    SUBSCRIPTIONS.append(sub)
    return jsonify({"success": True, "subscription": sub})

@app.route("/api/group-cart", methods=["POST"])
def create_group_cart():
    username = session.get("username")
    group_id = f"GRP{random.randint(10000,99999)}"
    GROUP_CARTS[group_id] = {"creator": username, "members": {username: []}, "created_at": datetime.now().isoformat()}
    return jsonify({"success": True, "group_id": group_id})

@app.route("/api/group-cart/<group_id>", methods=["GET"])
def get_group_cart(group_id):
    cart = GROUP_CARTS.get(group_id)
    if not cart:
        return jsonify({"error": "Group not found"}), 404
    return jsonify(cart)

@socketio.on("join")
def on_join(data):
    room = data.get("room", "general")
    join_room(room)
    emit("joined", {"room": room})

@socketio.on("kitchen_join")
def on_kitchen_join():
    join_room("kitchen")
    emit("joined", {"room": "kitchen"})

@socketio.on("user_join")
def on_user_join(data):
    username = data.get("username")
    if username:
        join_room(username)

@socketio.on("order_status_change")
def on_status_change(data):
    order_id = data.get("order_id")
    new_status = data.get("status")
    order = ORDERS.get(order_id)
    if order:
        order["status"] = new_status
        emit("order_update", {"order_id": order_id, "status": new_status, "token": order["token"]}, broadcast=True)

if __name__ == "__main__":
    print("CanteenOrder running at http://localhost:5000")
    socketio.run(app, debug=True, port=5000)
