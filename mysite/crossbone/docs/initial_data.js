db.events_types.drop()
db.events_types.insert({code:"course", name:"Curso"});
db.events_types.insert({code:"acamp", name:"Retiro"});
db.events_types.insert({code:"event", name:"Evento"});
db.events_types.insert({code:"metting", name:"Reunião de Células"});


db.groups_types.drop()
db.groups_types.insert({code:"cell", name:"Célula"});
db.groups_types.insert({code:"network", name:"Rede"});
db.groups_types.insert({code:"sector", name:"Setor"})
db.groups_types.insert({code:"region", name:"Região"});
db.groups_types.insert({code:"satelite_church", name:"Congregação"});
db.groups_types.insert({code:"main_church", name:"Igreja Sede"});
