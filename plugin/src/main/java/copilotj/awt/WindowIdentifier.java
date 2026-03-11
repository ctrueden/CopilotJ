/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package copilotj.awt;

import java.awt.Window;
import java.util.Map;
import java.util.WeakHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class WindowIdentifier {

  private final Map<Window, Integer> windowToIdMap = new WeakHashMap<>();
  private final AtomicInteger nextId = new AtomicInteger(0);

  /**
   * Gets a unique ID for the given AWT Window.
   * <p>
   * The ID is generated on the first call for a specific window instance
   * and will be consistent for subsequent calls for the same instance.
   * This mechanism uses a {@link WeakHashMap}, so it does not prevent windows
   * from being garbage collected. If a window is garbage collected, its ID
   * may be reused for a new window instance later.
   * </p>
   *
   * @param window The AWT Window for which to get an ID. Must not be null.
   * @return A unique integer ID for the window.
   * @throws IllegalArgumentException if the window is null.
   */
  public synchronized int getId(final Window window) {
    if (window == null) {
      throw new IllegalArgumentException("Window cannot be null");
    }
    // computeIfAbsent ensures that the ID is generated only once per window
    // and that the operation is atomic for the map under the synchronized method.
    // The WeakHashMap ensures that when the window is garbage collected,
    // its entry in the map can also be removed.
    return windowToIdMap.computeIfAbsent(window, k -> nextId.getAndIncrement());
  }
}
