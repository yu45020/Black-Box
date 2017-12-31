## Black-Box

Small tools to make research process easier.

### Life is short
* [MplDecorator](https://github.com/yu45020/MplDecorator) Customize Matplotlib parameters to create publication quality plots for  LaTex use. 

*  [Timeit Decorator](https://github.com/yu45020/Black-Box/blob/master/Tools/Python/TimeitDecorator.py): Store, display, format, and write run times for functions.

* [Clean LaTex aux](https://github.com/yu45020/Black-Box/blob/master/Tools/Python/latex_clear_aux.py) Automatically clean or hide LaTex aux while compiling. [Setup in TexStudio](https://user-images.githubusercontent.com/28139045/34075823-ba1e856c-e287-11e7-9001-34ff57864f7f.JPG)


* [Splite CSV](https://github.com/yu45020/Black-Box/blob/master/Tools/Python/spliteCSV.py) Splite large CSV file into several smaller files. Data are loaded by chunks (default is 150 MB) to maintain memory usage. It is used with RevoscaleR to transform large dataset (say, several GB CSV). 


### R
* [encodedummy](https://github.com/yu45020/encodedummy) Rely on data.table to fast encode non-numeric variables and transform them into dummy columns. It is used in processing data for Ridge/Lasso regressions in glmnet package, which only accept numeric matrces.  

* [Add Recessions in ggplots](https://github.com/yu45020/Black-Box/tree/master/Tools/R/plotting%20recession) From [R-bloggers post](https://www.r-bloggers.com/use-geom_rect-to-add-recession-bars-to-your-time-series-plots-rstats-ggplot/). Add US recession data (csv) and a self-defined plotting function.
