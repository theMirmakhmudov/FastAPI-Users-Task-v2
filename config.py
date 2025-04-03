import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = 'postgresql://neondb_owner:npg_cg7aQHGX1RxE@ep-broad-voice-a1pj6w14-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'