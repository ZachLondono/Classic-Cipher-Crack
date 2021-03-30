import sys
import ClassicCypherCrack as crack

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f"Invlid arguments\npython3 Usage: {sys.argv[0]} [filepath]")
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
	key = crack.decodeKey(encryptedText)

	if not key:
		print("Failed to find valid key")
		exit()

	# Write key to file
	try:
		keyFile = open("key.txt", 'w')
		keyFile.write(str(key))
	except Exception as e:
		print("Failed to write key to file")
		exit()

	count = 0
	for i in range(len(crack.alpha)):
		if crack.alpha[i] != key[i]:
			print(f"Wrong: {crack.alpha[i]}, {key[i]}")
			count += 1
	print(f"Acc: {(1 - count / 26) * 100}%")