db.events.drop();
db.groups.drop();


db.events_types.drop()
db.events_types.insert({code:"course", name:"Curso"});
db.events_types.insert({code:"acamp", name:"Retiro"});
db.events_types.insert({code:"event", name:"Evento"});
db.events_types.insert({code:"meeting", name:"Reunião de Células"});



db.groups_types.drop()
db.groups_types.insert({code:"cell", name:"Célula"});
db.groups_types.insert({code:"network", name:"Rede"});
db.groups_types.insert({code:"sector", name:"Setor"})
db.groups_types.insert({code:"region", name:"Região"});
db.groups_types.insert({code:"satelite_church", name:"Congregação"});
db.groups_types.insert({code:"main_church", name:"Igreja Sede"});



db.roles.drop()
/* Courses roles */
db.roles.insert({code:"student", name:"Aluno"});
db.roles.insert({code:"teacher", name:"Professor"});

/* Group roles */
db.roles.insert({code:"visitor", name:"Visitante"})
db.roles.insert({code:"cell_member", name:"Membro em Célula"})
db.roles.insert({code:"host", name:"Anfitrião"});
db.roles.insert({code:"leader", name:"Lider"});



db.users.drop();
db.users.insert({
	"user_name" : "msantos.douglas@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Douglas", "last_name": "Morais"}
});
db.users.insert({
	"user_name" : "tatiele@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Tatiele", "last_name": "Morais"}
});
db.users.insert({
	"user_name" : "altair@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Altair", "last_name": "Souza"}
});
db.users.insert({
	"user_name" : "indaia@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Indaia", "last_name": "Souza"}
});
db.users.insert({
	"user_name" : "felipe@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Felipe", "last_name": "Maia"}
});
db.users.insert({
	"user_name" : "camila@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Camila", "last_name": "Maia"}
});
db.users.insert({
	"user_name" : "jose@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Jose", "last_name": "Silva"}
});

