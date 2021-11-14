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

while True:
    orig = input(bcolors.HEADER + "Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break

    key = "ttn208CLFkY99sFH22IwgkigBsDKjEVQ"

    routeDecision = input("""Which route type do you want to use? Choose the number next to your answer.
[1] Quickest drive time route
[2] Shortest driving distance route
[3] Walking route
[4] Will only use roads on which bicycling is appropriate
: """)
    if routeDecision == "1":
        routeType = "fastest"
    elif routeDecision == "2":
        routeType = "shortest"
    elif routeDecision == "3":
        routeType = "pedestrian"
    elif routeDecision == "4":
        routeType = "bicycle"
        
    if routeType == "fastest" or routeType == "shortest":
        styleDecision = input("Would you like to input your driving style for the accurate calculation of your fuel usage? If no, normal driving style will be assumed. [yes/no]: ")
        if styleDecision == "yes":
            styleChoice = input("""Which type of driver are you? Choose the number next to your answer.
[1] Cautious Driver
[2] Normal Driver
[3] Aggressive Driver
: """)
            drivingStyle = styleChoice

        elif styleDecision == "no":
            drivingStyle = 2

        avoidDecision = input("Is there any type of road would you like to avoid? [yes/no]: ")
        if avoidDecision == "yes":
            avoidChoice = input("""Which road would you like to avoid? Choose the number next to your answer.
[1] Limited Access Highway
[2] Toll Road
[3] Unpaved Road
[4] Bridge
[5] Tunnel
: """)
            if avoidChoice == "1":
                avoid = "Limited Access"
            elif avoidChoice == "2":
                avoid = "Toll Road"
            elif avoidChoice == "3":
                avoid = "Unpaved"
            elif avoidChoice == "4":
                avoid = "Bridge"
            elif avoidChoice == "5":
                avoid = "Tunnel"

            language = input("Which language do you want to use? [en_US, fr_FR, de_DE, ru_RU]: ")

            url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType, "locale":language, "avoids":avoid, "drivingStyle":drivingStyle})

        elif avoidDecision == "no":
            language = input("Which language do you want to use? [en_US, fr_FR, de_DE, ru_RU]: ")

            url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType, "locale":language, "drivingStyle":drivingStyle})

    elif routeType == "bicycle":
        bikeDecision = input("Would you like to use a road grade strategy? [yes/no]: ")
        if bikeDecision == "yes":
            bikeChoice = input("""Which road grade strategy would you like to use? Choose the number next to your answer.
[1] Avoid uphill road grades
[2] Avoid downhill road grades
[3] Avoid all hill road grades
[4] Favor uphill road grades
[5] Favor downhill road grades
[6] Favor all hill road grades
: """)
            if bikeChoice == "1":
                roadGradeStrategy = "AVOID_UP_HILL"
            elif bikeChoice == "2":
                roadGradeStrategy = "AVOID_DOWN_HILL"
            elif bikeChoice == "3":
                roadGradeStrategy = "AVOID_ALL_HILLS"
            elif bikeChoice == "4":
                roadGradeStrategy = "FAVOR_UP_HILL"
            elif bikeChoice == "5":
                roadGradeStrategy = "FAVOR_DOWN_HILL"
            elif bikeChoice == "6":
                roadGradeStrategy = "FAVOR_ALL_HILLS"

        elif bikeDecision == "no":
            roadGradeStrategy = "DEFAULT_STRATEGY"

        language = input("Which language do you want to use? [en_US, fr_FR, de_DE, ru_RU]: ")

        url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType, "locale":language, "roadGradeStrategy":roadGradeStrategy})

    else:
        language = input("Which language do you want to use? [en_US, fr_FR, de_DE, ru_RU]: ")
        url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest, "routeType":routeType, "locale":language})
    bcolors.ENDC
    
    print(bcolors.OKBLUE + "URL: " + (url) + bcolors.ENDC)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print(bcolors.OKGREEN + "API Status: " + str(json_status) + " = A successful route call.\n" + bcolors.ENDC)
        print("=============================================")
        print(bcolors.OKCYAN + "Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
        print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))+ bcolors.ENDC)
        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(bcolors.OKGREEN + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)" + bcolors.ENDC))
        print("=============================================\n")
        
    elif json_status == 402:
        print("**********************************************")
        print(bcolors.FAIL + "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations." + bcolors.ENDC)
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print(bcolors.WARNING + "Status Code: " + str(json_status) + "; Missing an entry for one or both locations." + bcolors.ENDC)
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print(bcolors.FAIL + "For Staus Code: " + str(json_status) + "; Refer to:" + bcolors.ENDC)
        print(bcolors.OKBLUE + "https://developer.mapquest.com/documentation/directions-api/status-codes" + bcolors.ENDC)
        print("************************************************************************\n")



