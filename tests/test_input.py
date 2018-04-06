from ipaddress import IPv4Address, AddressValueError
from ipaddressrange import ip_rangify, IpRange
import pytest


class Test_ip_rangify(object):
    happy_pairs = (
        (
            ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
            "[IpRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4'))]"
        ),
        (
            [IPv4Address('192.168.2.1'), IPv4Address('192.168.2.2'), IPv4Address('192.168.2.3'), IPv4Address('192.168.2.4')],
            "[IpRange(IPv4Address('192.168.2.1'), end=IPv4Address('192.168.2.4'))]"
        ),
        (
            ['192.168.3.1', IPv4Address('192.168.3.2'), '192.168.3.3', '192.168.3.4'],
            "[IpRange(IPv4Address('192.168.3.1'), end=IPv4Address('192.168.3.4'))]"
        )
        # TODO cases of split ranges, ranges across human readable boundaries, big and small?
        # TODO test ranges including invalid IP's and catch exceptions
        # TODO above three cases for IPv6
    )

    def test_happyPath(self):
        for arg, range_repr in self.happy_pairs:
            result = repr(ip_rangify(arg))
            assert range_repr == result


class Test_IpRange(object):
    happy_triples = (
        (
            IpRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4')),
            "IpRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4'))",
            '192.168.1.[1-4]'
        ),
        (
            IpRange(IPv4Address('192.168.2.1'), count=4),
            "IpRange(IPv4Address('192.168.2.1'), end=IPv4Address('192.168.2.4'))",
            '192.168.2.[1-4]'
        ),
        (
            IpRange(IPv4Address('192.168.3.1'), end=IPv4Address('192.168.3.4'), count=3),
            "IpRange(IPv4Address('192.168.3.1'), end=IPv4Address('192.168.3.4'))",
            '192.168.3.[1-4]'
        )
        # TODO above three cases for IPv6
    )

    def test_create_listOfStrings(self):
        for arg, range_repr, range_str in self.happy_triples:
            print(repr(arg))
            assert repr(arg) == range_repr
            assert str(arg) == range_str

    def test_create_rangeOfOne(self):
        assert repr(IpRange(IPv4Address('192.168.1.1'), count=0)) == "IpRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.1'))"
        assert str(IpRange(IPv4Address('192.168.1.1'), count=0)) == '192.168.1.1'
        assert repr(IpRange(IPv4Address('192.168.2.1'), count=1)) == "IpRange(IPv4Address('192.168.2.1'), end=IPv4Address('192.168.2.1'))"
        assert str(IpRange(IPv4Address('192.168.1.1'), count=1)) == '192.168.1.1'

    def test_create_rangeCrossingOctet(self):
        assert repr(IpRange(IPv4Address('192.168.0.250'), count=10)) == "IpRange(IPv4Address('192.168.0.250'), end=IPv4Address('192.168.1.3'))"
        assert str(IpRange(IPv4Address('192.168.0.250'), count=10)) == '192.168.[0.250-1.3]'

    def test_exceptions(self):
        with pytest.raises(TypeError) as e_info:
            IpRange('192.168.1.1', count=2)
        assert 'Starting address: "192.168.1.1" must be a valid IP (v4 or v6) address.' in str(e_info.value)
        with pytest.raises(TypeError) as e_info:
            IpRange(IPv4Address('192.168.1.1'), count='abc')
        assert 'Count: "abc" must be an integer >0.' in str(e_info.value)
        with pytest.raises(TypeError) as e_info:
            IpRange(IPv4Address('192.168.1.1'), end='192.168.1.3')
        assert 'Ending address: "192.168.1.3" must be a valid IP (v4 or v6) address.' in str(e_info.value)
        with pytest.raises(AddressValueError) as e_info:
            IpRange(IPv4Address('255.255.255.255'), count=1)
        assert 'Count: 1 is too large, exceeding the acceptable address space for IPv4' in str(e_info.value)

    # TODO test no range version of str() Not yet implemented
    # TODO test with negative count

# TODO remember to reenable flake8
