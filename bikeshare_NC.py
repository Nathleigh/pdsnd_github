# PYTHON BIKESHARE PROJECT SUBMISSION BY NATHAN CHAPMAN
# Now housed on Nathleigh's github repo 
# https://github.com/Nathleigh/pdsnd_github.git

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# filter can be applied to select any months from the list
months_list = ['January', 'February', 'March', 'April', 'May', 'June']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). while loop handles invalid inputs
    city = ""
    while not city:
        city = input("Which city would you like data for: Chicago, New York, or Washington? ").lower()
        if city in ('chicago', 'new york', 'washington'):
            print("OK!") 
        else:
            print("Sorry, that isn't a valid city.")
            city=""

    # Ask for user filter preference
    filterchoice = ""
    while not filterchoice:
        filterchoice = input("Would you like to filter the data by month, day, or neither? ").lower()
        if filterchoice in ('month', 'day', 'neither'):
            print("OK!") 
        else:
            print("Sorry, that isn't a valid filter.")
            filterchoice=""

    # If they chose month, get user input for month
    if filterchoice == 'month':
        day = 'all'
        month = ''
        while not month:
            month = input("Which month - January, February, March, April, May, or June? ").title()
            if month in months_list:
                print("OK!") 
            else:
                print("Sorry, that isn't a valid month.")
                month=""

    # If they chose day, get user input for day of week
    if filterchoice == 'day':
        day = ''
        month = 'all'
        while not day:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").title()
            if day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
                print("OK!") 
            else:
                print("Sorry, that isn't a valid day.")
                day=""

    if filterchoice == 'neither':
        day = 'all'
        month = "all"    

    print('-'*40)
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
    # load selected city data into DataFrame df
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day_of_week & hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 
    df['hour'] = df['Start Time'].dt.hour

    # join start and stop stations to create new trip column
    df['trip'] = df['Start Station'] + " to " + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding integer
        month = months_list.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    month, day of week, hour of day """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    # use the index of the months list to get the corresponding str
    month = months_list[popular_month - 1] 
    print("The most common month is:", month.title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is:", popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    pop_trip_count = df['hour'].value_counts().iloc[0]
    print("The most common hour of the day is:", popular_hour, "- with", pop_trip_count, "trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start)
    
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    pop_trip_count = df['trip'].value_counts()[popular_trip]
    print('Most Common trip from start to end:', popular_trip, "- with", pop_trip_count, "trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel_time)
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Avg travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_data = df['User Type'].value_counts()
    print("Count of user types:\n", user_data.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("Count of user gender:\n", gender_count.to_string())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Birth statistics:")
        print("Earliest year of birth:", df['Birth Year'].min())
        print("Most recent year of birth:", df['Birth Year'].max())
        common_year = df['Birth Year'].mode()[0]
        print("Most common year of birth:", common_year)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask whether to print dataframe rows, and whether to print more
        start_row = 0
        end_row = 5
        print_data = input('\nWould you like to see the filtered trip data? Enter yes or no.\n')
        if print_data.lower() == 'yes':
            want_more = 'yes'
            while want_more.lower() == 'yes':
                print(df[start_row:end_row])
                start_row +=5
                end_row +=5
                want_more = input('\nWould you like another 5 rows? Enter yes or no.\n')
        
        # prompt to run again or exit
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
