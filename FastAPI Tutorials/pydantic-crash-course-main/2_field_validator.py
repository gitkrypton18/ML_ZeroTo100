# ==========================================================
# CUSTOM VALIDATORS IN PYDANTIC
# ==========================================================

# Until now we used built-in validators such as:
#
# EmailStr  -> validates email format
# Field()   -> validates ranges, lengths etc.
#
# But sometimes business requirements are custom.
#
# Example:
#
# Company policy says only emails from:
# - hdfc.com
# - icici.com
#
# are allowed.
#
# Pydantic's built-in validators cannot know this.
#
# For such situations we create CUSTOM VALIDATORS.


from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator
)

from typing import (
    List,
    Dict,
    Optional,
    Annotated
)


# ==========================================================
# PATIENT MODEL
# ==========================================================

# This model defines how patient data should look.

class Patient(BaseModel):

    # Basic string field
    name: str

    # EmailStr checks:
    #
    # abc@gmail.com  -> valid
    # abc.com        -> invalid
    #
    # But EmailStr only validates FORMAT.
    #
    # It does NOT check whether gmail.com,
    # icici.com or hdfc.com is allowed.
    #
    # We will add that logic ourselves later.

    email: EmailStr


    # Integer age
    age: int


    # Float weight
    weight: float


    # Boolean field
    married: bool


    # List of allergies
    allergies: List[str]


    # Dictionary
    #
    # Example:
    #
    # {
    #   "phone":"123456",
    #   "city":"Kota"
    # }

    contact_details: Dict[str, str]


    # ======================================================
    # EMAIL VALIDATOR
    # ======================================================

    # field_validator('email')
    #
    # tells Pydantic:
    #
    # "Whenever email is received,
    # run this function."

    @field_validator('email')

    # validator methods should generally
    # be class methods.

    @classmethod
    def email_validator(cls, value):

        # Allowed company domains

        valid_domains = [
            'hdfc.com',
            'icici.com'
        ]


        # INPUT:
        #
        # abc@icici.com
        #
        # split('@')
        #
        # ['abc', 'icici.com']
        #
        # [-1] means last element

        domain_name = value.split('@')[-1]


        # If domain is not allowed,
        # raise an error.

        if domain_name not in valid_domains:
            raise ValueError(
                'Not a valid domain'
            )


        # Always return value if valid

        return value


    # ======================================================
    # NAME TRANSFORMATION
    # ======================================================

    # Validators are not only for validation.
    #
    # They can also transform data.

    @field_validator('name')

    @classmethod
    def transform_name(cls, value):

        # nitish
        #
        # becomes
        #
        # NITISH

        return value.upper()


    # ======================================================
    # AGE VALIDATOR
    # ======================================================

    # mode='after'
    #
    # Means:
    #
    # First convert the datatype
    #
    # Then run validator.
    #
    # Example:
    #
    # age = "30"
    #
    # Step 1:
    # convert to integer 30
    #
    # Step 2:
    # run validator

    @field_validator('age', mode='after')

    @classmethod
    def validate_age(cls, value):

        if 0 < value < 100:
            return value

        else:
            raise ValueError(
                'Age should be in between 0 and 100'
            )


# ==========================================================
# FUNCTION
# ==========================================================

# Receives already validated Patient object.

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)

    print('updated')


# ==========================================================
# RAW USER INPUT
# ==========================================================

# Imagine this came from:
#
# - FastAPI request body
# - Frontend form
# - Database
# - JSON payload

patient_info = {

    'name': 'nitish',

    'email': 'abc@icici.com',

    # Notice:
    #
    # string not integer

    'age': '30',

    'weight': 75.2,

    'married': True,

    'allergies': [
        'pollen',
        'dust'
    ],

    'contact_details': {
        'phone': '2353462'
    }
}


# ==========================================================
# MODEL CREATION
# ==========================================================

# ** means dictionary unpacking

patient1 = Patient(**patient_info)


# What happens internally?
#
# Step 1:
# Validate email format
#
# abc@icici.com ✓
#
#
# Step 2:
# Run email_validator()
#
# icici.com ✓
#
#
# Step 3:
# Convert age
#
# "30" -> 30
#
#
# Step 4:
# Run validate_age()
#
# 30 ✓
#
#
# Step 5:
# Run transform_name()
#
# nitish -> NITISH
#
#
# Step 6:
# Create Patient object


# ==========================================================
# FUNCTION CALL
# ==========================================================

update_patient_data(patient1)


# OUTPUT
#
# NITISH
# 30
# ['pollen', 'dust']
# True
# updated