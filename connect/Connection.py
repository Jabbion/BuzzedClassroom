"""
Contains every connection related functions
Used for sending/receiving packets

@author TheDoctor
@version 0.1
@date 8.7.17
"""

import socket

from connect.ConnectionConstant import ConnectionConstants


class Connection(object):

    sock = None
    conn = None
    def __init__(self):
        self.connect()

    def connect(self):
        if self.sock != None:
            self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(ConnectionConstants.server_address)

    def sendMessageByte(self, byte):
        byteArray = []
        byteArray.append(byte)
        self.sendMessage(byteArray)

    def sendMessage(self, data):
        i = 0
        while i < len(data):
            packet = bytearray()
            if i + ConnectionConstants.lenDataChunk < len(data):
                packet.append(ConnectionConstants.normalPacket)
            else:
                packet.append(ConnectionConstants.lastPacket)
            packet.extend(data[i:i + ConnectionConstants.lenDataChunk])

            self.sock.sendall(packet)

            i += ConnectionConstants.lenDataChunk

    def readMessage(self):
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        data = []
        rawData = self.conn.recv(ConnectionConstants.lenDataChunk + 1)
        print(rawData)
        while rawData[0] != ConnectionConstants.lastPacket:
            data.append(rawData[1:ConnectionConstants.lenDataChunk + 1])
            rawData = self.conn.recv(ConnectionConstants.lenDataChunk + 1)
        data.append(rawData[1:ConnectionConstants.lenDataChunk + 1])

        endData = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                endData.append(data[i][j])

        return endData
