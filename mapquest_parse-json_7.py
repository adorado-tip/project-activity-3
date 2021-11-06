import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

while True:
    orig = input(bcolors.HEADER + "Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break

    key = "ttn208CLFkY99sFH22IwgkigBsDKjEVQ"

    routeType = input("Which route type do you want to use? [fastest, shortest, pedestrian, bicycle]: ")
    language = input("Which language do you want to use? [en_US, fr_FR, de_DE, ru_RU]: " + bcolors.ENDC)

    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType, "locale": language})

    print(bcolors.OKBLUE + "URL: " + (url) + bcolors.ENDC)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
        print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
        print("=============================================\n")
        
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print(bcolors.OKBLUE + "https://developer.mapquest.com/documentation/directions-api/status-codes" + bcolors.ENDC)
        print("************************************************************************\n")



