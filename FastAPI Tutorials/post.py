from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
from fastapi.responses import JSONResponse
import json

app = FastAPI()


class Patient(BaseModel):

    id: Annotated[
        str,
        Field(
            ...,
            description="Unique identifier for the patient",
            examples=["P001", "P002"]
        )
    ]

    name: Annotated[
        str,
        Field(
            ...,
            max_length=50,
            title="Name of the patient",
            description="Give the name of the patient in less than 50 chars",
            examples=["Nitish", "Amit"]
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            max_length=100,
            title="City of the patient",
            description="Give the city of the patient in less than 100 chars",
            examples=["New York", "Los Angeles"]
        )
    ]

    age: Annotated[
        int,
        Field(
            ...,
            ge=0,
            title="Age of the patient",
            description="Give the age of the patient",
            examples=[25, 30]
        )
    ]

    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(
            ...,
            title="Gender of the patient",
            description="Give the gender of the patient",
            examples=["Male", "Female"]
        )
    ]

    height: Annotated[
        float,
        Field(
            ...,
            gt=0,  # height cannot be 0 otherwise BMI calculation fails
            title="Height of the patient",
            description="Give the height of the patient in meters",
            examples=[1.75, 1.80]
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            title="Weight of the patient",
            description="Give the weight of the patient in kilograms",
            examples=[70.5, 80.0]
        )
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"

        elif 18.5 <= self.bmi < 25:
            return "Normal weight"

        elif 25 <= self.bmi < 30:
            return "Overweight"

        else:
            return "Obese"


# Utility Function
def load_data():

    try:
        with open("patients.json", "r") as f:  # Open the patients.json file in read mode
            data = json.load(f)  # Load the JSON data from the file

        return data  # Return the loaded data

    except FileNotFoundError:
        return {}


# Utility Function
def save_data(data):

    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")  # Define a GET endpoint at the root URL
def hello():

    return {
        "message": "Hello World"
    }  # Return a JSON response


@app.get("/about")  # Define a GET endpoint at the /about URL
def about():

    return {
        "message": "Kalpit is a developer."
    }  # Return a JSON response


@app.get('/view')
def view():

    data = load_data()  # Load the data from the JSON file

    return data  # Return the loaded data as a JSON response


@app.get('/patient/{patient_id}')
def get_patient(
    patient_id: str = Path(
        ...,
        description="The ID of the patient to retrieve"
    )
):
    # Load the data from the JSON file
    data = load_data()

    # Check if the patient ID exists in the data
    if patient_id in data:

        # Return the patient data as a JSON response
        return data[patient_id]

    # Raise an HTTP exception if the patient ID is not found
    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# Query Parameters Implementation
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(
        ...,
        description="The field to sort by height, weight, bmi"
    ),
    order: str = Query(
        'asc',
        description='Sort in ascending or descending order'
    )
):

    # Define valid fields for sorting
    valid_fields = ['height', 'weight', 'bmi']

    # Check if the sort_by parameter is valid
    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    # Check if the order parameter is valid
    if order not in ['asc', 'desc']:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort order"
        )

    # Load the data from the JSON file
    data = load_data()

    # Sort the data based on the specified field and order
    sorted_data = sorted(
        data.values(),
        key=lambda x: x[sort_by],
        reverse=(order == 'desc')
    )

    # Return the sorted data as a JSON response
    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):

    # Load existing data
    data = load_data()

    # Check if patient ID already exists
    if patient.id in data:

        raise HTTPException(
            status_code=400,
            detail="Patient ID already exists"
        )

    # Convert Pydantic model into dictionary
    # model_dump() converts model -> dict
    patient_data = patient.model_dump(
        exclude={'id'}
    )

    # Store patient data using patient id as key
    data[patient.id] = patient_data

    # Save updated data back to JSON file
    save_data(data)

    return JSONResponse(
        content={
            "message": "Patient created successfully"
        },
        status_code=201
    )