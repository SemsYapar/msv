from pycparser import parse_file, c_ast
import json
import ctypes
from ctypes import wintypes
import ctypes
import argparse
import platform

#Weller ve chatgpt nin büyük büyük yardımlarıyla

def is_process_64bit(pid):
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    # Open process handle
    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    OpenProcess.restype = wintypes.HANDLE

    hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not hProcess:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        # Try using IsWow64Process2 (Windows 10+)
        try:
            IsWow64Process2 = kernel32.IsWow64Process2
            IsWow64Process2.argtypes = [wintypes.HANDLE,
                                        ctypes.POINTER(wintypes.USHORT),
                                        ctypes.POINTER(wintypes.USHORT)]
            IsWow64Process2.restype = wintypes.BOOL

            process_machine = wintypes.USHORT()
            native_machine = wintypes.USHORT()
            if not IsWow64Process2(hProcess, ctypes.byref(process_machine), ctypes.byref(native_machine)):
                raise ctypes.WinError(ctypes.get_last_error())

            if process_machine.value == 0:
                return True  # 64-bit
            else:
                return False  # 32-bit via WOW64

        except AttributeError:
            # Fallback: Use IsWow64Process
            IsWow64Process = kernel32.IsWow64Process
            IsWow64Process.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
            IsWow64Process.restype = wintypes.BOOL

            wow64 = wintypes.BOOL()
            if not IsWow64Process(hProcess, ctypes.byref(wow64)):
                raise ctypes.WinError(ctypes.get_last_error())

            is_wow64 = bool(wow64.value)

            # Eğer işlem WOW64 altındaysa, 32-bittir
            # Aksi halde, sistem 64-bit ise işlem de 64-bit'tir
            is_os_64bit = ctypes.sizeof(ctypes.c_voidp) == 8
            return is_os_64bit and not is_wow64

    finally:
        kernel32.CloseHandle(hProcess)
def read_process_memory(pid, address, size):
    PROCESS_VM_READ = 0x0010
    PROCESS_QUERY_INFORMATION = 0x0400

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    OpenProcess.restype = wintypes.HANDLE

    ReadProcessMemory = kernel32.ReadProcessMemory
    ReadProcessMemory.argtypes = [
        wintypes.HANDLE,
        wintypes.LPCVOID,
        wintypes.LPVOID,
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_size_t)
    ]
    ReadProcessMemory.restype = wintypes.BOOL

    hProcess = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not hProcess:
        raise ctypes.WinError(ctypes.get_last_error())

    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t(0)
    if not ReadProcessMemory(hProcess, address, buffer, size, ctypes.byref(bytesRead)):
        kernel32.CloseHandle(hProcess)
        raise ctypes.WinError(ctypes.get_last_error())

    kernel32.CloseHandle(hProcess)
    return buffer.raw[:bytesRead.value]
# Basit tiplerin bayt cinsinden boyutları (64-bit varsayıyoruz pointerlar için)

ap = argparse.ArgumentParser(description="Process some integers.")
ap.add_argument("-p",'--pid', type=int, required=True, help='Process ID to read memory from')
ap.add_argument("-a",'--address', type=lambda x: eval(x, {"__builtins__": None}, {}), required=True, help='Memory address to read from')
ap.add_argument("-s",'--struct_name', type=str, required=True, help='Name of the struct to display')
ap.add_argument("-f",'--file', type=str, default='targetstruct.h', help='Header file containing struct definitions')
args = ap.parse_args()

POINTER_SIZE = 8 if is_process_64bit(args.pid) else 4

special_type_aligns = {

}

