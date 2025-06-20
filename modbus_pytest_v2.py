import logging
import time
import pytest
from mobus_operator import setup_modbus,close_modbus,read_registers,write_registers

# 设置日志级别为INFO，获取日志记录器实例
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# # 创建一个文件处理器，用于将日志写入文件
# file_handler = logging.FileHandler('test_can_bus_protocol_log.txt')
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

# ModBus-RTU registers for ROH
MODBUS_PROTOCOL_VERSION_MAJOR = 1

ROH_PROTOCOL_VERSION      = (1000) # R
ROH_FW_VERSION            = (1001) # R
ROH_FW_REVISION           = (1002) # R
ROH_HW_VERSION            = (1003) # R
ROH_BOOT_VERSION          = (1004) # R
ROH_NODE_ID               = (1005) # R/W
ROH_SUB_EXCEPTION         = (1006) # R
ROH_BATTERY_VOLTAGE       = (1007) # R
ROH_SELF_TEST_LEVEL       = (1008) # R/W
ROH_BEEP_SWITCH           = (1009) # R/W
ROH_BEEP_PERIOD           = (1010) # W
ROH_BUTTON_PRESS_CNT      = (1011) # R/W
ROH_RECALIBRATE           = (1012) # W
ROH_START_INIT            = (1013) # W
ROH_RESET                 = (1014) # W
ROH_POWER_OFF             = (1015) # W
ROH_RESERVED0             = (1016) # R/W
ROH_RESERVED1             = (1017) # R/W
ROH_RESERVED2             = (1018) # R/W
ROH_RESERVED3             = (1019) # R/W
ROH_CALI_END0             = (1020) # R/W
ROH_CALI_END1             = (1021) # R/W
ROH_CALI_END2             = (1022) # R/W
ROH_CALI_END3             = (1023) # R/W
ROH_CALI_END4             = (1024) # R/W
ROH_CALI_END5             = (1025) # R/W
ROH_CALI_END6             = (1026) # R/W
ROH_CALI_END7             = (1027) # R/W
ROH_CALI_END8             = (1028) # R/W
ROH_CALI_END9             = (1029) # R/W
ROH_CALI_START0           = (1030) # R/W
ROH_CALI_START1           = (1031) # R/W
ROH_CALI_START2           = (1032) # R/W
ROH_CALI_START3           = (1033) # R/W
ROH_CALI_START4           = (1034) # R/W
ROH_CALI_START5           = (1035) # R/W
ROH_CALI_START6           = (1036) # R/W
ROH_CALI_START7           = (1037) # R/W
ROH_CALI_START8           = (1038) # R/W
ROH_CALI_START9           = (1039) # R/W
ROH_CALI_THUMB_POS0       = (1040) # R/W
ROH_CALI_THUMB_POS1       = (1041) # R/W
ROH_CALI_THUMB_POS2       = (1042) # R/W
ROH_CALI_THUMB_POS3       = (1043) # R/W
ROH_CALI_THUMB_POS4       = (1044) # R/W
ROH_FINGER_P0             = (1045) # R/W
ROH_FINGER_P1             = (1046) # R/W
ROH_FINGER_P2             = (1047) # R/W
ROH_FINGER_P3             = (1048) # R/W
ROH_FINGER_P4             = (1049) # R/W
ROH_FINGER_P5             = (1050) # R/W
ROH_FINGER_P6             = (1051) # R/W
ROH_FINGER_P7             = (1052) # R/W
ROH_FINGER_P8             = (1053) # R/W
ROH_FINGER_P9             = (1054) # R/W
ROH_FINGER_I0             = (1055) # R/W
ROH_FINGER_I1             = (1056) # R/W
ROH_FINGER_I2             = (1057) # R/W
ROH_FINGER_I3             = (1058) # R/W
ROH_FINGER_I4             = (1059) # R/W
ROH_FINGER_I5             = (1060) # R/W
ROH_FINGER_I6             = (1061) # R/W
ROH_FINGER_I7             = (1062) # R/W
ROH_FINGER_I8             = (1063) # R/W
ROH_FINGER_I9             = (1064) # R/W
ROH_FINGER_D0             = (1065) # R/W
ROH_FINGER_D1             = (1066) # R/W
ROH_FINGER_D2             = (1067) # R/W
ROH_FINGER_D3             = (1068) # R/W
ROH_FINGER_D4             = (1069) # R/W
ROH_FINGER_D5             = (1070) # R/W
ROH_FINGER_D6             = (1071) # R/W
ROH_FINGER_D7             = (1072) # R/W
ROH_FINGER_D8             = (1073) # R/W
ROH_FINGER_D9             = (1074) # R/W
ROH_FINGER_G0             = (1075) # R/W
ROH_FINGER_G1             = (1076) # R/W
ROH_FINGER_G2             = (1077) # R/W
ROH_FINGER_G3             = (1078) # R/W
ROH_FINGER_G4             = (1079) # R/W
ROH_FINGER_G5             = (1080) # R/W
ROH_FINGER_G6             = (1081) # R/W
ROH_FINGER_G7             = (1082) # R/W
ROH_FINGER_G8             = (1083) # R/W
ROH_FINGER_G9             = (1084) # R/W
ROH_FINGER_STATUS0        = (1085) # R
ROH_FINGER_STATUS1        = (1086) # R
ROH_FINGER_STATUS2        = (1087) # R
ROH_FINGER_STATUS3        = (1088) # R
ROH_FINGER_STATUS4        = (1089) # R
ROH_FINGER_STATUS5        = (1090) # R
ROH_FINGER_STATUS6        = (1091) # R
ROH_FINGER_STATUS7        = (1092) # R
ROH_FINGER_STATUS8        = (1093) # R
ROH_FINGER_STATUS9        = (1094) # R
ROH_FINGER_CURRENT_LIMIT0 = (1095) # R/W
ROH_FINGER_CURRENT_LIMIT1 = (1096) # R/W
ROH_FINGER_CURRENT_LIMIT2 = (1097) # R/W
ROH_FINGER_CURRENT_LIMIT3 = (1098) # R/W
ROH_FINGER_CURRENT_LIMIT4 = (1099) # R/W
ROH_FINGER_CURRENT_LIMIT5 = (1100) # R/W
ROH_FINGER_CURRENT_LIMIT6 = (1101) # R/W
ROH_FINGER_CURRENT_LIMIT7 = (1102) # R/W
ROH_FINGER_CURRENT_LIMIT8 = (1103) # R/W
ROH_FINGER_CURRENT_LIMIT9 = (1104) # R/W
ROH_FINGER_CURRENT0       = (1105) # R
ROH_FINGER_CURRENT1       = (1106) # R
ROH_FINGER_CURRENT2       = (1107) # R
ROH_FINGER_CURRENT3       = (1108) # R
ROH_FINGER_CURRENT4       = (1109) # R
ROH_FINGER_CURRENT5       = (1110) # R
ROH_FINGER_CURRENT6       = (1111) # R
ROH_FINGER_CURRENT7       = (1112) # R
ROH_FINGER_CURRENT8       = (1113) # R
ROH_FINGER_CURRENT9       = (1114) # R
ROH_FINGER_FORCE_TARGET0   = (1115) # R/W
ROH_FINGER_FORCE_TARGET1   = (1116) # R/W
ROH_FINGER_FORCE_TARGET2   = (1117) # R/W
ROH_FINGER_FORCE_TARGET3   = (1118) # R/W
ROH_FINGER_FORCE_TARGET4   = (1119) # R/W
ROH_FINGER_FORCE_TARGET5   = (1120) # R
ROH_FINGER_FORCE_TARGET6   = (1121) # R
ROH_FINGER_FORCE_TARGET7   = (1122) # R
ROH_FINGER_FORCE_TARGET8   = (1123) # R
ROH_FINGER_FORCE_TARGET9   = (1124) # R
ROH_FINGER_SPEED0         = (1125) # R/W
ROH_FINGER_SPEED1         = (1126) # R/W
ROH_FINGER_SPEED2         = (1127) # R/W
ROH_FINGER_SPEED3         = (1128) # R/W
ROH_FINGER_SPEED4         = (1129) # R/W
ROH_FINGER_SPEED5         = (1130) # R/W
ROH_FINGER_SPEED6         = (1131) # R/W
ROH_FINGER_SPEED7         = (1132) # R/W
ROH_FINGER_SPEED8         = (1133) # R/W
ROH_FINGER_SPEED9         = (1134) # R/W
ROH_FINGER_POS_TARGET0    = (1135) # R/W
ROH_FINGER_POS_TARGET1    = (1136) # R/W
ROH_FINGER_POS_TARGET2    = (1137) # R/W
ROH_FINGER_POS_TARGET3    = (1138) # R/W
ROH_FINGER_POS_TARGET4    = (1139) # R/W
ROH_FINGER_POS_TARGET5    = (1140) # R/W
ROH_FINGER_POS_TARGET6    = (1141) # R/W
ROH_FINGER_POS_TARGET7    = (1142) # R/W
ROH_FINGER_POS_TARGET8    = (1143) # R/W
ROH_FINGER_POS_TARGET9    = (1144) # R/W
ROH_FINGER_POS0           = (1145) # R
ROH_FINGER_POS1           = (1146) # R
ROH_FINGER_POS2           = (1147) # R
ROH_FINGER_POS3           = (1148) # R
ROH_FINGER_POS4           = (1149) # R
ROH_FINGER_POS5           = (1150) # R
ROH_FINGER_POS6           = (1151) # R
ROH_FINGER_POS7           = (1152) # R
ROH_FINGER_POS8           = (1153) # R
ROH_FINGER_POS9           = (1154) # R
ROH_FINGER_ANGLE_TARGET0  = (1155) # R/W
ROH_FINGER_ANGLE_TARGET1  = (1156) # R/W
ROH_FINGER_ANGLE_TARGET2  = (1157) # R/W
ROH_FINGER_ANGLE_TARGET3  = (1158) # R/W
ROH_FINGER_ANGLE_TARGET4  = (1159) # R/W
ROH_FINGER_ANGLE_TARGET5  = (1160) # R/W
ROH_FINGER_ANGLE_TARGET6  = (1161) # R/W
ROH_FINGER_ANGLE_TARGET7  = (1162) # R/W
ROH_FINGER_ANGLE_TARGET8  = (1163) # R/W
ROH_FINGER_ANGLE_TARGET9  = (1164) # R/W
ROH_FINGER_ANGLE0         = (1165) # R
ROH_FINGER_ANGLE1         = (1166) # R
ROH_FINGER_ANGLE2         = (1167) # R
ROH_FINGER_ANGLE3         = (1168) # R
ROH_FINGER_ANGLE4         = (1169) # R
ROH_FINGER_ANGLE5         = (1170) # R
ROH_FINGER_ANGLE6         = (1171) # R
ROH_FINGER_ANGLE7         = (1172) # R
ROH_FINGER_ANGLE8         = (1173) # R
ROH_FINGER_ANGLE9         = (1174) # R

