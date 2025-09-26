# Description

A lightweight, full-stack platform to visualize carbon footprint of missions for researchers.

---

## Features

- Role-based access (Admin, Manager, Researcher)  
- Create/edit missions with cities autocompletion using GeoNames
- Live map preview (Leaflet & OpenStreetMap)  
- Carbon footprint estimation and visualization
- Import & export missions using GESLab / GES1p5 formats

---

## Tech Stack

**Frontend:** Vue 3, Pinia, Bulma, Leaflet  
**Backend:** Django, Django REST Framework, MySQL, JWT, Swagger  
**Third-party:** GeoNames API, OpenStreetMap

---

## API Resources

| Resource       | Action           | ADMIN | MISSIONMANAGER | STANDARD |
|----------------|------------------|:-----:|:--------------:|:--------:|
| **users**      | List/View        | ✅    | ❌             | ❌        |
|                | Create           | ✅    | ❌             | ❌        |
|                | Update           | ✅    | ❌             | ❌        |
|                | Partial Update   | ✅    | ❌             | ❌        |
|                | Delete           | ✅    | ❌             | ❌        |
|                | Retrieve         | ✅    | ❌             | ❌        |
| **groups**     | List/View        | ✅    | ✅             | ✅        |
| **status**     | List/View        | ✅    | ✅             | ✅        |
| **employees**  | List/View        | ✅    | ✅             | ❌        |
|                | Create           | ✅    | ✅             | ❌        |
|                | Update           | ✅    | ✅             | ❌        |
|                | Partial Update   | ✅    | ✅             | ❌        |
|                | Retrieve         | ✅    | ✅             | ❌        |
| **transports** | List/View        | ✅    | ✅             | ✅        |
| **trips**      | List/View        | ❌    | ✅             | ✅        |
|                | Create           | ❌    | ✅             | ❌        |
|                | Update           | ❌    | ✅             | ❌        |
|                | Partial Update   | ❌    | ✅             | ❌        |
|                | Delete           | ❌    | ✅             | ❌        |
|                | Retrieve         | ❌    | ✅             | ✅        |
| **missions**   | List/View        | ❌    | ✅             | ✅        |
|                | Create           | ❌    | ✅             | ❌        |
|                | Update           | ❌    | ✅             | ❌        |
|                | Partial Update   | ❌    | ✅             | ❌        |
|                | Delete           | ❌    | ✅             | ❌        |
|                | Retrieve         | ❌    | ✅             | ✅        |

---

## Install

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

## Set up environment variables
To make sure the frontend can communicate with the backend, you need to configure two environment variables. These variables are required for the backend URL and GeoNames API credentials.

```bash
export VUE_APP_GEONAMES_USERNAME="your_geonames_username"
export VUE_APP_SERVER_URL="http://127.0.0.1:8000/"
```

- Replace `BACKEND_URL` with the actual URL where your Django backend is running.
- Example: If your Django backend is running locally on the default port, it will be `http://127.0.0.1:8000/`.