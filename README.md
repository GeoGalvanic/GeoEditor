# GeoEditor

The **GeoEditor** is a light-weight desktop application for interactively editing Geodata files (currently only Shapefiles). 

## Features

* **Adding GeoData as layers to application**
  
  Upon opening the application the user will be greeted by a blank screen. To add data use one of the following options:
  * Create a new layer
  
    From the menu bar at the top select the `Layers` menu then select the `Add New Layer` button. If there is no data currently in the map it will zoom to the extents of this new layer (currently only works for polygons, see issue #)
    
  * ~~Add an existing layer from a saved file~~ (Not implemented: see #3)
  
    In the future users will be able to load layers created in this application from a file.
    
* **Interactive Map Frame**

  Matplotlib has its own navigation toolbar for interactive plots, notable including:
  * A pan tool that can also zoom by right-click dragging
  * A rectangular zoom tool
  
  More details can be found from matplotlib's [interactive navigation page](https://matplotlib.org/3.2.2/users/navigation_toolbar.html)
  
* **Attribute Editor Window**

  Clicking on any shape within the figure will open an attribute editor window from which the attribute data can be viewed. Attributes can be edited and then stored using the apply button or reset using the discard button. If another shape is clicked while the editor is open, it will placed into the dropdown box of the attribute editor where you can switch between editing the different features. To remove a single item from the dropdown box you can click the X button beneath it. The number next to the X button indicates the number of entities that are currently stored in the dropdown of the editor.
  
* **Layer Menu**

  Once a layer has been added, it will be placed inside of the layers menu. Under each layer's menu are a few convenience items:
  * Change the name of the layer (shown in the attribute layers menu and in the attribute editor drop downs)
  * Change the display name field for geometry in the layer (shown in attribute editor window)
  * Turning the selectability for layers on/off to prevent picking background layers
  * Remove layer

* **Save Data**

  There are two options for saving data to an output file in the layer menu:
  * Save source data: This option will overwrite the data file that was used to create the layer
  * Save new data file: Saves a copy of the edited data in a new file (does not reset the source of the layer)

* **Change Symbology** (currently points only)

  In the layer menu there is an option to change symbology.

### Dependencies

* [Matplotlib](https://github.com/matplotlib/matplotlib) v3.3.2

  Matplotlib is used for displaying interactive maps (graphs) of GeoData and 
* [Geopandas](https://github.com/geopandas/geopandas) v0.6.1

  Geopandas is used for opening geodata files, using GeoDataFrames to track attribute edits, plotting geometry to matplotlib and 
  
## To Do
See https://github.com/GeoGalvanic/GeoEditor/issues

