import subprocess

list = [
    ("CubeProgrammer_API.dll", r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\api\lib\CubeProgrammer_API.dll"), 
    ("CubeProgrammer_API.lib", r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\api\lib\x64\CubeProgrammer_API.lib"),
    ("CubeProgrammer_API.h",   r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\api\include\CubeProgrammer_API.h")
]

for x in list:
    (link, original) = x
    cmd = f'cmd /C mklink {link} "{original}"'
    x = subprocess.run(cmd.split())
    
input("Press Enter to continue...")
