



pip freeze > requirements.txt           #crea y actualiza el requeriments 


.venv\Scripts\activate                   #Activa entorno virtual


python manage.py startapp "nombre"      #Crea nuevas Apps 


python manage.py runserver              #Corre el servidor local 


python manage.py makemigrations         #Actualiza la base de datos con nuevos campos 
python manage.py migrate                #Las migra definitivo 


python manage.py createsuperuser        #Crea Superusuarios 


python manage.py runserver 0.0.0.0:8000    #Permite conexiones externas



python manage.py flush
👉 Sirve para:
borrar TODOS los datos
mantener la estructura (tablas, campos, etc.)

