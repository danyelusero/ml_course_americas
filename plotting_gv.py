import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy import stats
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_squared_error
import pandas as pd
from sklearn.inspection import permutation_importance
from scipy.stats import gaussian_kde
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.model_selection import RepeatedKFold, cross_val_score
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib

def cat1_in_cat2(cat1, cat2, title):
    fig = plt.figure(figsize=(12,8))

    x_labels = np.unique(cat1)
    x_ticks = [i for i in range(len(x_labels))]

    u_cats2 = np.unique(cat2)

    heights_sum = np.zeros(len(x_labels))

    for idx, i in enumerate(u_cats2):
        cat2_filter = cat2 == i
        
        heights = []
        
        for j in x_labels:
            cat1_filter = cat1 == j
            both = np.logical_and(cat2_filter, cat1_filter)
            heights.append(np.sum(both))
        
        plt.bar(x_ticks, heights, label=i, bottom=heights_sum)
        heights_sum = heights_sum + np.array(heights)

    plt.xticks(x_ticks, x_labels, rotation='vertical')
    plt.ylabel('# samples')
    plt.title(title)
    plt.legend()

    #plt.savefig(outfl, bbox_inches='tight', facecolor='white')

def elbow_plot(kmin, kmax, vars_std):

    n_clus = np.arange(kmin, kmax, 1)

    n_clusters = [] 
    inercia = [] 

    for i in n_clus: 
        kmeans = KMeans(n_clusters=i).fit(vars_std) 
        n_clusters.append(i) 
        inercia.append(kmeans.inertia_)

    fig, ax = plt.subplots(figsize=(14,10))

    ax.plot(n_clusters, inercia, marker='o', color='blue', label='K - Clusters')
    ax.set(

    xlabel='N Clusters',
    ylabel='Inércia',
    title='N Clusters x Inercia'
    )
    #ax.grid(visible=True, linestyle='--')
    ax.set_xticks(n_clusters)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_facecolor('white')
    ax.legend(loc='upper right', frameon=False, fontsize=12, markerscale=2)
    plt.show()

def dendogram(vars, method='ward', metric='euclidean'):
    z = linkage(vars, method='ward', metric='euclidean')
    plt.figure(figsize=(15,8))
    ddg = dendrogram(z, no_labels=True, color_threshold=15)

def cluster_metrics(n_clus, metric1,metric2,metric3, metric4):

    fig, axs = plt.subplots(1,2, figsize=(15,5))


    axs[0].set_ylabel('Sillhouete Score')
    axs[0].set_xlabel('N clusters')
    axs[0].plot(n_clus, metric1, label='KMeans', marker='o', markersize=5)
    axs[0].plot(n_clus, metric2, label='Agglomerative', marker='o', markersize=5)
    axs[0].set_title('Valores próximos a zero indicam sobreposição de grupos\nValores maiores indicam resultados melhores')
    axs[0].grid()
    axs[0].legend()
    axs[0].set_xticks(np.arange(1, len(n_clus)+1, 1))


    axs[1].set_xticks(np.arange(1, len(n_clus)+1, 1))
    axs[1].set_ylabel('Davies-Bouldin')
    axs[1].set_xlabel('N clusters')
    axs[1].set_title('Valores próximos a zero indicam melhores resultados')
    axs[1].plot(n_clus, metric3, label='KMeans', marker='o', markersize=5)
    axs[1].plot(n_clus, metric4, label='Agglomerative', marker='o', markersize=5)
    axs[1].grid()
    axs[1].legend()

