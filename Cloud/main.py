import Cloud
from consts import *


my_cloud = Cloud.Cloud("0.0.0.0", CLOUD_NEVOA_PORT, CLOUD_CAR_PORT)
my_cloud.start_cloud()
