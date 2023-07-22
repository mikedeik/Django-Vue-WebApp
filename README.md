# Μέλη ομάδας 6
- ΔΕΙΚΤΑΚΗΣ ΜΙΧΑΗΛ 1115200800018
- ΚΟΝΟΜΗ ΜΑΡΙΝΑ 1115201700054
- ΝΤΥΡΚΑΪ ΑΛΕΞΑΝΔΡΟΣ 1115201300220
- ΤΟΥΛΙΟΣ ΜΑΤΘΑΙΟΣ 1115201000170
- ΨΑΡΡΟΣ ΙΩΑΝΝΗΣ 1115201800216

Read docs for more info

BACKEND:
cd backend
docker-compose up --build // builds a venv and runs the server

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
