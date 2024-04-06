def read_file_in_blocks(path, block_size=1024):
    try:
        with open(path, 'rb') as file:
            while True:
                block = file.read(block_size)
                if not block:
                    break
                yield block
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error reading file: {e}")


file_path = 'wallpaper.jpg'
for block in read_file_in_blocks(file_path):
    print(block)
