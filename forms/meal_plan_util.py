def generate_default_5_day_plan(meal_types=['breakfast', 'lunch', 'dinner']):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return [{'day': day, 'meal_type': mt} for day in days for mt in meal_types]
