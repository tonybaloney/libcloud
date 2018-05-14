from libcloud3.drivers.demo import DemoDriver

driver = DemoDriver(1234)

print(driver.ComputeInstance.get())