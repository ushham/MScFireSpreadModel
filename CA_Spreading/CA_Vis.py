import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, colorConverter
from matplotlib.animation import FuncAnimation
from matplotlib import animation

def HeatMap(arr, background, k, save):
    figure = plt.figure()

    #include background in image
    if background.any() != None:
        for i in range(arr.shape[0]):
            arr[i, :, :] += background

    ca_plot = plt.imshow(arr[0, :, :], cmap='seismic', interpolation='bilinear', vmin=0, vmax=(k - 1))
    plt.colorbar(ca_plot)
    transparent = colorConverter.to_rgba('black', alpha=0)
    wall_colormap = LinearSegmentedColormap.from_list('my_colormap', [transparent, 'green'], 5)


    def animation_func(i):
        n = i % arr.shape[0]
        ca_plot.set_data(arr[n, :, :])
        return ca_plot



    ani = FuncAnimation(figure, animation_func, interval=1000, save_count=arr.shape[0])
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    if save != None:
        writer = animation.FFMpegWriter(fps=30)
        ani.save(save + ".mp4", writer=writer)
    else:
        plt.show()