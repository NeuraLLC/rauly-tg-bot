# Rauly Telegram Scraper & Analyzer

A professional Telegram UserBot for scanning public group admins, analyzing cross-project patterns, and discovering pre-TGE opportunities.

## 🚀 Features
- **Admin Extraction**: Identifies creators and admins in public groups.
- **Pattern Analysis**: Detects users who are admins across multiple crypto projects.
- **Pre-TGE Discovery**: Automated keyword-based search for upcoming listings and TGEs.
- **Google Sheets Integration**: Instant export of findings for research teams.
- **Production Ready**: Robust logging, rate-limit handling (FloodWait), and Docker support.

## 🛠️ Configuration
Create a `.env` file based on `.env.example`:
- `API_ID` / `API_HASH`: From [my.telegram.org](https://my.telegram.org).
- `PHONE_NUMBER`: Your Telegram account phone.
- `GOOGLE_SHEET_ID`: Target Google Sheet ID.
- `GOOGLE_SERVICE_ACCOUNT_FILE`: Path to your Service Account JSON.

## 📦 Deployment on Render (Paid Tier)
1. **Create a Private Repo**: Push this code to GitHub/GitLab.
2. **Connect to Render**:
   - Create a **Background Worker**.
   - Use the `Dockerfile` provided.
3. **Environment Variables**: Add your `.env` values to Render's environment settings.
4. **Persistent Disk**: Add a disk titled `rauly-data` mounted at `/app/sessions`. This preserves your Telegram login.
5. **Secret File**: Add your Google Service Account JSON through Render's "Secret Files" feature.

## 🏃 Usage (Local)
```bash
pip install -r requirements.txt
python main.py login   # First time setup
python main.py scan <link>  # Scan a group
python main.py report  # Analyze and export to Sheets
```
