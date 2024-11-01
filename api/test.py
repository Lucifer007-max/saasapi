# test_google.py
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import PyPDF2
    print("Imports successful")
except ModuleNotFoundError as e:
    print(e)
