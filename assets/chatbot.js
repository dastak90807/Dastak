/* Ask Dastak 90807: automated, rule-based helper (no AI). v2, Nov 2026 */
(function(){
var DATA={"services": [{"id": "learner-driving-license", "n": "Learner Driving License", "docs": ["CNIC of applicant", "Recent live photograph with white background (upper shoulders)", "Medical certificate (only required if age is above 50)"], "guide": null}, {"id": "renewal-of-learners-driving-license", "n": "Renewal of Learners Driving License", "docs": ["CNIC of applicant", "Recent live photograph with white background (upper shoulders)", "Medical certificate (only required if age is above 50)"], "guide": null}, {"id": "renewal-of-regular-license", "n": "Renewal of Regular License", "docs": ["CNIC of applicant", "Recent live photograph with white background (upper shoulders)", "Old driving license", "FIR (only if the original license was lost)", "Medical certificate (only required if age is above 50)"], "guide": null}, {"id": "duplicate-driving-license", "n": "Duplicate Driving License", "docs": ["CNIC of applicant", "Recent live photograph with white background (upper shoulders)", "FIR (lost license report) from the police station", "Medical certificate (only required if age is above 50)"], "guide": null}, {"id": "renewal-international-driving-license", "n": "Renewal International Driving License", "docs": ["CNIC of applicant", "Valid driving license", "Pakistani passport valid for at least 6 months, with visa", "Recent live photograph with white background (upper shoulders)", "FIR (only if the original license was lost)", "Medical certificate (only required if age is above 50)"], "guide": null}, {"id": "duplicate-international-driving-license", "n": "Duplicate International Driving License", "docs": ["FIR (only if the original driving license is lost): photocopy", "CNIC of applicant: original", "Valid driving license issued by the licensing authority: original", "Pakistani passport valid for at least 6 months, with visa: original", "Live photograph with white background (upper shoulders): original", "Medical certificate (only required if age is above 50 or LTV): original"], "guide": null}, {"id": "character-certificate", "n": "Character Certificate", "docs": ["CNIC of applicant", "Passport", "Authority letter if the applicant is abroad (embassy stamp, or attested by two respectable persons who know the applicant; it must state the length of stay)", "Recent live photograph with white background (upper shoulders)"], "guide": null}, {"id": "general-police-verification", "n": "General Police Verification", "docs": ["CNIC or B-form of applicant", "Authority letter if the applicant is abroad (embassy stamp, or attested by two respectable persons who know the applicant; it must state the length of stay)", "Recent live photograph with white background (upper shoulders)"], "guide": null}, {"id": "tenant-registration", "n": "Tenant Registration", "docs": ["CNIC of house owner", "CNIC of tenant", "Rent agreement", "Live photograph of tenant", "Live photograph of house owner"], "guide": null}, {"id": "loss-report", "n": "Loss Report", "docs": ["CNIC of applicant", "Written complaint by the applicant", "Proof of the lost documents, if available", "Any other supporting document, if available"], "guide": null}, {"id": "crime-report", "n": "Crime Report", "docs": ["CNIC of applicant"], "guide": null}, {"id": "copy-of-fir", "n": "Copy of FIR", "docs": ["CNIC or B-form of applicant", "Reason for needing the copy", "FIR number and police station"], "guide": null}, {"id": "traffic-challan", "n": "Traffic Challan", "docs": ["CNIC or vehicle details (for checking the challan)"], "guide": null}, {"id": "safe-city-challan", "n": "Safe City Challan", "docs": ["Vehicle number or CNIC number"], "guide": null}, {"id": "transfer-of-motor-vehicle", "n": "Transfer of Motor Vehicle", "docs": ["Vehicle number", "CNIC of buyer", "Vehicle file and book/card"], "guide": null}, {"id": "motor-vehicle-registration", "n": "Motor Vehicle Registration", "docs": ["Vehicle number (if bought at e-auction)", "CNIC of buyer", "Vehicle file and book"], "guide": null}, {"id": "token-tax", "n": "Token Tax", "docs": ["Vehicle number"], "guide": null}, {"id": "domicile-certificate", "n": "Domicile Certificate", "docs": ["Application Form P-1", "Recent photograph of applicant", "CNIC or B-form of applicant", "CNIC of father, mother or husband", "Affidavit on prescribed stamp paper", "Recent education certificate", "Utility bill"], "guide": null}, {"id": "duplicate-domicile", "n": "Duplicate Domicile", "docs": ["CNIC or B-form of applicant: original and photocopy", "Hand-written application: original", "Affidavit on prescribed stamp paper: original", "Transfer of Domicile NOC (old district): photocopy", "FIR of the lost domicile certificate: photocopy"], "guide": null}, {"id": "modification-domicile", "n": "Modification Domicile", "docs": ["CNIC or B-form of applicant", "Handwritten application", "Existing domicile certificate"], "guide": null}, {"id": "noc-for-domicile-transfer", "n": "NOC for Domicile Transfer", "docs": ["CNIC or B-form of applicant", "Hand-written application", "Affidavit on prescribed stamp paper", "Transfer of Domicile NOC (old district)"], "guide": null}, {"id": "e-stamping", "n": "E-Stamping", "docs": ["CNIC (verified)"], "guide": null}, {"id": "birth-certificate", "n": "Birth Certificate", "docs": ["Application Form A", "Two recent photographs of the child", "CNIC of applicant", "CNICs of father and mother", "CNIC of grandfather or his death certificate (optional)", "CNICs of two witnesses (home births only)", "Hospital-issued birth certificate", "Vaccination card", "Affidavit on prescribed stamp paper", "Written application with the reason for delay (if applying after 1 year)"], "guide": null}, {"id": "death-certificate", "n": "Death Certificate", "docs": ["Application Form B", "CNIC of the deceased", "CNIC of applicant (a blood relative)", "CNIC of father or husband", "CNICs of two witnesses", "Hospital death slip with cause of death, or CNICs of two witnesses for a home death", "Burial slip from the graveyard committee", "Affidavit on prescribed stamp paper", "Written application with the reason for delay (if late)"], "guide": null}, {"id": "marriage-certificate", "n": "Marriage Certificate", "docs": ["Application form", "Nikah Nama", "CNIC of applicant", "CNICs of bride and groom", "CNICs of the fathers of bride and groom"], "guide": null}, {"id": "divorce-certificate", "n": "Divorce Certificate", "docs": ["Application form", "Nikah Nama", "Arbitration council registration or court order", "CNIC of applicant", "CNICs of both parties", "CNICs of the fathers of both parties", "Three arbitration notices of the Union Council"], "guide": null}, {"id": "general-inquiry-and-guide", "n": "General Inquiry and Guide", "docs": [], "guide": "I give guidance on government procedures. I do not give legal advice."}, {"id": "other-punjab-dastak-services", "n": "Other Punjab Dastak Services", "docs": [], "guide": "The official Dastak portal lists many more Punjab services. Ask me if you are not sure I can help."}], "refund": "Fees are generated by the official Dastak system and paid through its payment options. Muhammad Usman does not receive or hold these government fees and cannot refund, reverse or cancel them. Any refund or cancellation is decided by the relevant government department under the official system's rules. Please check the official Dastak portal or helpline 1202.", "pay": "Fees are generated automatically by the official system. Payment options shown in the Dastak app include PSID (payable through any banking app or mobile wallet), IBFT, JazzCash, Easypaisa and cash on delivery. Available options may vary by service.", "portal": "https://dastak.punjab.gov.pk", "play": "https://play.google.com/store/apps/details?id=pk.pitb.gov.dastakHomeDelivery", "store": "https://apps.apple.com/us/app/dastak-home-delivery/id6479348922", "area": "Doorstep help in Gujar Khan, Kallar Syedan and surrounding areas, where available. Inquiries accepted 24 hours."};
var PH='923455583530',W='https://wa.me/'+PH;
function wa(msg){return W+'?text='+encodeURIComponent(msg);}
function handoff(q){return wa('Assalam o Alaikum. I asked on your website: '+String(q||'').slice(0,200));}
var CP=(document.documentElement.lang||'').toLowerCase().indexOf('ur')===0?'/ur/':'/en/';var CALC={dl:CP+'calculators/tools/punjab-driving-license-fee-calculator',car:CP+'calculators/tools/punjab-car-token-tax-transfer-fee-calculator',bike:CP+'calculators/tools/punjab-bike-registration-transfer-fee-calculator',hub:CP+'calculators/'};
var UR=[['السلام علیکم','assalam'],['اسلام علیکم','assalam'],['سلام','salam'],['ڈرائیونگ','driving'],['لائسنس','license'],['لائیسنس','license'],['فیس','fee'],['ڈومیسائل','domicile'],['کریکٹر','character'],['کردار','character'],['سرٹیفکیٹ','certificate'],['پولیس','police'],['ویریفکیشن','verification'],['ٹوکن','token'],['ٹیکس','tax'],['موٹر سائیکل','motorcycle'],['بائیک','bike'],['گاڑی','car'],['کرایہ دار','tenant'],['پیدائش','birth'],['نکاح','marriage'],['شادی','marriage'],['طلاق','divorce'],['وفات','death'],['بکنگ','booking'],['کاغذات','documents'],['دستاویزات','documents'],['ادائیگی','payment'],['رابطہ','contact'],['واٹس ایپ','whatsapp'],['کتنے دن','how long'],['کتنا وقت','how long'],['گم','lost'],['ای سٹیمپ','estamp'],['اسٹام','stamp'],['ٹرانسفر','transfer'],['رجسٹریشن','registration'],['چالان','challan'],['ایف آئی آر','fir'],['رپورٹ','report'],['فشریز','fisheries'],['ماہی','fisheries'],['فوڈ','food'],['کاروبار','business'],['تصدیق','verify'],['علاقہ','area'],['گوجرخان','gujar khan'],['راولپنڈی','rawalpindi'],['کیلکولیٹر','calculator']];
function urdu(s){s=s||'';for(var i=0;i<UR.length;i++)s=s.split(UR[i][0]).join(' '+UR[i][1]+' ');return s;}
function norm(s){return urdu(s).toLowerCase().replace(/licence/g,'license').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();}
var RE_CNIC=/\b\d{5}[- ]?\d{7}[- ]?\d\b|\b\d{13}\b/;
var RE_SECRET=/(password|passcode|\botp\b|\bpin\b|\bcvv\b|card number|account number|bank detail|bank account)/;
var RE_LEGAL=/(lawyer|legal advice|\bcourt\b|\bsue\b|\bbail\b|vakeel|wakeel|qanoon|against me|case against)/;
var RE_TIME=/(how long|how many days|kitne din|kitna time|kitna waqt|processing time|\bdays\b|kab tak|kab milega|deadline|time lagta|time lage)/;
var RE_FEE=/(\bfee\b|\bfees\b|price|charge|charges|cost|kitna|kitne|kitni|paisa|paise|rupee|rupay|how much|calculator|estimate)/;
var RE_REFUND=/(refund|money back|wapis|cancel)/;
var RE_PAY=/(\bpay\b|payment|psid|jazzcash|easypaisa|ibft|cash on delivery|\bcod\b|1bill)/;
var RE_VERIFY=/(verify|verified|\breal\b|genuine|fake|fraud|scam|registered|trust|legit)/;
var RE_BOOK=/(\bbook\b|booking|apply|how to start|doorstep delivery|kaise karen|kaise kare|kaise karun|app)/;
var RE_CONTACT=/(contact|number|whatsapp|\bcall\b|phone|talk to|speak to)/;
var RE_AREA=/(area|areas|where|gujar khan|rawalpindi|kallar|kahuta|daultala|jatli|bewal|sukho|jabbar|location|city|doorstep|ghar)/;
var RE_DOCS=/(document|documents|required|requirement|requirements|\bneed\b|needed|kaghaz|kagzat|lagte|lagta|checklist)/;
var RE_HI=/^(hi|hello|hey|salam|assalam|aoa|helo|asalam)\b/;
var RE_OTHER=/(fisher|fish|machli|food authority|food license|\bpfa\b|e ?biz|business registration|wildlife|hunting|shikar)/;
var RE_LOST=/(\blost\b|\blose\b|\bgum\b|kho gaya|kho gya|missing|stolen|chori)/;
var RE_CAR=/(\bcar\b|\bjeep\b|gari|gaari|gadi|\bcc\b)/;var RE_BIKE=/(bike|motorcycle|motor cycle|motorbike|e bike|scooty)/;var RE_DL=/(license|\bdl\b|\bidp\b|learner|driving)/;var RE_VEH=/(token|transfer|vehicle|registration)/;
var EXTRA={'renewal-of-regular-license':['driving']};
var STOP={'of':1,'for':1,'the':1,'and':1,'a':1,'copy':0};
var ALIAS={'nikah':'marriage-certificate','kirayedar':'tenant-registration','pcc':'character-certificate','talaq':'divorce-certificate','tlaq':'divorce-certificate','paidaish':'birth-certificate','wafat':'death-certificate','estamp':'e-stamping','estamping':'e-stamping','stamp':'e-stamping','noc':'noc-for-domicile-transfer','tenant':'tenant-registration','fir':'copy-of-fir'};
function L(t,h,k){return {t:t,h:h,k:k||''};}
function R(text,links,ev){return {text:text,links:links||[],ev:ev||''};}
function svc(id){for(var i=0;i<DATA.services.length;i++)if(DATA.services[i].id===id)return DATA.services[i];return null;}
function findServices(q){
 var toks=q.split(' ');
 for(var k=0;k<toks.length;k++){var a=ALIAS[toks[k]];if(a&&svc(a))return [svc(a)];}
 var best=0,hits=[];
 for(var i=0;i<DATA.services.length;i++){
  var s=DATA.services[i];if(s.id==='general-inquiry-and-guide'||s.id==='other-punjab-dastak-services')continue;
  var nt=s.n.toLowerCase().replace(/licence/g,'license').replace(/[^a-z0-9 ]/g,' ').split(' ').filter(function(w){return w.length>3&&!STOP[w];}).concat(EXTRA[s.id]||[]);var sc=0;
  for(var j=0;j<nt.length;j++){if(toks.indexOf(nt[j])>-1)sc++;}
  if(sc>0){if(sc>best){best=sc;hits=[s];}else if(sc===best)hits.push(s);}
 }
 return hits;
}
function svcAnswer(s,raw){
 var url='/en/services/'+s.id+'/';
 var links=[L('Open the '+s.n+' page',url)];
 var c=calcFor(s.id);if(c)links.push(L('Estimate the fee',c,'y'));
 links.push(L('Ask on WhatsApp',wa('Assalam o Alaikum. I want help with: '+s.n),'w'));
 if(s.docs&&s.docs.length)return R('Documents for '+s.n+' (please confirm the latest list in the Dastak app):\n- '+s.docs.join('\n- ')+'\n\nBook in the Dastak app with Facilitator Code 90807, or message me.',links,'service');
 return R(s.n+': '+(s.guide||'Please see the service page.'),links,'service');
}
function calcFor(id){
 if(/driving-license|regular-license|international/.test(id)&&!/learner/.test(id))return CALC.dl;
 if(id==='token-tax'||id==='transfer-of-motor-vehicle')return CALC.hub;
 if(id==='motor-vehicle-registration')return CALC.bike;
 return '';
}
function feeAnswer(q){
 var est='It is an estimate only. The final fee comes on the official PSID, so check it before you pay.';
 if(RE_BIKE.test(q))return R('You can get a free estimate with my Motorcycle Registration and Transfer Fee Calculator. It shows the government fee and my doorstep fee separately.\n\n'+est,[L('Open the calculator',CALC.bike,'y'),L('Vehicle transfer service','/en/services/transfer-of-motor-vehicle/'),L('WhatsApp me',handoff(q),'w')],'fee_bike');
 if(RE_CAR.test(q))return R('You can get a free estimate with my Car and Jeep Token Tax and Transfer Calculator. It shows the government fee and my doorstep fee separately.\n\n'+est,[L('Open the calculator',CALC.car,'y'),L('Token tax service','/en/services/token-tax/'),L('WhatsApp me',handoff(q),'w')],'fee_car');
 if(RE_DL.test(q))return R('You can get a free estimate with my Driving License Fee Calculator. It shows the government fee and my doorstep fee separately.\n\n'+est,[L('Open the calculator',CALC.dl,'y'),L('License renewal service','/en/services/renewal-of-regular-license/'),L('WhatsApp me',handoff(q),'w')],'fee_dl');
 if(RE_VEH.test(q))return R('Is it a car or a motorcycle? Both calculators are free and show the government fee and my doorstep fee separately.\n\n'+est,[L('Car and jeep calculator',CALC.car,'y'),L('Motorcycle calculator',CALC.bike,'y'),L('WhatsApp me',handoff(q),'w')],'fee_vehicle');
 return R('Fees are generated by the official system for each service. For a free estimate, use my calculators for driving licenses, cars and motorcycles. For other services, message me and I will tell you before you book.\n\n'+DATA.pay,[L('Fee calculators',CALC.hub,'y'),L('Ask about a fee',handoff(q),'w')],'fee');
}
var POP=[['Driving license renewal','renewal-of-regular-license'],['Character certificate','character-certificate'],['Domicile certificate','domicile-certificate'],['Vehicle transfer','transfer-of-motor-vehicle'],['Token tax','token-tax'],['Birth certificate','birth-certificate']];
function answer(text){
 var raw=text||'';var q=norm(raw);
 if(!raw.trim())return R('Please type a question, or tap one of the buttons.');
 if(RE_CNIC.test(raw)||/\d{12,}/.test(raw.replace(/[\s-]/g,''))||RE_SECRET.test(q))return R('Please do not share your CNIC number, passwords, OTPs or bank details here. I never need them in this chat. Message me on WhatsApp if you need personal help.',[L('WhatsApp me',W,'w')],'blocked');
 if(!q)return R('I could not read that. Please message me on WhatsApp and I will help you directly.',[L('Continue on WhatsApp',handoff(raw),'w')],'unknown');
 if(RE_LEGAL.test(q))return R('I explain government procedures and documents. I am not a lawyer, so for court or legal disputes please speak to a lawyer.',[L('Guidance and general inquiry','/en/services/general-inquiry-and-guide/'),L('Ask me on WhatsApp',handoff(raw),'w')],'legal');
 if(RE_REFUND.test(q))return R(DATA.refund,[L('Read the Terms','/en/terms/')],'refund');
 if(RE_TIME.test(q))return R('Time depends on the government department, so I cannot promise a date. Message me with your service and I will tell you what to expect.',[L('Ask on WhatsApp',handoff(raw),'w')],'time');
 if(RE_OTHER.test(q))return R('I give guidance on fisheries e-licenses, food authority licenses and business registrations (e-Biz). Availability can differ, so let me confirm it for you.',[L('Continue on WhatsApp',handoff(raw),'w'),L('Other Dastak services','/en/services/other-punjab-dastak-services/')],'other');
 if(RE_LOST.test(q)&&/(license|\bdl\b)/.test(q))return R('For a lost driving license you usually need a loss report first, then a duplicate license. Both can be booked through Dastak.',[L('Duplicate driving license','/en/services/duplicate-driving-license/'),L('Loss report','/en/services/loss-report/'),L('Ask on WhatsApp',handoff(raw),'w')],'lost');
 if(RE_FEE.test(q))return feeAnswer(q);
 if(RE_PAY.test(q))return R(DATA.pay,[L('How it works','/en/how-it-works/'),L('Ask on WhatsApp',handoff(raw),'w')],'pay');
 var sv=findServices(q);
 if(sv.length===1)return svcAnswer(sv[0],raw);
 if(sv.length>1&&sv.length<=6)return R('Which service do you mean? Please tap one:',sv.map(function(s){return L(s.n,'/en/services/'+s.id+'/');}),'choose');
 if(RE_VERIFY.test(q))return R('You can check me on the official Dastak portal or by calling the helpline 1202. When you book in the Dastak app, enter Facilitator Code 90807. Proof of my registration is available on request via WhatsApp.',[L('How to verify me','/en/about/#verify'),L('Official portal',DATA.portal)],'verify');
 if(RE_BOOK.test(q))return R('Book in the official Dastak Citizen App: choose Doorstep Delivery, select Self or On Behalf, and enter Facilitator Code 90807 in the Facilitator Code box. You can also message me on WhatsApp, call me on 0345-5583530, or call the helpline 1202.',[L('Dastak app (Google Play)',DATA.play),L('Dastak app (App Store)',DATA.store),L('WhatsApp me',W,'w')],'book');
 if(RE_CONTACT.test(q))return R('WhatsApp or call me on 0345-5583530. Inquiries are accepted 24 hours.',[L('WhatsApp me',W,'w'),L('Call me','tel:+'+PH)],'contact');
 if(RE_AREA.test(q))return R('Doorstep visits are available in Gujar Khan, Kallar Syedan, Kahuta, Daultala, Jatli, Bewal, Sukho, Jabbar and nearby areas. Many services can also be done online for anywhere in Punjab. Inquiries are accepted 24 hours.',[L('Gujar Khan page','/en/gujar-khan/'),L('Rawalpindi page','/en/rawalpindi/'),L('Ask about my area',handoff(raw),'w')],'area');
 if(RE_DOCS.test(q))return R('Which service do you need? Tap one to see the documents, or open the full checklist.',POP.map(function(p){return L(p[0],'/en/services/'+p[1]+'/');}).concat([L('Document checklist','/en/document-checklist/','y')]),'docs');
 if(RE_HI.test(q))return R('Wa Alaikum Assalam! I can answer questions about services, documents, booking, fees and doorstep areas. What do you need?');
 return R('I do not have a verified answer for that yet. Send it to me on WhatsApp and I will reply directly. Your question is already typed in the message.',[L('Continue on WhatsApp',handoff(raw),'w'),L('Call me','tel:+'+PH)],'unknown');
}
if(typeof module!=='undefined'){module.exports={answer:answer};}
if(typeof document==='undefined')return;
function ga(name,params){try{if(typeof window.gtag==='function')window.gtag('event',name,params||{});}catch(e){}}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e;}
var ICON='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>';
var SEND='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
var CHIPS=[['📄','Documents needed','ضروری کاغذات','Documents needed'],['📱','Book a service','بکنگ کیسے کریں','How do I book?'],['🧮','Fees & calculators','فیس معلوم کریں','fee calculator'],['📍','Doorstep areas','کن علاقوں میں','Which areas do you cover?'],['✅','Verify me','تصدیق کریں','How can I verify you?'],['','WhatsApp me','واٹس ایپ کریں','']];
var UR=(document.documentElement.lang||'').toLowerCase().indexOf('ur')===0;
var S=UR?{ask:'سوال پوچھیں',close:'✕ بند کریں',title:'دستک 90807 سے پوچھیں',sub:'خودکار مدد · فوری جواب',wa:'واٹس ایپ',closeA:'چیٹ بند کریں',note:'یہ خودکار مددگار ہے، سرکاری سروس نہیں۔ ',noteB:'اپنا شناختی کارڈ نمبر، پاس ورڈ یا OTP کبھی نہ لکھیں۔',lab:'آپ کا سوال',ph:'اپنا سوال لکھیں…',send:'بھیجیں',ft:'رجسٹرڈ فیسیلیٹیٹر کوڈ 90807 · آزاد سروس',hi:'السلام علیکم! آپ کو کس چیز میں مدد چاہیے؟ نیچے بٹن دبائیں یا اپنا سوال لکھیں۔',hiEn:'Answers are in English for now.',waMsg:'السلام علیکم، میرا ایک سوال ہے۔'}
 :{ask:'Ask a question',close:'✕ Close chat',title:'Ask Dastak 90807',sub:'Automated help · instant',wa:'WhatsApp',closeA:'Close chat',note:'Automated helper, not a government service. ',noteB:'Never type your CNIC, passwords or OTPs.',lab:'Your question',ph:'Type your question…',send:'Send',ft:'Registered Facilitator Code 90807 · Independent service',hi:'Assalam o Alaikum! What do you need help with? Tap a button or type your question.',hiEn:'',waMsg:'Assalam o Alaikum. I have a question.'};
function init(){
 if(document.getElementById('cbp'))return;
 var css=document.createElement('link');css.rel='stylesheet';css.href='/assets/chatbot.css?v=2';document.head.appendChild(css);
 var btn=el('button','cb-btn',S.ask);btn.type='button';btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-controls','cbp');
 var p=el('div','cb-p cb2');p.id='cbp';p.setAttribute('role','dialog');p.setAttribute('aria-label',S.title);p.hidden=true;
 var h=el('div','cb-h');var av=el('span','cb-av');av.innerHTML=ICON;h.appendChild(av);
 var tt=el('div','cb-t');tt.appendChild(el('b','',S.title));var sm=el('small');sm.appendChild(el('span','cb-dot'));sm.appendChild(document.createTextNode(S.sub));tt.appendChild(sm);h.appendChild(tt);
 var hw=el('a','cb-wa',S.wa);hw.href=wa(S.waMsg);hw.rel='noopener';hw.addEventListener('click',function(){ga('chat_whatsapp_handoff',{tool_name:'header'});});h.appendChild(hw);
 var x=el('button','cb-x','✕');x.type='button';x.setAttribute('aria-label',S.closeA);h.appendChild(x);p.appendChild(h);
 var n=el('p','cb-n');n.appendChild(document.createTextNode(S.note));n.appendChild(el('b','',S.noteB));p.appendChild(n);
 var log=el('div','cb-l');log.setAttribute('aria-live','polite');p.appendChild(log);
 var chips=el('div','cb-c');
 CHIPS.forEach(function(c){
  var b=c[3]?el('button','cb-chip'):el('a','cb-chip cb-chip-w');
  if(c[3])b.type='button';else{b.href=wa(S.waMsg);b.rel='noopener';}
  if(c[0]){var ic=el('span','cb-ic',c[0]);ic.setAttribute('aria-hidden','true');b.appendChild(ic);}
  var tx=el('span','cb-ct');if(UR){tx.appendChild(el('b','',c[2]));}else{tx.appendChild(el('b','',c[1]));var u=el('small','',c[2]);u.lang='ur';u.dir='rtl';tx.appendChild(u);}b.appendChild(tx);
  b.addEventListener('click',function(){ga(c[3]?'chat_quick_tap':'chat_whatsapp_handoff',{tool_name:c[1]});if(c[3])send(c[3],c[1]);});
  chips.appendChild(b);
 });
 p.appendChild(chips);
 var f=el('form','cb-f');var lab=el('label','cb-sr',S.lab);lab.setAttribute('for','cb-in');var i=el('input');i.id='cb-in';i.type='text';i.maxLength=200;i.autocomplete='off';i.placeholder=S.ph;i.setAttribute('enterkeyhint','send');
 var go=el('button','cb-go');go.type='submit';go.innerHTML=SEND;go.setAttribute('aria-label',S.send);
 f.appendChild(lab);f.appendChild(i);f.appendChild(go);p.appendChild(f);
 p.appendChild(el('p','cb-ft',S.ft));
 document.body.appendChild(p);document.body.appendChild(btn);
 function add(cls,t,links){var m=el('div','cb-m '+cls);var tx=el('div','cb-tx',t);m.appendChild(tx);
  if(links&&links.length){var lk=el('div','cb-lk');links.forEach(function(l){var a=el('a','cb-a'+(l.k?' '+l.k:''),l.t);a.href=l.h;if(/^https?:/.test(l.h))a.rel='noopener';
   a.addEventListener('click',function(){ga(/wa\.me/.test(l.h)?'chat_whatsapp_handoff':'chat_link_click',{tool_name:l.t});});lk.appendChild(a);});m.appendChild(lk);}
  log.appendChild(m);m.scrollIntoView({block:'nearest'});log.scrollTop=log.scrollHeight;}
 function send(t,label){add('u',(UR&&label?(CHIPS.filter(function(c){return c[1]===label;})[0]||[])[2]:0)||label||t);var r=answer(t);add('b',r.text,r.links);if(!label&&r.ev)ga('chat_question',{tool_name:r.ev});chips.hidden=true;}
 f.addEventListener('submit',function(e){e.preventDefault();var v=i.value.trim();if(!v)return;i.value='';send(v);});
 function open(o){p.hidden=!o;btn.setAttribute('aria-expanded',String(o));btn.textContent=o?S.close:S.ask;document.body.classList.toggle('cb-open',o);
  if(o){ga('chat_open');if(!log.children.length){add('b',S.hi);var ur=el('span','cb-ur',UR?S.hiEn:'سوال لکھیں یا نیچے بٹن دبائیں');if(UR){ur.lang='en';ur.dir='ltr';}else{ur.lang='ur';ur.dir='rtl';}log.lastChild.appendChild(ur);}if(window.matchMedia&&window.matchMedia('(pointer:fine)').matches)i.focus();}else btn.focus();}
 btn.addEventListener('click',function(){open(p.hidden);});x.addEventListener('click',function(){open(false);});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!p.hidden)open(false);});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
