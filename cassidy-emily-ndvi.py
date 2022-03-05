#!/usr/bin/env python
# coding: utf-8

# <img style="float: left;" src="earth-lab-logo-rgb.png" width="150" height="150" />
# 
# # Earth Analytics Education - EA  Python Course Spring 2021

# ## Important  - Assignment Guidelines
# 
# 1. Before you submit your assignment to GitHub, make sure to run the entire notebook with a fresh kernel. To do this first, **restart the kernel** (in the menubar, select Kernel$\rightarrow$Restart & Run All)
# 2. Always replace the `raise NotImplementedError()` code with your code that addresses the activity challenge. If you don't replace that code, your notebook will not run.
# 
# ```
# # YOUR CODE HERE
# raise NotImplementedError()
# ```
# 
# 3. Any open ended questions will have a "YOUR ANSWER HERE" within a markdown cell. Replace that text with your answer also formatted using Markdown.
# 4. **DO NOT RENAME THIS NOTEBOOK File!** If the file name changes, the autograder will not grade your assignment properly.
# 6. When you create a figure, comment out `plt.show()` to ensure the autograder can grade your plots. For figure cells, DO NOT DELETE the code that says `DO NOT REMOVE LINE BELOW`.
# 
# ```
# ### DO NOT REMOVE LINE BELOW ###
# student_plot1_ax = nb.convert_axes(plt)
# ```
# 
# * Only include the package imports, code, and outputs that are required to run your homework assignment.
# * Be sure that your code can be run on any operating system. This means that:
#    1. the data should be downloaded in the notebook to ensure it's reproducible
#    2. all paths should be created dynamically using the `os.path.join`
# 
# ## Follow to PEP 8 Syntax Guidelines & Documentation
# 
# * Run the `autopep8` tool on all cells prior to submitting (HINT: hit shift + the tool to run it on all cells at once!
# * Use clear and expressive names for variables. 
# * Organize your code to support readability.
# * Check for code line length
# * Use comments and white space sparingly where it is needed
# * Make sure all python imports are at the top of your notebook and follow PEP 8 order conventions
# * Spell check your Notebook before submitting it.
# 
# For all of the plots below, be sure to do the following:
# 
# * Make sure each plot has a clear TITLE and, where appropriate, label the x and y axes. Be sure to include UNITS in your labels.
# 

# ### Add Your Name Below 
# **Your Name:** Emily Cassidy

# <img style="float: left;" src="colored-bar.png"/>

# ---

# # Week 04 and 05 Homework - Automate NDVI Workflow
# 
# For this assignment, you will write code to generate a plot of the mean normalized difference vegetation index (NDVI) for two different sites in the United States across one year of data:
# 
# * San Joaquin Experimental Range (SJER) in Southern California, United States
# * Harvard Forest (HARV) in the Northeastern United States
# 
# The data that you will use for this week is available from **earthpy** using the following download: 
# 
# `et.data.get_data('ndvi-automation')`
# 
# ## Assignment Goals
# 
# Your goal in this assignment is to create the most efficient and concise workflow that you can that allows for:
# 
# 1. The code to scale if you added new sites or more time periods to the analysis.
# 2. Someone else to understand your workflow.
# 3. The LEAST and most efficient (i.e. runs fast, minimize repetition) amount of code that completes the task.
# 
# ### HINTS
# 
# * Remove values outside of the landsat valid range of values as specified in the metadata, as needed.
# * Keep any output files SEPARATE FROM input files. Outputs should be created in an outputs directory that is created in the code (if needed) and/or tested for.
# * Use the functions that we demonstrated during class to make your workflow more efficient.
# * BONUS - if you  chose - you can export your data as a csv file. You will get bonus points for doing this.
# 
# 
# ## Assignment Requirements
# 
# Your submission to the GitHub repository should include:
# * This Jupyter Notebook file (.ipynb) with:
#     * The code to create a plot of mean NDVI across a year for  2 NEON Field Sites:
#         * NDVI on the x axis and formatted dates on the y for both NEON sites on one figure/axis object
#     * The **data should be cleaned to remove the influence of clouds**. See the [earthdatascience website for an example of what your plot might look like with and without removal of clouds](https://www.earthdatascience.org/courses/earth-analytics-python/create-efficient-data-workflows/).
# * BONUS: Create one output `.csv` file that has 3 columns - NDVI, Date and Site Name - with values for SJER and HARV.
# 
# Your notebook should:
# * Have *at least* 2 well documented and well named functions with docstrings.
# * Include a Markdown cell at the top of the notebook that outlines the overall workflow using pseudocode (i.e. plain language, not code)
# * Include additional Markdown cells throughout the notebook to describe: 
#     * the data that you used - and where it is from
#     * how data are being processing
#     * how the code is optimized to run fast and be more concise

