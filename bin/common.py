#!/usr/bin/python
import os
import numpy as np
import multiprocessing as mp
import subprocessing as sub
import shlex









#Make sure a directory path contains a trailing /#
def fixDirName(dirpath):
	if dirpath[-1] != '/':
		dirpath += '/'
	return dirpath





#Check if a directory exists, make it if needed#
def makeDir(dirpath):
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	return 0










#Import sample names from a text file, if specifying a subset to process#
def importSampleList(infile):
	if os.path.exists(infile):
		files = []
		with open(infile, 'r') as IN:
			for x in IN:
				if len(x.rstrip().split('\t')) > 1:
					files.append(x.rstrip().split('\t')[0])
				else:
					files.append(x.rstrip())
	else:
		errorText = '\nERROR: the specified sample name file does not exist, please fix\n\t' + infile + '\n'
		print(errorText)
		raise SystemExit
		
	return files





#Get a list of samples to run processing for a specific step of the pipeline on#
def getSampleList(folder, sampleArg, extension):
	#to process all samples in the input folder#
	fileList = [ x for x in os.listdir(folder) if extension in x.split('.') ]

	#to process a specific subset of samples#
	if sampleArg:
		sampleList = importSampleList(sampleArg)
		fileList = [ x for x in fileList if any(y in x for y in sampleList) ]
			
		if len(sampleList) != len(fileList):
			errorText = '\nERROR: ' + str(len(fileList)) + ' samples exist for processing, but '
			errorText += str(len(sampleList)) + ' were specified in the sample list file, please fix any discrepancies\n'
			print(errorText)
			raise SystemExit

	fileList = [folder + x for x in fileList]	
	return fileList





#Import information about samples from a reference .txt file#
def importInfoFile(infoFile, columns, useFunction, skiprows=0):
	functionDict =	{
					'normalize': {'names': ('name', 'method', 'cells'), 'formats': ('S50', 'S50', 'int')},
					'normref': {'names': ('chrom', 'abspos', 'gc'), 'formats': ('S10', int', 'float')},
					'interpret': {'names': ('name', 'cells', 'group'), 'formats': ('S50', 'int', 'S50')}
					}
	
	if not infoFile:
		return functionDict[useFunction]
	
	if skiprows == 0:
		data = np.loadtxt(infoFile, usecols=columns, dtype=functionDict[useFunction])
	else:
		data = np.loadtxt(infoFile, usecols=columns, dtype=functionDict[useFunction], skiprows=skiprows)

	return data
		
		







		
###daemon to run multiprocessing and parallelize tasks###
def daemon(target, argList, name, cpuPerProcess=1):
	print( str( '\t' + str(len(argList)) + ' processes to run to ' + name ) )
	numCPU = mp.cpu_count()
	numWorkers = min( [int(numCPU / cpuPerProcess), len(argList)] )


	pool = mp.Pool(numWorkers)
	processes = [pool.apply_async(target, args=x) for x in argList]
	pool.close()

	for i,j in enumerate(processes):
		j.wait()

		if not j.successful():
			pool.terminate()

			print '\n\n\nprocessing failed, getting traceback now...'
	
			p = mp.Process(target=target, args=argList[i])
			p.start()
			p.join()
	#	else:
	#		print( str( '\t\t' + str(i+1) + ' of ' + str(len(argList)) + ' processes complete' ) )

	print( str( '\tAll processing to ' + name + ' complete\n' ) )

	
	
	
	
	
	
	
	
	
def zipping(filepath, gunzip=True):
	if filepath.split('.')[-1] != 'gz' and gunzip:
		return filepath
	elif filepath.split('.')[-1] == 'gz' and not gunzip:
		return filepath
	
	if gunzip:
		cmd = 'gunzip ' + filepath
		fixname = filepath[:-3]
	else:
		cmd = 'gzip ' + filepath
		fixname = filepath + '.gz'
	
	cmd = shlex.split(cmd)
	p = sub.Popen(cmd)
	p.wait()
	
	return fixname
	
	
	
	
	
	
	
	
	
	
