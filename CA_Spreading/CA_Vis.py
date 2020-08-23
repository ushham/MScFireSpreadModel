import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, colorConverter
from matplotlib.animation import FuncAnimation
from matplotlib import animation

class Visualisation:
    def __init__(self, arr, back, k, save):
        self.arr = arr
        self. bkground = back
        self.k = k
        self.saveloc = save

    def HeatMap(self):
        figure = plt.figure()

        #include background in image
        if self.bkground.any() != None:
            for i in range(self.arr.shape[0]):
                self.arr[i, :, :] += self.bkground

        ca_plot = plt.imshow(self.arr[0, :, :], cmap='seismic', interpolation='bilinear', vmin=0, vmax=(self.k - 1))
        plt.colorbar(ca_plot)
        transparent = colorConverter.to_rgba('black', alpha=0)
        wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'green'], 5)


        def animation_func(i):
            n = i % self.arr.shape[0]
            ca_plot.set_data(self.arr[n, :, :])
            return ca_plot

        ani = FuncAnimation(figure, animation_func, interval=1000, save_count=self.arr.shape[0])
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        if self.saveloc != None:
            writer = animation.FFMpegWriter(fps=30)
            ani.save(self.saveloc + ".mp4", writer=writer)
        else:
            plt.show()


    #def OneDim(self, rc, num):

    def TimeSnips(self):
        figure = plt.figure()
        ca_plot = plt.imshow(self.arr, cmap='seismic', interpolation='bilinear', vmin=0, vmax=(self.k - 1))
        plt.colorbar(ca_plot)
        #ca_plot.set_data(self.arr)
        plt.show()