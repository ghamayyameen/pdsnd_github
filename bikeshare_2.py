import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def choice_handler(*args):
    """Gives the user a display to choose from the keyword arguments.

    Returns:
        str: One of the keyword arguments.
    """
    
    choices=list(args)
    
    while(True):
        print("")
        for i in range(len(choices)):
            print(i+1, ". ", choices[i], sep='')
        select= int(input("Enter the number of the option > "))
        if select>0 and select<=(len(choices)):
            break
        print("\nIncorrect input!")

    return choices[select-1]


def yn_to_bool(question: str):
    """Displays a question, and changes the answer to a boolean.

    Args:
        question (str): The question to be used.

    Returns:
        bool: converted answer.
    """
    
    while True:
        
        choice= input(question+ " yes/no >").title()
        if choice=='Yes':
            return True
        elif choice=='No':
            return False
        else:
            print("Incorrect input")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    months=["all", "january", "february", "march", "april", "may", "june"]
    days=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = choice_handler("chicago",
                   "new york city",
                   "washington")

    # get user input for month (all, january, february, ... , june)
    month = choice_handler(*months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = choice_handler(*days)

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
    

    df = pd.read_csv(CITY_DATA[str(city)])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'Mmay', 'June']
#         month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month']==month.title()]
        
    # filter by day of week if applicable
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: ", df.mode()['month'][0])

    # display the most common day of week
    print("Most common day of the week: ", df.mode()['day_of_week'][0])

    # display the most common start 
    df['hour']=df["Start Time"].dt.hour
    print("Most common hour: ", df.mode()['hour'][0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: ", df.mode()['Start Station'][0])

    # display most commonly used end station
    print("Most commonly used end station: ", df.mode()['End Station'][0])

    # display most frequent combination of start station and end station trip
    df['station combination']=df['Start Station'] + ' - ' + df['End Station']
    print("Most commonly combination of start-end station: ", df.mode()['station combination'][0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total of", df.sum(numeric_only=True)['Trip Duration']/360, " hours of travel time.")

    # display mean travel time
    print("Mean travel time of", df.mean(numeric_only=True)['Trip Duration']/360, " hours.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print("There is no gender data!")
        
    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest date of birth is:", df['Birth Year'].min())
        print("Most recent date of birth is:", df['Birth Year'].max())
        print("Most common date of birth is:", df['Birth Year'].mode()[0])
    except KeyError:
        print("There is not date of birth data!")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    pd.set_option("display.max_columns",200)
    do=yn_to_bool("Do you want to view the raw data?")
    if do:
        index=0
        while index < len(df)+5:
            print(df[index:index+5])
            contin = yn_to_bool("Do you want to view mode lines?")
            if contin:
                index+=5
            else:
                break
        print("End.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # input(df)
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
