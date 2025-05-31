import mysql.connector

# Conexión a la base de datos local
mysqlConn = mysql.connector.connect(
    host='localhost',
    user='root',
<<<<<<< HEAD
    password='110011Sf',  # Asegúrate de que esta es la contraseña correcta del root
    database='Estheticease',
=======
    #password='110011Sf',  # Asegúrate de que esta es la contraseña correcta del root
    database='Estheticease1',
>>>>>>> Geral
    port=3306
)

# Crear el cursor
cleverCursor = mysqlConn.cursor()

