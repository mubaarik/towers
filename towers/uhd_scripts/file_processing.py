from parameters import *
from utility_funcs import *
from fft_file_analizer import *
if __name__=='__main__':
	sleeps=0
	max_number_of_sleeps = 200
	while True:
		files = directory_parser('meta_files', extension='.csv')
		if files:
			sleeps = 0
			for f in files:
				analizer = Analizer(f)
				for sample in analizer.row_map:
					analizer.pw_frq_pair_to_csv(sample)
		else:
			sleeps+=1
			if sleeps>=max_number_of_sleeps:
				break

			time.sleep(1)
		