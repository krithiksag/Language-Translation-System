import urequests as requests
import ujson
from time import sleep
import utime
import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import network

# Replace with your Wi-Fi network credentials
SSID = "Pranay"
PASSWORD = "11111111"

# Initialize and connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for the Wi-Fi connection
while not wlan.isconnected():
    pass

# Print the IP address when connected
print("Connected to Wi-Fi")
led_pin = machine.Pin("LED", machine.Pin.OUT)
led_pin.value(1)  # Turn on the LED
print("IP Address:", wlan.ifconfig()[0])
# Define your Telegram Bot API token
bot_token = "5644155420:AAGczZBhAWTJiMoDhLToKJunBKdXx03hem8"

# Define a translation dictionary
translation_dict = {
    "hello": "Bonjour",
    "goodbye": "Au revoir",
    "cat": "chat",
    "dog": "chien",
    "family": "famille",
    "home": "maison",
    "work": "travail",
    "school": "école",
    "book": "livre",
    "car": "voiture",
    "bus": "autobus",
    "money": "argent",
    "time": "temps",
    "day": "jour",
    "night": "nuit",
    "sun": "soleil",
    "moon": "lune",
    "star": "étoile",
    "tree": "arbre",
    "flower": "fleur",
    "bird": "oiseau",
    "fish": "poisson",
    "house": "maison",
    "street": "rue",
    "city": "ville",
    "country": "pays",
    "please": "s'il vous plaît",
    "excuse me": "excusez-moi",
    "yes": "oui",
    "no": "non",
    "help": "aide",
    "question": "question",
    "answer": "réponse",
    "problem": "problème",
    "information": "information",
    "name": "nom",
    "age": "âge",
    "color": "couleur",
    "red": "rouge",
    "blue": "bleu",
    "green": "vert",
    "yellow": "jaune",
    "black": "noir",
    "white": "blanc",
    "good": "bon",
    "bad": "mauvais",
    "sad": "triste",
    "eat": "manger",
    "drink": "boire",
    "sleep": "dormir",
    "walk": "marcher",
    "run": "courir",
    "swim": "nager",
    "read": "lire",
    "write": "écrire",
    "listen": "écouter",
    "speak": "parler",
    "understand": "comprendre",
    "love": "aimer",
    "hate": "détester",
    "buy": "acheter",
    "sell": "vendre",
    "open": "ouvrir",
    "close": "fermer",
    "enter": "entrer",
    "exit": "sortir",
    "stop": "arrêter",
    "go": "aller",
    "come": "venir",
    "wait": "attendre"
}

# Function to send a message to the Telegram bot
def send_message(chat_id, message):
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(send_url, json=data)
    print("Message sent")
    response.close()

# Function to handle updates from the Telegram bot
def handle_updates():
    offset = 0  # Initialize the offset to 0
    while True:
        try:
            request_url = f'https://api.telegram.org/bot{bot_token}/getUpdates?offset={offset}'
            response = requests.get(request_url)
            if response.status_code == 200:
                data = ujson.loads(response.text)
                if 'result' in data and data['result']:
                    for update in data['result']:
                        chat_id = update['message']['chat']['id']
                        text = update['message']['text']
                        
                        # Translate the message if it's in the dictionary, or use the original message
                        translated_text = translation_dict.get(text.lower(), text)
                        
                        # Send the translated message back to the user
                        send_message(chat_id, translated_text)
                        I2C_ADDR     = 0x27
                        I2C_NUM_ROWS = 4
                        I2C_NUM_COLS = 20
                        i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
                        lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

                        def greeting():
                            
                            lcd.clear()
                            lcd.move_to(0,0)
                            lcd.putstr("tralated word:-")
                            lcd.move_to(0,1)
                            lcd.putstr(translated_word)
                            utime.sleep(5)
                            lcd.clear()

                        translated_word=translated_text

                        greeting()  
                        
                        # Update the offset to avoid processing the same message again
                        offset = update['update_id'] + 1
            response.close()
        except Exception as e:
            print("Error:", str(e))
        sleep(2)

# Start handling updates
handle_updates()