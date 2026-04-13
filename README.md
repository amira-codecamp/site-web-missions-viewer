# 🌍 Carbon Footprint App

> A lightweight full-stack platform to visualize and analyze the carbon footprint of research missions for laboratories.
> 
---

## ✨ Features

- 🔐 Role-based access (Admin, Manager, Researcher)
- 🗺️ City autocomplete using GeoNames API
- 🌍 Live map visualization (Leaflet + OpenStreetMap)
- 📊 Carbon footprint estimation & visualization
- 📥 Import/export missions (GESLab / GES1p5 formats)

---

## 🛠 Tech Stack

**Frontend**
- Vue 3
- Pinia

**Backend**
- Django REST Framework
- MySQL
- JWT Authentication
- OpenAPI

**External Services**
- GeoNames API
- OpenStreetMap

---

## 🧩 API Resources

| Resource             | Operations | ADMIN | MANAGER | RESEARCHER      |
|----------------------|------------|:-----:|:-------:|:---------------:|
| User Accounts        | Full CRUD  | ✅    | ❌      | ❌               |
| Invited Researchers  | Full CRUD  | ✅    | ✅      | ❌               |
| Research Missions    | Full CRUD  | ❌    | ✅      | ✅ (own only)    |

---

## 📦 Install

```bash
# Backend
cd django_project
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Frontend
cd vue_project
npm install
npm run serve
```

## ⚙️ Environment Variables

You need to configure the required environment variables: backend URL (used by the frontend to access the API) and GeoNames API credentials.

```bash
export VUE_APP_GEONAMES_USERNAME="your_geonames_username"
export VUE_APP_SERVER_URL="http://127.0.0.1:8000/"
```

- Replace `BACKEND_URL` with the actual URL where your Django backend is running.
- If your Django backend is running locally on the default port, it will be `http://127.0.0.1:8000/`.
