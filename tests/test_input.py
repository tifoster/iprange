from ipaddress import IPv4Address, AddressValueError
from iprange import ip_rangify, IPRange
import pytest


class Test_ip_rangify(object):
    happy_pairs = (  # Tuples of the form: (constructor, repr(list of ranges))
        (  # String and IP inputs
            ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
            "[IPRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4'))]"
        ),
        (
            [IPv4Address('192.168.2.1'), IPv4Address('192.168.2.2'), IPv4Address('192.168.2.3'), IPv4Address('192.168.2.4')],
            "[IPRange(IPv4Address('192.168.2.1'), end=IPv4Address('192.168.2.4'))]"
        ),
        (
            ['192.168.3.1', IPv4Address('192.168.3.2'), '192.168.3.3', '192.168.3.4'],
            "[IPRange(IPv4Address('192.168.3.1'), end=IPv4Address('192.168.3.4'))]"
        ),
        # TODO above three cases for IPv6
        (  # several ranges
            ['192.168.4.1', '192.168.4.2', '192.168.5.3', '192.168.5.4'],
            "[IPRange(IPv4Address('192.168.4.1'), end=IPv4Address('192.168.4.2')), IPRange(IPv4Address('192.168.5.3'), end=IPv4Address('192.168.5.4'))]"
        ),
        (  # unsorted range
            [IPv4Address('192.168.6.3'), IPv4Address('192.168.6.2'), IPv4Address('192.168.6.1'), IPv4Address('192.168.6.4')],
            "[IPRange(IPv4Address('192.168.6.1'), end=IPv4Address('192.168.6.4'))]"
        ),
        (  # Across an octet
            [IPv4Address('192.168.7.255'), IPv4Address('192.168.8.0'), IPv4Address('192.168.8.1')],
            "[IPRange(IPv4Address('192.168.7.255'), end=IPv4Address('192.168.8.1'))]"
        )
    )

    def test_happy_path(self):
        for arg, range_repr in self.happy_pairs:
            assert range_repr == repr(ip_rangify(arg))

    def test_large_range(self):
        size = 4000
        r = []
        for i in range(size):
            r.append(IPv4Address('192.168.1.1') + i)
        assert "[IPRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.16.160'))]" == repr(ip_rangify(r))


class Test_IPRange(object):
    happy_triples = (  # Tuples of the form: (constructor,repr,str)
        (  # Basic cases
            IPRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4')),
            "IPRange(IPv4Address('192.168.1.1'), end=IPv4Address('192.168.1.4'))",
            '192.168.1.[1-4]',
            '192.168.1.1-192.168.1.4'
        ),
        (
            IPRange(IPv4Address('192.168.2.1'), count=4),
            "IPRange(IPv4Address('192.168.2.1'), end=IPv4Address('192.168.2.4'))",
            '192.168.2.[1-4]',
            '192.168.2.1-192.168.2.4'
        ),
        (  # Range of one
            IPRange(IPv4Address('192.168.3.1'), count=0),
            "IPRange(IPv4Address('192.168.3.1'), end=IPv4Address('192.168.3.1'))",
            '192.168.3.1',
            '192.168.3.1'
        ),
        (
            IPRange(IPv4Address('192.168.4.1'), count=1),
            "IPRange(IPv4Address('192.168.4.1'), end=IPv4Address('192.168.4.1'))",
            '192.168.4.1',
            '192.168.4.1'
        ),
        (  # Range crossing octet
            IPRange(IPv4Address('192.168.4.250'), count=10),
            "IPRange(IPv4Address('192.168.4.250'), end=IPv4Address('192.168.5.3'))",
            '192.168.[4.250-5.3]',
            '192.168.4.250-192.168.5.3'
        ),
        (  # Diminishing range
            IPRange(IPv4Address('192.168.6.3'), count=-3),
            "IPRange(IPv4Address('192.168.6.1'), end=IPv4Address('192.168.6.3'))",
            '192.168.6.[1-3]',
            '192.168.6.1-192.168.6.3'
        ),
        (
            IPRange(IPv4Address('192.168.7.3'), end=IPv4Address('192.168.7.1')),
            "IPRange(IPv4Address('192.168.7.1'), end=IPv4Address('192.168.7.3'))",
            '192.168.7.[1-3]',
            '192.168.7.1-192.168.7.3'
        )
        # TODO above cases for IPv6
    )

    def test_happy_path(self):
        for arg, range_repr, range_str, range_start_end in self.happy_triples:
            assert repr(arg) == range_repr
            assert str(arg) == range_str
            assert arg.start_to_end() == range_start_end

    def test_exceptions(self):
        with pytest.raises(TypeError) as e_info:
            IPRange('192.168.1.1', count=2)
        assert 'Starting address: "192.168.1.1" must be a valid IP (v4 or v6) address.' in str(e_info.value)
        with pytest.raises(TypeError) as e_info:
            IPRange(IPv4Address('192.168.1.1'), count='abc')
        assert 'Count: "abc" must be an integer >0.' in str(e_info.value)
        with pytest.raises(TypeError) as e_info:
            IPRange(IPv4Address('192.168.1.1'), end='192.168.1.3')
        assert 'Ending address: "192.168.1.3" must be a valid IP (v4 or v6) address.' in str(e_info.value)
        with pytest.raises(AddressValueError) as e_info:
            IPRange(IPv4Address('255.255.255.255'), count=2)
        assert 'Count: 1 is too large, exceeding the acceptable address space for IPv4' in str(e_info.value)
