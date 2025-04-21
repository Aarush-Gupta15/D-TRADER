# D‑Trader

A real‑time auction bidding platform where **sellers** can list items and **customers** can place live bids. Built with Flask, MySQL, and WebSockets, and deployed on AWS EC2 for high availability.

---

## 🚀 Features

- **Role‑Based Access**  
  - **Admin** — manage users and site settings  
  - **Seller** — upload products (name, description, category, price, image) and start auctions  
  - **Customer** — browse, search, filter, and place bids  
- **Real‑Time Bidding**  
  - Live updates via Socket.IO  
  - Maximum 5 bids per auction to keep things moving  
- **Leaderboard**  
  - Tracks top bidders in real time  
- **Responsive UI**  
  - Mobile‑friendly upload and bidding pages  
- **AWS Deployment**  
  - EC2 + Elastic IP for a stable endpoint  
  - Gunicorn as WSGI server, Nginx as reverse proxy (production‑grade setup)

---

## 🛠️ Tech Stack

| Component       | Technology               |
| --------------- | ------------------------ |
| Backend         | Python, Flask            |
| Real‑Time       | Socket.IO                |
| Database        | MySQL                    |
| Server‑Side WSGI| Gunicorn                 |
| Reverse Proxy   | Nginx                    |
| Hosting         | AWS EC2 + Elastic IP     |
| Frontend        | HTML, CSS, JavaScript    |

---

