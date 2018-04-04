from ipaddress import IPv4Network


class IpAddressRange():
    inputIps = []

    def parseStringList(self,stringList):
        for ipString in stringList:
            try:
                self.inputIps.append(IPv4Network(ipString))
            except ex: #TODO I think I should catch bad type, or cannot parse exceptions or something
                raise ex
            self.inputIps.sort()

    def parseIpList(self,ipList):
        self.inputIps = ipList
        #TODO trust but verify
        #TODO this may fail to sort if there's more than one value in any of the first three octets, as values are mod(256)
        self.inputIps.sort()

    def getRangesByLastOctet(self):
        sequences = []
        lastIp = [None,None]
        for ip in self.inputIps:
            curIp = str(ip.network_address).rsplit(sep='.',maxsplit=1)
            if (len(lastIp) > 0) and (lastIp[0] == curIp[0]) and (lastIp[1] == str(int(curIp[1]) - 1)):
                lastIp = curIp
                sequences[-1].append(curIp[1])
            else: #TODO consider splitting up the cases where the first three octets are the same vs. different
                lastIp = curIp
                sequences.append(curIp)
                next
        #TODO this is actually only sequences, now we need to condense them
        ranges = []
        for sequence in sequences:
            ranges.append([sequence[0],sequence[1],sequence[-1]])

        return ranges

    def getRanges(self):
        sequences = []
        lastIp = None
        for ip in self.inputIps:
            if (lastIp is not None) and (lastIp.network_address == (ip.network_address - 1)):
                lastIp = ip
                sequences[-1].append(str(ip.network_address))
            else:
                lastIp = ip
                sequences.append([str(ip.network_address)])
                next

        ranges = []
        for sequence in sequences:
            ranges.append([sequence[0],sequence[-1]])

        return ranges

    def printIpRangesByLastOctet(self):
        pass

    def printIpRanges(self):
        pass
