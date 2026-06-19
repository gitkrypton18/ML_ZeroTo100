from fastapi import FastAPI, Path, HTTPException, Query # Import FastAPI and Path from the fastapi library 
import json
app = FastAPI() # Create a FastAPI instance

def load_data():
    with open("patients.json", "r") as f: # Open the data.json file in read mode
        data = json.load(f) # Load the JSON data from the file
    return data # Return the loaded data    

@app.get("/") # Define a GET endpoint at the root URL
def hello():
    return {"message":" Hello World"} # Return a JSON response

@app.get("/about") # Define a GET endpoint at the /about URL
def about():
    return {"message":" Kalpit is a developer."} # Return a JSON response

@app.get('/view')
def view():
    data = load_data() # Load the data from the JSON file
    return data # Return the loaded data as a JSON response

@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve")): # Define a GET endpoint with a path parameter for patient ID
    data = load_data() # Load the data from the JSON file
    if patient_id in data: # Check if the patient ID exists in the data
        return data[patient_id] # Return the patient data as a JSON response
    raise HTTPException(status_code=404, detail="Patient not found") # Raise an HTTP exception if the patient ID is not found

# query parameters implqementation
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="The field to sort by height, weight, bmi"), order: str = Query('asc', description='Sort in ascending')): # MOVED 'order' UP HERE
    
    valid_fields = ['height', 'weight', 'bmi'] # Define valid fields for sorting
    if sort_by not in valid_fields: # Check if the sort_by parameter is valid
        raise HTTPException(status_code=400, detail=f"Invalid sort field") # Raise an HTTP exception if the sort_by parameter is invalid
    if order not in ['asc', 'desc']: # Check if the order parameter is valid    
        raise HTTPException(status_code=400, detail=f"Invalid sort order") # Raise an HTTP exception if the order parameter is invalid
    data = load_data() # Load the data from the JSON file
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == 'desc')) # Sort the data based on the specified field and order
    return sorted_data # Return the sorted data as a JSON response