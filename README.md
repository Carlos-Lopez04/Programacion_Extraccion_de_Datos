CREATE DATABASE pizza_ninja;
USE pizza_ninja;

-- 1. Customers
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(255)
);

-- 2. Employees
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Position VARCHAR(50),
    Phone VARCHAR(20)
);

-- 3. Pizzas
CREATE TABLE Pizzas (
    PizzaID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(6,2) NOT NULL
);

-- 4. Ingredients
CREATE TABLE Ingredients (
    IngredientID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- 5. Orders
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    EmployeeID INT,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(8,2),
    DeliveryAddress VARCHAR(255),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- 6. Order_Details
CREATE TABLE Order_Details (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    PizzaID INT,
    Quantity INT DEFAULT 1,
    Price DECIMAL(6,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (PizzaID) REFERENCES Pizzas(PizzaID)
);

-- 7. Pizza_Ingredients
CREATE TABLE Pizza_Ingredients (
    PizzaID INT,
    IngredientID INT,
    PRIMARY KEY (PizzaID, IngredientID),
    FOREIGN KEY (PizzaID) REFERENCES Pizzas(PizzaID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);

-- 8. Payments
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    PaymentMethod VARCHAR(50),
    Amount DECIMAL(8,2),
    PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 9. Delivery_Status
CREATE TABLE Delivery_Status (
    StatusID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    Status VARCHAR(50),
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 10. Promotions
CREATE TABLE Promotions (
    PromoID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    DiscountPercentage DECIMAL(5,2),
    StartDate DATE,
    EndDate DATE
);

-- Audit_Log para auditoría
CREATE TABLE Audit_Log (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    TableName VARCHAR(100),
    ActionType VARCHAR(10), -- INSERT, UPDATE, DELETE
    Details TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UserInfo VARCHAR(100)
);

show tables;
select * from audit_log;

-- TRIGGERS PARA LA TABLA DE AUDITORÍA

DELIMITER $$

-- Clientes
CREATE TRIGGER trg_after_insert_Customers
AFTER INSERT ON Customers
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Customers', 'INSERT', CONCAT('ID:', NEW.CustomerID, ', Name:', NEW.Name, ', Phone:', NEW.Phone, ', Address:', NEW.Address), USER());
END$$

CREATE TRIGGER trg_after_update_Customers
AFTER UPDATE ON Customers
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Customers', 'UPDATE', CONCAT('ID:', NEW.CustomerID, ', Name:', NEW.Name, ', Phone:', NEW.Phone, ', Address:', NEW.Address), USER());
END$$

CREATE TRIGGER trg_after_delete_Customers
AFTER DELETE ON Customers
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Customers', 'DELETE', CONCAT('ID:', OLD.CustomerID, ', Name:', OLD.Name, ', Phone:', OLD.Phone, ', Address:', OLD.Address), USER());
END$$

-- empleados

CREATE TRIGGER trg_after_insert_Employees
AFTER INSERT ON Employees
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Employees', 'INSERT', CONCAT('ID:', NEW.EmployeeID, ', Name:', NEW.Name, ', Position:', NEW.Position, ', Phone:', NEW.Phone), USER());
END$$

CREATE TRIGGER trg_after_update_Employees
AFTER UPDATE ON Employees
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Employees', 'UPDATE', CONCAT('ID:', NEW.EmployeeID, ', Name:', NEW.Name, ', Position:', NEW.Position, ', Phone:', NEW.Phone), USER());
END$$

CREATE TRIGGER trg_after_delete_Employees
AFTER DELETE ON Employees
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Employees', 'DELETE', CONCAT('ID:', OLD.EmployeeID, ', Name:', OLD.Name, ', Position:', OLD.Position, ', Phone:', OLD.Phone), USER());
END$$

DELIMITER $$

-- Pizzas
CREATE TRIGGER trg_after_insert_Pizzas
AFTER INSERT ON Pizzas
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Pizzas', 'INSERT', CONCAT('ID:', NEW.PizzaID, ', Name:', NEW.Name, ', Description:', NEW.Description, ', Price:', NEW.Price), USER());
END$$

CREATE TRIGGER trg_after_update_Pizzas
AFTER UPDATE ON Pizzas
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Pizzas', 'UPDATE', CONCAT('ID:', NEW.PizzaID, ', Name:', NEW.Name, ', Description:', NEW.Description, ', Price:', NEW.Price), USER());
END$$

CREATE TRIGGER trg_after_delete_Pizzas
AFTER DELETE ON Pizzas
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Pizzas', 'DELETE', CONCAT('ID:', OLD.PizzaID, ', Name:', OLD.Name, ', Description:', OLD.Description, ', Price:', OLD.Price), USER());
END$$

-- Ingredients
CREATE TRIGGER trg_after_insert_Ingredients
AFTER INSERT ON Ingredients
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Ingredients', 'INSERT', CONCAT('ID:', NEW.IngredientID, ', Name:', NEW.Name), USER());
END$$

CREATE TRIGGER trg_after_update_Ingredients
AFTER UPDATE ON Ingredients
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Ingredients', 'UPDATE', CONCAT('ID:', NEW.IngredientID, ', Name:', NEW.Name), USER());
END$$

CREATE TRIGGER trg_after_delete_Ingredients
AFTER DELETE ON Ingredients
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Ingredients', 'DELETE', CONCAT('ID:', OLD.IngredientID, ', Name:', OLD.Name), USER());
END$$

-- Orders
CREATE TRIGGER trg_after_insert_Orders
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Orders', 'INSERT', CONCAT('ID:', NEW.OrderID, ', CustomerID:', NEW.CustomerID, ', EmployeeID:', NEW.EmployeeID, ', TotalAmount:', NEW.TotalAmount, ', Address:', NEW.DeliveryAddress), USER());
END$$

CREATE TRIGGER trg_after_update_Orders
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Orders', 'UPDATE', CONCAT('ID:', NEW.OrderID, ', CustomerID:', NEW.CustomerID, ', EmployeeID:', NEW.EmployeeID, ', TotalAmount:', NEW.TotalAmount, ', Address:', NEW.DeliveryAddress), USER());
END$$

CREATE TRIGGER trg_after_delete_Orders
AFTER DELETE ON Orders
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Orders', 'DELETE', CONCAT('ID:', OLD.OrderID, ', CustomerID:', OLD.CustomerID, ', EmployeeID:', OLD.EmployeeID, ', TotalAmount:', OLD.TotalAmount, ', Address:', OLD.DeliveryAddress), USER());
END$$

-- Order_Details
CREATE TRIGGER trg_after_insert_OrderDetails
AFTER INSERT ON Order_Details
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Order_Details', 'INSERT', CONCAT('ID:', NEW.OrderDetailID, ', OrderID:', NEW.OrderID, ', PizzaID:', NEW.PizzaID, ', Quantity:', NEW.Quantity, ', Price:', NEW.Price), USER());
END$$

CREATE TRIGGER trg_after_update_OrderDetails
AFTER UPDATE ON Order_Details
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Order_Details', 'UPDATE', CONCAT('ID:', NEW.OrderDetailID, ', OrderID:', NEW.OrderID, ', PizzaID:', NEW.PizzaID, ', Quantity:', NEW.Quantity, ', Price:', NEW.Price), USER());
END$$

CREATE TRIGGER trg_after_delete_OrderDetails
AFTER DELETE ON Order_Details
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Order_Details', 'DELETE', CONCAT('ID:', OLD.OrderDetailID, ', OrderID:', OLD.OrderID, ', PizzaID:', OLD.PizzaID, ', Quantity:', OLD.Quantity, ', Price:', OLD.Price), USER());
END$$

-- Payments
CREATE TRIGGER trg_after_insert_Payments
AFTER INSERT ON Payments
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Payments', 'INSERT', CONCAT('ID:', NEW.PaymentID, ', OrderID:', NEW.OrderID, ', Method:', NEW.PaymentMethod, ', Amount:', NEW.Amount), USER());
END$$

CREATE TRIGGER trg_after_update_Payments
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Payments', 'UPDATE', CONCAT('ID:', NEW.PaymentID, ', OrderID:', NEW.OrderID, ', Method:', NEW.PaymentMethod, ', Amount:', NEW.Amount), USER());
END$$

CREATE TRIGGER trg_after_delete_Payments
AFTER DELETE ON Payments
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Payments', 'DELETE', CONCAT('ID:', OLD.PaymentID, ', OrderID:', OLD.OrderID, ', Method:', OLD.PaymentMethod, ', Amount:', OLD.Amount), USER());
END$$

-- Delivery_Status
CREATE TRIGGER trg_after_insert_DeliveryStatus
AFTER INSERT ON Delivery_Status
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Delivery_Status', 'INSERT', CONCAT('ID:', NEW.StatusID, ', OrderID:', NEW.OrderID, ', Status:', NEW.Status), USER());
END$$

CREATE TRIGGER trg_after_update_DeliveryStatus
AFTER UPDATE ON Delivery_Status
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Delivery_Status', 'UPDATE', CONCAT('ID:', NEW.StatusID, ', OrderID:', NEW.OrderID, ', Status:', NEW.Status), USER());
END$$

CREATE TRIGGER trg_after_delete_DeliveryStatus
AFTER DELETE ON Delivery_Status
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Delivery_Status', 'DELETE', CONCAT('ID:', OLD.StatusID, ', OrderID:', OLD.OrderID, ', Status:', OLD.Status), USER());
END$$

-- Promotions
CREATE TRIGGER trg_after_insert_Promotions
AFTER INSERT ON Promotions
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Promotions', 'INSERT', CONCAT('ID:', NEW.PromoID, ', Name:', NEW.Name, ', Discount:', NEW.DiscountPercentage, ', Dates:', NEW.StartDate, '-', NEW.EndDate), USER());
END$$

CREATE TRIGGER trg_after_update_Promotions
AFTER UPDATE ON Promotions
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Promotions', 'UPDATE', CONCAT('ID:', NEW.PromoID, ', Name:', NEW.Name, ', Discount:', NEW.DiscountPercentage, ', Dates:', NEW.StartDate, '-', NEW.EndDate), USER());
END$$

CREATE TRIGGER trg_after_delete_Promotions
AFTER DELETE ON Promotions
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(TableName, ActionType, Details, UserInfo)
    VALUES('Promotions', 'DELETE', CONCAT('ID:', OLD.PromoID, ', Name:', OLD.Name, ', Discount:', OLD.DiscountPercentage, ', Dates:', OLD.StartDate, '-', OLD.EndDate), USER());
END$$

DELIMITER ;
--

# insercion

-- Customers
INSERT INTO Customers (Name, Phone, Address) VALUES ('Olivia Cervántez', '(795)596-7587', 'Circuito Senegal 808 Edif. 330 , Depto. 153, San Renato los altos, PUE 10980');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Andrés Tórrez', '(040)856-4586x29596', 'Avenida Eritrea 374 Edif. 574 , Depto. 541, San Beatriz los altos, NAY 28007');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Citlali Puga Valenzuela', '(041)531-4075', 'Circunvalación Gastélum 015 Interior 832, Nueva Sri Lanka, PUE 93880-8750');
INSERT INTO Customers (Name, Phone, Address) VALUES ('José Carlos Galindo', '068.931.7618', 'Prolongación Posada 901 Interior 780, San Carla los altos, DF 55203-3030');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Sr(a). Susana Luna', '1-868-460-6664x023', 'Circuito Puebla 216 023, Nueva Montenegro, YUC 18836');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Luis Miguel Natividad de la Crúz', '1-125-133-8806', 'Circuito Letonia 596 Interior 012, Vieja Maldivas, DF 87538-6234');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Sr(a). José Emilio Carrión', '(395)832-1590x30751', 'Retorno Durango 705 Edif. 140 , Depto. 471, Vieja Alemania, PUE 66886-5993');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Benjamín Karla Alfaro', '(230)391-6869x453', 'Circuito Distrito Federal 246 651, Nueva San Marino, ZAC 31498');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Sr(a). Irma Bonilla', '(917)053-3441x4352', 'Cerrada Rosas 998 Interior 320, Nueva Paraguay, ZAC 72261');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Mauricio Cordero Granados', '336.973.8961x9974', 'Retorno López 508 Interior 484, Vieja Marruecos, AGS 55601');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Nayeli Regalado Alcántar', '07647441190', 'Calzada Olvera 246 237, San Marco Antonio los bajos, SLP 81770');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Lucas Isaac Casárez Juárez', '317-033-8714x7720', 'Avenida Baja California Sur 652 Interior 353, San Ruby de la Montaña, PUE 51191-0624');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Elvira José María Puente Quintana', '1-858-805-2423x787', 'Retorno Zacatecas 615 355, San Luis Miguel los bajos, ZAC 33033');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Juan Frida Ortiz', '(058)152-9024x3859', 'Privada Nayarit 488 063, San María Cristina los altos, COAH 61154');
INSERT INTO Customers (Name, Phone, Address) VALUES ('Lic. Jonás Delgado', '09484822765', 'Calle Norte Rael 707 Interior 789, San Elsa de la Montaña, CHIH 66597');

