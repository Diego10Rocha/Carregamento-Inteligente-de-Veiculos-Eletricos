import Cloud
from consts import *


my_cloud = Cloud.Cloud(CLOUD_ADDR, CLOUD_NEVOA_PORT, CLOUD_CAR_PORT)
my_cloud.start_cloud()
