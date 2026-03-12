function churchAssistant(question){

question = question.toLowerCase()

if(question.includes("member")){
return "To become a member, visit the Member Intake Portal on the church homepage."
}

if(question.includes("prayer")){
return "You can submit a prayer request through the Prayer Request section."
}

if(question.includes("minister")){
return "Minister applications are reviewed by the Seven Pillars Council. Visit the Minister Portal."
}

if(question.includes("health")){
return "Holistic Health education and research programs are available in the Holistic Health branch."
}

return "Welcome to the Seven-Fold Indigenous Global Church. How may I assist you?"
}
