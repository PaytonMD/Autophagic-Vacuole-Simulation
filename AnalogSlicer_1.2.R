# Take a slice of a virtual vacuole
# input = input text file, in Spheregen format, with the first line as a vacuole.  
# balls - ball locations
# r - ball radii
# z - location (in z dimension) of slice - 
# T - slice thickness
# calculates the maximum radius of each ball that is caught in the slice
slice1 = function(input, T = 5, vacmin = 50) {
   inputfile = read.table(input, sep = " ")  
   r = inputfile [2:nrow(inputfile),1] # creates a vector of the radii of all of bodies
   upside_down_balls = t(inputfile[2:nrow(inputfile),2:4])
   balls = apply(upside_down_balls, 2, rev) # locations of the bodies, with each column a body, and then the rows the (x, y, z) coordinates, top to bottom
   scale = inputfile[1,1] # takes the scale from the size of the vacuole
   z = inputfile[1,2] # takes the plane through which to slice from the center of the vacuole
   cellSize = 2*scale
   #zbound = scale-sqrt(scale^2-vacmin^2)
   #z = (runif(1, min=(0+zbound), max=(cellSize-zbound)))  Random Z, with bounds that guarranty that a slice of the vacuole at least vacmin large is cut.  But for now I'm just putting Z through the origin for reproducibility
   RR = NULL
   for (j in 1:length(r)) {
      # loops for the number of balls
      zoffset = abs(balls[3,j] - z)
      # the distance between the slice and the center of the ball
      if (zoffset < T/2) {
         # the center of the ball is in the slice
         rr = r[j] 
      }
      else if ((zoffset-T/2) < r[j]) {
         # in this case, the ball is cut by the edge of the slice
         rr = sqrt(r[j]^2-(zoffset-T/2)^2) 
         # the crossectional radius of the ball at the edge of the slice
      }
      else rr = 0
      # if the ball isn't in the slice
      RR = c(RR,rr)
   }
   
   list(rrmax=RR)
}

# Seems to work, but test more.  
# balls = matrix(c(110, 110, 110, 45, 50, 55), nrow = 3)
# r = c(40, 20)
# scale = 110
# z = 110