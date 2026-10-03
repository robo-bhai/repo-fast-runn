# 🦇 BatVoice Django OTA Auto-Update Backend

Yeh Django backend BatVoice Android app ke in-app automatic update system ke liye banaya gaya hai.

---

## 🚀 Quick Setup & Run (Local Development)

### 1. Requirements Install Karein
```bash
cd django_backend
pip install -r requirements.txt
```

### 2. Database Migrations Run Karein
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Superuser (Admin) Banayein
```bash
python manage.py createsuperuser
```
*(Apna username, email aur password set karein)*

### 4. Server Start Karein
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📱 Naya Update Kaise Release Karein?

1. Browser mein Admin Panel open karein:
   `http://localhost:8000/admin/` (ya aapki live domain par `https://your-domain.com/admin/`)
2. **"App Release Versions"** par click karein aur **"Add App Release Version"** dabayein.
3. Form fill karein:
   - **Version Code:** `2` *(Installed version code `1` se bara hona chahiye)*
   - **Version Name:** `1.1.0`
   - **APK File:** Nayi signed APK file upload karein (`batvoice_v1.1.0.apk`)
   - **Release Notes:** Naye features bullet points mein likhein:
     ```text
     - ⚡ Extreme Turbo Fast Charging added
     - 🎙️ Custom Voice Studio updated
     - 🚀 Bug fixes & performance speedup
     ```
   - **Force Update:** Agar chahein ke user bina update kiye app na chala sake toh check karein.
   - **Is Active:** Checked rakhein.
4. **Save** par click karein!

---

## 🌐 BatVoice Android App Mein URL Kaise Set Karein?

1. Android phone mein **BatVoice** app open karein.
2. **Settings** tab mein jayein.
3. **"Auto-Updates & Server Sync"** card mein apna API URL enter karein:
   - *Local testing (same Wi-Fi):* `http://192.168.1.X:8000/api/check-update/`
   - *Live Production:* `https://your-domain.com/api/check-update/`
4. **"Save Server URL"** dabayein aur **"Check For Update"** par tap karein!
5. App automatically naya version detect karegi, changelog dikhayegi aur ek click par download kar ke install kar degi.

---

## ☁️ Free Hosting Options
Aap is Django app ko asani se host kar sakte hain:
- **PythonAnywhere.com** (Free / Beginners ke liye best)
- **Render.com** (Free Web Service)
- **Railway.app**
- **DigitalOcean / Hetzner / AWS Ubuntu VPS** (via Nginx + Gunicorn)
# repo-fast-runn