# # Replace this cell with your pseudocode  for this workflow
# Pseudo code for NDVI workflow:
# - Before we start the analysis, we will need to import the NDVI data and open up the geographic boundary shapefile.
# - Then we will make a list of Landsat files we will loop through. To do that, make sure you're in the right site folder.
# - Open individual band files and clip to the boundary. Clean them up to only include numbers in a valid range.
# - Clean up the raster to only include numbers in a valid range.
# - Mask out clouds in the raster.
# - Calculate NDVI.
# - Put NDVI values, site name, and date in a Pandas DataFrame.
# 
# In[1]:


# Autograding imports - do not modify this cell
import matplotcheck.autograde as ag
import matplotcheck.notebook as nb
import matplotcheck.timeseries as ts
from datetime import datetime


# In[2]:


# Import needed packages in PEP 8 order
# and no unused imports listed (10 points total)

import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import rioxarray as rxr
import xarray as xr
from rasterio.plot import plotting_extent
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import earthpy.mask as em

# Get data and set working directory
data = et.data.get_data('ndvi-automation')
os.chdir(os.path.join(et.io.HOME,
                      "earth-analytics",
                      "data"))


# In[3]:


# DO NOT MODIFY THIS CELL
# Tests that the working directory is set to earth-analytics/data

path = os.path.normpath(os.getcwd())
student_wd_parts = path.split(os.sep)

if student_wd_parts[-2:] == ['earth-analytics', 'data']:
    print("\u2705 Great - it looks like your working directory is set correctly to ~/earth-analytics/data")
else:
    print("\u274C Oops, the autograder will not run unless your working directory is set to earth-analytics/data")


# # Figure 1: Plot 1 - Mean NDVI For Each Site Across the Year (50 points)
# 
# Create a plot of the mean normalized difference vegetation index (NDVI) for the two different sites in the United States across the year: 
# 
# * NDVI on the x axis and formatted dates on the y for both NEON sites on one figure/axis object.
# * Each site should be identified with a different color in the plot and legend.
# * The final plot **data should be cleaned to remove the influence of clouds**.
# * Be sure to include appropriate title and axes labels.
# 
# Add additional cells as needed for processing data (e.g. defining functions, etc), but be sure to:
# * follow the instructions in the code cells that have been provided to ensure that you are able to use the sanity check tests that are provided. 
# * include only the plot code in the cell identified for the final plot code below

# ## Task 1: 
# 
# In the cell below, create a single dataframe containing MEAN NDVI, the site name, 
# and the date of the data for the HARV site 
# scene `HARV/landsat-crop/LC080130302017031701T1-SC20181023151837`.  The column names for the  final
# DataFrame should be`mean_ndvi`, and `site`, and the data should be **indexed on the date**. 
# 
# Use the functions that we reviewed in class (or create your own versions of them) to implement your code
# 
# ### In the Cell below Place  All Functions Needed to Run this Notebook (20 points)

# In[4]:


### DO NOT REMOVE THIS LINE OR EDIT / MOVE THIS CELL ###
start_time = datetime.now()


# In[5]:


# Get a list of each directory
site_path = os.path.join("ndvi-automation", "sites")

# Get a list of both site directories 
sites = glob(site_path + "/*/")
site_name = 'HARV'


# In[6]:


vector_dir = os.path.join(site_path, site_name,
                          "vector")
# Open crop boundary
site_boundary_path = os.path.join(vector_dir,  site_name + "-crop.shp")
crop_bound = gpd.read_file(site_boundary_path)
crop_bound.plot()
type(crop_bound)


# In[7]:


# In the landsat directory, get files 
landsat_dir = os.path.join(site_path, site_name, "landsat-crop")
landsat_folder = os.path.join(landsat_dir, "LC080130302017031701T1-SC20181023151837")

# Open bands
band_files = sorted(glob(os.path.join(landsat_folder, "*band*[4-5].tif")))


# In[8]:


# In this cell place all of the functions needed to run your notebook
# You will be graded here on function application, docstrings, efficiency so ensure
# All functions are placed here!