type_sizes = {
    
    'char': 1,
    'int': 4,
    'float': 4,
    'double': 8,
    "bool": 1,
    "short": 2,
    "long": 4 if platform.system() == 'Windows' else 8,
    "long long": 8,
    "signed char": 1,
    "unsigned char": 1,
    "unsigned int": 4,
    "unsigned short": 2,
    "unsigned long": 4 if platform.system() == 'Windows' else 8,
    "unsigned long long": 8,


    # Fixed-width integer types
    'int8_t': 1,
    'uint8_t': 1,
    'int16_t': 2,
    'uint16_t': 2,
    'int32_t': 4,
    'uint32_t': 4,
    'int64_t': 8,
    'uint64_t': 8,

    # Platform-dependent integer types
    'size_t': POINTER_SIZE,
    'ssize_t': POINTER_SIZE,
    'intptr_t': POINTER_SIZE,
    'uintptr_t': POINTER_SIZE,
    'ptrdiff_t': POINTER_SIZE,
}


def get_type_name(type_node):
    """type_node’dan tip stringi alır, array ve pointer dahil."""
    if isinstance(type_node, c_ast.TypeDecl):
        t = type_node.type
        if isinstance(t, c_ast.IdentifierType):
            return ' '.join(t.names)
        elif isinstance(t, c_ast.Struct):
            return f"{t.name}"
        elif isinstance(t, c_ast.Union):
            return f"{t.name}"
        else:
            return str(t)
    elif isinstance(type_node, c_ast.PtrDecl):
        if isinstance(type_node.type, c_ast.FuncDecl):
            return get_type_name(type_node.type.type) + ' (*)'+('('+ ', '.join(get_type_name(param.type) + (" " + param.name if param.name != None else "") for param in type_node.type.args.params) +')' if type_node.type.args else '()')
        return get_type_name(type_node.type) + '*'
    #elif isinstance(type_node, c_ast.FuncDecl):
    #    return get_type_name(type_node.type) + ' ('+ ', '.join(get_type_name(param.type) + " " + param.name for param in type_node.args.params) +')'
    elif isinstance(type_node, c_ast.ArrayDecl):
        arr_type = get_type_name(type_node.type)
        arr_dim = None
        if type_node.dim:
            try:
                arr_dim = int(type_node.dim.value)
            except Exception:
                arr_dim = None
        if arr_dim is not None:
            return f"{arr_type}[{arr_dim}]"
        else:
            return arr_type + "[]"
    else:
        return str(type_node)


def get_type_size(type_str):
    if '[' in type_str:
        base, rest = type_str.split('[', 1)
        arr_dim = int(rest.split(']',1)[0])
        base_size = get_type_size(base)
        return base_size * arr_dim
    if type_str.endswith('*') or '(*)' in type_str:
        return POINTER_SIZE
    if type_str in type_sizes:
        return type_sizes[type_str]
    else:
        raise ValueError(f"Uyarı: Bilinmeyen tip '{type_str}' için boyut hesaplanamadı.")

def get_alignment(type_str):
    """Bir tipin alignment gereksinimini döner."""
    if type_str.endswith('*') or '(*)' in type_str:
        return POINTER_SIZE
    if '[' in type_str:
        base, _ = type_str.split('[', 1)
        return get_alignment(base)
    if type_str in special_type_aligns:
        return special_type_aligns[type_str]
    if type_str in type_sizes:
        return type_sizes[type_str]
    raise ValueError(f"Bilinmeyen tip '{type_str}' için alignment hesaplanamadı.")
    
def get_endoffset_of_field(offset, alignment):
    return (offset + alignment - 1) & ~(alignment - 1)

def parse_union_fields(union_node):
    offset = 0
    fields = []
    max_align = 1
    max_size = 0
    for decl in union_node.decls:
        name = decl.name
        type_str = get_type_name(decl.type)
        size = get_type_size(type_str)
        max_size = max(max_size, size)
        align_req = get_alignment(type_str)
        max_align = max(max_align, align_req)
        fields.append({'name': name, 'type': type_str, 'offset': 0, 'size': size})

    union_endoffset = get_endoffset_of_field(0, max_align)
    special_type_aligns[union_node.name] = max_align
    end_padding = union_endoffset - max_size
    if end_padding > 0:
        fields.append({'name': '__padding_end', 'type': 'char[]', 'size': end_padding, 'offset': offset})
    type_sizes[union_node.name] = max_size
    return fields

