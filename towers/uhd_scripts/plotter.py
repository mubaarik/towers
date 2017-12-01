import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import glob
import os
from argparse import ArgumentParser
'''
Replaces the white spaces in filename with the underscore character
'''
def filename_formatter(filename, extension):
	assert len(filename)>0, "The filename can't be an empty string!"
	formatted = filename.strip().replace(' ','_').strip()
	parts =formatted.split('.')
	assert len(parts)<=2, "The filename contains multiple extensions!"
	if len(parts)>1:
		return formatted
	else:
		return parts[0]+extension

'''
helper function for plotter, for plotting single files.
input: 
	input_file: csv file of format(index,freq,power)
	output_dirc: if not None saves the plot to that directory
	save_plot: if True saves the plot to output_dirc
	filename: If you want to save the file with specific name use this parameter 

Behavior:
	1. Plot the freq vs power
	2. Saves the plot to the named output directory if save_plot is true.
	The saved file is named file name if filename is not None otherwise with 
	same name as the inputfile

'''
def plotFile(input_file, output_dirc=None, save_plot=False,filename=None):
	if filename is None:
		filename = input_file.split('/')[-1].split('-')[0].split('.')[0]
	filename = filename_formatter(filename, '.jpg')
	data = pd.read_csv(input_file)
	fig, ax = plt.subplots()
	ax.plot(data['Freq'].values,10*np.log10(data['Power(dB)'].values))
	ax.set_title(filename.split('.')[0])
	if save_plot:
		fig.savefig('figures/'+filename)
	plt.show()
'''
inputs:
	input_dirc: Directory to look for csv files mapping frequencies 
			to powers(expects all the csv files in this directory to be of this format)
	output_dirc: A directory to save the plots to(makes the directory if it doesn't exist)
	save_plots: Saves the plots to output_dirc if true(defaults to False)
	plot_file: If you want to plot just the single file then set this variable to true
	input_file: If you just want to plot a single file of this format then specify 
			the input(expects plot_file to be true for this option to be chosen)
	output_file: If you want to save the plot with specific name, specify this parameter.
'''
def plotter(input_dirc=None, output_dirc='figures',save_plots=False, plot_file = False, input_file=None,output_file=None):
	print input_dirc
	assert (input_file is None and not plot_file), "expected plot_file to be true or input_dirc to be specified"
	if save_plots:
		if not os.path.exists(output_dirc):
			os.makedirs(output_dirc)
	if plot_file:
		plotFile(input_file, output_dirc=output_dirc, save_plot=save_plots,filename=output_file)
	else:
		for f in glob.glob(input_dirc+'/*.csv'):
			plotFile(f, output_dirc=output_dirc, save_plot=save_plots,filename=output_file)
	
	    
def options():
	parser = ArgumentParser(description='Plotting (freq,power) csv files and saving the plots for visual inspection');
	parser.add_argument('--input_dirc', action='store', default=None, 
		help="Directory to look for csv files mapping frequencies to powers"+
		" (expects all the csv files in this directory to be of this format)")
	parser.add_argument('--output_dirc', action='store', default='figures', 
		help="A directory to save the plots to(default=%default)")
	parser.add_argument('--save_plots', action="store_true", default=False, 
		help="Saves the plots to output_dirc if specified(default=%default)")
	parser.add_argument('--plot_file', action="store_true", default=False, 
		help="If you want to plot just the single file then set this variable(default=%default)")
	parser.add_argument('--input_file', action="store", default=None, 
		help="Name of the single file to be plotted(default=%default)")
	parser.add_argument('--output_file', action="store", default=None,
		help = "If you want to save the plot with specific name, set this paramter(default=%default)")
	args = parser.parse_args()
	return args
if __name__=="__main__":
	args = options()
	plotter(input_dirc=args.input_dirc, output_dirc=args.output_dirc,save_plots=args.save_plots, plot_file = args.plot_file,
	 input_file=args.input_file,output_file=args.output_file)







