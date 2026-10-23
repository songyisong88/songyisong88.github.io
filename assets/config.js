/* Kairon Arcade site config — the ONLY file to edit when ads are approved or a custom domain is added.
   adTest:   true  -> show empty ad-slot boxes labelled "โฆษณา" (placement preview only, no ad scripts).
             false -> every ad placeholder box is hidden completely (display:none).
   adClient: ''    -> later 'ca-pub-XXXXXXXXXXXXXXXX' after Song-yi approves AdSense. Empty = no ads ever.
   adHosts:  real ads may only render when location.hostname is in this list.
             Add a future custom domain here (e.g. 'kaironarcade.com', 'www.kaironarcade.com'). */
window.KA_CONFIG={
  adTest:true,
  adClient:'',
  adHosts:['songyisong88.github.io']
};
