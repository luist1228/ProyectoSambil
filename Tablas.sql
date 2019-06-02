---------------------------------TABLAS---------------------------
------------------------------------------------------------------
create table Beacon(
	id serial primary key,
	modelo varchar(20)
);


create table Tienda(
	id serial primary key,
	nombre varchar(20),
	dueño varchar(20),
	horaA time,
	horaC time,
	fkBeacon int references Beacon(id) 
);


create table Entrada(
	id serial primary key,
	Abierto boolean
);


create table Mesa(
	id serial primary key,
	puestos int2,
	fkBeacon int references Beacon(id)
);


create table Camara(
	id serial primary key,
	fkEntrada int references Entrada(id),
	modelo varchar(20)
);


create table EntradaCC(
	id serial primary key,
	fkCamara int references Camara(id),
	sexo varchar(10),
	edad int,
	macAdd varchar(20),
	registroE timestamp
);


create table SalidaCC(
	id serial primary key,
	fkCamara int references Camara(id),
	registroS timestamp,
	macAdd varchar(20)
);


create table Persona(
	id serial primary key,
	macAddres varchar(20) unique,
	nombre varchar(20),
	apellido varchar(20)
);


create table Compra (
	id serial primary key,
	fkTienda int references Tienda(id),
	fkPersonaMac varchar(20) references Persona(macaddres),
	fecha timestamp,
	total int
);

create table RegistroT(
	id serial primary key,
	mac varchar(20),
	fkBeacon int references Beacon(id),
	fecha timestamp,
	io boolean 
);

create table RegistroM(
	id serial primary key,
	mac varchar(20),
	fkMesa int references Mesa(id),
	fecha timestamp,
	io boolean 
);

create table CompraEntrada (
	id serial primary key,
	fkCompra int references Compra(id),
	fechaEntrada timestamp 
);

