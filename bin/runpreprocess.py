#!/usr/bin/python
import os

from preprocess import trimfile
import common 










def runAll(args):
	
	print('\n\n\nYou have requested preprocess (trim) fastq files')
	print('\tWARNING:')
	print('\t\tIF USING ANY LENGTH OTHER THAN 36 BP, REFERENCE FILES ARE NOT SUPPORTED FOR DOWNSTREAM PROCESSING')
	print('\n')
	

	#make sure environment is properly prepared#
	args.FastqDirectory = common.fixDirName(args.FastqDirectory)
	if not args.remove:
		common.makeDir(args.FastqDirectory + '/FullLength/')

	
		
	#get list of fastq files to process (depending on args.samples)
	fastqFiles = common.getSampleList(args.FastqDirectory, args.samples, 'fastq')
	
	
	
	#use the daemon to and preprocessing code to trim all fastq files with parallel processing
		
	if args.remove:
		argList = [(x, args.trim5, args.length, remove=True,) for x in fastqFiles]
	else:
		argList = [(x, args.trim5, args.length,) for x in fastqFiles]
		
	common.daemon(trimfile.preprocessOne, argList, 'trim sequencing reads to desired length', cpuPerProcess=1)
		
	
	
	print('\nPre-processing complete\n\n\n')

