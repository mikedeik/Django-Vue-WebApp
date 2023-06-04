# Μέλη ομάδας 6
- ΔΕΙΚΤΑΚΗΣ ΜΙΧΑΗΛ 1115200800018
- ΚΟΝΟΜΗ ΜΑΡΙΝΑ 1115201700054
- ΝΤΥΡΚΑΪ ΑΛΕΞΑΝΔΡΟΣ 1115201300220
- ΤΟΥΛΙΟΣ ΜΑΤΘΑΙΟΣ 1115201000170
- ΨΑΡΡΟΣ ΙΩΑΝΝΗΣ 1115201800216

BACKEND:
cd backend

Install Packages:
1) pip install django
2) pip install djangorestframework
3) pip install geopy
4) sudo apt-get install binutils libproj-dev gdal-bin
5) pip install channels
6) pip install daphne
7) python3 -m pip install channels_redis

pip install djangorestframework-simplejwt

Run Server:
sudo docker run -p 6379:6379 -d redis:5
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