def locmap(x, y, v, cat, figsize, title):
    
    #criando a figura e os axis
    fig, ax = plt.subplots(figsize=figsize)

    #configurando o plot
    ax.set(
    title = title,
    xlabel = 'X (m)',
    ylabel='Y (m)',
    aspect = 'equal'
    )

    ax.minorticks_on()
    ax.grid(linestyle='--', which='major')

    #verificando se a variavel e categorica
    if cat:
        ncats = np.unique(v).size
        cat_labels = np.unique(v)

        #transformando categorias de alphanum para num
        catdic = {j:i for i,j in enumerate(cat_labels)} 
        catnum = v.map(catdic) 
        vlim = (0, ncats)

        catcmap = plt.cm.get_cmap('jet', ncats) #criando nossa propria escala de cores

        #plotando
        scatvu = ax.scatter(x, y, c=catnum, cmap=catcmap, vmin=vlim[0], vmax=vlim[1])
        
        #definindo escala de cores
        ticks_location = np.arange(ncats) + 0.5

        cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
        cbar = plt.colorbar(scatvu, cax=cax, label='Teor %') # Similar to fig.colorbar(scatvu, cax = cax)"""
        ticks_location = np.arange(ncats) + 0.5
        cbar.set_ticks(ticks_location)
        cbar.set_ticklabels(cat_labels)


    else:
        #plotando
        scatvu = ax.scatter(x, y, c=v, cmap='jet')

        #definindo escala de cores
        cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
        cbar = plt.colorbar(scatvu, cax=cax, label='Teor %') # Similar to fig.colorbar(scatvu, cax = cax)"""




    #salvando
    #plt.savefig(outfl, bbox_inches='tight', facecolor='white', dpi=300) 
def scatterplot(df, x_col, y_col, c=None, title=None, lineregress=True):
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if c is None:
        nan_filter = np.isfinite(df[y_col])
        x, y = df[x_col][nan_filter], df[y_col][nan_filter]
        xy = np.vstack([x, y])
        c = stats.gaussian_kde(xy)(xy)
   
        scatvu = ax.scatter(x, y, c=c)
        ax.set(
        title=title,
        xlabel=x_col,
        ylabel=y_col,
        xlim=(np.min(x), np.max(x)),
        ylim=(np.min(y), np.max(y)),
        aspect='auto'
    )   
        fig.colorbar(scatvu, label='Kernel density')

    """if c:
        nan_filter = np.isfinite(df[y_col])
        x, y = df[x_col][nan_filter], df[y_col][nan_filter]
        c = df[c]
        scatvu = ax.scatter(x, y, c=c)
        ax.set(
        title = title,
        xlabel = x_col,
        ylabel=y_col,
        xlim=(np.min(x), np.max(x)),
        ylim=(np.min(y), np.max(y)),
        aspect = 'auto'
        )
        label = df[c].name
        fig.colorbar(scatvu, label='Grade')"""

    if lineregress:
        slope, intercept, r_value, p_value, std_errr = stats.linregress(x, y)
        x_d = np.linspace(np.min(x), np.max(x), 100)
        y_r = slope*x_d+intercept


        statsvals = '''
        n {}
        Slope {}
        Pearson rho {}
        '''.format(len(x), round(slope, 2), round(r_value, 2))
        ax.annotate(statsvals, xy=(0.7, 0.0), xycoords='axes fraction', color='black')
        ax.plot(x_d, y_r, color='black', linestyle='--', label='Regression line')

    
    ax.minorticks_on()
    ax.grid(linestyle='--', which='major')
    ax.legend()
    plt.show()

def histogram(var, bins=20, color='green',title='Histogram', labely='Frequência', labelx='Teor', cum=False):

    

    if cum:
        fig, ax = plt.subplots(figsize=(12,8))

        ax.hist(var, bins=bins, cumulative=True, density=True, color=color)

        ax.set(
        title = title,
        ylabel=labely,
        xlabel=labelx,
        )

        plt.grid(linestyle='--')

        plt.show()
    else:

        fig, ax = plt.subplots(figsize=(12,8))

        ax.hist(var, bins=20, color=color)

        ax.set(
        title = title,
        ylabel=labelx,
        xlabel=labely,
        )

        plt.grid(linestyle='--')

        plt.show()

