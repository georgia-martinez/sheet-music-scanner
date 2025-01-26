# Database Setup
================

To set up the database for the Sheet Music Scanner project, follow these steps:
1. **Install PostgreSQL**: Ensure that you have PostgreSQL installed on your machine. 
        You can download it from the (https://www.postgresql.org/download/).
2. **Create a Database**: Open your terminal and run the following command to create a new database named `music_processor`:
   ```bash
   createdb music_processor
   ```
3. **Access the Database**: Connect to the database using the `psql` command:
   ```bash
    psql -U postgres -d music_processor
    ```
4. **Create Tables**: Execute the SQL commands to create the necessary tables in the database. You can copy and paste the following SQL commands into the `psql` terminal:
5. **Create the `music` table**:
   ```sql
   CREATE TABLE music (
       id SERIAL PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       composer VARCHAR(255) NOT NULL,
       file_path VARCHAR(255) NOT NULL
   );
   ```
6. **Create the `notes` table**:
   ```sql
    CREATE TABLE notes (
         id SERIAL PRIMARY KEY,
         music_id INTEGER REFERENCES music(id),
         note_name VARCHAR(10) NOT NULL,
         note_duration VARCHAR(10) NOT NULL
    );
    ```
7. **Create the `users` table**:
8. ```sql
    CREATE TABLE users (
         id SERIAL PRIMARY KEY,
         username VARCHAR(50) NOT NULL,
         password_hash VARCHAR(255) NOT NULL
    );
    ```
9. **Create the `annotations` table**:
10. ```sql
    CREATE TABLE annotations (
         id SERIAL PRIMARY KEY,
         music_id INTEGER REFERENCES music(id),
         user_id INTEGER REFERENCES users(id),
         annotation_text TEXT NOT NULL
    );
    ```
11. **Exit the Database**: Type `\q` to exit the `psql` terminal.
12. **Database Setup Complete**: Your database is now set up and ready to be used with the Sheet Music Scanner application.
13. **Note**: Make sure to adjust the database connection settings in your application code if necessary.
14. 