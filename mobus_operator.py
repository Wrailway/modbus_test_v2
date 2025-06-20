import time
import can
import logging

from pymodbus import FramerType
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException

# 设置日志级别为INFO，获取日志记录器实例
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# # 创建一个文件处理器，用于将日志写入文件
# file_handler = logging.FileHandler('can_bus_operator_log.txt')
# file_handler.setLevel(logging.DEBUG)

# # 创建一个日志格式
# log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(log_format)

# # 将文件处理器添加到日志记录器
# logger.addHandler(file_handler)

console_handler = logging.StreamHandler()

# 设置处理程序的日志级别为 INFO
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

PORT = 'COM3'
NODE_ID = 2
BAUDRATE =115200
FRAMER =FramerType.RTU
# 定义指令类型常量
READ_REGISTER = 0b00
WRITE_REGISTER = 0b01

WAIT_TIME = 0.1 # 延迟打印，方便查看
ROH_SUB_EXCEPTION         = (1006) # R
# ROH 灵巧手错误代码
EC01_ILLEGAL_FUNCTION = 0X1  # 无效的功能码
EC02_ILLEGAL_DATA_ADDRESS = 0X2  # 无效的数据地址
EC03_ILLEGAL_DATA_VALUE = 0X3  # 无效的数据（协议层，非应用层）
EC04_SERVER_DEVICE_FAILURE = 0X4  # 设备故障
UNKNOWN_FAILURE = 0X5  # 未知错误

roh_exception_list = {
        EC01_ILLEGAL_FUNCTION: '无效的功能码',
        EC02_ILLEGAL_DATA_ADDRESS: '无效的数据地址',
        EC03_ILLEGAL_DATA_VALUE: '无效的数据（协议层，非应用层）',
        EC04_SERVER_DEVICE_FAILURE: '设备故障',
        UNKNOWN_FAILURE: '未知错误'
    }

# 寄存器 ROH_SUB_EXCEPTION 保存了具体的错误代码
ERR_STATUS_INIT = 0X1  # 等待初始化或者正在初始化，不接受此读写操作
ERR_STATUS_CALI = 0X2  # 等待校正，不接受此读写操作
ERR_INVALID_DATA = 0X3  # 无效的寄存器值
ERR_STATUS_STUCK = 0X4  # 电机堵转
ERR_OP_FAILED = 0X5  # 操作失败
ERR_SAVE_FAILED = 0X6  # 保存失败

roh_sub_exception_list = {
        ERR_STATUS_INIT: '等待初始化或者正在初始化，不接受此读写操作',
        ERR_STATUS_CALI: '等待校正，不接受此读写操作',
        ERR_INVALID_DATA: '无效的寄存器值',
        ERR_STATUS_STUCK: '电机堵转',
        ERR_OP_FAILED: '操作失败',
        ERR_SAVE_FAILED: '保存失败'
    }
    

def get_exception(bus,response):
    """
    根据传入的响应确定错误类型。

    参数：
    response：包含错误信息的响应对象。

    返回：
    错误类型的描述字符串。
    """
    strException = ''
    if response.exception_code > EC04_SERVER_DEVICE_FAILURE:
        strException = roh_exception_list.get(UNKNOWN_FAILURE)
    elif response.exception_code == EC04_SERVER_DEVICE_FAILURE:
        response2 = read_registers(bus=bus, start_address=ROH_SUB_EXCEPTION, register_count=1)
        strException = '设备故障，具体原因为'+roh_sub_exception_list.get(response2.registers[0])
    else:
        strException = roh_exception_list.get(response.exception_code)
        
    return strException

def setup_modbus():
    try:
        bus = ModbusSerialClient(port=PORT, framer=FRAMER, baudrate=BAUDRATE)
        # logger.info(f'setup_modbus = {bus},bus.connect()={bus.connect()}')
        if not bus.connect():
            logger.error(f"[port = {PORT}]Could not connect to Modbus device.")
            return None
        logger.info(f"[port = {PORT}]Successfully connected to Modbus device.")
        return bus
    except ConnectionException as e:
        logger.error(f"[port = {PORT}]Error during connection: {e}")
        return None

def close_modbus(bus):
    """
    关闭 CAN 总线连接
    :param bus: CAN 总线对象
    """
    if bus is not None:
        try:
            bus.close()
            logger.info(f"\n modbus connection closed.\n")
        except can.CanError as e:
            logger.error(f"\nError closing modbus connection: {e}\n")


def read_registers(bus, start_address, register_count=1,node_id =NODE_ID):
    response = None
    try:
        response = bus.read_holding_registers(address=start_address, count=register_count, slave=node_id)
        if response.isError():
            error_type = get_exception(bus=bus,response=response)
            logger.error(f'[读寄存器失败: {error_type}\n')
        time.sleep(WAIT_TIME)
    except Exception as e:
        logger.error(f'异常: {e}')
    return response


def write_registers(bus, start_address, data,node_id =NODE_ID):
    """
    向指定的寄存器地址写入数据。
    :param address: 要写入的寄存器地址。
    :param value: 要写入的值。
    :return: 如果写入成功则返回True，否则返回False。
    """
    try:
        response = bus.write_registers(address=start_address, values=data, slave=node_id)
        if not response.isError():
            time.sleep(WAIT_TIME)
            return True
        else:
            error_type = get_exception(bus=bus,response=response)
            logger.error(f'写寄存器失败: {error_type}\n')
            return False
    except Exception as e:
            logger.error(f'异常: {e}')
            return False
    
def get_version(response):
    try:
        if isinstance(response, int):
            major_version = (response >> 8) & 0xFF
            minor_version = response & 0xFF
            return f"V{major_version}.{minor_version}"
        elif hasattr(response, 'registers'):
            if len(response.registers) > 0:
                value = response.registers[0]
                major_version = (value >> 8) & 0xFF
                minor_version = value & 0xFF
                patch_version = None
                if isinstance(value, list) or isinstance(value, tuple) and len(value) >= 3:
                    patch_version = value[1]
                if patch_version is not None:
                    return f"V{major_version}.{minor_version}.{patch_version}"
                else:
                    # 如果没有补丁版本号，但存在格式为 V1.0 的情况，添加一个占位的 0 作为补丁版本号
                    return f"V{major_version}.{minor_version}.0"
            else:
                return "无法获取版本号"
        else:
            return "无法识别的响应类型"
    except Exception as e:
        return f"获取版本号时出现错误：{e}"
            
if __name__ == "__main__":
    # 初始化 modbus 总线
    bus = setup_modbus()

    if bus:
       response = read_registers(bus=bus,start_address=1140,register_count=1,node_id=2)
       if not response.isError():
          logger.info(f'f={response.registers[0]}')
          write_registers(bus=bus, start_address=1140, data=0,node_id =2)