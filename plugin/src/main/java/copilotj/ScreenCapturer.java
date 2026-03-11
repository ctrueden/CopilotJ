/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package copilotj;

import java.awt.Frame;
import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;
import java.awt.IllegalComponentStateException;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.image.BufferedImage;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import copilotj.awt.WindowIdentifier;
import copilotj.awt.window.IjImage;

import ij.IJ;
import ij.ImagePlus;
import ij.WindowManager;

public class ScreenCapturer {
  public static class CaptureImageRequest {
    public String title;
  }

  private final int maxWidth; // Max width for downsizing
  private final int maxHeight; // Max height for downsizing
  private final WindowIdentifier identifier;

  public ScreenCapturer(final int maxWidth, final int maxHeight, final WindowIdentifier identifier) {
    this.maxWidth = maxWidth;
    this.maxHeight = maxHeight;
    this.identifier = identifier;
  }

  public ScreenCapturer(final WindowIdentifier identifier) {
    this(512, 512, identifier);
  }

  public static class ScreenPreviews {
    public final List<IjImage.ImagePreview> screenshots;
    public final int countScreen;

    public ScreenPreviews(final List<IjImage.ImagePreview> screenshots, final int countScreen) {
      this.screenshots = screenshots;
      this.countScreen = countScreen;
    }
  }

  public ScreenPreviews captureScreen() {
    try {
      final Set<GraphicsDevice> screens = this.getImageJScreens();

      final List<IjImage.ImagePreview> previews = new java.util.ArrayList<>();
      for (GraphicsDevice device : screens) {
        // Capture the screen area containing ImageJ
        final Rectangle bounds = device.getDefaultConfiguration().getBounds();
        final BufferedImage screenshot = new Robot(device).createScreenCapture(bounds);
        final String title = "screenshot_" + device.getIDstring().replaceAll("[^a-zA-Z0-9]", "_");
        previews.add(new IjImage.ImagePreview(title, screenshot, maxWidth, maxHeight));
      }
      return new ScreenPreviews(previews, screens.size());

    } catch (final Exception e) {
      IJ.log("Error capturing screen: " + e.getMessage());
      return null;
    }
  }

  // TODO: fully remove this method
  public IjImage.ImagePreviewWithInfo captureImage(final CaptureImageRequest request) {
    if (WindowManager.getImageTitles().length == 0) {
      throw new IllegalArgumentException("There are no image opened.");
    }

    ImagePlus imp;
    if (request.title == null) {
      imp = IJ.getImage();

    } else {
      imp = WindowManager.getImage(request.title);
      if (imp == null) {
        final String[] titles = WindowManager.getImageTitles();
        final String opened = titles.length > 1
            ? "opened images: " + String.join(", ", titles)
            : "only image titled \"" + titles[0] + "\" opened.";

        throw new IllegalArgumentException(
            "There is no image titled \"" + request.title + "\" opened, " + opened);
      }
    }

    return IjImage.captureImage(this.identifier, imp, maxWidth, maxHeight);
  }

  private Set<GraphicsDevice> getImageJScreens() {
    final Set<GraphicsDevice> devicesWithImageJ = new HashSet<>();

    // Iterate through all open frames to find those that are showing ImageJ
    for (final Frame frame : Frame.getFrames()) {
      if (!frame.isShowing())
        continue;

      try {
        // Get the screen location of the window
        final Point loc = frame.getLocationOnScreen();

        // Get the GraphicsDevice for the window's location
        final GraphicsDevice device = getScreenDeviceAt(loc);
        if (device != null) {
          devicesWithImageJ.add(device);
        }

      } catch (final IllegalComponentStateException ignored) {
        // This exception can occur if the frame is not fully initialized
      }
    }

    return devicesWithImageJ;
  }

  private GraphicsDevice getScreenDeviceAt(final Point point) {
    final GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
    for (final GraphicsDevice gd : ge.getScreenDevices()) {
      final Rectangle bounds = gd.getDefaultConfiguration().getBounds();
      if (bounds.contains(point)) {
        return gd;
      }
    }
    return null;
  }
}
