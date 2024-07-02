from typing import List, Union
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os


def plot_maps(maps_list: List[np.array], save_img_path: Union[str, None, os.PathLike] = None) -> None:
    """
    Plot a list of maps.

    Args:
        maps_list (List[np.array]): List of maps to plot. Each map is a 2D numpy array.
        save_img_path (Union[str, None, os.PathLike], optional): Path to save the image. Defaults to None.
    """
    rows = int(np.ceil(np.sqrt(len(maps_list))))
    fig, axs = plt.subplots(rows, rows, figsize=(20, 20))
    cmap = colors.ListedColormap(['white','black'])
    if len(maps_list) > 1:
        for i in range(rows**2):
            axs[i//rows, i%rows].axis('off')
            if i < len(maps_list):
                axs[i//rows, i%rows].pcolor(maps_list[i], cmap=cmap, edgecolors='gray', linewidths=1)
    else:
        axs.axis('off')
        axs.pcolor(maps_list[0], cmap=cmap, edgecolors='gray', linewidths=1)
    plt.tight_layout()
    if save_img_path is not None:
        fig.savefig(save_img_path)
    plt.show()
    plt.close(fig)



def plot_map(map: np.array, save_img_path : Union[str, None, os.PathLike] = None) -> None:
    """
    Plot a single map.

    Args:
        map (np.array): Map to plot. A 2D numpy array.
        save_img_path (Union[str, None, os.PathLike], optional): Path to save the image. Defaults to None.
    """

    plot_maps([map], save_img_path)