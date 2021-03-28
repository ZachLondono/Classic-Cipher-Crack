import sys

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f"Invlid arguments\n Usage: {sys.argv[0]} [filepath]")
		exit()

	# Open file which contains encrypted data
	try:
		encryptedFile = open(sys.argv[1], 'r')
	except Exception as e:
		print("Error: failed to open file")
		exit()

	# Read encrypted data
	try:
		encryptedText = encryptedFile.read()
		encryptedFile.close()
	except Exception as e:
		print("Error: failed to read from file")
		exit()

	# Find key from data
	# print(encryptedText)

	key = "ABCDE"
	# Write key to file
	try:
		keyFile = open("key.txt", 'w')
		keyFile.write(key)
	except Exception as e:
		print("Failed to write key to file")
		exit()	