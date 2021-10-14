import WinCppDll

x = WinCppDll.add2(2, 3)

print(x)

WinCppDll.add_ref2(2, 3, x)
print(x)

x = WinCppDll.set_integer_ref_gets_100()
print(f'set_integer_ref_gets_100 {x}')

x = WinCppDll.set_integer_ptr_gets_200()
print(f'set_integer_ptr_gets_200 {x}')

x = WinCppDll.set_integer_ref_ptr_gets_300()
print(f'set_integer_ref_ptr_gets_300 {x}')

x = WinCppDll.pass_by_ptr_arr_gets_1357()
print(f'pass_by_ptr_arr_gets_1357 {x}')

x = WinCppDll.pass_by_ref_ptr_arr()
print(f'pass_by_ref_ptr_arr {x}')

x = WinCppDll.get_data_array2()
print(f'get_data_array2 {x}')

