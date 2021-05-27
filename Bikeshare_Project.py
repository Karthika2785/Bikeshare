import time
import pandas as pd
import numpy as np
import calendar as cal
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    """
    Ask user to provide city for analysis

    Args : No agrument
    Returns :
            (str) city
    """
    countries = ['chicago','new york city','washington']
    while True:
        try:
            city = str(input("Please enter any one of these countries :chicago , new york city, washington\n"))
            if city.lower() in countries:
                break
            else:
                print("Please enter a valid country name:('chicago' or 'new york city' or 'washington')\n")
        except Exception  as e:
            print("Exception Occurred: {}".format(e))
    return city

def get_month():
    """
    Ask user to provide a month for analysis

    Args : No argument
    Returns:
            (str) month
    """
    while True:
        try:
            month = str(input("Please enter any one of 12 months (Eg:march,january,february....) or all :\n"))
            month = month.title()
            if month in cal.month_name[1:13] or month == 'All':
                break
            else:
                print("Please enter a valid month \n")
        except Exception as e:
            print("Exception Occurred: {}".format(e))
    return month

def get_day():
    """
    Ask user to provide a day for analysis

    Args: No argument
    Returns:
            (str) day
    """
    while True:
        try:
            day = str(input("Please enter any one of 7 days (Eg:monday,tuesday...) or all :\n"))
            day = day.title()
            if day in cal.day_name[0:] or day == "All":
                break
            else:
                print("Please enter a valid month\n")
        except Exception as e:
            print("Exception Occurred : {}".format(e))
    return day

def get_raw_data(df):
    """
    Ask user if they wish to see first 5 rows of data

    Args : dataframe(df)
    returns: does not return any values. It prints requested lines from data file.
    """
    option = str(input('Would you like to see first 5 rows of the data file?: Yes or No\n'))
    if option.title() == 'Yes':
        print(df.head(5))
        option = str(input('Want to see 5 more rows?: Yes or No\n'))
        if option.title() == 'Yes':
            print(df[5:10])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city -  name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

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
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    # convert the Start Time column to datetime
    #giving option to see raw data
    get_raw_data(df)
    print("Below are the records for month - {} and day - {} in country - {}!!!\n".format(month,day,city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month Number'] = df['Start Time'].dt.month
    df['weekday name'] = df['Start Time'].dt.day_name()
    month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',
                          10:'October',11:'November',12:'December'}
    # creating new column for Month name
    df['Month Name'] = df['Month Number'].map(month_dict)
    # filter by month if applicable
    if month != 'All':
        df = df[df['Month Name'] == month.title()]
        if df.empty == True:
            print("Sorry! we have no data or records for this month.\n")
            option = str(input("Want to enter different month? Yes or No.\n"))
            if option.title() == 'Yes':
                month = get_month()
                df = load_data(city,month,day)

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df [df['weekday name'] == day.title()]
        if df.empty == True:
            print("Sorry! we have no data or records for this day.\n")
            option = str(input("Want to enter different day? Yes or No. \n"))
            if option.title() == 'Yes':
                day = get_day()
                df = load_data(city,month,day)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args: Dataframe(df)

    Returns: Nothing

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month Name'].mode()[0]
    print("The most common month from filtered data is : {}".format(common_month))

    # display the most common day of week
    common_day = df['weekday name'].mode()[0]
    print("The most common day of week from filtered data is : {}".format(common_day))

    # display the most common start hour
    freq_hour = df['Start Time'].dt.hour
    freq_hour = freq_hour.dropna()
    print("The most common start hour is : ",freq_hour.value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args: Dataframe(df)
    Returns: Nothing

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_st = df['Start Station'].mode()[0]
    print("The most common start station from filtered data is : {}".format(common_start_st))

    # display most commonly used end station
    common_end_st = df['End Station'].mode()[0]
    print("The most common end station from filtered data is : {}".format(common_end_st))


    # display most frequent combination of start station and end station trip\
    common_start_end = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most frequent combination of start and end station is : {}".format(common_start_end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum(),2)
    hr_total_time = round(total_travel_time/60,2)
    day_total_time = round(hr_total_time/24,2)
    print("The total travel time is : {}(mins), {}(hrs),{}(days)".format(total_travel_time,hr_total_time,day_total_time))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(),2)
    hr_mean_time = round(mean_travel_time/60,2)
    day_mean_time = round(hr_mean_time/24,2)
    print("The mean travel time is : {} (mins),{}(hours),{}(days)".format(mean_travel_time,hr_mean_time,day_mean_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
    Args: Dataframe (df), str(city)

    Returns : Nothing

    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df.groupby(['User Type']).size()
    print("The user type counts are :\n{}".format(user_type_count))

    # Display counts of gender
    if city.lower() != 'washington':
        gender_count = df.groupby('Gender').size()
        print("\n\nNumber of Male and Female :\n{}".format(gender_count))
    else:
        print("Sorry!!! City - Washington does not have Gender data.\n")

    # Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        common_birth_yr = int(df['Birth Year'].mode()[0])
        earliest_yr = int(df['Birth Year'].min())
        recent_yr = int(df['Birth Year'].max())
        print("The most common year of birth is : {}\n".format(common_birth_yr))
        print("Earliest year of birth is : {}\n".format(earliest_yr))
        print("The most recent year of birth is :  {}\n".format(recent_yr))
    else:
        print("Sorry!!! City - Washington does not have Birth year data. \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
