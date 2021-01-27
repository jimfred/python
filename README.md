# python
Personal Python collection

The python-gdb folder has an application that finds the address for several symbols in a .elf file, where addresses could be used by pyocd to fetch values from firmware. Although pyocd can extract symbol addresses from an ELF, it cannot extract addresses based on complex, nested structures and this is where GDB shines. The only problem is that GDB is called out-of-process. This example has a GDB executable for ARM, and a Blink.elf file targeted for an STM32.
