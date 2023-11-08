# SBRP G8 T1
How to run the application:
1. Clone the repo (Skip to step 3 if you are using the local files)
2. Copy the .env file under the root folder from the submission's source code and place it into the repo's root folder
3. Open the gitlab folder on VSCode. type "cd backend" followed by "docker-compose up" to start endpoints.
Use "docker-compose up -d" if you want to use the terminal.
4. Open frontend/login.html and login with these emails for testing (passwords are empty):
    - boss@email.com.sg (Manager role)
    - colins_email@email.com.sg (HR role)
    - tan_ah_gao@all-in-one.com.sg (Staff role)
5. When done, go back to the terminal that you dock-composed in and type "docker-compose down"