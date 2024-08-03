MALE_MEASUREMENTS = {
    name: 0.0 for name in [
            "chest_burst", "stomach",
            "top_length", "shoulder",
            "sleeve_length", "neck",
            "muscle", "waist", "laps",
            "knee",
        ]
}

FEMALE_MEASUREMENTS = {
    name: 0.0 for name in [
            "burst", "waist",
            "hips", "shoulder",
            "full_length", "half_length",
            "round_sleeve", "neck"
        ]
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

SUCCESSFUL_UPDATE = {"message": "Successfully updated"}
