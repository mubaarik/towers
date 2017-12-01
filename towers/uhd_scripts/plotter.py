import pandas as pd
import glob
import os
'''
Replaces the white spaces in filename with the underscore character
'''
def filename_formatter(filename, extension):
	assert len(filename)>0, "The filename can't be an empty string!"
	formatted = filename.strip().replace(' ','_').strip()
	parts =formatted.split('.')
	assert len(parts)<=2, "The filename contains multiple extensions!"
	if parts.len(parts)>1:
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
    ax.plot(data['1'].values,10*np.log10(data['0'].values))
    ax.set_title(filename.split('.')[0])
    if save_plot:
    	fig.savefig('figures/'+filename)
    plt.show()
'''
inputs:
	input_dirc: Directory to look for csv files mapping frequencies 
			to powers(expects all the files this directory to be of this format)
	output_directory: A directory to save the plots to(makes the directory if it doesn't exist)
	save_plots: Saves the plots to output_dirc if true(defaults to False)
	plot_file: If you want to plot just the single file then set this variable to true
	input_file: If you just want to plot a single file of this format then specify 
			the input(expects plot_file to be true for this option to be chosen)
	output_file: If you want to save the plot with specific name, specify this parameter.
'''
def plotter(input_dirc=None, output_dirc='figures',save_plots=False, plot_file = False, input_file=None,output_file=None):
	assert (input_file is not None or plot_file), "expected plot_file to be true or input_dirc to be specified"
	if save_plots:
		if not os.path.exists(output_dirc):
			os.makedirs(output_dirc)
	if plot_file:
		plotFile(input_file, output_dirc=output_dirc, save_plot=save_plots,filename=output_file)
	else:
		for f in glob.glob(input_dirc+'/*.csv'):
			plotFile(f, output_dirc=output_dirc, save_plot=save_plots,filename=output_file)
	
	    






