import random
import socket
import netifaces as ni
import time
import subprocess
import re
from ipaddress import ip_address
from logger import logger


class NetworkData():
    
    def get_private_ip(self):
        """
        Function to get the device's private IP.

        Return:
            String containing the streaming IP.
        """
        start_time = time.time()
        ip = self._parse_ip()       
        return ip
    
    def _get_network_interfaces_data(self):
        """
        Private function to get network data. Loopback address not included!
            
        Returns:
            Dictionary containing the interface as a key and the IP as value
        """
        ip_interfaces = ni.interfaces()
        interf_dict = {}
        
        for interface in ip_interfaces:
            interface_ip_address = ""

            if ni.AF_INET in ni.ifaddresses(interface):
                interface_ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            interf_dict[interface]= interface_ip_address
        
        return interf_dict


    def _parse_ip(self):
        """
        Private function to parse ip from the dictionary returned by _get_network_interfaces_data().

            Returns:
                a random IP from a random interface 'eth0' or 'wlan0' if exists or None
        """

        network_dict = self._get_network_interfaces_data()
        interface = ""
        network_dict = self._check_streamable_ips(network_dict)
        logger.info(f"Found the following IPs for the server: {network_dict.values()}")
    
        if network_dict:
            interface = random.choice(list(network_dict))
            ip = network_dict[interface]
            logger.info(f"The IP selected for stream is: \'{ip}\'. The inferface is: {interface}")
            return network_dict[interface]
        else:
            return
    
    
    def _check_streamable_ips(self, original_network_dict):
        """
        Function that verifies to select an interface for streaming
        
        Returns:
            dictionary with interfaces to use for streaming
        """
        network_dict = original_network_dict.copy()
        
        logger.info("Removing loopback interface.") 
        network_dict.pop('lo')  # use for test only
        logger.info(f"Checking for private IPs")

        for interf, ip_addr in original_network_dict.items():
            try:
                streamable = ip_address(ip_addr).is_private
            except ValueError:
                logger.error(f"Removing interface \'{interf}\' with ip addr: \'{interf}\'")
                network_dict.pop(interf)

        network_dict
        if not network_dict:
            raise ValueError("Failed to find private IPs for the test! {original_network_dict}")

        return network_dict
