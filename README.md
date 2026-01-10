# **Library Management System**

A **console-based Library Management System** implemented in Python that handles **students, books, issued books, fines, and user authentication**. This system allows **Admin** and **Student** users to perform specific actions with professional formatting and functionalities.<br><br>

---

## **Table of Contents**

- [Features](#features)  
- [Installation](#installation)  
- [Files & Structure](#files--structure)  
- [How to Run](#how-to-run)  
- [System Modules](#system-modules)  
  - [Admin Modules](#admin-modules)  
  - [Student Modules](#student-modules)  
- [CSV Data Structure](#csv-data-structure)  
- [Notes](#notes)  

---

## **Features**

**Admin Features**<br>
- Manage students: Add, view, delete students  
- Manage books: Add, view, delete books  
- Manage fines: View, update fines and rents  
- Password management: Change own or student passwords  
- View student status and allocated books  
- Block students automatically if fine > 1000  

**Student Features**<br>
- Login and view personal details (except password)  
- View available books  
- Request and return books  
- View allotted books with overdue highlights  
- View fines and status (Blocked/Regular)  
- Change own password  

**Automatic System Features**<br>
- Fine calculation based on overdue days  
- Rent calculation per day  
- Automatic update of student status based on fine amount  
- CSV-based storage for persistence  
- Console-based interactive menus with formatted output  

---

## **Installation**

1. Ensure you have **Python 3.x** installed on your system.<br>
2. Download the project files including all `.py` and `.csv` files.<br>
3. No additional libraries are required (built-in modules used).<br>

---

## **Files & Structure**

- `library_system.py` : Main Python file with all modules.<br>
- `students.csv` : Stores student records.<br>
- `books.csv` : Stores book records.<br>
- `issued_books.csv` : Stores issued book details.<br>
- `fine.csv` : Stores fines and rent details.<br>
- `admin.csv` : Stores admin username and password.<br>

---

## **How to Run**

1. Open terminal/command prompt.<br>
2. Navigate to the folder containing `library_system.py`.<br>
3. Run the program:  

```bash
python library_system.py

