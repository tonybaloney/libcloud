from libcloud3.drivers.demo import DemoDriver

driver = DemoDriver(1234)

instances = driver.ComputeInstance.get()

print(instances)

print(instances[0].stop())

