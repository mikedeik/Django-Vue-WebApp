# texlo

BACKEND:
cd backend

Install Packages:
pip install django
pip install djangorestframework

Run Server:
py manage.py runserver

FRONTEND:
cd frontend

Install Packages:
yarn install

Run Server:
yarn dev

types

poi:
id,name,categoryID,nomos,perifereia,x,y,image(?),date of creation

category:
id,name

user:
id,username,password,role

notification:
id,text,userId,isRead

saved search:
id,userId,categoryId[],radius,date of creation
