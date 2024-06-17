
from database import conn, cursor
from models.category import Category

class Catalogue:
    TABLE_NAME = "catalogues"

    def __init__(self, name, description, image, category_id, chef):
        self.id = None
        self.name = name
        self.description = description
        self.image = image
        self.category_id = category_id
        self.chef = chef
        self.created_at = None

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, description, image, category_id, chef)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.description, self.image, self.category_id, self.chef))
        conn.commit()
        self.id = cursor.lastrowid

        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "category_id": self.category_id,
            "chef": self.chef,
            "created_at": self.created_at
        }

    @classmethod
    def find_all(cls):
        sql = """
            SELECT catalogues.*, categories.* FROM catalogues
            LEFT JOIN categories ON catalogues.category_id = categories.id
            ORDER BY catalogues.created_at ASC
        """

        rows = cursor.execute(sql).fetchall()

        return [
            cls.row_to_instance(row).to_dict() for row in rows
        ]

    @classmethod
    def row_to_instance(cls, row):
        if row is None:
            return None

        catalogue = cls(row[1], row[2], row[3], row[4], row[5])
        catalogue.id = row[0]
        catalogue.created_at = row[6]

        category = Category(row[8])
        category.id = row[7]

        catalogue.category = category.to_dict()

        return catalogue

    @classmethod
    def create_table(cls):
        # Drop table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {cls.TABLE_NAME}")
        
        # Create the table
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                chef TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """
        cursor.execute(sql)
        conn.commit()
        print(f"Catalogue table created successfully")

# Ensure the correct table creation
Catalogue.create_table()

# Verify table creation
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables in the database:", tables)
