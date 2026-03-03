import requests
import os
import datetime as dt

today = dt.datetime.now().strftime("%Y%m%d")

pixela_url = "https://pixe.la"
pixela_endpoint = f"{pixela_url}/v1/users"
graphs_endpoint = f"{pixela_endpoint}/{os.getenv("PIXELA_USERNAME")}/graphs"
pull_ups_graph_endpoint = f"{graphs_endpoint}/{os.getenv("PIXELA_PULL_UPS_GRAPH_ID")}"
dips_graph_endpoint = f"{graphs_endpoint}/{os.getenv("PIXELA_DIPS_GRAPH_ID")}"
pistols_graph_endpoint = f"{graphs_endpoint}/{os.getenv("PIXELA_PISTOLS_GRAPH_ID")}"
pull_ups_graph_update_endpoint = f"{graphs_endpoint}/{os.getenv("PIXELA_PULL_UPS_GRAPH_ID")}/{today}"
# https://pixe.la/@testoviron


########################################################################
##                          CREATE ACCOUNT                            ##
########################################################################

# parameters = {
#     "username": os.getenv("PIXELA_USERNAME"),
#     "token": os.getenv("PIXELA_TOKEN"),
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes"
# }

# response = requests.post(url=pixela_endpoint, json=parameters)
# print(response.text)


########################################################################
##                           CREATE GRAPHS                            ##
########################################################################

# parameters = {
#     "id": os.getenv("PIXELA_PULL_UPS_GRAPH_ID"),
#     "name": os.getenv("PIXELA_PULL_UPS_GRAPH_NAME"),
#     "unit": "reps",
#     "type": "int",
#     "color": "shibafu",
#     "timezone": "Europe/Warsaw"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=graphs_endpoint, json=parameters, headers=headers)
# print(response.text)

# parameters = {
#     "id": os.getenv("PIXELA_DIPS_GRAPH_ID"),
#     "name": os.getenv("PIXELA_DIPS_GRAPH_NAME"),
#     "unit": "reps",
#     "type": "int",
#     "color": "momiji",
#     "timezone": "Europe/Warsaw"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=graphs_endpoint, json=parameters, headers=headers)
# print(response.text)

# parameters = {
#     "id": os.getenv("PIXELA_PISTOLS_GRAPH_ID"),
#     "name": os.getenv("PIXELA_PISTOLS_GRAPH_NAME"),
#     "unit": "reps",
#     "type": "int",
#     "color": "sora",
#     "timezone": "Europe/Warsaw"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=graphs_endpoint, json=parameters, headers=headers)
# print(response.text)


########################################################################
##                            ADD PIXELS                              ##
########################################################################

# parameters = {
#     "date": today,
#     "quantity": "32"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=pull_ups_graph_endpoint, json=parameters, headers=headers)
# print(response.text)

# parameters = {
#     "date": today,
#     "quantity": "40"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=dips_graph_endpoint, json=parameters, headers=headers)
# print(response.text)

# parameters = {
#     "date": today,
#     "quantity": "16"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.post(url=pistols_graph_endpoint, json=parameters, headers=headers)
# print(response.text)


########################################################################
##                           UPDATE PIXELS                            ##
########################################################################

# parameters = {
#     "quantity": "24"
# }

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.put(url=pull_ups_graph_update_endpoint, json=parameters, headers=headers)
# print(response.text)


########################################################################
##                           DELETE PIXELS                            ##
########################################################################

# headers = {
#     "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
# }

# response = requests.delete(url=pull_ups_graph_update_endpoint, headers=headers)
# print(response.text)
