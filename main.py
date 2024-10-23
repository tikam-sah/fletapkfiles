import flet as ft
import requests as req
import define as d

API_TOKEN_URL = 'https://marketing.binayahcapital.com/api/lead_token'
API_LOGIN_URL = 'https://marketing.binayahcapital.com/api/agents_login'

def get_api_token():
    response = req.post(API_TOKEN_URL)
    token = response.json().get("token")
    return token

headers = d.headers_auth(get_api_token())

def main(page: ft.Page):
    user_name = page.client_storage.get("user_name")
    if user_name:
        page.controls.clear()
        dashboard(page)
    else:
        d.page_title(page)
        logo = d.site_logo(ft)  # Create the logo and center it using a Container
        # Create username and password text fields
        username = ft.TextField(label="Username", width=300, bgcolor="#fcfcfc")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, bgcolor="#fcfcfc")
        error_message = ft.Text("", color=ft.colors.RED)     # Create a Text element for error messages

        # Create a submit button with custom color
        submit_button = ft.ElevatedButton(
            text="Submit", color="#ffffff", bgcolor="#cdaa52",  on_click=lambda e: submit(page, username.value, password.value, error_message)
        )
        # Create a container to hold the login form elements
        login_form = ft.Column(
            controls=[logo, username, password,error_message, submit_button ],      
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
        )
        # Add the login form to the page
        page.add(
            ft.Container(
                content=login_form,
                alignment=ft.alignment.center,
                padding=20,
                bgcolor=ft.colors.TRANSPARENT,
                border_radius=10,
                width=400,
                height=400,
            )
        )

def submit(page, username, password, error_message):
    if not username or not password:
        error_message.value = d.fill_user_pass
    else:
        error_message.value = ""
        payload = {"username": username, "password": password}
        try:
            response = req.post(API_LOGIN_URL, headers=headers, json=payload)
            if response.status_code == 200:
                json_data = response.json()  
                user_data = json_data.get('data', {})

                page.client_storage.set("user_id", user_data.get('id', {}))
                page.client_storage.set("user_name", user_data.get('name', {}))
                page.client_storage.set("user_username", user_data.get('username', {}))
                page.client_storage.set("user_number", user_data.get('contact_number', {}))
                page.client_storage.set("user_is_logged_in", user_data.get('is_loggedin', {}))
                page.client_storage.set("user_email", user_data.get('email', {}))
                page.client_storage.set("user_status", user_data.get('status', {}))

                page.controls.clear()
                dashboard(page)
            else:
                error_message.value = d.invalid_user_password
        except Exception as e:
            error_message.value =  d.internal_error
            
    # Update the UI
    error_message.update()

