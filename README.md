# EM-stellar
This repository is official implementation of [**EM-stellar: benchmarking deep learning for electron microscopy image segmentation**](https://www.biorxiv.org/content/10.1101/2020.07.15.203836v1) on Google Colab.

---

<font size = 4>This notebook represents the implementation of the [**EM-stellar**](https://www.biorxiv.org/content/10.1101/2020.07.15.203836v1). Deep learning (DL) methods offer an exciting opportunity to automate the segmentation process by learning from manual annotations of a small sample of EM data. While many DL methods are being rapidly adopted to segment EM data no benchmark analysis has been conducted on these methods to date. We present EM-stellar as a platform that can be used to benchmark the performance of a range of state-of-the-art DL methods on user-provided datasets. 



---
<font size = 4>Papers related to this Notebook: 

- <font size = 3>**EM-stellar: benchmarking deep learning for electron microscopy image segmentation** by *Afshin Khadangi, Thomas Boudier, Vijay Rajagopal*  (https://www.biorxiv.org/content/10.1101/2020.07.15.203836v1)

- <font size = 3>**EM-net: Deep learning for electron microscopy image segmentation** by *Afshin Khadangi, Thomas Boudier, Vijay Rajagopal*  (https://www.biorxiv.org/content/10.1101/2020.02.03.933127v1)


<font size = 4>**Please cite** [**this original paper**](https://www.biorxiv.org/content/10.1101/2020.07.15.203836v1) **when using or developing this notebook.**
  
  ---

# **How to use?!**

<font size = 4>We have provided the instructions for the usage of this Notebook in the following link:
  - [**Colab Notebook**](https://colab.research.google.com/github/akhadangi/EM-stellar/blob/master/EM_stellar.ipynb): Walk through the pipeline including data upload and deploying the benchmarking.

**Important: Make sure that you create a copy of the following Colab Notebook on your Google Drive before running or making any changes to the notebook**

---
### **Images**
<font size = 4>We have provided a sample dataset as folder "Images", which includes the directories of the ground-truth and predicted segmentation masks. These images can be used as a demo implementation of the EM-stellar. However, you are encouraged to follow the same formatting and structure to try EM-stellar on your own data. For further information, please follow the instructions as highlighted on the notebook.  

---
### **Structure of a notebook**

<font size = 4>The notebook contains two types of cell:  

<font size = 4>**Text cells** provide information and can be modified by douple-clicking the cell. You are currently reading the text cell. You can create a new text by clicking `+ Text`.

<font size = 4>**Code cells** contain code and the code can be modfied by selecting the cell. To execute the cell, move your cursor on the `[ ]`-mark on the left side of the cell (play button appears). Click to execute the cell. After execution is done the animation of play button stops. You can create a new coding cell by clicking `+ Code`.

---
### **Table of contents, Code snippets** and **Files**

<font size = 4>On the top left side of the notebook you find three tabs which contain from top to bottom:

<font size = 4>*Table of contents* = contains structure of the notebook. Click the content to move quickly between sections.

<font size = 4>*Code snippets* = contain examples how to code certain tasks. You can ignore this when using this notebook.

<font size = 4>*Files* = contain all available files. After mounting your google drive (see section 1.) you will find your files and folders here. 

<font size = 4>**Remember that all uploaded files are purged after changing the runtime.** All files saved in Google Drive will remain. You do not need to use the Mount Drive-button; your Google Drive is connected in section 1.2.

<font size = 4>**Note:** The "sample data" in "Files" contains default files. Do not upload anything in here!

---
### **Making changes to the notebook**

<font size = 4>**You can make a copy** of the notebook and save it to your Google Drive. To do this click file -> save a copy in drive.

<font size = 4>To **edit a cell**, double click on the text. This will show you either the source code (in code cells) or the source text (in text cells).
You can use the `#`-mark in code cells to comment out parts of the code. This allows you to keep the original code piece in the cell as a comment.
  
---

# **Running EM-stellar on your local resources**

<font size = 4>We have received some good reviews from users who have storage issues on Google Drive or face security/privacy concern over their data. We truly understand such concerns and hence we have provided python script that you can run on your local computer/cluster. The code is provided in `run_EM-stellar.py`

## Prerequisties
This code has been implemented in python. You need to install [pyimagej](https://pypi.org/project/pyimagej/) which is a python wrapper for ImageJ. 

To install pyimagej:
```
$ pip install pyimagej
```
To install scikit-learn:
```
$ pip install scikit-learn
```
To install scikit-image:
```
$ pip install scikit-image
```
To install pandas:
```
$ pip install pandas
```
To install tqdm:
```
$ pip install tqdm
```
To install seaborn:
```
$ pip install seaborn
```
To install matplotlib:
```
$ pip install matplotlib
```
You will also need to install [Fiji](https://imagej.net/Fiji/Downloads). If you have already installed Fiji, then we are good!

## Help
To get help on using EM-stellar run `python run_EM-stellar.py --help`

### Examples:
* Run EM-stellar using the Fiji.app, segmentation results and ground-truth images directories: *
* Linux/Mac:
`
python --imagej_dir=~/Fiji.app --segmentation_results_dir=~/predicted_masks --ground_truth_binary_masks_dir=~/ground_truth_masks
`
* Windows:
`
python --imagej_dir=C:/Users/user/Desktop/Fiji.app --segmentation_results_dir=~/datasets --ground_truth_binary_masks_dir=config-f --windows=true
`
