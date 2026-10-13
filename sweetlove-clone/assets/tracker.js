/**
 * Wedding Website Analytics & Tracking Pixel Engine
 * Bukola & Olaoluwa Wedding 2026
 *
 * Supports:
 * - Vercel Web Analytics (Privacy-friendly, native)
 * - Google Analytics 4 (gtag.js)
 * - Meta Pixel (Facebook / Instagram fbevents.js)
 * - Google Tag Manager (GTM)
 * - Unified window.trackEvent() dispatcher
 */
(function () {
  'use strict';

  var config = window.TRACKING_CONFIG || {};

  // Check URL query parameters for dynamic overrides (useful for testing or ad campaigns)
  try {
    var params = new URLSearchParams(window.location.search);
    if (params.get('ga')) config.googleAnalyticsId = params.get('ga');
    if (params.get('meta') || params.get('fbpixel')) config.metaPixelId = params.get('meta') || params.get('fbpixel');
    if (params.get('gtm')) config.googleTagManagerId = params.get('gtm');
  } catch (e) {}

  var isDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  var isDebug = isDev || window.location.search.indexOf('debug_tracking=true') !== -1;

  function log() {
    if (isDebug && window.console && window.console.log) {
      window.console.log.apply(window.console, ['[Tracker]'].concat(Array.prototype.slice.call(arguments)));
    }
  }

  // 1. Initialize Vercel Analytics
  if (config.vercelAnalytics !== false) {
    try {
      window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
      var vaScript = document.createElement('script');
      vaScript.defer = true;
      vaScript.src = '/_vercel/insights/script.js';
      vaScript.onerror = function () {
        // Fallback to Vercel direct CDN if running locally or preview
        var cdnScript = document.createElement('script');
        cdnScript.defer = true;
        cdnScript.src = 'https://va.vercel-scripts.com/v1/script.js';
        document.head.appendChild(cdnScript);
      };
      document.head.appendChild(vaScript);
      log('Vercel Analytics initialized');
    } catch (err) {
      log('Vercel Analytics init error:', err);
    }
  }

  // 2. Initialize Google Analytics (GA4)
  if (config.googleAnalyticsId && typeof config.googleAnalyticsId === 'string' && config.googleAnalyticsId.trim()) {
    var gaId = config.googleAnalyticsId.trim();
    try {
      window.dataLayer = window.dataLayer || [];
      window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      window.gtag('config', gaId, {
        send_page_view: true,
        page_title: document.title,
        page_location: window.location.href
      });

      var gaScript = document.createElement('script');
      gaScript.async = true;
      gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaId);
      document.head.appendChild(gaScript);
      log('Google Analytics (GA4) initialized with ID:', gaId);
    } catch (err) {
      log('Google Analytics init error:', err);
    }
  }

  // 3. Initialize Google Tag Manager (GTM)
  if (config.googleTagManagerId && typeof config.googleTagManagerId === 'string' && config.googleTagManagerId.trim()) {
    var gtmId = config.googleTagManagerId.trim();
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
      var gtmScript = document.createElement('script');
      gtmScript.async = true;
      gtmScript.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(gtmId);
      document.head.appendChild(gtmScript);
      log('Google Tag Manager initialized with ID:', gtmId);
    } catch (err) {
      log('Google Tag Manager init error:', err);
    }
  }

  // 4. Initialize Meta Pixel (Facebook / Instagram)
  if (config.metaPixelId && typeof config.metaPixelId === 'string' && config.metaPixelId.trim()) {
    var pixelId = config.metaPixelId.trim();
    try {
      (function (f, b, e, v, n, t, s) {
        if (f.fbq) return;
        n = f.fbq = function () {
          n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
        };
        if (!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = !0;
        n.version = '2.0';
        n.queue = [];
        t = b.createElement(e);
        t.async = !0;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t, s);
      })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

      window.fbq('init', pixelId);
      window.fbq('track', 'PageView');
      log('Meta Pixel initialized with ID:', pixelId);
    } catch (err) {
      log('Meta Pixel init error:', err);
    }
  }

  // 5. Unified Event Tracking Function
  window.trackEvent = function (eventName, eventParams) {
    eventParams = eventParams || {};
    log('Event Dispatched:', eventName, eventParams);

    // Vercel Analytics Event
    try {
      if (typeof window.va === 'function') {
        window.va('event', { name: eventName, ...eventParams });
      }
    } catch (e) {
      log('Vercel track error:', e);
    }

    // Google Analytics (GA4)
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, eventParams);
      }
    } catch (e) {
      log('GA track error:', e);
    }

    // Google Tag Manager dataLayer
    try {
      if (window.dataLayer && Array.isArray(window.dataLayer)) {
        window.dataLayer.push({
          event: eventName,
          ...eventParams
        });
      }
    } catch (e) {
      log('GTM track error:', e);
    }

    // Meta Pixel
    try {
      if (typeof window.fbq === 'function') {
        if (eventName === 'rsvp_submitted') {
          // Standard Meta Lead event
          window.fbq('track', 'Lead', {
            content_name: 'Wedding RSVP',
            status: eventParams.attending || 'Joyfully Accept'
          });
        } else if (eventName === 'calendar_add') {
          window.fbq('trackCustom', 'AddToCalendar', eventParams);
        } else if (eventName === 'envelope_opened') {
          window.fbq('trackCustom', 'EnvelopeOpened', eventParams);
        } else if (eventName === 'map_opened') {
          window.fbq('trackCustom', 'ViewDirections', eventParams);
        } else {
          window.fbq('trackCustom', eventName, eventParams);
        }
      }
    } catch (e) {
      log('Meta track error:', e);
    }

    // Dispatch a native CustomEvent so any listener can tap into it
    try {
      window.dispatchEvent(new CustomEvent('wedding:track', {
        detail: { event: eventName, params: eventParams }
      }));
    } catch (e) {}
  };

  log('Tracking engine loaded and ready.');
})();
