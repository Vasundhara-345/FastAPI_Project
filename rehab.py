import pandas as pd

class Person:
    def __init__(self, person_id, name, age, addiction_type):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.addiction_type = addiction_type

    def __repr__(self):
        return f"Person({self.person_id}, {self.name}, {self.age}, {self.addiction_type})"

class RehabilitationCenter:
    def __init__(self):
        self.admitted_people = []
        self.rehabilitated_people = []
        self.transferred_people = []
        self.left_against_medical_advice_people = []

    def admit_person(self, person):
        self.admitted_people.append(person)

    def rehabilitate_person(self, person_id):
        for person in self.admitted_people:
            if person.person_id == person_id:
                self.admitted_people.remove(person)
                self.rehabilitated_people.append(person)
                return

    def transfer_person(self, person):
        self.transferred_people.append(person)
        self.admitted_people = [p for p in self.admitted_people if p.person_id != person.person_id]

    def left_against_medical_advice(self, person):
        self.left_against_medical_advice_people.append(person)
        self.admitted_people = [p for p in self.admitted_people if p.person_id != person.person_id]

    def update_person_details(self, person_id, name, age, addiction_type):
        for person in self.admitted_people:
            if person.person_id == person_id:
                person.name = name
                person.age = age
                person.addiction_type = addiction_type
                return
        for person in self.rehabilitated_people:
            if person.person_id == person_id:
                person.name = name
                person.age = age
                person.addiction_type = addiction_type
                return
        for person in self.transferred_people:
            if person.person_id == person_id:
                person.name = name
                person.age = age
                person.addiction_type = addiction_type
                return
        for person in self.left_against_medical_advice_people:
            if person.person_id == person_id:
                person.name = name
                person.age = age
                person.addiction_type = addiction_type
                return

    def get_admitted_people_dataframe(self):
        data = {
            'Person ID': [p.person_id for p in self.admitted_people],
            'Name': [p.name for p in self.admitted_people],
            'Age': [p.age for p in self.admitted_people],
            'Addiction Type': [p.addiction_type for p in self.admitted_people]
        }
        df = pd.DataFrame(data)
        return df

    def get_rehabilitated_people_dataframe(self):
        data = {
            'Person ID': [p.person_id for p in self.rehabilitated_people],
            'Name': [p.name for p in self.rehabilitated_people],
            'Age': [p.age for p in self.rehabilitated_people],
            'Addiction Type': [p.addiction_type for p in self.rehabilitated_people]
        }
        df = pd.DataFrame(data)
        return df

    def get_transferred_people_dataframe(self):
        data = {
            'Person ID': [p.person_id for p in self.transferred_people],
            'Name': [p.name for p in self.transferred_people],
            'Age': [p.age for p in self.transferred_people],
            'Addiction Type': [p.addiction_type for p in self.transferred_people]
        }
        df = pd.DataFrame(data)
        return df

    def get_left_against_medical_advice_people_dataframe(self):
        data = {
            'Person ID': [p.person_id for p in self.left_against_medical_advice_people],
            'Name': [p.name for p in self.left_against_medical_advice_people],
            'Age': [p.age for p in self.left_against_medical_advice_people],
            'Addiction Type': [p.addiction_type for p in self.left_against_medical_advice_people]
        }
        df = pd.DataFrame(data)
        return df

    def search_patient_by_name(self, name):
        for person in self.admitted_people + self.rehabilitated_people + self.transferred_people + self.left_against_medical_advice_people:
            if person.name.lower() == name.lower():
                return person
        return None

    def get_rehabilitation_status(self, name):
        person = self.search_patient_by_name(name)
        if person:
            if person in self.admitted_people:
                return f"{person.name} is currently admitted."
            elif person in self.rehabilitated_people:
                return f"{person.name} has been rehabilitated."
            elif person in self.transferred_people:
                return f"{person.name} has been transferred."
            elif person in self.left_against_medical_advice_people:
                return f"{person.name} left against medical advice."
        else:
            return None
