from ipaddress import *


def ip_rangify(ip_list):
    """ Takes a list of IP's and returns a list of contiguous ranges """
    input_ips = []
    for ip in ip_list:
        input_ips.append(ip_address(ip))
    input_ips.sort()

    sequences = []
    last_ip = None
    for ip in input_ips:
        if (last_ip is not None) and (last_ip == (ip - 1)):
            last_ip = ip
            sequences[-1].append(ip)
        else:
            last_ip = ip
            sequences.append([ip])
            next

    ranges = []
    for sequence in sequences:
        ranges.append(IpRange(sequence[0], end=sequence[-1]))
    return ranges


class IpRange(object):
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
        return 'IpRange({!r}, end={!r})'.format(self.start, self.end)
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