ROH_FINGER_FORCE0         = (1175) # R
ROH_FINGER_FORCE1         = (1176) # R
ROH_FINGER_FORCE2         = (1177) # R
ROH_FINGER_FORCE3         = (1178) # R
ROH_FINGER_FORCE4         = (1179) # R
ROH_FINGER_FORCE5         = (1180) # R
ROH_FINGER_FORCE6         = (1181) # R
ROH_FINGER_FORCE7         = (1182) # R
ROH_FINGER_FORCE8         = (1183) # R
ROH_FINGER_FORCE9         = (1184) # R

# 当前版本号信息
PROTOCOL_VERSION = 'V1.0.0'
FW_VERSION = 'V3.0.0'
FW_REVISION = 'V0.130'
HW_VERSION = '1B01'
BOOT_VERSION = 'V1.7.0'

#设备寄存器的默认值，测试后用于恢复，否则设备可能无法使用

SELF_TEST_LEVEL       = 1 # 开机自检开关， 0 时等待 ROH_START_INIT 写 1 自检，设成 1 时允许开机归零，设成 2 时允许开机完整
BEEP_SWITCH           = 1 # 蜂鸣器开关，1 时允许发声，0 时蜂鸣器静音
BEEP_PERIOD           = 500 # 蜂鸣器发声时常（单位毫)
NODE_ID               = 2 # 设备ID默认的值为2

FINGER_P0             = 25000 # 大拇指弯曲 P 值
FINGER_P1             = 25000 # 食指弯曲 P 值
FINGER_P2             = 25000 # 中指弯曲 P 值
FINGER_P3             = 25000 # 无名指弯曲 P 值
FINGER_P4             = 25000 # 小指弯曲 P 值
FINGER_P5             = 25000 # 大拇指旋转 P 值

FINGER_I0             = 200 # 大拇指弯曲 I 值
FINGER_I1             = 200 # 食指弯曲 I 值
FINGER_I2             = 200 # 中指弯曲 I 值
FINGER_I3             = 200 # 无名指弯曲 I 值
FINGER_I4             = 200 # 小指弯曲 I 值
FINGER_I5             = 200 # 大拇指旋转 I 值


FINGER_D0             = 25000 # 大拇指弯曲 D 值
FINGER_D1             = 25000 # 食指弯曲 D 值
FINGER_D2             = 25000 # 中指弯曲 D 值
FINGER_D3             = 25000 # 无名指弯曲 D 值
FINGER_D4             = 25000 # 小指弯曲 D 值
FINGER_D5             = 25000 # 大拇指旋转 D 值


