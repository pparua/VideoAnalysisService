import ibm_boto3
from ibm_botocore.client import Config, ClientError
from const import constants as consts

# Upload File to IBM Cloud Object Storage 
def upload_file_cos(filePath, keyName):

    # Create client
    cos = ibm_boto3.client("s3",
        ibm_api_key_id=consts.IBM_COS_API_KEY,
        ibm_service_instance_id=consts.IBM_COS_SVC_INSTANCE,
        ibm_auth_endpoint=consts.IBM_COS_AUTH,
        config=Config(signature_version="oauth"),
        endpoint_url= consts.IBM_COS_ENDPOINT
    )

    try:
        cos.upload_file(Filename=filePath,Bucket=consts.IBM_COS_BUCKET,Key=keyName)
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create file: {0}".format(e))
