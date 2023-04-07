# Μέλη ομάδας 6
- ΔΕΙΚΤΑΚΗΣ ΜΙΧΑΗΛ 1115200800018
- ΚΟΝΟΜΗ ΜΑΡΙΝΑ 1115201700054
- ΝΤΥΡΚΑΪ ΑΛΕΞΑΝΔΡΟΣ 1115201300220
- ΤΟΥΛΙΟΣ ΜΑΤΘΑΙΟΣ 1115201000170
- ΨΑΡΡΟΣ ΙΩΑΝΝΗΣ 1115201800216

BACKEND:
cd backend

Install Packages:
pip install django
pip install djangorestframework
pip install geopy
sudo apt-get install binutils libproj-dev gdal-bin

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
