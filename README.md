# 📊 YouTube Data Harvesting and Warehousing

A Streamlit-based data engineering application that extracts YouTube channel data using the YouTube Data API, stores it in MongoDB as a data lake, migrates structured data to MySQL, and provides analytical insights through SQL queries.

---

## 🚀 Project Overview

YouTube generates massive amounts of data related to channels, videos, playlists, and comments. Analyzing this data manually is difficult and time-consuming.

This project automates the process of collecting, storing, transforming, and analyzing YouTube data using a complete ETL (Extract, Transform, Load) pipeline.

Users can enter a YouTube Channel ID, fetch channel information using the YouTube Data API, store the data in MongoDB, migrate it to MySQL, and perform analytical queries through an interactive Streamlit dashboard.

---

## 🎯 Objectives

* Extract YouTube channel data using YouTube Data API v3.
* Store raw data in MongoDB (Data Lake).
* Transform and migrate data into MySQL (Data Warehouse).
* Perform SQL-based analytical queries.
* Provide an interactive dashboard for data exploration.

---

## ✨ Features

### Channel Data Collection

* Fetch channel details
* Retrieve playlist information
* Extract video metadata
* Collect video comments

### Data Lake (MongoDB)

* Store raw API responses
* Maintain flexible document structure
* Support multiple channel collections

### Data Warehouse (MySQL)

* Store structured data in relational tables
* Normalize channel, video, and comment data
* Enable SQL querying and analytics

### Analytics Dashboard

* View harvested channel information
* Execute predefined SQL queries
* Analyze channel performance metrics
* Explore video statistics and engagement

---

## 🏗️ Architecture

```text
YouTube Data API
        │
        ▼
 Python Data Extraction
        │
        ▼
 MongoDB Atlas
   (Data Lake)
        │
        ▼
 Data Transformation
        │
        ▼
 MySQL Database
 (Data Warehouse)
        │
        ▼
 Streamlit Dashboard
        │
        ▼
 Analytics & Insights
```

## 🛠️ Tech Stack

### Programming Language

* Python

### Frontend

* Streamlit

### Database

* MongoDB Atlas
* MySQL

### Libraries

* google-api-python-client
* pymongo
* mysql-connector-python
* pandas
* streamlit

### API

* YouTube Data API v3

---

## 📂 Database Schema

### Channels Table

| Column       |
| ------------ |
| Channel_ID   |
| Channel_Name |
| Subscribers  |
| Views        |
| Total_Videos |
| Description  |

### Videos Table

| Column         |
| -------------- |
| Video_ID       |
| Channel_ID     |
| Title          |
| Views          |
| Likes          |
| Comments       |
| Duration       |
| Published_Date |

### Comments Table

| Column         |
| -------------- |
| Comment_ID     |
| Video_ID       |
| Comment_Text   |
| Author         |
| Published_Date |

---

## 📈 Sample Analytical Queries

* Top 10 most viewed videos
* Channels with highest subscribers
* Videos with most likes
* Videos published in a specific year
* Average video duration per channel
* Most commented videos
* Channel-wise total video count
* Highest engagement videos

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/youtube-data-harvesting.git
cd youtube-data-harvesting
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create a file named:

```python
config.py
```

Add:

```python
API_KEY = "YOUR_YOUTUBE_API_KEY"
```

### Run Application

```bash
streamlit run app.py
```

---

## 📷 Screenshots

### Home Page

<img width="1920" height="1080" alt="home_youtube" src="https://github.com/user-attachments/assets/d0d6fe7f-abc8-49e0-9b3a-e6997fece3a5" />


### Channel Data Extraction

<img width="1920" height="1020" alt="fetch_data1" src="https://github.com/user-attachments/assets/6699f915-f91c-4279-ab20-af07aa64c616" />


### MongoDB Storage

<img width="1648" height="646" alt="Screenshot 2025-04-21 190138" src="https://github.com/user-attachments/assets/6cc2b05a-0387-4038-b03c-a3d66939d60b" />


### SQL Analytics Dashboard

<img width="1920" height="1020" alt="dashboard_youtube" src="https://github.com/user-attachments/assets/bee5d7ac-621f-489c-b78f-a282984ed72a" />


---

## 🔑 Key Learnings

* REST API Integration
* ETL Pipeline Development
* Data Warehousing Concepts
* MongoDB Data Modeling
* SQL Query Optimization
* Streamlit Dashboard Development
* Data Engineering Fundamentals

---

## 📌 Future Enhancements

* Real-time dashboard updates
* Advanced visualizations using Plotly
* Sentiment analysis on comments
* Channel comparison dashboard
* Export reports to Excel/PDF
* User authentication system

---

## 👨‍💻 Author

**Subramanian T**

MCA Graduate | Python Developer | AI & Data Enthusiast

LinkedIn: [www.linkedin.com/in/subramaniant2001](https://www.linkedin.com/in/subramanian-t-6b7b92255/)

GitHub: https://github.com/Subramanian638545
