#!/usr/bin/python
def usage():
    import sys
    print """
        ###########
        splitndgrid
        ###########       
        
        Program to read an ASCII list of scattered points in nD space and bin 
        them into files representing bins on an N-dimesional cartesian grid. A 
        border may defined around each bin, where border width is constant for 
        each dimension. Borders of adjacent bins may overlap so that points may
        be binned into more than one bin.
        
        Usage:
            
            splitndgrid INFILE OUTPATH NDIMS MINS MAXS BINSIZE BORDERSIZE
                    
        Arguments:
            
            INFILE - Path to the ASCII source file containing the points. Each
                     record must be formatted: D1 D2...DN\\n  where e.g. D1 is
                     the position of the point in dimension 1. Note that fields
                     are whitespace separated and each record is terminated with
                     a newline character.
            
            OUTPATH - The output path. Output file names for each bin on the 
                      grid are made by suffixing OUTPATH with a string made of
                      underscore-separated bin numbers (which start at 0).
            
            NDIMS   - The number of dimensions, the first n fields to
                      read from each line in INFILE that describe the location
                      of the point.
            
            MINS    - Comma separated string containing the minimum values of the
                      grid to bin onto for dimensions 1..n.
                      
            MAXS    - Comma separated string containing the maximum values of the
                      grid to bin onto for dimensions 1..n.
            
            BINSIZE - Comma separated string containing the bin widths for each
                      dimension.
            
            BORDERSIZE - Comma separated string containing the border widths for 
                         each dimension.
            
        Example:
            
            To bin a list of points on a lat lon grid where each record contains
            the fields:
                LAT LON ALTITUDE
            
            We only want to bin the records into 5x5 degree lat lon bins. The 
            altitude field is propagated into the binned files. We assign no
            border in the longitude direction, but one of 0.02 degrees in the 
            latitude direction.
            
            splitndgrid globalelev.txt ~/elevbins/bin_ 2 -90,0 90,360 5,5 0.02,0
            
            Note that points may be in more than one bin in the latitude 
            direction, because the 0.02 degree borders of adjacent bins overlap
            in that dimension.
            
            This example will produce 2592 files from:
                    ~/elevbins/bin_01_01.txt
                to:
                    ~/elevbins/bin_36_72.txt
                
        Author: Elliot Sefton-Nash  (e.sefton-nash@uclmail.net)  
        
        Changelog: 
            2014-01-13 Original       
    """
    sys.exit()


def warn(msg):
    import sys    
    print >> sys.stderr, 'splitndgrid: WARNING // '+msg


def error(msg):
    import sys    
    print >> sys.stderr, 'splitndgrid: ERROR // '+msg
    sys.exit()


def parseArgs(argv):
    argnames = ('INFILE','OUTPATH','NDIMS','MINS','MAXS','BINSIZE','BORDERSIZE')
    for i,a in enumerate(argv):
        if i == 2:
            try:
                exec(argnames[i]+'=int(a)')                
            except:
                usage()

        elif i>2:
            # At this point nDims has been defined, if it doesn't equal the size
            # of mins, maxs, binSize and buffs then error.
            try:
                exec(argnames[i]+'=[float(s) for s in a.split(\',\')]')
            except:
                usage()
            exec('thisLen=len('+argnames[i]+')') 
            if thisLen != NDIMS:
                error(argnames[i]+' must have NDIMS elements')
            
        elif i<2:
            exec(argnames[i]+'=a')

    return (INFILE,OUTPATH,NDIMS,MINS,MAXS,BINSIZE,BORDERSIZE)


def doBin(infilepath,outstem,nDims,mins,maxs,binSize,buffs):    
    
    print infilepath,outstem,nDims,mins,maxs,binSize,buffs
    
    import numpy as np
    import itertools
    
    lowers,uppers = [],[]
    for id in range(nDims):
        # Vector of bin boundaries for each dimension, including buffers
        tmp=np.arange(mins[id],maxs[id],binSize[id])
        lowers.append(tmp-buffs[id])
        uppers.append(tmp+binSize[id]+buffs[id])
    
    # Make two lists containing filenames and  tuples of coordinates in the grid
    shapearg = ','.join( [ 'range('+str(len(lowers[i]))+')' for i in range(nDims) ] )
    fPath,gridCoords = [],[] # Lists of file paths and objects
    for thisBin in eval('itertools.product('+shapearg+')'):
        fPath.append(outstem+'_'.join([ str(thisBin[i]+1) for i in range(len(thisBin)) ])+'.txt')
        gridCoords.append(thisBin)
    
    openFileList,fObj = [],[]
    
    try:
        fin = open(infilepath,'r')
    except IOError:
        error('Unable to open '+infilepath)
    
    for line in fin:
        
        # Get numbers out of line
        vec = map(float, line.strip().split())[0:nDims]
        
        # For each dimension, which bins is it in?
        inBins=[]
        for id in range(nDims):
            inBins.append(np.where((vec[id] >= lowers[id]) & (vec[id] < uppers[id]))[0])
    
        # For every bin that the grid cell is in. Similar itertool trick to what we used 
        # for file opening.
        argStr = ','.join( [ 'inBins['+str(i)+']' for i in range(nDims) ] )
        for thisBin in eval('itertools.product('+argStr+')'):

            # Returns file name for this record.
            thisfPath = fPath[gridCoords.index(thisBin)] 
            
            # If the list file objects doesn't contain the path then file isn't 
            # open. Open it.
            if not openFileList.__contains__(thisfPath):
            
                # Add file object to list
                openFileList.append(thisfPath)                     
                fObj.append( open(thisfPath,'w'))

            # Write the record to the appropriate file.            
            fObj[openFileList.index(thisfPath)].write(line)
            
    # Close all open files
    fin.close()
    for thisfObj in fObj:
        thisfObj.close()


if __name__ == '__main__':

    import sys
    
    if len(sys.argv) != 8:
        usage()

    infilepath,outstem,nDims,mins,maxs,binSize,buffs = parseArgs(sys.argv[1:])         
    doBin(infilepath,outstem,nDims,mins,maxs,binSize,buffs)
