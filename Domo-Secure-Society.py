#------------------------------ [IMPORT]------------------------------------


import network, time, urequests
from utelegram import Bot
from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
from time import sleep

TOKEN = '5432867794:AAFEpHFlSXImoc2SSBtyCCn-FvUyPQHzb64'

#--------------------------- [OBJETOS]---------------------------------------
ancho = 128
alto = 64


bot = Bot(TOKEN)
led = Pin (15, Pin.OUT, value = 0)      #Salida del LED 
PIR = Pin(4, Pin.IN)                    #Entrada del sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #Pantalla Oled
oled = SSD1306_I2C(ancho, alto, i2c)    #Ancho
servo = PWM(Pin(5), freq=50)



print(i2c.scan())  # Verificar si hay problemas en la conexion Oled


#----------------------[ CONECTAR WIFI ]---------------------------------------------------------#

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

def map(x):
        return int((x - 0) * (125- 25) / (180 - 0) + 25) # v1.19 -- duty(m) -- 0 y 1023  
    
def bip():        #Hace sonar un bip
    buzzer = PWM(Pin(23), freq=293) 
    buzzer.duty(100)
    sleep(1)
    
def bip_off():
    buzzer = PWM(Pin(23), freq=0)
    buzzer.duty(0)
    

def flash ():      #Encender led
    led.on ()
         
         
def imagen_Open ():  # Envia mensaje movimiento detectado
     oled.fill(0)
     oled.text("!!!!!_OJO_!!!!!", 0, 10)
     oled.text("Cerradurqa On", 0, 20)
     oled.show()
     
def imagen_Close ():  # Envia mensaje sin movimientos
     oled.fill(0)
     oled.text("####_CALMA_####", 0, 10)
     oled.text("Cerradurqa Off", 0, 20)
     oled.show()

#------------------------------------[BOT]---------------------------------------------------------------------#

if conectaWifi ("E2G", "L322A32*"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    print("ok")
    
    @bot.add_message_handler("Inicio")
    def help(update):
        update.reply('''¡Sistema Inteligente se seguridad!   \U0001F92B \U0001F92B
                     \n Menu Principal
                     \n Elije una opción:
                     
                     \n------Cerradura-------
                     
                     Open : 1  \U0001F60E
                     Close: 2  \U0001F9D0
                     
                     \n----- Alarma ---------
                     
                     Activar : 3 \U0001F60F
                     Desactivar : 4  \U0001FAE3
                     
                     \n Tu seguridad a la mano''')
    
    @bot.add_message_handler("1")
    def help(update):
         m = map(180)
         servo.duty(m)
         imagen_Open()
         update.reply("Open the Door")
                     
        
    @bot.add_message_handler("2")
    def help(update):
         m = map(1)
         servo.duty(m)
         imagen_Close()
         update.reply("Close the Door")
        
    @bot.add_message_handler("3")
    def help(update):
        Contador = 1
        while Contador < 3:
            estado = PIR.value()
            sleep(0.05)
            if PIR.value()==1:  #Se activa la salida del sensor?
                print("Movimiento:",Contador)
                update.reply("Movimiento detectado: " + str(Contador))
                Contador += 1 
                imagen_Open()
                flash ()
                bip()
                sleep(1)
            else:
                bip_off()
                led.off ()
                imagen_Close()
                
        bip_off()
        led.off ()
        imagen_Close()
        
    @bot.add_message_handler("4")
    def help(update):
        
            update.reply("Apagando")
    
        
            
    bot.start_loop()
    
      

else:
       print ("Imposible conectar")
       miRed.active (False)