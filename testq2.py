#!/usr/bin/env python3

from qgis.core import * #(
    #QgsApplication, QgsRasterLayer, QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry, )
from qgis.gui import * #QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from qgis.PyQt.QtWidgets import * #QDialog, QVBoxLayout, QMainWindow, QApplication
from qgis.PyQt.QtCore import * #Qt, QObject, pyqtSignal
from PyQt5 import uic
import sys, os
import qgis
import qgis.gui, qgis.utils


def set_up_interface(qgis_app, canvas):
    iface = QgisInterface(canvas)

    return qgis_app, canvas, iface

class QMessageBar(QObject):
    def __init__ (self):
        QObject.__init__(self)

    def popWidget(self):
        pass 

#noinspection PyMethodMayBeStatic,PyPep8Naming
class QgisInterface(QObject):
    """Class to expose QGIS objects and functions to plugins.

    This class is here for enabling us to run unit tests only,
    so most methods are simply stubs.
    """
    # currentLayerChanged = pyqtSignal(QgsMapCanvasLayer)

    def __init__(self, canvas):
        """Constructor
        :param canvas:
        """
        QObject.__init__(self)
        self.messageBar = QMessageBar
        self.canvas = canvas
        self.legend_interface = MyLegendInterface()
        self.active_layer = None
        # Set up slots so we can mimic the behaviour of QGIS when layers
        # are added.
        # LOGGER.debug('Initialising canvas...')
        # noinspection PyArgumentList
        # QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayer)
        # noinspection PyArgumentList
        # QgsMapLayerRegistry.instance().layerWasAdded.connect(self.addLayer)
        # noinspection PyArgumentList
        # QgsMapLayerRegistry.instance().removeAll.connect(self.removeAllLayers)

        # For processing module
        self.destCrs = None


    @pyqtSlot('QgsMapLayer')
    def addLayer(self, layer):
        """Handle a layer being added to the registry so it shows up in canvas.

        :param layer: list<QgsMapLayer> list of map layers that were added

        .. note: The QgsInterface api does not include this method, it is added
                 here as a helper to facilitate testing.

        .. note: The addLayer method was deprecated in QGIS 1.8 so you should
                 not need this method much.
        """
        # set the recently added layer as active
        # LOGGER.debug('Layer Count Before: %s' % len(self.canvas.layers()))
        current_layers = self.canvas.layers()
        final_layers = [] + current_layers
        final_layers.append(QgsMapCanvasLayer(layer))
        self.canvas.setLayerSet(final_layers)
        self.active_layer = layer

    @pyqtSlot()
    def removeAllLayers(self):
        """Remove layers from the canvas before they get deleted."""
        self.canvas.setLayerSet([])

    def newProject(self):
        """Create new project."""
        # noinspection PyArgumentList
        QgsMapLayerRegistry.instance().removeAllMapLayers()

    def legendInterface(self):
        """Get the legend."""
        return self.legend_interface

    def activeLayer(self):
        """Get pointer to the active layer (layer selected in the legend)."""
        return self.active_layer

    def setActiveLayer(self, layer):
        """Set the given layer as active.
        :param layer: Layer that shall be set active
        :type layer: QgsMapLayer
        """
        self.active_layer = layer

    class actionAddFeature(object):

        def __init__(self):
            pass

        def trigger(self):
            pass

    class actionZoomToLayer(object):

        def __init__(self):
            pass

        def trigger(self):
            pass

    # ---------------- API Mock for QgsInterface follows -------------------
    def zoomFull(self):
        """Zoom to the map full extent."""
        pass

    def zoomToPrevious(self):
        """Zoom to previous view extent."""
        pass

    def zoomToNext(self):
        """Zoom to next view extent."""
        pass

    def zoomToActiveLayer(self):
        """Zoom to extent of active layer."""
        pass

    def addVectorLayer(self, path, base_name, provider_key):
        """Add a vector layer.

        :param path: Path to layer.
        :type path: str

        :param base_name: Base name for layer.
        :type base_name: str

        :param provider_key: Provider key e.g. 'ogr'
        :type provider_key: str
        """
        pass

    def addRasterLayer(self, path, base_name):
        """Add a raster layer given a raster layer file name

        :param path: Path to layer.
        :type path: str

        :param base_name: Base name for layer.
        :type base_name: str
        """
        pass

    def addToolBarIcon(self, action):
        """Add an icon to the plugins toolbar.

        :param action: Action to add to the toolbar.
        :type action: QAction
        """
        pass

    def removeToolBarIcon(self, action):
        """Remove an action (icon) from the plugin toolbar.

        :param action: Action to add to the toolbar.
        :type action: QAction
        """
        pass

    def addToolBar(self, name):
        """Add toolbar with specified name.

        :param name: Name for the toolbar.
        :type name: str
        """
        pass

    def mapCanvas(self):
        """Return a pointer to the map canvas."""
        return self.canvas

    def mainWindow(self):
        """Return a pointer to the main window.

        In case of QGIS it returns an instance of QgisApp.
        """
        pass

    def addDockWidget(self, area, dock_widget):
        """Add a dock widget to the main window.

        :param area: Where in the ui the dock should be placed.
        :type area:

        :param dock_widget: A dock widget to add to the UI.
        :type dock_widget: QDockWidget
        """
        pass


class MyLegendInterface(object):

    def __init__(self):
        self.layer_visibility = {}

    def setLayerVisible(self, layer, yes_no):
        self.layer_visibility[layer.name()] = yes_no

    def isLayerVisible(self, layer):
        try:
            return self.layer_visibility[layer.name()]
        except KeyError:
            print('Layer {} has not been set (in)visible yet.'.format(layer.name()))
            return False


class MyMapCanvas(object):

    def __init__(self):
        self.layer_set = []

    def layers(self):
        return self.layer_set

    def layer(self, index):
        layer = self.layer_set[index].layer()
        return layer

    def setLayerSet(self, layer_set):
        self.layer_set = layer_set

    def layerCount(self):
        return len(self.layer_set)


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__() 
        uic.loadUi('mainwindow.ui', self) 

        self.parent = parent

        project = QgsProject()
        # mapCanvas = QgsMapCanvas()
        # bridge = QgsLayerTreeMapCanvasBridge(
        #     project.layerTreeRoot(),
        #     mapCanvas
        # )
        # bridge.setCanvasLayers()

        tms = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
        layer = QgsRasterLayer(tms,'OSM', 'wms')

        if layer.isValid():
            print("Basemap loaded successfully!")
            project.instance().addMapLayer(layer)
            
            self.mapCanvas.setExtent(layer.extent())
            self.mapCanvas.setLayers([layer])

        else:
            print("Unable to load basemap.")
            
        self.mapCanvas.show()

        qgis.utils.plugin_paths = ['/usr/share/qgis/python/plugins', os.path.expanduser('~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/'),]
        qgis.utils.updateAvailablePlugins()
        
        qgis_app, canvas, iface = set_up_interface(parent, self.mapCanvas)
        qgis.utils.iface = iface
        
        print (qgis.utils.available_plugins)
        print ("...load:", qgis.utils.loadPlugin(u'qgis2web'))
        print ("...start:", qgis.utils.startPlugin(u'qgis2web'))





if __name__ == '__main__':
    QgsApplication.setPrefixPath('/usr', True)
    print(QgsApplication.showSettings())
    application = QgsApplication([], True)
    application.initQgis()

    mv = MainWindow(application)
    mv.show()

    application.exec()

    # application.exitQgis()
