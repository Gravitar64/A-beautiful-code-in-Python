import sys, math
  
def hilbert(x0, y0, xi, xj, yi, yj, n):
    if n <= 0:
        X = x0 + (xi + yi)/2
        Y = y0 + (xj + yj)/2
        
        # Output the coordinates of the cv
        print ('%s %s 0' % (X, Y))
    else:
        hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1)
        hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1)
        
def main():
    args = sys.stdin.readline()
    # Remain the loop until the renderer releases the helper...
    while args:
        arg = args.split()
        # Get the inputs
        pixels = float(arg[0])
        ctype = arg[1]
        reps = int(arg[2])
        width = float(arg[3])
        
        # Calculate the number of curve cv's
        cvs = int(math.pow(4, reps))
            
        # Begin the RenderMan curve statement
        print ('Basis \"b-spline\" 1 \"b-spline\" 1')
        print ('Curves \"%s\" [%s] \"nonperiodic\" \"P\" [' % (ctype, cvs))
    
        # Create the curve
        hilbert(0.0, 0.0, 1.0, 0.0, 0.0, 1.0, reps)
    
        # End the curve statement
        print ('] \"constantwidth\" [%s]' % width)
      
        # Tell the renderer we have finished   
        sys.stdout.write('\377')
        sys.stdout.flush()
        
        # read the next set of inputs
        args = sys.stdin.readline()
if __name__ == "__main__":
    main()