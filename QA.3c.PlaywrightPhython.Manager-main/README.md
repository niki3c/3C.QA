# QA.3c.PlaywrightPhython.Manager
Repository for automation tests written in Python, using Playwright, for the 3c Manager/Hub

A .env file is required on the local machine.  It holds urls, login credentials, and the playwright headless mode state.

The .env file should be located in the project root and contains the following:

STAGE_MANAGER_REGISTRATION_URL=https://dev1-manager.threecolts.com/v2/register/

STAGE_MANAGER_LOGIN_URL=https://dev1-manager.threecolts.com/v2/login/

STAGE_MANAGER_TESTING_USERNAME=your_user_name_here

STAGE_MANAGER_TESTING_PW=your_pw_here

HEADLESS_MODE=False

The user/pw combination must be a valid user/pw for logging in to the 3C Manager/Hub
