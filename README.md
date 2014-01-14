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

