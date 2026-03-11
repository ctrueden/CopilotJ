/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import type { MaybeRef } from "vue";
import {
  computed,
  isRef,
  nextTick,
  onActivated,
  onDeactivated,
  onMounted,
  onUnmounted,
  ref,
  shallowRef,
  unref,
  watch,
} from "vue";

type ScrollContainer = HTMLElement | null | undefined;

type UseCustomScrollOptions = {
  // top offset: determine "arrived" when approaching threshold
  offsetTop?: number;

  // bottom offset: determine "arrived" when approaching threshold
  offsetBottom?: number;

  // behavior of window.scrollTo
  behavior?: ScrollBehavior;

  // whether event listener is passive (recommended true for performance)
  passive?: boolean;

  /**
   * scroll event throttling:
   * - 'raf': merge with requestAnimationFrame
   * - number: throttle with timer in milliseconds
   * - null: no throttling
   */
  throttle?: number | "frame" | null;

  // whether to re-measure on ResizeObserver changes
  measureOnResize?: boolean;
};

export function useCustomScroll(containerRef: MaybeRef<ScrollContainer>, options: UseCustomScrollOptions = {}) {
  const {
    offsetTop = 0,
    offsetBottom = 32,
    behavior = "smooth",
    passive = true,
    throttle = "frame",
    measureOnResize = true,
  } = options;

  // state
  const y = ref(0);
  const prevY = ref(0);
  const direction = computed<"up" | "down" | "none">(() => {
    if (y.value === prevY.value) return "none";
    return y.value > prevY.value ? "down" : "up";
  });

  const arrivedTop = ref(true);
  const arrivedBottom = ref(false);
  const isScrolling = ref(false);
  const scrollHeight = ref(0);
  const clientHeight = ref(0);

  // internals
  const cleanupFns: Array<() => void> = [];
  const ro = shallowRef<ResizeObserver | null>(null);
  let ticking = false;
  let throttleTimer: number | null = null;

  const _measureCore = (el: HTMLElement) => {
    const top = el.scrollTop;
    prevY.value = y.value;
    y.value = top;
    scrollHeight.value = el.scrollHeight;
    clientHeight.value = el.clientHeight;

    arrivedTop.value = top <= offsetTop;
    arrivedBottom.value = top + el.clientHeight >= el.scrollHeight - offsetBottom;
  };

  const measure = () => {
    const el = unref(containerRef);
    if (!el) return;
    _measureCore(el);
  };

  // throttled/frame scroll handler
  const handleScroll = () => {
    const el = unref(containerRef);
    if (!el) return;

    if (throttle === "frame") {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        _measureCore(el);
        ticking = false;
      });
      return;
    }

    if (typeof throttle === "number" && throttle > 0) {
      if (throttleTimer != null) return;
      throttleTimer = window.setTimeout(() => {
        _measureCore(el);
        throttleTimer = null;
      }, throttle) as unknown as number;
      return;
    }

    _measureCore(el);
  };

  // scroll APIs
  const scrollTo = (top: number) => {
    const el = unref(containerRef);
    if (!el) return;
    el.scrollTo({ top, behavior });
  };

  const scrollBy = (delta: number) => {
    const el = unref(containerRef);
    if (!el) return;
    el.scrollTo({
      top: el.scrollTop + delta,
      behavior,
    });
  };

  const scrollToTop = () => scrollTo(0);

  const scrollToBottom = () => {
    const el = unref(containerRef);
    if (!el) return;
    el.scrollTo({
      top: el.scrollHeight - el.clientHeight,
      behavior,
    });
    // To ensure measurement is in post-scroll state, measure in next frame
    requestAnimationFrame(measure);

    // Additionally: delay once more to accommodate asynchronous content expansion
    setTimeout(measure, 0);
    setTimeout(measure, 50);

    // If you want to leave a bottom offset when scrolling to bottom, you can use:
    // el.scrollTo({ top: Math.max(0, el.scrollHeight - el.clientHeight - offsetBottom), behavior })
  };

  // ---- listeners setup/cleanup
  const setupScrollListener = (el: HTMLElement) => {
    el.addEventListener("scroll", onScroll, { passive: passive ?? true });
    cleanupFns.push(() => el.removeEventListener("scroll", onScroll));
  };

  const onScroll = (evt: Event) => {
    isScrolling.value = true;
    handleScroll();
    // Reset isScrolling at the end of a macro task, indicating this scroll cycle is complete (approximate)
    queueMicrotask(() => {
      isScrolling.value = false;
    });
  };

  const setupResizeObserver = (el: HTMLElement) => {
    if (!("ResizeObserver" in window) || !measureOnResize) return;
    const observer = new ResizeObserver(() => {
      // Re-measure when container size changes or content reflows
      measure();
    });
    observer.observe(el);
    ro.value = observer;
    cleanupFns.push(() => {
      observer.disconnect();
      ro.value = null;
    });
  };

  const setup = (el: HTMLElement) => {
    setupScrollListener(el);
    setupResizeObserver(el);
    // Initial measurement: first nextTick wait for DOM stable, then measure + add another frame
    nextTick(() => {
      measure();
      requestAnimationFrame(measure);
    });
  };

  const cleanup = () => {
    cleanupFns.splice(0).forEach((fn) => {
      try {
        fn();
      } catch {}
    });
    if (throttleTimer != null) {
      clearTimeout(throttleTimer);
      throttleTimer = null;
    }
    ticking = false;
  };

  // ---- lifecycle
  onMounted(() => {
    const el = unref(containerRef);
    if (el) setup(el as HTMLElement);
  });

  onUnmounted(() => {
    cleanup();
  });

  // Support keep-alive: re-measure on activation to avoid inaccurate status due to size/content changes
  onActivated(() => {
    requestAnimationFrame(measure);
  });
  onDeactivated(() => {
    // Process as needed
  });

  // Rebind when container reference changes
  if (isRef(containerRef)) {
    watch(
      containerRef,
      (el, oldEl) => {
        if (oldEl) cleanup();
        if (el) setup(el as HTMLElement);
      },
      { flush: "post" },
    );
  }

  return {
    // state
    y,
    direction,
    arrivedTop,
    arrivedBottom,
    isScrolling,
    scrollHeight,
    clientHeight,

    // actions
    measure,
    scrollTo,
    scrollBy,
    scrollToTop,
    scrollToBottom,
  };
}
