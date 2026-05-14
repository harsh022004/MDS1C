# Post Office Finder (Google App Engine)

A professional web application built with Flask and deployed on Google App Engine. This tool allows users to find post office details (State, Name, Block, District) by entering a 6-digit Indian PIN code.

## 🚀 Features
- **Instant Lookup**: Fetch real-time data from the Indian Postal API.
- **Flask Backend**: Lightweight and efficient Python routing.
- **App Engine Ready**: Fully configured for Google Cloud Platform.
- **Responsive UI**: Clean design using standard CSS and HTML5.

## 🛠️ Project Structure
- `main.py`: The core Flask application logic and API handling.
- `app.yaml`: Configuration file for Google App Engine.
- `index.html`: The search interface.
- `results.html`: Displays the post office information.
- `requirements.txt`: List of Python dependencies (Flask, etc.).

---

## 💻 Local Development Setup

### 1. Prerequisites
- **Python 3.9 or higher** installed.
- **Google Cloud SDK (gcloud CLI)** installed.
- (Optional) A virtual environment.

### 2. Install Dependencies
Open your terminal in the project folder and run:
```powershell
pip install -r requirements.txt
```

### 3. Launching the App (Local Dev Server)
There are two ways to run this project locally:

#### **Method A: Using Google Cloud Dev Server (Recommended for GAE Testing)**
This mimics the App Engine environment.
1. Open the **Google Cloud SDK Shell** or your standard terminal.
2. Run the following command:
   ```powershell
   py "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\dev_appserver.py" app.yaml
   ```
3. Open your browser to: [http://localhost:8080](http://localhost:8080)

#### **Method B: Running Flask Directly**
Faster for quick UI/logic changes.
1. Run the script:
   ```powershell
   python main.py
   ```
2. Open your browser to: [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## ☁️ Deployment to Google Cloud
To deploy your application to the live internet:

1. **Initialize gcloud** (if not done already):
   ```powershell
   gcloud init
   ```
2. **Create an App Engine App** (if first time):
   ```powershell
   gcloud app create
   ```
3. **Deploy the project**:
   ```powershell
   gcloud app deploy
   ```
4. **View your live site**:
   ```powershell
   gcloud app browse
   ```

---

## 📝 Notes
- Ensure your `app.yaml` runtime matches your installed Python version (e.g., `python39` or `python310`).
- The application uses the [Postal PIN Code API](https://www.postalpincode.in/Api-Details) for data retrieval.
