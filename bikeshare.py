import time
import pandas as pd
import numpy as np

# Welcome to this simple Python program used to explore US Bikeshare data. In combination with the csv files mentioned below, this will run in your command line.

# KT - Dictionary to hold the data sources for the cities
CITY_DATA = {'chicago': 'chicago.csv',
			 'new york city': 'new_york_city.csv',
			 'washington': 'washington.csv'}


def get_filters():
	""" Asks user to specify a city, month, and day to analyze.
	Returns:
	(str) city - name of the city to analyze
	(str) month - name of the month to filter by, or "all" to apply no month filter
	(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""
	print("\nHi there! Let\'s explore some US bikeshare data together!\nLet's begin.")

	# KT - while loops to acquire inputs to filter by city, month and day
	while True:
		city = input("\nFirst, please specify which city you're interested in: Chicago, New York City, or Washington (not case sensitive): ").strip().strip("'").lower()
		if city == 'chicago' or city == 'new york city' or city == 'washington':
			print("\nGreat, thanks!")
			break
		else:
			print("\nOops, something doesn\'t look right! Double check your input and try again")
	while True:
		month = input("Do you want to see data for a specific month? If so, please enter the full name, e.g. 'January', 'february' (not case sensitive). If not, enter 'all':  ").strip().strip("'").lower()
		if month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all':
			print("\nPerfect, thank you.")
			break
		else:
			print("\nOops, something doesn\'t look right! Double check your input and try again")
	while True:
		day = input("Are you looking to view data for a specific day of the week? If so, please enter the full name, e.g. Monday, tuesday (not case sensitive). If not, enter 'all': ").strip().strip("'").lower()
		if day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all':
			print("\nNice one.")
			break
		else:
			print("\nOops, something doesn\'t look right! Double check your input and try again")


	print('-'*80)
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
	# KT - loading the data for the city from the csv
	df = pd.read_csv(CITY_DATA[city])

	# KT - convert the 'Start Time' column to datetime
	df['Start Time'] = pd.to_datetime(df['Start Time'])

	# KT - extract the month, day of the week and hour from the 'Start Time' column to create 3 new columns
	df['month'] = df['Start Time'].dt.month
	df['weekday'] = df['Start Time'].dt.dayofweek
	df['hour'] = df['Start Time'].dt.hour

	# KT - create the station start-end combination column
	df['Start End Combo'] = df['Start Station'] + " to " + df['End Station']

	# KT - define the months list
	months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

	# KT - define the days dictionary
	days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6, 'all':7}

	# KT - defining month number via the index plus 1, e.g. February is index 1, plus 1 = month number 2
	month_num = int(months.index(month) + 1)

	# KT - defining the day number
	day_num = int(days[day])

	if month != 'all':
		df = df[df['month'] == month_num]
	if day != 'all':
		df = df[df['weekday'] == day_num]
	return df


def time_stats(df, month, day):
	"""Displays statistics on the most frequent times of travel."""

	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()

	# KT done -- TO DO: display the most common month

	if month == "all":
		pop_month_num = df['month'].mode()[0]
		print("\nThe most common travel month is: ", pop_month_num)

	# KT done -- TO DO: display the most common day of week

	if day == 'all':
		pop_day_num = df['weekday'].mode()[0]
		print("\nThe most common travel day is: ", pop_day_num)
		# KT done -- TO DO: display the most common start hour
		pop_hour = df['hour'].mode()[0]
		print("\nThe most frequent start hour is: ", pop_hour)

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*80)


def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""

	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()

	# KT done -- TO DO: display most commonly used start station
	common_start_station = df['Start Station'].mode()[0]
	print(f"\nThe most commonly used start station is {common_start_station}")

	# KT done -- TO DO: display most commonly used end station
	common_end_station = df['End Station'].mode()[0]
	print(f"\nThe most commonly used end station is {common_end_station}")

	# KT done -- TO DO: display most frequent combination of start station and end station trip
	df['combination'] = df['Start Station'] + " to " + df['End Station']
	print('\nThe most combination of start station and end station trip is\n {}'.format((df['combination'].mode()[0])))


	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*80)


def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()

	# KT done -- TO DO: display total travel time
	# KT - calculates sum of trip duration, in seconds
	total_travel_time = df['Trip Duration'].sum()

	# KT - gets the duration in minutes and seconds format
	minute, second = divmod(total_travel_time, 60)
	# KT - gets the duration in hours and minutes format
	hour, minute = divmod(minute, 60)
	print(f"\n The total duration of all trips is {hour} hours, {minute} minutes and {second} seconds.")

	# KT done -- TO DO: display mean travel time
	# KT - calculates the average trip duration using the mean method (and rounding to prevent issues in calculating hours, mins and secs)
	avg_duration = round(df['Trip Duration'].mean())

	# KT - finds the average duration in minutes and seconds format
	mins, sec = divmod(avg_duration, 60)

	# KT - the following filter prints the time in hours, mins and secs format if the duration in minutes is 60 or higher
	if mins >= 60:
		hrs, mins = divmod(mins, 60)
		print(f"\n The mean trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
	else:
		print(f"\n The mean trip duration is {mins} minutes and {sec} seconds.")

	# KT done -- TO DO: display median travel time
	# KT - calculates the average trip duration using the mean method (and rounding to prevent issues in calculating hours, mins and secs)
	med_duration = round(df['Trip Duration'].median())

	# KT - finds the average duration in minutes and seconds format
	mins, sec = divmod(med_duration, 60)

	# KT - the following filter prints the time in hours, mins and secs format if the duration in minutes is 60 or higher
	if mins >= 60:
		hrs, mins = divmod(mins, 60)
		print(f"\n The median trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
	else:
		print(f"\n The median trip duration is {mins} minutes and {sec} seconds.")

	# KT done -- TO DO: display max travel time
	# KT - calculates the max trip duration using the max method
	max_duration = round(df['Trip Duration'].max())

	# KT - finds the max duration in minutes and seconds format
	mins, sec = divmod(max_duration, 60)

	# KT - the following filter prints the time in hours, mins and secs format if the duration in minutes is 60 or higher
	if mins >= 60:
		hrs, mins = divmod(mins, 60)
		print(f"\n The longest trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
	else:
		print(f"\n The longest trip duration is {mins} minutes and {sec} seconds.")

	# KT done -- TO DO: display min travel time
	# KT - calculates the min trip duration using the min method
	min_duration = round(df['Trip Duration'].min())

	# KT - finds the max duration in minutes and seconds format
	mins, sec = divmod(min_duration, 60)

	# KT - the following filter prints the time in hours, mins and secs format if the duration in minutes is 60 or higher
	if mins >= 60:
		hrs, mins = divmod(mins, 60)
		print(f"\n The shortest trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
	else:
		print(f"\n The shortest trip duration is {mins} minutes and {sec} seconds.")

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*80)


def user_stats(df):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

	# KT done -- TO DO: Display counts of user types

	# KT - the total users are counted below and then displayed
	user_type = df['User Type'].value_counts()

	print(f"\n The types and numbers of users are given below:\n\n{user_type}")

	# KT done -- TO DO: Display counts of gender

	# KT - the try clause attempts to display the number of users by gender, and shows an alternative message if the column does not exist in the dataframe
	try:
		gender = df['Gender'].value_counts()
		print(f"\n The types of users by gender are as follows:\n\n{gender}")
	except:
		print("\nThis file has no 'Gender' column, so this data is unavailable.")


	# KT done -- TO DO: Display earliest, most recent, and most common year of birth

	# KT - the try clause attempts to display the birth years, and shows an alternative message if the column does not exist in the dataframe

	try:
		earliest_birth_year = int(df['Birth Year'].min())
		most_recent_birth_year = int(df['Birth Year'].max())
		most_common_birth_year = int(df['Birth Year'].mode()[0])
		print(f"\n The earliest birth year is {earliest_birth_year}.\n The most recent birth year is {most_recent_birth_year}.\n The most common birth year is {most_common_birth_year}.")
	except:
		print("\nThis file has no 'Birth Year' column, so this data is unavailable.")


	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*80)

#Function to display the data frame itself as per user request
def display_data(df):
	"""Displays 5 rows of data from the csv file for the selected city.

	Args:
		param1 (df): The data frame you wish to work with.

	Returns:
		None.
	"""
	# KT - list of acceptable responses
	response_list = ['yes', 'no']
	response_data = ''
	# KT - row_counter variable used to ensure only data from a specific point is displayed
	row_counter = 0
	while response_data not in response_list:
		print("\nDo you wish to view the first 5 rows of raw data?")
		print("\nAccepted responses (not case sensitive):\nYes\nNo")
		response_data = input().lower()
		# KT - if yes, the first 5 rows of the dataframe are displayed
		if response_data == "yes":
			print(df.head())
		elif response_data not in response_list:
			print("\nOops, something doesn\'t look right! Double check your input and try again")
			print("\nRestarting...\n")

	# KT - additional while loop to ask users if they wish to continue viewing more data
	while response_data == 'yes':
		print("Do you wish to view more raw data?")
		row_counter += 5
		response_data = input().lower()
		# KT - if the user opts for it, this displays next 5 rows of data
		if response_data == "yes":
			 print(df[row_counter:row_counter+5])
		elif response_data != "yes":
			 break

	print('-'*80)

def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)

		display_data(df)
		time_stats(df, month, day)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)

		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