-- Employees
INSERT INTO Employees (Name, Position, Phone) VALUES ('Raúl Olivera', 'Cajero', '1-159-311-0861x97609');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Ing. Marcela Flores', 'Cajero', '949.664.6769');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Natalia Alfredo Arenas Ojeda', 'Cocinero', '05557122186');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Joaquín José Manuél Valle', 'Repartidor', '1-477-323-0370x298');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Leonor Alonso', 'Gerente', '951.927.2157x80549');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Julio César Guevara', 'Cocinero', '(918)884-1064');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Fernanda Aideé Ayala', 'Repartidor', '(283)780-6260');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Ricardo Esteban Valerio', 'Cajero', '1-464-214-5786');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Dulce María Alanís', 'Cocinero', '188.127.0191');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Álvaro Guillén', 'Repartidor', '908-313-7543x344');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Arturo Lara Padilla', 'Gerente', '1-683-693-8036');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Marisol Contreras Aguirre', 'Cocinero', '293-726-8810');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Javier Vázquez', 'Cajero', '801-408-3982x060');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Adriana Ocampo', 'Gerente', '1-715-119-0280');
INSERT INTO Employees (Name, Position, Phone) VALUES ('Erick Domínguez', 'Repartidor', '1-229-960-6182x224');

-- Pizzas
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Pepperoni Especial 1', 'Deliciosa combinación de ingredientes artesanales.', 123.99);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Hawaiana Especial 2', 'Receta secreta con ingredientes frescos.', 137.49);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Barbacoa Especial 3', 'Perfecta para cualquier ocasión.', 110.50);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Carnes Frías Especial 4', 'Sabores intensos en cada bocado.', 149.00);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Pollo BBQ Especial 5', 'Receta tradicional mexicana.', 125.75);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Vegetariana Especial 6', 'Frescura de verduras seleccionadas.', 98.30);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Cuatro Quesos Especial 7', 'Cuatro quesos derretidos en armonía.', 112.60);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Mexicana Especial 8', 'Sabor picante y delicioso.', 130.25);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Pepperoni Especial 9', 'Con extra de pepperoni.', 119.90);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Hawaiana Especial 10', 'Clásica con piña y jamón.', 105.40);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Barbacoa Especial 11', 'Carnes jugosas y salsa BBQ.', 140.99);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Carnes Frías Especial 12', 'Selección gourmet.', 132.80);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Pollo BBQ Especial 13', 'Ideal para compartir.', 117.60);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Vegetariana Especial 14', 'Opciones verdes saludables.', 100.00);
INSERT INTO Pizzas (Name, Description, Price) VALUES ('Cuatro Quesos Especial 15', 'Fusión de quesos europeos.', 144.20);

