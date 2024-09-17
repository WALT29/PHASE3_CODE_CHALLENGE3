# Concert Management System

This project is a simple Concert Management System implemented in Python using SQLite for database management. It allows users to manage `Bands`, `Venues`, and `Concerts`, offering functionalities such as creating, updating, deleting records, and retrieving information about concerts and their participants.

## Features

- **Bands**: Create, update, delete, and query band information.
- **Venues**: Manage concert venues with the ability to list concerts and bands performing at a particular venue.
- **Concerts**: Organize concerts, allowing bands to perform at venues on specific dates.
- Query information such as:
  - All concerts for a band
  - The venues where a band has performed
  - Band with the most performances
  - Most frequent band at a venue
  - Concert introductions and hometown shows

## Database Schema

The project contains three primary tables:
1. **Bands** - Manages band information, such as name and hometown.
2. **Venues** - Manages venue information, including title and city.
3. **Concerts** - Records concert events, associating a band with a venue and date.

