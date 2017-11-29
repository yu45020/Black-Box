library(data.table)
library(parallel)
stime = Sys.time()

num = 10^5

test_draw = function(){
  # draw cards and count number of ones
  # turn white ---> black if distance of ones >32
  df = sample(x=c(0,1),size=num, replace=TRUE,prob=c(0.97,0.03))
  df = data.table(N = seq(1,num),draw=df)
  ones = df[draw==1,.N]
  
  get_one_location = df[draw==1,.(N)]
  first = get_one_location[1]
  diff_one_location = get_one_location[,N:=N-shift(N,type='lag', n=1L)]
  diff_one_location[1] = first
  
  turn_black = diff_one_location[,N%/%33]
  blacks = sum(turn_black)+ones
  return(blacks/num)
}

# prepare for parallel computing
no_cores = detectCores()
cl=makeCluster(no_cores)
clusterExport(cl,c('test_draw','num'))
clusterEvalQ(cl,library(data.table))

# go parallel
results = parLapply(cl,1:100,
                    fun = function(x)test_draw())
mean(unlist(results))
Sys.time()-stime

stopCluster(cl)
