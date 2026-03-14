function churchAssistant(question){

question = question.toLowerCase()

if(question.includes("member") || question.includes("join")){
return "To join the church, go to the Intake page and complete the New Member Intake form. A registry ID can be generated through the intake system."
}

if(question.includes("minister") || question.includes("ordination")){
return "Minister applicants may register through the intake system and minister portal. Registry IDs for ministers begin with LOAI-MIN."
}

if(question.includes("practitioner") || question.includes("holistic") || question.includes("health")){
return "Holistic Health practitioners may register through the intake system. Practitioner registry IDs begin with LOAI-HP."
}

if(question.includes("donation") || question.includes("donate")){
return "Donations support church education, registry operations, and outreach programs."
}

if(question.includes("library") || question.includes("resources")){
return "Visit the Church Library page for study materials and ministry resources."
}

if(question.includes("registry") || question.includes("id")){
return "Registry IDs identify members, ministers, and practitioners in the Hybrid AI Human Registry system."
}

if(question.includes("certificate")){
return "Certificates and credentials connect to registry records and verification through the church registry."
}
if(question.includes("scripture") || question.includes("bible")){
window.location.href = "scripture.html";
return "Opening Scripture Study..."

}

if(question.includes("wisdom") || question.includes("indigenous")){
window.location.href = "wisdom.html";
return "Opening Indigenous Wisdom..."

}

if(question.includes("education") || question.includes("learning")){
window.location.href = "education.html";
return "Opening Holistic Education..."

}

if(question.includes("publications") || question.includes("research")){
window.location.href = "publications.html";
return "Opening Research Publications..."

}
return "Welcome to the Seven-Fold Indigenous Global Church assistant. Ask about membership, ministers, practitioners, donations, registry IDs, or church programs."

}
