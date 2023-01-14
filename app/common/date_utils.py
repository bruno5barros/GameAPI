from datetime import date


valid_age = 18


def calculate_age(birthdate):
    """Calculate the user age"""
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) <
                                         (birthdate.month, birthdate.day))
    return age


def convert_str_date(new_date: str):
    """Convert type str to date"""
    try:
        return date.fromisoformat(new_date)
    except ValueError:
        raise ValueError("The input is invalid.")


def convert_date_str(date):
    try:
        return date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("The input is invalid.")