-- Ingredients
INSERT INTO Ingredients (Name) VALUES ('Queso');
INSERT INTO Ingredients (Name) VALUES ('Jamón');
INSERT INTO Ingredients (Name) VALUES ('Piña');
INSERT INTO Ingredients (Name) VALUES ('Pepperoni');
INSERT INTO Ingredients (Name) VALUES ('Salchicha');
INSERT INTO Ingredients (Name) VALUES ('Champiñones');
INSERT INTO Ingredients (Name) VALUES ('Pimiento');
INSERT INTO Ingredients (Name) VALUES ('Cebolla');
INSERT INTO Ingredients (Name) VALUES ('Aceitunas');
INSERT INTO Ingredients (Name) VALUES ('Pollo');
INSERT INTO Ingredients (Name) VALUES ('Carne molida');
INSERT INTO Ingredients (Name) VALUES ('Tocino');
INSERT INTO Ingredients (Name) VALUES ('Jalapeño');
INSERT INTO Ingredients (Name) VALUES ('Tomate');
INSERT INTO Ingredients (Name) VALUES ('Albahaca');

INSERT INTO Orders (CustomerID, EmployeeID, TotalAmount, DeliveryAddress) VALUES
(1, 1, 250.00, 'Calle 1, Tijuana'),
(2, 2, 130.00, 'Calle 2, Tijuana'),
(3, 3, 260.00, 'Calle 3, Tijuana'),
(4, 4, 140.00, 'Calle 4, Tijuana'),
(5, 5, 270.00, 'Calle 5, Tijuana'),
(6, 6, 150.00, 'Calle 6, Tijuana'),
(7, 7, 280.00, 'Calle 7, Tijuana'),
(8, 8, 160.00, 'Calle 8, Tijuana'),
(9, 9, 290.00, 'Calle 9, Tijuana'),
(10, 10, 170.00, 'Calle 10, Tijuana'),
(11, 11, 300.00, 'Calle 11, Tijuana'),
(12, 12, 180.00, 'Calle 12, Tijuana'),
(13, 13, 310.00, 'Calle 13, Tijuana'),
(14, 14, 190.00, 'Calle 14, Tijuana'),
(15, 15, 320.00, 'Calle 15, Tijuana');

