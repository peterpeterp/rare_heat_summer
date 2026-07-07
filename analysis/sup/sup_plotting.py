import os
import matplotlib
import matplotlib.pyplot as plt
import cartopy
import matplotlib.units as munits
from matplotlib.dates import ConciseDateConverter
import seaborn as sns
import distinctipy

from mpl_toolkits.axes_grid1.inset_locator import inset_axes



import numpy as np

matplotlib.rcParams['savefig.bbox'] = 'standard'
matplotlib.rcParams['scatter.marker']='.'

from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

def savefig(name, also_png=True, **kwargs):
    for possible_location in ['PATH_TO_SPECIFY']: # specify where to store plots
        if os.path.isdir(possible_location):
            out_fl = f"{possible_location}/{name}"
            break
    os.makedirs('/'.join(out_fl.split('/')[:-1]), exist_ok=True)
    plt.savefig(f"{out_fl}.pdf", **kwargs)
    if also_png:
        plt.savefig(f"{out_fl}.png", dpi=600, **kwargs)


def plot_table(t, cmap='RdBu_r', centered=True, lim=None):
    vals = np.array(t.values, float).round(2)
    if lim is not None:
        norm = plt.Normalize(*lim)
    else:
        if centered:
            maxabs = np.max(np.abs(vals))
            norm = plt.Normalize(-maxabs, maxabs)
        else:
            norm = plt.Normalize(vals.min(), vals.max())
    colours = matplotlib.cm.get_cmap(cmap)(norm(vals))
    fig = plt.figure(figsize=(t.shape[0], t.shape[1] / 3))
    ax = fig.add_subplot(111, frameon=False, xticks=[], yticks=[])
    the_table = plt.table(cellText=vals, rowLabels=t.index, colLabels=t.columns, 
                            #colWidths = [0.1] * t.shape[1], 
                            loc='center', 
                            cellColours=colours)
    plt.tight_layout()
    return fig,ax


def fix_violin(violin_parts, color):
    for pc in violin_parts['bodies']:
        pc.set_facecolor(color)
        pc.set_edgecolor('none')
    for partname in ('cbars','cmins','cmaxes'):
        vp = violin_parts[partname]
        vp.set_edgecolor('none')

def format_sig_plain(x, sig=2):
    s = f"{x:.{sig}g}"
    if "e" in s or "E" in s:
        x = float(s)
        if x.is_integer():
            return str(int(x))
        return str(x)
    return s