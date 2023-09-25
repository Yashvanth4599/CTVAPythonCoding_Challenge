# Weather Statistics Application

This project is a weather statistics application that enables users to view and interact with weather data. It consists of a backend server developed using Flask and a frontend UI designed using HTML, CSS, and JavaScript. This document details the project structure, setup instructions, usage, and other relevant information.

## Features
- Seamless user experience with pagination.
- Detailed weather data viewing with further filtering options.
- Average weather statistics computation based on station ID.
- Elegant UI design for easy navigation and data retrieval.

## Table of Contents

- [Project Structure](#project-structure)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Installation](#installation)
- [Starting the Backend Server](#starting-the-backend-server)
- [Usage](#usage)
- [Logging](#logging)
- [Development Tools](#development-tools)
- [Viewing README in VS Code](#viewing-readme-in-vs-code)
- [Future Improvements](#future-improvements)
- [Deployment](#deployment)
- [Conclusion](#conclusion)

## Project Structure

### Backend

- File: `app.py`
- Technology: Flask
- Description: Contains the backend logic for fetching and processing weather data.
- Endpoints:
  - `/`: Retrieves data from the txt files and loads them into the models.
  - `/api/weather`: Retrieves weather data based on the given parameters.
  - `/api/weather/stats`: Retrieves aggregated weather data based on the given parameters.

### Frontend

- Files:
  - `home.html`: Home page of the application.
  - `stats.html`: Provides statistics based on a given station ID.
  - `weather.html`: Users can input a weather station and date to retrieve and display weather data with further filtering options.

## Installation

1. Ensure you have [Python](https://www.python.org/) installed on your machine.
2. Clone the repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Activate the virtual environmant :
```bash
python -m venv env

.\env\Scripts\activate  # On Windows

source env/bin/activate  # On macOS and Linux
```

5. Install the required packages using the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Starting the Backend Server
1. Navigate to the backend directory.
```

Run the following command to start the backend server:


export Flask_APP=app.py
flask run
```

## Starting the Frontend Server
1. Open a new terminal.
2. Navigate to the Frontend directory.
```

Run the following command to start the backend server:

flask run -p 5001
```

## Usage

1. Open a web browser and navigate to [http://localhost:5001](http://localhost:5001).
2. Upon the first visit, the data will load into the database which might take around 6 minutes. Subsequent visits will be seamless with the pagination feature provided.
3. Use the navigation bar to switch between the different pages of the UI.
4. On the "Weather" page, enter a weather station and date, then click "Search" to retrieve and display weather data with options for further filtering on dates, years, etc.
5. On the "Statistics" page, enter a Station ID/Year and click "Search" to view the average weather statistics for that station.
6. To open the swagger url run the backend and navigate to [http://localhost:5000](http://localhost:5000).
7. Then naviagte to [http://localhost:5000/swagger/](http://localhost:5000/swagger/).
8. When querying for the data in swagger make sure you give in the page number.
9. If the response returns an empty response try querying a smaller page number. 

## Logging

- All server logs are stored in a file named `app.log` in the project root directory.

## Development Tools

- Text Editor: Visual Studio Code (VS Code)
- Version Control: Git and GitHub

## Viewing README in VS Code

1. Open the project directory in VS Code.
2. Navigate to the README file.
3. To view the Markdown preview, press `Ctrl+Shift+V` (Windows) or `Cmd+Shift+V` (Mac).

## Future Improvements
- Enhancing the UI/UX design to provide a more engaging user experience.
- Adding more complex filtering and sorting options to handle large datasets efficiently.
- Integrating additional data sources to provide a more comprehensive analysis of weather patterns.
- Implementing a caching mechanism to further reduce data loading times and improve the application's responsiveness.

## Deployment

- The application can be deployed on cloud platforms like AWS, Azure, or Google Cloud Platform.
- Utilizing cloud platforms for deployment would allow for better scalability to handle increased traffic and data load.
- Cloud deployment would also ensure higher availability and reliability compared to traditional hosting solutions.
- Moreover, cloud platforms provide various managed services and monitoring tools which can be used to maintain and optimize the application performance.
- Deploying the application on a cloud platform would also provide automatic backups, security monitoring, and other essential management features which are crucial for maintaining a robust and reliable web application.

## Conclusion
- All the specified tasks have been successfully completed with an intuitive and easy-to-use interface.
- The database initialization has been optimized to ensure that the data loading time is minimized during the first visit.
- The application provides a seamless user experience with the implementation of pagination, filtering, and sorting functionalities.
- Extensive logging has been integrated to monitor the application's performance and troubleshoot issues swiftly.
