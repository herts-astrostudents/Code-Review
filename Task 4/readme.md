# BPT classifications

BPT diagrams are used to classify galaxies into star-forming or AGN (among other things).
The BPT diagram is formed of two line ratios. The y-axis is the logarithm of the OIII line flux over the Hbeta line flux and the x-axis is the logarithm of NII over Halpha. 
There is a line you can draw which is meant to separate the AGN branch from the star-forming branch. (see diagram)

![BPT diagram](https://astrobites.org/wp-content/uploads/2011/10/Fig2.jpg "BPT")

The task is to write a function in `solution.py` called `solution`. `solution` should classify objects based on what side of the line they are on and whether all relevant lines are detected at 5 sigma. 

The function `solution` should take an `astropy.table.Table` with the following columns:

    OIII_FLUX
    NII_6584_FLUX
    H_BETA_FLUX
    H_ALPHA_FLUX
    OIII_FLUX_ERR
    NII_6584_FLUX_ERR
    H_BETA_FLUX_ERR
    H_ALPHA_FLUX_ERR
    OIII_FLUX_SNR
    NII_6584_FLUX_SNR
    H_BETA_FLUX_SNR
    H_ALPHA_FLUX_SNR


The function `solution` should return an `astropy.table.Table` with the following columns:


    OIII_FLUX
    NII_6584_FLUX
    H_BETA_FLUX
    H_ALPHA_FLUX
    OIII_FLUX_ERR
    NII_6584_FLUX_ERR
    H_BETA_FLUX_ERR
    H_ALPHA_FLUX_ERR
    OIII_FLUX_SNR
    NII_6584_FLUX_SNR
    H_BETA_FLUX_SNR
    H_ALPHA_FLUX_SNR
    BPT_Y  # y axis of the BPT diagram
    BPT_X  # x axis of the BPT diagram
    is_5_sigma  # is the source detected at 5 sigma in all lines?
    BPT_class  # what classification is the source according to BPT ('starforming', 'AGN')


When you run `python run.py`, it will try to plot a BPT diagram based on what you have written in `solution.py`. Have a look at the code to see what it's doing.

*Don't change `run.py`, that is cheating!*

Be aware, these classification lines have asymptotes and so they go to infinity at a certain point. Take this into account.


There is a third classification that can be made from the BPT diagram: composite objects. They lie between star-forming objects and AGN (in grey in the figure above). You can classify these objects as well (using the lines `log_OIII_Hb_NII_lower` and `log_OIII_Hb_NII_upper`) if you dare!