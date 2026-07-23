import os
from plantuml import PlantUML

ARTIFACT_DIR = r"C:\Users\BIT\.gemini\antigravity-ide\brain\f629e099-6b60-4990-9e8e-5d584246f9e3"

uml_code = """
@startuml
skinparam backgroundColor #FFFFFF
skinparam sequence {
    ArrowColor #000000
    ActorBorderColor #000000
    LifeLineBorderColor #000000
    LifeLineBackgroundColor #FFFFFF
    ParticipantBorderColor #000000
    ParticipantBackgroundColor #F3F4F6
    ParticipantFontColor #000000
    ActorFontColor #000000
}

actor User
participant "React UI" as UI
participant "FastAPI" as API
participant "NLP Engine" as NLP
participant "Vectorizer" as Vec
participant "PyTorch MLP" as PyTorch
participant "Naive Bayes" as NB
participant "FIR Drafter" as Drafter

User -> UI : Enters Hinglish Text
activate UI
UI -> API : POST /api/analyze JSON
activate API

API -> NLP : Pass Raw Text String
activate NLP
NLP -> NLP : Lowercase & Clean Regex
NLP -> NLP : Map via HINGLISH_MAP
NLP --> API : Return Processed Text
deactivate NLP

API -> Vec : Transform Processed Text
activate Vec
Vec --> API : Return 2000D Matrix
deactivate Vec

API -> PyTorch : Forward Pass (2000D Matrix)
activate PyTorch
PyTorch --> API : Return Threat Level (High/Med/Low)
deactivate PyTorch

API -> NB : Predict BNS (2000D Matrix)
activate NB
NB --> API : Return BNS Section
deactivate NB

alt Threat Level == High or Medium
    API -> Drafter : Pass Meta (Text, BNS, Level)
    activate Drafter
    Drafter --> API : Return FIR Complaint Draft
    deactivate Drafter
end

API --> UI : JSON (Threat, BNS, Draft)
deactivate API

UI --> User : Render Brutalist Alert UI
deactivate UI
@enduml
"""

txt_path = os.path.join(ARTIFACT_DIR, 'sequence.txt')
png_path = os.path.join(ARTIFACT_DIR, 'sequence_diagram_light.png')

with open(txt_path, 'w') as f:
    f.write(uml_code)

server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
server.processes_file(txt_path, outfile=png_path)
print(f"Successfully generated: {png_path}")