def validate_regression(pred, test, title):

    edefined = np.isfinite(pred)
    tdefined = np.isfinite(test)
    bothdefined = np.logical_and(edefined, tdefined)
    estimated = pred[bothdefined]
    true = test[bothdefined]

    fig, axs = plt.subplots(1, 3, figsize=(20,6))
    min_val = np.min([np.nanmin(estimated), np.nanmin(true)])
    max_val = np.max([np.nanmax(estimated), np.nanmax(true)])

    axs[0].plot([min_val, max_val], [min_val, max_val], color='red')
    slope, intercept, r_value, p_value, std_err = stats.linregress(estimated,true)
    x_d = np.linspace(min_val, max_val, 100)
    y_r = slope*x_d+intercept

    bias = true-estimated
    mse = np.mean(bias**2)
    r2 = r2_score(test, pred)
    mae = mean_absolute_error(test, pred)
    mse = mean_squared_error(test, pred)
    rmse = np.sqrt(mse)

    statsvals = '''
    n {}
    Slope {}
    Pearson rho {}
    '''.format(len(estimated), round(slope, 2), round(r_value, 2))


    axs[0].plot(x_d, y_r, color='gray', linestyle='--', label='Regression line')
    axs[0].annotate(statsvals, xy=(0.7, 0.0), xycoords='axes fraction', color='black')

    axs[0].scatter(estimated, true, c='black')
    axs[0].set_ylim([min_val, max_val])
    axs[0].set_xlim([min_val, max_val])
    axs[0].grid()
    axs[0].set_ylabel('True')
    axs[0].set_xlabel('Estimated')

    axs[1].hist(bias, bins=20, color='green')
    statsvals = '''
    Mean: {}
    Std: {}
    R² {}
    MAE {}
    MSE {}
    RMSE {}
    '''.format(
        round(np.mean(bias), 2),
        round(np.std(bias), 2),
        round(r2, 2),
        round(mae, 2),
        round(mse, 2),
        round(rmse, 2),
    )
    axs[1].annotate(statsvals, xy=(0.6, 0.5), xycoords='axes fraction', color='black')
    axs[1].grid()

    axs[2].scatter(true, bias, color='black')
    axs[2].grid()
    axs[2].set_ylabel('Error')
    axs[2].set_xlabel('Grade')
    axs[2].axhline(0, color='red')

    #saving
    plt.suptitle(title)
    plt.tight_layout()

    #plt.savefig(outfl, facecolor='white', bbox_inches='tight')


def features_importance(model, X_test, varnames, y_test, clf=True):
    
    if clf == True:
        metric = 'accuracy'
    else:
        metric = 'r2'

    fig, axs = plt.subplots(2, 1, figsize=(15,8))
    
    importances = model.feature_importances_
    std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
    forest_importances = pd.Series(importances, index=varnames)
    
    forest_importances.plot.bar(yerr=std, ax=axs[0])
    axs[0].set_title("Feature importances using mean decrease")
    axs[0].set_ylabel("Mean decrease")
    axs[0].grid()
    
    result = permutation_importance(model, X_test, y_test, scoring=metric, n_repeats=10)
    forest_importances = pd.Series(result.importances_mean, index=varnames)

    forest_importances.plot.bar(yerr=result.importances_std, ax=axs[1])
    axs[1].set_title("Feature importances using permutation")
    axs[1].set_ylabel("{} decrease".format(metric))
    axs[1].grid()

    fig.tight_layout()
    #fig.savefig(outfl, facecolor='white')

import math
import numpy as np
import matplotlib.pyplot as plt

def discrete_cmap(N, base_cmap='jet'):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)


def confusion_matrix_plot(clf, y_test, y_pred, title, figsize=(10,10), report=True, cmap='Blues', colorbar=False):

    cm = confusion_matrix(y_test, y_pred, normalize='true')

    fig, axs = plt.subplots(1,1, figsize=figsize)

    acc = round(accuracy_score(y_test, y_pred), 2)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    axs.set_title('{} - acc {} - n {}'.format(title, acc, len(y_test)))

    disp.plot(ax=axs, cmap=cmap, colorbar=colorbar)
    if report:
        print(classification_report(y_test, y_pred))
    #plt.savefig(outfl, facecolor='white', bbox_inches='tight')

