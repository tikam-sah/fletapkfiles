#import logging
#import sys

#logging.basicConfig(level=logging.DEBUG)


invalid_user_password = "Invalid username or password."
internal_error = "An error occurred. Please try again."
fill_user_pass = "Please fill in both fields."
error_update = "Unable to update the leads at this moment.Please try again later"

API_LOGOUT_URL = 'https://marketing.binayahcapital.com/api/agents_logout'
API_LEAD_LIST_URL = 'https://marketing.binayahcapital.com/api/app_get_lead_id'
API_UPDATE_STATUS_URL = 'https://marketing.binayahcapital.com/api/create_leads_status'

def page_title(page):
    page.bgcolor = "#004e41"
    page.title = "Login Page"

def dashboard_title(page):
    page.bgcolor = "#004e41"  
    page.title = "Dashboard" 

def headers_auth(auth):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+ auth
    }
    return headers 

def site_logo(ft):
    return ft.Container(content=ft.Image(src="assets/logo.png", width=200, height=100),alignment=ft.alignment.center)

def bottom_nav(ft):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("© 2024 Binayah Properties", color=ft.colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER, spacing=20   
        ),
        bgcolor="#cdaa52", padding=10
       
    )

def user_leads(page,headers,req,ft):
    user_number = page.client_storage.get("user_number")
    payload = {"agent_number": user_number}
    try:
        response = req.post(API_LEAD_LIST_URL, headers=headers, json=payload)
        if response.status_code == 200:
            json_data = response.json() 
            lead_data = json_data.get('data', {}) 
            return ft.Dropdown(label="Select Lead ID", bgcolor="#fcfcfc", options=[ft.dropdown.Option(item) for item in lead_data])         
    except Exception as e:
        return internal_error
    
    
def user_leads_options(page,headers,req):
    user_number = page.client_storage.get("user_number")
    payload = {"agent_number": user_number}
    try:
        response = req.post(API_LEAD_LIST_URL, headers=headers, json=payload)
        if response.status_code == 200:
            json_data = response.json() 
            lead_data = json_data.get('data', {}) 
            return lead_data        
    except Exception as e:
        return internal_error


def user_logout(page,headers,req):
    user_id = page.client_storage.get("user_id")
    payload = {"id": user_id}
    try:
        response = req.post(API_LOGOUT_URL, headers=headers, json=payload)
        if response.status_code == 200:
            page.client_storage.clear()
            page.controls.clear()
            return 'success'
        else:
            return internal_error
    except Exception as e:
        return internal_error

def update_lead_status(page,headers,req,lead_id,status,sub_status,comment):
    agent_number = page.client_storage.get("user_number")
    payload ={  "agent_number":agent_number, "lead_id": lead_id, "status": status,  "sub_status":sub_status, "comment": comment }
    try:
        response = req.post(API_UPDATE_STATUS_URL, headers=headers, json=payload)
        if response.status_code == 200:
            json_data = response.json() 
            res = json_data.get('status_code', {})  
            if(res ==200):
                #page.controls.clear()
                return 'success'
            else:
                return error_update
        else:
            return internal_error
    except Exception as e:
        return internal_error
    
def status_list(ft):
    return ft.Dropdown(label="Select Status", bgcolor="#fcfcfc", options=[
        ft.dropdown.Option("Open"),
        ft.dropdown.Option("Closed"),
        ft.dropdown.Option("Not Specified"),
    ])

def sub_status_list(ft):
    return ft.Dropdown(label="Select Sub Status", bgcolor="#fcfcfc", options=[
            ft.dropdown.Option("Duplicate"),
            ft.dropdown.Option("In Progress"),
            ft.dropdown.Option("Successful"),
            ft.dropdown.Option("Unsuccessful"),
            ft.dropdown.Option("Not Yet Contacted"),
            ft.dropdown.Option("Follow up"),
            ft.dropdown.Option("Viewing arranged"),
            ft.dropdown.Option("Not specified"),
            ft.dropdown.Option("Offer made"),
            ft.dropdown.Option("Needs more info"),
            ft.dropdown.Option("Budge differs"),
            ft.dropdown.Option("Needs time"),
            ft.dropdown.Option("Client to revert"),
            ft.dropdown.Option("Interested"),
            ft.dropdown.Option("Interested to meet"),
            ft.dropdown.Option("Not interested"),
            ft.dropdown.Option("Look-see"),
            ft.dropdown.Option("Not interested"),
            ft.dropdown.Option("Client contacted online to agent"),
            ft.dropdown.Option("SMS sent to agent"),
            ft.dropdown.Option("Email sent to agent"),
            ft.dropdown.Option("Client not reachable"),
            ft.dropdown.Option("Incorrect contact details"),
            ft.dropdown.Option("Invalid enquiry"),
            ft.dropdown.Option("Price too high"),
            ft.dropdown.Option("Viewing Done"),
        ])

def comment_box(ft):
    return ft.TextField(label="Comments", hint_text="Enter your comments here...", multiline=True, bgcolor="#fcfcfc",  width=450, height=50)






    
