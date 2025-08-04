# MIA Automation

Intelligent message processing and automation for business workflows.  
MIA uses AI to classify, extract, and route messages such as orders, RFQs, complaints, and invoices.

---

## Features

- **Smart Classification:** Automatically detects message type (Order, RFQ, Complaint, Invoice).
- **AI Extraction:** Uses Gemini AI to extract product names, quantities, and customer info.
- **Automated Routing:** Routes messages to the correct backend service.
- **MongoDB Integration:** Stores and retrieves data for orders, stock, and invoices.
- **Modern Frontend:** Includes both a static HTML/CSS/JS frontend and a React app.

---

## Folder Structure

```
MIA/
├── backends/
│   ├── getInvoice.py
│   ├── getStock.py
│   ├── updateStock.py
│   └── writeToDB.py
├── frontend/
│   ├── index.html
│   ├── landing.html
│   ├── main.js
│   ├── style.css
│   └── mia-frontend/        # React app (created with Create React App)
│       ├── public/
│       ├── src/
│       ├── package.json
│       └── ...
├── app.py
├── classifier.py
├── jsonAgent.py
├── pdfAgent.py
└── samples.txt
```

---

## Setup Instructions

### 1. **Backend**

- Install Python 3.10+ and MongoDB.
- Install dependencies:
  ```sh
  pip install flask pymongo python-dotenv google-generativeai requests
  ```
- Set up your `.env` file with your Gemini API key:
  ```
  GEMINI_API_KEY=your_key_here
  ```
- Start each backend service in a separate terminal:
  ```sh
  python backends/getStock.py
  python backends/writeToDB.py
  python backends/getInvoice.py
  python backends/updateStock.py
  python classifier.py
  python jsonAgent.py
  python pdfAgent.py
  ```

### 2. **Frontend (Static HTML/JS/CSS)**

- Open `frontend/landing.html` for the landing page.
- Open `frontend/index.html` for the main app.
- Or serve the `frontend` folder using a simple HTTP server:
  ```sh
  cd frontend
  python -m http.server 8080
  ```

### 3. **Frontend (React App)**

- Go to the React app folder:
  ```sh
  cd frontend/mia-frontend
  ```
- Install dependencies:
  ```sh
  npm install
  ```
- Start the React app:
  ```sh
  npm start
  ```
- Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Usage

- Paste a sample message (see `samples.txt`) into the app.
- Click **Process Message**.
- View the step-by-step status and extracted data.

  <img width="1909" height="905" alt="Screenshot 2025-08-05 004659" src="https://github.com/user-attachments/assets/3c5efe92-f177-4032-b18d-2d2badbe212b" />
  <img width="1888" height="896" alt="Screenshot 2025-08-05 004718" src="https://github.com/user-attachments/assets/58108766-cf1b-4774-a4e7-204df29728c8" />
  <img width="1914" height="903" alt="Screenshot 2025-08-05 004536" src="https://github.com/user-attachments/assets/3c4cc3ce-a338-4f04-baa2-0b235bb0ca50" />
