#!/usr/bin/python
import argparse










###basic parser for parent help statement###
def parentArgs():

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
		description='''\
	Suzanne's pipeline to identify somatic CNVs from single-cell whole-genome sequencing data
	=========================================================================================

	You must specify a function to perform:
	  *preprocess (trim fastq reads to the appropriate length)
	  *[More functions coming soon]
		''')

	parser.print_help()

	raise SystemExit









###interpret arguments needed to perform preprocessing of fastq files###
def preprocessArgs():

	parser = argparse.ArgumentParser(description='Trim fastq reads to the appropriate length')

	#required arguments#
	parser.add_argument('FastqDirectory', 
		help = 'The path to the folder that contains fastq files to be processed')
	
	#optional arguments#
	parser.add_arugment('-5', '--trim5', metavar='X', type=int, default=0,
		help = "Number of 5' bases to trim from fastq reads")
	parser.add_arugment('-l', '--length', metavar='X', type=int, default=36,
		help = 'The desired read length')
	parser.add_arugment('-r', '--remove', action='store_true'
		help = 'Set this flag if you want to delete the full length fastq files')
	parser.add_argument('-s', '--samples', metavar='/path/to/sample_list.txt', default=False,
		help='Path to a file containing a list of fastq files to be processed\n\tsample names only, no path or file extension needed')










###interpret arguments needed to perform mapping of fastq files###
def mapArgs():
	
	parser = argparse.ArgumentParser(description='Map fastq files to the appropriate reference genome')

	#required arguments#
	parser.add_argument('FastqDirectory', 
		help = 'The path to the folder that contains fastq files to be processed')
	parser.add_argument('species', choices=['hg38', 'mm10'], 
		help = 'The genome build of the species being assessed')
	
	#optional arguments#
	parser.add_arugment('-t', '--trim', metavar='X', nargs=2, type=int, default=[0, 0],
		help = "Number of 5' and 3' bases to trim from fastq reads during mapping")
	parser.add_arugment('-o', '--output', metavar='/path/to/output_directory/', default=False,
		help = 'A filepath to the desired directory where you would like sam files saved, if not in the same parent directory as the fastq files')
	parser.add_arugment('-x', '--statdir', metavar='/path/to/statistics_directory/', default=False,
		help = 'A filepath to the desired directory where you would like mapping statistics saved, if not in the same parent directory as the fastq files')
	parser.add_argument('-s', '--samples', metavar='/path/to/sample_list.txt', default=False,
		help='Path to a file containing a list of fastq files to be processed\n\tsample names only, no path or file extension needed')
	
	

	





###interpret arguments needed to perform counting of unique.sam files###
def countArgs():
	
	parser = argparse.ArgumentParser(description='Count the reads per genomic bin from unique sam files')

	#required arguments#
	parser.add_argument('SamDirectory', 
		help = 'The path to the folder that contains unique.sam files to be processed')
	parser.add_argument('species', choices=['hg38', 'mm10'], 
		help = 'The genome build of the species being assessed')
	
	#optional arguments#
	parser.add_arugment('-o', '--output', metavar='/path/to/output_directory/', default=False,
		help = 'A filepath to the desired directory where you would like bincount.txt files saved, if not in the same parent directory as the sam files')
	parser.add_arugment('-x', '--statdir', metavar='/path/to/statistics_directory/', default=False,
		help = 'A filepath to the desired directory where you would like mapping statistics saved, if not in the same parent directory as the sam files')
	parser.add_argument('-s', '--samples', metavar='/path/to/sample_list.txt', default=False,
		help='Path to a file containing a list of unique.sam files to be processed\n\tsample names only, no path or file extension needed')

	
	
	
	
	
	
	
	
	
