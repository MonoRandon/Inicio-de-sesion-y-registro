-- Base de datos para Compañero de Viaje
CREATE DATABASE IF NOT EXISTS companero_de_viaje_db;
USE companero_de_viaje_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de viajes
CREATE TABLE IF NOT EXISTS viajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destino VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_de_viaje_desde DATE NOT NULL,
    fecha_de_viaje_a DATE NOT NULL,
    usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de usuarios_unidos (usuarios que se unen a viajes de otros)
CREATE TABLE IF NOT EXISTS usuarios_unidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    viaje_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE
);
