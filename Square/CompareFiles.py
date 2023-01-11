import sys


class CompileFiles:
    def comparefile(path1, path2):
        file1 = open(path1, "r")
        file2 = open(path2, "r")
        while not file1.closed and not file2.closed:
            if file1.readline().strip() != file2.readline().strip():
                print(f"compare failed at {file1.lineno}")
        file1.close()
        file2.close()

    if __name__ == "__main__":
        comparefile(sys.argv[1], sys.argv[2])
