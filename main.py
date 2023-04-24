import numpy as np
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

# Create a variable that will hold the API Key
# Create a variable that will hold the city name
# Create a dictionary that will store the info the user wants to store
apiKey = ''
cityName = ''
storageData = dict()


# Create a function that will fetch data based on the city name.
# The two parameters will represent the API key and city name
# Create a variable that will represent the url endpoint
def get_weather_info(user_key, city):
    url_endpoint = f"https://api.weatherapi.com/v1/current.json?key={user_key}&q={city}&aqi=no"
    requested_info = requests.get(url_endpoint)
    data = json.loads(requested_info.text)
    if 'error' in data.keys():
        print("There was an error found. Please make sure everything is entered correctly")
        print(data["error"]["message"])
        return False
    else:
        return data


# This function will transform the textfile data to a dataFrame
# It will allow the user to know more about the data
# Plot graph, get min , max, avg and etc...
def getMoreInsight():
    try:

        # Open the file
        f = open("textfile.txt", "r")
        # Read the file
        file_to_read1 = f.read()
        # Remove extra spaces
        file_to_read2 = file_to_read1.strip()
        # Convert the file to list based on the new line
        file_to_read3 = file_to_read2.split("\n")
        # Create 3 containers that will store values
        sample_set = set()
        sample_dic = dict()
        sample_list = list()
        # loop through the  list, replace the single quotes with double
        for x in file_to_read3:
            x2 = x.replace("'", '"')
            # convert each item to dictionary
            x3 = json.loads(x2)
            # Loop through each item and add the keys to a set
            for item in x3:
                sample_set.add(item)
        # Create a new list based on unique values the set
        # The new list will only contain unique keys
        for setItem in sample_set:
            sample_dic[setItem] = ""
        new_list = list()
        new_list.extend(sample_set)
        print(new_list)
        """ Create a function that will create a list 
            that will contain all the values of one key example: 'city': ["New York", "Boston"]
            This function then returns the list 
        """

        def get_items(key):
            for file_item in file_to_read3:
                file_item2 = file_item.replace("'", '"')
                file_item3 = json.loads(file_item2)
                sample_list.append(file_item3[key])
            return sample_list

        """ Loop through each unique keys from the list containing unique keys.
            Create a new key inside a dictionary we created earlier and 
            as value put the list containing all values based on that key
            """
        for listItem in new_list:
            sample_dic[listItem] = get_items(listItem)
            sample_list = []

        data_frame_storage = pd.DataFrame(sample_dic)
        print(data_frame_storage)
        x = np.array(data_frame_storage["City"])
        y = np.array(data_frame_storage["Weather"])
        plt.plot(x, y, 'o')
        font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
        font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
        plt.xlabel("Cities", fontdict=font1)
        plt.ylabel("Weather", fontdict=font2)
        plt.title("Weather Watch Data", fontdict=font2)

        print("Minimum weather", round(np.min(data_frame_storage["Weather"]), 2), "°C")
        print("Maximum weather", round(np.max(data_frame_storage["Weather"]), 2), "°C")
        print("Average weather", round(np.mean(data_frame_storage["Weather"]), 2), "°C")
        plt.show()
    except json.decoder.JSONDecodeError:
        print("File may be empty, does not exit or has been changed")
        print(json.decoder.JSONDecodeError)


# Create a function that will ask the user what info they want to store
# Use a try except to handle errors


print("Option 1: Get more insight about the file you created with this program")
print("Option 2: Run again")
print("Option 3: Quit")
def get_user_input():
    api_key = input("Enter your API key: ")
    city_name = input("Enter the name of the city: ")
    data_returned = get_weather_info(api_key, city_name)

    if not data_returned:
        exit()
    user_choices = [1, 2, 3]
    while True:
        if data_returned == "":
            exit()
        try:
            user_option = int(input("Enter your option: "))
        except:
            print("Please enter an integer")
        else:
            storageData["City"] = data_returned['location']['name']
            storageData["Weather"] = data_returned['current']['temp_c']
            storageData["Country"] = data_returned['location']['country']
            storageData["Condition"] = data_returned['current']['condition']['text']
            f = open("textfile.txt", "a")
            dict_data = str(storageData) + "\n"
            f.write(dict_data)
            f.close()
            if user_option not in user_choices:
                print("Please select an option between 1 - 3")

            elif user_option == 1:
                getMoreInsight()
                break
            elif user_option == 2:
                get_user_input()

            elif user_option == 3:
                print("Goodbye!")
                break


get_user_input()