def parse_struct_fields(struct_node):
    offset = 0
    fields = []
    max_align = 1  # struct genel align için
    for decl in struct_node.decls:
        name = decl.name
        type_str = get_type_name(decl.type)
        size = get_type_size(type_str)
        align_req = get_alignment(type_str)
        max_align = max(max_align, align_req)

        endoffset = get_endoffset_of_field(offset, align_req)
        padding = endoffset - offset
        if padding > 0:
            fields.append({'name': f'__padding_before_{name}', 'type': 'char[]', 'size': padding, 'offset': offset})
        offset = endoffset

        fields.append({'name': name, 'type': type_str, 'offset': offset, 'size': size})
        offset += size
        
    special_type_aligns[struct_node.name] = max_align
    # Struct sonu padding (struct align için)
    struct_endoffset = get_endoffset_of_field(offset, max_align)
    end_padding = struct_endoffset - offset
    if end_padding > 0:
        fields.append({'name': '__padding_end', 'type': 'char[]', 'size': end_padding, 'offset': offset})

    type_sizes[struct_node.name] = struct_endoffset
    return fields

class BlockVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.structs = {}
        self.unions = {}

    def visit_Struct(self, node):
        if node.decls and node.name:  # isimli structlar
            fields = parse_struct_fields(node)
            self.structs[node.name] = fields
    def visit_Union(self, node):
        if node.decls and node.name:
            fields = parse_union_fields(node)
            self.unions[node.name] = fields

def parse_blocks(filename):
    ast = parse_file(filename)
    v = BlockVisitor()
    v.visit(ast)
    return v.structs,v.unions

def display_block_table(block_fields, raw_data):
    headers = ["Offset", "Size", "Type", "Name", "Value"]
    col_widths = [8, 6, 50, 50, 35]

    def print_border():
        print('+' + '+'.join(['-' * (w + 2) for w in col_widths]) + '+')

    def print_row(cells):
        row = '|'.join(f' {str(c)[:w]:<{w}} ' for c, w in zip(cells, col_widths))
        print('|' + row + '|')

    print_border()
    print_row(headers)
    print_border()

    for field in block_fields:
        offset = field['offset']
        size = field['size']
        name = field['name']
        type_str = field['type']
        data = raw_data[offset:offset + size]
        if "*" in type_str or "ptrdiff_t" == type_str or "uintptr_t" == type_str or "intptr_t" == type_str:
            value = f"0x{int.from_bytes(data, 'little'):016X}"
        elif "int" in type_str or "size_t" == type_str or "ssize_t" == type_str or "long" in type_str or "short" in type_str:
            signed = ('int' in type_str and 'uint' not in type_str) or ("signed" in type_str and "unsigned" not in type_str) or ("ssize_t" == type_str and "size_t" != type_str )
            value = int.from_bytes(data, 'little', signed=signed)
        elif 'float' == type_str:
            value = data.hex()+" ("+str(ctypes.c_float.from_buffer_copy(data).value)+")"
        elif 'double' == type_str:
            value = data.hex()+" ("+str(ctypes.c_double.from_buffer_copy(data).value)+")"
        elif type_str == 'char':
            value = chr(data[0]) if 32 <= data[0] < 127 else f"\\x{data[0]:02X}"
        elif type_str == "bool":
            value = data.hex()+" ("+("true" if data[0] else "false")+")"
        elif type_str == 'char[]':
            value = 'padding'
        else:
            value = data.hex()

        print_row([offset, size, type_str, name, value])

    print_border()



if __name__ == '__main__':
    structs, unions = parse_blocks(args.file)
    s_json = json.dumps(structs, indent=4)
    #print(s_json)

    block_name = args.struct_name
    if block_name in structs:
        block_fields = structs[block_name]
        total_size = type_sizes[block_name]
    elif block_name in unions:
        block_fields = unions[block_name]
        total_size = type_sizes[block_name]    
    else:
        print(f"{block_name} tanımlı değil.")
        exit(1)



    try:
        raw_data = read_process_memory(args.pid, args.address, total_size)
        display_block_table(block_fields, raw_data)
    except Exception as e:
        print(f"Hata: {e}")
