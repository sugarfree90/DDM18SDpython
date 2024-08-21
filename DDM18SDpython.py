import time
import struct
#pymodbus version 2.5.3
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(port='/dev/ttyUSB0', method="rtu", baudrate=9600, parity="E",bytesize=8, stopbits=1)


def registerCombiner(registers):
    combined_value = (registers[0] << 16) | registers[1]
    return(struct.unpack('>f', struct.pack('>I', combined_value))[0])

def readValue(itemAddress):
    try:
        # you can read slave address on the screen of the DDM18SD during restart
        rr = client.read_input_registers(address=itemAddress, count=2, slave=14)
        return(registerCombiner(rr.registers))
    except Exception as e:
        print("error "+str(e))
        return(0)
client.connect()

while True:
    print("current: "+str(readValue(8)))
    print("active power: "+str(readValue(18)))
    print("reactive power: "+str(readValue(26)))
    print("power factor: "+str(readValue(42)))
    print("frequency: "+str(readValue(54)))
    print("total active power: "+str(readValue(256)))
    print("total reactive power: "+str(readValue(1024)))
    print("-----------------------------------------------")
    time.sleep(1)
