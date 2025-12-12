from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def ReadRifugi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT * FROM rifugio"""

        cursor.execute(query)
        for row in cursor:
            result.append(Rifugio(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(year, dict_rifugi):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
                    FROM connessione
                    WHERE anno <= %s and id_rifugio1 < id_rifugio2 """

        cursor.execute(query, (year,))
        for row in cursor:
            id_connessione = row['id']
            # prendo gli oggetti rifugio relativi a quell'id rifugio attraverso il map dei rigufi passato dal model
            rifugio1 = dict_rifugi[row['id_rifugio1']]
            rifugio2 = dict_rifugi[row['id_rifugio2']]

            #calcolo fattore difficoltà:
            fattore_difficolta = 0
            if row["difficolta"] == "facile":
                fattore_difficolta = 1.0
            elif row["difficolta"] == "media":
                fattore_difficolta = 1.5
            elif row["difficolta"] == "difficile":
                fattore_difficolta = 2.0

            result.append(Connessione(id_connessione, rifugio1, rifugio2, row["distanza"], fattore_difficolta, row["durata"], row["anno"] ))
        cursor.close()
        conn.close()
        return result