#  This function has the code from the workflow above
def open_clean_bands(band_path,
                     crop_bound,
                     valid_range=None,):
    """Open and mask a single landsat band using a pixel_qa layer.

    Parameters
    -----------
    band_path : string
        A path to the array to be opened
    crop_bound : GeoPandas DataFrame
        A data from that tells us the extent of the site of interest
    valid_range : tuple (optional)
        A tuple of min and max range of values for the data. Default = None


    Returns
    -----------
    arr : xarray DataArray
        An xarray DataArray with values that should be 
        masked set to 1 for True (Boolean)
    """
    # TODO add tests to ensure the arrays are the same .shape
    band = rxr.open_rasterio(band_path, masked=True).rio.clip(crop_bound.geometry,
                                                              from_disk=True).squeeze()

    # Only run this step if a valid range tuple is provided
    if valid_range:
        mask = ((band < valid_range[0]) | (band > valid_range[1]))
        band_xr = band.where(~xr.where(mask, True, False))

    return band_xr

def cloud_mask_ndvi(ndvi_array, folder_path, crop_bound, masked_values):
    """Use landsat QA files to mask clouds from Landsat geotiffs.
     Parameters
    -----------
    ndvi_array: xarray DataArray
        An xarray DataArray with ndvi values
    folder_path : string
        A path to the site folder in which QA array lives
    crop_bound : GeoPandas DataFrame
        A data from that tells us the extent of the site of interest
    masked_values : list
        A list of all values to be masked


    Returns
    -----------
    arr : xarray DataArray
        An xarray DataArray with ndvi values, masked to values provided
    """
    qa_path = glob(os.path.normpath(os.path.join(folder_path, "*pixel*.tif")))
    qa_file = rxr.open_rasterio(
            qa_path[0], masked=True).rio.clip(crop_bound.geometry, 
                                              from_disk=True).squeeze()
    ndvi_clean_crop = ndvi_array.where(~qa_file.isin(masked_values))
    
    return ndvi_clean_crop


# In[9]:


# Create dataframe of mean NDVI in this cell using the functions created above
# Important: to use the ungraded tests below as a sanity check,
# name your columns: mean_ndvi and site
# Call the dataframe at the end of the cell so the tests run on it!
# Be sure that the date column is an index of type date
# HINT: the time series lessons may help you remember how to do this!

all_bands = []
for aband in band_files:
    print("Opening up", aband)
    cleaned_band = open_clean_bands(band_path=aband,
                                    crop_bound=crop_bound,
                                    valid_range=(0, 10000))
    all_bands.append(cleaned_band)


# Then calculate NDVI
ndvi_xr = (all_bands[1]-all_bands[0]) / (all_bands[1]+all_bands[0])
ndvi_xr.plot()


# In[10]:


# Get QA data from the Landsat folder to determine cloud mask.
qa_path = glob(os.path.normpath(os.path.join(landsat_folder, "*pixel*.tif")))

qa_file = rxr.open_rasterio(
    qa_path[0], masked=True).rio.clip(crop_bound.geometry, 
                                      from_disk=True).squeeze()

high_cloud_confidence = em.pixel_flags["pixel_qa"]["L8"]["High Cloud Confidence"]
cloud = em.pixel_flags["pixel_qa"]["L8"]["Cloud"]
cloud_shadow = em.pixel_flags["pixel_qa"]["L8"]["Cloud Shadow"]
    
all_masked_values = cloud_shadow + cloud + high_cloud_confidence

ndvi_clean_crop = ndvi_xr.where(~qa_file.isin(all_masked_values))
ndvi_clean_crop.plot()


# In[20]:


# Get the mean of the xarray and get the value from the array
ndvi_mean = ndvi_clean_crop.mean()
ndvi_mean_value = ndvi_mean.item()


# In[12]:


# Now using components of the path, create a dataframe with mean ndvi,
# data, and site.

path_components = landsat_folder.split(os.sep)
site = path_components[2]
file_string = path_components[4]

date = file_string[10:18]
date_time = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')

ndvi_list =  []
ndvi_list.append([site, date_time, ndvi_mean_value])
ndvi_list

ndvi_df = pd.DataFrame(ndvi_list, columns=['site', 'date', 'mean_ndvi'])
ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
ndvi_df.set_index("date", inplace = True)
ndvi_df


# In[13]:


# This cell  is testing your data output above

student_ndvi_ts_single_site = _

single_scene_points = 0

# Ensure the data is stored in a dataframe.
if isinstance(student_ndvi_ts_single_site, pd.DataFrame):
    print('\u2705 Your data is stored in a DataFrame!')
    single_scene_points += 1
else:
    print('\u274C It appears your data is not stored in a DataFrame. ',
          'To see what type of object your data is stored in, check its type with type(object)')

