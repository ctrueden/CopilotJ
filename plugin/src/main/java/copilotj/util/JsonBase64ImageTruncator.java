/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package copilotj.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JsonBase64ImageTruncator {
  public static class WithTitle extends JsonBase64ImageTruncator {
    final String title;

    public WithTitle(final String title, final String json) {
      super(json, 16);
      this.title = title;
    }

    @Override
    public String toString() {
      return title + ": " + super.toString();
    }
  }

  private static final Pattern BASE64_IMAGE_PATTERN = Pattern.compile("(\"data:image/\\w+;base64,)([^\"]+)(\")");

  // Optional static helper method
  public static String truncateJsonBase64(final String json, final int maxLength) {
    return new JsonBase64ImageTruncator(json, maxLength).toString();
  }

  private final String json;

  private final int maxLength;

  public JsonBase64ImageTruncator(final String json, final int maxLength) {
    this.json = json;
    this.maxLength = maxLength;
  }

  @Override
  public String toString() {
    final Matcher matcher = BASE64_IMAGE_PATTERN.matcher(json);
    final StringBuffer result = new StringBuffer();

    while (matcher.find()) {
      final String prefix = matcher.group(1);
      String content = matcher.group(2);
      final String suffix = matcher.group(3);

      if (content.length() > maxLength) {
        content = content.substring(0, Math.max(0, maxLength - 3)) + "...";
      }

      matcher.appendReplacement(result, Matcher.quoteReplacement(prefix + content + suffix));
    }

    matcher.appendTail(result);
    return result.toString();
  }
}
