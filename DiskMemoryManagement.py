class MemoryBlock:
    def __init__(self, start, size, file_name=None):
        self.start = start
        self.size = size
        self.file_name = file_name

class DiskManager:
    def __init__(self):
        self.total_capacity = 368640
        self.occupied_blocks = []
        self.free_blocks = [MemoryBlock(0, self.total_capacity)]

    def write_file(self, file_name, file_size):
        if file_size < 18 or file_size > 32768:
            return f"Error: File size {file_size} bytes is out of valid range (18-32768 bytes)"

        best_block = None
        best_index = -1
        for i, block in enumerate(self.free_blocks):
            if block.size >= file_size:
                if best_block is None or block.size < best_block.size:
                    best_block = block
                    best_index = i

        if best_block is None:

            if self.occupied_blocks and self.occupied_blocks[-1].start + self.occupied_blocks[-1].size + file_size <= self.total_capacity:
                new_block = MemoryBlock(self.occupied_blocks[-1].start + self.occupied_blocks[-1].size, file_size, file_name)
                self.occupied_blocks.append(new_block)
                return f"File {file_name} written at position {new_block.start}"
            return f"Error: No suitable space for file {file_name} of size {file_size} bytes"


        new_block = MemoryBlock(best_block.start, file_size, file_name)
        self.occupied_blocks.append(new_block)
        self.occupied_blocks.sort(key=lambda x: x.start)

        if best_block.size == file_size:
            self.free_blocks.pop(best_index)
        else:
            best_block.start += file_size
            best_block.size -= file_size

        self.free_blocks.sort(key=lambda x: x.start)
        self._merge_free_blocks()
        return f"File {file_name} written at position {new_block.start}"

    def delete_file(self, file_name):
        for i, block in enumerate(self.occupied_blocks):
            if block.file_name == file_name:
                new_free_block = MemoryBlock(block.start, block.size)
                self.free_blocks.append(new_free_block)
                self.free_blocks.sort(key=lambda x: x.start)
                self.occupied_blocks.pop(i)
                self._merge_free_blocks()
                return f"File {file_name} deleted"
        return f"Error: File {file_name} not found"

    def _merge_free_blocks(self):
        if not self.free_blocks:
            return
        merged = []
        current = self.free_blocks[0]
        for block in self.free_blocks[1:]:
            if current.start + current.size == block.start:
                current.size += block.size
            else:
                merged.append(current)
                current = block
        merged.append(current)
        self.free_blocks = merged

    def get_status(self):
        status = "Disk Status:\nOccupied Blocks:\n"
        for block in self.occupied_blocks:
            status += f"File: {block.file_name}, Start: {block.start}, Size: {block.size} bytes\n"
        status += "\nFree Blocks:\n"
        for block in self.free_blocks:
            status += f"Start: {block.start}, Size: {block.size} bytes\n"
        return status

def main():
    disk = DiskManager()
    while True:
        print("\n1. Write file")
        print("2. Delete file")
        print("3. Show disk status")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            file_name = input("Enter file name: ")
            try:
                file_size = int(input("Enter file size (bytes): "))
                print(disk.write_file(file_name, file_size))
            except ValueError:
                print("Error: Invalid file size")
        elif choice == '2':
            file_name = input("Enter file name to delete: ")
            print(disk.delete_file(file_name))
        elif choice == '3':
            print(disk.get_status())
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()