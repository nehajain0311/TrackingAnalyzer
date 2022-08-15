import sqlite3
from pathlib import Path
import pandas as pd


DATABASE_NAME='TrackData.db'
TABLE1='fleet'
TABLE2='track'
SQL_SELECT={
"List of fleets":"select * from fleet",
"Show me running fleets":'''select * from fleet where STATUS=="Running"''',
"List of planned fleets":'''select * from fleet where STATUS=="Planned"''',
"List of closed fleets":'''select * from fleet where STATUS=="Closed"''',
"What are my inactive fleets":'''select * from fleet where STATUS=="Inactive"''',
"Show me delayed tracks":'''select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where OPERATION_STATUS=="Delayed"''',
"List all tracks in transit":''' select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where OPERATION_STATUS=="Transit"''',
"Show me completed tracks":''' select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where OPERATION_STATUS=="Completed"''',
"List all the track started today":'''select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where DATE_OF_DEPARTURE==date()''',
"List all the tracks with eta today":'''select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where DATE_OF_ARRIVAL==date()''',
"List all tracks in running today":'''select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where OPERATION_STATUS!="Completed"''',
"List all tracks reached destination today":''' select t.TRACK_ID,t.FLEET_ID, f.OPERATOR_NAME,t.SOURCE,t.DESTINATION,t.DATE_OF_DEPARTURE,t.DATE_OF_ARRIVAL,t.DURATION,t.load,t.OPERATION_STATUS from track t join fleet f on t.FLEET_ID=f.FLEET_ID where OPERATION_STATUS=="Completed" and DATE_OF_ARRIVAL==date()'''
}

def addSQL_Query(NL_Query):
    SQL_SELECT[NL_Query] = "under process"

def create_database_tables():
    #creates database
    Path(DATABASE_NAME).touch()
    #creates table schema
    create_tables()
    # creates initial table_data from csv
    insert_data()

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # fleet_id	operator_name	fleet_type	capacity	status
    c.execute(f'''CREATE TABLE {TABLE1} (FLEET_ID int primary key, OPERATOR_NAME text,FLEET_TYPE text, CAPACITY text,STATUS text)''')
    # track_id	fleet_id	source	destination	date_of_departure	date_of_arrival	duration	load	operation_status
    c.execute(f'''CREATE TABLE {TABLE2} (TRACK_ID text,	FLEET_ID int REFERENCES fleet(FLEET_ID),	SOURCE text,	DESTINATION	text, DATE_OF_DEPARTURE text,DATE_OF_ARRIVAL text,	DURATION text,	LOAD text,	OPERATION_STATUS text)''')
    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    fleet_csv_path=(Path(__file__).resolve().parents[1]).joinpath('fleet.csv')
    track_csv_path=(Path(__file__).resolve().parents[1]).joinpath('track.csv')

    # load data in pandas dataframe
    fleet = pd.read_csv(fleet_csv_path)
    track=pd.read_csv(track_csv_path)
    # write the data to a sqlite table
    fleet.to_sql(f'{TABLE1}', conn, if_exists='append', index=False)
    track.to_sql(f'{TABLE2}', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

# this will be used later and updated to avoid SQL injection
def insert_update(queries):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    for query in queries:
        c.execute(query)
    conn.commit()
    conn.close()


def select_query(dropdown_select):
    # As main.py is not in util folder,database_name provided with path
    conn = sqlite3.connect(f'util/{DATABASE_NAME}')
    df=pd.read_sql(SQL_SELECT[dropdown_select], conn)
    conn.close()
    return df


#add button to download csvs for user


