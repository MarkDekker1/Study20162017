#!/usr/bin/env python

__version__ = "Time-stamp: <2010-12-27 17:42 yannick@lyopc469>"
__author__ = "Yannick Copin <yannick.copin@laposte.net>"

"""
Taylor diagram (Taylor, 2001) test implementation.

http://www-pcmdi.llnl.gov/about/staff/Taylor/CV/Taylor_diagram_primer.htm
"""

import numpy as NP

class TaylorDiagram(object):
    """Taylor diagram: plot model standard deviation and correlation
    to reference (data) sample in a single-quadrant polar plot, with
    r=stddev and theta=arccos(correlation).
    """

    def __init__(self, refsample):
        """refsample is the reference (data) sample to be compared to."""

        self.ref = NP.asarray(refsample)

    def setup_axes(self, fig, rect=111):
        """Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using mpl_toolkits.axisartist.floating_axes.

        Wouldn't the ideal be to define its own non-linear
        transformation, so that coordinates are directly r=stddev and
        theta=correlation? I guess it would allow 
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = NP.concatenate((NP.arange(10)/10.,[0.95,0.99]))
        tlocs = NP.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))

        ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0,NP.pi/2, # 1st quadrant
                                                     0,1.5*self.ref.std()),
                                           grid_locator1=gl1,
                                           tick_formatter1=tf1,
                                           )

        ax = FA.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        ax.axis["left"].set_axis_direction("bottom") # "X axis"
        ax.axis["left"].label.set_text("Standard deviation")

        ax.axis["right"].set_axis_direction("top")   # "Y axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")

        ax.axis["bottom"].set_visible(False)         # Useless
        
        # Grid
        ax.grid()

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        print("Reference std:", self.ref.std())
        self.ax.plot([0],self.ref.std(),'ko', label='_')
        t = NP.linspace(0,NP.pi/2)
        r = NP.zeros_like(t) + self.ref.std()
        self.ax.plot(t,r,'k--', label='_')

        return self.ax

    def get_coords(self, sample):
        """Computes theta=arccos(correlation),rad=stddev of sample
        wrt. reference sample."""

        std = NP.std(sample)
        corr = NP.corrcoef(self.ref, sample) # [[1,rho],[rho,1]]
        theta = NP.arccos(corr[0,1])

        print("Sample std,rho:",std,corr[0,1])

        return theta,std

    def plot_sample(self, sample, *args, **kwargs):
        """Add sample to the Taylor diagram. args and kwargs are
        directly propagated to the plot command."""

        t,r = self.get_coords(sample)
        l, = self.ax.plot(t,r, *args, **kwargs) # (theta,radius)

        return l


if __name__=='__main__':

    import matplotlib.pyplot as PLT

    v_meas=v0vec
    time_end=timevec/3600.
    
    x = time_end
    data = v_meas

    dia = TaylorDiagram(data)
    
    fig = PLT.figure(figsize=(10,4))
    #ax1 = fig.add_subplot(1,2,1, xlabel='X', ylabel='Y')
    ax2 = dia.setup_axes(fig, 111)
    ldavec=[0.00015,0.0002,0.00022, 0.0003, 0.0005, 0.001,0.01,0.1]
    #ldavec=[0.001,0.002]
    #ax1.plot(x,data,'ko', label='Data')
    #ax1.plot(x,m1,'b-', label='Model 1')
    colors=np.linspace(0,100,len(ldavec))
    colormap = PLT.cm.jet
    PLT.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(ldavec))])
    legendEntries=[]
    legendText=[]
    for i in range(0,len(colors)):
        lda=ldavec[i]
        for t in range(1,np.int(tmax/dt)):
            pgrady0=pgrady[t]#M*np.cos(omega*t+theta/360.*2.*np.pi)
            pgradx0=pgradx[t]#A*np.cos(omega*t+phi/360.*2.*np.pi)+B
            
            vg=1/(rhoc*f)*pgradx0
            ug=-1./(rhoc*f)*pgrady0
            
            vvec_all[t]=vvec_all[t-1]+(-f*(uvec_all[t-1]-ug)-lda*vvec_all[t-1])*dt
            uvec_all[t]=uvec_all[t-1]+(f*(vvec_all[t]-vg)-A*np.cos(omega*t+phi/360.*2.*np.pi)/rhoc-lda*uvec_all[t-1])*dt

        m1=vvec_all[0:172800:3600]
        plotje=dia.plot_sample(m1, 'o',markersize=15)
        legendEntries.append(plotje)
        legendText.append(np.str(ldavec[i]))
    
    #lgd = PLT.legend(legendEntries,legendText,numpoints=1,loc='upper right') # example of how to draw the legend     
    
    #PLT.legend(['','','0.0001','0.0002','0.00022','0.0003','0.0005','0.001','0.01','0.1'], loc='best')

    PLT.show()