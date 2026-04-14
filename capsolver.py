import requests


def create_turnstile_task(api_key:str,site_key,website):
    if api_key.startswith("CAP"):
        url = "https://api.capsolver.com/createTask"
        tasktype="AntiTurnstileTaskProxyLess"
    else:
        pass
    payload = {
        "clientKey": api_key,
        "task": {
            "type": tasktype,
            "websiteURL": website,
            "websiteKey": site_key
        }
    }
    print(payload)
    response = requests.post(url, json=payload)
    print(response.json())
    if response.status_code == 200:
        return response.json()['taskId']
    else:
        return {"error": f"Request failed with status code {response.status_code}"}



def get_turnstile_response(task_id,api_key):
    if api_key.startswith("CAP"):

        url = "https://api.capsolver.com/getTaskResult"
    payload= {
                "clientKey": api_key, 
                "taskId": task_id
            }
    
    response = requests.post(url,json=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
        if data['status'] == "ready":
            return data['solution']['token']
        else:
            return False
        
def solve_dawn(api_key):
    filename="./static/screenshot.png"
    try:
        from twocaptcha import TwoCaptcha
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "twocaptcha is required only for Dawn CAPTCHA solving. "
            "Install it with `pip install 2captcha-python` or disable the Dawn flow."
        ) from exc

    solver = TwoCaptcha(api_key)
    result = solver.normal(filename)
    return (result)
