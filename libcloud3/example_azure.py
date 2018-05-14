from libcloud3.drivers.azure import AzureDriver
import os

subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
client_id = os.environ['AZURE_CLIENT_ID']
secret = os.environ['AZURE_SECRET']
tenant = os.environ['AZURE_TENANT']

driver = AzureDriver(subscription_id, client_id, secret, tenant)

print(driver.ResourceGroup.get())