from urllib.parse import urlparse
import gdal 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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
