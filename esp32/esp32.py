from machine import Pin, ADC,Timer,PWM
import time
import dht
import machine
from time import sleep_ms
import network
import urequests  
import json

serverip = 'http://192.168.123.2:8000'# 学校地址
url = '/blog/upload'#房间号
postUrl = serverip + url
alertUrl = serverip + '/blog/alarm'
headers = {'Content-Type': 'application/json'}

temperature = 20.0
humidity = 30.0
MQ2_con = 0
SoilWet = 0.0
detected = 'no'
Light = 0
Sensor = 0
fireSensor = 'yes'
TempThreshold = 28

# 红外检测  
p15 = Pin(4,Pin.IN)  
# 初始化和设置  
# p15.init()   
def RedSensor():
    global detected
    if p15.value():  # 如果检测到人
        time.sleep(0.1)
        if p15.value():
                detected = 'yes'
                print('有人')
                data = {'alert':'something closing', 'value':'something closing'}
                json_data = json.dumps(data) 
                print(json_data)
                response = urequests.post(alertUrl, data=json_data, headers=headers) 
                print(response.text)
                buzzerWork()
    else:  # 如果未检测到人
        detected = 'no'
        print('没人')


# 烟雾传感器
MQ2_PIN_ADC = 32
MQ2_PIN_DIGITAL = 35

adc_MQ2 = ADC(Pin(MQ2_PIN_ADC))
adc_MQ2.atten(ADC.ATTN_11DB)


MQ2_state = 0

PIN_MQ2 = Pin(MQ2_PIN_DIGITAL, Pin.IN)

def MQ2_read():
    global MQ2_state,MQ2_con
    MQ2_ADC_value = adc_MQ2.read_uv()
    MQ2_state = PIN_MQ2.value()
    MQ2_con = (MQ2_ADC_value / 3300000) * 100

# 土壤湿度

def SoilSensor():
    global SoilWet
    ps2_y = ADC(Pin(33))
    ps2_y.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
    # 数字量
    p15 = Pin(25, Pin.IN)
    val_y = ps2_y.read()  # 0-4095
    light = p15.value()
    SoilWet = 100 - (val_y/4095)*100
    if SoilWet == 0.0:
        pass
    else:
        pass

# 光敏传感器
def LightSensor():
    global Light
    ps2_y = ADC(Pin(34))
    ps2_y.atten(ADC.ATTN_11DB)
    global Light
    val_y = ps2_y.read()  # 0-4095
    Light = (4095 - val_y)/4095 * 100
    print(Light)
    

    
fire = Pin(13,Pin.IN)
def FireSensor():
    global fireSensor,Sensor
    Sensor = fire.value() 
    if Sensor == 1:
        fireSensor = 'no'
    else:
        fireSensor = 'yes'

# 蜂鸣器
class BUZZER:
    def __init__(self, sig_pin):
        self.pwm = PWM(Pin(sig_pin, Pin.OUT))

    def play(self, melodies, wait, duty):
        for note in melodies:
            print("note:{}".format(note))
            if note:
                self.pwm.freq(note)
            self.pwm.duty(duty)
            sleep_ms(wait)
        # 暂停PWM，将占空比设置为0
        self.pwm.duty(0)
E7 = 0
mario = [
    E7,E7,E7
]
buzzer = BUZZER(26)
def buzzerWork():
    buzzer.play(mario, 200, 512)
    sleep_ms(100)
    buzzer.play(mario, 200, 512)
    sleep_ms(100)
    buzzer.play(mario, 200, 512)
    
def buzzerStop():
    buzzer.pwm.duty(0)
    

# 温湿度

dht27 = dht.DHT11(Pin(27))
def TemHumSensor():
    global temperature,humidity
    dht27.measure()
    temperature = dht27.temperature()
    humidity = dht27.humidity()
    print("Temperature: %.2f C" % temperature)  
    print("Humidity: %.2f %%" % humidity)
    
tim_dht11 = Timer(1)
tim_dht11.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: TemHumSensor())

def upload():
    data = {'Temperature':temperature, 'Humidity':humidity,'MQ':MQ2_con,'WaterRate':SoilWet,'detected':detected,'Illumination':Light,'fire':fireSensor}
    json_data = json.dumps(data) 
    print(json_data)
    response = urequests.post(postUrl, data=json_data, headers=headers) 
    # 打印服务器的响应  
    print(response.text)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'password')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())
    
    
def alert(info):
    data = {'alert':temperature, 'value':humidity}
    json_data = json.dumps(data) 
    print(json_data)
    #response = urequests.post(postUrl, data=json_data, headers=headers) 
    # 打印服务器的响应  
    #print(response.text)


    
do_connect()
buzzerStop()
while True:
    LightSensor()
    FireSensor()
    SoilSensor()
    RedSensor()
    MQ2_read()
    upload()
    
    print(Sensor)
    if temperature >= TempThreshold or MQ2_con >= 40 or Sensor == 0 :
        if temperature >= TempThreshold:
            data = {'alert':'temperature warning', 'value':humidity}
            json_data = json.dumps(data) 
            print(json_data)
            response = urequests.post(alertUrl, data=json_data, headers=headers) 
            # 打印服务器的响应  
            print(response.text)
            buzzerWork()
            print('temperature报警')
        if MQ2_con >= 40:
            data = {'alert':'MQ2_con warning', 'value':MQ2_con}
            json_data = json.dumps(data) 
            print(json_data)
            response = urequests.post(alertUrl, data=json_data, headers=headers) 
            # 打印服务器的响应  
            print(response.text)
            buzzerWork()
            print('MQ2_con报警')
        if Sensor != 1:
            data = {'alert':'fire warning', 'value':'fire'}
            json_data = json.dumps(data) 
            print(json_data)
            response = urequests.post(alertUrl, data=json_data, headers=headers) 
            # 打印服务器的响应  
            print(response.text)
            buzzerWork()
            print('fire')
            time.sleep(1)
    else:
        pass
    Sensor = 0
    
    time.sleep(1)