INSERT INTO Order_Details (OrderID, PizzaID, Quantity, Price) VALUES
(1, 1, 2, 120.00),
(2, 2, 1, 130.00),
(3, 3, 2, 125.00),
(4, 4, 1, 140.00),
(5, 5, 2, 115.00),
(6, 6, 1, 135.00),
(7, 7, 2, 130.00),
(8, 8, 1, 150.00),
(9, 9, 2, 145.00),
(10, 10, 1, 125.00),
(11, 11, 2, 160.00),
(12, 12, 1, 135.00),
(13, 13, 2, 150.00),
(14, 14, 1, 140.00),
(15, 15, 2, 130.00);

INSERT INTO Pizza_Ingredients (PizzaID, IngredientID) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 2), (2, 4),
(3, 1), (3, 2), (3, 5), (3, 6),
(4, 1), (4, 7), (4, 8), (4, 9),
(5, 1), (5, 2), (5, 10), (5, 11), (5, 12),
(6, 1), (6, 2), (6, 13), (6, 14),
(7, 1), (7, 2), (7, 15),
(8, 1), (8, 2), (8, 12),
(9, 1), (9, 2), (9, 4), (9, 5),
(10, 1), (10, 2), (10, 12),
(11, 1), (11, 2), (11, 3), (11, 4), (11, 5),
(12, 1), (12, 2), (12, 4), (12, 3),
(13, 1), (13, 2), (13, 4), (13, 12), (13, 10),
(14, 1), (14, 2), (14, 4), (14, 11),
(15, 1), (15, 2), (15, 11);

