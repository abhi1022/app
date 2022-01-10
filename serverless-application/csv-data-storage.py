import csv
from google.cloud import storage
import sqlalchemy


db_user = 'rootadmin'
db_pass = 'password@123456'
db_name = 'csv_storage'
cloud_sql_connection_name = 'csv-data-storage'


db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": "/cloudsql/development-tier:us-central1:{}".format(cloud_sql_connection_name)},
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=800,
)


def insert_into_db(value):
    sql = "insert into storage values(\'" + value[1] + "\', \'" + value[0] + "\');"
    print(sql)
    with db.connect() as conn:
        conn.execute(sql)
        print('Data is inserted!!')



def hello_gcs(event, context):

    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

    print('data: {}'.format(event))

    bucket_name = event['bucket']
    file_name = event['name']

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    model_filename = file_name
    blob = bucket.blob(model_filename)
    blob.download_to_filename('/tmp/temp.csv')

    fields = []
    rows = []

    with open('/tmp/temp.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)

        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)

    for value in rows:
        print('Name: {}'.format(value[0]))
        print('Age: {}'.format(value[1]))
        insert_into_db(value)