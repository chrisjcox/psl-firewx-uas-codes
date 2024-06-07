

def access_info():
    
    # CONFIG OPTIONS
    #   Instead of using a config file, we will keep it self-contained and relay 
    #   authentication credentials to AWS/boto3 through environmental variables. 
    #   Hopefully this keeps things portable and less prone to premissions issues.
    #
    #
    # Config data provided by J. Intrieri 8 May 2024
    username        = 'WMO-UASDC-Participant'
    aws_key         = ***REMOVED***
    aws_secret_key  = ***REMOVED***
    entry_bucket    = ***REMOVED***
    product_bucket  = ***REMOVED***
    
    return username, aws_key, aws_secret_key, entry_bucket, product_bucket
    