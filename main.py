import os
import discord
import paho.mqtt.client as mqtt

TOKEN = os.getenv("TOKEN")

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")

TOPIC_CMD = "maison/esp1/cmd"

# ---- MQTT CLIENT ----
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

# ---- DISCORD BOT ----
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot connecté :", client.user)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!on":
        mqtt_client.publish(TOPIC_CMD, "ON")
        await message.channel.send("LED allumée via MQTT !")

    if message.content == "!off":
        mqtt_client.publish(TOPIC_CMD, "OFF")
        await message.channel.send("LED éteinte via MQTT !")

client.run(TOKEN)
