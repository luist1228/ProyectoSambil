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


create table EntradaP(
	id serial primary key,
	fkCamara int references Camara(id),
	sexo varchar(10),
	edad int,
	macAdd varchar(20),
	registroE timestamp
);


create table SalidaP(
	id serial primary key,
	fkCamara int references Camara(id),
	registroS timestamp,
	macAdd varchar(20)
);


create table Persona(
	id serial primary key,
	macAddres varchar(20),
	nombre varchar(20),
	apellido varchar(20)
);


create table Compra (
	id serial primary key,
	fkTienda int references Tienda(id),
	fkPersona int references Persona(id),
	fecha timestamp,
	total int
);


create table RegistroB(
	id serial primary key,
	macadd int references Persona(id),
	tiempoI timestamp,
	tiempoF timestamp
);


