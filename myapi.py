from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 20,
        "year" : "year 12"
    }
}

# We can use Pydantic models to define the structure of the data we want to receive in our API. This allows us to validate the data and also to automatically generate documentation for our API.
class Student(BaseModel):
    name: str
    age: int
    year : str

# We can use the same model for both creating and updating a student, but we can also create a separate model for updating a student if we want to make some fields optional.
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year : Optional[str] = None

@app.get("/")
def index():
    return{
        "name" : "1 data"
    }

# Path parameters
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0 , lt=3)):
    return students[student_id]

# Query parameters
@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {
        "Data" : "Not found"
    }

#combine path and query parameters
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {
        "Data" : "Not found"
    }

# Add a student using post method
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student:Student):
    if student_id in students:
        return {
            "Error" : "Student already exists"
        }
    
    students[student_id] = student
    return students[student_id]

# Update a student using put method
@app.put("/update-student/{student_id}")
def update_student(student_id : int, student:UpdateStudent):
    if student_id not in students:
        return {
            "Error" : "Student does not exist"
        }
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
    return students[student_id]

# Delete a student using delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {
            "Error" : "Student does not exist"
        }
    del students[student_id]
    return {
        "Message" : "Student deleted successfully"
    }
