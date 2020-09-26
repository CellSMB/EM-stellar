# Copyright (c) 2020, Afshin Khadangi. All rights reserved.
#
# This work is made available under the MIT License.

import argparse
import copy
import sys
from skimage import io
import glob
import os
import imagej
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, jaccard_score
from skimage.io import imread_collection, imsave
from PIL import Image
import seaborn as sns
from pathlib import Path
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------

def run(imagej_dir, segmentation_results_dir, ground_truth_binary_masks_dir, windows=False):
    ij = imagej.init(imagej_dir)
    path = Path(segmentation_results_dir)
    if (windows):
        base_directory = (str(path.parent))
    else:
        base_directory = '/'+(str(path.parent))
    Temp_dir = base_directory + '/Temp'
    if os.path.exists(Temp_dir):
        shutil.rmtree(Temp_dir)
    os.mkdir(Temp_dir)
    for root, dirs, files in os.walk(segmentation_results_dir, topdown=True):
      if (len(dirs)>0):
        childdirs = dirs
    parentdir = [ground_truth_binary_masks_dir, segmentation_results_dir]
    childdirs_imgs = []
    print("iterating the segmentation results directories ...")
    for item in tqdm(childdirs):
        Test_directory = parentdir[1]+"/"+item+"/*.png"  # Specify labels directory
        files = glob.glob (Test_directory)
        X_data = []
        for myFile in files:
            image = io.imread(myFile)
            X_data.append (image)
        tmp = np.asarray(X_data,dtype='float32')
        if (np.max(tmp)>1):tmp=tmp/255.0
        childdirs_imgs.append(tmp)
        tmp = np.vstack((tmp,tmp))
        imsave(Temp_dir+'/'+item+'.tif',tmp)
    Ground_data = np.asarray(list(imread_collection(parentdir[0]+"/*.png")),dtype='float32')
    Ground_dataTmp = np.vstack((Ground_data,Ground_data))
    zipdata = zip(childdirs, childdirs_imgs)
    mydict = dict(zipdata)
    if (np.max(Ground_data)>1):Ground_data=Ground_data/255.0
    if (np.max(Ground_dataTmp)>1):Ground_dataTmp=Ground_dataTmp/255.0
    imsave(Temp_dir+'/Ground.tif',Ground_dataTmp)
    Language_extension = "BeanShell"
    macroVRand = """
    import trainableSegmentation.metrics.*;
    #@output String VRand
    metric = new RandError( originalLabels, proposedLabels );
    maxThres = 1.0;
    maxScore = metric.getMaximalVRandAfterThinning( 0.0, maxThres, 0.1, true );  
    VRand = maxScore;
    """
    macroVInfo = """
    import trainableSegmentation.metrics.*;
    #@output String VInfo
    metric = new VariationOfInformation( originalLabels, proposedLabels );
    maxThres =1.0;
    maxScore = metric.getMaximalVInfoAfterThinning( 0.0, maxThres, 0.1 );  
    VInfo = maxScore;
    """
    current_path = Temp_dir
    if (windows):
        current_path  = current_path.replace("\\", "/")
    VRandDf = []
    VInfoDf = []
    print("Retrieving Rand/Info metrics for the networks ...")
    for item in tqdm(childdirs):
        macroVRandTmp = ('\nimport ij.IJ;\noriginalLabels=IJ.openImage("' + current_path + '/' + 'Ground' + '.tif");' +
                  '\nproposedLabels=IJ.openImage("' + current_path + '/' + item + '.tif");' + '\nimport trainableSegmentation.metrics.*;'
                  + '\n#@output String VRand' + '\nmetric = new RandError( originalLabels, proposedLabels );' + '\nmaxThres = 1.0;' + '\nmaxScore = metric.getMaximalVRandAfterThinning( 0.0, maxThres, 0.1, true );'
                  + '\nVRand = maxScore;')
        VRand = float(ij.py.run_script(Language_extension, macroVRandTmp).getOutput('VRand'))
        VRandDf.append(VRand)
        macroVInfoTmp = ('\nimport ij.IJ;\noriginalLabels=IJ.openImage("' + current_path + '/' + 'Ground' + '.tif");' +
                  '\nproposedLabels=IJ.openImage("' + current_path + '/' + item + '.tif");' + '\nimport trainableSegmentation.metrics.*;'
                  + '\n#@output String VInfo' + '\nmetric = new VariationOfInformation( originalLabels, proposedLabels );' + '\nmaxThres = 1.0;' + '\nmaxScore = metric.getMaximalVInfoAfterThinning( 0.0, maxThres, 0.1 );'
                  + '\nVInfo = maxScore;')
        VInfo = float(ij.py.run_script(Language_extension, macroVInfoTmp).getOutput('VInfo'))
        VInfoDf.append(VInfo)
    print("Retrieving standard metrics for the segmentation results ...")
    Ground = Ground_data.flatten()
    Ground = (Ground > 0.5).astype(np.int_)
    F1score = []
    accuracy = []
    sensitivity = []
    specificity = []
    PPV = []
    NPV = []
    Jaccard = []
    for item in tqdm(mydict):
        itemTmp = mydict[item]
        itemTmp = (itemTmp > 0.5).astype(np.int_)
        itemTmp = itemTmp.flatten()
        tn, fp, fn, tp = confusion_matrix(Ground, itemTmp).ravel()
        accuracy.append((tp+tn)/(tp+tn+fp+fn))
        sn = tp/(tp+fn)
        sensitivity.append(sn)
        specificity.append(tn/(tn+fp))
        pr = tp/(tp+fp)
        PPV.append(pr)
        NPV.append(tn/(tn+fn))
        Jaccard.append(jaccard_score(Ground, itemTmp))
        F1score.append(2*(pr*sn)/(pr+sn))    
    MyDataFrameDict = {'Network': childdirs,
          'F1-score': F1score,
          'VRand': VRandDf,
          'VInfo': VInfoDf,
          'accuracy': accuracy,
          'sensitivity': sensitivity,
          'specificity': specificity,
          'PPV': PPV,
          'NPV': NPV,
          'Jaccard': Jaccard
          }
    df = pd.DataFrame(MyDataFrameDict, index=childdirs, columns = ['F1-score', 'VRand', 'VInfo', 'accuracy', 'sensitivity', 
        'specificity', 'PPV', 'NPV', 'Jaccard'])
    df = df.round(decimals=5)
    cm = sns.diverging_palette(20, 130, n = len(childdirs), l=70, as_cmap=True)
    styles = [
        dict(props=[("font-family", "Times New Roman"),
                                   ("text-align", "center")])
    ]
    pd.set_option('precision', 5)
    df.sort_index(axis=0, inplace = True)
    html = (df.style.set_table_styles(styles).background_gradient(cmap=cm))
    f=open("Dataframe_output.html","w")
    f.write(html.render())
    f.close()
    # html.to_csv('results.csv')
    plt.figure(figsize=(6, 6), dpi=300)
    sns.set(font_scale=0.8, font="sans-serif")
    csfont = {'fontname':'sans-serif'}
    heat_map = sns.heatmap(df, cmap="Spectral")
    plt.suptitle("Heatmap of the segmentation methods relative to different metrics", fontsize=10, y=1)
    plt.xlabel("Metrics", fontsize=8, **csfont)
    plt.ylabel("Methods", fontsize=8, **csfont)
    plt.autoscale() 
    plt.savefig('Heatmap_output.png', dpi = 300)


