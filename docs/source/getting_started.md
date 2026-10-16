# 🚀 Getting Started

Welcome to Rookie Route! This guide will help you get started with the platform.

## 🛠️ Installation

### Prerequisites

* Node.js (v24 or higher)
* Python 3.11+
* MySQL

### 1. Backend Setup

The run_server.bat script relies on a virtual environment named venv. 

Please follow these steps strictly.

```
# 1. Create a virtual environment in the root directory
python -m venv venv

# 2. Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
# Navigate to backend directory and install packages
cd app/backend
pip install -r requirements.txt

# 4. Configuration
# Create a .env file in the app/backend directory with your database config
```

### 2. Frontend Setup

```
# Navigate to frontend directory
cd app/frontend

# Install dependencies
npm install
```


## 🚀 Running the Application

### Option 1: One-Click Start (Recommended for Windows)

We provide a script to run both backend and frontend servers simultaneously.

1. Make sure you are in the project root directory.

2. Double-click run_server.bat or run it in the terminal:

```
./run_server.bat
```

3. Two command prompt windows will open automatically (one for Backend, one for Frontend).

### Option 2: Manual Start

If you are not using Windows or prefer running servers manually, use the following commands in separate terminals.

#### Terminal 1: Backend

```
# From the root directory
source venv/bin/activate  # (Windows: venv\Scripts\activate)
cd app/backend
uvicorn back_main:app --reload
```

#### Terminal 2: Frontend

```
# From the root directory
cd app/frontend
npm run dev
```


## ➡️ Next Steps

- Check out the [Usage Guide](usage.md) to learn how to use the platform
- Read about our [Features](about.md)
- Join our [Discord Community](https://discord.gg/qzEBPv6bAV)
