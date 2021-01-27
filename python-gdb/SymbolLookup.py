'''
SymbolLookup.py
2020-04-19 Jim Fred

Perform symbol lookup using gdb.
Requires a path to gdb and a .elf file  and a list of variable names.
See  __main__ for example usage.

This example does a subprocess.run() for gdb and passes all parameters using --batch so that gdb exits when complete.
This is a bit faster than several itterative calls.

'''
import re
import subprocess

'''
Class SymbolLookup has a constructor that takes all necessary paramters and creates a dictionary keyed by symbol name 
where values are the address and type.
'''
class SymbolLookup:

    """
    Class used by SymbolLookup to store symbol addresses and type.
    """
    class SymbolAddressType:
        def __init__(self, address, type):
            self.address = address
            self.type = type

        def __repr__(self):
            return '({0})0x{1:X}'.format(self.type, self.address)

    '''
    Constructor creates a dictionary.
    '''
    def __init__(self, gdb_exe, target_img, symbol_list):
        if 1:
            gdb_args = [
                gdb_exe,
                target_img,  # target executable.
                '--batch'   # Causes gdb to exit when done processing initial args.
            ]

            for sym in symbol_list:
                gdb_args.append('-ex=p(&{0})'.format(sym))

            # For more robust error checking, print "done" at the end, from gdb to the response list.
            gdb_args.append('--ex=p("done")')

            # Create a gdb object.
            result = subprocess.run(gdb_args, stdout=subprocess.PIPE)

            responses = result.stdout.decode('utf-8').splitlines()

            # validate the response based on the length and the last response being  '$3 = "done"' where 3 is the len() of responses.
            if (len(responses) != (len(symbol_list) + 1)  or responses[-1] != '${0} = "done"'.format(len(symbol_list) + 1)):
                raise Exception('Unexpected response from gdb.')

            del responses[-1] # delete the last element of the responses (containing "done").

            # Compose a dictionary of results, indexed by the symbol name.
            self.symbols = {}

            for eachResponse in responses:
                try:
                    # for a string like '$1 = (float *) 0x20000a64 <HeaterControl::htrCurrentTotal_amps>', parse for 'float *' and  '0x20000a64'.
                    reg_exp_match = re.search('\$(\d*?) = \((.*?)\) 0x([0-9A-Fa-f]*) ', eachResponse)
                    index = int(reg_exp_match.group(1)) - 1
                    address = int(reg_exp_match.group(3), 16)
                    type = reg_exp_match.group(2)
                    ###print('{0}: {1:08X}, {2}'.format(index, address, type))
                except:
                    print('Can\'t parse {0}'.format(eachResponse))

                # Add this response to the dictionary.
                self.symbols[symbol_list[index]] = SymbolLookup.SymbolAddressType(address, type)

        # self.symbols should now be complete.
        return

'''
Test the usage of SymbolLookup.
'''
if __name__ == "__main__":

    symbol_lookup = SymbolLookup(
      gdb_exe = './resources/gdb.exe',
      target_img = './resources/Blink.elf',
      symbol_list=[
          'user_data.sub_type[1].i[2]',
          'user_data.sub_type[2].f[3]',
          'user_data.ticks',
          'user_data.btn_pressed',
          'main'
      ]
    )

    for symbol_name, symbol_info in symbol_lookup.symbols.items():
        print('{0} is ({1}) at 0x{2:X}'.format(symbol_name, symbol_info.type, symbol_info.address))

# eof.
