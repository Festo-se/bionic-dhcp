#!/usr/bin/env python3

#############
# Adapted work of
# https://github.com/playma/simple_dhcp
##############

import socket
import sys
import time

MAX_BYTES = 1024

serverPort = 67
clientPort = 68

class DHCP_client(object):

    def client(self):
        print("DHCP client is starting...\n")
        dest = ('255.255.255.255', serverPort)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', clientPort))

        print("Send DHCP discovery.")
        discover_data = self.discover_get()
        s.sendto(discover_data, dest)        
        offer_data, address = s.recvfrom(MAX_BYTES)
        print("Receive DHCP offer.")
        #print(data)
        
        print("Send DHCP request.")
        request_data = self.request_get(offer_data)
        s.sendto(request_data, dest)        
        pack_data ,address = s.recvfrom(MAX_BYTES)
        print("Receive DHCP pack.\n")
        self.readout_relevant_data(pack_data)
        print (self.new_ip)

        while True:
            time.sleep(10)

    def readout_relevant_data(self, data):
        """
        Reads out the relvant data for the hdcp pack received
        """

        self.new_ip = [data[16], data[17], data[18], data[19]]       

    def discover_get(self):
        OP = bytes([0x01])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        YIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        SIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00]) 
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
        Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCPOptions1 = bytes([53 , 1 , 1])        
        DHCPOptions2 = bytes([55 , 4 , 1, 3, 15, 6])

        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2

        return package

    def request_get(self, data):
        OP = bytes([0x01])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        YIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        SIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00]) 
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
        Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCPOptions1 = bytes([53 , 1 , 3])
        DHCPOptions2 = bytes([50 , 4 , data[16], data[17], data[18], data[19]])        
        DHCPOptions3 = bytes([54 , 4 , 0x00, 0x00, 0x00, 0x00])
        DHCPOptions4 = bytes([55 , 4 , 1, 3, 15, 6])
	
        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2 +  DHCPOptions3 + DHCPOptions4

        return package

if __name__ == '__main__':
    dhcp_client = DHCP_client()
    dhcp_client.client()