# Ensure that the date column is the index
if isinstance(student_ndvi_ts_single_site.index, pd.core.indexes.datetimes.DatetimeIndex):
    print('\u2705 You have the index set to the date column!')
    single_scene_points += 2
else:
    print('\u274C You do not have the index set to the date column.')

# Ensure that the date column is datetime
if isinstance(student_ndvi_ts_single_site.index[0], pd._libs.tslibs.timestamps.Timestamp):
    print('\u2705 The data in your date column is datetime!')
    single_scene_points += 2
else:
    print('\u274C The data in your date column is not datetime.')

# Ensure the site name is correct
if student_ndvi_ts_single_site.site.values[0] == 'HARV':
    print('\u2705 You have the correct site name!')
    single_scene_points += 5
else:
    print('\u274C You do not have the correct site name.')

if np.allclose(0.281131628228094, student_ndvi_ts_single_site.mean_ndvi.values[0]):
    print('\u2705 You have the correct mean NDVI value!')
    single_scene_points += 5
else:
    print('\u274C You do not have the correct mean ndvi value.')

print("\n \u27A1 You received {} out of 15 points for creating a dataframe.".format(
    single_scene_points))
single_scene_points


# ## Task 2:
# 
# In the cell below, process all of the landsat scenes. Create a DataFrame that contains the following 
# information for each scene
# 
# 
# |   | index  | site  | mean_ndvi  | 
# |---|---|---|---|
# | Date  |   |   |   |
# |  2017-01-07  | 0  | SJER  | .4  |  
# 
# Be sure to call your dataframe at the end of the cell to ensure autograding works.
# HINT: FOR THIS STEP, leave any rows containing missing values (`NAN`).

# In[14]:


# Create dataframe of NDVI including the cleaning data to deal with clouds

# Important: to use the ungraded tests below as a sanity check,
# name your columns: mean_ndvi and site
# Don't forget to set date as the index and make the values of type datetime

# Get a list of each directory
site_path = os.path.join("ndvi-automation", "sites")

# Get a list of both site directories 
sites = glob(os.path.join(site_path, "*"))

ndvi_list = []
for site in sites:
    path_components = site.split(os.sep)
    site_name = path_components[2]
    vector_dir = os.path.join(site_path, site_name,
                          "vector")
    # Open crop boundary
    site_boundary_path = os.path.join(vector_dir,  site_name + "-crop.shp")
    crop_bound = gpd.read_file(site_boundary_path)

    # In the landsat directory, get files 
    landsat_dir = os.path.join(site_path, site_name, "landsat-crop")
    landsat_folders = sorted(glob(os.path.join(landsat_dir, "*")))
    
    for folder in landsat_folders:
        # Open bands
        band_files = sorted(glob(os.path.join(folder, "*band*[4-5].tif")))
        all_bands = []
        for aband in band_files:
            print("Opening up", aband)
            cleaned_band = open_clean_bands(band_path=aband, 
                                            crop_bound=crop_bound,
                                            valid_range=(0, 10000))
            all_bands.append(cleaned_band)
        
        # Then calculate NDVI
        ndvi_xr = (all_bands[1]-all_bands[0]) / (all_bands[1]+all_bands[0])
        
        high_cloud_confidence = em.pixel_flags["pixel_qa"]["L8"]["High Cloud Confidence"]
        cloud = em.pixel_flags["pixel_qa"]["L8"]["Cloud"]
        cloud_shadow = em.pixel_flags["pixel_qa"]["L8"]["Cloud Shadow"]
        all_masked_values = cloud_shadow + cloud + high_cloud_confidence
        ndvi_clean_crop = cloud_mask_ndvi(
            ndvi_array=ndvi_xr, folder_path=folder,
            crop_bound=crop_bound, masked_values=all_masked_values)
        
        ndvi_mean = ndvi_clean_crop.mean(skipna=True)
        ndvi_mean_value = ndvi_mean.item()
        
        path_components = folder.split(os.sep)
        site = path_components[2]
        file_string = path_components[4]
        date = file_string[10:18]
        date_time = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')
        ndvi_list.append([site, date_time, ndvi_mean_value])

ndvi_df = pd.DataFrame(ndvi_list, columns=['site', 'date', 'mean_ndvi'])
ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
ndvi_df.set_index("date", inplace = True)
ndvi_df


# In[15]:


# Last sanity check before creating your plot (10 points)

# Ensure that you call your dataframe at the bottom of the cell above
# and that it has columns called: mean_ndvi and site

# Ensure the data is stored in a dataframe.
student_ndvi_df = _

df_points = 0

