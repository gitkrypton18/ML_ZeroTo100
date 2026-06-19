# ==========================================
# PYDANTIC CRASH COURSE
# ==========================================

# BaseModel:
# Parent class of every Pydantic model.
# Gives automatic validation, parsing,
# serialization and type checking.

# EmailStr:
# Validates whether a string is a valid email.

# AnyUrl:
# Validates whether a string is a proper URL.

# Field:
# Used for adding constraints and metadata.

from pydantic import BaseModel, EmailStr, AnyUrl, Field


# List     -> list of values
# Dict     -> key-value pairs
# Optional -> value can be None
# Annotated-> combine type hint + validation

from typing import List, Dict, Optional, Annotated


# ==========================================
# DEFINING A PYDANTIC MODEL
# ==========================================

# Think of this as a blueprint/schema
# for patient data.

class Patient(BaseModel):

    # --------------------------------------
    # NAME FIELD
    # --------------------------------------

    # Annotated combines:
    # 1. Actual datatype (str)
    # 2. Validation rules (Field)

    name: Annotated[
        str,

        Field(
            # Name must not exceed 50 chars
            max_length=50,

            # Used in Swagger docs
            title='Name of the patient',

            # Documentation for APIs
            description='Give the name of the patient in less than 50 chars',

            # Example values shown in docs
            examples=['Nitish', 'Amit']
        )
    ]


    # --------------------------------------
    # EMAIL FIELD
    # --------------------------------------

    # EmailStr automatically validates email

    email: EmailStr


    # --------------------------------------
    # URL FIELD
    # --------------------------------------

    # AnyUrl checks whether URL is valid

    linkedin_url: AnyUrl


    # --------------------------------------
    # AGE FIELD
    # --------------------------------------

    # gt = greater than
    # lt = less than

    # Valid ages:
    # 1 to 119

    age: int = Field(
        gt=0,
        lt=120
    )


    # --------------------------------------
    # WEIGHT FIELD
    # --------------------------------------

    # strict=True means:
    # no automatic conversion allowed

    # Example:
    # weight=75.2  -> valid
    # weight="75.2" -> invalid

    weight: Annotated[
        float,
        Field(
            gt=0,
            strict=True
        )
    ]


    # --------------------------------------
    # MARRIED FIELD
    # --------------------------------------

    # bool can be:
    # True
    # False

    # default=None means field is optional

    married: Annotated[
        bool,
        Field(
            default=None,
            description='Is the patient married or not'
        )
    ]


    # --------------------------------------
    # ALLERGIES FIELD
    # --------------------------------------

    # Optional[List[str]]

    # Means:
    # List[str]
    # OR
    # None

    allergies: Annotated[
        Optional[List[str]],

        Field(
            default=None,

            # maximum 5 allergies
            max_length=5
        )
    ]


    # --------------------------------------
    # CONTACT DETAILS
    # --------------------------------------

    # Dict[str,str]

    # Key = string
    # Value = string

    # Example:
    # {
    #   "phone":"12345",
    #   "city":"Kota"
    # }

    contact_details: Dict[str, str]


# ==========================================
# FUNCTION USING THE MODEL
# ==========================================

def update_patient_data(patient: Patient):

    # Accessing validated data

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)

    print('updated')


# ==========================================
# RAW DATA COMING FROM USER/API
# ==========================================

patient_info = {

    'name': 'nitish',

    'email': 'abc@gmail.com',

    'linkedin_url': 'http://linkedin.com/1322',

    # Notice age is STRING
    # Pydantic will convert it to int
    'age': '30',

    'weight': 75.2,

    'contact_details': {
        'phone': '2353462'
    }
}


# ==========================================
# MODEL CREATION
# ==========================================

# ** means dictionary unpacking

# Equivalent to:

# Patient(
#   name='nitish',
#   email='abc@gmail.com',
#   ...
# )

patient1 = Patient(**patient_info)


# During this step Pydantic:

# 1. Validates email
# 2. Validates URL
# 3. Checks age range
# 4. Checks weight > 0
# 5. Converts age '30' -> 30
# 6. Creates Patient object


# ==========================================
# FUNCTION CALL
# ==========================================

update_patient_data(patient1)


# Expected Output

# nitish
# 30
# None
# None
# updated

