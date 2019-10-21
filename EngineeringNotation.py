"""
EngineeringNotation.py

Provides function to convert to engineering notation (similar to schetific notation).
Uses the 'decimal' library.

"""


def to_string(num_arg: float, precision_arg: int = 3) -> str:
    import decimal
    decimal.getcontext().prec = precision_arg
    return decimal.Decimal(num_arg).normalize().to_eng_string()


# Test function for to_eng_string()
if __name__ == '__main__':

    import math

    print('Start.')

    # Test cases taken from http://code.activestate.com/recipes/579046-engineering-notation/
    # some string-based test cases added.
    test = [
        '-78951',
        '-500',
        '1e-3',
        '0.005',
        '0.05',
        '0.12',
        '10',
        '23.3456789',
        '50',
        '150',
        '250',
        '800',
        '1250',
        '127e11',
        '51234562',
        str(math.pi),
        str(1.0/3.0),
        'inf',
        'nan'
    ]

    print("{0:>20}: {1:>20} {2:>10} {3:>14}".format('string', 'float', 'default', 'prec=8'))
    for x in test:
        f = float(x)
        print("{0:>20}: {1:>20} {2:>10} {3:>14}".format(x, f, to_string(f), to_string(f, 8)))

    print('Done.')

