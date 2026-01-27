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

def savefig(name, **kwargs):
    for possible_location in ['/work/bb1152/u290372/REA_post/plots/heat_wEU_JJA/', '/home/peterp/Dokumente/0_paper-drafts/rea_heat_summer_weu_overleaf/figures/']:
        if os.path.isdir(possible_location):
            out_fl = f"{possible_location}/{name}"
            break
    os.makedirs('/'.join(out_fl.split('/')[:-1]), exist_ok=True)
    plt.savefig(f"{out_fl}.pdf", **kwargs)
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

# https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def format_sig_plain(x, sig=2):
    s = f"{x:.{sig}g}"
    if "e" in s or "E" in s:
        x = float(s)
        if x.is_integer():
            return str(int(x))
        return str(x)
    return s