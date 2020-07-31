import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, colorConverter
from matplotlib.animation import FuncAnimation

def HeatMap(arr, k):
    figure = plt.figure()

    ca_plot = plt.imshow(arr[0, :, :], cmap='seismic', interpolation='bilinear', vmin=0, vmax=(k - 1))
    plt.colorbar(ca_plot)
    transparent = colorConverter.to_rgba('black', alpha=0)
    wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'green'], 5)


    def animation_func(i):
        n = i % arr.shape[0]
        ca_plot.set_data(arr[n, :, :])
        return ca_plot



    animation = FuncAnimation(figure, animation_func, interval=1000)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()