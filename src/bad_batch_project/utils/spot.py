import bosdyn.client
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandClient, blocking_stand
from PIL import Image
import io
from bosdyn.geometry import EulerZXY
from bosdyn.client.robot_command import RobotCommandBuilder
from utils.auth import get_spot_password, get_spot_username
import time
from termcolor import colored

initialized = False
command_client = None
robot = None
state_client = None

class PowerException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def check_init():
    global initialized
    if not initialized:
        print(colored("SPOT NOT INITIALIZD", "red"))
        exit()

    if not bosdyn.client.power.is_powered_on(state_client):
        print(colored("SPOT MOTORS NOT ON", "red"))
        raise PowerException("spot motors not on")


def init():
    global command_client
    global robot
    global initialized
    global state_client


    sdk = bosdyn.client.create_standard_sdk('understanding-spot')
    robot = sdk.create_robot('192.168.80.3')
    id_client = robot.ensure_client('robot-id')
    robot.authenticate(get_spot_username(), get_spot_password())
    state_client = robot.ensure_client('robot-state')

    estop_client = robot.ensure_client('estop')
    estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='my_estop', estop_timeout=9.0)
    estop_endpoint.force_simple_setup()
    estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(estop_endpoint)

    lease_client = robot.ensure_client('lease')
    lease = lease_client.take()
    lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(lease_client)

    robot.power_on(timeout_sec=20)
    robot.time_sync.wait_for_sync()

    command_client = robot.ensure_client(RobotCommandClient.default_service_name)
    blocking_stand(command_client, timeout_sec=10)

    # Command Spot to rotate about the Z axis.
    footprint_R_body = EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
    cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
    command_client.robot_command(cmd)
    cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
    command_client.robot_command(cmd)

    # robot.power_off(cut_immediately=False)
    initialized = True

def turnOff():
    check_init()
    robot.power_off(cut_immediately=False)

def turnOn():
    try:
        check_init()
    except PowerException as e:
        print(colored("TURNING ON MOTORS", "green"))
    finally:
        robot.power_on(timeout_sec=20)


def stand():
    check_init()
    footprint_R_body = EulerZXY(yaw=0.0, roll=0.0, pitch=0.0)
    cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
    command_client.robot_command(cmd)

def lay():
    check_init()
    cmd = RobotCommandBuilder.synchro_sit_command()
    command_client.robot_command(cmd)

def sit():
    check_init()
    footprint_R_body = EulerZXY(yaw=0.0, roll=0.0, pitch=-1)
    cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
    command_client.robot_command(cmd)

def twerk(interval=.1, duration=5):
    check_init()
    down = RobotCommandBuilder.synchro_stand_command(footprint_R_body=EulerZXY(yaw=0.0, roll=0.0, pitch=-1))
    up = RobotCommandBuilder.synchro_stand_command(footprint_R_body=EulerZXY(yaw=0.0, roll=0.0, pitch=0.0))

    start = time.time()
    while time.time() - start < duration:
        command_client.robot_command(up)
        time.sleep(interval)
        command_client.robot_command(down)
        time.sleep(interval)


