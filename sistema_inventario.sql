/* Creación de Tablas */
CREATE TABLE Productos ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100), 
    descripcion TEXT, 
    precio DECIMAL(10, 2), 
    stock INT 
); 
 
CREATE TABLE Proveedores ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100), 
    contacto VARCHAR(100), 
    telefono VARCHAR(15) 
); 
 
CREATE TABLE Compras ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    id_producto INT, 
    id_proveedor INT, 
    cantidad INT, 
    fecha DATE, 
    FOREIGN KEY (id_producto) REFERENCES Productos(id), 
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id) 
);

