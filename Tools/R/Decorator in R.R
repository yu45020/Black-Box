# Create decorator functions. The usage is similar to Python syntax
`%@%` = function(decorator, fn){
  return(decorator(fn))
}

time_decorator = function(fn,...){
  wrapper = function(...){
    start_t = Sys.time()
    return_fn = fn(...)
    end_t = Sys.time()
    print(sprintf("Runtime: %.2f seconds",end_t-start_t))
    return(return_fn)
  }
  return(wrapper)
}


  


fn1 = time_decorator %@% function(x){
  Sys.sleep(0.1)
  return(x)
}

fn1(1)


#### Error Handler 

error.decorator = function(fn,...){
  # record error message
  error.log = function(c){
    msg = conditionMessage(c)
    return(msg)
  }
  
  wrapper = function(...){
    result = tryCatch(
      fn(...), # try the function
      error = error.log #if error -->> record message
      )
    return(result)
  }
  
  return(wrapper)
}

divi = error.decorator  %@%  function(x,y){
  print("======")
  print("Start")
  Sys.sleep(0.1)
  result = x/y
  return(result)
}


divi(1,"as")

# Double decorator 
divi2 = time_decorator %@% divi
divi2(1,"as")
