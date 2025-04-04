import asyncpg


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def connect(self):
        """
        Connect to the database and create a connection pool.
        """
        self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=5)
        print("Database connection pool created")

    async def create_user(self, fullname: str, username: str, email: str, password: str):
        """
        Create a new user in the database.
        """
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    fullname TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT,
                    password TEXT NOT NULL
                );
                """
            )
            await connection.execute(
                """
                INSERT INTO users (fullname, username, email, password)
                VALUES ($1, $2, $3, $4);
                """, fullname, username, email, password
            )
            print(f"User {username} created successfully")

    async def update_user(self, user_id: int, fullname: str = None, username: str = None, email: str = None,
                          password: str = None):
        """
        Update user details in the database by user_id.
        """
        fields = []
        values = []

        if fullname:
            fields.append("fullname = $1")
            values.append(fullname)
        if username:
            fields.append("username = $2")
            values.append(username)
        if email:
            fields.append("email = $3")
            values.append(email)
        if password:
            fields.append("password = $4")
            values.append(password)

        if fields:
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ${len(values) + 1};"
            values.append(user_id)
            async with self.pool.acquire() as connection:
                await connection.execute(query, *values)
            print(f"User {user_id} updated successfully")
        else:
            print("No fields to update")

    async def read_users(self):
        """
        Retrieve all users from the database.
        """
        async with self.pool.acquire() as connection:
            users = await connection.fetch("SELECT * FROM users;")
            if users:
                users_dict = [dict(user) for user in users]
                return users_dict
            else:
                return []

    async def read_user_detail(self, user_id):
        async with self.pool.acquire() as connection:
            try:
                user = await connection.fetch("SELECT * FROM users WHERE id=$1", user_id)
                if not user:
                    return "Does not exists"
                return user[0]
            except Exception as e:
                print(f"Error retrieving user details: {e}")
                return None

    async def delete_user(self, user_id: int):
        """
        Delete a user from the database by user_id.
        """
        async with self.pool.acquire() as connection:
            await connection.execute("DELETE FROM users WHERE id = $1;", user_id)
            print(f"User with id {user_id} deleted successfully")

    async def close(self):
        """
        Close the database connection pool.
        """
        if self.pool:
            await self.pool.close()
            print("Database connection pool closed")