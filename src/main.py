from database import *

def main():
    connection = connect_db()

    #create_tables(connection)
    #print('done')
    populate_database(connection)
    print('done')
    return None

if __name__ == "__main__":
    main()