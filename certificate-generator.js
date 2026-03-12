function generateCertificate(name, id, type){

let title = ""

if(type === "member"){
title = "Church Member Certificate"
}

if(type === "minister"){
title = "Minister Credential"
}

if(type === "practitioner"){
title = "Holistic Health Practitioner Credential"
}

let certificate = `
<div style="
border:3px solid black;
padding:25px;
margin-top:20px;
background:white;
color:black;
text-align:center;
">

<h2>Seven-Fold Indigenous Global Church</h2>

<h3>${title}</h3>

<p>This certifies that</p>

<h2>${name}</h2>

<p>is registered within the</p>

<p>Hybrid AI Human Registry System</p>

<p><strong>Registry ID:</strong> ${id}</p>

<p>Issued through the Church Registry System</p>

</div>
`

return certificate
}
