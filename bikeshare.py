#Author: Irwin Cheng, May 2021
#Update: May 27, 2021
#Purpose: Provide desriptive statistics as part of the Bike Share data analysis project written in Python
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?')
        #convert the city input to lower case
        city = city.lower()
        if city in ['washington','new york city','chicago']:
            break
        else:
            print("Please enter the city correctly")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month? January, February, March, April, May or June? Please enter 'all' if you do not wish to filter by months.")
        #convert the month input to lower case
        month = month.lower()
        if month in ['all','january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Please enter the valid month correctly")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Which day of the week? Enter 'all' if you do not wish to filter by day of the week.")
            #convert alphabets to lower case
            day = day.lower()
            if day in ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']:
                break
            else:
                print("Plese enter day of week")
        except:
                print("Plese enter day of week")

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    # weekday_name did not work, use day_name() to show day of week instead
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    #filter by day of week if applicable
    if day !='all':
        # filter by day of week to create the new dataframe
        ##DEBUG: days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        ##DEBUG troubleshoot :day = days.index(day) + 1
        # weekday_name did not work, use day_name()  to display day of week instead
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].mode()[0]==1:
        common_month ="January"
    elif df['month'].mode()[0] ==2:
        common_month = "February"
    elif df['month'].mode()[0]==3:
        common_month = "March"
    elif df['month'].mode()[0]==4:
        common_month = "April"
    elif df['month'].mode()[0]==5:
        common_month = "May"
    elif df['month'].mode()[0]==6:
        common_month = "June"

    print("The most common month: ", common_month, "\n")

    # display the most common day of week
    print("The most common day of week: ", df['day_of_week'].mode()[0], "\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station: ", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start and end station trip is: ", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    #Increase line break hyphens to 50 in station stat function of bikeshare Python file
    print('-'*50)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time, round value to 1 decimal place
    total_travel_time = sum(df['Trip Duration'])
    print("The total travel time: ", round(total_travel_time, 1)," seconds", "\n")

    # display mean travel time, round value to 1 decimal place
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time: ", round(mean_travel_time, 1), " seconds","\n" )

    print("\nThis took %s seconds." % (time.time() - start_time))
    #Increase number of line breaks to 50 dash characters in trip_duration_stat function
    print('-'*50)

def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print("Counts of each User Type: \n")
    print(user_types, "\n")

    # Display counts of gender
    if city != 'washington':
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest = int(df["Birth Year"].min())
        most_recent_birth_year = int(df["Birth Year"].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest birth year: ", earliest, "\n")
        print("The most recent birth year: ", most_recent_birth_year, "\n")
        print("The most common birth year: ", most_common_birth_year, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    #Increase line break hyphens to 50 in user stat function of the Python file
    print('-'*50)

def display_raw_data(df):
    """ Your docstring here """
    input_message="\nWould you like to view 5 rows of individual trip data? Enter yes or no\n"
    start_loc = 0
    raw = input(input_message).lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            # appropriately subset/slice your dataframe to display next five rows
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            raw = input(input_message).lower() # convert the user input to lower case using lower() function
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        #display raw data every 5 rows at a time to improve user experience
        display_raw_data(df)

        #use lower() method to convert alphabets to lower case
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