INSERT INTO Payments (OrderID, PaymentMethod, Amount) VALUES
(1, 'Efectivo', 250.00),
(2, 'Tarjeta', 130.00),
(3, 'Efectivo', 260.00),
(4, 'Tarjeta', 140.00),
(5, 'Efectivo', 270.00),
(6, 'Tarjeta', 150.00),
(7, 'Efectivo', 280.00),
(8, 'Tarjeta', 160.00),
(9, 'Efectivo', 290.00),
(10, 'Tarjeta', 170.00),
(11, 'Efectivo', 300.00),
(12, 'Tarjeta', 180.00),
(13, 'Efectivo', 310.00),
(14, 'Tarjeta', 190.00),
(15, 'Tarjeta', 160.00);

INSERT INTO Delivery_Status (OrderID, Status, UpdatedAt) VALUES
(1, 'En camino', '2025-05-01 13:00:00'),
(2, 'Entregado', '2025-05-01 14:30:00'),
(3, 'En preparación', '2025-05-01 14:45:00'),
(4, 'Entregado', '2025-05-01 15:00:00'),
(5, 'Cancelado', '2025-05-01 15:15:00'),
(6, 'Entregado', '2025-05-01 15:30:00'),
(7, 'En camino', '2025-05-01 16:00:00'),
(8, 'Entregado', '2025-05-01 16:15:00'),
(9, 'Reprogramado', '2025-05-01 16:45:00'),
(10, 'Entregado', '2025-05-01 17:00:00'),
(11, 'En camino', '2025-05-01 17:15:00'),
(12, 'Entregado', '2025-05-01 17:30:00'),
(13, 'En preparación', '2025-05-01 17:45:00'),
(14, 'Entregado', '2025-05-01 18:00:00'),
(15, 'Entregado', '2025-05-01 18:15:00');

INSERT INTO Promotions (PromoID, Name, DiscountPercentage, StartDate, EndDate) VALUES
( 1,'2x1 en pizza Margarita', 50, '2025-05-01', '2025-05-07'),
( 2,'15% de descuento en Pepperoni', 15, '2025-05-01', '2025-05-07'),
( 3,'Hawaiana al 20% menos', 20, '2025-05-01', '2025-05-07'),
( 4,'Promo 4 Quesos - 10% OFF', 10, '2025-05-01', '2025-05-07'),
( 5,'Vegetariana saludable - 25% menos', 25, '2025-05-01', '2025-05-07'),
( 6,'Mexicana ardiente 10% menos', 10, '2025-05-01', '2025-05-07'),
( 7,'BBQ Pollo - 2x1 los martes', 50, '2025-05-01', '2025-05-31'),
( 8,'Mariscos 30% de descuento', 30, '2025-05-01', '2025-05-07'),
( 9,'Carnes Frías 10% menos', 10, '2025-05-01', '2025-05-07'),
( 10,'Champiñones a solo $99', 20, '2025-05-01', '2025-05-07');

