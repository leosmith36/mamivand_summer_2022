from paraview.simple import *
import os

# This file uses paraview to get a microstructure image for Fe from each exodus file

def run(file,name,output,img_name):

    #### disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()

    # create a new 'IOSS Reader'
    reader = IOSSReader(registrationName=name, FileName=[file])

    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    display = Show(reader, renderView1, 'UnstructuredGridRepresentation')

    # trace defaults for the display properties.
    display.Representation = 'Surface'

    # reset view to fit data
    renderView1.ResetCamera(False)

    #changing interaction mode based on data extents
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [100.0, 100.0, 10000.0]
    renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(display, ('CELLS', 'fe'))

    # rescale color and/or opacity maps used to include current data range
    display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'fe'
    feLUT = GetColorTransferFunction('fe')

    # get opacity transfer function/opacity map for 'fe'
    fePWF = GetOpacityTransferFunction('fe')

    # Hide orientation axes
    renderView1.OrientationAxesVisibility = 0

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    feLUT.ApplyPreset('Grayscale', True)

    # hide color bar/color legend
    display.SetScalarBarVisibility(renderView1, False)

    # show color bar/color legend
    display.SetScalarBarVisibility(renderView1, True)

    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(1304, 540)

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [100.0, 100.0, 10000.0]
    renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]
    renderView1.CameraParallelScale = 141.4213562373095

    # save screenshot
    SaveScreenshot(os.path.join(output,img_name), renderView1, ImageResolution=[1304, 540],
        TransparentBackground=1)

    #================================================================
    # addendum: following script captures some of the application
    # state to faithfully reproduce the visualization during playback
    #================================================================

    #--------------------------------
    # saving layout sizes for layouts

    # layout/tab size in pixels
    layout1.SetSize(1304, 540)

    #-----------------------------------
    # saving camera placements for views

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [100.0, 100.0, 10000.0]
    renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]
    renderView1.CameraParallelScale = 141.4213562373095

    #--------------------------------------------
    # uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).