def correlation_matrix(df, fsize, method='pearson'):

    f = plt.figure(figsize=fsize)
    correlations = df.corr(method=method).values
    plt.matshow(correlations, fignum=f.number, cmap='viridis')
    plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14, rotation=90)
    plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
    #cb = plt.colorbar()
    #cb.ax.tick_params(labelsize=14)

    for idxi, i in enumerate(range(correlations.shape[0])):
            for idxj, j in enumerate(range(correlations.shape[1])):
                plt.text(idxj, idxi, round(correlations[idxi, idxj], 2), ha="center", va="center", color="black")
                plt.text(idxj, idxi, round(correlations[idxi, idxj], 2), ha="center", va="center", color="black")
    
    #plt.savefig(outfl, bbox_inches='tight', facecolor='white')

def boxplots(df, vars_names_array, cat, title, cmap='jet'):
    n_var = len(vars_names_array)
    n_lines = math.ceil(n_var/3)
    fig, axs = plt.subplots(n_lines, 3, figsize=(15,15))

    axs = axs.flatten()

    unique_cats = np.unique(cat)
    cmap = matplotlib.cm.get_cmap(cmap, len(unique_cats))
    colors = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]

    for i, v_name in enumerate(vars_names_array):
        print('Processing {}'.format(v_name))

        v = df[v_name]
        fdef = np.isfinite(v)
        v = v[fdef]
        cat_aux = cat[fdef]
        
        bplot = axs[i].boxplot([v[cat_aux==c] for c in unique_cats], labels=unique_cats, patch_artist=True, notch=False)
        axs[i].tick_params(axis='x', labelrotation = 90)
        
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
        
        axs[i].set_title(v_name)
        axs[i].grid()

    iidx = n_lines*3-(n_lines*3-len(vars_names_array))
    axs_to_remove = np.arange(iidx, n_lines*3)
    for i in axs_to_remove:
        axs[i].set_visible(False)

    fig.suptitle(title, y=1.0)

    plt.tight_layout()

def sctt(x, y, ax, c=None):

    xdef = np.isfinite(x)
    ydef = np.isfinite(y)
    bothdef = np.logical_and(xdef, ydef)
    x, y = x[bothdef], y[bothdef]
    if c is None:
        xy = np.vstack([x, y])
        c = gaussian_kde(xy)(xy)

    corr = round(np.corrcoef([x, y])[0,1], 2)

    ax.scatter(x, y, c=c, s=1, cmap='jet')
    ax.set_title('rho: {}'.format(corr))



def scatter_matrix(df, figsize=(30,30), nmax=None, cat=None):
    if nmax is not None:
        idxs = np.arange(len(df))
        ridxs = np.random.choice(idxs, size=nmax, replace=False)
        df = df.iloc[ridxs]
    else:
        pass

    vars_array = [df[col].values for col in df.columns]
    vars_name = df.columns

    data = np.array(vars_array)
    numvars, numdata = data.shape
    fig, axes = plt.subplots(nrows=numvars, ncols=numvars, figsize=figsize)

    for i, j in zip(*np.triu_indices_from(axes, k=1)):
        for x, y in [(i,j), (j,i)]:

            sctt(data[x], data[y], axes[x,y], cat)
            axes[x,y].grid()
            axes[x,y].set_xlabel(vars_name[x])
            axes[x,y].set_ylabel(vars_name[y])

    for i, label in enumerate(vars_name):
        axes[i,i].hist(data[i], color='green')
        axes[i,i].set_title(label)

    plt.tight_layout()

