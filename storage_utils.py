from minio import Minio
from minio.error import S3Error

from io import BytesIO
import os

# Create a client with the MinIO server playground, its access key
# and secret key.

def store_model(data):
    # the credentials are defined in the os.environment variables
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY");
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY");
    if(MINIO_ACCESS_KEY == None or MINIO_SECRET_KEY == None):
        raise ValueError("Minio credentials are not defined");
    client = Minio(
        "objectstorage:9010",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    );



    # Make 'model-bucket' bucket if not exist.
    found = client.bucket_exists("model-bucket")
    if not found:
        client.make_bucket("model-bucket")
    else:
        print("Bucket 'model-bucket' already exists")
    
    # data = BytesIO(data);

    # Upload the model
    client.put_object(
        "model-bucket", "model.keras", BytesIO(data), len(data)
    );
    print("upload successful");
    return True;


def fetch_model():
    # the credentials are defined in the os.environment variables
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY");
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY");
    if(MINIO_ACCESS_KEY == None or MINIO_SECRET_KEY == None):
        raise ValueError("Minio credentials are not defined");
    client = Minio(
        "objectstorage:9010",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    );

    # Make 'model-bucket' bucket if not exist.
    found = client.bucket_exists("model-bucket");
    data = None;
    if not found:
        raise ValueError("Bucket 'model-bucket' does not exist");
    response = None;
    try:
        response = client.get_object("model-bucket", "model.keras")
    finally:
        if(response.status == 200):
            data = response.read();
        else:
            data = False;
        response.close()
        response.release_conn()
    return data;