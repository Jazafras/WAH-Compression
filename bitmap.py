from itertools import groupby

def bitmap_creation(lines, file):
    for x in lines:
        data = x.split(',')

        #write bit for type of animal
        if data[0] == 'cat':
            file.write('1000')
        elif data[0] == 'dog':
            file.write('0100')
        elif data[0] == 'turtle':
            file.write('0010')
        elif data[0] == 'bird':
            file.write('0001')

        #write bit for age of animal
        if 1 <= int(data[1]) <= 10:
            file.write('1000000000')
        elif 11 <= int(data[1]) <= 20:
            file.write('0100000000')
        elif 21 <= int(data[1]) <= 30:
            file.write('0010000000')
        elif 31 <= int(data[1]) <= 40:
            file.write('0001000000')
        elif 41 <= int(data[1]) <= 50:
            file.write('0000100000')
        elif 51 <= int(data[1]) <= 60:
            file.write('0000010000')
        elif 61 <= int(data[1]) <= 70:
            file.write('0000001000')
        elif 71 <= int(data[1]) <= 80:
            file.write('0000000100')
        elif 81 <= int(data[1]) <= 90:
            file.write('0000000010')
        elif 91 <= int(data[1]) <= 100:
            file.write('0000000001')

        #write bit for whether animal is adopted or not
        if data[2] == 'True':
           file.write('10\n')
        elif data[2] == 'False':
           file.write('01\n')

def compression(lines, file, column, bit):
    bit_count = 0
    bit_strings = ""
    # split column into rows of bit length
    for x in lines:
        bits = list(x[column])
        for y in bits:
            bit_strings += y
            bit_count += 1
            if bit_count == bit - 1:
                bit_strings += ","
                bit_count = 0
    bit_list = [x.strip() for x in bit_strings.split(',')]

    #group bits by (segment, # of consecutive repetitions)
    grouped_bit_list = [(k, sum(1 for i in g)) for k, g in groupby(bit_list)]

    #write compression to file
    for x in grouped_bit_list:
        segment = x[0]
        binary_count = "{0:b}".format(x[1])
        max_length = (bit - 2) - len(binary_count)
        if segment.count(segment[0]) == len(segment) and len(segment) == (bit - 1): #segment is a run
            file.write("1") #flag as a run
            file.write(segment[0]) #flag what type of run
            for i in range(0, max_length):
                file.write("0")
            file.write(binary_count) #flag how many repetitions of run
            #file.write("\n")
        else: #segment is a literal
            file.write("0") #flag as a literal
            file.write(segment) #write segment as is
    file.write("\n")

def fill_count(lines, column, bit):
    fillCount = 0
    bit_count = 0
    bit_strings = ""
    # split column into rows of given bits
    for x in lines:
        bits = list(x[column])
        for y in bits:
            bit_strings += y
            bit_count += 1
            if bit_count == (bit - 1):
                bit_strings += ","
                bit_count = 0
    bit_list = [x.strip() for x in bit_strings.split(',')]

    # group bits by (segment, # of consecutive repetitions)
    grouped_bit_list = [(k, sum(1 for i in g)) for k, g in groupby(bit_list)]

    for x in grouped_bit_list:
        segment = x[0]
        if segment.count(segment[0]) == len(segment): #segment is a fill
            fillCount += x[1]
    return fillCount

def literal_count(lines, column, bit):
    literalCount = 0
    bit_count = 0
    bit_strings = ""
    # split column into rows of given bits
    for x in lines:
        bits = list(x[column])
        for y in bits:
            bit_strings += y
            bit_count += 1
            if bit_count == (bit - 1):
                bit_strings += ","
                bit_count = 0
    bit_list = [x.strip() for x in bit_strings.split(',')]

    # group bits by (segment, # of consecutive repetitions)
    grouped_bit_list = [(k, sum(1 for i in g)) for k, g in groupby(bit_list)]

    for x in grouped_bit_list:
        segment = x[0]
        if segment.count(segment[0]) != len(segment): #segment is a literal
            literalCount += x[1]
    return literalCount

def file_write(fileName, lines, bit):
    bit_compression = open(fileName, "w")
    fills = 0
    literals = 0
    for i in range(0, 16): #column-oriented compression
        compression(lines, bit_compression, i, bit)
        fills += fill_count(lines, i, bit)
        literals += literal_count(lines, i, bit)
    print(fileName + " fill count: " + str(fills))
    print(fileName + " literal count: " + str(literals))
    bit_compression.close()

def main():
    # hard-coded address of file
    lines = [line.rstrip('\n') for line in open('animals.txt')]
    #lines = [line.rstrip('\n') for line in open('test_solution_32bit_words/animals_test.txt')]
    sorted_lines = sorted(lines)

    # unsorted bitmap creation
    unsorted_bitmap = open("animals_unsorted_bitmap.txt", "w")
    bitmap_creation(lines, unsorted_bitmap)
    unsorted_bitmap.close()

    # sorted bitmap creation
    sorted_bitmap = open("animals_sorted_bitmap.txt", "w")
    bitmap_creation(sorted_lines, sorted_bitmap)
    sorted_bitmap.close()

    ######### Unsorted 32-bit and 64-bit compression #########
    bit_lines = [line.rstrip('\n') for line in open('animals_unsorted_bitmap.txt')]

    file_write("animals_unsorted_32bit_compression.txt", bit_lines, 32)
    file_write("animals_unsorted_64bit_compression.txt", bit_lines, 64)

    ######### Sorted 32-bit and 64-bit compression #########
    sorted_bit_lines = [line.rstrip('\n') for line in open('animals_sorted_bitmap.txt')]

    file_write("animals_sorted_32bit_compression.txt", sorted_bit_lines, 32)
    file_write("animals_sorted_64bit_compression.txt", sorted_bit_lines, 64)
main()