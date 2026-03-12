function generateRegistryID(type){

let prefix = ""

if(type === "member"){
prefix = "LOAI-M"
}

if(type === "minister"){
prefix = "LOAI-MIN"
}

if(type === "practitioner"){
prefix = "LOAI-HP"
}

let random = Math.floor(Math.random()*900000)+100000

return prefix + "-" + random

}

function registerMember(name){

let id = generateRegistryID("member")

return {
name:name,
registryID:id,
status:"Active Member"
}

}

function registerMinister(name){

let id = generateRegistryID("minister")

return {
name:name,
registryID:id,
status:"Registered Minister"
}

}
