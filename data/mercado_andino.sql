DROP TABLE IF EXISTS ventas;
CREATE TABLE ventas (venta_id INTEGER PRIMARY KEY, fecha TEXT, cliente_id INTEGER, ciudad TEXT, categoria TEXT, canal TEXT, importe REAL, coste REAL);
INSERT INTO ventas VALUES
(1,'2026-01-05',1,'Neuquén','Hogar','Web',120,75),
(2,'2026-01-06',2,'Córdoba','Tecnología','Tienda',300,210),
(3,'2026-01-12',3,'Mendoza','Hogar','Web',80,45),
(4,'2026-01-16',1,'Neuquén','Tecnología','Tienda',250,180),
(5,'2026-02-02',4,'Córdoba','Hogar','Web',140,85),
(6,'2026-02-07',3,'Mendoza','Tecnología','Tienda',320,230),
(7,'2026-02-15',5,'Neuquén','Hogar','Web',100,60),
(8,'2026-02-22',2,'Córdoba','Tecnología','Web',200,145),
(9,'2026-03-04',6,'Mendoza','Hogar','Tienda',160,100),
(10,'2026-03-08',5,'Neuquén','Tecnología','Tienda',280,195),
(11,'2026-03-18',4,'Córdoba','Hogar','Tienda',90,55),
(12,'2026-03-26',6,'Mendoza','Tecnología','Web',400,280);
CREATE TABLE clientes (cliente_id INTEGER PRIMARY KEY, segmento TEXT);
INSERT INTO clientes VALUES (1,'Frecuente'),(2,'Frecuente'),(3,'Frecuente'),(4,'Ocasional'),(5,'Ocasional'),(6,'Ocasional');
