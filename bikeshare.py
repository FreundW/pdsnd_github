import time
import pandas as pd

MONTH2NUM = { 'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'all': -1}

NUM2MONTH = { 1: 'january',
              2: 'february',
              3: 'march',
              4: 'april',
              5: 'may',
              6: 'june'}

DAY2NUM = { 'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
            'all': -1}

NUM2DAY = { 0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'}

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
    city = ''
    while not city in ['chicago', 'new york', 'washington']:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n' ).lower()
        if not city in ['chicago', 'new york', 'washington']:
            print('It looks like some typo occurred and I cannot resolve the given input. Please check and chose a valid city.')

    filter = ''
    while not filter in ['month', 'day', 'both', 'none']:
        filter = input('Would you like to filter the data by \'month\', \'day\', \'both\', or not at all? Enter \'none\' for no time filters.\n' ).lower()

    # get user input for month (all, january, february, ... , june)
    month = 'all'
    if filter in ['month', 'both']:
        while not month in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('Would you like to see data for January, February, March, April, May, June?\n' ).lower()
            if not month in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('It looks like some typo occurred and I cannot resolve the given input. Please check and chose a valid month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'all'
    if filter in ['day', 'both']:
        while not day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('Would you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n' ).lower()
            if not day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print('It looks like some typo occurred and I cannot resolve the given input. Please check and chose a valid day.')

    if filter == 'none':
        month = day = 'all'

    print(('Your data will be processed for following City: {c} filtered by Month: {m}, Day: {d}').format(c=city.title(),
                                                                                                          m=month.title(),
                                                                                                          d=day.title()))

    print('-'*40)

    if city == 'new york':
        city = 'new_york_city'

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

    df = pd.read_csv(('{name}.csv').format(name=city))
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['weekday'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    month = MONTH2NUM[month]
    day = DAY2NUM[day]

    if not month == -1:
        df = df.loc[df['month'] == month]
    if not day == -1:
        df = df.loc[df['weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts()
    print(('Most Popular Month: {m} with a count of: {c}').format(m=NUM2MONTH[popular_month.index[0]], c=str(popular_month.values[0])))

    # display the most common day of week
    popular_day = df['weekday'].value_counts()
    print(('Most Popular Weekday: {w} with a count of: {c}').format(w=NUM2DAY[popular_day.index[0]], c=str(popular_day.values[0])))

    # display the most common start hour
    ## find the most popular hour
    popular_hour = df['hour'].value_counts()
    print(('Most Popular Start Hour: {h} with a count of: {c}').format(h=popular_hour.index[0], c=str(popular_hour.values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_staion = df['Start Station'].value_counts()
    print(('Most commonly used Start Station: {s} with a count of: {c}').format(s=popular_start_staion.index[0], c=str(popular_start_staion.values[0])))

    # display most commonly used end station
    popular_end_staion = df['End Station'].value_counts()
    print(('Most commonly used End Station: {s} with a count of: {c}').format(s=popular_end_staion.index[0], c=str(popular_end_staion.values[0])))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].value_counts()
    print(('Most frequent combination of Start Station and End Station:: {s} with a count of: {c}').format(s=popular_trip.index[0],
                                                                              c=str(popular_trip.values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time amounts to: ', time.strftime("%Hh %Mmin %Ssec", time.gmtime(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time amounts to: ', time.strftime("%Hh %Mmin %Ssec", time.gmtime(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of the different User Types: ')
    print(user_types.to_string(index=True))

    # Display counts of gender
    print('\nGender count of the Users:')
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender.to_string(index=True))
    else:
        print('\nSorry, No Gender Information contained in Data!')

    # Display earliest, most recent, and most common year of birth
    print('\nDeeper information on Birth Years of the Users:')
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        print('Earliest Year of Birth: ', str(earliest))
        most_recent = int(df['Birth Year'].max())
        print('Most Recent Year of Birth: ', str(most_recent))
        most_common = int(df['Birth Year'].mode()[0])
        print('Most Common Date of Birth:', str(most_common))
    else:
        print('\nSorry, No Birth Year Information contained in Data!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_output(df):
    """Offers the possibility to print raw data used for evaluation"""
    print('\nDisplay of raw data if wanted...\n')
    rows = 0
    df = df.drop(['month', 'weekday', 'hour', 'trip'], axis=1)
    df = df.reset_index(drop=True)
    while True:
        raw_data = input('Would you like to see five rows of the raw data used for the evaluation? Enter yes or no.\n').lower()
        if raw_data == 'yes':
            print(df.loc[rows:rows+4,:].to_string())
            rows += 5
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

        raw_data_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
