import datetime

# Définition des dates
timesheet_line_date = datetime.date(2023, 9, 22)
date_start = datetime.date(2023, 9, 21)
date_end = datetime.date(2023, 9, 24)

# Liste des dates autorisées
valid_dates = [date_start, date_end]

# Assertion qui va échouer
assert (
    timesheet_line_date in valid_dates
), f"{timesheet_line_date} not found in {valid_dates}"

print("Assertion passed!")
