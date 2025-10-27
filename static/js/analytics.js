/* ==========================================
   analytics.js — scripts de seguimiento
   ========================================== */

/* 🔹 Google Analytics (GA4) */
(function() {
  const gtagScript = document.createElement("script");
  gtagScript.src = "https://www.googletagmanager.com/gtag/js?id=G-M24NDJ63FD";
  gtagScript.async = true;
  document.head.appendChild(gtagScript);

  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag("js", new Date());
  gtag("config", "G-M24NDJ63FD");
})();

/* 🔹 Microsoft Clarity */
(function(c,l,a,r,i,t,y){
  c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
  t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
  y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "po9nb5gcah");

/* 🔹 Omnisend */
(function() {
  window.omnisend = window.omnisend || [];
  omnisend.push(["brandID", "67f74837b7f0a3dba0637399"]);
  omnisend.push(["track", "$pageViewed"]);
  const omni = document.createElement("script");
  omni.type = "text/javascript";
  omni.async = true;
  omni.src = "https://omnisnippet1.com/inshop/launcher-v2.js";
  document.head.appendChild(omni);
})();
