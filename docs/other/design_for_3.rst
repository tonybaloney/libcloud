API Design Proposal Apache Libcloud v3.0
========================================

This is a design proposal for a replacement API in the next major version of Apache Libcloud 3.0.

Principles
~~~~~~~~~~

1. Leverage vendor-backed Python packages for integration
---------------------------------------------------------

Reasoning :

* Community-driven development of a libcloud-only implementation of AWS and Azure is unsustainable. The Azure driver is buggy and only supports a fraction of services.
* Cloud vendors have moved toward auto-generated API clients, supporting
* Drivers can depend upon 3rd party libraries, where those libraries are maintained by the cloud vendor.

2. Drop the driver-service pattern in favour of a resource-operation API
------------------------------------------------------------------------

Reasoning:

* Back when Libcloud was originally designed, there were only 4 major services in public cloud, IaaS (VM), Object Storage, DNS and Load Balancing
* This is no longer the case, each cloud provider offers 10's, and in some cases, 100's of unique services
* Providing abstraction layers for each-and-every service 



3. Support asynchronous programming and Python 3.5+ idioms
----------------------------------------------------------

Reasoning:

* Python 3.5 offers asynchronous programming APIs and an asynchronous HTTP client
* Many of the operations (e.g. provisioning, paging results) would greatly benefit from task queing


Example snippets
~~~~~~~~~~~~~~~~

Get a list of resource groups in Microsoft Azure
------------------------------------------------

.. code-block:: Python

    from libcloud3.drivers.azure import AzureDriver

    driver = AzureDriver(subscription_id, client_id, secret, tenant)

    print(driver.ResourceGroup.get())
