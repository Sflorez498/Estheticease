import mysql.connector
from app.database.Clever_MySQL_conn import mysqlConn

def check_tables():
    try:
        cursor = mysqlConn.cursor()
        
        # Verificar tabla servicios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INT AUTO_INCREMENT PRIMARY KEY,
                nombre_servicio VARCHAR(100) NOT NULL,
                duracion_minutos INT NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Verificar tabla empleados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                especialidad VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Verificar tabla citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id_cita INT AUTO_INCREMENT PRIMARY KEY,
                id_cliente INT NOT NULL,
                id_empleado INT NOT NULL,
                id_servicio INT NOT NULL,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estado VARCHAR(20) DEFAULT 'Pendiente',
                notas TEXT,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
                FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
            )
        ''')
        
        # Verificar si hay datos de prueba
        cursor.execute("SELECT COUNT(*) FROM servicios")
        servicios_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM empleados")
        empleados_count = cursor.fetchone()[0]
        
        print(f"Tablas verificadas y creadas si no existían")
        print(f"Número de servicios: {servicios_count}")
        print(f"Número de empleados: {empleados_count}")
        
        mysqlConn.commit()
        
    except mysql.connector.Error as e:
        print(f"Error MySQL: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    check_tables()