def thank_you_page(page: ft.Page):
    page.controls.clear()
    logo = d.site_logo(ft)  
    thank_you = ft.Text("Thank You", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    thank_you_message_1 = ft.Text("Your Status Has",   size=18, weight=ft.FontWeight.BOLD, color="#C0C0C0")
    thank_you_message_2 = ft.Text("Been Updated Successfully",  size=18, weight=ft.FontWeight.BOLD, color="#C0C0C0")
    return_button = ft.ElevatedButton( text="Return to Dashboard",  bgcolor="#cdaa52", color=ft.colors.WHITE,  on_click=lambda e: dashboard(page)     
    )

    # Create a container for the thank you page content
    thank_you_content = ft.Column(
        controls=[  logo,thank_you, thank_you_message_1,thank_you_message_2,return_button ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    # Add the thank you content to the page
    page.add(
        ft.Container(
            content=thank_you_content,
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.colors.TRANSPARENT,
            border_radius=10,
            width=400,
            height=450,
        )
    )

def dashboard(page: ft.Page):
    page.controls.clear()
    d.dashboard_title(page)
    # Create the top navigation bar
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    "Welcome, " + page.client_storage.get("user_name"),
                    on_click=lambda e: print("Home clicked"),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE 
                    )
                ),
                ft.TextButton(
                    "Logout",
                    on_click=lambda e: logout(page),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE  
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        bgcolor="#cdaa52",
        padding=10
    )


    bottom_nav = d.bottom_nav(ft) # Create the bottom navigation bar with copyright content

    # Create a header for the dashboard
    header = ft.Text("Update Status", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    #lead_dropdown = d.user_leads(page,headers,req,ft) # Create dropdowns, Leads

    options = d.user_leads_options(page,headers,req)

    #-------------------------------
    # Create a text field for user input
    lead_field = ft.TextField(
        hint_text="Type to lead ID...",
        bgcolor="#fcfcfc", 
        on_change=lambda e: update_autocomplete(e.control.value)
    )

    suggestions_container = ft.Container(
        content=ft.ListView(
            spacing=5,
            controls=[],  # Your controls will go here
            height=200,   # Set a height for the list view
            auto_scroll=True,  # Enable auto scrolling if needed
        ),
        visible=False,
        padding=10,
        border_radius=5,
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(1, ft.colors.WHITE),
    )

    # Function to update suggestions based on input
    def update_autocomplete(value):
        # Filter items based on user input
        filtered_items = [item for item in options if item.lower().startswith(value.lower())]
        suggestions_container.content.controls.clear()
        for item in filtered_items:
            suggestions_container.content.controls.append(
                ft.ListTile(
                    title=ft.Text(item),
                    on_click=lambda e, item=item: select_item(item)
                )
            )
        
        # Show or hide the suggestions container
        suggestions_container.visible = bool(filtered_items)
        page.update()

    # Function to handle item selection
    def select_item(item):
        lead_field.value = item
        suggestions_container.visible = False  # Hide suggestions after selection
        page.update()


    # Position the suggestions container below the text field
    def update_suggestions_position():
        suggestions_container.left = lead_field.left
        suggestions_container.top = lead_field.top + lead_field.height
        suggestions_container.width = lead_field.width
        page.update()

    lead_field.on_focus_changed = update_suggestions_position


    #-----------------------------
    
    '''
    # TextField for search input
    search_input = ft.TextField(
        hint_text="Search for leads...",
        bgcolor="#fcfcfc", 
        on_change=lambda e: filter_options(e.control.value)
    )

    # Dropdown to show filtered options
    
    dropdown = ft.Dropdown(
        label="Select Lead ID",
        bgcolor="#fcfcfc", 
    )

    def filter_options(query):
        filtered = [option for option in options if query.lower() in option.lower()]
        dropdown.options = [ft.dropdown.Option(option) for option in filtered]
        dropdown.update()
    '''

    status_dropdown = d.status_list(ft) # Create dropdowns, status 
    substatus_dropdown = d.sub_status_list(ft) # Create dropdowns, sub status
    textarea = d.comment_box(ft)  # Create Text area, Multiline
    error_message = ft.Text("", color=ft.colors.RED)
    submit_button = ft.ElevatedButton(
        text="Submit",
        bgcolor="#cdaa52",
        color="#ffffff",
        on_click=lambda e: handle_form_submission(page,lead_field,status_dropdown, substatus_dropdown, textarea, error_message)
    )

    # Create dashboard content
    dashboard_content = ft.Column(
        controls=[
            top_nav,
            header,
            lead_field, suggestions_container,
            #search_input,
            #dropdown,
            #lead_dropdown,
            status_dropdown,
            substatus_dropdown,
            textarea,
            error_message,
            submit_button,
            bottom_nav  
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        expand=True,  # Allow the column to take up available space
    )

    # Add the components to the page
    page.add(
        ft.Container(
            content=dashboard_content,
            alignment=ft.alignment.center,
            padding=15,
            bgcolor=ft.colors.TRANSPARENT,
            border_radius=10,
            width=400,  # Adjusted width for better layout
            height=600,  # Make sure there's enough height
        )
    )


def handle_form_submission(page,lead_field ,status_dropdown, substatus_dropdown, textarea,error_message):
    if not lead_field.value or not status_dropdown.value or not substatus_dropdown.value or not textarea.value:
        error_message.value =  "All fields are required."    
    else:
        #lead_id = lead_dropdown.value
        status = status_dropdown.value
        sub_status = substatus_dropdown.value
        comment = textarea.value
        #lead_id = dropdown.value
        lead_field = lead_field.value
        lead_id = lead_field.upper()
        update = d.update_lead_status(page,headers,req,lead_id,status,sub_status,comment)
        update = 'success'
        if update == 'success':
            thank_you_page(page)  
        else : 
            error_message.value =  update
    
    error_message.update()
    

def logout(page: ft.Page):
    logout = d.user_logout(page,headers,req)
    if logout == 'success':
        main(page)
    else:
        pass
ft.app(target=main)



