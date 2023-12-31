HEADER_SIZE = 1078  # Header size of bmp file : 14 + 40 + 1024 bytes


class Decryption:
    def read_header(self):
        for i in range(0, HEADER_SIZE):
            self.f.read(1)


    def get_int(self):
        curr_hide_bin = ''
        for i in range(0, 32):
            curr_image_byte = self.f.read(1)
            if len(curr_image_byte) == 0:
                return ''
            curr_image_bin = '{0:08b}'.format(ord(curr_image_byte))
            curr_hide_bin += curr_image_bin[0]
        curr_hide_int = int(curr_hide_bin, 2)
        return curr_hide_int


    def get_char(self):
        curr_hide_bin = ''
        for i in range(0, 8):
            curr_image_byte = self.f.read(1)
            if len(curr_image_byte) == 0:
                return ''
            curr_image_bin = '{0:08b}'.format(ord(curr_image_byte))
            curr_hide_bin += curr_image_bin[0]
        curr_hide_char = chr(int(curr_hide_bin, 2))
        return curr_hide_char


    def find_hide(self):
        curr_hide_int = self.get_int()
        for i in range(0, curr_hide_int):
            curr_hide_char = self.get_char()
            self.hide_msg += curr_hide_char
        self.f.close()


    def run(self):
        self.read_header()
        self.find_hide()
        return self.hide_msg


    def __init__(self, new_file_name):
        self.new_file_name = new_file_name
        self.f = open(self.new_file_name, 'rb')
        self.hide_msg = ''
        