show tables;

DELIMITER $$

-- Customers
CREATE PROCEDURE getAllCustomers()
BEGIN
    SELECT * FROM Customers;
END$$

CREATE PROCEDURE getCustomerById(IN p_CustomerID INT)
BEGIN
    SELECT * FROM Customers WHERE CustomerID = p_CustomerID;
END$$

CREATE PROCEDURE insertCustomer(
    IN p_Name VARCHAR(100),
    IN p_Phone VARCHAR(20),
    IN p_Address VARCHAR(255)
)
BEGIN
    INSERT INTO Customers(Name, Phone, Address) VALUES (p_Name, p_Phone, p_Address);
END$$

CREATE PROCEDURE updateCustomer(
    IN p_CustomerID INT,
    IN p_Name VARCHAR(100),
    IN p_Phone VARCHAR(20),
    IN p_Address VARCHAR(255)
)
BEGIN
    UPDATE Customers
    SET Name = p_Name, Phone = p_Phone, Address = p_Address
    WHERE CustomerID = p_CustomerID;
END$$

CREATE PROCEDURE deleteCustomer(IN p_CustomerID INT)
BEGIN
    DELETE FROM Customers WHERE CustomerID = p_CustomerID;
END$$


-- Employees
CREATE PROCEDURE getAllEmployees()
BEGIN
    SELECT * FROM Employees;
END$$

CREATE PROCEDURE getEmployeeById(IN p_EmployeeID INT)
BEGIN
    SELECT * FROM Employees WHERE EmployeeID = p_EmployeeID;
END$$

CREATE PROCEDURE insertEmployee(
    IN p_Name VARCHAR(100),
    IN p_Position VARCHAR(50),
    IN p_Phone VARCHAR(20)
)
BEGIN
    INSERT INTO Employees(Name, Position, Phone) VALUES (p_Name, p_Position, p_Phone);
END$$

CREATE PROCEDURE updateEmployee(
    IN p_EmployeeID INT,
    IN p_Name VARCHAR(100),
    IN p_Position VARCHAR(50),
    IN p_Phone VARCHAR(20)
)
BEGIN
    UPDATE Employees
    SET Name = p_Name, Position = p_Position, Phone = p_Phone
    WHERE EmployeeID = p_EmployeeID;
END$$

CREATE PROCEDURE deleteEmployee(IN p_EmployeeID INT)
BEGIN
    DELETE FROM Employees WHERE EmployeeID = p_EmployeeID;
END$$


-- Pizzas
CREATE PROCEDURE getAllPizzas()
BEGIN
    SELECT * FROM Pizzas;
END$$

CREATE PROCEDURE getPizzaById(IN p_PizzaID INT)
BEGIN
    SELECT * FROM Pizzas WHERE PizzaID = p_PizzaID;
END$$

CREATE PROCEDURE insertPizza(
    IN p_Name VARCHAR(100),
    IN p_Description TEXT,
    IN p_Price DECIMAL(6,2)
)
BEGIN
    INSERT INTO Pizzas(Name, Description, Price) VALUES (p_Name, p_Description, p_Price);
END$$

CREATE PROCEDURE updatePizza(
    IN p_PizzaID INT,
    IN p_Name VARCHAR(100),
    IN p_Description TEXT,
    IN p_Price DECIMAL(6,2)
)
BEGIN
    UPDATE Pizzas
    SET Name = p_Name, Description = p_Description, Price = p_Price
    WHERE PizzaID = p_PizzaID;
END$$

CREATE PROCEDURE deletePizza(IN p_PizzaID INT)
BEGIN
    DELETE FROM Pizzas WHERE PizzaID = p_PizzaID;
END$$


-- Ingredients
CREATE PROCEDURE getAllIngredients()
BEGIN
    SELECT * FROM Ingredients;
END$$

CREATE PROCEDURE getIngredientById(IN p_IngredientID INT)
BEGIN
    SELECT * FROM Ingredients WHERE IngredientID = p_IngredientID;
END$$

CREATE PROCEDURE insertIngredient(
    IN p_Name VARCHAR(100)
)
BEGIN
    INSERT INTO Ingredients(Name) VALUES (p_Name);
END$$

CREATE PROCEDURE updateIngredient(
    IN p_IngredientID INT,
    IN p_Name VARCHAR(100)
)
BEGIN
    UPDATE Ingredients SET Name = p_Name WHERE IngredientID = p_IngredientID;
