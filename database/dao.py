from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artists_with_min_albums(n_alb):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT a.id,a.name 
                    FROM artist a, album a1
                    WHERE a.id = a1.artist_id
                    GROUP BY a.id,a.nome
                     HAVING COUNT(DISTINCT a1.id) >= %s)
                    ORDER BY a.name
                """

        cursor.execute(query, (n_alb,))
        for row in cursor:
            result.append(Artist(id=row['id'], name=row['name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges_common_genres(n_alb):
        #prendo una lista di triple (id1,id2,peso) dove il peso sono i generi in comune
        #si considerano solo gli artsti con numero di album maggiore di n_album


        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT a1.id as id1, a2.id as id2, COUNT(DISTINCT t1.genre_id) AS peso
                   FROM artist a1, ,artist a2, album al1,album al2, track t1, track t2
                WHERE al1.artist_id = a1.id AND t1.album_id = al1.id AND al2.artist_id = a2.id 
                  AND t2.album_id = al2.id AND 
                    AND a1.id < a2.id AND t1.genre_ is NOT NULL AND t2.genre_ is NOT NULL
            AND t1.genre_id = t2.genre_id
            AND a1.id IN (SELECT a.id 
                          FROM artist a,album al 
                WHERE al.artist_id = a1.id 
                GROUP BY a.id
                HAVING COUNT (DISTINCT al.id) >= %s)
            
            AND a2.id IN (SELECT a.id 
                          FROM artist a,album al 
                WHERE al.artist_id = a1.id 
                GROUP BY a.id
                HAVING COUNT (DISTINCT al.id) >= %s)
            
            GROUP BY a1.id, a2.id
                """

        cursor.execute(query, (n_alb,n_alb))
        for row in cursor:
            result.append((row['id1'], row['id2'], row['peso']))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artists_with_track_min_duration(dmin):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT a.id
        FROM artist a, album al, track t
                WHERE al.artist_id = a.id 
            AND t.album_id = al.id 
            WHERE t.milliseconds >= %s
                """


        cursor.execute(query, (dmin,))
        result = {row['id'] for row in cursor}

        cursor.close()
        conn.close()
        return result