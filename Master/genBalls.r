# This script contains functions for running the resim function either without clumping
# or with "type one" glpk clumping
library(MultiRNG)
library(tibble)
library(glpkAPI)
# r - vector of radii
# Generates positions for the bodies - first randomly positioned in a sphere, then clumped with compactSpheres
# now for genballs, enter number of bodies and vacuole radius. will output txt file with
# vacuole and bodies radii and x y z center locations in positive octant
genBalls = function(bodies=15, vacRad=1000, mu=5, sigma=0.2, iterations=4) {
  # Generate N points on a 3-dimensional unit sphere.
  r <- rlnorm(bodies, mu, sigma) # can change the 5 and 0.2 to change mean(mu) and std. dev(sigma) on norm log vacRad respectively
  N = length(r)
  X = generate.point.in.sphere (N,3)
  # generate random distances from the center, with maximum = vacrad
  D = runif(N)*vacRad
  # vacRad each point by the random distance, so that all are inside vacuole (sphere)
  pos = X*D
  # transpose matrix, so that rows are coordinates and columns are points, as required later
  tpos = t(pos)
  Y = t(pos)
  cellSize=2*vacRad
  R = r[1:N]
  for ( i in 1:iterations) {
    sol = suppressWarnings(compactSpheres(Y,R,Xmax=cellSize,Ymax=cellSize,Zmax=cellSize))
    Y = sol$pos
  }
  list1 <- list(R=R, orig=tpos,compact=Y, cellSize=cellSize)
  print (list1)
  compact <- t(list1$compact) 
  #translate all coordinates to the positive quadrant
  for (i in 1:ncol(compact)){
	compact[,i]=compact[,i]+(vacRad-mean(compact[,i]))}
  output_spheregen <- cbind(as.numeric(R), compact)
  output_spheregen <- rbind(cellSize/2, output_spheregen)
  print (output_spheregen)
  write.table(output_spheregen, "rData.txt", row.names = FALSE, col.names = FALSE)
}


# Clumping routine, to cluster all of the bodies together in the vacuole
#-- Simplex-based simulation of spheres in 3-space
compactSpheres = function(X,r,Xmax=1,Ymax=1,Zmax=1) {
  # Constrains
  require(glpkAPI)
  c2r <- system.file(package = "glpkAPI", "c2r.map")
  source(c2r)
  Xmin=Ymin=Zmin=0
  N = length(r)
  Nc2 = choose(N,2)
  prob = glp_create_prob()
  glp_add_cols(prob,3*N)
  for (i in 0:(N-1)) {
    glp_set_col_name(prob,i*3 + 1, paste("x",i+1,sep=""))
    glp_set_col_name(prob,i*3 + 2, paste("y",i+1,sep=""))
    glp_set_col_name(prob,i*3 + 3, paste("z",i+1,sep=""))
  }
  # (i) box constraints x+r <= Xmax (x - r) >= Xmin
  for (i in 1:N) {
    crow = glp_get_num_rows(prob)
    glp_add_rows(prob,6)
    glp_set_mat_row(prob,crow + 1,1,3*(i-1) + 1,1)
    glp_set_mat_row(prob,crow + 2,1,3*(i-1) + 2,1)
    glp_set_mat_row(prob,crow + 3,1,3*(i-1) + 3,1)
    glp_set_row_bnds(prob,crow+1,GLP_DB,Xmin+r[i],Xmax-r[i])
    glp_set_row_bnds(prob,crow+2,GLP_DB,Xmin+r[i],Xmax-r[i])
    glp_set_row_bnds(prob,crow+3,GLP_DB,Xmin+r[i],Xmax-r[i])
  }
  # (ii) collision constraints
  for (i in 1:N) {
    if (i < N)
      for (j in (i+1):N) {
        pi = X[,i]
        pj = X[,j]
        u = (pj - pi) / sqrt( (pj - pi) %*% (pj - pi) )
        a = matrix(0,nrow(X),ncol(X))
        a[,j] = u
        a[,i] = -u
        a = as.vector(a)
        crow = glp_get_num_rows(prob)
        glp_add_rows(prob,1)
        nz = which(a!=0)
        glp_set_mat_row(prob,crow + 1, length(nz),nz, -a[nz])
        glp_set_row_bnds(prob,crow+1, GLP_UP, 0,-(r[i] + r[j]))
      }
  }
  # (iii) distance constraints
  #
  glp_add_cols(prob,Nc2)
  ij = 1
  for (i in 1:N)
    if (i < N)
      for (j in (i+1):N) {
        pi = X[,i]
        pj = X[,j]
        u = (pj - pi) / sqrt( (pj - pi) %*% (pj - pi) )
        U = cbind(u, c(0,0,1),c(0,0,-1),c(0,1,0),c(0,-1,0),c(1,0,0),c(-
                                                                        1,0,0))
        for (k in 1:ncol(U)) {
          u = U[,k]
          a = matrix(0,nrow(X),ncol(X))
          a[,j] = u
          a[,i] = -u
          D = rep(0,Nc2)
          D[ij] = -1
          a = c(as.vector(a),D)
          crow = glp_get_num_rows(prob)
          glp_add_rows(prob,1)
          nz = which(a!=0)
          glp_set_mat_row(prob,crow + 1, length(nz),nz, a[nz])
          glp_set_row_bnds(prob,crow+1, GLP_UP, 0,0)
        }
        ij = ij + 1
      }
  for (i in 1:Nc2)
    glp_set_obj_coef(prob,3*N+i,1)
  for (i in 1: glp_get_num_cols(prob))
    glp_set_col_bnds(prob,i,GLP_FR,0,0)
  glp_simplex(prob)
  X = matrix(0,ncol=N, nrow=3)
  for (i in 1:(3*N))
    X[i]=glp_get_col_prim(prob,i)
  list(positions=X,status=glp_get_status(prob))
}

#Since it is easier to run just genBalls than calling a specific function, I've added a simple call to the genBalls function
#at the end of this file so that a call to genBalls.r automatically uses the genBalls function.
#Might capture arguments passed in and use them in the genBalls parameters.
setwd("C:\\Users\\Temp\\Desktop\\AVS\\Master")
genBalls()
