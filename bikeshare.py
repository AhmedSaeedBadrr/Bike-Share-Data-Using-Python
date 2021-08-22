import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
is_washington = False
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = "all"
    day = "all"
    city = "none"
    listOfGlobals = globals()
    listOfGlobals['is_washington'] = False
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = str(input("Would you like to see data for Chicago, New York City, or Washington?\n"))
        if (city.lower() == 'chicago' or city.lower() == 'new york city' or city.lower() == 'washington'):
            break;
        else:
            print("Input Not Valid! please enter one of the 3 cities\n")
    bool = False
    while True:
        option = str(input("Would you like to filter data by month, day, both, or not at all?Type \"none\" for no time filter.\n"))
        if(option.lower() == 'month' or option.lower() == 'both'):
            if(option.lower() == 'both'):
                bool = True
            while True:
                month = str(input("Which month? or you can choose all months by type \"all\", January, February, March, April, May, or June?\n"))
                if(month.lower()=='january' or month.lower()=='february' or month.lower()=='march' or month.lower()=='april' or month.lower()=='may' or month.lower()=='june' or month.lower()=='all'):
                    break;
                else:
                    print("Input Not Valid! please enter a valid month\n")
            break;
        elif(option.lower() == 'day'):
            bool = True
            break;
        elif(option.lower()=='none'):
            break;

        else:
            print("Input Not Valid! please enter a valid input\n")

    while(True and bool == True):
        day = str(input("Which day? or you can choose all days by type \"all\", (e.g., Sunday)\n"))
        if (day.lower() == 'sunday' or day.lower() == 'monday' or day.lower() == 'tuesday' or day.lower() == 'wednesday' or day.lower() == 'thursday' or day.lower() == 'friday' or day.lower() == 'saturday' or day.lower() == 'all'):
            break;
        else:
            print("Input Not Valid! please enter valid day\n")

    print('-'*40)
    city = city.lower()
    month = month.lower()
    day = day.lower()
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #git change
    df = pd.read_csv(CITY_DATA[city])
    if (city == 'washington'):
        listOfGlobals = globals()
        listOfGlobals['is_washington'] = True
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("The most common Month is:",common_month)
    common_day = df['day_of_week'].mode()[0]
    print("The most common Day is:",common_day)
    common_hour = df['hour'].mode()[0]
    print("The most common Hour is:",common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is:",common_start_station)
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is:",common_end_station)
    common_comb_station = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is:",common_comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    #git change
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    total_travel_formatted = str(datetime.timedelta(seconds=int(total_travel_time)))
    print("Total Travel Time is:",total_travel_formatted," Days")
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_formatted = str(datetime.timedelta(seconds=int(mean_travel_time)))
    print("Average Travel Time is:",mean_travel_formatted," Days")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_count = df['User Type'].value_counts();
    print("The user types counts is:\n",user_count)
    if(is_washington == False):
        user_gender = df['Gender'].value_counts();
        print("The user Genders counts is:\n",user_gender)
        earliest_year = df['Birth Year'].min()
        print("earliest year of birth is:",int(earliest_year))
        most_recent = df['Birth Year'].max()
        print("most recent year of birth is:",int(most_recent))
        most_common = df['Birth Year'].mode()[0]
        print("most common year of birth is:",int(most_common))
    else:
        print("Washington has no Gender and Birth Year Data!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays individual trip data for only 5 rows each time user type yes untill he type no"""
    x, y= 0, 5
    while True:
        show_data = input("\nWould you like to view individual trip data? please type 'yes' or 'No'.\n")
        if show_data.lower() == 'yes':
            print(df[x:y])
            x= y
            y+= 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
