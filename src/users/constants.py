MALE_MEASUREMENTS = {
    "measurement_type": "MALE",
    **{name: 0.0 for name in [
        "chest_burst", "stomach", "top_length", "shoulder",
        "sleeve_length", "neck", "muscle", "waist", "laps",
        "knee"
    ]}
}

FEMALE_MEASUREMENTS = {
    "measurement_type": "FEMALE",
    **{name: 0.0 for name in [
        "burst", "waist", "hips", "shoulder",
        "full_length", "half_length", "round_sleeve", "neck"
    ]}
}
VALID_MEASUREMENT_NAMES = [
    "chest_burst", "stomach",
    "top_length", "shoulder",
    "sleeve_length", "neck",
    "muscle", "waist", "laps",
    "knee", "burst", "hips",
    "full_length", "half_length",
     "round_sleeve"
]

FAVORITES = {
    "tailors": [],
    "products": []
}

MEASUREMENT_TYPES = ["male", "female", "kids"]
SUCCESSFUL_UPDATE = {"message": "Successfully updated"}
