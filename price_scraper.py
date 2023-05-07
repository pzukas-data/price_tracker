import mysql.connector
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# function to establish a connection to MySQL database
def open_connection():
    return mysql.connector.connect(
        host="host",
        user="user",
        password="password",
        port="port",
        database="database",
    )


def specdarbai():
    try:
        # scrape data from webpage
        soup = getsoup("https://www.specdarbai.lt/produktas/htw-konsolinis-split-tipo-oro"
                       "-kondicionieriussilumos"
                       "-siurblys-htw-f-035l01r32-22c/?fbclid"
                       "=IwAR2C8ryy4B_FbkW2CsWTICFa9jBr41gIL2OotiWKezLghYaBOuql5Bv_Ma8")
        # extract price from webpage using BeautifulSoup
        return (
            "specdarbai",
            "specdarbai",
            float(soup.select_one("span.price").text.replace(" €", ""))
        )
    except Exception as e:
        print(f"Error getting data from specdarbai.lt: {e}")
        return "specdarbai", None


def getsoup(url):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                      "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    })
    return BeautifulSoup(session.get(url).text, "html.parser")


def komfortocentras():
    try:
        soup = getsoup("https://komfortocentras.lt/produktas/htw-konsolinis-split-tipo-oro-kondicionierius"
                       "-silumos-siurblys-htw-f-035l01r32/")
        return (
            "komfortocentras",
            "komfortocentras",
            float(soup.select("span.woocommerce-Price-amount.amount bdi")[3].text.replace("€", ""))
        )
    except Exception as e:
        print(f"Error getting data from komfortocentras.lt: {e}")
        return "komfortocentras", None


def kondicionieriai24():
    try:
        soup = getsoup("https://kondicionieriai24.lt/produktas/htw-konsolinis-split-tipo-oro"
                       "-kondicionieriussilumos-siurblys-htw-f-035l01r32-22c/")
        return (
            "kondicionieriai24",
            "kondicionieriai24",
            float(soup.select("span.woocommerce-Price-amount.amount")[2].text.replace("€", "").replace(",", ""))
        )
    except Exception as e:
        print(f"Error getting data from kondicionieriai24.lt: {e}")
        return "kondicionieriai24", None


def derekis():
    try:
        soup = getsoup("https://www.derekis.lt/konsolinis-split-tipo-oro-kondicionieriussilumos-siurblys-htw-f"
                       "-035l01r32")
        return (
            "derekis",
            "derekis",
            float(soup.select_one("strong.price").text.replace("€", "").replace("Kaina\n", "").strip())
        )
    except Exception as e:
        print(f"Error getting data from derekis.lt: {e}")
        return "derekis", None

# function to insert data into a MySQL table
def insert_data(table_name, name, price, timestamp):
    try:
        with open_connection() as mydb:
            mycursor = mydb.cursor()
            sql = f"INSERT INTO {table_name} (name, price, timestamp) VALUES (%s, %s, %s)"
            data = (name, price, timestamp)
            # execute query and commit changes to database
            mycursor.execute(sql, data)
            mydb.commit()
    except mysql.connector.Error as error:
        print("Failed to insert data into MySQL table:", error)

# main function to scrape data from websites and insert into MySQL database
def main():
    # scrape data from websites and store in list
    data = [
        specdarbai(),
        komfortocentras(),
        kondicionieriai24(),
        derekis()
    ]

    timestamp = datetime.now()

    try:
        # loop through data and insert into database using insert_data() function
        for table_name, name, price in data:
            insert_data(table_name, name, price, timestamp)
            print(name, price, timestamp)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()