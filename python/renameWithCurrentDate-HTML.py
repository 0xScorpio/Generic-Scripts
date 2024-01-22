import os
from datetime import date

def main():
	findDate = date.today()
	today = findDate.strftime("_%d%m%y")

	dir_path = 'EDIT-DIRECTORY-PATH'
	for filename in os.listdir(dir_path):
		if filename.endswith('.html'):
			size = len(filename)
			mod = filename[:size - 12] + today + '.html'
			src = dir_path + filename
			dest = dir_path + mod
			os.rename(src, dest)

if __name__ == '__main__':
	main()
