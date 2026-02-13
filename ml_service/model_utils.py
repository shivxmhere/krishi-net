# Define the class labels in the exact order the model was trained
CLASS_LABELS = {
    0: "Healthy",
    1: "Wheat Rust",
    2: "Potato Blight",
    3: "Corn Common Smut"
    # Add more classes as per your trained model
}

# Define treatment info for each class
TREATMENT_INFO = {
    "Healthy": {
        "severity": "Low",
        "treatments": [
            "Continue regular monitoring",
            "Maintain proper irrigation",
            "Ensure balanced fertilization"
        ]
    },
    "Wheat Rust": {
        "severity": "High",
        "treatments": [
            "Apply fungicides like Tebuconazole or Propiconazole",
            "Remove and destroy infected plant parts",
            "Plant resistant varieties in future seasons",
            "Avoid overhead irrigation to reduce moisture on leaves"
        ]
    },
    "Potato Blight": {
        "severity": "High",
        "treatments": [
            "Apply copper-based fungicides",
            "Improve air circulation between plants",
            "Remove infected leaves immediately",
            "Avoid watering in the evening"
        ]
    },
    "Corn Common Smut": {
        "severity": "Moderate",
        "treatments": [
            "Remove galls before they rupture",
            "Avoid mechanical injury to plants",
            "Maintain balanced nitrogen levels",
            "Rotate crops"
        ]
    },
    "Unknown": {
        "severity": "Unknown",
        "treatments": ["Consult a local agricultural expert"]
    }
}
