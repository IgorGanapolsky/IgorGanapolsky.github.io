window.resumeOSAnalytics = (function () {
  var config = {
    plausibleDomain: "igorganapolsky.github.io",
    gaMeasurementId: "G-2GEM6RYXZE",
    posthogKey: window.RESUMEOS_POSTHOG_KEY || window.APPLYOPS_POSTHOG_KEY || "",
    posthogHost: "https://us.i.posthog.com",
  };
  var eventNames = {
    checkoutClick: "checkout_click",
    checkoutAbandonReason: "checkout_abandon_reason",
    leadClick: "lead_click",
    intakeSubmit: "intake_submit",
    offerObjectionClick: "offer_objection_click",
    purchaseSuccess: "purchase_success",
  };
  var utmKeys = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
  ];

  window.plausible =
    window.plausible ||
    function () {
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };

  window.dataLayer = window.dataLayer || [];
  window.gtag =
    window.gtag ||
    function () {
      window.dataLayer.push(arguments);
    };
  window.gtag("js", new Date());
  window.gtag("config", config.gaMeasurementId);

  function initPostHog() {
    if (window.__resumeOSPostHogLoaded || !config.posthogKey) return;
    window.__resumeOSPostHogLoaded = true;
    !(function (t, e) {
      var o, n, p, r;
      e.__SV ||
        ((window.posthog = e),
        (e._i = []),
        (e.init = function (i, s, a) {
          function g(t, e) {
            var o = e.split(".");
            (2 == o.length && ((t = t[o[0]]), (e = o[1])),
              (t[e] = function () {
                t.push([e].concat(Array.prototype.slice.call(arguments, 0)));
              }));
          }
          (((p = t.createElement("script")).type = "text/javascript"),
            (p.async = !0),
            (p.src = s.api_host + "/static/array.js"),
            (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(
              p,
              r,
            ));
          var u = e;
          for (
            void 0 !== a ? (u = e[a] = []) : (a = "posthog"),
              u.people = u.people || [],
              u.toString = function (t) {
                var e = "posthog";
                return (
                  "posthog" !== a && (e += "." + a),
                  t || (e += " (stub)"),
                  e
                );
              },
              u.people.toString = function () {
                return u.toString(1) + ".people (stub)";
              },
              o =
                "capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(
                  " ",
                ),
              n = 0;
            n < o.length;
            n++
          )
            g(u, o[n]);
          e._i.push([i, s, a]);
        }),
        (e.__SV = 1));
    })(document, window.posthog || []);
    window.posthog.init(config.posthogKey, { api_host: config.posthogHost });
  }

  function cleanProps(props) {
    var out = {};
    Object.keys(props || {}).forEach(function (key) {
      if (
        props[key] !== "" &&
        props[key] !== null &&
        typeof props[key] !== "undefined"
      ) {
        out[key] = props[key];
      }
    });
    return out;
  }

  function attributionProps() {
    var params = new URLSearchParams(window.location.search);
    var props = {
      page_path: location.pathname,
      page_title: document.title,
      referrer: document.referrer || undefined,
    };
    utmKeys.forEach(function (key) {
      var value = params.get(key);
      if (value) props[key] = value;
    });
    return props;
  }

  function track(eventName, props) {
    var payload = cleanProps(
      Object.assign({}, attributionProps(), props || {}),
    );
    try {
      window.plausible(eventName, { props: payload });
    } catch (_) {}
    try {
      window.gtag("event", eventName, payload);
    } catch (_) {}
    try {
      if (window.posthog && typeof window.posthog.capture === "function") {
        window.posthog.capture(eventName, payload);
      }
    } catch (_) {}
  }

  function shouldDelayNavigation(event, node) {
    if (event.defaultPrevented) return false;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
      return false;
    if (node.target && node.target !== "_self") return false;
    var href = node.getAttribute("href") || "";
    return /^https:\/\/buy\.stripe\.com\//.test(href) || /^mailto:/.test(href);
  }

  function bindTrackedLinks() {
    document.querySelectorAll("[data-track]").forEach(function (node) {
      if (node.dataset.analyticsBound === "true") return;
      node.dataset.analyticsBound = "true";
      node.addEventListener("click", function (event) {
        var href = node.getAttribute("href");
        track(node.dataset.track, {
          tier: node.dataset.tier,
          price: node.dataset.price ? Number(node.dataset.price) : undefined,
          placement: node.dataset.placement,
          reason: node.dataset.reason,
          surface: node.dataset.surface || location.pathname,
          href: href,
          client_reference_id: new URL(
            node.href,
            location.href,
          ).searchParams.get("client_reference_id"),
        });
        if (href && shouldDelayNavigation(event, node)) {
          event.preventDefault();
          window.setTimeout(function () {
            window.location.href = href;
          }, 180);
        }
      });
    });
  }

  function bindTrackedForms() {
    document
      .querySelectorAll("form[data-track-submit]")
      .forEach(function (node) {
        if (node.dataset.analyticsBound === "true") return;
        node.dataset.analyticsBound = "true";
        node.addEventListener("submit", function () {
          track(node.dataset.trackSubmit, {
            surface: node.dataset.surface || location.pathname,
            placement: node.dataset.placement,
          });
        });
      });
  }

  function bindObjectionCapture() {
    if (window.__resumeOSObjectionCaptureBound) return;
    window.__resumeOSObjectionCaptureBound = true;

    var checkoutSeen = false;
    var surveyShown = false;

    function hasCheckoutSurface() {
      return Boolean(document.querySelector("[data-track='checkout_click']"));
    }

    function isEligiblePath() {
      return /^(resumeos\/?|applyops\/?)$/.test(location.pathname.replace(/^\/+/, ""));
    }

    function isEligibleForSurvey() {
      return isEligiblePath() || hasCheckoutSurface();
    }

    document.addEventListener(
      "click",
      function (event) {
        var target = event.target && event.target.closest
          ? event.target.closest("[data-track='checkout_click']")
          : null;
        if (target) {
          checkoutSeen = true;
          try {
            sessionStorage.setItem("resumeos_checkout_seen", "true");
          } catch (_) {}
        }
      },
      true,
    );

    function buildSurvey() {
      var wrap = document.createElement("aside");
      wrap.setAttribute("aria-label", "Purchase feedback");
      wrap.style.cssText =
        "position:fixed;right:16px;bottom:16px;z-index:9999;width:min(320px,calc(100vw - 32px));background:#111827;color:#f9fafb;border:1px solid #374151;border-radius:8px;box-shadow:0 16px 40px rgba(0,0,0,.35);padding:14px;font:14px/1.4 system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif";
      wrap.innerHTML =
        '<button type="button" data-survey-close aria-label="Close feedback" style="float:right;background:transparent;border:0;color:#9ca3af;font-size:18px;line-height:1;cursor:pointer">x</button>' +
        '<strong style="display:block;margin:0 24px 8px 0;font-size:14px">Not buying today?</strong>' +
        '<div style="display:grid;gap:8px">' +
        '<button type="button" data-reason="price_unclear">Price or scope unclear</button>' +
        '<button type="button" data-reason="need_sample">Need a better sample</button>' +
        '<button type="button" data-reason="not_urgent">Not urgent right now</button>' +
        '<button type="button" data-reason="trust_gap">Need more proof first</button>' +
        "</div>";
      Array.prototype.forEach.call(wrap.querySelectorAll("button[data-reason]"), function (btn) {
        btn.style.cssText =
          "text-align:left;border:1px solid #374151;background:#1f2937;color:#f9fafb;border-radius:6px;padding:8px 10px;cursor:pointer";
        btn.addEventListener("click", function () {
          track(eventNames.checkoutAbandonReason, {
            reason: btn.getAttribute("data-reason"),
            checkout_seen: checkoutSeen ? "true" : "false",
            surface: location.pathname,
          });
          wrap.remove();
        });
      });
      wrap.querySelector("[data-survey-close]").addEventListener("click", function () {
        track(eventNames.offerObjectionClick, {
          action: "dismiss",
          checkout_seen: checkoutSeen ? "true" : "false",
          surface: location.pathname,
        });
        wrap.remove();
      });
      return wrap;
    }

    function showSurvey(trigger) {
      if (!isEligibleForSurvey() || surveyShown || document.querySelector("[aria-label='Purchase feedback']")) return;
      surveyShown = true;
      track(eventNames.offerObjectionClick, {
        action: "shown",
        trigger: trigger,
        checkout_seen: checkoutSeen ? "true" : "false",
        surface: location.pathname,
      });
      document.body.appendChild(buildSurvey());
    }

    window.setTimeout(function () {
      showSurvey("time_on_page_35s");
    }, 35000);
    document.addEventListener("mouseleave", function (event) {
      if (event.clientY <= 0) showSurvey("exit_intent");
    });
    window.addEventListener("pagehide", function () {
      var sawCheckout = checkoutSeen;
      try {
        sawCheckout = sawCheckout || sessionStorage.getItem("resumeos_checkout_seen") === "true";
      } catch (_) {}
      if (!sawCheckout && isEligibleForSurvey()) {
        track(eventNames.offerObjectionClick, {
          action: "left_without_checkout",
          surface: location.pathname,
        });
      }
    });
  }

  function trackSuccessFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var tier = params.get("tier") || "unknown";
    var sessionId = params.get("session_id") || "";
    track("purchase_success", {
      tier: tier,
      stripe_session_id_present: sessionId ? "true" : "false",
      surface: location.pathname,
    });
    track("Purchase", { tier: tier });
  }

  initPostHog();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bindTrackedLinks();
      bindTrackedForms();
      bindObjectionCapture();
    });
  } else {
    bindTrackedLinks();
    bindTrackedForms();
    bindObjectionCapture();
  }

  return {
    config: config,
    track: track,
    trackSuccessFromUrl: trackSuccessFromUrl,
  };
})();
