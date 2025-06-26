# 🌍 Mission Trip Manager

A lightweight, full-stack platform to manage missions and employee trips with city autocomplete and carbon tracking.

---

## 🚀 Features

- ✅ Role-based access (Admin, Manager, Employee)  
- ✅ Create/edit trips with city autocomplete (GeoNames)  
- ✅ Live map preview (Leaflet & OpenStreetMap)  
- ✅ Carbon footprint estimation  
- ✅ Model-based mission creation

---

## 🔧 Tech Stack

**Frontend:** Vue 3, Pinia, Bulma, Leaflet  
**Backend:** Django, Django REST Framework, MySQL, JWT  
**Third-party:** GeoNames API, OpenStreetMap

---

## 🔐 API Resources

| Resource     | List | Create | Update | Delete |
|--------------|:----:|:------:|:------:|:------:|
| `users`      | ✅   | ✅     | ✅     | ✅     |
| `groups`     | ✅   | ❌     | ❌     | ❌     |
| `status`     | ✅   | ❌     | ❌     | ❌     |
| `employees`  | ✅   | ❌     | ✅     | ❌     |
| `transports` | ✅   | ❌     | ❌     | ❌     |
| `trips`      | ✅   | ✅     | ✅     | ✅     |
| `missions`   | ✅   | ✅     | ✅     | ✅     |

---

## 📈 Roadmap

- ✅ Mission/trip models 
- ✅ GeoNames API integration  
- ✅ Map routing with Leaflet
- ✅ Carbon footprint calculation  
- ✅ Carbon footprint visualization
- ✅ Role-based permissions  
- ⬜ Import/export trips 
- ⬜ Anonymized user statistics   

---

## 🧪 Setup Instructions

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
./start.sh

## 🔗 Live Access

🧭 Project link: [https://depot.lipn.univ-paris13.fr/lacroix/sitewebmission](https://depot.lipn.univ-paris13.fr/lacroix/sitewebmission)