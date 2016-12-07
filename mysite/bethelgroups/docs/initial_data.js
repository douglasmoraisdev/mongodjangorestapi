db.events.drop();
db.groups.drop();

/* Events Types */
db.events_types.drop();
db.events_types.insert({code:"subject", name:"Disciplina"});
db.events_types.insert({code:"course", name:"Curso"});
db.events_types.insert({code:"acamp", name:"Retiro"});
db.events_types.insert({code:"event", name:"Evento"});
db.events_types.insert({code:"meeting", name:"Reunião de Células"});


/* Groups Types */
db.groups_types.drop()
db.groups_types.insert({code:"cell", name:"Célula"});
db.groups_types.insert({code:"network", name:"Rede"});
db.groups_types.insert({code:"sector", name:"Setor"})
db.groups_types.insert({code:"region", name:"Região"});
db.groups_types.insert({code:"satelite_church", name:"Congregação"});
db.groups_types.insert({code:"main_church", name:"Igreja Sede"});


db.roles.drop()
/* Courses roles */
var student = {code:"student", name:"Aluno"};
db.roles.save(student);
var teacher = {code:"teacher", name:"Professor"};
db.roles.save(teacher);

/* Group roles */
var visitor = {code:"visitor", name:"Visitante"}
db.roles.save(visitor);
var cell_member = {code:"cell_member", name:"Membro em Célula"}
db.roles.save(cell_member);
var host = {code:"host", name:"Anfitrião"};
db.roles.save(host);
var leader = {code:"leader", name:"Lider"};
db.roles.save(leader);


/* Permissions */
db.permissions.drop()
db.permissions.insert({target_obj:"groups", perms: "rwc+", role: leader._id});
db.permissions.insert({target_obj:"groups", perms: "r", role: cell_member._id});

db.permissions.insert({target_obj:"events", perms: "rwc+", role: leader._id});
db.permissions.insert({target_obj:"events", perms: "r", role: cell_member._id});

/* Users */
db.users.drop();
db.users.insert({
	"user_name" : "msantos.douglas@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Douglas", "last_name": "Morais", "profile_image": "douglas.jpg",
					"addr_lat":"-30.1515134802916", "addr_lng" : "-51.3381549802916"
	}
});
db.users.insert({
	"user_name" : "tatiele@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Tatiele", "last_name": "Morais", "profile_image": "tatiele.jpg",
					"addr_lat":"-30.1515134802916", "addr_lng" : "-51.3381549802916"
	}
});
db.users.insert({
	"user_name" : "altair@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Altair", "last_name": "Souza", "profile_image": "altair.jpg",
					"addr_lat":"-30.1291731", "addr_lng" : "-51.315149"
	}
});
db.users.insert({
	"user_name" : "indaia@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Indaia", "last_name": "Souza", "profile_image": "indaia.jpg",
					"addr_lat":"-30.1291731", "addr_lng" : "-51.315149"
	}
});
db.users.insert({
	"user_name" : "felipe@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Felipe", "last_name": "Maia", "profile_image": "felipe.jpg",
					"addr_lat":"-30.1312171", "addr_lng" : "-51.3143318"
	}
});
db.users.insert({
	"user_name" : "camila@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Camila", "last_name": "Maia", "profile_image": "camila.jpg",
					"addr_lat":"-30.1312171", "addr_lng" : "-51.3143318"
	}
});
db.users.insert({
	"user_name" : "jose@gmail.com",
	"auth_type" : "password",
	"auth_token" : "abacate",
	"extra_data" : {"first_name" : "Jose", "last_name": "Silva",
					"addr_lat":"-30.108204", "addr_lng" : "-51.330102"
	}
});

