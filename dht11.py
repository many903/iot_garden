from cmath import asin
from time import sleep
from dhtxx import DHT11
dht11= DHT11(18)
while True:
    r=dht11.get(max_tries=10)
    if r:
        print(r)
    else:
        print("failed")
    sleep()