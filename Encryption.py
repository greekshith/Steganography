HEADER_SIZE = 1078  # Header size of bmp file : 14 + 40 + 1024 bytes

class Encryption:
    def open_bmp_file(self):
        with open(self.original_file_name, 'rb') as f:
            self.original_image_data = f.read()


    def copy_header(self):
        # file header (14) and bitmap info header (40) and palette (1024)
        for i in range(0, HEADER_SIZE):
            self.new_image_data.append(self.original_image_data[i])
            self.byte_count += 1


    def hide_int(self, curr_hide_int):
        curr_hide_binary = '{:032b}'.format(curr_hide_int)
        for i in range(0, 32):
            curr_image_bin = '{0:08b}'.format(self.original_image_data[self.byte_count])
            new_image_bin = curr_hide_binary[i] + curr_image_bin[1:]
            new_image_int = int(new_image_bin, 2)
            self.new_image_data.append(new_image_int)
            self.byte_count += 1


    def hide_char(self, curr_hide_byte):
        # Get binary value of one byte
        # Example:
        # a = '{0:08b}'.format(255)
        # print(a) # '1111111'
        curr_hide_binary = '{0:08b}'.format(ord(curr_hide_byte))

        # Hide one byte in eight bytes
        for i in range(0, len(curr_hide_binary)):
            curr_image_bin = '{0:08b}'.format(self.original_image_data[self.byte_count])
            new_image_bin = curr_hide_binary[i] + curr_image_bin[1:]
            new_image_int = int(new_image_bin, 2)
            self.new_image_data.append(new_image_int)
            self.byte_count += 1


    def start_hide(self):
        self.hide_int(len(self.hide_msg))
        for i in range(0, len(self.hide_msg)):
            self.hide_char(self.hide_msg[i])


    def copy_remaining(self):
        left_data = self.original_image_data[self.byte_count:]
        for left_byte in left_data:
            self.new_image_data.append(left_byte)


    def write_file(self):
        with open(self.new_file_name, 'wb') as out:
            new_image_bytes = bytearray(self.new_image_data)
            out.write(new_image_bytes)


    def run(self):
        self.open_bmp_file()
        self.copy_header()
        self.start_hide()
        self.copy_remaining()
        self.write_file()


    def __init__(self, original_file_name, new_file_name, hide_msg):
        self.original_file_name = original_file_name
        self.new_file_name = new_file_name
        self.hide_msg = hide_msg
        self.byte_count = 0
        self.original_image_data = ''
        self.new_image_data = []

