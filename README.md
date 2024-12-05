<!-- ABOUT THE PROJECT -->
## About The Project
With the abundance of irrelevant and distant listings on classified advertising platforms such as Facebook Marketplace and Craigslist, our team decided to develop an open-source marketplace platform tailored to students.
To achieve this goal and learn as much as possible about critical tools in the software industry, we chose to develop the platform using Django Rest Framework (Python) for the backend API and React + Vite (JavaScript/JSX) for the frontend.

### Work In Progress
We are still testing, finishing up features, and optimizing our code, but we are well on the way to the completed project.

More info will be added here as we finish things up!


## Run the Code
To install the dependencies and run the project as it is now, follow these simple steps in your terminal:

1. Clone the repo (into the currect directory)
```sh
git clone https://github.com/bennettbDEV/CollegeMarketplace.git .
```
2. (Optionally) Set up a [virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
```sh
python -m venv venv
```
2a. Activate the virtual environment - for Windows:
```sh
.\venv\Scripts\activate
```
2b. Activate the virtual environment - for Linux/Mac:
```sh
source venv/bin/activate
```
3. Move to the backend directory 
```sh
cd backend
```
4. Install necessary packages
```sh
python -m pip install -r requirements.txt
```
5. Navigate back to the base directory
```sh
cd ..
```
6. Go to the frontend directory
```sh
cd frontend
```
7. Install necessary packages
```sh
npm install
```
8. Create an env file (Links our development servers together)
```sh
echo VITE_API_URL="http://localhost:8000/" > .env
```
9. Start the frontend
```sh
npm run dev
```
10. After splitting or creating a new terminal, navigate to CollegeMarketplace/backend
```sh
cd ..
cd backend
```
11. Start the backend
```sh
python manage.py runserver
```
12. Done!
    Open a browser and enter "http://localhost:5173/" into the search bar to interact with the Marketplace
