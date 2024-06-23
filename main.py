import os
from datetime import datetime, timedelta
import random

"Disclaimer"
"This Script is only used to pad stats, you may or may not get better at coding by using this"
"Results will vary"

def is_weekend(date):
    """Check if a given date is a weekend (Saturday or Sunday)."""
    return date.weekday() >= 5  # 5 for Saturday, 6 for Sunday

def generate_weekdays_for_years(years: int):
    """Generate a list of all weekdays (excluding weekends) in the past `years` years."""
    current_date = datetime.now()
    start_date = current_date - timedelta(days=365 * years)
    date_range = [start_date + timedelta(days=x) for x in range((current_date - start_date).days + 1)]
    weekdays = [date for date in date_range if not is_weekend(date)]
    return weekdays

def select_random_days(weekdays, days_per_week_min, days_per_week_max):
    """Select random days per week within the specified range."""
    selected_days = []
    weekly_dates = {}

    # Organize weekdays by week number
    for date in weekdays:
        week_number = date.strftime("%Y-%U")  # Format as "Year-WeekNumber"
        if week_number not in weekly_dates:
            weekly_dates[week_number] = []
        weekly_dates[week_number].append(date)

    # Randomly select 3-4 days from each week's available weekdays
    for week, days in weekly_dates.items():
        if random.choice([True, False]):  # Randomly decide if this week has no commits
            num_days = random.randint(days_per_week_min, days_per_week_max)
            if num_days > len(days):
                num_days = len(days)  # Limit to the available days if less than the random range
            selected_days.extend(random.sample(days, num_days))

    return selected_days

def makeCommits(years: int, days_per_week_min: int, days_per_week_max: int):
    """Create commits on random weekdays within the past given years."""

    if years < 1 or days_per_week_min < 1 or days_per_week_max < days_per_week_min:
        print("Invalid input parameters.")
        return

    # Generate all valid weekdays for the past given years
    weekdays = generate_weekdays_for_years(years)

    # Select random days per week
    commit_dates = select_random_days(weekdays, days_per_week_min, days_per_week_max)

    for date in commit_dates:
        commit_date_str = date.strftime("%Y-%m-%d")

        # Random number of commits for the day
        num_commits = random.randint(1, 20)

        for i in range(num_commits):
            # Randomize commit time within the day
            commit_time = date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
            commit_time_str = commit_time.strftime("%Y-%m-%d %H:%M:%S")

            # Write to demo.txt
            with open('demo.txt', 'a') as file:
                file.write(f'{commit_time_str} <- Commit Listed in a Day!\n')

            # Set the environment variables for the commit
            os.environ['GIT_COMMITTER_DATE'] = commit_time_str
            os.environ['GIT_AUTHOR_DATE'] = commit_time_str

            # Add and commit the changes
            os.system('git add demo.txt')
            os.system(f'git commit --date="{commit_time_str}" -m "Commit on {commit_time_str}"')

    # Final push to repository
    os.system('git push')

# Example usage: Make commits for the last 3 years, 3-4 days a week, with 1-20 commits per day
makeCommits(3, 3, 4)
