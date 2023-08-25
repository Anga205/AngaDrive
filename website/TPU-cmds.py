import requests, platform, os

'''if platform.system()=="Windows":
    token_path="..\\tokens"
else:
    token_path="../token"

if os.path.exists(token_path):
    token=open(token_path,"r").read().split("\n")[0]
else:
    token=input("Enter your TPU token: ")
    open(token_path, "w").write(token)

def get_stored_file_names()

    url = "https://images.flowinity.com/api/v3/gallery?page=1&search=&textMetadata=true&filter=all&sort=%22newest%22"

    # Assuming you need to include the token in the Authorization header
    params = {
        "Authorization": token,
        "accept": "application/json"
    }

    response = requests.get(url, headers=params)

    if response.status_code == 200:
        data = response.json()
        return [x["name"] for x in data["gallery"]]
    else:
        print(f"Request failed with status code: {response.status_code}")
'''
