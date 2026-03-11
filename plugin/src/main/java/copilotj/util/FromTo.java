/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package copilotj.util;

public class FromTo<T> {
  public final T from;
  public final T to;

  public FromTo(final T from, final T to) {
    this.from = from;
    this.to = to;
  }
}
