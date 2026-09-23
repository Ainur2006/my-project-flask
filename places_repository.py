import psycopg
from psycopg.rows import dict_row


class PlacesRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('SELECT * FROM places')
                return cur.fetchall()


    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('SELECT * FROM places WHERE id = %s', (id,))
                return cur.fetchone()

    def save(self, places_data):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                if 'id' not in places_data:
                    cur.execute('INSERT INTO places (name, address) VALUES (%s, %s) RETURNING id', (places_data['name'], places_data['address']))
                    places_data['id'] = cur.fetchone()[0]
                else:
                    cur.execute('UPDATE places SET name = %s, address = %s WHERE id = %s',
                                (places_data['name'], places_data['address'], places_data['id']))
            conn.commit()
        return places_data['id']

    def destroy(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM places WHERE id = %s', (id,))
            conn.commit()