def evaluate_kfolds(X, y, n_folds, n_repeats, model, clf=True, figsize=(14,12), regscore='r2', classcore='balanced_accuracy'):
    # prepare the cross-validation procedure
    cv = RepeatedKFold(n_splits=n_folds, n_repeats=n_repeats, random_state=1)

    if clf:
        scoring = classcore
    else:
        scoring = regscore

    # evaluate model
    scores = cross_val_score(model, X, y, scoring=scoring, cv=cv, n_jobs=-1)

    # plot the results
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(f'Model Performance K-Folds ({n_repeats} Repeats, {n_folds} Folds)')
    ax.set_xlabel('K-Folds')
    ax.set_ylabel(f'{scoring} score')
    ax.boxplot(np.array(scores).reshape(n_repeats, n_folds), showmeans=True)
    ax.legend([f'{n_repeats} Repeats, {n_folds} Folds'])
    plt.show()

def flag_outliers(df, column, iqr_distance=1.5, remove_outliers=False):
    array = df[column].values
    upper_quartile = np.nanpercentile(array, 75)
    lower_quartile = np.nanpercentile(array, 25)
    IQR = (upper_quartile - lower_quartile) * iqr_distance
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    
    fiqr = np.logical_and(array > quartileSet[0], array < quartileSet[1])
    fpos = array > 0
    f = np.logical_and(fiqr, fpos)
    
    print('{} samples were flagged as outliers.'.format(np.sum(~f)))
    print('Set True on remove outliers argument for clean outliers!')
    
    if remove_outliers:
        df = df.drop(df.index[~f], inplace=True)
        df = df
        
    return df


def tdscatter(x, y, z, c, zex=0.5, figsize=(10,30), title='title', s=2, elev=30, azim=60):

    # Obtenha o número de categorias em "c"
    cat_to_num = {cat: num for num, cat in enumerate(np.unique(c))}

    c_num = c.map(cat_to_num)
    k = len(np.unique(c))
    cats = np.unique(c)

    # Defina a paleta de cores
    cmap = plt.cm.get_cmap('jet', k)

    # Defina os locais dos marcadores de tick na barra de cores
    ticks_location = np.arange(k) 

  

    # Crie o gráfico de dispersão tridimensional
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect((np.ptp(x), np.ptp(y), zex*np.ptp(z)))
    ts = ax.scatter(x, y, z, c=c_num, s=s, cmap=cmap)
    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')
    ax.set_zlabel('Elevation (m)')
    ax.set_title(title)

    ax.view_init(elev=elev, azim=azim)
    # Adicione a barra de cores ao gráfico
    cax = fig.add_axes([ax.get_position().x1+0.05,ax.get_position().y0,0.02,ax.get_position().height])
    cbar = plt.colorbar(ts, cax=cax, ticks=ticks_location)
    cbar.set_ticklabels(np.unique(c))

    # Posicione a caixa delimitadora do eixo da legenda fora do gráfico
    cax_pos = cax.get_position()
    cax.set_position([cax_pos.x0 + 0.2, cax_pos.y0, cax_pos.width, cax_pos.height])
    cbar.set_ticks(ticks_location)
    cbar.set_ticklabels(cats)
    fig.subplots_adjust(right=1)
    fig.subplots_adjust(wspace=0.5)          

def count_cat(cat):   
    fig, ax = plt.subplots(figsize=(12,8))

    x_labels = np.unique(cat)
    x_ticks = np.arange(len(x_labels))

    heights = [np.sum(cat==i) for i in x_labels]

    ax.bar(x_ticks, heights)

    for x, y in zip(x_ticks, heights):
        ax.annotate(str(y), (x, y), ha='center')

    ax.set(
    title='Categorias',
    ylabel='Numero de amostras',
    xticks=x_ticks,
    )
    ax.set_xticklabels(x_labels, rotation=90) #definindo xticklabes fora do metodo set para rotacionar 

    plt.grid(linestyle='--', axis='y')

    plt.show()
