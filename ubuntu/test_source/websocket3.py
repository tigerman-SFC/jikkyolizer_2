from websocket import create_connection  
ws = create_connection("http://challenge-server.code-check.io/")  
print ("Sending 'Hello, World'...")
ws.send("Hello, World")  
print ("Sent")  
print ("Reeiving...")  
result =  ws.recv()  
print ("Received '%s'" % result)  
ws.close()  