END$$

CREATE PROCEDURE deleteIngredient(IN p_IngredientID INT)
BEGIN
    DELETE FROM Ingredients WHERE IngredientID = p_IngredientID;
END$$


-- Orders
CREATE PROCEDURE getAllOrders()
BEGIN
    SELECT * FROM Orders;
END$$

CREATE PROCEDURE getOrderById(IN p_OrderID INT)
BEGIN
    SELECT * FROM Orders WHERE OrderID = p_OrderID;
END$$

CREATE PROCEDURE insertOrder(
    IN p_CustomerID INT,
    IN p_EmployeeID INT,
    IN p_OrderDate DATETIME,
    IN p_TotalAmount DECIMAL(8,2),
    IN p_DeliveryAddress VARCHAR(255)
)
BEGIN
    INSERT INTO Orders(CustomerID, EmployeeID, OrderDate, TotalAmount, DeliveryAddress) 
    VALUES (p_CustomerID, p_EmployeeID, p_OrderDate, p_TotalAmount, p_DeliveryAddress);
END$$

CREATE PROCEDURE updateOrder(
    IN p_OrderID INT,
    IN p_CustomerID INT,
    IN p_EmployeeID INT,
    IN p_OrderDate DATETIME,
    IN p_TotalAmount DECIMAL(8,2),
    IN p_DeliveryAddress VARCHAR(255)
)
BEGIN
    UPDATE Orders
    SET CustomerID = p_CustomerID,
        EmployeeID = p_EmployeeID,
        OrderDate = p_OrderDate,
        TotalAmount = p_TotalAmount,
        DeliveryAddress = p_DeliveryAddress
    WHERE OrderID = p_OrderID;
END$$

CREATE PROCEDURE deleteOrder(IN p_OrderID INT)
BEGIN
    DELETE FROM Orders WHERE OrderID = p_OrderID;
END$$


-- Order_Details
CREATE PROCEDURE getAllOrderDetails()
BEGIN
    SELECT * FROM Order_Details;
END$$

CREATE PROCEDURE getOrderDetailById(IN p_OrderDetailID INT)
BEGIN
    SELECT * FROM Order_Details WHERE OrderDetailID = p_OrderDetailID;
END$$

CREATE PROCEDURE insertOrderDetail(
    IN p_OrderID INT,
    IN p_PizzaID INT,
    IN p_Quantity INT,
    IN p_Price DECIMAL(6,2)
)
BEGIN
    INSERT INTO Order_Details(OrderID, PizzaID, Quantity, Price) VALUES (p_OrderID, p_PizzaID, p_Quantity, p_Price);
END$$

CREATE PROCEDURE updateOrderDetail(
    IN p_OrderDetailID INT,
    IN p_OrderID INT,
    IN p_PizzaID INT,
    IN p_Quantity INT,
    IN p_Price DECIMAL(6,2)
)
BEGIN
    UPDATE Order_Details
    SET OrderID = p_OrderID,
        PizzaID = p_PizzaID,
        Quantity = p_Quantity,
        Price = p_Price
    WHERE OrderDetailID = p_OrderDetailID;
END$$

CREATE PROCEDURE deleteOrderDetail(IN p_OrderDetailID INT)
BEGIN
    DELETE FROM Order_Details WHERE OrderDetailID = p_OrderDetailID;
END$$


-- Pizza_Ingredients
CREATE PROCEDURE getAllPizzaIngredients()
BEGIN
    SELECT * FROM Pizza_Ingredients;
END$$

CREATE PROCEDURE getPizzaIngredientById(
    IN p_PizzaID INT,
    IN p_IngredientID INT
)
BEGIN
    SELECT * FROM Pizza_Ingredients 
    WHERE PizzaID = p_PizzaID AND IngredientID = p_IngredientID;
END$$

CREATE PROCEDURE insertPizzaIngredient(
    IN p_PizzaID INT,
    IN p_IngredientID INT
)
BEGIN
    INSERT INTO Pizza_Ingredients(PizzaID, IngredientID) VALUES (p_PizzaID, p_IngredientID);
END$$

CREATE PROCEDURE updatePizzaIngredient(
    IN p_PizzaID INT,
    IN p_IngredientID INT,
    IN p_NewIngredientID INT
)
BEGIN
    UPDATE Pizza_Ingredients
    SET IngredientID = p_NewIngredientID
    WHERE PizzaID = p_PizzaID AND IngredientID = p_IngredientID;
END$$

