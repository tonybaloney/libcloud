from libcloud3.drivers.gcp import GcpDriver

driver = GcpDriver(project_id='libcloud-dev')
instances = driver.ComputeInstance.get('us-west1-b')

print(instances)

kubernetes_cluster = driver.KubernetesCluster.get('us-central1-a')

print(kubernetes_cluster)

buckets = driver.StorageBucket.get()

print(buckets)