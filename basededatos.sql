-- Base de datos para Registro e Inicio de Sesión
CREATE DATABASE IF NOT EXISTS companero_de_viaje_db;
USE companero_de_viaje_db;

-- Tabla de usuarios (adaptada a la consigna y bonus)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero ENUM('Masculino','Femenino','Otro') DEFAULT 'Otro',
    terminos BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
