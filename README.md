# 🚚 Delivery Cost Tracker

A full-stack delivery tracking dashboard for calculating and managing delivery costs based on delivery duration and hourly rate. Built with **Flask** for the backend and **React** for the frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![MadeWith](https://img.shields.io/badge/Made%20with-React%20%26%20Flask-blue)

---

## 📌 Overview

**Delivery Cost Tracker** is a lightweight logistics dashboard to help operations teams and small businesses monitor deliveries, record working hours, calculate real-time costs, and visualize delivery activity—all from a simple UI.

### ✨ Key Features

- Add delivery records with driver ID, start/end time, and hourly rate
- Automatically calculates delivery duration and cost
- Displays total cost across all deliveries
- Responsive UI with clean table display
- REST API built with Flask + SQLAlchemy
- Minimal setup and extensible structure

---

## 🧰 Tech Stack

| Layer      | Tech Used              |
|------------|------------------------|
| Frontend   | React, JavaScript, Fetch API |
| Backend    | Flask, SQLAlchemy, Flask-CORS |
| Database   | SQLite (can be upgraded to PostgreSQL/MySQL) |
| Styling    | Inline CSS (customizable) |

---

## 📁 Project Structure

```
delivery-cost-tracker/
├── backend/
│   ├── main.py             # Flask application
│   ├── db.py               # DB engine and session setup
│   ├── models.py           # SQLAlchemy Delivery model
├── frontend/
│   └── src/
│       └── App.js          # React UI
├── README.md
├── requirements.txt
└── ...
```

---

## 🚀 Getting Started

### 1. 🔧 Backend Setup (Flask)

#### Prerequisites:
- Python 3.8+
- `pip` installed

```bash
# Clone repo
git clone https://github.com/lakkaramnaveen/delivery
cd delivery/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

Backend will run on: `http://127.0.0.1:5000`

---

### 2. 🖥️ Frontend Setup (React)

#### Prerequisites:
- Node.js (v16+)
- `npm` installed

```bash
cd ../frontend

# Install dependencies
npm install

# Start React app
npm start
```

Frontend will run on: `http://localhost:3000`

---

## 🌐 API Endpoints

| Method | Endpoint         | Description             |
|--------|------------------|-------------------------|
| GET    | `/deliveries`    | List all deliveries     |
| POST   | `/deliveries`    | Add a new delivery      |
| GET    | `/total-cost`    | Calculate total cost    |

> ⚠️ API expects `start_time` and `end_time` in ISO format (`YYYY-MM-DDTHH:MM:SS`)

---

## 🧪 Example Payload

### POST `/deliveries`

```json
{
  "driver_id": 1,
  "start_time": "2025-07-20T08:00:00",
  "end_time": "2025-07-20T12:00:00",
  "hourly_rate": 25.5
}
```

### Response
```json
{
  "message": "Delivery added successfully"
}
```

---

## 🧱 Future Improvements

- Edit/Delete delivery entries
- Duration + cost breakdown per delivery
- Auth system (e.g., JWT)
- Export to CSV
- Charts and graphs
- Test coverage

---

## 🤝 Contributing

We welcome contributions from the community!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a pull request

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Made with ❤️ by [Naveen](https://github.com/lakkaramnaveen)
