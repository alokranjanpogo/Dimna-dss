def get_alert(level):

    if level >= 529.5:
        return {
            "status": "RED",
            "message": "MANDATORY WITHDRAWAL 150 MLD"
        }

    elif level >= 529:
        return {
            "status": "YELLOW",
            "message": "Reservoir Near Alert Level"
        }

    return {
        "status": "GREEN",
        "message": "Normal"
    }