def _string_2_boolean(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


#----------------------------------------------------------------------------

_examples = '''examples:

  # Run EM-stellar using the Fiji.app, segmentation results and ground-truth images directories:
  Linux/Mac:
  python --imagej_dir=~/Fiji.app --segmentation_results_dir=~/predicted_masks --ground_truth_binary_masks_dir=~/ground_truth_masks
  Windows:
  python --imagej_dir=C:/Users/Fiji.app --segmentation_results_dir=C:/Users/predicted --ground_truth_binary_masks_dir=C:/Users/ground --windows=true
  ''' 

def main():
    parser = argparse.ArgumentParser(
        description='Run EM-stellar',
        epilog=_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--imagej_dir', help='Directory address for "Fiji.app" folder',  required=True, metavar='DIR')
    parser.add_argument('--segmentation_results_dir', help='Predicted masks root directory', required=True,  metavar='DIR')
    parser.add_argument('--ground_truth_binary_masks_dir', help='Ground-truth data directory', required=True,  metavar='DIR')
    parser.add_argument('--windows', help='Running on windows? Set this arg value as True (default: %(default)s)', default=False, metavar='BOOL', type=_string_2_boolean)

    args = parser.parse_args()

    if not os.path.exists(args.imagej_dir):
        print ('Error: imagej root directory does not exist.')
        sys.exit(1)



    run(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------