###interpret arguments needed to perform normalization and segmentation of bincounts.txt files###
def segmentArgs():
	
	parser = argparse.ArgumentParser(description='Normalize and segment bincounts files to begin CNV identification process')

	#required arguments#
	parser.add_argument('CountDirectory', 
		help = 'The path to the folder that contains bincounts.txt files to be processed')
	parser.add_argument('species', choices=['hg38', 'mm10'], 
		help = 'The genome build of the species being assessed')
	
	#optional arguments#
	parser.add_arugment('-o', '--output', metavar='/path/to/output_directory/', default=False,
		help = 'A filepath to the desired PARENT directory where you would like lowess.txt and segments.txt files saved, if not in the same parent directory as the bincounts files')
	parser.add_argument('-i', '--infofile', metavar='/path/to/sample.info.txt', default=False,
		help='Path to a .txt file containing information about the samples to be processed (unique name, amplification method, number of cells)\n\tIf not all are identical. This file should not have a header row')
	parser.add_argument('-c', '--columns', metavar='X X X', default=[0, 1, 2], type=int, nargs=3,
		help='The zero-indexed locations of the columns to import from the infofile in the order: name, method, cell number (if not the first 3 columns)')
	parser.add_arugment('-g', '--gconly', action='store_true'
		help = 'Set this flag if you only want GC-correction to be performed during normalization')
	parser.add_arugment('-n', '--normalizeonly', action='store_true'
		help = 'Set this flag if you do not want CBS to be performed')
	parser.add_argument('-s', '--samples', metavar='/path/to/sample_list.txt', default=False,
		help='Path to a file containing a list of bincounts.txt files to be processed\n\tsample names only, no path or file extension needed')

	
	
	
	
	
	
	
	
	
###interpret arguments needed to perform QC and CNV analysis of each single cell sample###
def interpretArgs():
	
	parser = argparse.ArgumentParser(description='Assess sample quality, filter unreliable CNVs, and generate user-friendly output')

	#required arguments#
	parser.add_argument('AnalysisDirectory', 
		help = 'The path to the folder to save output files')
	parser.add_argument('species', choices=['hg38', 'mm10'], 
		help = 'The genome build of the species being assessed')
	
	#optional arguments#
	parser.add_arugment('-f', '--nofilter', action='store_true'
		help = 'Set this flag if you do not want to perform FUnC filtering of low-quality CNV calls')
	parser.add_argument('-i', '--infofile', metavar='/path/to/sample.info.txt', default=False,
		help='Path to a .txt file containing information about the samples to be processed (unique name, number of cells, group)\n\tIf not all are identical. This file should not have a header row')
	parser.add_argument('-c', '--columns', metavar='X X X', default=[0, 1, 2], type=int, nargs=3,
		help='The zero-indexed locations of the columns to import from the infofile in the order: name, cell number, group (if not the first 3 columns)')
	parser.add_arugment('-l', '--lowess', metavar='/path/to/lowess.txt/files/', default=False,
		help = 'A filepath to the desired directory where all lowess.txt files are saved, if not AnalysisDirectory/Lowess/')
	parser.add_arugment('-g', '--segments', metavar='/path/to/segments.txt/files/', default=False,
		help = 'A filepath to the desired directory where all segments.txt files are saved, if not AnalysisDirectory/Segments/')
	parser.add_arugment('-r', '--countstats', metavar='/path/to/bincounts.stats.txt/files/', default=False,
		help = 'A filepath to the desired directory where all bincounts.stats.txt files are saved, if not AnalysisDirectory/PipelineStats/')	
	parser.add_argument('-s', '--samples', metavar='/path/to/sample_list.txt', default=False,
		help='Path to a file containing a list of sample names to be processed\n\tno path or file extension needed')

	
	
	
	
	

	
	
	
def fullParser(input):

	functionDict =	{ 
			'-h': parentArgs,
			'--help': parentArgs,
			'preprocess': preprocessArgs, 
			'map': mapArgs,
			'count': countArgs,
			'segment': segmentArgs,
			'interpret': interpretArgs,
			}

	
	
	if input == []:
		parentArgs()
		
	if input not in functionDict.keys():
		return input[0], False

	
	
	parser = functionDict[input[0]]()
	args = parser.parse_args(input[1:])

	return input[0], args









