from datetime import datetime, timedelta
from collections import defaultdict

# Given leave periods where format is (departure, return)
leave_dates = [
    ("7/6/2023", "20/9/2023"),
    ("8/12/2023", "15/12/2023"),
    ("17/12/2023", "8/1/2024"),
    ("20/6/2024", "16/9/2024"),
    ("17/9/2024", "22/9/2024")
]

# leave_dates = [
#     ("5/6/2023", "18/9/2023"),
#     ("8/12/2023", "15/12/2023"),
#     ("11/06/2024", "17/09/2024")
# ]

def parse_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y")

def days_out_of_uk(leave_start, leave_end):
    return (leave_end - leave_start).days

# Parsing and processing
monthly_days = defaultdict(lambda: defaultdict(int))  # year -> month -> days out

for start_str, end_str in leave_dates:
    leave_start = parse_date(start_str)
    leave_end = parse_date(end_str)
    
    days_out = days_out_of_uk(leave_start, leave_end)
    
    current_start = leave_start
    
    while current_start <= leave_end:
        end_of_month = (current_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        days_in_month = (end_of_month - current_start).days + 1
        if end_of_month > leave_end:
            days_in_month = (leave_end - current_start).days + 1
        
        monthly_days[current_start.year][current_start.month] += days_in_month
        current_start = (end_of_month + timedelta(days=1))

# Output the result
monthly_days_out = {year: dict(months) for year, months in monthly_days.items()}
for year, months in monthly_days_out.items():
    print(f"{year}: {months}")

def check_12_months_period(monthly_days):
    # Flatten the monthly_days structure into a list of tuples (year, month, days_out)
    flattened_days = []
    for year, months in sorted(monthly_days.items()):
        for month, days in sorted(months.items()):
            flattened_days.append((year, month, days))
    
    # Check every 12-month window
    limit = 180
    for i in range(len(flattened_days)):
        total_days = 0
        for j in range(i, len(flattened_days)):
            year, month, days = flattened_days[j]
            total_days += days
            
            # Calculate the difference in months between the first entry in the window and the current entry
            start_year, start_month, _ = flattened_days[i]
            delta_months = (year - start_year) * 12 + (month - start_month)
            
            # If it's a 12-month period, check the limit
            if delta_months == 11:
                if total_days > limit:
                    return False
                break
    return True

def total_days_out_of_uk(leave_dates):
    total_days = 0
    for start_str, end_str in leave_dates:
        leave_start = parse_date(start_str)
        leave_end = parse_date(end_str)
        total_days += days_out_of_uk(leave_start, leave_end)
    return total_days

# Example usage
total_days = total_days_out_of_uk(leave_dates)
print(f"Total days out of the UK: {total_days}, days left: {450-total_days}")


meets_requirement = check_12_months_period(monthly_days)
if meets_requirement:
  print("requirement meet")
else:
  print("requirement not meet")