FINGER_G0             = 100 # 大拇指弯曲 G 值
FINGER_G1             = 100 # 食指弯曲 G 值
FINGER_G2             = 100 # 中指弯曲 G 值
FINGER_G3             = 100 # 无名指弯曲 G 值
FINGER_G4             = 100 # 小指弯曲 G 值
FINGER_G5             = 100 # 大拇指旋转 G 值


FINGER_CURRENT_LIMIT0  = 1299 # 大拇指弯曲电机电流限制值（mA）
FINGER_CURRENT_LIMIT1  = 1299 # 食指弯曲电机电流限制值（mA）
FINGER_CURRENT_LIMIT2  = 1299 # 中指弯曲电机电流限制值（mA）
FINGER_CURRENT_LIMIT3  = 1299 # 无名指弯曲电机电流限制值（mA）
FINGER_CURRENT_LIMIT4  = 1299 # 小指弯曲电机电流限制值（mA） 
FINGER_CURRENT_LIMIT5  = 1299 # 大拇指旋转电机电流限制值（mA）

FINGER_FORCE_TARGET0 = 0 # 大拇指力量目标值（uint16），单位 mN
FINGER_FORCE_TARGET1 = 0 # 食指力量目标值（uint16），单位 mN
FINGER_FORCE_TARGET2 = 0 # 中指力量目标值（uint16），单位 mN
FINGER_FORCE_TARGET3 = 0 # 无名指力量目标值（uint16），单位 mN
FINGER_FORCE_TARGET4 = 0 #  小指力量目标值（uint16），单位 mN


FINGER_FORCE_LIMIT0  = 15000 # 大拇指力量限制值（单位 mN）
FINGER_FORCE_LIMIT1  = 15000 # 食指指力量限制值（单位 mN）
FINGER_FORCE_LIMIT2  = 15000 # 中指力量限制值（单位 mN）
FINGER_FORCE_LIMIT3  = 15000 # 无名指力量限制值（单位 mN）
FINGER_FORCE_LIMIT4  = 15000 # 小指力量限制值（单位 mN）

FINGER_SPEED0 = 65535 # 大拇指弯曲逻辑速度（逻辑位置/秒）
FINGER_SPEED1 = 65535 # 食指弯曲逻辑速度（逻辑位置/秒）
FINGER_SPEED2 = 65535 # 中指弯曲逻辑速度（逻辑位置/秒）
FINGER_SPEED3 = 65535 # 无名指弯曲逻辑速度（逻辑位置/秒）
FINGER_SPEED4 = 65535 # 小指弯曲逻辑速度（逻辑位置/秒）
FINGER_SPEED5 = 65535 # 大拇旋转逻辑速度（逻辑位置/秒）

FINGER_POS_TARGET0 = 0 #大拇指弯曲逻辑目标位置
FINGER_POS_TARGET1 = 0 #食指弯曲逻辑目标位置
FINGER_POS_TARGET2 = 0 #中指弯曲逻辑目标位置
FINGER_POS_TARGET3 = 0 #无名指弯曲逻辑目标位置
FINGER_POS_TARGET4 = 0 #小指弯曲逻辑目标位置
FINGER_POS_TARGET5 = 728 #大拇旋转指逻辑目标位置
FINGER_POS_TARGET_MAX_LOSS = 32 # 位置最大精度损失


FINGER_ANGLE_TARGET0 = 32367 # 大拇指电机轴与旋转轴夹角的目标值
FINGER_ANGLE_TARGET1 = 32367 # 食指第一节与掌平面夹角的目标值
FINGER_ANGLE_TARGET2 = 32367 # 中指第一节与掌平面夹角的目标值
FINGER_ANGLE_TARGET3 = 32367 # 无名指第一节与掌平面夹角的目标值
FINGER_ANGLE_TARGET4 = 32367 # 小指第一节与掌平面夹角的目标值
FINGER_ANGLE_TARGET5 = 0 # 大拇旋转目标角度
FINGER_ANGLE_TARGET_MAX_LOSS = 5 # 角度最大精度损失


# WAIT_TIME = 0.1 # 延迟打印，方便查看

