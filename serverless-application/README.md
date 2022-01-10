Application Description.

The entire deployment topology is based on Google CLoud Platform. 

Buckets in Google Cloud Platform are referred to as Storage Buckets. 
S3 buckets (AWS) => Google Storage Buckets
Lambda Functions (AWS) => Google Cloud Functions

Architecture. 

I created a Cloud Function which monitors a storage bucket "test-upload-01" for any file upload.
When there is a file upload (In our case "Test.csv"), the function which is python script "csv-data-storage.py" gets triggered , reads the 
contents of the file, and push the data into the MySQL DB "csv-data-storage".

Images for complete end to end run. 

1. Storage Bucket -> Bucket details.png
2. CSV File -> Test.csv
3. Cloud Function ("storage-bucket-object-creation") -> Cloud Function Deployment.png
4. Cloud Function details -> Cloud Function details.png
5. Database data -> Database.png
6. Table data after inserting the contents -> Tables data details.png
