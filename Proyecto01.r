# librerías
library(repmis)
library(ggplot2)
library(lattice)

mlc <- function(N, x0, a, c, m){
  list1 <- rep(0,N)
  list1[1] <- x0
  for (i in 2:N) list1[i] <- (a*list1[i-1]+c)%%m
  r <- list1/m
  return(r)
}

seq 

mlc(N = 10, x0 = 6, a = 32, c = 3, m = 80)

#Cargar tabla ejemplo
titulo <- c("x")
test <- read.table(file= "/Users/macbookpro/Documents/R/chi_data.txt",header=FALSE,sep = " " ,col.names = titulo)
data_frame <- data.frame(test)

print(data_frame)

# Cargar intervalos
testIntervalos <- read.table(file = "/Users/macbookpro/Documents/R/intervalos.txt")
intervalosData_frame <- data.frame(testIntervalos)


tablaIntervalos <-table(cut(data_frame$x,breaks = 10))
IT = format(tablaIntervalos,digits = 5)
IntervalTable <- data.frame(IT)
print(IntervalTable)

ejemplo <- table(cut_interval(0:1,10))

ejemplo                

