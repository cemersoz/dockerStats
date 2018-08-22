import time
import logging

logger = logging.getLogger(__name__)

class Device(object):

  def __init__(self, privateKeyLocation='~/.ssh/id_rsa',
                     publicKeyLocation='~/.ssh/id_rsa.pub',
                     serverPublicKeyLocation='~/.ssh/server_rsa.pub'):

    fPriv = open(privateKeyLocation, 'r')
    fPub = open(publicKeyLocation, 'r')
    sPub = open(serverPublicKeyLocation, 'r')

    self.privateKey = fPriv.read()
    self.publicKey = fPub.read()
    self.serverPublicKey = sPub.read()

    fPriv.close()
    fPub.close()
    sPub.close()
    
  ''' Here we get the ID of this device, this should obviously be overwritten
      in your specific implementation
  '''

  def getID(self):
    return 0

  def privateKeyEncrypt(self, message):
    #TODO: actually encrypt the message
    return message

  ''' Here we get the message (stats) and encrypt it using our private key.
      We then add our device_id in plaintext and the timestamp. 

      NOTE: we're trying to verify the message authenticity and *not* make
            the message hard to decode. Hence the private key.

      Once it receives the message the server will decrypt the message using 
      our public key (verifying our authenticity) and log this message

      @param message: message to be encrypted with our private key
      @return: encrypted message and metadata
  '''
  def encodeAsDevice(self, message):
    encrypted_message = self.privateKeyEncrypt(message)
    return {'device_id': self.getId(),
            'timestamp': time.time(),
            'message': encrypted_message}

  ''' Here we get a message that we assume has been encrypted with our public key
      to prevent other entities to decode the message and decode it with our private key.

      NOTE: Here we are trying to ensure only we can see the message and *not* that the
            origin is a trusted source

      @param message: encrypted message
      @return: decrypted message
  '''
  def decodeAsDevice(self, message):
    #TODO: actually decrypt the message
    return message

  ''' Here we get a message that we assume is enctypted with the trusted server's private key
      to verify the authenticity of the message and we decode it with our private key
 
      NOTE: Here we are trying to ensure the authenticity of the sender and *not* that other
            persons cannot read our message

      @param message: encrypted message
      @return: decrypted message
  '''
  def decodeFromServer(self, message):
    #TODO: actually decrypt the message
    return message

  ''' This function assumes that the message has been ecrypted once with our public key
      to ensure only we can see it and then with the server's private key to ensure
      origin authenticity.

      NOTE: Here we are trying to verify the message originated from our trusted server
            *and* we're trying to make it impossible for entities other than us to
            decode the message
      
      @param message: encrypted message
      @return: decrypted message
  '''
  def decodeAsDeviceFromServer(message):
    half_decrypted = self.decodeFromServer(message) #decoded by server public key
    if half_decrypted is None: return None

    return decodeAsDevice(half_decrypted) #decoded as our private key
