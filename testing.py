import requests

API_URL = "http://127.0.0.1:8000/jobs/"
VALID_KEY = "SECRET_KEY_123"
INVALID_KEY = "wrong_key"

# 1. TEST FĂRĂ CHEIE (Ar trebui să returneze 401)
print("--- Test 1: Fără API Key (401) ---")
response = requests.get(API_URL)
print(f"Status: {response.status_code}, Detalii: {response.json().get('detail')}")

# 2. TEST CU CHEIE INCORECTĂ (Ar trebui să returneze 401)
print("\n--- Test 2: API Key Incorectă (401) ---")
response = requests.get(API_URL, headers={"X-API-Key": INVALID_KEY})
print(f"Status: {response.status_code}, Detalii: {response.json().get('detail')}")

# 3. TEST DE SUCCES (Ar trebui să returneze 200)
print("\n--- Test 3: Succes (200) ---")
response = requests.get(API_URL, headers={"X-API-Key": VALID_KEY})
print(f"Status: {response.status_code}, Număr joburi: {len(response.json())}")

# 4. TEST DE THROTLLING (După 5 cereri ar trebui să returneze 429)
print("\n--- Test 4: Throttling (429) ---")
for i in range(1, 8):
    response = requests.get(API_URL, headers={"X-API-Key": VALID_KEY})
    if response.status_code == 429:
        print(f"La cererea {i}: Status {response.status_code}, Throttled!")
        break
    else:
        print(f"La cererea {i}: Status {response.status_code}, OK")


def add_new_job():
    api_key = input("Please enter the api key:")
    if api_key == VALID_KEY:
        print("Thank you! You can enter a job")
    else:
        print("Invalid API key!")
        return
    print("\n Add a New Job")
    print("Please enter the details for the new job:")

    title = input("Job Name:")
    while True:
        try:
            salary_str = input("Salary: ")
            salary = float(salary_str)
            break
        except ValueError:
            print("Invalid salary. Please enter a number")

    new_job_data = {
        "name": title,
        "salary": salary
    }

    try:
        response = requests.post(API_URL, json=new_job_data)
        #status code 200 OK, status code 201 Job Created
        if response.status_code in (200, 201):
            print("\nSuccessfully created new job!")
            print("New Job Data:", response.json())
        else:
            print(f"Error: Could not create job. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
add_new_job()