CREATE PROCEDURE deletePizzaIngredient(
    IN p_PizzaID INT,
    IN p_IngredientID INT
)
BEGIN
    DELETE FROM Pizza_Ingredients WHERE PizzaID = p_PizzaID AND IngredientID = p_IngredientID;
END$$


-- Payments
CREATE PROCEDURE getAllPayments()
BEGIN
    SELECT * FROM Payments;
END$$

CREATE PROCEDURE getPaymentById(IN p_PaymentID INT)
BEGIN
    SELECT * FROM Payments WHERE PaymentID = p_PaymentID;
END$$

CREATE PROCEDURE insertPayment(
    IN p_OrderID INT,
    IN p_PaymentMethod VARCHAR(50),
    IN p_Amount DECIMAL(8,2),
    IN p_PaymentDate DATETIME
)
BEGIN
    INSERT INTO Payments(OrderID, PaymentMethod, Amount, PaymentDate) 
    VALUES (p_OrderID, p_PaymentMethod, p_Amount, p_PaymentDate);
END$$

CREATE PROCEDURE updatePayment(
    IN p_PaymentID INT,
    IN p_OrderID INT,
    IN p_PaymentMethod VARCHAR(50),
    IN p_Amount DECIMAL(8,2),
    IN p_PaymentDate DATETIME
)
BEGIN
    UPDATE Payments
    SET OrderID = p_OrderID,
        PaymentMethod = p_PaymentMethod,
        Amount = p_Amount,
        PaymentDate = p_PaymentDate
    WHERE PaymentID = p_PaymentID;
END$$

CREATE PROCEDURE deletePayment(IN p_PaymentID INT)
BEGIN
    DELETE FROM Payments WHERE PaymentID = p_PaymentID;
END$$


-- Delivery_Status
CREATE PROCEDURE getAllDeliveryStatus()
BEGIN
    SELECT * FROM Delivery_Status;
END$$

CREATE PROCEDURE getDeliveryStatusById(IN p_StatusID INT)
BEGIN
    SELECT * FROM Delivery_Status WHERE StatusID = p_StatusID;
END$$

CREATE PROCEDURE insertDeliveryStatus(
    IN p_OrderID INT,
    IN p_Status VARCHAR(50),
    IN p_UpdatedAt DATETIME
)
BEGIN
    INSERT INTO Delivery_Status(OrderID, Status, UpdatedAt) VALUES (p_OrderID, p_Status, p_UpdatedAt);
END$$

CREATE PROCEDURE updateDeliveryStatus(
    IN p_StatusID INT,
    IN p_OrderID INT,
    IN p_Status VARCHAR(50),
    IN p_UpdatedAt DATETIME
)
BEGIN
    UPDATE Delivery_Status
    SET OrderID = p_OrderID,
        Status = p_Status,
        UpdatedAt = p_UpdatedAt
    WHERE StatusID = p_StatusID;
END$$

CREATE PROCEDURE deleteDeliveryStatus(IN p_StatusID INT)
BEGIN
    DELETE FROM Delivery_Status WHERE StatusID = p_StatusID;
END$$


-- Promotions
CREATE PROCEDURE getAllPromotions()
BEGIN
    SELECT * FROM Promotions;
END$$

CREATE PROCEDURE getPromotionById(IN p_PromoID INT)
BEGIN
    SELECT * FROM Promotions WHERE PromoID = p_PromoID;
END$$

CREATE PROCEDURE insertPromotion(
    IN p_Name VARCHAR(100),
    IN p_DiscountPercentage DECIMAL(5,2),
    IN p_StartDate DATE,
    IN p_EndDate DATE
)
BEGIN
    INSERT INTO Promotions(Name, DiscountPercentage, StartDate, EndDate)
    VALUES (p_Name, p_DiscountPercentage, p_StartDate, p_EndDate);
END$$

CREATE PROCEDURE updatePromotion(
    IN p_PromoID INT,
    IN p_Name VARCHAR(100),
    IN p_DiscountPercentage DECIMAL(5,2),
    IN p_StartDate DATE,
    IN p_EndDate DATE
)
BEGIN
    UPDATE Promotions
    SET Name = p_Name,
        DiscountPercentage = p_DiscountPercentage,
        StartDate = p_StartDate,
        EndDate = p_EndDate
    WHERE PromoID = p_PromoID;
END$$

CREATE PROCEDURE deletePromotion(IN p_PromoID INT)
BEGIN
    DELETE FROM Promotions WHERE PromoID = p_PromoID;
END$$

DELIMITER ;
