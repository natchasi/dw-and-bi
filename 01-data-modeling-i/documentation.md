# Data modeling
1. สำรวจและทำความเข้าใจความสัมพันธ์ข้อมูลจาก file.json
2. ออกแบบ data model ด้วยรูปแบบ relational database -> มีทั้งหมด 3 ตาราง ดังนี้
   2.1) actors 
         4 column -> id(PK), login, display, url
   2.2) repositories
         3 columns -> id(PK), name, actor_id(FK)
   2.3) events
         5 columns -> id(PK), type, actor_id(FK), repo_id(FK), create_at

ซึ่งแต่ละตารางมีความสัมพันธ์กัน คือ actors สามารถมีได้หลาย events และหลาย repositories 
โดยที่แต่ละ repositories สามารถมีได้หลาย events

3. เรียกใช้ container ด้วยการ run docker compose เพื่อเข้าสู่ web server ของ database
4. สร้างตารางตามที่ได้ออกแบบ model ไว้ในไฟล์ create_table.py
5. จัดการกับข้อมูลด้วยการ insert ข้อมูลที่อ้างอิงจาก file.json ที่ไฟล์ etl.py 
6. ทำการทดสอบ database บน web server (Postgres)