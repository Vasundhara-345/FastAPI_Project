from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from data_patient import data_dict
from rehab import RehabilitationCenter, Person as RehabPerson

app = FastAPI(title="Drug Rehabilitation Centre",
              description="This is to display the details of patients in a Drug Rehabilitation Facility"
              )

class Person(BaseModel):
    name: str
    age: int
    addiction_type: str

class PersonInput(BaseModel):
    name: str
    age: int
    addiction_type: str
    rehabilitation_status: Optional[str] = None

# Create a global instance of the RehabilitationCenter
rehab_center = RehabilitationCenter()

def load_data_from_dict(data):
    for idx, entry in enumerate(data):
        person = RehabPerson(person_id=idx, name=entry['name'], age=entry['age'], addiction_type=entry['type_of_drug'])
        rehab_center.admit_person(person)
        if entry['rehabilitation_status'] == 'Completed':
            rehab_center.rehabilitate_person(idx)
        elif entry['rehabilitation_status'] == 'Left Against Medical Advice':
            rehab_center.left_against_medical_advice(person)
        elif entry['rehabilitation_status'] == 'Transferred':
            rehab_center.transfer_person(person)

load_data_from_dict(data_dict)

@app.get("/")
async def root():
    return{"message": "Welcome"}

@app.post("/admit_person/", response_model=Person)
async def admit_person(person_input: PersonInput):
    existing_person = rehab_center.search_patient_by_name(person_input.name)
    if existing_person:
        rehab_center.update_person_details(
            existing_person.person_id,
            person_input.name,
            person_input.age,
            person_input.addiction_type
        )
        if person_input.rehabilitation_status == 'Completed':
            rehab_center.rehabilitate_person(existing_person.person_id)
        elif person_input.rehabilitation_status == 'Left Against Medical Advice':
            rehab_center.left_against_medical_advice(existing_person)
        elif person_input.rehabilitation_status == 'Transferred':
            rehab_center.transfer_person(existing_person)
        return existing_person
    else:
        person_id = len(rehab_center.admitted_people) + len(rehab_center.rehabilitated_people) + len(rehab_center.transferred_people) + len(rehab_center.left_against_medical_advice_people)
        person = RehabPerson(
            person_id=person_id,
            name=person_input.name,
            age=person_input.age,
            addiction_type=person_input.addiction_type
        )
        rehab_center.admit_person(person)
        return person

@app.post("/rehabilitate_person/{person_id}")
async def rehabilitate_person(person_id: int, person_input: Optional[PersonInput] = None):
    if person_input:
        rehab_center.update_person_details(person_id, person_input.name, person_input.age, person_input.addiction_type)
    person = rehab_center.search_patient_by_name(person_input.name)
    rehab_center.admitted_people.remove(person)
    rehab_center.rehabilitated_people.append(person)
    rehab_center.rehabilitate_person(person_id)
    return {"message": f"Person with ID {person_id} has been rehabilitated."}

@app.get("/admitted_people/", response_model=List[Person])
async def get_admitted_people():
    return [
        {"name": p.name, "age": p.age, "addiction_type": p.addiction_type}
        for p in rehab_center.admitted_people
    ]

@app.get("/rehabilitated_people/", response_model=List[Person])
async def get_rehabilitated_people():
    return [
        {"name": p.name, "age": p.age, "addiction_type": p.addiction_type}
        for p in rehab_center.rehabilitated_people
    ]

@app.get("/transferred_people/", response_model=List[Person])
async def get_transferred_people():
    return [
        {"name": p.name, "age": p.age, "addiction_type": p.addiction_type}
        for p in rehab_center.transferred_people
    ]

@app.get("/left_against_medical_advice_people/", response_model=List[Person])
async def get_left_against_medical_advice_people():
    return [
        {"name": p.name, "age": p.age, "addiction_type": p.addiction_type}
        for p in rehab_center.left_against_medical_advice_people
    ]

@app.get("/search_patient_by_name/{name}", response_model=Person)
async def search_patient_by_name(name: str):
    person = rehab_center.search_patient_by_name(name)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"name": person.name, "age": person.age, "addiction_type": person.addiction_type}

@app.get("/rehabilitation_status/{name}")
async def get_rehabilitation_status(name: str):
    status = rehab_center.get_rehabilitation_status(name)
    if status is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"status": status}