if isinstance(student_ndvi_df, pd.DataFrame):
    print('\u2705 Your data is stored in a DataFrame!')
    df_points +=2
else:
    print('\u274C It appears your data is not stored in a DataFrame. ',
          'To see what type of object your data is stored in, check its type with type(object)')

# Check that dataframe contains the appropriate number of NAN values
if student_ndvi_df.mean_ndvi.isna().sum() == 15:
    print('\u2705 Correct number of masked data values!')
    df_points +=2
else:
    print('\u274C The amount of null data in your dataframe is incorrect.')


# Ensure that the date column is the index
if isinstance(student_ndvi_df.index, pd.core.indexes.datetimes.DatetimeIndex):
    print('\u2705 You have the index set to the date column!')
    df_points +=3
else:
    print('\u274C You do not have the index set to the date column.')

# Ensure that the date column is datetime
if isinstance(student_ndvi_df.index[0], pd._libs.tslibs.timestamps.Timestamp):
    print('\u2705 The data in your date column is datetime!')
    df_points +=3
else:
    print('\u274C The data in your date column is not datetime.')

# Output for timer, # DO NOT MODIFY
end_time = datetime.now()
total_time = end_time - start_time
print(
    "Your total run time for processing the data was {0}.".format(total_time))

print("\n \u27A1 You received {} out of 10 points for creating a dataframe.".format(
    df_points))

df_points


# In[16]:


# Add only the plot code to this cell

# This is the final figure of mean NDVI
# for both sites across the year
# with data cleaned to deal with clouds

f, ax = plt.subplots(figsize=(14, 9))
for s, df in ndvi_df.dropna().groupby('site'):
    ax.plot(df['mean_ndvi'], 'o-',  label=s)
    
ax.set(title="Mean Normalized Vegetation Difference Index (NDVI) for two NEON sites Over One Year",
       xlabel='Date',
       ylabel='NDVI Mean')
plt.legend(bbox_to_anchor=(0.98,0.98))


### DO NOT REMOVE LINES BELOW ###
final_masked_solution = nb.convert_axes(plt, which_axes="current")

### DO NOT REMOVE LINES BELOW ###
final_masked_solution = nb.convert_axes(plt, which_axes="current")


# In[17]:


# Ignore this cell for the autograding tests


# In[18]:


# Ignore this cell for the autograding tests


# # Question 1 (10 points)
# 
# Imagine that you are planning NEON’s upcoming flight season to capture remote sensing data in these locations and want to ensure that you fly the area when the vegetation is the most green.
# 
# When would you recommend the flights take place for each site? 
# 
# Answer the question in 2-3 sentences in the Markdown cell below.

# If I were planning NEON’s upcoming flight season, I would choose the flights to take place over the HARV site in June, and the flights over the SJER site to take place at the end of March or early April. This would ensure the flights would be capturing data in these locations when the vegetation is the most green.
# 
# However, it might be useful to get more data points for the SJER site in the March and April to ensure we would be capturing peak green. We have no valid data for early-to-mid-April.

# # Question 2 (10 points)
# 
# How could you modify your workflow to look at vegetation changes over time in each site? 
# 
# Answer the question in 2-3 sentences in the Markdown cell below.

# There are a few different ways we can automate this code with functions and it was difficult to tell which sections of the code were the best to turn into functions. I think if I had more time I would think more about how to make the code more readable and reproducible, which would help inform which sections of code are the most useful to turn into functions.

# # Do not edit this cell! (10 points)
# 
# The notebook includes:
# * additional Markdown cells throughout the notebook to describe: 
#     * the data that you used - and where it is from
#     * how data are being processing
#     * how the code is optimized to run fast and be more concise

# # Do not edit this cell! (20 points)
# 
# The notebook will also be checked for overall clean code requirements as specified at the **top** of this notebook. Some of these requirements include (review the top cells for more specifics): 
# 
# * Notebook begins at cell [1] and runs on any machine in its entirety.
# * PEP 8 format is applied throughout (including lengths of comment and code lines).
# * No additional code or imports in the notebook that is not needed for the workflow.
# * Notebook is fully reproducible. This means:
#    * reproducible paths using the os module.
#    * data downloaded using code in the notebook.
#    * all imports at top of notebook.

# ## BONUS - Export a  .CSV File to Share (10 points possible)
# 
# This is optional - if you export a **.csv** file with the columns specified above: Site, Date and NDVI Value you can get an additional 10 points.
# 
# * FULL CREDIT: File exists in csv format and contains the columns specified.
# We will check your github repo for this file!
# 
