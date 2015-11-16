#!/usr/bin/python

import subprocess
import time

print('ps aux|grep bluetooth')
ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE,)
grep = subprocess.Popen(['grep', 'bluetooth'], stdin=ps.stdout, stdout=subprocess.PIPE,)
end_of_pipe = grep.stdout

moji_2 = []
result = []
detect = 0
for line in end_of_pipe:
    if line.find('bluetoothd') != -1:
        moji_2 = line.split(' ')
        detect=1

val2 = 0
if detect == 1:
    for val in range(0,len(moji_2)):
        if moji_2[val-val2] == "":
            moji_2.pop(val-val2)
            val2=val2+1
    print('kill '+moji_2[1])
    kill = subprocess.Popen(['kill',moji_2[1]], stdout=subprocess.PIPE,)
    end_of_pipe = kill.stdout
    detect = 0

time.sleep(1.0)
print('bluetoothd -nE')
bluetoothd = subprocess.Popen(['bluetoothd','-nE'], stdout=subprocess.PIPE,)
end_of_pipe = bluetoothd.stdout
time.sleep(1.0)

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
import gobject

from random import randint

import rospy
from std_msgs.msg import String

rospy.init_node('bleNode', anonymous=True)
pub = rospy.Publisher('BleToControl', String, queue_size = 10)

mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'

class InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'

class NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'

class NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'

class InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'

class FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'


class Service(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/service'

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_SERVICE_IFACE: {
                        'UUID': self.uuid,
                        'Primary': self.primary,
                        'Characteristics': dbus.Array(
                                self.get_characteristic_paths(),
                                signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        result = []
        for chrc in self.characteristics:
            result.append(chrc.get_path())
        return result

    def get_characteristics(self):
        return self.characteristics

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_SERVICE_IFACE:
            raise InvalidArgsException()

        return self.get_properties[GATT_SERVICE_IFACE]

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        response[self.get_path()] = self.get_properties()
        chrcs = self.get_characteristics()
        for chrc in chrcs:
            response[chrc.get_path()] = chrc.get_properties()
            descs = chrc.get_descriptors()
            for desc in descs:
                response[desc.get_path()] = desc.get_properties()

        return response


class Characteristic(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + '/char' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_CHRC_IFACE: {
                        'Service': self.service.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                        'Descriptors': dbus.Array(
                                self.get_descriptor_paths(),
                                signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_CHRC_IFACE:
            raise InvalidArgsException()

        return self.get_properties[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_CHRC_IFACE, out_signature='ay')
    def ReadValue(self):
        print('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE, in_signature='ay')
    def WriteValue(self, value):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StartNotify(self):
        print('Default StartNotify called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StopNotify(self):
        print('Default StopNotify called, returning error')
        raise NotSupportedException()

    @dbus.service.signal(DBUS_PROP_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass


class Descriptor(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = characteristic.path + '/desc' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_DESC_IFACE: {
                        'Characteristic': self.chrc.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_DESC_IFACE:
            raise InvalidArgsException()

        return self.get_properties[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_DESC_IFACE, out_signature='ay')
    def ReadValue(self):
        print ('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_DESC_IFACE, in_signature='ay')
    def WriteValue(self, value):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

class TestService(Service):
    """
    Dummy test service that provides characteristics and descriptors that
    exercise various API functionality.

    """
    TEST_SVC_UUID = 'E1F40469-CFE1-43C1-838D-DDBC9DAFDDE6'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.TEST_SVC_UUID, True)
        self.add_characteristic(TestCharacteristic(bus, 0, self))

class TestCharacteristic(Characteristic):
    """
    Dummy test characteristic. Allows writing arbitrary bytes to its value, and
    contains "extended properties", as well as a test descriptor.

    """
    TEST_CHRC_UUID = 'F90E9CFE-7E05-44A5-9D75-F13644D6F645'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.TEST_CHRC_UUID,
                ['read', 'write', 'writable-auxiliaries'],
                service)
        self.value = []
        self.add_descriptor(
                CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self):
        print('TestCharacteristic Read: ' + repr(self.value))
        print('TestCharacteristic Read value: ' + str(self.value))
        return self.value

    def WriteValue(self, value):
        #print('TestCharacteristic Write: ' + repr(value))
        #print('TestCharacteristic Write value: ' + str(value))
        self.value = value
        s = "".join(chr(b) for b in value)
        print s
        if ('#' in s or '$' in s or '<' in s or '>' in s):
            LEDon = String()
            LEDon.data = "gpio,w,act"
            send(LEDon)

        message = String()
        message.data = "serial,w," + s
        send(message)

class TestDescriptor(Descriptor):
    """
    Dummy test descriptor. Returns a static value.

    """
    TEST_DESC_UUID = '12345678-1234-5678-1234-56789abcdef2'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
                self, bus, index,
                self.TEST_DESC_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self):
        return [
                dbus.Byte('T'), dbus.Byte('e'), dbus.Byte('s'), dbus.Byte('t')
        ]


class CharacteristicUserDescriptionDescriptor(Descriptor):
    """
    Writable CUD descriptor.

    """
    CUD_UUID = '2901'

    def __init__(self, bus, index, characteristic):
        self.writable = 'writable-auxiliaries' in characteristic.flags
        self.value = array.array('B', 'TX Data')
        self.value = self.value.tolist()
        Descriptor.__init__(
                self, bus, index,
                self.CUD_UUID,
                ['read', 'write'],
                characteristic)

    def ReadValue(self):
        return self.value

    def WriteValue(self, value):
        if not self.writable:
            raise NotPermittedException()
        self.value = value

def property_changed(interface, changed, invalidated, path):
    iface = interface[interface.rfind(".") + 1:]
    for name, value in changed.iteritems():
        val = str(value)
        if name == 'Connected':
            if val == '1':
                print('PLEN_LED_ON')
                message = String()
                message.data = "gpio,w,on"
                send(message)
            elif val == '0':
                print('PLEN_LED_OFF')
                message = String()
                message.data = "gpio,w,off"
                send(message)
                advertise()
            else:
                pass
        else:
            pass

def register_service_cb():
    print('GATT service registered')


def register_service_error_cb(error):
    print('Failed to register service: ' + str(error))
    mainloop.quit()


def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.iteritems():
        if props.has_key(GATT_MANAGER_IFACE):
            return o

    return None

def send(message):
    rospy.loginfo("controlNode %s", message.data)
    global pub
    #pub = rospy.Publisher('BleToControl', String, queue_size = 10)
    pub.publish(message)

def advertise():
    print('hciconfig hci0 up')
    hci_on = subprocess.Popen(['hciconfig','hci0','up'], stdout=subprocess.PIPE,)
    end_of_pipe = hci_on.stdout
    time.sleep(1.0)
    print('hciconfig hci0 leadv')
    leadv = subprocess.Popen(['hciconfig','hci0','leadv','0'], stdout=subprocess.PIPE,)
    end_of_pipe = leadv.stdout
    pass

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

    bat_service = BatteryService(bus, 0)
    test_service = TestService(bus, 1)

    mainloop = gobject.MainLoop(is_running=True)

    bus.add_signal_receiver(property_changed, bus_name="org.bluez",
            dbus_interface="org.freedesktop.DBus.Properties",
            signal_name="PropertiesChanged",
            path_keyword="path")

    service_manager.RegisterService(test_service.get_path(), {},
                                    reply_handler=register_service_cb,
                                    error_handler=register_service_error_cb)
    advertise()
    while mainloop.is_running():
        try:
            mainloop.run()
        except:
            quit()

if __name__ == '__main__':
    #rospy.init_node('bleNode', anonymous=True)
    main()