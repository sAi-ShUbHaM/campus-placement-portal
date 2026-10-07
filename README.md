### **# Campus Placement \& Internship Portal**



A three-tier, role-based web application for managing campus placement and internship activities between students, recruiters, and the placement cell.



##### **## Overview**



The Campus Placement \& Internship Portal provides a centralized platform where:



\* Students can create their profiles, view eligible job opportunities, apply for jobs, and track application status.

\* Recruiters can manage company profiles, create job postings, view eligible candidates, and update application statuses.

\* Placement Cell Administrators can approve or reject companies and job postings before they become visible to students.



The system also implements backend eligibility validation based on CGPA, department/branch, and graduation year.



##### **## Features**

##### 

###### **### Student**



\* Student registration and login

\* Student profile management

\* Branch, CGPA, graduation year and resume details

\* View approved job postings

\* Automatic eligibility checking

\* Eligibility explanation for unavailable jobs

\* Apply for eligible jobs

\* Duplicate application prevention

\* Track application status



###### **### Recruiter**



\* Recruiter registration and login

\* Company profile management

\* Create job postings

\* Specify:



&#x20; \* Minimum CGPA

&#x20; \* Eligible departments

&#x20; \* Graduation year

\* View applicants

\* Update candidate application status

\* Batch update application statuses



###### **### Placement Cell Admin**



\* Admin authentication

\* View pending companies

\* Approve/reject companies

\* View pending job postings

\* Approve/reject job postings

\* Control which companies and jobs become visible to students

\* Role-based access control



##### **## Application Statuses**



The portal supports the following application statuses:



\* APPLIED

\* SHORTLISTED

\* INTERVIEW

\* SELECTED

\* REJECTED



##### **## Eligibility System**



A student can apply for a job only when the required eligibility conditions are satisfied.



The backend checks:



1\. Student profile availability

2\. Minimum CGPA requirement

3\. Allowed department/branch

4\. Required graduation year

5\. Duplicate application status



Eligibility is enforced at the backend level, so users cannot bypass the restriction simply by directly accessing the application route.



##### **## Technology Stack**



###### **### Frontend**



\* HTML5

\* CSS3

\* JavaScript



###### **### Backend**



\* Python

\* Flask

\* Werkzeug



###### **### Database**



\* SQLite



###### **### Architecture**



The project follows a three-tier architecture:





Presentation Layer

&#x20;       ↓

HTML / CSS / JavaScript

&#x20;       ↓

Application Layer

&#x20;       ↓

Flask Routes / Business Logic / Authentication

&#x20;       ↓

Data Layer

&#x20;       ↓

SQLite Database





\## Project Structure





campus-placement-portal/

│

├── app.py

├── database.py

├── placement.db

├── create\_admin.py

├── requirements.txt

├── README.md

│

├── routes/

│   ├── \_\_init\_\_.py

│   ├── auth.py

│   ├── student.py

│   ├── recruiter.py

│   └── admin.py

│

├── templates/

│   ├── home.html

│   ├── login.html

│   ├── register.html

│   ├── student\_profile.html

│   ├── student\_dashboard.html

│   ├── recruiter\_company.html

│   ├── recruiter\_dashboard.html

│   ├── create\_job.html

│   ├── recruiter\_candidates.html

│   ├── admin\_dashboard.html

│   └── 403.html

│

└── static/

&#x20;   ├── css/

&#x20;   ├── style.css

&#x20;   └── theme.js





##### **## Installation**



###### **### 1. Clone the repository**





git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd campus-placement-portal





###### **### 2. Create a virtual environment**



Windows:





py -m venv venv





###### **### 3. Install dependencies**





\& ".\\venv\\Scripts\\python.exe" -m pip install -r requirements.txt





###### **### 4. Run the application**





\& ".\\venv\\Scripts\\python.exe" app.py





The application will start on the local Flask development server.



Open the displayed localhost address in your browser.



##### **## Demo Admin Account**



The project contains a demo administrator account for testing:





Email: admin@college.com

Password: admin123





\*\*This credential is for local/demo testing only and should not be used in a production deployment.\*\*



##### **## Testing Flow**



A complete placement workflow can be tested in the following order:





Recruiter Registration

&#x20;       ↓

Recruiter Creates Company Profile

&#x20;       ↓

Admin Approves Company

&#x20;       ↓

Recruiter Creates Job

&#x20;       ↓

Admin Approves Job

&#x20;       ↓

Eligible Student Sees Job

&#x20;       ↓

Student Applies

&#x20;       ↓

Recruiter Views Candidate

&#x20;       ↓

Recruiter Updates Application Status

&#x20;       ↓

Student Tracks Updated Status





##### **## Security \& Access Control**



The application implements role-based access control for:



\* Student routes

\* Recruiter routes

\* Admin routes



Unauthorized users attempting to access restricted functionality receive an appropriate access-denied response.



Backend validation is used for important actions such as job eligibility and application submission.



##### **## Future Improvements**



Possible future improvements include:



\* Email notifications

\* Resume file uploads

\* Advanced recruiter filtering

\* Interview scheduling

\* Placement statistics and analytics

\* Admin audit-log interface

\* Production database such as PostgreSQL

\* Deployment to a cloud platform

\* Improved frontend animations and UI customization



##### **## Project Purpose**



This project was developed as an academic web application to demonstrate:



\* Full-stack web development

\* Flask application development

\* Role-based authentication

\* Database management

\* Backend business logic

\* Eligibility validation

\* Multi-user workflows

\* Three-tier application architecture



