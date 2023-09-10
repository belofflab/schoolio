from math import floor
from random import random

def generate():
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[floor(random() * length)]
 
    return OTP