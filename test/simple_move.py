import bosdyn.client
from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandClient, blocking_stand
from PIL import Image
import io
from bosdyn.geometry import EulerZXY
from bosdyn.client.robot_command import RobotCommandBuilder
from utils.auth import get_spot_password, get_spot_username


sdk = bosdyn.client.create_standard_sdk('understanding-spot')
robot = sdk.create_robot('192.168.80.3')
id_client = robot.ensure_client('robot-id')
print(id_client.get_id())

robot.authenticate(get_spot_username(), get_spot_password())
state_client = robot.ensure_client('robot-state')
print(state_client.get_robot_state())


image_client = robot.ensure_client(ImageClient.default_service_name)
sources = image_client.list_image_sources()
print([source.name for source in sources])

image_response = image_client.get_image_from_sources(["left_fisheye_image"])[0]
image = Image.open(io.BytesIO(image_response.shot.image.data))
# image.show()

estop_client = robot.ensure_client('estop')
print(estop_client.get_status())

estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='my_estop', estop_timeout=9.0)
estop_endpoint.force_simple_setup()

print(estop_client.get_status())

estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(estop_endpoint)
print(estop_client.get_status())

lease_client = robot.ensure_client('lease')
print(lease_client.list_leases())

lease = lease_client.take()
lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(lease_client)
print(lease_client.list_leases())

robot.power_on(timeout_sec=20)
print(f"Power Status: {robot.is_powered_on()}")

robot.time_sync.wait_for_sync()

command_client = robot.ensure_client(RobotCommandClient.default_service_name)
blocking_stand(command_client, timeout_sec=10)



# Command Spot to rotate about the Z axis.
footprint_R_body = EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
command_client.robot_command(cmd)
cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
command_client.robot_command(cmd)

robot.power_off(cut_immediately=False)



