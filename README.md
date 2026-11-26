# docker-compose-expense# 💰 Docker Compose 記帳全端 API 系統 (FastAPI + PostgreSQL)

這是一個基於 **Docker Compose** 的多容器架構練習專案，整合 **Python FastAPI** 後端服務與 **PostgreSQL 16** 關聯式資料庫。重點展示多容器編排、服務健康檢查（Healthcheck）、內部 DNS 網路通訊，以及透過 Docker Named Volume 實現資料庫資料持久化。

---

## 📁 專案結構

```text
docker-compose-expense/
├── .dockerignore          # 排除無用檔案
├── .env                   # 資料庫帳號密碼與環境設定
├── Dockerfile             # FastAPI 後端服務映像檔建置檔
├── docker-compose.yml     # 多容器服務編排與 Volume 設定
├── main.py                # FastAPI 應用程式與 SQLAlchemy 模型
├── requirements.txt       # Python 套件相依清單
└── README.md              # 專案說明與維運指令文件
```

---

## 🚀 快速啟動與部署

### 一鍵建置並啟動所有服務（API + PostgreSQL）

```bash
docker compose up -d --build
```

* **Swagger API 互動測試介面**：`http://localhost:8030/docs`
* **查詢所有記帳紀錄**：`http://localhost:8030/expenses`

---

## 🛠️ Docker Compose 常用維運指令

### 1. 狀態檢查與日誌監控
* **查看 Compose 管理的容器狀態：**
  ```bash
  docker compose ps
  ```
* **同時監看所有服務（API + DB）的即時日誌：**
  ```bash
  docker compose logs -f
  ```
* **僅查看單一服務（例如 `api`）的日誌：**
  ```bash
  docker compose logs -f api
  ```

### 2. 進入容器與資料庫除錯
* **進入後端 API 容器終端機：**
  ```bash
  docker compose exec api bash
  ```
* **直接進入 PostgreSQL 資料庫指令列（psql）：**
  ```bash
  docker compose exec db psql -U admin -d expense_db
  ```
  > 進入後可輸入 `\dt` 查看資料表、`SELECT * FROM expenses;` 查詢資料，輸入 `\q` 離開。

### 3. 停止與環境清理
* **停止並移除容器與網路（保留資料庫 Volume 資料）：**
  ```bash
  docker compose down
  ```
* **徹底停止並移除容器、網路，以及清空所有資料庫 Volume 資料：**
  ```bash
  docker compose down -v
  ```
* **查看本機所有 Docker Volumes：**
  ```bash
  docker volume ls
  ```