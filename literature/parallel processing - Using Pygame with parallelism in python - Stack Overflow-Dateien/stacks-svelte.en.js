"use strict";(self.webpackChunkstackoverflow=self.webpackChunkstackoverflow||[]).push([[4613],{88781:(t,e,n)=>{n.d(e,{x:()=>l});const l=t=>{const e=e=>{const n=e.target;t.contains(n)||t.dispatchEvent(new CustomEvent("outclick",{detail:n}))};return document.addEventListener("click",e,!0),{destroy(){document.removeEventListener("click",e,!0)}}}},39022:(t,e,n)=>{if(n.d(e,{x:()=>l.x,e:()=>d}),!/^(1751|4301|4877|5|7228|8104)$/.test(n.j))var l=n(88781);var s=n(74982);const o=/^(1751|4301|4877|5|7228|8104|9852)$/.test(n.j)?null:["a[href]","area[href]",'input:not([disabled]):not([type="hidden"]):not([aria-hidden])',"select:not([disabled]):not([aria-hidden])","textarea:not([disabled]):not([aria-hidden])","button:not([disabled]):not([aria-hidden])","iframe","object","embed","[contenteditable]",'[tabindex]:not([tabindex^="-"])'],i=t=>{const e=document.defaultView?.getComputedStyle(t);return!(!e||"none"===e.getPropertyValue("display")||"hidden"===e.getPropertyValue("visibility"))},a=async t=>(await(0,s.Ky)(),[...t.querySelectorAll(o.join(", "))].filter(i)),c=t=>{t[0]&&t[0].focus()},r=t=>{t[t.length-1]&&t[t.length-1].focus()},d=(t,{active:e,initialFocusElement:n,returnFocusElement:l})=>{let s;const o=async e=>{const{key:n,shiftKey:l}=e;if("Tab"===n){e.preventDefault(),e.stopPropagation();const n=await a(t),s=document.activeElement;l?(({allFocusableItems:t,currentlyFocusedItem:e})=>{if(!e)return void r(t);const n=t.indexOf(e);if(0===n)return void r(t);const l=t[n-1];l&&l.focus()})({allFocusableItems:n,currentlyFocusedItem:s}):(({allFocusableItems:t,currentlyFocusedItem:e})=>{if(!e)return void c(t);const n=t.indexOf(e);if(t.length-1===n)return void c(t);const l=t[n+1];l&&l.focus()})({allFocusableItems:n,currentlyFocusedItem:s})}},i=async()=>{const e=await a(t);s??=document.activeElement,n?n.focus():c(e),document.addEventListener("keydown",o)},d=()=>{l?l.focus():s?.focus(),document.removeEventListener("keydown",o),s=null};return e&&i(),{update:({active:t})=>{t?i():d()},destroy:d}}},60355:(t,e,n)=>{n.d(e,{zx:()=>u,JO:()=>f,u_:()=>V,J2:()=>Y,us:()=>ot,yk:()=>rt,zW:()=>tt,Od:()=>k,$j:()=>h});var l=n(52932);n(77460);const s=t=>({}),o=t=>({});function i(t){let e,n,i,a;const c=t[17].badge,r=(0,l.nuO)(c,t,t[16],o);return{c(){e=(0,l.fLW)(" "),n=(0,l.bGB)("span"),i=(0,l.bGB)("span"),r&&r.c(),(0,l.Ljt)(i,"class","s-btn--number"),(0,l.Ljt)(n,"class","s-btn--badge")},m(t,s){(0,l.$Tr)(t,e,s),(0,l.$Tr)(t,n,s),(0,l.R3I)(n,i),r&&r.m(i,null),a=!0},p(t,e){r&&r.p&&(!a||65536&e)&&(0,l.kmG)(r,c,t,t[16],a?(0,l.u2N)(c,t[16],e,s):(0,l.VOJ)(t[16]),o)},i(t){a||((0,l.Ui)(r,t),a=!0)},o(t){(0,l.etI)(r,t),a=!1},d(t){t&&((0,l.ogt)(e),(0,l.ogt)(n)),r&&r.d(t)}}}function a(t){let e,n,s,o,a,c;const r=t[17].default,d=(0,l.nuO)(r,t,t[16],null);let u=t[4].badge&&i(t),p=[{href:t[0]},{class:t[2]},{disabled:n=!t[0]&&t[1]||null},{"aria-disabled":s=t[0]&&t[1]?"true":null},t[3]],b={};for(let t=0;t<p.length;t+=1)b=(0,l.f0i)(b,p[t]);return{c(){e=(0,l.bGB)(t[0]?"a":"button"),d&&d.c(),u&&u.c(),(0,l.Kp5)(t[0]?"a":"button")(e,b)},m(n,s){(0,l.$Tr)(n,e,s),d&&d.m(e,null),u&&u.m(e,null),o=!0,a||(c=(0,l.oLt)(e,"click",t[18]),a=!0)},p(t,a){d&&d.p&&(!o||65536&a)&&(0,l.kmG)(d,r,t,t[16],o?(0,l.u2N)(r,t[16],a,null):(0,l.VOJ)(t[16]),null),t[4].badge?u?(u.p(t,a),16&a&&(0,l.Ui)(u,1)):(u=i(t),u.c(),(0,l.Ui)(u,1),u.m(e,null)):u&&((0,l.dvw)(),(0,l.etI)(u,1,1,(()=>{u=null})),(0,l.gbL)()),(0,l.Kp5)(t[0]?"a":"button")(e,b=(0,l.LoY)(p,[(!o||1&a)&&{href:t[0]},(!o||4&a)&&{class:t[2]},(!o||3&a&&n!==(n=!t[0]&&t[1]||null))&&{disabled:n},(!o||3&a&&s!==(s=t[0]&&t[1]?"true":null))&&{"aria-disabled":s},8&a&&t[3]]))},i(t){o||((0,l.Ui)(d,t),(0,l.Ui)(u),o=!0)},o(t){(0,l.etI)(d,t),(0,l.etI)(u),o=!1},d(t){t&&(0,l.ogt)(e),d&&d.d(t),u&&u.d(),a=!1,c()}}}function c(t){let e,n,s=t[0]?"a":"button",o=(t[0]?"a":"button")&&a(t);return{c(){o&&o.c(),e=(0,l.cSb)()},m(t,s){o&&o.m(t,s),(0,l.$Tr)(t,e,s),n=!0},p(t,[n]){t[0]||"button"?s?(0,l.N8)(s,t[0]?"a":"button")?(o.d(1),o=a(t),s=t[0]?"a":"button",o.c(),o.m(e.parentNode,e)):o.p(t,n):(o=a(t),s=t[0]?"a":"button",o.c(),o.m(e.parentNode,e)):s&&(o.d(1),o=null,s=t[0]?"a":"button")},i(t){n||((0,l.Ui)(o,t),n=!0)},o(t){(0,l.etI)(o,t),n=!1},d(t){t&&(0,l.ogt)(e),o&&o.d(t)}}}function r(t,e,n){let s;const o=["branding","size","variant","weight","href","disabled","dropdown","icon","link","loading","selected","unset","class"];let i=(0,l.q2N)(e,o),{$$slots:a={},$$scope:c}=e;const r=(0,l.XGm)(a);let{branding:d=""}=e,{size:u=""}=e,{variant:p=""}=e,{weight:b=""}=e,{href:$}=e,{disabled:f=!1}=e,{dropdown:v=!1}=e,{icon:m=!1}=e,{link:g=!1}=e,{loading:h=!1}=e,{selected:L=!1}=e,{unset:j=!1}=e,{class:w=""}=e;return t.$$set=t=>{e=(0,l.f0i)((0,l.f0i)({},e),(0,l.Jvk)(t)),n(3,i=(0,l.q2N)(e,o)),"branding"in t&&n(5,d=t.branding),"size"in t&&n(6,u=t.size),"variant"in t&&n(7,p=t.variant),"weight"in t&&n(8,b=t.weight),"href"in t&&n(0,$=t.href),"disabled"in t&&n(1,f=t.disabled),"dropdown"in t&&n(9,v=t.dropdown),"icon"in t&&n(10,m=t.icon),"link"in t&&n(11,g=t.link),"loading"in t&&n(12,h=t.loading),"selected"in t&&n(13,L=t.selected),"unset"in t&&n(14,j=t.unset),"class"in t&&n(15,w=t.class),"$$scope"in t&&n(16,c=t.$$scope)},t.$$.update=()=>{65504&t.$$.dirty&&n(2,s=((t,e,n,l,s,o,i,a,c,r,d)=>{const u="s-btn";let p=u;return t&&(p+=" "+t),[e,n,l,s].forEach((t=>{t&&(p+=` ${u}__${t}`)})),o&&(p+=` ${u}__dropdown`),i&&(p+=` ${u}__link`),a&&(p+=` ${u}__icon`),c&&(p+=` ${u}__unset`),r&&(p+=" is-loading"),d&&(p+=" is-selected"),p})(w,d,u,p,b,v,g,m,j,h,L))},[$,f,s,i,r,d,u,p,b,v,m,g,h,L,j,w,c,a,function(e){l.cKT.call(this,t,e)}]}class d extends(/^((175|376|430|562)1|4877|9852)$/.test(n.j)?null:l.f_C){constructor(t){super(),(0,l.S1n)(this,t,r,c,l.N8,{branding:5,size:6,variant:7,weight:8,href:0,disabled:1,dropdown:9,icon:10,link:11,loading:12,selected:13,unset:14,class:15})}}const u=/^((175|376|430|562)1|4877|9852)$/.test(n.j)?null:d;function p(t){let e,n;return{c(){e=new l.FWw(!1),n=(0,l.cSb)(),e.a=n},m(s,o){e.m(t[0],s,o),(0,l.$Tr)(s,n,o)},p(t,[n]){1&n&&e.p(t[0])},i:l.ZTd,o:l.ZTd,d(t){t&&((0,l.ogt)(n),e.d())}}}function b(t,e,n){let l,{src:s}=e,{title:o=""}=e,{native:i=!1}=e,{class:a=""}=e;return t.$$set=t=>{"src"in t&&n(1,s=t.src),"title"in t&&n(2,o=t.title),"native"in t&&n(3,i=t.native),"class"in t&&n(4,a=t.class)},t.$$.update=()=>{30&t.$$.dirty&&n(0,l=((t,e,n,l)=>{let s=t;return e&&(s=s.replace("</svg>","<title>"+e+"</title></svg>"),s=s.replace(' aria-hidden="true"',"")),n&&(s=s.replace(/class="/,'class="native ')),l&&(s=s.replace(/class="/,'class="'+l+" ")),s})(s,o,i,a))},[l,s,o,i,a]}class $ extends(/^(3229|513|8959)$/.test(n.j)?null:l.f_C){constructor(t){super(),(0,l.S1n)(this,t,b,p,l.N8,{src:1,title:2,native:3,class:4})}}const f=/^(3229|513|8959)$/.test(n.j)?null:$;function v(t){let e,n,s;return{c(){e=(0,l.bGB)("div"),n=(0,l.bGB)("div"),s=(0,l.fLW)(t[0]),(0,l.Ljt)(n,"class","v-visible-sr"),(0,l.Ljt)(e,"class",t[1])},m(t,o){(0,l.$Tr)(t,e,o),(0,l.R3I)(e,n),(0,l.R3I)(n,s)},p(t,[n]){1&n&&(0,l.rTO)(s,t[0]),2&n&&(0,l.Ljt)(e,"class",t[1])},i:l.ZTd,o:l.ZTd,d(t){t&&(0,l.ogt)(e)}}}function m(t,e,n){let l,{label:s="Loading…"}=e,{size:o=""}=e,{class:i=""}=e;return t.$$set=t=>{"label"in t&&n(0,s=t.label),"size"in t&&n(2,o=t.size),"class"in t&&n(3,i=t.class)},t.$$.update=()=>{12&t.$$.dirty&&n(1,l=((t,e)=>{let n="s-spinner";return t&&(n+=" "+t),e&&(n+=" s-spinner__"+e),n})(i,o))},[s,l,o,i]}class g extends(8104==n.j?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,m,v,l.N8,{label:0,size:2,class:3})}}const h=8104==n.j?g:null;function L(t){(0,l.qOq)(t,"svelte-15wbbs5",'.s-skeleton.svelte-15wbbs5{overflow:hidden;position:relative}.s-skeleton.svelte-15wbbs5:after{opacity:25%;animation:svelte-15wbbs5-flow 8s linear infinite;background-image:linear-gradient(\n            to right,\n            #ac76f0 8.33%,\n            #297fff 16.67%,\n            #6abcf8 25%,\n            #ac76f0 41.67%,\n            #297fff 58.34%,\n            #6abcf8 75.01%,\n            #ac76f0 83.34%\n        );background-size:400% 100%;content:"";inset:0;position:absolute;z-index:1}@keyframes svelte-15wbbs5-flow{0%{background-position:400% 50%}100%{background-position:0% 50%}}')}function j(t){let e,n,s,o,i,a,c,r,d;return{c(){e=(0,l.bGB)("div"),n=(0,l.bGB)("div"),s=(0,l.DhX)(),o=(0,l.bGB)("div"),i=(0,l.DhX)(),a=(0,l.bGB)("div"),c=(0,l.DhX)(),r=(0,l.bGB)("span"),d=(0,l.fLW)(t[0]),(0,l.Ljt)(n,"class","s-skeleton bar-pill h16 w100 svelte-15wbbs5"),(0,l.Ljt)(o,"class","s-skeleton bar-pill h16 w80 svelte-15wbbs5"),(0,l.Ljt)(a,"class","s-skeleton bar-pill h16 w33 svelte-15wbbs5"),(0,l.Ljt)(r,"class","v-visible-sr"),(0,l.Ljt)(e,"class","d-flex g4 fd-column")},m(t,u){(0,l.$Tr)(t,e,u),(0,l.R3I)(e,n),(0,l.R3I)(e,s),(0,l.R3I)(e,o),(0,l.R3I)(e,i),(0,l.R3I)(e,a),(0,l.R3I)(e,c),(0,l.R3I)(e,r),(0,l.R3I)(r,d)},p(t,[e]){1&e&&(0,l.rTO)(d,t[0])},i:l.ZTd,o:l.ZTd,d(t){t&&(0,l.ogt)(e)}}}function w(t,e,n){let{label:l="Loading content..."}=e;return t.$$set=t=>{"label"in t&&n(0,l=t.label)},[l]}class y extends(/^(5|5621|7228)$/.test(n.j)?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,w,j,l.N8,{label:0},L)}}const k=/^(5|5621|7228)$/.test(n.j)?y:null;var I=n(74982),T=n(39022);const x=t=>({}),C=t=>({}),B=t=>({}),_=t=>({}),O=t=>({}),G=t=>({});function E(t){let e,n;const s=t[10].footer,o=(0,l.nuO)(s,t,t[12],C);return{c(){e=(0,l.bGB)("div"),o&&o.c(),(0,l.Ljt)(e,"class","d-flex g8 s-modal--footer")},m(t,s){(0,l.$Tr)(t,e,s),o&&o.m(e,null),n=!0},p(t,e){o&&o.p&&(!n||4096&e)&&(0,l.kmG)(o,s,t,t[12],n?(0,l.u2N)(s,t[12],e,x):(0,l.VOJ)(t[12]),C)},i(t){n||((0,l.Ui)(o,t),n=!0)},o(t){(0,l.etI)(o,t),n=!1},d(t){t&&(0,l.ogt)(e),o&&o.d(t)}}}function R(t){let e;return{c(){e=(0,l.bGB)("div"),e.textContent="X",(0,l.Ljt)(e,"class","modal-close")},m(t,n){(0,l.$Tr)(t,e,n)},p:l.ZTd,d(t){t&&(0,l.ogt)(e)}}}function U(t){let e,n,s,o,i,a,c,r,d,p,b,$,f,v,m,g,h,L;const j=t[10].header,w=(0,l.nuO)(j,t,t[12],G),y=t[10].body,k=(0,l.nuO)(y,t,t[12],_);let I=t[8].footer&&E(t);return p=new u({props:{variant:"muted",icon:!0,"aria-label":t[3],class:"s-modal--close",$$slots:{default:[R]},$$scope:{ctx:t}}}),p.$on("click",t[6]),{c(){e=(0,l.bGB)("aside"),n=(0,l.bGB)("div"),s=(0,l.bGB)("h1"),w&&w.c(),i=(0,l.DhX)(),a=(0,l.bGB)("div"),k&&k.c(),r=(0,l.DhX)(),I&&I.c(),d=(0,l.DhX)(),(0,l.YCL)(p.$$.fragment),(0,l.Ljt)(s,"id",o=`${t[1]}-title`),(0,l.Ljt)(s,"class","s-modal--header"),(0,l.Ljt)(a,"id",c=`${t[1]}-description`),(0,l.Ljt)(a,"class","s-modal--body"),(0,l.Ljt)(n,"class",t[5]),(0,l.Ljt)(n,"role","document"),(0,l.Ljt)(e,"class","s-modal"),(0,l.Ljt)(e,"role","dialog"),(0,l.Ljt)(e,"aria-hidden",f=!t[0]),(0,l.Ljt)(e,"aria-labelledby",v=`${t[1]}-title`),(0,l.Ljt)(e,"aria-describedby",m=`${t[1]}-description`),(0,l.VHj)(e,"s-modal__danger","danger"===t[2]),(0,l.VHj)(e,"s-modal__celebration","celebration"===t[2])},m(o,c){(0,l.$Tr)(o,e,c),(0,l.R3I)(e,n),(0,l.R3I)(n,s),w&&w.m(s,null),(0,l.R3I)(n,i),(0,l.R3I)(n,a),k&&k.m(a,null),(0,l.R3I)(n,r),I&&I.m(n,null),(0,l.R3I)(n,d),(0,l.yef)(p,n,null),g=!0,h||(L=[(0,l.oLt)(window,"keydown",t[7]),(0,l.TVh)(b=T.x.call(null,n)),(0,l.TVh)($=T.e.call(null,n,{active:t[0]})),(0,l.oLt)(n,"outclick",t[11])],h=!0)},p(t,[i]){w&&w.p&&(!g||4096&i)&&(0,l.kmG)(w,j,t,t[12],g?(0,l.u2N)(j,t[12],i,O):(0,l.VOJ)(t[12]),G),(!g||2&i&&o!==(o=`${t[1]}-title`))&&(0,l.Ljt)(s,"id",o),k&&k.p&&(!g||4096&i)&&(0,l.kmG)(k,y,t,t[12],g?(0,l.u2N)(y,t[12],i,B):(0,l.VOJ)(t[12]),_),(!g||2&i&&c!==(c=`${t[1]}-description`))&&(0,l.Ljt)(a,"id",c),t[8].footer?I?(I.p(t,i),256&i&&(0,l.Ui)(I,1)):(I=E(t),I.c(),(0,l.Ui)(I,1),I.m(n,d)):I&&((0,l.dvw)(),(0,l.etI)(I,1,1,(()=>{I=null})),(0,l.gbL)());const r={};8&i&&(r["aria-label"]=t[3]),4096&i&&(r.$$scope={dirty:i,ctx:t}),p.$set(r),(!g||32&i)&&(0,l.Ljt)(n,"class",t[5]),$&&(0,l.sBU)($.update)&&1&i&&$.update.call(null,{active:t[0]}),(!g||1&i&&f!==(f=!t[0]))&&(0,l.Ljt)(e,"aria-hidden",f),(!g||2&i&&v!==(v=`${t[1]}-title`))&&(0,l.Ljt)(e,"aria-labelledby",v),(!g||2&i&&m!==(m=`${t[1]}-description`))&&(0,l.Ljt)(e,"aria-describedby",m),(!g||4&i)&&(0,l.VHj)(e,"s-modal__danger","danger"===t[2]),(!g||4&i)&&(0,l.VHj)(e,"s-modal__celebration","celebration"===t[2])},i(t){g||((0,l.Ui)(w,t),(0,l.Ui)(k,t),(0,l.Ui)(I),(0,l.Ui)(p.$$.fragment,t),g=!0)},o(t){(0,l.etI)(w,t),(0,l.etI)(k,t),(0,l.etI)(I),(0,l.etI)(p.$$.fragment,t),g=!1},d(t){t&&(0,l.ogt)(e),w&&w.d(t),k&&k.d(t),I&&I.d(),(0,l.vpE)(p),h=!1,(0,l.j7q)(L)}}}function F(t,e,n){let s,{$$slots:o={},$$scope:i}=e;const a=(0,l.XGm)(o);let{id:c}=e,{visible:r=!1}=e,{state:d=""}=e,{class:u=""}=e,{i18nCloseButtonLabel:p="Close"}=e,{preventCloseOnClickOutside:b=!1}=e;const $=(0,I.x)(),f=()=>{r&&(n(0,r=!1),$("close"))};return t.$$set=t=>{"id"in t&&n(1,c=t.id),"visible"in t&&n(0,r=t.visible),"state"in t&&n(2,d=t.state),"class"in t&&n(9,u=t.class),"i18nCloseButtonLabel"in t&&n(3,p=t.i18nCloseButtonLabel),"preventCloseOnClickOutside"in t&&n(4,b=t.preventCloseOnClickOutside),"$$scope"in t&&n(12,i=t.$$scope)},t.$$.update=()=>{512&t.$$.dirty&&n(5,s=(t=>{let e="s-modal--dialog";return t&&(e+=" "+t),e})(u))},[r,c,d,p,b,s,f,t=>{"Escape"===t.key&&f()},a,u,o,()=>!b&&f(),i]}class N extends(/^(1(001|565|596)|3229|8959)$/.test(n.j)?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,F,U,l.N8,{id:1,visible:0,state:2,class:9,i18nCloseButtonLabel:3,preventCloseOnClickOutside:4})}}const V=/^(1(001|565|596)|3229|8959)$/.test(n.j)?N:null;var P=n(84950);if(/^(1565|3761|513|5621)$/.test(n.j))var S=n(13397);var z=n(41270);const{window:J}=l.globals,X=t=>({visible:1&t}),D=t=>({visible:t[0].visible,open:t[2],close:t[3]});function Z(t){let e,n,s;const o=t[16].default,i=(0,l.nuO)(o,t,t[15],D);return{c(){i&&i.c()},m(o,a){i&&i.m(o,a),e=!0,n||(s=(0,l.oLt)(J,"keydown",t[4]),n=!0)},p(t,[n]){i&&i.p&&(!e||32769&n)&&(0,l.kmG)(i,o,t,t[15],e?(0,l.u2N)(o,t[15],n,X):(0,l.VOJ)(t[15]),D)},i(t){e||((0,l.Ui)(i,t),e=!0)},o(t){(0,l.etI)(i,t),e=!1},d(t){i&&i.d(t),n=!1,s()}}}const q="popover-context";function K(t){let e=(0,I.fw)(q);if(void 0===e)throw new Error(`<${t} /> is missing a parent <Popover /> component.`);return e}function H(t,e,n){let s,o,i,a,c,{$$slots:r={},$$scope:d}=e,{id:u}=e,{autoshow:p=!1}=e,{visible:b}=e,{placement:$="bottom"}=e,{strategy:f="absolute"}=e,{trapFocus:v=!1}=e,{dismissible:m=!0}=e,{tooltip:g=!1}=e;const h=(0,P.fZ)();(0,l.FIv)(t,h,(t=>n(19,i=t)));const[L,j,w]=(0,z.V)({placement:$,strategy:f,middleware:[(0,S.cv)(10),(0,S.RR)(),(0,S.Qo)(),(0,z.x)({element:h})],onComputed({placement:t,middlewareData:e}){if((0,l.fxP)(x,o.computedPlacement=t,o),e.arrow){const{x:t,y:n}=e.arrow;Object.assign(i.style,{left:null!=t?`${t}px`:"",top:null!=n?`${n}px`:""})}}}),y=(0,I.x)(),k=(t=0)=>{window.clearTimeout(c),s||o.visible||(c=window.setTimeout((()=>{(0,l.fxP)(x,o.visible=!0,o),y("open")}),t))},T=(t=0)=>{window.clearTimeout(c),s||o.visible&&(c=window.setTimeout((()=>{(0,l.fxP)(x,o.visible=!1,o),g||a.focus(),y("close")}),t))},x=(0,P.fZ)({id:u,controlled:void 0!==e.visible,visible:p,dismissible:m,trapFocus:v,computedPlacement:$,tooltip:g,floatingRef:t=>{a=t,L(t)},floatingContent:j,arrowEl:h,onOutclick:t=>{m&&t.detail!==a&&T()},open:k,openTooltip:()=>{g&&k(300)},close:T,closeTooltip:()=>{g&&T(100)},toggle:()=>{o.visible?T():k()}});return(0,l.FIv)(t,x,(t=>n(0,o=t))),(0,I.v)(q,x),t.$$set=t=>{n(28,e=(0,l.f0i)((0,l.f0i)({},e),(0,l.Jvk)(t))),"id"in t&&n(6,u=t.id),"autoshow"in t&&n(7,p=t.autoshow),"visible"in t&&n(8,b=t.visible),"placement"in t&&n(9,$=t.placement),"strategy"in t&&n(10,f=t.strategy),"trapFocus"in t&&n(11,v=t.trapFocus),"dismissible"in t&&n(12,m=t.dismissible),"tooltip"in t&&n(13,g=t.tooltip),"$$scope"in t&&n(15,d=t.$$scope)},t.$$.update=()=>{n(14,s=void 0!==e.visible),16640&t.$$.dirty&&s&&(0,l.fxP)(x,o.visible=b,o),512&t.$$.dirty&&w({placement:$})},e=(0,l.Jvk)(e),[o,h,k,T,t=>{"Escape"===t.key&&m&&T()},x,u,p,b,$,f,v,m,g,s,d,r]}class W extends(/^(1565|3761|513|5621)$/.test(n.j)?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,H,Z,l.N8,{id:6,autoshow:7,visible:8,placement:9,strategy:10,trapFocus:11,dismissible:12,tooltip:13})}}const Y=/^(1565|3761|513|5621)$/.test(n.j)?W:null;function A(t){let e,n;const s=t[6].default,o=(0,l.nuO)(s,t,t[5],null);return{c(){e=(0,l.bGB)("span"),o&&o.c()},m(s,i){(0,l.$Tr)(s,e,i),o&&o.m(e,null),t[7](e),n=!0},p(t,[e]){o&&o.p&&(!n||32&e)&&(0,l.kmG)(o,s,t,t[5],n?(0,l.u2N)(s,t[5],e,null):(0,l.VOJ)(t[5]),null)},i(t){n||((0,l.Ui)(o,t),n=!0)},o(t){(0,l.etI)(o,t),n=!1},d(n){n&&(0,l.ogt)(e),o&&o.d(n),t[7](null)}}}function Q(t,e,n){let s,o,i,{$$slots:a={},$$scope:c}=e,{elementId:r=null}=e,d=K("PopoverReference");(0,l.FIv)(t,d,(t=>n(4,s=t)));return(0,I.H3)((()=>{n(3,i=((t,e,n)=>{const l=t?document.getElementById(t):e.firstElementChild;if(!l)throw new Error("No reference element found.");return n.floatingRef(l),l})(r,o,s)),s.controlled||(s.tooltip?((t,e)=>{t.addEventListener("mouseenter",e.openTooltip),t.addEventListener("mouseleave",e.closeTooltip),t.addEventListener("focusin",e.openTooltip),t.addEventListener("focusout",e.closeTooltip),t.setAttribute("aria-describedby",`${e.id}-popover`)})(i,s):((t,e)=>{if("button"!==t.tagName.toLowerCase()&&"button"!==t.role)throw new Error("Reference element must have a role of 'button' for uncontrolled popovers.");t.setAttribute("aria-controls",`${e.id}-popover`);const n=e.dismissible?e.toggle:e.open;t.addEventListener("click",n)})(i,s))})),t.$$set=t=>{"elementId"in t&&n(2,r=t.elementId),"$$scope"in t&&n(5,c=t.$$scope)},t.$$.update=()=>{24&t.$$.dirty&&(s.controlled||s.tooltip||i?.setAttribute("aria-expanded",Boolean(s.visible).toString()))},[o,d,r,i,s,c,a,function(t){l.VnY[t?"unshift":"push"]((()=>{o=t,n(0,o)}))}]}class M extends(/^(1565|3761|513|5621)$/.test(n.j)?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,Q,A,l.N8,{elementId:2})}}const tt=/^(1565|3761|513|5621)$/.test(n.j)?M:null;if(3761==n.j)var et=n(17843);function nt(t){let e,n,s,o,i,a;return n=new f({props:{src:et.LmC}}),{c(){e=(0,l.bGB)("button"),(0,l.YCL)(n.$$.fragment),(0,l.Ljt)(e,"aria-label",t[0]),(0,l.Ljt)(e,"class",s="s-popover--close s-btn s-btn__muted ps-absolute"+(t[1]?` ${t[1]}`:"")),(0,l.Ljt)(e,"type","button")},m(s,c){(0,l.$Tr)(s,e,c),(0,l.yef)(n,e,null),o=!0,i||(a=[(0,l.oLt)(e,"click",(function(){(0,l.sBU)(t[2].close)&&t[2].close.apply(this,arguments)})),(0,l.oLt)(e,"click",t[4])],i=!0)},p(n,[i]){t=n,(!o||1&i)&&(0,l.Ljt)(e,"aria-label",t[0]),(!o||2&i&&s!==(s="s-popover--close s-btn s-btn__muted ps-absolute"+(t[1]?` ${t[1]}`:"")))&&(0,l.Ljt)(e,"class",s)},i(t){o||((0,l.Ui)(n.$$.fragment,t),o=!0)},o(t){(0,l.etI)(n.$$.fragment,t),o=!1},d(t){t&&(0,l.ogt)(e),(0,l.vpE)(n),i=!1,(0,l.j7q)(a)}}}function lt(t,e,n){let s;const o=K("PopoverCloseButton");(0,l.FIv)(t,o,(t=>n(2,s=t)));let{label:i="Close"}=e,{class:a=""}=e;return t.$$set=t=>{"label"in t&&n(0,i=t.label),"class"in t&&n(1,a=t.class)},[i,a,s,o,function(e){l.cKT.call(this,t,e)}]}class st extends(3761==n.j?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,lt,nt,l.N8,{label:0,class:1})}}const ot=3761==n.j?st:null;function it(t){let e,n,s,o,i,a,c,r,d,u,p,b,$,f,v,m;const g=t[8].default,h=(0,l.nuO)(g,t,t[7],null);return{c(){e=(0,l.bGB)("div"),n=(0,l.bGB)("div"),s=(0,l.DhX)(),o=(0,l.bGB)("div"),i=(0,l.bGB)("div"),h&&h.c(),(0,l.Ljt)(n,"class","s-popover--arrow"),(0,l.Ljt)(i,"class","ps-relative"),(0,l.Ljt)(o,"class","s-popover--content p12 mn12"),(0,l.Ljt)(e,"id",a=`${t[2].id}-popover`),(0,l.Ljt)(e,"class",c=`${t[1]}${t[2].visible?" is-visible":""}`),(0,l.Ljt)(e,"role",r=t[0]||(t[2].tooltip?"tooltip":"dialog")),(0,l.Ljt)(e,"aria-hidden",d=!t[2].visible),(0,l.Ljt)(e,"data-popper-placement",u=t[2].computedPlacement)},m(a,c){(0,l.$Tr)(a,e,c),(0,l.R3I)(e,n),t[9](n),(0,l.R3I)(e,s),(0,l.R3I)(e,o),(0,l.R3I)(o,i),h&&h.m(i,null),f=!0,v||(m=[(0,l.TVh)(p=t[2].floatingContent(e)),(0,l.TVh)(b=T.e.call(null,e,{active:t[2].trapFocus&&!!t[2].visible})),(0,l.TVh)($=T.x.call(null,e)),(0,l.oLt)(e,"outclick",(function(){(0,l.sBU)(t[2].onOutclick)&&t[2].onOutclick.apply(this,arguments)})),(0,l.oLt)(e,"mouseenter",(function(){(0,l.sBU)(t[2].openTooltip)&&t[2].openTooltip.apply(this,arguments)})),(0,l.oLt)(e,"mouseleave",(function(){(0,l.sBU)(t[2].closeTooltip)&&t[2].closeTooltip.apply(this,arguments)})),(0,l.oLt)(e,"focusin",(function(){(0,l.sBU)(t[2].openTooltip)&&t[2].openTooltip.apply(this,arguments)})),(0,l.oLt)(e,"focusout",(function(){(0,l.sBU)(t[2].closeTooltip)&&t[2].closeTooltip.apply(this,arguments)}))],v=!0)},p(n,[s]){t=n,h&&h.p&&(!f||128&s)&&(0,l.kmG)(h,g,t,t[7],f?(0,l.u2N)(g,t[7],s,null):(0,l.VOJ)(t[7]),null),(!f||4&s&&a!==(a=`${t[2].id}-popover`))&&(0,l.Ljt)(e,"id",a),(!f||6&s&&c!==(c=`${t[1]}${t[2].visible?" is-visible":""}`))&&(0,l.Ljt)(e,"class",c),(!f||5&s&&r!==(r=t[0]||(t[2].tooltip?"tooltip":"dialog")))&&(0,l.Ljt)(e,"role",r),(!f||4&s&&d!==(d=!t[2].visible))&&(0,l.Ljt)(e,"aria-hidden",d),(!f||4&s&&u!==(u=t[2].computedPlacement))&&(0,l.Ljt)(e,"data-popper-placement",u),b&&(0,l.sBU)(b.update)&&4&s&&b.update.call(null,{active:t[2].trapFocus&&!!t[2].visible})},i(t){f||((0,l.Ui)(h,t),f=!0)},o(t){(0,l.etI)(h,t),f=!1},d(n){n&&(0,l.ogt)(e),t[9](null),h&&h.d(n),v=!1,(0,l.j7q)(m)}}}function at(t,e,n){let s,o,{$$slots:i={},$$scope:a}=e,{role:c=null}=e,{class:r=""}=e,d=K("PopoverContent");(0,l.FIv)(t,d,(t=>n(2,s=t)));let u="s-popover";const p=s.arrowEl;return(0,l.FIv)(t,p,(t=>n(3,o=t))),s.tooltip&&(u+=" s-popover__tooltip"),r&&(u+=" "+r),t.$$set=t=>{"role"in t&&n(0,c=t.role),"class"in t&&n(6,r=t.class),"$$scope"in t&&n(7,a=t.$$scope)},[c,u,s,o,d,p,r,a,i,function(t){l.VnY[t?"unshift":"push"]((()=>{o=t,p.set(o)}))}]}class ct extends(/^(1565|3761|513|5621)$/.test(n.j)?l.f_C:null){constructor(t){super(),(0,l.S1n)(this,t,at,it,l.N8,{role:0,class:6})}}const rt=/^(1565|3761|513|5621)$/.test(n.j)?ct:null}}]);