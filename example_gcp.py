from libcloud3.drivers.gcp import GcpDriver
import os

driver = GcpDriver(
    project_id='libcloud-dev',
    developer_key=os.environ['GOOGLE_API_KEY'])

instances = driver.ComputeInstance.get()

print(instances)