class TestModbusProtocol:
    TEST_START = 0X0
    TEST_END = 0X3

    roh_test_status_list = {
        TEST_START: '开始测试',
        TEST_END: '测试结束',
    }

    def print_test_info(self, status, info=''):
        # 检查 status 是否为合法值
        if status not in self.roh_test_status_list:
            raise ValueError(f"Invalid status value: {status}")
       
        start_message = f'###########################  {self.roh_test_status_list.get(status)} <{info}> ############################'
        border = '-' * len(start_message)
        logger.info(border)
        logger.info(start_message)
        logger.info(border + '\n')
       
    def isNotNone(self, response):
        logger.info(f'isNotNone-->{response.registers[0] }')
        return response is not None
    
    @pytest.fixture(autouse=True)
    def modbus(self):
        """
        pytest 夹具，用于初始化 modbus 总线连接，并在测试结束后关闭连接
        """
        self.bus = setup_modbus()
        if self.bus is None:
            logger.error("Could not connect to  modbus. Skipping tests.")
            pytest.skip("Could not connect to modbus. Skipping tests.")
        yield
        try:
            close_modbus(self.bus)
            self.bus = None
        except Exception as e:
            logger.error(f"Error closing modbus connection: {e}")
            
    def to_version(self, response):
        major_version = (response.registers[0] >> 8) & 0xFF
        # 提取次版本号（低 8 位）
        minor_version = response.registers[0] & 0xFF
        version_str = f"V{major_version}.{minor_version}"
        return version_str
            
    def to_revision(self,response):
        # revision = ((response & 0xFF) << 8) | ((response >> 8) & 0xFF) 
        revision = response.registers[0]  # 高低位已经兑换过，这里不需要额外操作
        return f'V{revision}'
    
    # def to_integer(self,byte_list):
    #     """
    #     将包含两个字节的列表转换为整数，列表中第一个元素为低位字节，第二个元素为高位字节
    #     :param byte_list: 包含两个字节的列表
    #     :return: 组合后的整数
    #     """
    #     if len(byte_list) != 2:
    #         raise ValueError("输入的列表必须包含两个字节")
    #     low_byte = byte_list[0]
    #     high_byte = byte_list[1]
    #     return (high_byte << 8) | low_byte
            
    def test_read_protocol_version(self):
        self.print_test_info(status=self.TEST_START, info='read protocol version')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_PROTOCOL_VERSION, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_PROTOCOL_VERSION}>失败'
            logger.info(f'读取寄存器<{ROH_PROTOCOL_VERSION}>成功,读取的值为:{self.to_version(response=response)}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_PROTOCOL_VERSION}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_PROTOCOL_VERSION}>失败,发生异常')
            
    def test_read_fw_version(self):
        self.print_test_info(status=self.TEST_START, info='read fireware version')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FW_VERSION, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FW_VERSION}>失败'
            logger.info(f'读取寄存器<{ROH_FW_VERSION}>成功,读取的值为:{self.to_version(response=response)}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FW_VERSION}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FW_VERSION}>失败,发生异常')
            
    def test_read_fw_revision(self):
        self.print_test_info(status=self.TEST_START, info='read fireware revision')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FW_REVISION, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FW_REVISION}>失败'
            logger.info(f'读取寄存器<{ROH_FW_REVISION}>成功,读取的值为:{self.to_revision(response=response)}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FW_REVISION}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FW_REVISION}>失败,发生异常')
            
    def test_read_hw_version(self):
        self.print_test_info(status=self.TEST_START, info='read hardware version')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_HW_VERSION, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_HW_VERSION}>失败'
            logger.info(f'读取寄存器<{ROH_HW_VERSION}>成功,读取的值为:{self.to_version(response=response)}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_HW_VERSION}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_HW_VERSION}>失败,发生异常')
    
    def test_read_boot_version(self):
        self.print_test_info(status=self.TEST_START, info='read boot loader version')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_BOOT_VERSION, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_BOOT_VERSION}>失败'
            logger.info(f'读取寄存器<{ROH_BOOT_VERSION}>成功,读取的值为:{self.to_version(response=response)}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_BOOT_VERSION}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_BOOT_VERSION}>失败,发生异常')
            
    def test_read_nodeID_version(self):
        self.print_test_info(status=self.TEST_START, info='read node id')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_NODE_ID, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_NODE_ID}>失败'
            logger.info(f'读取寄存器<{ROH_NODE_ID}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_NODE_ID}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_NODE_ID}>失败,发生异常')
            
    def wait_device_reboot(self, max_attempts=60, delay_time=1,target_node_id = 2):
        attempt_count = 0
        while attempt_count < max_attempts:
            logger.info(f'等待设备重启中...{attempt_count}')
            time.sleep(delay_time)
            self.bus = setup_modbus()
            if self.bus is None:
                attempt_count += 1
                continue
            # if(attempt_count % 5 == 0):
            response = read_registers(bus=self.bus,start_address=ROH_NODE_ID,register_count=1,node_id=target_node_id)
            if(self.isNotNone(response=response)):
                logger.info(f'wait_device_reboot-->check = {response.registers[0]}')
                logger.info(f'设备已启动')
                break
            attempt_count += 1
        # attempt_count = 0
        # while attempt_count < max_attempts:
        #     logger.info(f'等待设备重启中...{attempt_count}')
        #     time.sleep(delay_time)
        #     self.bus = setup_modbus()
        #     if(attempt_count % 5 == 0  and self.isNotNone(self.bus)):
        #         response = read_registers(bus=self.bus,start_address=ROH_NODE_ID,register_count=1,node_id=target_node_id)
        #         if(self.isNotNone(response=response)):
        #             logger.info(f'设备已启动')
        #             break
        #     attempt_count += 1
            
    @pytest.mark.skip('skip write node id,some bug need to fix')
    def test_write_nodeID_version(self):
        self.print_test_info(status=self.TEST_START,info='write node id,The normal range is [2, 247]')
        verify_sets = [
            3
        ]
        default_node_id = 2 # 默认设备ID为2
        for index,value in enumerate(verify_sets):
            try:
                # if index == 0:
                current_node_id = NODE_ID #将值转换成十进制
                # else :
                    # current_node_id = verify_sets[index-1]
                data = value
                logger.info(f'当前的node id = {current_node_id}，要写入的 node id ={data}')
                write_response1 = write_registers(self.bus, start_address=ROH_NODE_ID, data=value,node_id=current_node_id)
                assert write_response1,f'写寄存器{ROH_NODE_ID}失败\n'
                
                self.wait_device_reboot(max_attempts=60,delay_time=1,target_node_id=data)
                read_response1 = read_registers(bus=self.bus,start_address=ROH_NODE_ID, register_count=1,node_id=value)
                assert read_response1.registers[0] == data, f"从寄存器{ROH_NODE_ID}读出的值{read_response1.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_NODE_ID}读出的值{read_response1.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                logger.error(f"写寄存器<{ROH_NODE_ID}>失败,发生异常: {e}")
                pytest.fail(f'写寄存器<{ROH_NODE_ID}>失败,发生异常')
                
        #恢复默认值
        try:
            logger.info("开始恢复默认值\n")
            write_response2 = write_registers(self.bus, start_address=ROH_NODE_ID, data=NODE_ID,node_id=3)
            self.wait_device_reboot(max_attempts=60,delay_time=1)
            assert write_response2, f"恢复默认值失败\n"
            read_response2 = read_registers(bus=self.bus,start_address=ROH_NODE_ID, register_count=1,node_id=NODE_ID)
            assert read_response2.registers[0] == NODE_ID, f"从寄存器{ROH_NODE_ID}读出的值{read_response2.registers[0]}与写入的值{data}不匹配"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
                
            
    def test_read_battery_voltage(self):
        self.print_test_info(status=self.TEST_START, info='read battery_voltage')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_BATTERY_VOLTAGE, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_BATTERY_VOLTAGE}>失败'
            logger.info(f'读取寄存器<{ROH_BATTERY_VOLTAGE}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_BATTERY_VOLTAGE}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_BATTERY_VOLTAGE}>失败,发生异常')
    
    def test_read_self_test_level(self):
        self.print_test_info(status=self.TEST_START, info='read self test level')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_SELF_TEST_LEVEL, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_SELF_TEST_LEVEL}>失败'
            logger.info(f'读取寄存器<{ROH_SELF_TEST_LEVEL}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_SELF_TEST_LEVEL}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_SELF_TEST_LEVEL}>失败,发生异常')
    
    def test_write_self_test_level(self):
        self.print_test_info(status=self.TEST_START, info='write self test level,The normal range is {0, 1, 2}, and the out-of-range values fall within {3, 65535}')
        verify_sets = [
            0,
            1,
            2,
            3,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_SELF_TEST_LEVEL, data=value,node_id = NODE_ID)
                data = value #将值转换成十进制
                if index > 2:
                    assert not response, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_SELF_TEST_LEVEL, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_SELF_TEST_LEVEL}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_SELF_TEST_LEVEL}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_SELF_TEST_LEVEL}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_SELF_TEST_LEVEL}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_SELF_TEST_LEVEL, data=SELF_TEST_LEVEL)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_beep_switch(self):
        self.print_test_info(status=self.TEST_START, info='read beep switch')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_BEEP_SWITCH, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_BEEP_SWITCH}>失败'
            logger.info(f'读取寄存器<{ROH_BEEP_SWITCH}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_BEEP_SWITCH}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_BEEP_SWITCH}>失败,发生异常')
                
    def test_write_beep_switch(self):
        self.print_test_info(status=self.TEST_START, info='write beep switch,The normal range is 0 or not 0')
        verify_sets = [
            0,
            1,
            255
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_BEEP_SWITCH, data=value)
                data = value
                if index > 0:
                    expected_data = 1
                else :
                    expected_data = 0
                read_response = read_registers(bus=self.bus, start_address=ROH_BEEP_SWITCH, register_count=1)
                assert read_response.registers[0] == expected_data, f"从寄存器{ROH_BEEP_SWITCH}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_BEEP_SWITCH}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_BEEP_SWITCH}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_BEEP_SWITCH}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_BEEP_SWITCH, data=BEEP_SWITCH)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
        
        
    def test_write_beep_period(self):
        self.print_test_info(status=self.TEST_START, info='write beep period,The normal range is [1,65535], and the out-of-range values fall within [0]')
        verify_sets = [
            0,
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_BEEP_PERIOD, data=
                                           value)
                data = value
                if index ==0:
                    assert not response, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    # read_response = read_registers(bus=self.bus, start_address=ROH_BEEP_PERIOD, register_count=1)
                    assert response, f"写寄存器{ROH_BEEP_PERIOD}失败，写入值为{data}"
                    logger.info(f"写寄存器{ROH_BEEP_PERIOD}成功,写入值为{data}\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_BEEP_PERIOD}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_BEEP_PERIOD}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_BEEP_PERIOD, data=BEEP_PERIOD)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_P0(self):
        self.print_test_info(status=self.TEST_START,info='read finger P0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P0}>失败,发生异常')
  
    def test_write_finger_P0(self):
        self.print_test_info(status=self.TEST_START, info='write finger P0,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P0, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P0, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P0, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P0, data=FINGER_P0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_P1(self):
        self.print_test_info(status=self.TEST_START,info='read finger P1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P1}>失败,发生异常')
  
    def test_write_finger_P1(self):
        self.print_test_info(status=self.TEST_START, info='write finger P1,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P1, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P1, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P1, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P1}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P1, data=FINGER_P1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_P2(self):
        self.print_test_info(status=self.TEST_START,info='read finger P2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P2}>失败,发生异常')
  
    def test_write_finger_P2(self):
        self.print_test_info(status=self.TEST_START, info='write finger P2,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P2, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P2, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P2, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P2, data=FINGER_P2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_P3(self):
        self.print_test_info(status=self.TEST_START,info='read finger P3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P3}>失败,发生异常')
  
    def test_write_finger_P3(self):
        self.print_test_info(status=self.TEST_START, info='write finger P3,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P3, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P3, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P3, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P3, data=FINGER_P3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_P4(self):
        self.print_test_info(status=self.TEST_START,info='read finger P4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P4}>失败,发生异常')
  
    def test_write_finger_P4(self):
        self.print_test_info(status=self.TEST_START, info='write finger P4,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P4, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P4, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P4, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P4, data=FINGER_P4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
    
    def test_read_finger_P5(self):
        self.print_test_info(status=self.TEST_START,info='read finger P5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_P5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_P5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_P5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_P5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_P5}>失败,发生异常')
  
    def test_write_finger_P5(self):
        self.print_test_info(status=self.TEST_START, info='write finger P5,The normal range is [100,50000], and the out-of-range values fall within {0,1,99,50001,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            99,# 99
            100,# 100
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_P5, data=value)
                data = value
                if index <= 2 or index >= 6 : # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P5, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_P5, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_P5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_P5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_P5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_P5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_P5, data=FINGER_P5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_I0(self):
        self.print_test_info(status=self.TEST_START,info='read finger I0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I0}>失败,发生异常')
  
    def test_write_finger_I0(self):
        self.print_test_info(status=self.TEST_START, info='write finger I0,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I0, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I0, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I0, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I0, data=FINGER_I0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_I1(self):
        self.print_test_info(status=self.TEST_START,info='read finger I1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I1}>失败,发生异常')
  
    def test_write_finger_I1(self):
        self.print_test_info(status=self.TEST_START, info='write finger I1,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I1, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I1, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I1, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I1}读出的值{read_response.registers[0]           }与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I1, data=FINGER_I1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_I2(self):
        self.print_test_info(status=self.TEST_START,info='read finger I2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I2}>失败,发生异常')
  
    def test_write_finger_I2(self):
        self.print_test_info(status=self.TEST_START, info='write finger I2,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I2, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I2, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I2, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I2, data=FINGER_I2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
    
    def test_read_finger_I3(self):
        self.print_test_info(status=self.TEST_START,info='read finger I3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I3}>失败,发生异常')
  
    def test_write_finger_I3(self):
        self.print_test_info(status=self.TEST_START, info='write finger I3,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I3, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I3, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I3, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I3, data=FINGER_I3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_I4(self):
        self.print_test_info(status=self.TEST_START,info='read finger I4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I4}>失败,发生异常')
  
    def test_write_finger_I4(self):
        self.print_test_info(status=self.TEST_START, info='write finger I4,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I4, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I4, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I4, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I4, data=FINGER_I4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_I5(self):
        self.print_test_info(status=self.TEST_START,info='read finger I5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_I5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_I5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_I5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_I5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_I5}>失败,发生异常')
  
    def test_write_finger_I5(self):
        self.print_test_info(status=self.TEST_START, info='write finger I5,The normal range is [0,10000], and the out-of-range values fall within {10001,65535}')
        verify_sets = [
            0,# 0
            5000,# 5000
            10000,# 10000
            10001,# 10001
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_I5, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I5, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_I5, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_I5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_I5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_I5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_I5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_I5, data=FINGER_I5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
    
    
    def test_read_finger_D0(self):
        self.print_test_info(status=self.TEST_START,info='read finger D0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D0}>失败,发生异常')
  
    def test_write_finger_D0(self):
        self.print_test_info(status=self.TEST_START, info='write finger D0,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D0, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D0, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D0, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D0, data=FINGER_D0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_D1(self):
        self.print_test_info(status=self.TEST_START,info='read finger D1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D1}>失败,发生异常')
  
    def test_write_finger_D1(self):
        self.print_test_info(status=self.TEST_START, info='write finger D1,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D1, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D1, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D1, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D1}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D1, data=FINGER_D1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_D2(self):
        self.print_test_info(status=self.TEST_START,info='read finger D2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D2}>失败,发生异常')
  
    def test_write_finger_D2(self):
        self.print_test_info(status=self.TEST_START, info='write finger D2,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D2, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D2, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D2, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D2, data=FINGER_D2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_D3(self):
        self.print_test_info(status=self.TEST_START,info='read finger D3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D3}>失败,发生异常')
  
    def test_write_finger_D3(self):
        self.print_test_info(status=self.TEST_START, info='write finger D3,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D3, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D3, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D3, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D3, data=FINGER_D3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_D4(self):
        self.print_test_info(status=self.TEST_START,info='read finger D4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D4}>失败,发生异常')
  
    def test_write_finger_D4(self):
        self.print_test_info(status=self.TEST_START, info='write finger D4,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D4, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D4, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D4, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D4, data=FINGER_D4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_D5(self):
        self.print_test_info(status=self.TEST_START,info='read finger D5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_D5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_D5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_D5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_D5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_D5}>失败,发生异常')
  
    def test_write_finger_D5(self):
        self.print_test_info(status=self.TEST_START, info='write finger D5,The normal range is [0,50000], and the out-of-range values fall within {50001,65535}')
        verify_sets = [
            0,# 0
            25000,# 25000
            50000,# 50000 
            50001,# 50001 
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_D5, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D5, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_D5, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_D5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_D5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_D5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_D5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_D5, data=FINGER_D5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_G0(self):
        self.print_test_info(status=self.TEST_START,info='read finger G0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G0}>成功,读取的值为:{response}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G0}>失败,发生异常')
  
    def test_write_finger_G0(self):
        self.print_test_info(status=self.TEST_START, info='write finger G0,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G0, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G0, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G0, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G0, data=FINGER_G0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_G1(self):
        self.print_test_info(status=self.TEST_START,info='read finger G1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G1}>失败,发生异常')
  
    def test_write_finger_G1(self):
        self.print_test_info(status=self.TEST_START, info='write finger G1,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G1, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G1, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G1, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G1}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G1, data=FINGER_G1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_G2(self):
        self.print_test_info(status=self.TEST_START,info='read finger G2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G2}>失败,发生异常')
  
    def test_write_finger_G2(self):
        self.print_test_info(status=self.TEST_START, info='write finger G2,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G2, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G2, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G2, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G2, data=FINGER_G2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_G3(self):
        self.print_test_info(status=self.TEST_START,info='read finger G3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G3}>失败,发生异常')
  
    def test_write_finger_G3(self):
        self.print_test_info(status=self.TEST_START, info='write finger G3,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G3, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G3, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G3, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G3, data=FINGER_G3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_G4(self):
        self.print_test_info(status=self.TEST_START,info='read finger G4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G4}>失败,发生异常')
  
    def test_write_finger_G4(self):
        self.print_test_info(status=self.TEST_START, info='write finger G4,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G4, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G4, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G4, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G4, data=FINGER_G4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_G5(self):
        self.print_test_info(status=self.TEST_START,info='read finger G5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_G5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_G5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_G5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_G5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_G5}>失败,发生异常')
  
    def test_write_finger_G5(self):
        self.print_test_info(status=self.TEST_START, info='write finger G5,The normal range is [1,100], and the out-of-range values fall within {0,101,65535}')
        verify_sets = [
            0,# 0
            1,# 1
            50,# 50
            100,# 100
            101,# 101
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_G5, data=value)
                data = value
                if index ==0 or index > 3: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G5, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_G5, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_G5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_G5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_G5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_G5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_G5, data=FINGER_G5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_status0(self):
        self.print_test_info(status=self.TEST_START,info='read finger status0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS0}>失败,发生异常')
            
    def test_read_finger_status1(self):
        self.print_test_info(status=self.TEST_START,info='read finger status1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS1}>失败,发生异常')
            
    def test_read_finger_status2(self):
        self.print_test_info(status=self.TEST_START,info='read finger status2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS2}>失败,发生异常')
            
    def test_read_finger_status3(self):
        self.print_test_info(status=self.TEST_START,info='read finger status3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS3}>失败,发生异常')
            
    def test_read_finger_status4(self):
        self.print_test_info(status=self.TEST_START,info='read finger status4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS4}>失败,发生异常')
            
    def test_read_finger_status5(self):
        self.print_test_info(status=self.TEST_START,info='read finger status5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_STATUS5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_STATUS5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_STATUS5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_STATUS5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_STATUS5}>失败,发生异常')
            
    def test_read_finger_current_limit0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT0}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit0(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit0,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, data=FINGER_CURRENT_LIMIT0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current_limit1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT1}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit1(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit1,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT1, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT1, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT1, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT1}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT1, data=FINGER_CURRENT_LIMIT1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current_limit2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT2}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit2(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit2,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT2, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT2, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT2, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT2, data=FINGER_CURRENT_LIMIT2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current_limit3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT3}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit3(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit3,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT3, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT3, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT3, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT3, data=FINGER_CURRENT_LIMIT3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current_limit4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT4}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit4(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit4,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT4, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT4, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT4, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT4, data=FINGER_CURRENT_LIMIT4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current_limit5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current limit5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT_LIMIT5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT_LIMIT5}>失败,发生异常')
    
    # @pytest.mark.skip('1200边界值写入后,读出来是1178,需要研发修改')        
    def test_write_current_limit5(self):
        self.print_test_info(status=self.TEST_START, info='write finger current limit5,The normal range is [0,1299], and the out-of-range values fall within {1300,65535}')
        verify_sets = [
            0,# 0
            600,# 600
            1299,# 1299
            1300,# 1300
            65535# 65535 
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT5, data=value)
                data = value
                if index > 2: # 异常值写进去不生效,底层不报错
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT5, register_count=1)
                    assert read_response.registers[0] != data, f"超出范围的值{data}未被检测出\n"
                    logger.info(f"成功检测出超出范围的值{data}\n")
                else:
                    read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT5, register_count=1)
                    assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_CURRENT_LIMIT5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                    logger.info(f"从寄存器{ROH_FINGER_CURRENT_LIMIT5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_CURRENT_LIMIT5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_CURRENT_LIMIT5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT5, data=FINGER_CURRENT_LIMIT5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_current0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT0}>失败,发生异常')
            
    def test_read_finger_current1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT1}>失败,发生异常')
            
    def test_read_finger_current2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT2}>失败,发生异常')
            
    def test_read_finger_current3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT3}>失败,发生异常')
            
    def test_read_finger_current4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT4}>失败,发生异常')
            
    def test_read_finger_current5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger current5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_CURRENT5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_CURRENT5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_CURRENT5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_CURRENT5}>失败,发生异常')
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit0')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit0(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit0')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit1')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit1(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit1')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit2')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit2(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit2')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit3')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit3(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit3')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit4')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit4(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit4')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_read_finger_force_limit5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force limit5')
        pass
    
    @pytest.mark.skip('力传感器暂未添加，先跳过')
    def test_write_finger_force_limit5(self):
        self.print_test_info(status=self.TEST_START,info='write finger force limit5')
        pass
    
    def test_read_finger_force0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_FORCE0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_FORCE0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_FORCE0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_FORCE0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_FORCE0}>失败,发生异常')
            
    def test_read_finger_force1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_FORCE1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_FORCE1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_FORCE1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_FORCE1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_FORCE1}>失败,发生异常')
            
    def test_read_finger_force2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_FORCE2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_FORCE2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_FORCE2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_FORCE2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_FORCE2}>失败,发生异常')
            
    def test_read_finger_force3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_FORCE3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_FORCE3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_FORCE3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_FORCE3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_FORCE3}>失败,发生异常')
            
    def test_read_finger_force4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger force4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_FORCE4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_FORCE4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_FORCE4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_FORCE4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_FORCE4}>失败,发生异常')
            
    def test_read_finger_speed0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED0}>失败,发生异常')
            
    def test_write_finger_speed0(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed0,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED0, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED0, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED0}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED0}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED0, data=FINGER_SPEED0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_speed1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED1}>失败,发生异常')
            
    def test_write_finger_speed1(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed1,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED1, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED1, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED1}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED1}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED1, data=FINGER_SPEED1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_speed2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED2}>失败,发生异常')
            
    def test_write_finger_speed2(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed2,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED2, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED2, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED2}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED2}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED2, data=FINGER_SPEED2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_speed3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED3}>失败,发生异常')
            
    def test_write_finger_speed3(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed3,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED3, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED3, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED3}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED3}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED3, data=FINGER_SPEED3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_speed4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED4}>失败,发生异常')
            
    def test_write_finger_speed4(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed4,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED4, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED4, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED4}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED4}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED4, data=FINGER_SPEED4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_speed5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger speed5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_SPEED5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_SPEED5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_SPEED5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_SPEED5}>失败,发生异常')
            
    def test_write_finger_speed5(self):
        self.print_test_info(status=self.TEST_START, info='write finger speed5,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_SPEED5, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_SPEED5, register_count=1)
                assert read_response.registers[0] == data, f"从寄存器{ROH_FINGER_SPEED5}读出的值{read_response.registers[0]}与写入的值{data}不匹配"
                logger.info(f"从寄存器{ROH_FINGER_SPEED5}读出的值{read_response.registers[0]}与写入的值{data}匹配成功\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_SPEED5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_SPEED5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_SPEED5, data=FINGER_SPEED5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET0}>失败,发生异常')
            
    def test_write_finger_pos_target0(self):
        self.print_test_info(status=self.TEST_START, info='write finger pos target0,The normal range is [0,65535]')
        verify_sets = [
            # 0, 
            # 1,
            728,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET0, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET0, register_count=1)
                assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET0, data=FINGER_POS_TARGET0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET1}>失败,发生异常')
            
    def test_write_finger_pos_target1(self):
        self.print_test_info(status=self.TEST_START, info='write finger pos target1,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET1, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET1, register_count=1)
                assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET1, data=FINGER_POS_TARGET1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET2}>失败,发生异常')
            
    def test_write_finger_pos_target2(self):
        self.print_test_info(status=self.TEST_START, info='write finger pos target2,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET2, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET2, register_count=1)
                assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET2, data=FINGER_POS_TARGET2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET3}>失败,发生异常')
            
    def test_write_finger_pos_target3(self):
        self.print_test_info(status=self.TEST_START, info='write finger pos target3,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET3, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET3, register_count=1)
                assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET3, data=FINGER_POS_TARGET3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET4}>失败,发生异常')
            
    def test_write_finger_pos_target4(self):
        self.print_test_info(status=self.TEST_START, info='write finger pos target4,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET4, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET4, register_count=1)
                assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET4, data=FINGER_POS_TARGET4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_pos_target5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos target5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS_TARGET5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS_TARGET5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS_TARGET5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS_TARGET5}>失败,发生异常')
    
    def test_write_finger_pos_target5(self): #从寄存器1140读出的值728与写入的值0比较
        self.print_test_info(status=self.TEST_START, info='write finger pos target5,The normal range is [0,65535]')
        verify_sets = [
            0, 
            1,
            728,
            32767,
            32768,
            65535
        ]
        
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET5, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS_TARGET5, register_count=1)
                if index in(0,1,2):
                    assert read_response.registers[0] == FINGER_POS_TARGET5, f"从寄存器{ROH_FINGER_POS_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                else:    
                    assert abs(read_response.registers[0] - data) <= FINGER_POS_TARGET_MAX_LOSS, f"从寄存器{ROH_FINGER_POS_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n"
                logger.info(f"从寄存器{ROH_FINGER_POS_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_POS_TARGET5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_POS_TARGET5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_POS_TARGET5, data=FINGER_POS_TARGET5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
 
    def test_read_finger_pos0(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS0}>失败,发生异常')
    
    def test_read_finger_pos1(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS1}>失败,发生异常')
            
    def test_read_finger_pos2(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS2}>失败,发生异常')
            
    def test_read_finger_pos3(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS3}>失败,发生异常')
            
    def test_read_finger_pos4(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS4}>失败,发生异常')
            
    def test_read_finger_pos5(self):                                                                                                                                                                                                                                                                                                                                                                                                           
        self.print_test_info(status=self.TEST_START,info='read finger pos5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_POS5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_POS5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_POS5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_POS5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_POS5}>失败,发生异常')
            
    def get_min_angle(self,addr):
        values = 0
        if write_registers(bus=self.bus,start_address=addr,data=values):
           response = read_registers(bus=self.bus,start_address=addr,register_count=1)
           logger.info(f'get min angle : {addr} ->{response.registers[0]}')
           return response.registers[0]
        else:
            logger.info(f'get min angle : {addr} 尝试获取最小值失败')
            return 0
        
    def get_max_angle(self,addr):
        values = 32767
        if write_registers(bus=self.bus,start_address=addr,data=values):
           response = read_registers(bus=self.bus,start_address=addr,register_count=1)
           logger.info(f'get max angle : {addr} ->{response.registers[0]}')
           return response.registers[0]
        else:
            logger.info(f'get max angle : {addr} 尝试获取最大值失败')
            return 32767
        
    def get_max_negative_angle(self,addr):
        values = 32768
        if write_registers(bus=self.bus,start_address=addr,data=values):
           response = read_registers(bus=self.bus,start_address=addr,register_count=1)
           logger.info(f'get max negative angle : {addr} ->{response.registers[0]}')
           return response.registers[0]
        else:
            logger.info(f'get max negative angle : {addr} 尝试获取最大负值失败')
            return 32768
        
    def get_min_negative_angle(self,addr):
        values = 65535
        if write_registers(bus=self.bus,start_address=addr,data=values):
           response = read_registers(bus=self.bus,start_address=addr,register_count=1)
           logger.info(f'get min negative angle : {addr} ->{response.registers[0]}')
           return response.registers[0]
        else:
            logger.info(f'get max negative angle : {addr} 尝试获取最小负值失败')
            return 65535
        
    def test_read_finger_angle_target0(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET0}>失败,发生异常')
            
    def test_write_finger_angle_target0(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target0,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET0)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET0)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET0)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET0)
        # NORMAL_NEG_ANGLE= int(MIN_NEG_ANGLE + (MAX_NEG_ANGLE - MIN_NEG_ANGLE)/2)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,#32768,max negative value
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535#65535,min value
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET0, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET0, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4:
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 5:
                     assert read_response.registers[0] == MAX_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET0}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET0}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET0}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET0, data=FINGER_ANGLE_TARGET0)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_angle_target1(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET1}>失败,发生异常')
            
    def test_write_finger_angle_target1(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target1,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET1)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET1)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET1)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET1)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET1, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET1, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4 :
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET1}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET1}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET1}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET1, data=FINGER_ANGLE_TARGET1)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
    
            
    def test_read_finger_angle_target2(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET2}>失败,发生异常')
            
    def test_write_finger_angle_target2(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target2,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET2)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET2)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET2)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET2)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET2, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET2, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4 :
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET2}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET2}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET2}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET2, data=FINGER_ANGLE_TARGET2)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_angle_target3(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET3}>失败,发生异常')
            
    def test_write_finger_angle_target3(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target3,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET3)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET3)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET3)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET3)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET3, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET3, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4 :
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET3}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET3}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET3}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET3, data=FINGER_ANGLE_TARGET3)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_angle_target4(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET4}>失败,发生异常')
            
    def test_write_finger_angle_target4(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target4,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET4)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET4)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET4)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET4)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET4, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET4, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4 :
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET4}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET4}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET4}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET4, data=FINGER_ANGLE_TARGET4)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
            
    def test_read_finger_angle_target5(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle target5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE_TARGET5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE_TARGET5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE_TARGET5}>失败,发生异常')
        
    def test_write_finger_angle_target5(self):
        self.print_test_info(status=self.TEST_START, info='write finger angle target5,The normal range is [0,65535]')
        MIN_ANGLE = self.get_min_angle(addr=ROH_FINGER_ANGLE_TARGET5)
        MAX_ANGLE = self.get_max_angle(addr=ROH_FINGER_ANGLE_TARGET5)
        NORMAL_ANGLE= int(MIN_ANGLE + (MAX_ANGLE - MIN_ANGLE)/2)
        MIN_NEG_ANGLE = self.get_min_negative_angle(addr=ROH_FINGER_ANGLE_TARGET5)
        MAX_NEG_ANGLE = self.get_max_negative_angle(addr=ROH_FINGER_ANGLE_TARGET5)
        verify_sets = [
            0, 
            MIN_ANGLE,
            NORMAL_ANGLE,
            MAX_ANGLE,
            32767,#32767,max value
            32768,
            MAX_NEG_ANGLE,
            MIN_NEG_ANGLE,
            65535
        ]
        for index,value in enumerate(verify_sets):
            try:
                response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET5, data=value)
                data = value
                read_response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE_TARGET5, register_count=1)
                if index == 0:
                    assert read_response.registers[0] == MIN_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (1,2,3):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index == 4 :
                    assert read_response.registers[0] == MAX_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                elif index in (6,7):
                    assert abs(read_response.registers[0] - data) <= FINGER_ANGLE_TARGET_MAX_LOSS,f'从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                else:
                    assert read_response.registers[0] == MIN_NEG_ANGLE,f'从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失不符合要求\n'
                logger.info(f"从寄存器{ROH_FINGER_ANGLE_TARGET5}读出的值{read_response.registers[0]}与写入的值{data}比较，精度损失符合要求\n")
            except Exception as e:
                    logger.error(f"写寄存器<{ROH_FINGER_ANGLE_TARGET5}>失败,发生异常: {e}")
                    pytest.fail(f'写寄存器<{ROH_FINGER_ANGLE_TARGET5}>失败,发生异常')
                    
        # 恢复默认值
        logger.info('恢复默认值')
        try:
            write_response = write_registers(self.bus, start_address=ROH_FINGER_ANGLE_TARGET5, data=FINGER_ANGLE_TARGET5)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")
            
    def test_read_finger_angle0(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle0')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE0, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE0}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE0}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE0}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE0}>失败,发生异常')
            
    def test_read_finger_angle1(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle1')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE1, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE1}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE1}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE1}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE1}>失败,发生异常')
            
    def test_read_finger_angle2(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle2')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE2, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE2}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE2}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE2}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE2}>失败,发生异常')
            
    def test_read_finger_angle3(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle3')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE3, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE3}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE3}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE3}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE3}>失败,发生异常')
            
    def test_read_finger_angle4(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle4')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE4, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE4}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE4}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE4}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE4}>失败,发生异常')
            
    def test_read_finger_angle5(self):
        self.print_test_info(status=self.TEST_START,info='read finger angle5')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_ANGLE5, register_count=1)
            assert response is not None,f'读取寄存器<{ROH_FINGER_ANGLE5}>失败'
            logger.info(f'读取寄存器<{ROH_FINGER_ANGLE5}>成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器<{ROH_FINGER_ANGLE5}>失败,发生异常: {e}")
            pytest.fail(f'读取寄存器<{ROH_FINGER_ANGLE5}>失败,发生异常')
      
    # @pytest.mark.skip('暂时跳过多个寄存器的读操作')    
    def test_read_multiple_holding_registers(self):
        self.print_test_info(status=self.TEST_START,info='read multiple registers')
        try:
            response = read_registers(bus=self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, register_count=6)
            assert response is not None,f'读取寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>连续6个寄存器的值失败'
            logger.info(f'读取寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>连续6个寄存器的值成功,读取的值为:{response.registers[0]}')
        except Exception as e:
            logger.error(f"读取寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>连续6个寄存器的值失败,发生异常: {e}")
            pytest.fail(f'读取寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>连续6个寄存器的值失败,发生异常')
            
    # @pytest.mark.skip('暂时跳过多个寄存器的写操作')
    def test_write_multiple_holding_registers(self): 
        self.print_test_info(status=self.TEST_START,info='write multiple registers')
        verify_sets = [600,600,# 600
                       600,600,# 600
                       600,600# 600
        ]
        try:
            response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, data=verify_sets)
            assert response,f'写寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>,连续6个寄存器失败'
            logger.info(f'写寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>,连续6个寄存器成功')
        except Exception as e:
            logger.error(f"写寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>,连续6个寄存器失败,发生异常: {e}")
            pytest.fail(f'写寄存器起始地址<{ROH_FINGER_CURRENT_LIMIT0}>,连续6个寄存器失败,发生异常')
            
         # 恢复默认值
        logger.info('恢复默认值')
        try:
            default_sets = [1200,1200,# 1200
                            1200,1200,# 1200
                            1200,1200 # 1200
        ]
            write_response = write_registers(self.bus, start_address=ROH_FINGER_CURRENT_LIMIT0, data=default_sets)
            assert write_response, f"恢复默认值失败\n"
            logger.info("恢复默认值成功\n")
        except Exception as e:
            logger.error(f"恢复默认值发生了异常: {e}")