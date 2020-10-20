from urllib.parse import urlparse
import gdal 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyproj
from functools import partial
import numbers
from sklearn.cluster import DBSCAN, KMeans

def get_vsi_url(enclosure, username=None, api_key=None):
    
    
    parsed_url = urlparse(enclosure)

    if(username != None):
        url = '/vsicurl/{}://{}:{}@{}/api{}'.format(list(parsed_url)[0],
                                            username, 
                                            api_key, 
                                            list(parsed_url)[1],
                                            list(parsed_url)[2])
    else:
        url = '/vsicurl/{}://{}/api{}'.format(list(parsed_url)[0],
                                            list(parsed_url)[1],
                                            list(parsed_url)[2])        
    
    return url 

def vsi_download(url, bbox, username=None, api_key=None):
    
    vsi_url = get_vsi_url(url, username, api_key)
    print(vsi_url)
    
    ulx, uly, lrx, lry = bbox[0], bbox[3], bbox[2], bbox[1] 
    
    # load VSI URL in memory
    output = '/vsimem/subset.tif'
    
    ds = gdal.Open(vsi_url)
    
    ds = gdal.Translate(destName=output, 
                        srcDS=ds, 
                        projWin = [ulx, uly, lrx, lry], 
                        projWinSRS = 'EPSG:4326',
                        outputType=gdal.GDT_Float32)
    ds = None
    
    # create a numpy array
    ds = gdal.Open(output)
    
    layers = []

    for i in range(1, ds.RasterCount+1):
        layers.append(ds.GetRasterBand(i).ReadAsArray())

    return np.dstack(layers)

def read_raster_band(path,band):
    ds = gdal.Open(path)

    return ds.GetRasterBand(band).ReadAsArray()

 
def load_image(path):
        
    # create a numpy array
    ds = gdal.Open(path)
    
    layers = []

    for i in range(1, ds.RasterCount+1):
        layers.append(ds.GetRasterBand(i).ReadAsArray())

    return np.dstack(layers)
    
def plot_bands_row(image,vmin=0,vmax=255,cmap=plt.cm.gray, colormap=False):

    #to support single bands
    if(image.ndim == 2):
        image=np.expand_dims(image, axis=-1)
        
    columns=image.shape[2]
    fig = plt.figure(figsize=(20,20))
    for i in range(0, columns):
        a=fig.add_subplot(1, columns, i+1)
        width = 12
        height = 12
        data=image[:,:,i]
        imgplot = plt.imshow(data.reshape(data.shape[0],data.shape[1]), cmap=cmap , vmin=vmin, vmax=vmax)
        if(colormap):
            plt.colorbar(imgplot,fraction=0.046, pad=0.04)

    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    
def plot_rgb(red,green,blue):
    data = np.dstack((red, 
                       green,
                       blue)).astype(np.uint8) 

       
    #fig = plt.figure(figsize=(20,20))
    #a=fig.add_subplot(1, 1, 1)
    img = Image.fromarray(data)
    imgplot = plt.imshow(img)
    
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
      

def image_histogram_equalization(image, number_bins=256):
    # from http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html

    # get image histogram
    image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
    cdf = image_histogram.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

    return image_equalized.reshape(image.shape), cdf

def project_coords(coords, from_proj, to_proj):
    if len(coords) < 1:
        return []

    if isinstance(coords[0], numbers.Number):
        from_x, from_y = coords
        to_x, to_y = pyproj.transform(from_proj, to_proj, from_x, from_y)
        return [to_x, to_y]

    new_coords = []
    for coord in coords:
        new_coords.append(project_coords(coord, from_proj, to_proj))
    return new_coords

def project_feature(feature, from_proj, to_proj):
    if not 'geometry' in feature or not 'coordinates' in feature['geometry']:
        print('Failed project feature', feature)
        return None

    new_coordinates = project_coords(feature['geometry']['coordinates'], from_proj, to_proj)
    feature['geometry']['coordinates'] = new_coordinates
    return feature

def convert2byte(array, minSource, maxSource):
    arrayflatten = array.flatten()
    byteArray = np.zeros(len(arrayflatten)).astype(np.uint8)
    for index in range(len(arrayflatten)):
        if (arrayflatten[index]<minSource):
            byteArray[index]=0
        elif (arrayflatten[index]>maxSource):
            byteArray[index]=255
        else:
            byteArray[index]= ((arrayflatten[index]-minSource) * 255/(maxSource-minSource)).astype(np.uint8)
    return byteArray.reshape(array.shape)

def km_clust(array, n_clusters):
    
    # Create a line array, the lazy way
    X = array.reshape((-1, 1))
    # Define the k-means clustering problem
    k_m = KMeans(n_clusters=n_clusters, n_init=4)
    # Solve the k-means clustering problem
    k_m.fit(X)
    # Get the coordinates of the clusters centres as a 1D array
    values = k_m.cluster_centers_.squeeze()
    # Get the label of each point
    labels = k_m.labels_
    return(values, labels)
'''
def db_clust(array, eps, min_samples):
    
    # Create a line array, the lazy way
    X = array.reshape((-1, 1))
    # Define the k-means clustering problem
    k_m = DBSCAN(eps=eps, min_samples=min_samples)
    # Solve the k-means clustering problem
    k_m.fit(X)
    # Get the coordinates of the clusters centres as a 1D array
    values = k_m.cluster_centers_.squeeze()
    # Get the label of each point
    labels = k_m.labels_
    return(values, labels)
'''