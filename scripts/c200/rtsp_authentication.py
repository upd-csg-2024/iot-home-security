#! /usr/bin/python

# Original script from https://gist.github.com/crayfishapps/a13e2026ba872ec192695a95b851f4a0

# Modified the values for URI, the username and the password.
# We also fixed the encoding problems when running with Python 3.
# Digest auth in the original script is removed.

import socket,time,string,base64,hashlib,xml.etree.ElementTree as ET

m_Vars = {
    "bufLen" : 1024,
    "defaultServerIp" : "192.168.1.15",
    "defaultServerPort" : 554,
    "defaultTestUri" : "/stream1",
    "defaultUserAgent" : "RTSP Client",
    "defaultUsername" : "cs198csg",
    "defaultPassword" : "cs198csg"
}

def genmsg_DESCRIBE(url,seq,userAgent,authSeq):
    msgRet = "DESCRIBE " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "Authorization: " + authSeq + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Accept: application/sdp\r\n"
    msgRet += "\r\n"
    return msgRet
    
def genmsg_SETUP(url,seq,userAgent,authSeq = "", sessionID = ""):
    msgRet = "SETUP " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    if authSeq != "":
        msgRet += "Authorization: " + authSeq + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Blocksize: 65535\r\n"
    msgRet += "Transport: RTP/AVP;unicast;client_port=57932-57933\r\n"
    if sessionID != "":
        msgRet += "Session: " + sessionID + "\r\n"
    msgRet += "\r\n"
    return msgRet

def genmsg_OPTIONS(url,seq,userAgent):
    msgRet = "OPTIONS " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "\r\n"
    return msgRet

def genmsg_PLAY(url,seq,userAgent,authSeq,sessionId):
    msgRet = "PLAY " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Session: " + sessionId + "\r\n"
    msgRet += "Range: npt=0.000-\r\n"
    msgRet += "\r\n"
    return msgRet

def genmsg_TEARDOWN(url,seq,userAgent,authSeq,sessionId):
    msgRet = "TEARDOWN " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "Session: " + sessionId + "\r\n"
    msgRet += "\r\n"
    return msgRet

def decodeControl(strContent):
    mapRetInf = {}
    messageStrings = strContent.split("\n")
    for element in messageStrings:
        a = element.find("rtsp")
        if a >= 0:
            mapRetInf = element[a:]
    return mapRetInf

def decodeSession(strContent):
    mapRetInf = ""
    messageStrings = strContent.split("\n")
    for element in messageStrings:
        if "Session" in element:
            a = element.find(":")
            b = element.find(";")
            mapRetInf = element[a+2:b]
    return mapRetInf    

def generateAuthString(username,password,realm,method,uri,nonce):
    mapRetInf = {}
    m1 = hashlib.md5(username + ":" + realm + ":" + password).hexdigest()
    m2 = hashlib.md5(method + ":" + uri).hexdigest()
    response = hashlib.md5(m1 + ":" + nonce + ":" + m2).hexdigest()

    mapRetInf = "Digest "
    mapRetInf += "username=\"" + m_Vars["defaultUsername"] + "\", "
    mapRetInf += "realm=\"" + realm + "\", "
    mapRetInf += "algorithm=\"MD5\", "
    mapRetInf += "nonce=\"" + nonce + "\", "    
    mapRetInf += "uri=\"" + uri + "\", "
    mapRetInf += "response=\"" + response + "\""
    return mapRetInf  

# RTSP Setup                                
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((m_Vars["defaultServerIp"],m_Vars["defaultServerPort"]))  
seq  = 1

url = "rtsp://" + m_Vars["defaultServerIp"] + m_Vars["defaultTestUri"]

# Basic Auth Encoding
authSeq = base64.b64encode((m_Vars["defaultUsername"] + ":" + m_Vars["defaultPassword"]).encode("ascii"))
authSeq = "Basic " + authSeq.decode("ascii")

# OPTIONS
print(genmsg_OPTIONS(url,seq,m_Vars["defaultUserAgent"]))
s.send(genmsg_OPTIONS(url,seq,m_Vars["defaultUserAgent"]).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1

# DESCRIBE WITH BASIC AUTH
print(genmsg_DESCRIBE(url,seq,m_Vars["defaultUserAgent"], authSeq))
s.send(genmsg_DESCRIBE(url,seq,m_Vars["defaultUserAgent"], authSeq).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1

# SETUP WITH BASIC AUTH, GET SESSION ID
print(genmsg_SETUP(url + "/track1",seq,m_Vars["defaultUserAgent"], authSeq))
s.send(genmsg_SETUP(url + "/track1",seq,m_Vars["defaultUserAgent"], authSeq).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1

sessionID = decodeSession(msg1)

# SETUP WITH BASIC AUTH, USE SESSION ID
print(genmsg_SETUP(url + "/track2",seq,m_Vars["defaultUserAgent"], authSeq, sessionID))
s.send(genmsg_SETUP(url + "/track2",seq,m_Vars["defaultUserAgent"], authSeq, sessionID).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1

# PLAY WITH NO AUTH, USE SESSION ID
print(genmsg_PLAY(url,seq,m_Vars["defaultUserAgent"], authSeq, sessionID))
s.send(genmsg_PLAY(url,seq,m_Vars["defaultUserAgent"], authSeq, sessionID).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1

# TEARDOWN
print(genmsg_TEARDOWN(url,seq,m_Vars["defaultUserAgent"], authSeq, sessionID))
s.send(genmsg_TEARDOWN(url,seq,m_Vars["defaultUserAgent"], authSeq, sessionID).encode())
msg1 = s.recv(m_Vars["bufLen"]).decode()
print(msg1)
seq = seq + 1
