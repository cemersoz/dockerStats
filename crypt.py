''' we _should_ encrypt the message with the servers public key before sending it
    here we use the servers public key to encode the message
    @param message: message to be encrypted with the servers public key
    @return: encrypted message
'''
def encode_for_server(message):
  return message

''' the server _should_ use our public key to encrypt its response, here we use our
    private key to decode this message
    @param message: message encrypted with our public key
    @return: decrypted message
'''
def decode_from_server(message):
  return message
