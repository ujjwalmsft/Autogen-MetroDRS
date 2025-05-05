# 🚀 Run Metro Multi-Agent System Locally (Cross-Platform)
 
This guide walks you through setting up and running the project using Python 3.9–3.11 with Azure OpenAI.
 
---
 
## 🧰 Prerequisites
 
- Python 3.9, 3.10, or 3.11 installed

- [pip](https://pip.pypa.io/en/stable/installation/)

- [Git](https://git-scm.com/)

- Internet access

- Azure OpenAI resource with a deployed model (e.g., `gpt-35-turbo`)
 
---
 
## ⚙️ Setup Instructions
 
### 1. 📁 Clone the Repository (or unzip package)
 
```bash

git clone <your-repo-url>

cd MetroAgenticDemo

```
 
---
 
### 2. 🌍 Create .env File with Azure OpenAI Credentials
 
Create a `.env` file in the project root and add:
 
```env

AZURE_OPENAI_API_KEY=your-azure-key

AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo

AZURE_OPENAI_API_VERSION=2023-07-01-preview

```
 
---
 
## 💻 Run on macOS or Linux
 
```bash

# Create and activate virtual environment

python3.11 -m venv .venv

source .venv/bin/activate
 
# Install requirements

pip install -r requirements.txt
 
# Run the app

uvicorn app.main:app --reload

```
 
---
 
## 🪟 Run on Windows
 
```cmd

:: Create and activate virtual environment

python -m venv .venv

.venv\Scripts\activate
 
:: Install dependencies

pip install -r requirements.txt
 
:: Start the app

uvicorn app.main:app --reload

```
 
---
 
## 🌐 Access the Application
 
Open your browser and visit:
 
```
http://localhost:8000

```
 
You should see a simple form that allows you to simulate a metro train disruption and view the multi-agent system respond in real-time.
 
---
 
## 🧪 Troubleshooting
 
- Ensure your `.env` file is in the root directory and correctly formatted

- Use Python 3.9–3.11 (not 3.13)

- If `uvicorn` is not found, try: `python -m uvicorn app.main:app --reload`
 
---
 
## 📦 Ready to Deploy?
 
This system is fully compatible with:
 
- Azure App Service (Python)

- Azure Container Apps (Docker)

- GitHub Actions (CI/CD)

 