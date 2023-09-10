import hashlib
from Crypto.Cipher import AES
from base64 import urlsafe_b64encode, urlsafe_b64decode

from django.http import Http404

from .models import LastMessage, Room, RoomSession, LastSeenMessage


# urlsafe_b64encode encryption
from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class AESRoomEnc(object):
    iv = 'a2xhcgAAAAAAAAAA'
    front_key = b'Zx*}kn@bf>(sX8Ep'
    back_key = b'TrVMD/+_mG(j76,8'
    def __init__(self, key): 
        self.bs = 16
        cryption_key = "%^&+@=$-%#-#@"+ key +"+^&_-!@#&^&="
        self.key = hashlib.md5(cryption_key.encode()).digest().hex().upper()
    def encrypt(self, raw):
        #append strings to both end
        plain_text = self.front_key + raw + self.back_key
        plain_text = self._pad(plain_text.decode('utf-8'))

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypt = urlsafe_b64encode(cipher.encrypt(plain_text))
        return encrypt

    def decrypt(self, enc):
        # Try catch added for throwing incorrect padding exception
        try:
            enc = urlsafe_b64decode(enc)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypt = self._unpad(cipher.decrypt(enc)).decode('utf-8')
            decoded_front_key = decrypt[:16]
            decoded_back_key = decrypt[-16:]
            # check these string matches our key, if matches remove these strings from the decoded string
            if decoded_front_key == self.front_key and decoded_back_key == self.back_key:
                # remove first 16 char
                decrypt =  decrypt[16:]
                # remove end 16 char
                decrypt =  decrypt[:-16]
            return decrypt
        except Exception as e:
            pp(e)
            return ""
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):        
        return s[:-ord(s[len(s)-1:])]



# -------------------------------------------#
#               Room Functions               #
# -------------------------------------------#

def exist_user_in_room(user,room):
    if Room.objects.filter(participants=user.id,name=room).exists():
        return True
    else:
        return False

def exist_user_in_roomId(user,room):
    if Room.objects.filter(participants=user.id,id=room).exists():
        return True
    else:
        return Http404

def set_room_session(user,room):
    obj, created = RoomSession.objects.get_or_create( user_id=user.id,
    defaults={'room_id': room})
    return True
    
def exist_room(room):
    if Room.objects.filter(name=room).exists():
        return True
    else:
        return False
    
def update_room_last_message(messageId, room):
    lastMsg,created = LastMessage.objects.get_or_create(room_id=room)
    if lastMsg:
        lastMsg.message = messageId
        lastMsg.save()

def update_last_seen_message(user,room):
    lastViewedMessage,created = LastSeenMessage.objects.get_or_create(room_id=room,user_id=user.id)
    lastMsgId = LastMessage.objects.filter(room_id=room).last()
    if lastViewedMessage and lastMsgId:
        lastViewedMessage.message = lastMsgId.message
        lastViewedMessage.save()