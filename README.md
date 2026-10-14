# 🎓 Final Project - EduMate Website

> A comprehensive Academic Management System designed to simplify university administration through digital automation, featuring attendance tracking, course management, AI-powered recommendations, and role-based access.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![AWS](https://img.shields.io/badge/Hosted_on-AWS-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

EduMate is a Final Year Software Engineering project that digitizes academic management by providing a centralized platform for students, lecturers, and administrators.

The system streamlines attendance management, course administration, announcements, assignments, and academic activities while integrating machine learning to deliver personalized course recommendations.

---

# ✨ Key Features

## 👨‍🎓 Student

- Secure Login
- Student Dashboard
- View Courses
- Attendance Tracking
- Assignment Submission
- Notices & Announcements
- Timetable
- Course Recommendation
- Profile Management

## 👨‍🏫 Lecturer

- Manage Courses
- Mark Attendance
- Upload Assignments
- Grade Students
- View Reports
- Student Management

## 👨‍💼 Administrator

- User Management
- Department Management
- Course Management
- Academic Year Management
- Faculty Management
- Dashboard Analytics
- Reports
- System Configuration

---

# 🏗️ System Architecture


[![Architecture diagram of sahanhansaja026/final-project-edumate-website](https://gitdiagram.com/sahanhansaja026/final-project-edumate-website/diagram.png)](https://gitdiagram.com/sahanhansaja026/final-project-edumate-website?utm_source=readme&utm_medium=picture)


---

# 🛠 Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios

## Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic
- JWT Authentication
- Alembic
- Docker

## Database

- PostgreSQL

## Cloud Services

- AWS EC2
- AWS S3
- AWS RDS PostgreSQL

---

# 📁 Repository Structure

```
Final-Project-EduMate-Website/

├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# ⚙️ Backend Deployment

The backend is fully containerized using Docker and deployed on AWS.

Deployment architecture:

- Dockerized FastAPI application
- Hosted on AWS EC2
- PostgreSQL hosted using AWS RDS
- File uploads stored in AWS S3
- REST API consumed by the Next.js frontend

---

# 🚀 Local Installation

## Clone Repository

```bash
git clone https://github.com/sahanHansaja026/Final-Project-EduMate-Website.git

cd Final-Project-EduMate-Website
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Runs on

```
http://localhost:3000
```

---

# Backend Setup

```bash
cd backend

python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn app.main:app --reload
```

Runs on

```
http://localhost:8000
```

---

# 🐳 Docker

Build Docker image

```bash
docker build -t edumate-backend .
```

Run container

```bash
docker run -p 8000:8000 edumate-backend
```

---

# 🔐 Environment Variables

Backend

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_BUCKET_NAME=
```

Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

# 📸 Screenshots

Include screenshots such as:

```
docs/

home.png

login.png

dashboard.png

attendance.png

courses.png

admin-dashboard.png

student-dashboard.png

lecturer-dashboard.png
```

Example

```markdown
## Login

![Login](docs/login.png)

## Dashboard

![Dashboard](docs/dashboard.png)
```

---

# 🔄 API Flow

```
User

↓

Next.js Frontend

↓

FastAPI REST API

↓

JWT Authentication

↓

PostgreSQL Database

↓

AWS S3 Storage
```

---

# 🔒 Authentication

- JWT Authentication
- Role-based Authorization
- Protected Routes
- Secure Password Hashing
- Token Validation

---

# 📦 Major Modules

- Authentication
- User Management
- Student Management
- Lecturer Management
- Course Management
- Attendance Management
- Assignment Management
- Announcements
- Reports
- File Uploads
- AI Course Recommendation

---

# 📈 Future Improvements

- Mobile Application
- QR Attendance
- Push Notifications
- Real-time Chat
- Video Lecture Integration
- Analytics Dashboard
- AI Chatbot
- Online Examinations

---

# 👨‍💻 Developer

**Sahan Hansaja**

Software Engineering Undergraduate

GitHub

https://github.com/sahanHansaja026

---

# 📄 License

This project is developed for educational purposes as part of the BSc (Hons) Software Engineering Final Year Project.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
