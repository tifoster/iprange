from ipaddress import *


def ip_rangify(ip_list):
    """ Takes a list of IP's and returns a list of contiguous ranges """
    input_ips = []
    for ip in ip_list:
        input_ips.append(ip_address(ip))
    input_ips.sort()

    if not input_ips:
        return []

    sequences = [[input_ips[0], input_ips[0]]]
    for ip in input_ips[1:]:
        if ip - 1 != sequences[-1][-1]:
            sequences.append([ip, ip])
        sequences[-1][-1] = ip

    ranges = []
    for sequence in sequences:
        ranges.append(IPRange(sequence[0], end=sequence[-1]))
    return ranges


class IPRange(object):
    def __init__(self, start, count=0, end=None):
        if isinstance(start, (IPv4Address, IPv6Address)):
            self.start = start
        else:
            raise TypeError('Starting address: "{}" must be a valid IP (v4 or v6) address.'.format(str(start)))

        if end is None:
            if not isinstance(count, int):
                raise TypeError('Count: "{}" must be an integer >0.'.format(count))
            elif count == 0:
                count = 1
            count += 1 if count < 0 else -1  # correction for cardinal numbers
            try:
                end = start + count
            except AddressValueError as e:
                raise AddressValueError('Count: {} is too large, exceeding the acceptable address space for IPv{}.'.format(count, start.version))
        elif not isinstance(end, (IPv4Address, IPv6Address)):
            raise TypeError('Ending address: "{}" must be a valid IP (v4 or v6) address.'.format(end))

        self.end = end

        if self.end < self.start:  # swap start and end if user reversed them or gave negative count
            temp = self.end
            self.end = self.start
            self.start = temp

        for p in range(4):
            if str(start).split('.')[p] == str(end).split('.')[p]:
                self.prefix = p + 1
            else:
                break

    def __repr__(self):
        return 'IPRange({!r}, end={!r})'.format(self.start, self.end)
        # return str(self) #.encode('utf-8')

    def __str__(self):
        output_string = ''
        start_string = str(self.start)
        end_string = str(self.end)
        if self.prefix == 4:
            return start_string
        for i in range(self.prefix):
            output_string += start_string.split('.')[i] + '.'
        output_string = output_string[:-1] + '.[{}'.format('.'.join(start_string.split('.')[self.prefix:]))
        output_string += '-{}]'.format('.'.join(end_string.split('.')[self.prefix:]))
        return output_string

    def start_to_end(self):
        if repr(self.start) != repr(self.end):
            return '{}-{}'.format(str(self.start), str(self.end))
        else:
            return str(self.start)

    def __unicode__(self):
        str(self).encode(encoding='UTF-8')
