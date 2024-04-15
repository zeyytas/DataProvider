#Introduction

The Data Provider helps hotels manage booking and cancellation events easily. It stores all event information and provides simple ways for hotels to access and add new events. 

#Installation Guide

This guide will help you set up and run the application locally using Docker, and it will also cover endpoints and running tests.

##Prerequisites
Docker installed on your machine.
 
##Installation Steps
1. Clone the Repository: Clone the repository to your local machine.

    ```shell
    git clone <repository_url>
    ```

2. Navigate to the Project Directory: Go to the root directory of the project.
   
   ```shell
   cd DataProvider
   ```

3. Build Docker Images: Build the Docker images using Docker Compose.
    
   ```shell
   docker-compose build
   ```
PS: HERE PLEASE FOLLOW POSTGRESQL SETUP STEPS BEFORE CONTINUE WITH 5.  

4. Create external network:
   
   ```shell
   docker network create dataprovider_default
   ```

5. Run Docker Containers: Start the Docker containers

   ```shell
   docker-compose up
   ```
   
6. Create database: Once the service is running, you need to create the database dashboarddb.:

   ```shell
   docker-compose exec db createdb -U postgres dataproviderdb
   ```

7. Access the Application: The application should now be accessible at _http://localhost:8000_.

## PostgreSQL Setup

### Creating a PostgreSQL User

If you're working with PostgreSQL for the first time, you may need to create a PostgreSQL user with appropriate permissions.   
Follow these steps to create a new user:

1. Open a terminal or command prompt.
2. Connect to the PostgreSQL server using the `psql` command-line utility. You may need to provide the PostgreSQL administrator password.

   ```bash
   psql -U postgres
   ```
3. Once connected, you can create a new user with the following SQL command

   ```bash
   CREATE USER admin WITH PASSWORD admin;
   ```

4. Grant necessary permissions to the user.

   ```bash
   ALTER USER admin CREATEDB;
   ```

##Endpoints

###1. GET /api/v1/events/  
Retrieve a list of events happened within a particular hotel.  
  
**Example Request:**  
GET /api/v1/events?hotel_id=1&rpg_status=1&night_of_stay__gte=2022-01-01

**Query Parameters**

1. **hotel_id**: _string_  
   Specifies the ID of the hotel for which events should be retrieved.

2. **updated__gte**: _string<date-time>_  
   Filters events to include only those that occurred on or after the specified date and time.

3. **updated__lte**: _string<date-time>_  
   Filters events to include only those that occurred on or before the specified date and time.

4. **rpg_status**: _integer_  
   Specifies the status of the event to filter by. The value 1 indicates a booking event, and 2 indicates a cancellation event.

5. **room_id**: _uuid_  
   Specifies the ID of the room associated with the event to filter by.

6. **night_of_stay__gte**: _string<date->_  
   Filters events to include only those with a night of stay on or after the specified date.

7. **night_of_stay__lte**: _string<date->_  
   Filters events to include only those with a night of stay on or before th


**Example Response:**
```json
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/v1/events/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "hotel_id": 753,
            "timestamp": "2024-04-13T06:33:22.967611Z",
            "rpg_status": 2,
            "room_id": "ebc4b19c-10bf-4a76-a13b-acdcb8c8857e",
            "night_of_stay": "2025-01-16"
        },
        {
            "id": 2,
            "hotel_id": 1731,
            "timestamp": "2024-04-13T06:34:14.135059Z",
            "rpg_status": 1,
            "room_id": "0bbff6de-d695-48c5-8a1b-921919887cbf",
            "night_of_stay": "2025-10-15"
        }
    ]
}
```

###2. POST /api/v1/events/  
Creates a new event.  
**Example Body:**    
```json
{
  "hotel_id": 1,
  "rpg_status": 1,
  "room_id": "0013e338-0158-4d5c-8698-aebe00cba360",
  "night_of_stay": "2022-04-15"
}
```
**Example Response:**    
```json
{
  "id": 3,
  "hotel_id": 1,
  "timestamp": "2022-04-15T10:00:00Z",
  "rpg_status": 1,
  "room_id": "0013e338-0158-4d5c-8698-aebe00cba360",
  "night_of_stay": "2022-04-15"
}
```

###3. POST /api/token/  
Handles the generation and refreshing of access tokens.

**Body must be:**
```json
{
  "username": "admin",
  "password": "admin"
}
```

**Example Response:**    
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMzE4Njg2MSwiaWF0IjoxNzEzMTAwNDYxLCJqdGkiOiJjODI3NzYyMDBkMzA0Njg0YWQ2NzZmNjY0MzQ1ZWQwMyIsInVzZXJfaWQiOjF9.gnFGZyHILf9lTjtljThKn3XujsbS_RfthRL-t2TeTiQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzMTAwNzYxLCJpYXQiOjE3MTMxMDA0NjEsImp0aSI6ImUwNzg3NDc4ODdlZTRlMGI4OTAwOTZmYjhmNWNmZmE1IiwidXNlcl9pZCI6MX0.KCukTQwz47jtu61YaWLZQ-N-czG-BvKFX_16KsONgNI"
}
```

##Running Tests  

To ensure the correctness and stability of the application, automated tests are provided. These tests cover various aspects of the application, including API endpoints, models, and integration between different components.  

To run tests, follow these steps:
1. Ensure that the Docker containers are running.
2. Open a new terminal window.
3. Navigate to the project directory.
4. Run pytest.

   ```shell
   docker-compose exec web pytest event/tests/tests.py
   ```

##Additional Information
- The application uses Django Rest Framework for API development.
- PostgreSQL is used as the database, RabbitMQ for message queuing, and Celery for asynchronous task processing.
- The Docker Compose configuration ensures that all services required by the application are running together seamlessly.
