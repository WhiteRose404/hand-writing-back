from minio import Minio
from minio.error import S3Error

from io import BytesIO

# Create a client with the MinIO server playground, its access key
# and secret key.

def store_model(data):
    client = Minio(
        "localhost:9010",
        access_key="<>",                         # to be stored in a .env file
        secret_key="<>",                         # to be stored in a .env file
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
    client = Minio(
        "localhost:9010",
        access_key="",
        secret_key="",
        secure=False
    );

    # Make 'model-bucket' bucket if not exist.
    found = client.bucket_exists("model-bucket");
    data = None;
    if not found:
        print("Bucket 'model-bucket' does not exist")
        return False;
    
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