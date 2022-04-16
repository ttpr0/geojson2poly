import unittest
import logging

def int_to_ordinal(num:int):
    """converts int to ordinal (e.g. 1 -> 1st, 3 -> 3rd)\n
    params:
        num -> input integer

    returns:
        -> ordinal as string
    """
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return str(num) + 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return str(num) + 'st'
    elif (lastDigit == 2):
        return str(num)+ 'nd'
    elif (lastDigit == 3):
        return str(num)+ 'rd'
    else:
        return str(num)+ 'th'

def fortran_format(n) -> str:
    """converts number to scientific notation (7 decimal places)\n
    params:
        n -> input number

    returns:
        -> number in scientific notation as string
    """
    return '{:.7E}'.format(float(n))