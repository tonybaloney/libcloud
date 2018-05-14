from libcloud3.drivers.gcp import GcpDriver

driver = GcpDriver(project_id='libcloud-dev')
instances = driver.ComputeInstance.get('us-west1-b')

print(instances)
