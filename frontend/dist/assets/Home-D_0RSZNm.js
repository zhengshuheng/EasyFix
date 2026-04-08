import{_ as Hf,s as kf,a as Wf}from"./_plugin-vue_export-helper-TVmdkUQu.js";import{c as Yt,e as Y,S as Nr,a as Uu,i as St,b as ui,m as Xf,p as jf,d as Vu,f as Nt,C as Zf,g as we,h as qf,j as Be,k as Yf,l as Hu,n as ho,o as $f,q as ji,M as zr,r as un,w as ms,_ as me,B as Ur,s as Kf,t as Jf,u as fi,v as Qf,x as ec,y as Bo,z as Zt,A as hn,D as tc,E as ku,F as Kt,G as rc,H as ic,I as Zn,J as mt,T as nc,K as ac,L as Jt,N as _t,O as dr,P as oc,Q as sc,R as lc,U as uc,V as hc,W as fc,X as _s,Y as cc,Z as Fo,$ as Wu,a0 as Ct,a1 as Ut,a2 as pt,a3 as dc,a4 as $t,a5 as Zi,a6 as ft,a7 as ys,a8 as vc,a9 as pc,aa as qn,ab as fn,ac as gc,ad as ha,ae as lt,af as fa,ag as qi,ah as xs,ai as Xu,aj as ju,ak as Go,al as ci,am as ai,an as mc,ao as Ts,ap as cn,aq as ws,ar as zo,as as Xr,at as Yn,au as Ss,av as He,aw as Yi,ax as bs,ay as it,az as As,aA as gr,aB as _c,aC as yc,aD as Es,aE as xc,aF as Tc,aG as Uo,aH as wc,aI as Ls,aJ as Cs,aK as Sc,aL as bc,aM as Ac,aN as Ec,aO as Lc,aP as Rt,aQ as le,aR as Cc,aS as Mc,aT as Zu,aU as qu,aV as fo,aW as Dc,aX as wa,aY as dn,aZ as Pc,a_ as Ms,a$ as Ds,b0 as Nc,b1 as co,b2 as Ic,b3 as Rc,b4 as Yu,b5 as Oc,b6 as Bc,b7 as Ps,b8 as Ns,b9 as Qt,ba as Fc,bb as $u,bc as Ku,bd as Vo,be as Gc,bf as zc,bg as Uc,bh as Vc,bi as Is,bj as Hc,bk as kc,bl as Rs,bm as Ne,bn as Wc,bo as Xc,bp as ce,bq as $i,br as jc,bs as Ju,bt as Qu,bu as Ho,bv as Zc,bw as eh,bx as qc,by as Yc,bz as $c,bA as xn,bB as Kc,bC as Jc,bD as Qc,bE as ed,bF as td,bG as Os,bH as rd,bI as th,bJ as id,bK as nd,bL as rh,bM as vo,bN as ad,bO as od,bP as sd,bQ as ld,bR as ih,bS as $n,bT as nh,bU as ah,bV as po,bW as vn,bX as ko,bY as ud,bZ as hd,b_ as oi,b$ as Bs,c0 as fd,c1 as cd,c2 as oh,c3 as dd,c4 as vd,c5 as Fs,c6 as Gs,c7 as pd,c8 as gd,c9 as md,ca as _d}from"./install-ByvwahZo.js";import{o as yd,a as Bt,c as Zr,b as J,w as re,d as O,t as Ee,u as zs,e as Tn,F as Sa,r as ba,f as nr,g as wn,h as $e,i as Sr}from"./index-C5VSoMlN.js";const xd="/icons/%E9%94%99%E9%A2%98%E6%80%BB%E6%95%B0.png",Td="/icons/%E5%AD%A6%E7%A7%91%E6%95%B0%E9%87%8F.png",wd="/icons/%E6%B4%BB%E8%B7%83%E5%AD%A6%E4%B9%A0%E5%A4%A9%E6%95%B0.png",Us="/icons/%E5%BE%85%E5%A4%8D%E4%B9%A0(%E9%94%99%E9%A2%98).png",Sd="/icons/%E5%A4%8D%E4%B9%A0%E6%AC%A1%E6%95%B0.png",bd="/icons/%E5%8D%95%E8%AF%8D%E6%80%BB%E6%95%B0.png",Ad="/icons/%E5%B7%B2%E5%A4%8D%E4%B9%A0%E5%8D%95%E8%AF%8D.png",Ed="/icons/%E5%8D%95%E8%AF%8D%E6%AD%A3%E7%A1%AE%E7%8E%87.png";var Ld=function(){function e(t){this.coordSysDims=[],this.axisMap=Yt(),this.categoryAxisMap=Yt(),this.coordSysName=t}return e}();function Cd(e){var t=e.get("coordinateSystem"),r=new Ld(t),i=Md[t];if(i)return i(e,r,r.axisMap,r.categoryAxisMap),r}var Md={cartesian2d:function(e,t,r,i){var n=e.getReferringComponents("xAxis",Nr).models[0],a=e.getReferringComponents("yAxis",Nr).models[0];t.coordSysDims=["x","y"],r.set("x",n),r.set("y",a),qr(n)&&(i.set("x",n),t.firstCategoryDimIndex=0),qr(a)&&(i.set("y",a),t.firstCategoryDimIndex==null&&(t.firstCategoryDimIndex=1))},singleAxis:function(e,t,r,i){var n=e.getReferringComponents("singleAxis",Nr).models[0];t.coordSysDims=["single"],r.set("single",n),qr(n)&&(i.set("single",n),t.firstCategoryDimIndex=0)},polar:function(e,t,r,i){var n=e.getReferringComponents("polar",Nr).models[0],a=n.findAxisModel("radiusAxis"),o=n.findAxisModel("angleAxis");t.coordSysDims=["radius","angle"],r.set("radius",a),r.set("angle",o),qr(a)&&(i.set("radius",a),t.firstCategoryDimIndex=0),qr(o)&&(i.set("angle",o),t.firstCategoryDimIndex==null&&(t.firstCategoryDimIndex=1))},geo:function(e,t,r,i){t.coordSysDims=["lng","lat"]},parallel:function(e,t,r,i){var n=e.ecModel,a=n.getComponent("parallel",e.get("parallelIndex")),o=t.coordSysDims=a.dimensions.slice();Y(a.parallelAxisIndex,function(s,l){var u=n.getComponent("parallelAxis",s),h=o[l];r.set(h,u),qr(u)&&(i.set(h,u),t.firstCategoryDimIndex==null&&(t.firstCategoryDimIndex=l))})}};function qr(e){return e.get("type")==="category"}function Dd(e,t){var r=e.get("coordinateSystem"),i=Zf.get(r),n;return t&&t.coordSysDims&&(n=we(t.coordSysDims,function(a){var o={name:a},s=t.axisMap.get(a);if(s){var l=s.get("type");o.type=qf(l)}return o})),n||(n=i&&(i.getDimensionsInfo?i.getDimensionsInfo():i.dimensions.slice())||["x","y"]),n}function Pd(e,t,r){var i,n;return r&&Y(e,function(a,o){var s=a.coordDim,l=r.categoryAxisMap.get(s);l&&(i==null&&(i=o),a.ordinalMeta=l.getOrdinalMeta(),t&&(a.createInvertedIndices=!0)),a.otherDims.itemName!=null&&(n=!0)}),!n&&i!=null&&(e[i].otherDims.itemName=0),i}function ca(e,t,r){r=r||{};var i=t.getSourceManager(),n,a=!1;n=i.getSource(),a=n.sourceFormat===Uu;var o=Cd(t),s=Dd(t,o),l=r.useEncodeDefaulter,u=St(l)?l:l?ui(Xf,s,t):null,h={coordDimensions:s,generateCoord:r.generateCoord,encodeDefine:t.getEncode(),encodeDefaulter:u,canOmitUnusedDimensions:!a},f=jf(n,h),d=Pd(f.dimensions,r.createInvertedIndices,o),c=a?null:i.getSharedDataStore(f),v=Vu(t,{schema:f,store:c}),p=new Nt(f,t);p.setCalculationInfo(v);var _=d!=null&&Nd(n)?function(m,g,y,x){return x===d?y:this.defaultDimValueGetter(m,g,y,x)}:null;return p.hasItemOption=!1,p.initData(a?n:c,null,_),p}function Nd(e){if(e.sourceFormat===Uu){var t=Id(e.data||[]);return!Be(Yf(t))}}function Id(e){for(var t=0;t<e.length&&e[t]==null;)t++;return e[t]}var Wo=function(){function e(){}return e.prototype.getNeedCrossZero=function(){var t=this.option;return!t.scale},e.prototype.getCoordSysModel=function(){},e}();function Rd(e){return ca(null,e)}var Xo={isDimensionStacked:ji,enableDataStack:Vu,getStackedDimension:$f};function jo(e,t){var r=t;t instanceof zr||(r=new zr(t));var i=Hu(r);return i.setExtent(e[0],e[1]),ho(i,r),i}function Od(e){un(e,Wo)}var Bd=1e-8;function Vs(e,t){return Math.abs(e-t)<Bd}function Hs(e,t,r){var i=0,n=e[0];if(!n)return!1;for(var a=1;a<e.length;a++){var o=e[a];i+=ms(n[0],n[1],o[0],o[1],t,r),n=o}var s=e[0];return(!Vs(n[0],s[0])||!Vs(n[1],s[1]))&&(i+=ms(n[0],n[1],s[0],s[1],t,r)),i!==0}var Fd=[];function Aa(e,t){for(var r=0;r<e.length;r++)fi(e[r],e[r],t)}function ks(e,t,r,i){for(var n=0;n<e.length;n++){var a=e[n];i&&(a=i.project(a)),a&&isFinite(a[0])&&isFinite(a[1])&&(Kf(t,t,a),Jf(r,r,a))}}function Gd(e){for(var t=0,r=0,i=0,n=e.length,a=e[n-1][0],o=e[n-1][1],s=0;s<n;s++){var l=e[s][0],u=e[s][1],h=a*u-l*o;t+=h,r+=(a+l)*h,i+=(o+u)*h,a=l,o=u}return t?[r/t/3,i/t/3,t]:[e[0][0]||0,e[0][1]||0]}var sh=function(){function e(t){this.name=t}return e.prototype.setCenter=function(t){this._center=t},e.prototype.getCenter=function(){var t=this._center;return t||(t=this._center=this.calcCenter()),t},e}(),Ws=function(){function e(t,r){this.type="polygon",this.exterior=t,this.interiors=r}return e}(),Xs=function(){function e(t){this.type="linestring",this.points=t}return e}(),zd=function(e){me(t,e);function t(r,i,n){var a=e.call(this,r)||this;return a.type="geoJSON",a.geometries=i,a._center=n&&[n[0],n[1]],a}return t.prototype.calcCenter=function(){for(var r=this.geometries,i,n=0,a=0;a<r.length;a++){var o=r[a],s=o.exterior,l=s&&s.length;l>n&&(i=o,n=l)}if(i)return Gd(i.exterior);var u=this.getBoundingRect();return[u.x+u.width/2,u.y+u.height/2]},t.prototype.getBoundingRect=function(r){var i=this._rect;if(i&&!r)return i;var n=[1/0,1/0],a=[-1/0,-1/0],o=this.geometries;return Y(o,function(s){s.type==="polygon"?ks(s.exterior,n,a,r):Y(s.points,function(l){ks(l,n,a,r)})}),isFinite(n[0])&&isFinite(n[1])&&isFinite(a[0])&&isFinite(a[1])||(n[0]=n[1]=a[0]=a[1]=0),i=new Ur(n[0],n[1],a[0]-n[0],a[1]-n[1]),r||(this._rect=i),i},t.prototype.contain=function(r){var i=this.getBoundingRect(),n=this.geometries;if(!i.contain(r[0],r[1]))return!1;e:for(var a=0,o=n.length;a<o;a++){var s=n[a];if(s.type==="polygon"){var l=s.exterior,u=s.interiors;if(Hs(l,r[0],r[1])){for(var h=0;h<(u?u.length:0);h++)if(Hs(u[h],r[0],r[1]))continue e;return!0}}}return!1},t.prototype.transformTo=function(r,i,n,a){var o=this.getBoundingRect(),s=o.width/o.height;n?a||(a=n/s):n=s*a;for(var l=new Ur(r,i,n,a),u=o.calculateTransform(l),h=this.geometries,f=0;f<h.length;f++){var d=h[f];d.type==="polygon"?(Aa(d.exterior,u),Y(d.interiors,function(c){Aa(c,u)})):Y(d.points,function(c){Aa(c,u)})}o=this._rect,o.copy(l),this._center=[o.x+o.width/2,o.y+o.height/2]},t.prototype.cloneShallow=function(r){r==null&&(r=this.name);var i=new t(r,this.geometries,this._center);return i._rect=this._rect,i.transformTo=null,i},t}(sh);(function(e){me(t,e);function t(r,i){var n=e.call(this,r)||this;return n.type="geoSVG",n._elOnlyForCalculate=i,n}return t.prototype.calcCenter=function(){for(var r=this._elOnlyForCalculate,i=r.getBoundingRect(),n=[i.x+i.width/2,i.y+i.height/2],a=Qf(Fd),o=r;o&&!o.isGeoSVGGraphicRoot;)ec(a,o.getLocalTransform(),a),o=o.parent;return Bo(a,a),fi(n,n,a),n},t})(sh);function Ud(e){if(!e.UTF8Encoding)return e;var t=e,r=t.UTF8Scale;r==null&&(r=1024);var i=t.features;return Y(i,function(n){var a=n.geometry,o=a.encodeOffsets,s=a.coordinates;if(o)switch(a.type){case"LineString":a.coordinates=lh(s,o,r);break;case"Polygon":Ea(s,o,r);break;case"MultiLineString":Ea(s,o,r);break;case"MultiPolygon":Y(s,function(l,u){return Ea(l,o[u],r)})}}),t.UTF8Encoding=!1,t}function Ea(e,t,r){for(var i=0;i<e.length;i++)e[i]=lh(e[i],t[i],r)}function lh(e,t,r){for(var i=[],n=t[0],a=t[1],o=0;o<e.length;o+=2){var s=e.charCodeAt(o)-64,l=e.charCodeAt(o+1)-64;s=s>>1^-(s&1),l=l>>1^-(l&1),s+=n,l+=a,n=s,a=l,i.push([s/r,l/r])}return i}function js(e,t){return e=Ud(e),we(Zt(e.features,function(r){return r.geometry&&r.properties&&r.geometry.coordinates.length>0}),function(r){var i=r.properties,n=r.geometry,a=[];switch(n.type){case"Polygon":var o=n.coordinates;a.push(new Ws(o[0],o.slice(1)));break;case"MultiPolygon":Y(n.coordinates,function(l){l[0]&&a.push(new Ws(l[0],l.slice(1)))});break;case"LineString":a.push(new Xs([n.coordinates]));break;case"MultiLineString":a.push(new Xs(n.coordinates))}var s=new zd(i[t||"name"],a,i.cp);return s.properties=i,s})}var Ki=Kt();function uh(e,t){var r=we(t,function(i){return e.scale.parse(i)});return e.type==="time"&&r.length>0&&(r.sort(),r.unshift(r[0]),r.push(r[r.length-1])),r}function Vd(e){var t=e.getLabelModel().get("customValues");if(t){var r=hn(e),i=e.scale.getExtent(),n=uh(e,t),a=Zt(n,function(o){return o>=i[0]&&o<=i[1]});return{labels:we(a,function(o){var s={value:o};return{formattedLabel:r(s),rawLabel:e.scale.getLabel(s),tickValue:o}})}}return e.type==="category"?kd(e):Xd(e)}function Hd(e,t){var r=e.getTickModel().get("customValues");if(r){var i=e.scale.getExtent(),n=uh(e,r);return{ticks:Zt(n,function(a){return a>=i[0]&&a<=i[1]})}}return e.type==="category"?Wd(e,t):{ticks:we(e.scale.getTicks(),function(a){return a.value})}}function kd(e){var t=e.getLabelModel(),r=hh(e,t);return!t.get("show")||e.scale.isBlank()?{labels:[],labelCategoryInterval:r.labelCategoryInterval}:r}function hh(e,t){var r=fh(e,"labels"),i=ku(t),n=ch(r,i);if(n)return n;var a,o;return St(i)?a=ph(e,i):(o=i==="auto"?jd(e):i,a=vh(e,o)),dh(r,i,{labels:a,labelCategoryInterval:o})}function Wd(e,t){var r=fh(e,"ticks"),i=ku(t),n=ch(r,i);if(n)return n;var a,o;if((!t.get("show")||e.scale.isBlank())&&(a=[]),St(i))a=ph(e,i,!0);else if(i==="auto"){var s=hh(e,e.getLabelModel());o=s.labelCategoryInterval,a=we(s.labels,function(l){return l.tickValue})}else o=i,a=vh(e,o,!0);return dh(r,i,{ticks:a,tickCategoryInterval:o})}function Xd(e){var t=e.scale.getTicks(),r=hn(e);return{labels:we(t,function(i,n){return{level:i.level,formattedLabel:r(i,n),rawLabel:e.scale.getLabel(i),tickValue:i.value}})}}function fh(e,t){return Ki(e)[t]||(Ki(e)[t]=[])}function ch(e,t){for(var r=0;r<e.length;r++)if(e[r].key===t)return e[r].value}function dh(e,t,r){return e.push({key:t,value:r}),r}function jd(e){var t=Ki(e).autoInterval;return t??(Ki(e).autoInterval=e.calculateCategoryInterval())}function Zd(e){var t=qd(e),r=hn(e),i=(t.axisRotate-t.labelRotate)/180*Math.PI,n=e.scale,a=n.getExtent(),o=n.count();if(a[1]-a[0]<1)return 0;var s=1;o>40&&(s=Math.max(1,Math.floor(o/40)));for(var l=a[0],u=e.dataToCoord(l+1)-e.dataToCoord(l),h=Math.abs(u*Math.cos(i)),f=Math.abs(u*Math.sin(i)),d=0,c=0;l<=a[1];l+=s){var v=0,p=0,_=tc(r({value:l}),t.font,"center","top");v=_.width*1.3,p=_.height*1.3,d=Math.max(d,v,7),c=Math.max(c,p,7)}var m=d/h,g=c/f;isNaN(m)&&(m=1/0),isNaN(g)&&(g=1/0);var y=Math.max(0,Math.floor(Math.min(m,g))),x=Ki(e.model),w=e.getExtent(),T=x.lastAutoInterval,b=x.lastTickCount;return T!=null&&b!=null&&Math.abs(T-y)<=1&&Math.abs(b-o)<=1&&T>y&&x.axisExtent0===w[0]&&x.axisExtent1===w[1]?y=T:(x.lastTickCount=o,x.lastAutoInterval=y,x.axisExtent0=w[0],x.axisExtent1=w[1]),y}function qd(e){var t=e.getLabelModel();return{axisRotate:e.getRotate?e.getRotate():e.isHorizontal&&!e.isHorizontal()?90:0,labelRotate:t.get("rotate")||0,font:t.getFont()}}function vh(e,t,r){var i=hn(e),n=e.scale,a=n.getExtent(),o=e.getLabelModel(),s=[],l=Math.max((t||0)+1,1),u=a[0],h=n.count();u!==0&&l>1&&h/l>2&&(u=Math.round(Math.ceil(u/l)*l));var f=rc(e),d=o.get("showMinLabel")||f,c=o.get("showMaxLabel")||f;d&&u!==a[0]&&p(a[0]);for(var v=u;v<=a[1];v+=l)p(v);c&&v-l!==a[1]&&p(a[1]);function p(_){var m={value:_};s.push(r?_:{formattedLabel:i(m),rawLabel:n.getLabel(m),tickValue:_})}return s}function ph(e,t,r){var i=e.scale,n=hn(e),a=[];return Y(i.getTicks(),function(o){var s=i.getLabel(o),l=o.value;t(o.value,s)&&a.push(r?l:{formattedLabel:n(o),rawLabel:s,tickValue:l})}),a}var Zs=[0,1],Si=function(){function e(t,r,i){this.onBand=!1,this.inverse=!1,this.dim=t,this.scale=r,this._extent=i||[0,0]}return e.prototype.contain=function(t){var r=this._extent,i=Math.min(r[0],r[1]),n=Math.max(r[0],r[1]);return t>=i&&t<=n},e.prototype.containData=function(t){return this.scale.contain(t)},e.prototype.getExtent=function(){return this._extent.slice()},e.prototype.getPixelPrecision=function(t){return ic(t||this.scale.getExtent(),this._extent)},e.prototype.setExtent=function(t,r){var i=this._extent;i[0]=t,i[1]=r},e.prototype.dataToCoord=function(t,r){var i=this._extent,n=this.scale;return t=n.normalize(t),this.onBand&&n.type==="ordinal"&&(i=i.slice(),qs(i,n.count())),Zn(t,Zs,i,r)},e.prototype.coordToData=function(t,r){var i=this._extent,n=this.scale;this.onBand&&n.type==="ordinal"&&(i=i.slice(),qs(i,n.count()));var a=Zn(t,i,Zs,r);return this.scale.scale(a)},e.prototype.pointToData=function(t,r){},e.prototype.getTicksCoords=function(t){t=t||{};var r=t.tickModel||this.getTickModel(),i=Hd(this,r),n=i.ticks,a=we(n,function(s){return{coord:this.dataToCoord(this.scale.type==="ordinal"?this.scale.getRawOrdinalNumber(s):s),tickValue:s}},this),o=r.get("alignWithLabel");return Yd(this,a,o,t.clamp),a},e.prototype.getMinorTicksCoords=function(){if(this.scale.type==="ordinal")return[];var t=this.model.getModel("minorTick"),r=t.get("splitNumber");r>0&&r<100||(r=5);var i=this.scale.getMinorTicks(r),n=we(i,function(a){return we(a,function(o){return{coord:this.dataToCoord(o),tickValue:o}},this)},this);return n},e.prototype.getViewLabels=function(){return Vd(this).labels},e.prototype.getLabelModel=function(){return this.model.getModel("axisLabel")},e.prototype.getTickModel=function(){return this.model.getModel("axisTick")},e.prototype.getBandWidth=function(){var t=this._extent,r=this.scale.getExtent(),i=r[1]-r[0]+(this.onBand?1:0);i===0&&(i=1);var n=Math.abs(t[1]-t[0]);return Math.abs(n)/i},e.prototype.calculateCategoryInterval=function(){return Zd(this)},e}();function qs(e,t){var r=e[1]-e[0],i=t,n=r/i/2;e[0]+=n,e[1]-=n}function Yd(e,t,r,i){var n=t.length;if(!e.onBand||r||!n)return;var a=e.getExtent(),o,s;if(n===1)t[0].coord=a[0],o=t[1]={coord:a[1],tickValue:t[0].tickValue};else{var l=t[n-1].tickValue-t[0].tickValue,u=(t[n-1].coord-t[0].coord)/l;Y(t,function(c){c.coord-=u/2});var h=e.scale.getExtent();s=1+h[1]-t[n-1].tickValue,o={coord:t[n-1].coord+u*s,tickValue:h[1]+1},t.push(o)}var f=a[0]>a[1];d(t[0].coord,a[0])&&(i?t[0].coord=a[0]:t.shift()),i&&d(a[0],t[0].coord)&&t.unshift({coord:a[0]}),d(a[1],o.coord)&&(i?o.coord=a[1]:t.pop()),i&&d(o.coord,a[1])&&t.push({coord:a[1]});function d(c,v){return c=mt(c),v=mt(v),f?c>v:c<v}}function $d(e){if(e){for(var t=[],r=0;r<e.length;r++)t.push(e[r].slice());return t}}function Kd(e,t){var r=e.label,i=t&&t.getTextGuideLine();return{dataIndex:e.dataIndex,dataType:e.dataType,seriesIndex:e.seriesModel.seriesIndex,text:e.label.style.text,rect:e.hostRect,labelRect:e.rect,align:r.style.align,verticalAlign:r.style.verticalAlign,labelLinePoints:$d(i&&i.shape.points)}}var Ys=["align","verticalAlign","width","height","fontSize"],nt=new nc,La=Kt(),Jd=Kt();function Sn(e,t,r){for(var i=0;i<r.length;i++){var n=r[i];t[n]!=null&&(e[n]=t[n])}}var bn=["x","y","rotation"],Qd=function(){function e(){this._labelList=[],this._chartViewList=[]}return e.prototype.clearLabels=function(){this._labelList=[],this._chartViewList=[]},e.prototype._addLabel=function(t,r,i,n,a){var o=n.style,s=n.__hostTarget,l=s.textConfig||{},u=n.getComputedTransform(),h=n.getBoundingRect().plain();Ur.applyTransform(h,h,u),u?nt.setLocalTransform(u):(nt.x=nt.y=nt.rotation=nt.originX=nt.originY=0,nt.scaleX=nt.scaleY=1),nt.rotation=ac(nt.rotation);var f=n.__hostTarget,d;if(f){d=f.getBoundingRect().plain();var c=f.getComputedTransform();Ur.applyTransform(d,d,c)}var v=d&&f.getTextGuideLine();this._labelList.push({label:n,labelLine:v,seriesModel:i,dataIndex:t,dataType:r,layoutOption:a,computedLayoutOption:null,rect:h,hostRect:d,priority:d?d.width*d.height:0,defaultAttr:{ignore:n.ignore,labelGuideIgnore:v&&v.ignore,x:nt.x,y:nt.y,scaleX:nt.scaleX,scaleY:nt.scaleY,rotation:nt.rotation,style:{x:o.x,y:o.y,align:o.align,verticalAlign:o.verticalAlign,width:o.width,height:o.height,fontSize:o.fontSize},cursor:n.cursor,attachedPos:l.position,attachedRot:l.rotation}})},e.prototype.addLabelsOfSeries=function(t){var r=this;this._chartViewList.push(t);var i=t.__model,n=i.get("labelLayout");(St(n)||Jt(n).length)&&t.group.traverse(function(a){if(a.ignore)return!0;var o=a.getTextContent(),s=_t(a);o&&!o.disableLabelLayout&&r._addLabel(s.dataIndex,s.dataType,i,o,n)})},e.prototype.updateLayoutConfig=function(t){var r=t.getWidth(),i=t.getHeight();function n(y,x){return function(){_s(y,x)}}for(var a=0;a<this._labelList.length;a++){var o=this._labelList[a],s=o.label,l=s.__hostTarget,u=o.defaultAttr,h=void 0;St(o.layoutOption)?h=o.layoutOption(Kd(o,l)):h=o.layoutOption,h=h||{},o.computedLayoutOption=h;var f=Math.PI/180;l&&l.setTextConfig({local:!1,position:h.x!=null||h.y!=null?null:u.attachedPos,rotation:h.rotate!=null?h.rotate*f:u.attachedRot,offset:[h.dx||0,h.dy||0]});var d=!1;if(h.x!=null?(s.x=dr(h.x,r),s.setStyle("x",0),d=!0):(s.x=u.x,s.setStyle("x",u.style.x)),h.y!=null?(s.y=dr(h.y,i),s.setStyle("y",0),d=!0):(s.y=u.y,s.setStyle("y",u.style.y)),h.labelLinePoints){var c=l.getTextGuideLine();c&&(c.setShape({points:h.labelLinePoints}),d=!1)}var v=La(s);v.needsUpdateLabelLine=d,s.rotation=h.rotate!=null?h.rotate*f:u.rotation,s.scaleX=u.scaleX,s.scaleY=u.scaleY;for(var p=0;p<Ys.length;p++){var _=Ys[p];s.setStyle(_,h[_]!=null?h[_]:u.style[_])}if(h.draggable){if(s.draggable=!0,s.cursor="move",l){var m=o.seriesModel;if(o.dataIndex!=null){var g=o.seriesModel.getData(o.dataType);m=g.getItemModel(o.dataIndex)}s.on("drag",n(l,m.getModel("labelLine")))}}else s.off("drag"),s.cursor=u.cursor}},e.prototype.layout=function(t){var r=t.getWidth(),i=t.getHeight(),n=oc(this._labelList),a=Zt(n,function(l){return l.layoutOption.moveOverlap==="shiftX"}),o=Zt(n,function(l){return l.layoutOption.moveOverlap==="shiftY"});sc(a,0,r),lc(o,0,i);var s=Zt(n,function(l){return l.layoutOption.hideOverlap});uc(s)},e.prototype.processLabelsOverall=function(){var t=this;Y(this._chartViewList,function(r){var i=r.__model,n=r.ignoreLabelLineUpdate,a=i.isAnimationEnabled();r.group.traverse(function(o){if(o.ignore&&!o.forceLabelAnimation)return!0;var s=!n,l=o.getTextContent();!s&&l&&(s=La(l).needsUpdateLabelLine),s&&t._updateLabelLine(o,i),a&&t._animateLabels(o,i)})})},e.prototype._updateLabelLine=function(t,r){var i=t.getTextContent(),n=_t(t),a=n.dataIndex;if(i&&a!=null){var o=r.getData(n.dataType),s=o.getItemModel(a),l={},u=o.getItemVisual(a,"style");if(u){var h=o.getVisual("drawType");l.stroke=u[h]}var f=s.getModel("labelLine");hc(t,fc(s),l),_s(t,f)}},e.prototype._animateLabels=function(t,r){var i=t.getTextContent(),n=t.getTextGuideLine();if(i&&(t.forceLabelAnimation||!i.ignore&&!i.invisible&&!t.disableLabelAnimation&&!cc(t))){var a=La(i),o=a.oldLayout,s=_t(t),l=s.dataIndex,u={x:i.x,y:i.y,rotation:i.rotation},h=r.getData(s.dataType);if(o){i.attr(o);var d=t.prevStates;d&&(Ut(d,"select")>=0&&i.attr(a.oldLayoutSelect),Ut(d,"emphasis")>=0&&i.attr(a.oldLayoutEmphasis)),pt(i,u,r,l)}else if(i.attr(u),!Fo(i).valueAnimation){var f=Wu(i.style.opacity,1);i.style.opacity=0,Ct(i,{style:{opacity:f}},r,l)}if(a.oldLayout=u,i.states.select){var c=a.oldLayoutSelect={};Sn(c,u,bn),Sn(c,i.states.select,bn)}if(i.states.emphasis){var v=a.oldLayoutEmphasis={};Sn(v,u,bn),Sn(v,i.states.emphasis,bn)}dc(i,l,h,r,r)}if(n&&!n.ignore&&!n.invisible){var a=Jd(n),o=a.oldLayout,p={points:n.shape.points};o?(n.attr({shape:o}),pt(n,{shape:p},r)):(n.setShape(p),n.style.strokePercent=0,Ct(n,{style:{strokePercent:1}},r)),a.oldLayout=p}},e}(),Ca=Kt();function ev(e){e.registerUpdateLifecycle("series:beforeupdate",function(t,r,i){var n=Ca(r).labelManager;n||(n=Ca(r).labelManager=new Qd),n.clearLabels()}),e.registerUpdateLifecycle("series:layoutlabels",function(t,r,i){var n=Ca(r).labelManager;i.updatedSeries.forEach(function(a){n.addLabelsOfSeries(r.getViewOfSeriesModel(a))}),n.updateLayoutConfig(r),n.layout(r),n.processLabelsOverall()})}var tv=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r.hasSymbolVisual=!0,r}return t.prototype.getInitialData=function(r){return ca(null,this,{useEncodeDefaulter:!0})},t.prototype.getLegendIcon=function(r){var i=new $t,n=Zi("line",0,r.itemHeight/2,r.itemWidth,0,r.lineStyle.stroke,!1);i.add(n),n.setStyle(r.lineStyle);var a=this.getData().getVisual("symbol"),o=this.getData().getVisual("symbolRotate"),s=a==="none"?"circle":a,l=r.itemHeight*.8,u=Zi(s,(r.itemWidth-l)/2,(r.itemHeight-l)/2,l,l,r.itemStyle.fill);i.add(u),u.setStyle(r.itemStyle);var h=r.iconRotate==="inherit"?o:r.iconRotate||0;return u.rotation=h*Math.PI/180,u.setOrigin([r.itemWidth/2,r.itemHeight/2]),s.indexOf("empty")>-1&&(u.style.stroke=u.style.fill,u.style.fill="#fff",u.style.lineWidth=2),i},t.type="series.line",t.dependencies=["grid","polar"],t.defaultOption={z:3,coordinateSystem:"cartesian2d",legendHoverLink:!0,clip:!0,label:{position:"top"},endLabel:{show:!1,valueAnimation:!0,distance:8},lineStyle:{width:2,type:"solid"},emphasis:{scale:!0},step:!1,smooth:!1,smoothMonotone:null,symbol:"emptyCircle",symbolSize:4,symbolRotate:null,showSymbol:!0,showAllSymbol:"auto",connectNulls:!1,sampling:"none",animationEasing:"linear",progressive:0,hoverLayerThreshold:1/0,universalTransition:{divideShape:"clone"},triggerLineEvent:!1},t}(ft);function Zo(e,t){var r=e.mapDimensionsAll("defaultedLabel"),i=r.length;if(i===1){var n=ys(e,t,r[0]);return n!=null?n+"":null}else if(i){for(var a=[],o=0;o<r.length;o++)a.push(ys(e,t,r[o]));return a.join(" ")}}function gh(e,t){var r=e.mapDimensionsAll("defaultedLabel");if(!Be(t))return t+"";for(var i=[],n=0;n<r.length;n++){var a=e.getDimensionIndex(r[n]);a>=0&&i.push(t[a])}return i.join(" ")}var qo=function(e){me(t,e);function t(r,i,n,a){var o=e.call(this)||this;return o.updateData(r,i,n,a),o}return t.prototype._createSymbol=function(r,i,n,a,o){this.removeAll();var s=Zi(r,-1,-1,2,2,null,o);s.attr({z2:100,culling:!0,scaleX:a[0]/2,scaleY:a[1]/2}),s.drift=rv,this._symbolType=r,this.add(s)},t.prototype.stopSymbolAnimation=function(r){this.childAt(0).stopAnimation(null,r)},t.prototype.getSymbolType=function(){return this._symbolType},t.prototype.getSymbolPath=function(){return this.childAt(0)},t.prototype.highlight=function(){vc(this.childAt(0))},t.prototype.downplay=function(){pc(this.childAt(0))},t.prototype.setZ=function(r,i){var n=this.childAt(0);n.zlevel=r,n.z=i},t.prototype.setDraggable=function(r,i){var n=this.childAt(0);n.draggable=r,n.cursor=!i&&r?"move":n.cursor},t.prototype.updateData=function(r,i,n,a){this.silent=!1;var o=r.getItemVisual(i,"symbol")||"circle",s=r.hostModel,l=t.getSymbolSize(r,i),u=o!==this._symbolType,h=a&&a.disableAnimation;if(u){var f=r.getItemVisual(i,"symbolKeepAspect");this._createSymbol(o,r,i,l,f)}else{var d=this.childAt(0);d.silent=!1;var c={scaleX:l[0]/2,scaleY:l[1]/2};h?d.attr(c):pt(d,c,s,i),qn(d)}if(this._updateCommon(r,i,l,n,a),u){var d=this.childAt(0);if(!h){var c={scaleX:this._sizeX,scaleY:this._sizeY,style:{opacity:d.style.opacity}};d.scaleX=d.scaleY=0,d.style.opacity=0,Ct(d,c,s,i)}}h&&this.childAt(0).stopAnimation("leave")},t.prototype._updateCommon=function(r,i,n,a,o){var s=this.childAt(0),l=r.hostModel,u,h,f,d,c,v,p,_,m;if(a&&(u=a.emphasisItemStyle,h=a.blurItemStyle,f=a.selectItemStyle,d=a.focus,c=a.blurScope,p=a.labelStatesModels,_=a.hoverScale,m=a.cursorStyle,v=a.emphasisDisabled),!a||r.hasItemOption){var g=a&&a.itemModel?a.itemModel:r.getItemModel(i),y=g.getModel("emphasis");u=y.getModel("itemStyle").getItemStyle(),f=g.getModel(["select","itemStyle"]).getItemStyle(),h=g.getModel(["blur","itemStyle"]).getItemStyle(),d=y.get("focus"),c=y.get("blurScope"),v=y.get("disabled"),p=fn(g),_=y.getShallow("scale"),m=g.getShallow("cursor")}var x=r.getItemVisual(i,"symbolRotate");s.attr("rotation",(x||0)*Math.PI/180||0);var w=gc(r.getItemVisual(i,"symbolOffset"),n);w&&(s.x=w[0],s.y=w[1]),m&&s.attr("cursor",m);var T=r.getItemVisual(i,"style"),b=T.fill;if(s instanceof ha){var A=s.style;s.useStyle(lt({image:A.image,x:A.x,y:A.y,width:A.width,height:A.height},T))}else s.__isEmptyBrush?s.useStyle(lt({},T)):s.useStyle(T),s.style.decal=null,s.setColor(b,o&&o.symbolInnerColor),s.style.strokeNoScale=!0;var C=r.getItemVisual(i,"liftZ"),D=this._z2;C!=null?D==null&&(this._z2=s.z2,s.z2+=C):D!=null&&(s.z2=D,this._z2=null);var L=o&&o.useNameLabel;fa(s,p,{labelFetcher:l,labelDataIndex:i,defaultText:M,inheritColor:b,defaultOpacity:T.opacity});function M(I){return L?r.getName(I):Zo(r,I)}this._sizeX=n[0]/2,this._sizeY=n[1]/2;var P=s.ensureState("emphasis");P.style=u,s.ensureState("select").style=f,s.ensureState("blur").style=h;var N=_==null||_===!0?Math.max(1.1,3/this._sizeY):isFinite(_)&&_>0?+_:1;P.scaleX=this._sizeX*N,P.scaleY=this._sizeY*N,this.setSymbolScale(1),qi(this,d,c,v)},t.prototype.setSymbolScale=function(r){this.scaleX=this.scaleY=r},t.prototype.fadeOut=function(r,i,n){var a=this.childAt(0),o=_t(this).dataIndex,s=n&&n.animation;if(this.silent=a.silent=!0,n&&n.fadeLabel){var l=a.getTextContent();l&&xs(l,{style:{opacity:0}},i,{dataIndex:o,removeOpt:s,cb:function(){a.removeTextContent()}})}else a.removeTextContent();xs(a,{style:{opacity:0},scaleX:0,scaleY:0},i,{dataIndex:o,cb:r,removeOpt:s})},t.getSymbolSize=function(r,i){return Xu(r.getItemVisual(i,"symbolSize"))},t}($t);function rv(e,t){this.parent.drift(e,t)}function Ma(e,t,r,i){return t&&!isNaN(t[0])&&!isNaN(t[1])&&!(i.isIgnore&&i.isIgnore(r))&&!(i.clipShape&&!i.clipShape.contain(t[0],t[1]))&&e.getItemVisual(r,"symbol")!=="none"}function $s(e){return e!=null&&!Go(e)&&(e={isIgnore:e}),e||{}}function Ks(e){var t=e.hostModel,r=t.getModel("emphasis");return{emphasisItemStyle:r.getModel("itemStyle").getItemStyle(),blurItemStyle:t.getModel(["blur","itemStyle"]).getItemStyle(),selectItemStyle:t.getModel(["select","itemStyle"]).getItemStyle(),focus:r.get("focus"),blurScope:r.get("blurScope"),emphasisDisabled:r.get("disabled"),hoverScale:r.get("scale"),labelStatesModels:fn(t),cursorStyle:t.get("cursor")}}var iv=function(){function e(t){this.group=new $t,this._SymbolCtor=t||qo}return e.prototype.updateData=function(t,r){this._progressiveEls=null,r=$s(r);var i=this.group,n=t.hostModel,a=this._data,o=this._SymbolCtor,s=r.disableAnimation,l=Ks(t),u={disableAnimation:s},h=r.getSymbolPoint||function(f){return t.getItemLayout(f)};a||i.removeAll(),t.diff(a).add(function(f){var d=h(f);if(Ma(t,d,f,r)){var c=new o(t,f,l,u);c.setPosition(d),t.setItemGraphicEl(f,c),i.add(c)}}).update(function(f,d){var c=a.getItemGraphicEl(d),v=h(f);if(!Ma(t,v,f,r)){i.remove(c);return}var p=t.getItemVisual(f,"symbol")||"circle",_=c&&c.getSymbolType&&c.getSymbolType();if(!c||_&&_!==p)i.remove(c),c=new o(t,f,l,u),c.setPosition(v);else{c.updateData(t,f,l,u);var m={x:v[0],y:v[1]};s?c.attr(m):pt(c,m,n)}i.add(c),t.setItemGraphicEl(f,c)}).remove(function(f){var d=a.getItemGraphicEl(f);d&&d.fadeOut(function(){i.remove(d)},n)}).execute(),this._getSymbolPoint=h,this._data=t},e.prototype.updateLayout=function(){var t=this,r=this._data;r&&r.eachItemGraphicEl(function(i,n){var a=t._getSymbolPoint(n);i.setPosition(a),i.markRedraw()})},e.prototype.incrementalPrepareUpdate=function(t){this._seriesScope=Ks(t),this._data=null,this.group.removeAll()},e.prototype.incrementalUpdate=function(t,r,i){this._progressiveEls=[],i=$s(i);function n(l){l.isGroup||(l.incremental=!0,l.ensureState("emphasis").hoverLayer=!0)}for(var a=t.start;a<t.end;a++){var o=r.getItemLayout(a);if(Ma(r,o,a,i)){var s=new this._SymbolCtor(r,a,this._seriesScope);s.traverse(n),s.setPosition(o),this.group.add(s),r.setItemGraphicEl(a,s),this._progressiveEls.push(s)}}},e.prototype.eachRendered=function(t){ju(this._progressiveEls||this.group,t)},e.prototype.remove=function(t){var r=this.group,i=this._data;i&&t?i.eachItemGraphicEl(function(n){n.fadeOut(function(){r.remove(n)},i.hostModel)}):r.removeAll()},e}();function mh(e,t,r){var i=e.getBaseAxis(),n=e.getOtherAxis(i),a=nv(n,r),o=i.dim,s=n.dim,l=t.mapDimension(s),u=t.mapDimension(o),h=s==="x"||s==="radius"?1:0,f=we(e.dimensions,function(v){return t.mapDimension(v)}),d=!1,c=t.getCalculationInfo("stackResultDimension");return ji(t,f[0])&&(d=!0,f[0]=c),ji(t,f[1])&&(d=!0,f[1]=c),{dataDimsForPoint:f,valueStart:a,valueAxisDim:s,baseAxisDim:o,stacked:!!d,valueDim:l,baseDim:u,baseDataOffset:h,stackedOverDimension:t.getCalculationInfo("stackedOverDimension")}}function nv(e,t){var r=0,i=e.scale.getExtent();return t==="start"?r=i[0]:t==="end"?r=i[1]:ci(t)&&!isNaN(t)?r=t:i[0]>0?r=i[0]:i[1]<0&&(r=i[1]),r}function _h(e,t,r,i){var n=NaN;e.stacked&&(n=r.get(r.getCalculationInfo("stackedOverDimension"),i)),isNaN(n)&&(n=e.valueStart);var a=e.baseDataOffset,o=[];return o[a]=r.get(e.baseDim,i),o[1-a]=n,t.dataToPoint(o)}function av(e,t){var r=[];return t.diff(e).add(function(i){r.push({cmd:"+",idx:i})}).update(function(i,n){r.push({cmd:"=",idx:n,idx1:i})}).remove(function(i){r.push({cmd:"-",idx:i})}).execute(),r}function ov(e,t,r,i,n,a,o,s){for(var l=av(e,t),u=[],h=[],f=[],d=[],c=[],v=[],p=[],_=mh(n,t,o),m=e.getLayout("points")||[],g=t.getLayout("points")||[],y=0;y<l.length;y++){var x=l[y],w=!0,T=void 0,b=void 0;switch(x.cmd){case"=":T=x.idx*2,b=x.idx1*2;var A=m[T],C=m[T+1],D=g[b],L=g[b+1];(isNaN(A)||isNaN(C))&&(A=D,C=L),u.push(A,C),h.push(D,L),f.push(r[T],r[T+1]),d.push(i[b],i[b+1]),p.push(t.getRawIndex(x.idx1));break;case"+":var M=x.idx,P=_.dataDimsForPoint,N=n.dataToPoint([t.get(P[0],M),t.get(P[1],M)]);b=M*2,u.push(N[0],N[1]),h.push(g[b],g[b+1]);var I=_h(_,n,t,M);f.push(I[0],I[1]),d.push(i[b],i[b+1]),p.push(t.getRawIndex(M));break;case"-":w=!1}w&&(c.push(x),v.push(v.length))}v.sort(function(ee,be){return p[ee]-p[be]});for(var V=u.length,Z=ai(V),B=ai(V),$=ai(V),q=ai(V),j=[],y=0;y<v.length;y++){var Q=v[y],ie=y*2,ae=Q*2;Z[ie]=u[ae],Z[ie+1]=u[ae+1],B[ie]=h[ae],B[ie+1]=h[ae+1],$[ie]=f[ae],$[ie+1]=f[ae+1],q[ie]=d[ae],q[ie+1]=d[ae+1],j[y]=c[Q]}return{current:Z,next:B,stackedOnCurrent:$,stackedOnNext:q,status:j}}var ar=Math.min,or=Math.max;function Br(e,t){return isNaN(e)||isNaN(t)}function go(e,t,r,i,n,a,o,s,l){for(var u,h,f,d,c,v,p=r,_=0;_<i;_++){var m=t[p*2],g=t[p*2+1];if(p>=n||p<0)break;if(Br(m,g)){if(l){p+=a;continue}break}if(p===r)e[a>0?"moveTo":"lineTo"](m,g),f=m,d=g;else{var y=m-u,x=g-h;if(y*y+x*x<.5){p+=a;continue}if(o>0){for(var w=p+a,T=t[w*2],b=t[w*2+1];T===m&&b===g&&_<i;)_++,w+=a,p+=a,T=t[w*2],b=t[w*2+1],m=t[p*2],g=t[p*2+1],y=m-u,x=g-h;var A=_+1;if(l)for(;Br(T,b)&&A<i;)A++,w+=a,T=t[w*2],b=t[w*2+1];var C=.5,D=0,L=0,M=void 0,P=void 0;if(A>=i||Br(T,b))c=m,v=g;else{D=T-u,L=b-h;var N=m-u,I=T-m,V=g-h,Z=b-g,B=void 0,$=void 0;if(s==="x"){B=Math.abs(N),$=Math.abs(I);var q=D>0?1:-1;c=m-q*B*o,v=g,M=m+q*$*o,P=g}else if(s==="y"){B=Math.abs(V),$=Math.abs(Z);var j=L>0?1:-1;c=m,v=g-j*B*o,M=m,P=g+j*$*o}else B=Math.sqrt(N*N+V*V),$=Math.sqrt(I*I+Z*Z),C=$/($+B),c=m-D*o*(1-C),v=g-L*o*(1-C),M=m+D*o*C,P=g+L*o*C,M=ar(M,or(T,m)),P=ar(P,or(b,g)),M=or(M,ar(T,m)),P=or(P,ar(b,g)),D=M-m,L=P-g,c=m-D*B/$,v=g-L*B/$,c=ar(c,or(u,m)),v=ar(v,or(h,g)),c=or(c,ar(u,m)),v=or(v,ar(h,g)),D=m-c,L=g-v,M=m+D*$/B,P=g+L*$/B}e.bezierCurveTo(f,d,c,v,m,g),f=M,d=P}else e.lineTo(m,g)}u=m,h=g,p+=a}return _}var yh=function(){function e(){this.smooth=0,this.smoothConstraint=!0}return e}(),sv=function(e){me(t,e);function t(r){var i=e.call(this,r)||this;return i.type="ec-polyline",i}return t.prototype.getDefaultStyle=function(){return{stroke:"#000",fill:null}},t.prototype.getDefaultShape=function(){return new yh},t.prototype.buildPath=function(r,i){var n=i.points,a=0,o=n.length/2;if(i.connectNulls){for(;o>0&&Br(n[o*2-2],n[o*2-1]);o--);for(;a<o&&Br(n[a*2],n[a*2+1]);a++);}for(;a<o;)a+=go(r,n,a,o,o,1,i.smooth,i.smoothMonotone,i.connectNulls)+1},t.prototype.getPointOn=function(r,i){this.path||(this.createPathProxy(),this.buildPath(this.path,this.shape));for(var n=this.path,a=n.data,o=mc.CMD,s,l,u=i==="x",h=[],f=0;f<a.length;){var d=a[f++],c=void 0,v=void 0,p=void 0,_=void 0,m=void 0,g=void 0,y=void 0;switch(d){case o.M:s=a[f++],l=a[f++];break;case o.L:if(c=a[f++],v=a[f++],y=u?(r-s)/(c-s):(r-l)/(v-l),y<=1&&y>=0){var x=u?(v-l)*y+l:(c-s)*y+s;return u?[r,x]:[x,r]}s=c,l=v;break;case o.C:c=a[f++],v=a[f++],p=a[f++],_=a[f++],m=a[f++],g=a[f++];var w=u?Ts(s,c,p,m,r,h):Ts(l,v,_,g,r,h);if(w>0)for(var T=0;T<w;T++){var b=h[T];if(b<=1&&b>=0){var x=u?ws(l,v,_,g,b):ws(s,c,p,m,b);return u?[r,x]:[x,r]}}s=m,l=g;break}}},t}(cn),lv=function(e){me(t,e);function t(){return e!==null&&e.apply(this,arguments)||this}return t}(yh),uv=function(e){me(t,e);function t(r){var i=e.call(this,r)||this;return i.type="ec-polygon",i}return t.prototype.getDefaultShape=function(){return new lv},t.prototype.buildPath=function(r,i){var n=i.points,a=i.stackedOnPoints,o=0,s=n.length/2,l=i.smoothMonotone;if(i.connectNulls){for(;s>0&&Br(n[s*2-2],n[s*2-1]);s--);for(;o<s&&Br(n[o*2],n[o*2+1]);o++);}for(;o<s;){var u=go(r,n,o,s,s,1,i.smooth,l,i.connectNulls);go(r,a,o+u-1,u,s,-1,i.stackedOnSmooth,l,i.connectNulls),o+=u+1,r.closePath()}},t}(cn);function xh(e,t,r,i,n){var a=e.getArea(),o=a.x,s=a.y,l=a.width,u=a.height,h=r.get(["lineStyle","width"])||0;o-=h/2,s-=h/2,l+=h,u+=h,l=Math.ceil(l),o!==Math.floor(o)&&(o=Math.floor(o),l++);var f=new Xr({shape:{x:o,y:s,width:l,height:u}});if(t){var d=e.getBaseAxis(),c=d.isHorizontal(),v=d.inverse;c?(v&&(f.shape.x+=l),f.shape.width=0):(v||(f.shape.y+=u),f.shape.height=0);var p=St(n)?function(_){n(_,f)}:null;Ct(f,{shape:{width:l,height:u,x:o,y:s}},r,null,i,p)}return f}function Th(e,t,r){var i=e.getArea(),n=mt(i.r0,1),a=mt(i.r,1),o=new zo({shape:{cx:mt(e.cx,1),cy:mt(e.cy,1),r0:n,r:a,startAngle:i.startAngle,endAngle:i.endAngle,clockwise:i.clockwise}});if(t){var s=e.getBaseAxis().dim==="angle";s?o.shape.endAngle=i.startAngle:o.shape.r=n,Ct(o,{shape:{endAngle:i.endAngle,r:a}},r)}return o}function hv(e,t,r,i,n){if(e){if(e.type==="polar")return Th(e,t,r);if(e.type==="cartesian2d")return xh(e,t,r,i,n)}else return null;return null}function Yo(e,t){return e.type===t}function Js(e,t){if(e.length===t.length){for(var r=0;r<e.length;r++)if(e[r]!==t[r])return;return!0}}function Qs(e){for(var t=1/0,r=1/0,i=-1/0,n=-1/0,a=0;a<e.length;){var o=e[a++],s=e[a++];isNaN(o)||(t=Math.min(o,t),i=Math.max(o,i)),isNaN(s)||(r=Math.min(s,r),n=Math.max(s,n))}return[[t,r],[i,n]]}function el(e,t){var r=Qs(e),i=r[0],n=r[1],a=Qs(t),o=a[0],s=a[1];return Math.max(Math.abs(i[0]-o[0]),Math.abs(i[1]-o[1]),Math.abs(n[0]-s[0]),Math.abs(n[1]-s[1]))}function tl(e){return ci(e)?e:e?.5:0}function fv(e,t,r){if(!r.valueDim)return[];for(var i=t.count(),n=ai(i*2),a=0;a<i;a++){var o=_h(r,e,t,a);n[a*2]=o[0],n[a*2+1]=o[1]}return n}function sr(e,t,r,i,n){var a=r.getBaseAxis(),o=a.dim==="x"||a.dim==="radius"?0:1,s=[],l=0,u=[],h=[],f=[],d=[];if(n){for(l=0;l<e.length;l+=2){var c=t||e;!isNaN(c[l])&&!isNaN(c[l+1])&&d.push(e[l],e[l+1])}e=d}for(l=0;l<e.length-2;l+=2)switch(f[0]=e[l+2],f[1]=e[l+3],h[0]=e[l],h[1]=e[l+1],s.push(h[0],h[1]),i){case"end":u[o]=f[o],u[1-o]=h[1-o],s.push(u[0],u[1]);break;case"middle":var v=(h[o]+f[o])/2,p=[];u[o]=p[o]=v,u[1-o]=h[1-o],p[1-o]=f[1-o],s.push(u[0],u[1]),s.push(p[0],p[1]);break;default:u[o]=h[o],u[1-o]=f[1-o],s.push(u[0],u[1])}return s.push(e[l++],e[l++]),s}function cv(e,t){var r=[],i=e.length,n,a;function o(h,f,d){var c=h.coord,v=(d-c)/(f.coord-c),p=xc(v,[h.color,f.color]);return{coord:d,color:p}}for(var s=0;s<i;s++){var l=e[s],u=l.coord;if(u<0)n=l;else if(u>t){a?r.push(o(a,l,t)):n&&r.push(o(n,l,0),o(n,l,t));break}else n&&(r.push(o(n,l,0)),n=null),r.push(l),a=l}return r}function dv(e,t,r){var i=e.getVisual("visualMeta");if(!(!i||!i.length||!e.count())&&t.type==="cartesian2d"){for(var n,a,o=i.length-1;o>=0;o--){var s=e.getDimensionInfo(i[o].dimension);if(n=s&&s.coordDim,n==="x"||n==="y"){a=i[o];break}}if(a){var l=t.getAxis(n),u=we(a.stops,function(y){return{coord:l.toGlobalCoord(l.dataToCoord(y.value)),color:y.color}}),h=u.length,f=a.outerColors.slice();h&&u[0].coord>u[h-1].coord&&(u.reverse(),f.reverse());var d=cv(u,n==="x"?r.getWidth():r.getHeight()),c=d.length;if(!c&&h)return u[0].coord<0?f[1]?f[1]:u[h-1].color:f[0]?f[0]:u[0].color;var v=10,p=d[0].coord-v,_=d[c-1].coord+v,m=_-p;if(m<.001)return"transparent";Y(d,function(y){y.offset=(y.coord-p)/m}),d.push({offset:c?d[c-1].offset:.5,color:f[1]||"transparent"}),d.unshift({offset:c?d[0].offset:.5,color:f[0]||"transparent"});var g=new yc(0,0,0,0,d,!0);return g[n]=p,g[n+"2"]=_,g}}}function vv(e,t,r){var i=e.get("showAllSymbol"),n=i==="auto";if(!(i&&!n)){var a=r.getAxesByScale("ordinal")[0];if(a&&!(n&&pv(a,t))){var o=t.mapDimension(a.dim),s={};return Y(a.getViewLabels(),function(l){var u=a.scale.getRawOrdinalNumber(l.tickValue);s[u]=1}),function(l){return!s.hasOwnProperty(t.get(o,l))}}}}function pv(e,t){var r=e.getExtent(),i=Math.abs(r[1]-r[0])/e.scale.count();isNaN(i)&&(i=0);for(var n=t.count(),a=Math.max(1,Math.round(n/5)),o=0;o<n;o+=a)if(qo.getSymbolSize(t,o)[e.isHorizontal()?1:0]*1.5>i)return!1;return!0}function gv(e,t){return isNaN(e)||isNaN(t)}function mv(e){for(var t=e.length/2;t>0&&gv(e[t*2-2],e[t*2-1]);t--);return t-1}function rl(e,t){return[e[t*2],e[t*2+1]]}function _v(e,t,r){for(var i=e.length/2,n=r==="x"?0:1,a,o,s=0,l=-1,u=0;u<i;u++)if(o=e[u*2+n],!(isNaN(o)||isNaN(e[u*2+1-n]))){if(u===0){a=o;continue}if(a<=t&&o>=t||a>=t&&o<=t){l=u;break}s=u,a=o}return{range:[s,l],t:(t-a)/(o-a)}}function wh(e){if(e.get(["endLabel","show"]))return!0;for(var t=0;t<Es.length;t++)if(e.get([Es[t],"endLabel","show"]))return!0;return!1}function Da(e,t,r,i){if(Yo(t,"cartesian2d")){var n=i.getModel("endLabel"),a=n.get("valueAnimation"),o=i.getData(),s={lastFrameIndex:0},l=wh(i)?function(c,v){e._endLabelOnDuring(c,v,o,s,a,n,t)}:null,u=t.getBaseAxis().isHorizontal(),h=xh(t,r,i,function(){var c=e._endLabel;c&&r&&s.originalX!=null&&c.attr({x:s.originalX,y:s.originalY})},l);if(!i.get("clip",!0)){var f=h.shape,d=Math.max(f.width,f.height);u?(f.y-=d,f.height+=d*2):(f.x-=d,f.width+=d*2)}return l&&l(1,h),h}else return Th(t,r,i)}function yv(e,t){var r=t.getBaseAxis(),i=r.isHorizontal(),n=r.inverse,a=i?n?"right":"left":"center",o=i?"middle":n?"top":"bottom";return{normal:{align:e.get("align")||a,verticalAlign:e.get("verticalAlign")||o}}}var xv=function(e){me(t,e);function t(){return e!==null&&e.apply(this,arguments)||this}return t.prototype.init=function(){var r=new $t,i=new iv;this.group.add(i.group),this._symbolDraw=i,this._lineGroup=r,this._changePolyState=Yn(this._changePolyState,this)},t.prototype.render=function(r,i,n){var a=r.coordinateSystem,o=this.group,s=r.getData(),l=r.getModel("lineStyle"),u=r.getModel("areaStyle"),h=s.getLayout("points")||[],f=a.type==="polar",d=this._coordSys,c=this._symbolDraw,v=this._polyline,p=this._polygon,_=this._lineGroup,m=!i.ssr&&r.get("animation"),g=!u.isEmpty(),y=u.get("origin"),x=mh(a,s,y),w=g&&fv(a,s,x),T=r.get("showSymbol"),b=r.get("connectNulls"),A=T&&!f&&vv(r,s,a),C=this._data;C&&C.eachItemGraphicEl(function(ee,be){ee.__temp&&(o.remove(ee),C.setItemGraphicEl(be,null))}),T||c.remove(),o.add(_);var D=f?!1:r.get("step"),L;a&&a.getArea&&r.get("clip",!0)&&(L=a.getArea(),L.width!=null?(L.x-=.1,L.y-=.1,L.width+=.2,L.height+=.2):L.r0&&(L.r0-=.5,L.r+=.5)),this._clipShapeForSymbol=L;var M=dv(s,a,n)||s.getVisual("style")[s.getVisual("drawType")];if(!(v&&d.type===a.type&&D===this._step))T&&c.updateData(s,{isIgnore:A,clipShape:L,disableAnimation:!0,getSymbolPoint:function(ee){return[h[ee*2],h[ee*2+1]]}}),m&&this._initSymbolLabelAnimation(s,a,L),D&&(w&&(w=sr(w,h,a,D,b)),h=sr(h,null,a,D,b)),v=this._newPolyline(h),g?p=this._newPolygon(h,w):p&&(_.remove(p),p=this._polygon=null),f||this._initOrUpdateEndLabel(r,a,Ss(M)),_.setClipPath(Da(this,a,!0,r));else{g&&!p?p=this._newPolygon(h,w):p&&!g&&(_.remove(p),p=this._polygon=null),f||this._initOrUpdateEndLabel(r,a,Ss(M));var P=_.getClipPath();if(P){var N=Da(this,a,!1,r);Ct(P,{shape:N.shape},r)}else _.setClipPath(Da(this,a,!0,r));T&&c.updateData(s,{isIgnore:A,clipShape:L,disableAnimation:!0,getSymbolPoint:function(ee){return[h[ee*2],h[ee*2+1]]}}),(!Js(this._stackedOnPoints,w)||!Js(this._points,h))&&(m?this._doUpdateAnimation(s,w,a,n,D,y,b):(D&&(w&&(w=sr(w,h,a,D,b)),h=sr(h,null,a,D,b)),v.setShape({points:h}),p&&p.setShape({points:h,stackedOnPoints:w})))}var I=r.getModel("emphasis"),V=I.get("focus"),Z=I.get("blurScope"),B=I.get("disabled");if(v.useStyle(He(l.getLineStyle(),{fill:"none",stroke:M,lineJoin:"bevel"})),Yi(v,r,"lineStyle"),v.style.lineWidth>0&&r.get(["emphasis","lineStyle","width"])==="bolder"){var $=v.getState("emphasis").style;$.lineWidth=+v.style.lineWidth+1}_t(v).seriesIndex=r.seriesIndex,qi(v,V,Z,B);var q=tl(r.get("smooth")),j=r.get("smoothMonotone");if(v.setShape({smooth:q,smoothMonotone:j,connectNulls:b}),p){var Q=s.getCalculationInfo("stackedOnSeries"),ie=0;p.useStyle(He(u.getAreaStyle(),{fill:M,opacity:.7,lineJoin:"bevel",decal:s.getVisual("style").decal})),Q&&(ie=tl(Q.get("smooth"))),p.setShape({smooth:q,stackedOnSmooth:ie,smoothMonotone:j,connectNulls:b}),Yi(p,r,"areaStyle"),_t(p).seriesIndex=r.seriesIndex,qi(p,V,Z,B)}var ae=this._changePolyState;s.eachItemGraphicEl(function(ee){ee&&(ee.onHoverStateChange=ae)}),this._polyline.onHoverStateChange=ae,this._data=s,this._coordSys=a,this._stackedOnPoints=w,this._points=h,this._step=D,this._valueOrigin=y,r.get("triggerLineEvent")&&(this.packEventData(r,v),p&&this.packEventData(r,p))},t.prototype.packEventData=function(r,i){_t(i).eventData={componentType:"series",componentSubType:"line",componentIndex:r.componentIndex,seriesIndex:r.seriesIndex,seriesName:r.name,seriesType:"line"}},t.prototype.highlight=function(r,i,n,a){var o=r.getData(),s=bs(o,a);if(this._changePolyState("emphasis"),!(s instanceof Array)&&s!=null&&s>=0){var l=o.getLayout("points"),u=o.getItemGraphicEl(s);if(!u){var h=l[s*2],f=l[s*2+1];if(isNaN(h)||isNaN(f)||this._clipShapeForSymbol&&!this._clipShapeForSymbol.contain(h,f))return;var d=r.get("zlevel")||0,c=r.get("z")||0;u=new qo(o,s),u.x=h,u.y=f,u.setZ(d,c);var v=u.getSymbolPath().getTextContent();v&&(v.zlevel=d,v.z=c,v.z2=this._polyline.z2+1),u.__temp=!0,o.setItemGraphicEl(s,u),u.stopSymbolAnimation(!0),this.group.add(u)}u.highlight()}else it.prototype.highlight.call(this,r,i,n,a)},t.prototype.downplay=function(r,i,n,a){var o=r.getData(),s=bs(o,a);if(this._changePolyState("normal"),s!=null&&s>=0){var l=o.getItemGraphicEl(s);l&&(l.__temp?(o.setItemGraphicEl(s,null),this.group.remove(l)):l.downplay())}else it.prototype.downplay.call(this,r,i,n,a)},t.prototype._changePolyState=function(r){var i=this._polygon;As(this._polyline,r),i&&As(i,r)},t.prototype._newPolyline=function(r){var i=this._polyline;return i&&this._lineGroup.remove(i),i=new sv({shape:{points:r},segmentIgnoreThreshold:2,z2:10}),this._lineGroup.add(i),this._polyline=i,i},t.prototype._newPolygon=function(r,i){var n=this._polygon;return n&&this._lineGroup.remove(n),n=new uv({shape:{points:r,stackedOnPoints:i},segmentIgnoreThreshold:2}),this._lineGroup.add(n),this._polygon=n,n},t.prototype._initSymbolLabelAnimation=function(r,i,n){var a,o,s=i.getBaseAxis(),l=s.inverse;i.type==="cartesian2d"?(a=s.isHorizontal(),o=!1):i.type==="polar"&&(a=s.dim==="angle",o=!0);var u=r.hostModel,h=u.get("animationDuration");St(h)&&(h=h(null));var f=u.get("animationDelay")||0,d=St(f)?f(null):f;r.eachItemGraphicEl(function(c,v){var p=c;if(p){var _=[c.x,c.y],m=void 0,g=void 0,y=void 0;if(n)if(o){var x=n,w=i.pointToCoord(_);a?(m=x.startAngle,g=x.endAngle,y=-w[1]/180*Math.PI):(m=x.r0,g=x.r,y=w[0])}else{var T=n;a?(m=T.x,g=T.x+T.width,y=c.x):(m=T.y+T.height,g=T.y,y=c.y)}var b=g===m?0:(y-m)/(g-m);l&&(b=1-b);var A=St(f)?f(v):h*b+d,C=p.getSymbolPath(),D=C.getTextContent();p.attr({scaleX:0,scaleY:0}),p.animateTo({scaleX:1,scaleY:1},{duration:200,setToFinal:!0,delay:A}),D&&D.animateFrom({style:{opacity:0}},{duration:300,delay:A}),C.disableLabelAnimation=!0}})},t.prototype._initOrUpdateEndLabel=function(r,i,n){var a=r.getModel("endLabel");if(wh(r)){var o=r.getData(),s=this._polyline,l=o.getLayout("points");if(!l){s.removeTextContent(),this._endLabel=null;return}var u=this._endLabel;u||(u=this._endLabel=new gr({z2:200}),u.ignoreClip=!0,s.setTextContent(this._endLabel),s.disableLabelAnimation=!0);var h=mv(l);h>=0&&(fa(s,fn(r,"endLabel"),{inheritColor:n,labelFetcher:r,labelDataIndex:h,defaultText:function(f,d,c){return c!=null?gh(o,c):Zo(o,f)},enableTextSetter:!0},yv(a,i)),s.textConfig.position=null)}else this._endLabel&&(this._polyline.removeTextContent(),this._endLabel=null)},t.prototype._endLabelOnDuring=function(r,i,n,a,o,s,l){var u=this._endLabel,h=this._polyline;if(u){r<1&&a.originalX==null&&(a.originalX=u.x,a.originalY=u.y);var f=n.getLayout("points"),d=n.hostModel,c=d.get("connectNulls"),v=s.get("precision"),p=s.get("distance")||0,_=l.getBaseAxis(),m=_.isHorizontal(),g=_.inverse,y=i.shape,x=g?m?y.x:y.y+y.height:m?y.x+y.width:y.y,w=(m?p:0)*(g?-1:1),T=(m?0:-p)*(g?-1:1),b=m?"x":"y",A=_v(f,x,b),C=A.range,D=C[1]-C[0],L=void 0;if(D>=1){if(D>1&&!c){var M=rl(f,C[0]);u.attr({x:M[0]+w,y:M[1]+T}),o&&(L=d.getRawValue(C[0]))}else{var M=h.getPointOn(x,b);M&&u.attr({x:M[0]+w,y:M[1]+T});var P=d.getRawValue(C[0]),N=d.getRawValue(C[1]);o&&(L=_c(n,v,P,N,A.t))}a.lastFrameIndex=C[0]}else{var I=r===1||a.lastFrameIndex>0?C[0]:0,M=rl(f,I);o&&(L=d.getRawValue(I)),u.attr({x:M[0]+w,y:M[1]+T})}if(o){var V=Fo(u);typeof V.setLabelText=="function"&&V.setLabelText(L)}}},t.prototype._doUpdateAnimation=function(r,i,n,a,o,s,l){var u=this._polyline,h=this._polygon,f=r.hostModel,d=ov(this._data,r,this._stackedOnPoints,i,this._coordSys,n,this._valueOrigin),c=d.current,v=d.stackedOnCurrent,p=d.next,_=d.stackedOnNext;if(o&&(v=sr(d.stackedOnCurrent,d.current,n,o,l),c=sr(d.current,null,n,o,l),_=sr(d.stackedOnNext,d.next,n,o,l),p=sr(d.next,null,n,o,l)),el(c,p)>3e3||h&&el(v,_)>3e3){u.stopAnimation(),u.setShape({points:p}),h&&(h.stopAnimation(),h.setShape({points:p,stackedOnPoints:_}));return}u.shape.__points=d.current,u.shape.points=c;var m={shape:{points:p}};d.current!==c&&(m.shape.__points=d.next),u.stopAnimation(),pt(u,m,f),h&&(h.setShape({points:c,stackedOnPoints:v}),h.stopAnimation(),pt(h,{shape:{stackedOnPoints:_}},f),u.shape.points!==h.shape.points&&(h.shape.points=u.shape.points));for(var g=[],y=d.status,x=0;x<y.length;x++){var w=y[x].cmd;if(w==="="){var T=r.getItemGraphicEl(y[x].idx1);T&&g.push({el:T,ptIdx:x})}}u.animators&&u.animators.length&&u.animators[0].during(function(){h&&h.dirtyShape();for(var b=u.shape.__points,A=0;A<g.length;A++){var C=g[A].el,D=g[A].ptIdx*2;C.x=b[D],C.y=b[D+1],C.markRedraw()}})},t.prototype.remove=function(r){var i=this.group,n=this._data;this._lineGroup.removeAll(),this._symbolDraw.remove(!0),n&&n.eachItemGraphicEl(function(a,o){a.__temp&&(i.remove(a),n.setItemGraphicEl(o,null))}),this._polyline=this._polygon=this._coordSys=this._points=this._stackedOnPoints=this._endLabel=this._data=null},t.type="line",t}(it);function Tv(e,t){return{seriesType:e,plan:Tc(),reset:function(r){var i=r.getData(),n=r.coordinateSystem;if(r.pipelineContext,!!n){var a=we(n.dimensions,function(f){return i.mapDimension(f)}).slice(0,2),o=a.length,s=i.getCalculationInfo("stackResultDimension");ji(i,a[0])&&(a[0]=s),ji(i,a[1])&&(a[1]=s);var l=i.getStore(),u=i.getDimensionIndex(a[0]),h=i.getDimensionIndex(a[1]);return o&&{progress:function(f,d){for(var c=f.end-f.start,v=ai(c*o),p=[],_=[],m=f.start,g=0;m<f.end;m++){var y=void 0;if(o===1){var x=l.get(u,m);y=n.dataToPoint(x,null,_)}else p[0]=l.get(u,m),p[1]=l.get(h,m),y=n.dataToPoint(p,null,_);v[g++]=y[0],v[g++]=y[1]}d.setLayout("points",v)}}}}}}var wv={average:function(e){for(var t=0,r=0,i=0;i<e.length;i++)isNaN(e[i])||(t+=e[i],r++);return r===0?NaN:t/r},sum:function(e){for(var t=0,r=0;r<e.length;r++)t+=e[r]||0;return t},max:function(e){for(var t=-1/0,r=0;r<e.length;r++)e[r]>t&&(t=e[r]);return isFinite(t)?t:NaN},min:function(e){for(var t=1/0,r=0;r<e.length;r++)e[r]<t&&(t=e[r]);return isFinite(t)?t:NaN},nearest:function(e){return e[0]}},Sv=function(e){return Math.round(e.length/2)};function Sh(e){return{seriesType:e,reset:function(t,r,i){var n=t.getData(),a=t.get("sampling"),o=t.coordinateSystem,s=n.count();if(s>10&&o.type==="cartesian2d"&&a){var l=o.getBaseAxis(),u=o.getOtherAxis(l),h=l.getExtent(),f=i.getDevicePixelRatio(),d=Math.abs(h[1]-h[0])*(f||1),c=Math.round(s/d);if(isFinite(c)&&c>1){a==="lttb"?t.setData(n.lttbDownSample(n.mapDimension(u.dim),1/c)):a==="minmax"&&t.setData(n.minmaxDownSample(n.mapDimension(u.dim),1/c));var v=void 0;Uo(a)?v=wv[a]:St(a)&&(v=a),v&&t.setData(n.downSample(n.mapDimension(u.dim),1/c,v,Sv))}}}}}function bv(e){e.registerChartView(xv),e.registerSeriesModel(tv),e.registerLayout(Tv("line")),e.registerVisual({seriesType:"line",reset:function(t){var r=t.getData(),i=t.getModel("lineStyle").getLineStyle();i&&!i.stroke&&(i.stroke=r.getVisual("style").fill),r.setVisual("legendLineStyle",i)}}),e.registerProcessor(e.PRIORITY.PROCESSOR.STATISTIC,Sh("line"))}var mo=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.getInitialData=function(r,i){return ca(null,this,{useEncodeDefaulter:!0})},t.prototype.getMarkerPosition=function(r,i,n){var a=this.coordinateSystem;if(a&&a.clampData){var o=a.clampData(r),s=a.dataToPoint(o);if(n)Y(a.getAxes(),function(d,c){if(d.type==="category"&&i!=null){var v=d.getTicksCoords(),p=d.getTickModel().get("alignWithLabel"),_=o[c],m=i[c]==="x1"||i[c]==="y1";if(m&&!p&&(_+=1),v.length<2)return;if(v.length===2){s[c]=d.toGlobalCoord(d.getExtent()[m?1:0]);return}for(var g=void 0,y=void 0,x=1,w=0;w<v.length;w++){var T=v[w].coord,b=w===v.length-1?v[w-1].tickValue+x:v[w].tickValue;if(b===_){y=T;break}else if(b<_)g=T;else if(g!=null&&b>_){y=(T+g)/2;break}w===1&&(x=b-v[0].tickValue)}y==null&&(g?g&&(y=v[v.length-1].coord):y=v[0].coord),s[c]=d.toGlobalCoord(y)}});else{var l=this.getData(),u=l.getLayout("offset"),h=l.getLayout("size"),f=a.getBaseAxis().isHorizontal()?0:1;s[f]+=u+h/2}return s}return[NaN,NaN]},t.type="series.__base_bar__",t.defaultOption={z:2,coordinateSystem:"cartesian2d",legendHoverLink:!0,barMinHeight:0,barMinAngle:0,large:!1,largeThreshold:400,progressive:3e3,progressiveChunkMode:"mod"},t}(ft);ft.registerClass(mo);var Av=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.getInitialData=function(){return ca(null,this,{useEncodeDefaulter:!0,createInvertedIndices:!!this.get("realtimeSort",!0)||null})},t.prototype.getProgressive=function(){return this.get("large")?this.get("progressive"):!1},t.prototype.getProgressiveThreshold=function(){var r=this.get("progressiveThreshold"),i=this.get("largeThreshold");return i>r&&(r=i),r},t.prototype.brushSelector=function(r,i,n){return n.rect(i.getItemLayout(r))},t.type="series.bar",t.dependencies=["grid","polar"],t.defaultOption=wc(mo.defaultOption,{clip:!0,roundCap:!1,showBackground:!1,backgroundStyle:{color:"rgba(180, 180, 180, 0.2)",borderColor:null,borderWidth:0,borderType:"solid",borderRadius:0,shadowBlur:0,shadowColor:null,shadowOffsetX:0,shadowOffsetY:0,opacity:1},select:{itemStyle:{borderColor:"#212121"}},realtimeSort:!1}),t}(mo),Ev=function(){function e(){this.cx=0,this.cy=0,this.r0=0,this.r=0,this.startAngle=0,this.endAngle=Math.PI*2,this.clockwise=!0}return e}(),il=function(e){me(t,e);function t(r){var i=e.call(this,r)||this;return i.type="sausage",i}return t.prototype.getDefaultShape=function(){return new Ev},t.prototype.buildPath=function(r,i){var n=i.cx,a=i.cy,o=Math.max(i.r0||0,0),s=Math.max(i.r,0),l=(s-o)*.5,u=o+l,h=i.startAngle,f=i.endAngle,d=i.clockwise,c=Math.PI*2,v=d?f-h<c:h-f<c;v||(h=f-(d?c:-c));var p=Math.cos(h),_=Math.sin(h),m=Math.cos(f),g=Math.sin(f);v?(r.moveTo(p*o+n,_*o+a),r.arc(p*u+n,_*u+a,l,-Math.PI+h,h,!d)):r.moveTo(p*s+n,_*s+a),r.arc(n,a,s,h,f,!d),r.arc(m*u+n,g*u+a,l,f-Math.PI*2,f-Math.PI,!d),o!==0&&r.arc(n,a,o,f,h,d)},t}(cn);function Lv(e,t){t=t||{};var r=t.isRoundCap;return function(i,n,a){var o=n.position;if(!o||o instanceof Array)return Ls(i,n,a);var s=e(o),l=n.distance!=null?n.distance:5,u=this.shape,h=u.cx,f=u.cy,d=u.r,c=u.r0,v=(d+c)/2,p=u.startAngle,_=u.endAngle,m=(p+_)/2,g=r?Math.abs(d-c)/2:0,y=Math.cos,x=Math.sin,w=h+d*y(p),T=f+d*x(p),b="left",A="top";switch(s){case"startArc":w=h+(c-l)*y(m),T=f+(c-l)*x(m),b="center",A="top";break;case"insideStartArc":w=h+(c+l)*y(m),T=f+(c+l)*x(m),b="center",A="bottom";break;case"startAngle":w=h+v*y(p)+An(p,l+g,!1),T=f+v*x(p)+En(p,l+g,!1),b="right",A="middle";break;case"insideStartAngle":w=h+v*y(p)+An(p,-l+g,!1),T=f+v*x(p)+En(p,-l+g,!1),b="left",A="middle";break;case"middle":w=h+v*y(m),T=f+v*x(m),b="center",A="middle";break;case"endArc":w=h+(d+l)*y(m),T=f+(d+l)*x(m),b="center",A="bottom";break;case"insideEndArc":w=h+(d-l)*y(m),T=f+(d-l)*x(m),b="center",A="top";break;case"endAngle":w=h+v*y(_)+An(_,l+g,!0),T=f+v*x(_)+En(_,l+g,!0),b="left",A="middle";break;case"insideEndAngle":w=h+v*y(_)+An(_,-l+g,!0),T=f+v*x(_)+En(_,-l+g,!0),b="right",A="middle";break;default:return Ls(i,n,a)}return i=i||{},i.x=w,i.y=T,i.align=b,i.verticalAlign=A,i}}function Cv(e,t,r,i){if(ci(i)){e.setTextConfig({rotation:i});return}else if(Be(t)){e.setTextConfig({rotation:0});return}var n=e.shape,a=n.clockwise?n.startAngle:n.endAngle,o=n.clockwise?n.endAngle:n.startAngle,s=(a+o)/2,l,u=r(t);switch(u){case"startArc":case"insideStartArc":case"middle":case"insideEndArc":case"endArc":l=s;break;case"startAngle":case"insideStartAngle":l=a;break;case"endAngle":case"insideEndAngle":l=o;break;default:e.setTextConfig({rotation:0});return}var h=Math.PI*1.5-l;u==="middle"&&h>Math.PI/2&&h<Math.PI*1.5&&(h-=Math.PI),e.setTextConfig({rotation:h})}function An(e,t,r){return t*Math.sin(e)*(r?-1:1)}function En(e,t,r){return t*Math.cos(e)*(r?1:-1)}var Pa=Math.max,Na=Math.min;function Mv(e,t){var r=e.getArea&&e.getArea();if(Yo(e,"cartesian2d")){var i=e.getBaseAxis();if(i.type!=="category"||!i.onBand){var n=t.getLayout("bandWidth");i.isHorizontal()?(r.x-=n,r.width+=n*2):(r.y-=n,r.height+=n*2)}}return r}var Dv=function(e){me(t,e);function t(){var r=e.call(this)||this;return r.type=t.type,r._isFirstFrame=!0,r}return t.prototype.render=function(r,i,n,a){this._model=r,this._removeOnRenderedListener(n),this._updateDrawMode(r);var o=r.get("coordinateSystem");(o==="cartesian2d"||o==="polar")&&(this._progressiveEls=null,this._isLargeDraw?this._renderLarge(r,i,n):this._renderNormal(r,i,n,a))},t.prototype.incrementalPrepareRender=function(r){this._clear(),this._updateDrawMode(r),this._updateLargeClip(r)},t.prototype.incrementalRender=function(r,i){this._progressiveEls=[],this._incrementalRenderLarge(r,i)},t.prototype.eachRendered=function(r){ju(this._progressiveEls||this.group,r)},t.prototype._updateDrawMode=function(r){var i=r.pipelineContext.large;(this._isLargeDraw==null||i!==this._isLargeDraw)&&(this._isLargeDraw=i,this._clear())},t.prototype._renderNormal=function(r,i,n,a){var o=this.group,s=r.getData(),l=this._data,u=r.coordinateSystem,h=u.getBaseAxis(),f;u.type==="cartesian2d"?f=h.isHorizontal():u.type==="polar"&&(f=h.dim==="angle");var d=r.isAnimationEnabled()?r:null,c=Pv(r,u);c&&this._enableRealtimeSort(c,s,n);var v=r.get("clip",!0)||c,p=Mv(u,s);o.removeClipPath();var _=r.get("roundCap",!0),m=r.get("showBackground",!0),g=r.getModel("backgroundStyle"),y=g.get("borderRadius")||0,x=[],w=this._backgroundEls,T=a&&a.isInitSort,b=a&&a.type==="changeAxisOrder";function A(L){var M=Ln[u.type](s,L),P=Gv(u,f,M);return P.useStyle(g.getItemStyle()),u.type==="cartesian2d"?P.setShape("r",y):P.setShape("cornerRadius",y),x[L]=P,P}s.diff(l).add(function(L){var M=s.getItemModel(L),P=Ln[u.type](s,L,M);if(m&&A(L),!(!s.hasValue(L)||!ll[u.type](P))){var N=!1;v&&(N=nl[u.type](p,P));var I=al[u.type](r,s,L,P,f,d,h.model,!1,_);c&&(I.forceLabelAnimation=!0),ul(I,s,L,M,P,r,f,u.type==="polar"),T?I.attr({shape:P}):c?ol(c,d,I,P,L,f,!1,!1):Ct(I,{shape:P},r,L),s.setItemGraphicEl(L,I),o.add(I),I.ignore=N}}).update(function(L,M){var P=s.getItemModel(L),N=Ln[u.type](s,L,P);if(m){var I=void 0;w.length===0?I=A(M):(I=w[M],I.useStyle(g.getItemStyle()),u.type==="cartesian2d"?I.setShape("r",y):I.setShape("cornerRadius",y),x[L]=I);var V=Ln[u.type](s,L),Z=Ah(f,V,u);pt(I,{shape:Z},d,L)}var B=l.getItemGraphicEl(M);if(!s.hasValue(L)||!ll[u.type](N)){o.remove(B);return}var $=!1;if(v&&($=nl[u.type](p,N),$&&o.remove(B)),B?qn(B):B=al[u.type](r,s,L,N,f,d,h.model,!!B,_),c&&(B.forceLabelAnimation=!0),b){var q=B.getTextContent();if(q){var j=Fo(q);j.prevValue!=null&&(j.prevValue=j.value)}}else ul(B,s,L,P,N,r,f,u.type==="polar");T?B.attr({shape:N}):c?ol(c,d,B,N,L,f,!0,b):pt(B,{shape:N},r,L,null),s.setItemGraphicEl(L,B),B.ignore=$,o.add(B)}).remove(function(L){var M=l.getItemGraphicEl(L);M&&Cs(M,r,L)}).execute();var C=this._backgroundGroup||(this._backgroundGroup=new $t);C.removeAll();for(var D=0;D<x.length;++D)C.add(x[D]);o.add(C),this._backgroundEls=x,this._data=s},t.prototype._renderLarge=function(r,i,n){this._clear(),fl(r,this.group),this._updateLargeClip(r)},t.prototype._incrementalRenderLarge=function(r,i){this._removeBackground(),fl(i,this.group,this._progressiveEls,!0)},t.prototype._updateLargeClip=function(r){var i=r.get("clip",!0)&&hv(r.coordinateSystem,!1,r),n=this.group;i?n.setClipPath(i):n.removeClipPath()},t.prototype._enableRealtimeSort=function(r,i,n){var a=this;if(i.count()){var o=r.baseAxis;if(this._isFirstFrame)this._dispatchInitSort(i,r,n),this._isFirstFrame=!1;else{var s=function(l){var u=i.getItemGraphicEl(l),h=u&&u.shape;return h&&Math.abs(o.isHorizontal()?h.height:h.width)||0};this._onRendered=function(){a._updateSortWithinSameData(i,s,o,n)},n.getZr().on("rendered",this._onRendered)}}},t.prototype._dataSort=function(r,i,n){var a=[];return r.each(r.mapDimension(i.dim),function(o,s){var l=n(s);l=l??NaN,a.push({dataIndex:s,mappedValue:l,ordinalNumber:o})}),a.sort(function(o,s){return s.mappedValue-o.mappedValue}),{ordinalNumbers:we(a,function(o){return o.ordinalNumber})}},t.prototype._isOrderChangedWithinSameData=function(r,i,n){for(var a=n.scale,o=r.mapDimension(n.dim),s=Number.MAX_VALUE,l=0,u=a.getOrdinalMeta().categories.length;l<u;++l){var h=r.rawIndexOf(o,a.getRawOrdinalNumber(l)),f=h<0?Number.MIN_VALUE:i(r.indexOfRawIndex(h));if(f>s)return!0;s=f}return!1},t.prototype._isOrderDifferentInView=function(r,i){for(var n=i.scale,a=n.getExtent(),o=Math.max(0,a[0]),s=Math.min(a[1],n.getOrdinalMeta().categories.length-1);o<=s;++o)if(r.ordinalNumbers[o]!==n.getRawOrdinalNumber(o))return!0},t.prototype._updateSortWithinSameData=function(r,i,n,a){if(this._isOrderChangedWithinSameData(r,i,n)){var o=this._dataSort(r,n,i);this._isOrderDifferentInView(o,n)&&(this._removeOnRenderedListener(a),a.dispatchAction({type:"changeAxisOrder",componentType:n.dim+"Axis",axisId:n.index,sortInfo:o}))}},t.prototype._dispatchInitSort=function(r,i,n){var a=i.baseAxis,o=this._dataSort(r,a,function(s){return r.get(r.mapDimension(i.otherAxis.dim),s)});n.dispatchAction({type:"changeAxisOrder",componentType:a.dim+"Axis",isInitSort:!0,axisId:a.index,sortInfo:o})},t.prototype.remove=function(r,i){this._clear(this._model),this._removeOnRenderedListener(i)},t.prototype.dispose=function(r,i){this._removeOnRenderedListener(i)},t.prototype._removeOnRenderedListener=function(r){this._onRendered&&(r.getZr().off("rendered",this._onRendered),this._onRendered=null)},t.prototype._clear=function(r){var i=this.group,n=this._data;r&&r.isAnimationEnabled()&&n&&!this._isLargeDraw?(this._removeBackground(),this._backgroundEls=[],n.eachItemGraphicEl(function(a){Cs(a,r,_t(a).dataIndex)})):i.removeAll(),this._data=null,this._isFirstFrame=!0},t.prototype._removeBackground=function(){this.group.remove(this._backgroundGroup),this._backgroundGroup=null},t.type="bar",t}(it),nl={cartesian2d:function(e,t){var r=t.width<0?-1:1,i=t.height<0?-1:1;r<0&&(t.x+=t.width,t.width=-t.width),i<0&&(t.y+=t.height,t.height=-t.height);var n=e.x+e.width,a=e.y+e.height,o=Pa(t.x,e.x),s=Na(t.x+t.width,n),l=Pa(t.y,e.y),u=Na(t.y+t.height,a),h=s<o,f=u<l;return t.x=h&&o>n?s:o,t.y=f&&l>a?u:l,t.width=h?0:s-o,t.height=f?0:u-l,r<0&&(t.x+=t.width,t.width=-t.width),i<0&&(t.y+=t.height,t.height=-t.height),h||f},polar:function(e,t){var r=t.r0<=t.r?1:-1;if(r<0){var i=t.r;t.r=t.r0,t.r0=i}var n=Na(t.r,e.r),a=Pa(t.r0,e.r0);t.r=n,t.r0=a;var o=n-a<0;if(r<0){var i=t.r;t.r=t.r0,t.r0=i}return o}},al={cartesian2d:function(e,t,r,i,n,a,o,s,l){var u=new Xr({shape:lt({},i),z2:1});if(u.__dataIndex=r,u.name="item",a){var h=u.shape,f=n?"height":"width";h[f]=0}return u},polar:function(e,t,r,i,n,a,o,s,l){var u=!n&&l?il:zo,h=new u({shape:i,z2:1});h.name="item";var f=bh(n);if(h.calculateTextPosition=Lv(f,{isRoundCap:u===il}),a){var d=h.shape,c=n?"r":"endAngle",v={};d[c]=n?i.r0:i.startAngle,v[c]=i[c],(s?pt:Ct)(h,{shape:v},a)}return h}};function Pv(e,t){var r=e.get("realtimeSort",!0),i=t.getBaseAxis();if(r&&i.type==="category"&&t.type==="cartesian2d")return{baseAxis:i,otherAxis:t.getOtherAxis(i)}}function ol(e,t,r,i,n,a,o,s){var l,u;a?(u={x:i.x,width:i.width},l={y:i.y,height:i.height}):(u={y:i.y,height:i.height},l={x:i.x,width:i.width}),s||(o?pt:Ct)(r,{shape:l},t,n,null);var h=t?e.baseAxis.model:null;(o?pt:Ct)(r,{shape:u},h,n)}function sl(e,t){for(var r=0;r<t.length;r++)if(!isFinite(e[t[r]]))return!0;return!1}var Nv=["x","y","width","height"],Iv=["cx","cy","r","startAngle","endAngle"],ll={cartesian2d:function(e){return!sl(e,Nv)},polar:function(e){return!sl(e,Iv)}},Ln={cartesian2d:function(e,t,r){var i=e.getItemLayout(t),n=r?Ov(r,i):0,a=i.width>0?1:-1,o=i.height>0?1:-1;return{x:i.x+a*n/2,y:i.y+o*n/2,width:i.width-a*n,height:i.height-o*n}},polar:function(e,t,r){var i=e.getItemLayout(t);return{cx:i.cx,cy:i.cy,r0:i.r0,r:i.r,startAngle:i.startAngle,endAngle:i.endAngle,clockwise:i.clockwise}}};function Rv(e){return e.startAngle!=null&&e.endAngle!=null&&e.startAngle===e.endAngle}function bh(e){return function(t){var r=t?"Arc":"Angle";return function(i){switch(i){case"start":case"insideStart":case"end":case"insideEnd":return i+r;default:return i}}}(e)}function ul(e,t,r,i,n,a,o,s){var l=t.getItemVisual(r,"style");if(s){if(!a.get("roundCap")){var h=e.shape,f=Sc(i.getModel("itemStyle"),h,!0);lt(h,f),e.setShape(h)}}else{var u=i.get(["itemStyle","borderRadius"])||0;e.setShape("r",u)}e.useStyle(l);var d=i.getShallow("cursor");d&&e.attr("cursor",d);var c=s?o?n.r>=n.r0?"endArc":"startArc":n.endAngle>=n.startAngle?"endAngle":"startAngle":o?n.height>=0?"bottom":"top":n.width>=0?"right":"left",v=fn(i);fa(e,v,{labelFetcher:a,labelDataIndex:r,defaultText:Zo(a.getData(),r),inheritColor:l.fill,defaultOpacity:l.opacity,defaultOutsidePosition:c});var p=e.getTextContent();if(s&&p){var _=i.get(["label","position"]);e.textConfig.inside=_==="middle"?!0:null,Cv(e,_==="outside"?c:_,bh(o),i.get(["label","rotate"]))}bc(p,v,a.getRawValue(r),function(g){return gh(t,g)});var m=i.getModel(["emphasis"]);qi(e,m.get("focus"),m.get("blurScope"),m.get("disabled")),Yi(e,i),Rv(n)&&(e.style.fill="none",e.style.stroke="none",Y(e.states,function(g){g.style&&(g.style.fill=g.style.stroke="none")}))}function Ov(e,t){var r=e.get(["itemStyle","borderColor"]);if(!r||r==="none")return 0;var i=e.get(["itemStyle","borderWidth"])||0,n=isNaN(t.width)?Number.MAX_VALUE:Math.abs(t.width),a=isNaN(t.height)?Number.MAX_VALUE:Math.abs(t.height);return Math.min(i,n,a)}var Bv=function(){function e(){}return e}(),hl=function(e){me(t,e);function t(r){var i=e.call(this,r)||this;return i.type="largeBar",i}return t.prototype.getDefaultShape=function(){return new Bv},t.prototype.buildPath=function(r,i){for(var n=i.points,a=this.baseDimIdx,o=1-this.baseDimIdx,s=[],l=[],u=this.barWidth,h=0;h<n.length;h+=3)l[a]=u,l[o]=n[h+2],s[a]=n[h+a],s[o]=n[h+o],r.rect(s[0],s[1],l[0],l[1])},t}(cn);function fl(e,t,r,i){var n=e.getData(),a=n.getLayout("valueAxisHorizontal")?1:0,o=n.getLayout("largeDataIndices"),s=n.getLayout("size"),l=e.getModel("backgroundStyle"),u=n.getLayout("largeBackgroundPoints");if(u){var h=new hl({shape:{points:u},incremental:!!i,silent:!0,z2:0});h.baseDimIdx=a,h.largeDataIndices=o,h.barWidth=s,h.useStyle(l.getItemStyle()),t.add(h),r&&r.push(h)}var f=new hl({shape:{points:n.getLayout("largePoints")},incremental:!!i,ignoreCoarsePointer:!0,z2:1});f.baseDimIdx=a,f.largeDataIndices=o,f.barWidth=s,t.add(f),f.useStyle(n.getVisual("style")),f.style.stroke=null,_t(f).seriesIndex=e.seriesIndex,e.get("silent")||(f.on("mousedown",cl),f.on("mousemove",cl)),r&&r.push(f)}var cl=Ac(function(e){var t=this,r=Fv(t,e.offsetX,e.offsetY);_t(t).dataIndex=r>=0?r:null},30,!1);function Fv(e,t,r){for(var i=e.baseDimIdx,n=1-i,a=e.shape.points,o=e.largeDataIndices,s=[],l=[],u=e.barWidth,h=0,f=a.length/3;h<f;h++){var d=h*3;if(l[i]=u,l[n]=a[d+2],s[i]=a[d+i],s[n]=a[d+n],l[n]<0&&(s[n]+=l[n],l[n]=-l[n]),t>=s[0]&&t<=s[0]+l[0]&&r>=s[1]&&r<=s[1]+l[1])return o[h]}return-1}function Ah(e,t,r){if(Yo(r,"cartesian2d")){var i=t,n=r.getArea();return{x:e?i.x:n.x,y:e?n.y:i.y,width:e?i.width:n.width,height:e?n.height:i.height}}else{var n=r.getArea(),a=t;return{cx:n.cx,cy:n.cy,r0:e?n.r0:a.r0,r:e?n.r:a.r,startAngle:e?a.startAngle:0,endAngle:e?a.endAngle:Math.PI*2}}}function Gv(e,t,r){var i=e.type==="polar"?zo:Xr;return new i({shape:Ah(t,r,e),silent:!0,z2:0})}function zv(e){e.registerChartView(Dv),e.registerSeriesModel(Av),e.registerLayout(e.PRIORITY.VISUAL.LAYOUT,ui(Ec,"bar")),e.registerLayout(e.PRIORITY.VISUAL.PROGRESSIVE_LAYOUT,Lc("bar")),e.registerProcessor(e.PRIORITY.PROCESSOR.STATISTIC,Sh("bar")),e.registerAction({type:"changeAxisOrder",event:"changeAxisOrder",update:"update"},function(t,r){var i=t.componentType||"series";r.eachComponent({mainType:i,query:t},function(n){t.sortInfo&&n.axis.setCategorySortInfo(t.sortInfo)})})}var Uv=function(e){me(t,e);function t(){return e!==null&&e.apply(this,arguments)||this}return t.type="grid",t.dependencies=["xAxis","yAxis"],t.layoutMode="box",t.defaultOption={show:!1,z:0,left:"10%",top:60,right:"10%",bottom:70,containLabel:!1,backgroundColor:"rgba(0,0,0,0)",borderWidth:1,borderColor:"#ccc"},t}(Rt),_o=function(e){me(t,e);function t(){return e!==null&&e.apply(this,arguments)||this}return t.prototype.getCoordSysModel=function(){return this.getReferringComponents("grid",Nr).models[0]},t.type="cartesian2dAxis",t}(Rt);un(_o,Wo);var Eh={show:!0,z:0,inverse:!1,name:"",nameLocation:"end",nameRotate:null,nameTruncate:{maxWidth:null,ellipsis:"...",placeholder:"."},nameTextStyle:{},nameGap:15,silent:!1,triggerEvent:!1,tooltip:{show:!1},axisPointer:{},axisLine:{show:!0,onZero:!0,onZeroAxisIndex:null,lineStyle:{color:"#6E7079",width:1,type:"solid"},symbol:["none","none"],symbolSize:[10,15]},axisTick:{show:!0,inside:!1,length:5,lineStyle:{width:1}},axisLabel:{show:!0,inside:!1,rotate:0,showMinLabel:null,showMaxLabel:null,margin:8,fontSize:12},splitLine:{show:!0,showMinLine:!0,showMaxLine:!0,lineStyle:{color:["#E0E6F1"],width:1,type:"solid"}},splitArea:{show:!1,areaStyle:{color:["rgba(250,250,250,0.2)","rgba(210,219,238,0.2)"]}}},Vv=le({boundaryGap:!0,deduplication:null,splitLine:{show:!1},axisTick:{alignWithLabel:!1,interval:"auto"},axisLabel:{interval:"auto"}},Eh),$o=le({boundaryGap:[0,0],axisLine:{show:"auto"},axisTick:{show:"auto"},splitNumber:5,minorTick:{show:!1,splitNumber:5,length:3,lineStyle:{}},minorSplitLine:{show:!1,lineStyle:{color:"#F4F7FD",width:1}}},Eh),Hv=le({splitNumber:6,axisLabel:{showMinLabel:!1,showMaxLabel:!1,rich:{primary:{fontWeight:"bold"}}},splitLine:{show:!1}},$o),kv=He({logBase:10},$o);const Lh={category:Vv,value:$o,time:Hv,log:kv};var Wv={value:1,category:1,time:1,log:1};function dl(e,t,r,i){Y(Wv,function(n,a){var o=le(le({},Lh[a],!0),i,!0),s=function(l){me(u,l);function u(){var h=l!==null&&l.apply(this,arguments)||this;return h.type=t+"Axis."+a,h}return u.prototype.mergeDefaultAndTheme=function(h,f){var d=Cc(this),c=d?Mc(h):{},v=f.getTheme();le(h,v.get(a+"Axis")),le(h,this.getDefaultOption()),h.type=vl(h),d&&Zu(h,c,d)},u.prototype.optionUpdated=function(){var h=this.option;h.type==="category"&&(this.__ordinalMeta=qu.createByAxisModel(this))},u.prototype.getCategories=function(h){var f=this.option;if(f.type==="category")return h?f.data:this.__ordinalMeta.categories},u.prototype.getOrdinalMeta=function(){return this.__ordinalMeta},u.type=t+"Axis."+a,u.defaultOption=o,u}(r);e.registerComponentModel(s)}),e.registerSubTypeDefaulter(t+"Axis",vl)}function vl(e){return e.type||(e.data?"category":"value")}var Ko=function(){function e(t){this.type="cartesian",this._dimList=[],this._axes={},this.name=t||""}return e.prototype.getAxis=function(t){return this._axes[t]},e.prototype.getAxes=function(){return we(this._dimList,function(t){return this._axes[t]},this)},e.prototype.getAxesByScale=function(t){return t=t.toLowerCase(),Zt(this.getAxes(),function(r){return r.scale.type===t})},e.prototype.addAxis=function(t){var r=t.dim;this._axes[r]=t,this._dimList.push(r)},e}(),yo=["x","y"];function pl(e){return e.type==="interval"||e.type==="time"}var Xv=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type="cartesian2d",r.dimensions=yo,r}return t.prototype.calcAffineTransform=function(){this._transform=this._invTransform=null;var r=this.getAxis("x").scale,i=this.getAxis("y").scale;if(!(!pl(r)||!pl(i))){var n=r.getExtent(),a=i.getExtent(),o=this.dataToPoint([n[0],a[0]]),s=this.dataToPoint([n[1],a[1]]),l=n[1]-n[0],u=a[1]-a[0];if(!(!l||!u)){var h=(s[0]-o[0])/l,f=(s[1]-o[1])/u,d=o[0]-n[0]*h,c=o[1]-a[0]*f,v=this._transform=[h,0,0,f,d,c];this._invTransform=Bo([],v)}}},t.prototype.getBaseAxis=function(){return this.getAxesByScale("ordinal")[0]||this.getAxesByScale("time")[0]||this.getAxis("x")},t.prototype.containPoint=function(r){var i=this.getAxis("x"),n=this.getAxis("y");return i.contain(i.toLocalCoord(r[0]))&&n.contain(n.toLocalCoord(r[1]))},t.prototype.containData=function(r){return this.getAxis("x").containData(r[0])&&this.getAxis("y").containData(r[1])},t.prototype.containZone=function(r,i){var n=this.dataToPoint(r),a=this.dataToPoint(i),o=this.getArea(),s=new Ur(n[0],n[1],a[0]-n[0],a[1]-n[1]);return o.intersect(s)},t.prototype.dataToPoint=function(r,i,n){n=n||[];var a=r[0],o=r[1];if(this._transform&&a!=null&&isFinite(a)&&o!=null&&isFinite(o))return fi(n,r,this._transform);var s=this.getAxis("x"),l=this.getAxis("y");return n[0]=s.toGlobalCoord(s.dataToCoord(a,i)),n[1]=l.toGlobalCoord(l.dataToCoord(o,i)),n},t.prototype.clampData=function(r,i){var n=this.getAxis("x").scale,a=this.getAxis("y").scale,o=n.getExtent(),s=a.getExtent(),l=n.parse(r[0]),u=a.parse(r[1]);return i=i||[],i[0]=Math.min(Math.max(Math.min(o[0],o[1]),l),Math.max(o[0],o[1])),i[1]=Math.min(Math.max(Math.min(s[0],s[1]),u),Math.max(s[0],s[1])),i},t.prototype.pointToData=function(r,i){var n=[];if(this._invTransform)return fi(n,r,this._invTransform);var a=this.getAxis("x"),o=this.getAxis("y");return n[0]=a.coordToData(a.toLocalCoord(r[0]),i),n[1]=o.coordToData(o.toLocalCoord(r[1]),i),n},t.prototype.getOtherAxis=function(r){return this.getAxis(r.dim==="x"?"y":"x")},t.prototype.getArea=function(r){r=r||0;var i=this.getAxis("x").getGlobalExtent(),n=this.getAxis("y").getGlobalExtent(),a=Math.min(i[0],i[1])-r,o=Math.min(n[0],n[1])-r,s=Math.max(i[0],i[1])-a+r,l=Math.max(n[0],n[1])-o+r;return new Ur(a,o,s,l)},t}(Ko),jv=function(e){me(t,e);function t(r,i,n,a,o){var s=e.call(this,r,i,n)||this;return s.index=0,s.type=a||"value",s.position=o||"bottom",s}return t.prototype.isHorizontal=function(){var r=this.position;return r==="top"||r==="bottom"},t.prototype.getGlobalExtent=function(r){var i=this.getExtent();return i[0]=this.toGlobalCoord(i[0]),i[1]=this.toGlobalCoord(i[1]),r&&i[0]>i[1]&&i.reverse(),i},t.prototype.pointToData=function(r,i){return this.coordToData(this.toLocalCoord(r[this.dim==="x"?0:1]),i)},t.prototype.setCategorySortInfo=function(r){if(this.type!=="category")return!1;this.model.option.categorySortInfo=r,this.scale.setSortInfo(r)},t}(Si),Ia=Math.log;function Ch(e,t,r){var i=fo.prototype,n=i.getTicks.call(r),a=i.getTicks.call(r,!0),o=n.length-1,s=i.getInterval.call(r),l=Dc(e,t),u=l.extent,h=l.fixMin,f=l.fixMax;if(e.type==="log"){var d=Ia(e.base);u=[Ia(u[0])/d,Ia(u[1])/d]}e.setExtent(u[0],u[1]),e.calcNiceExtent({splitNumber:o,fixMin:h,fixMax:f});var c=i.getExtent.call(e);h&&(u[0]=c[0]),f&&(u[1]=c[1]);var v=i.getInterval.call(e),p=u[0],_=u[1];if(h&&f)v=(_-p)/o;else if(h)for(_=u[0]+v*o;_<u[1]&&isFinite(_)&&isFinite(u[1]);)v=wa(v),_=u[0]+v*o;else if(f)for(p=u[1]-v*o;p>u[0]&&isFinite(p)&&isFinite(u[0]);)v=wa(v),p=u[1]-v*o;else{var m=e.getTicks().length-1;m>o&&(v=wa(v));var g=v*o;_=Math.ceil(u[1]/v)*v,p=mt(_-g),p<0&&u[0]>=0?(p=0,_=mt(g)):_>0&&u[1]<=0&&(_=0,p=-mt(g))}var y=(n[0].value-a[0].value)/s,x=(n[o].value-a[o].value)/s;i.setExtent.call(e,p+v*y,_+v*x),i.setInterval.call(e,v),(y||x)&&i.setNiceExtent.call(e,p+v,_-v)}var Zv=function(){function e(t,r,i){this.type="grid",this._coordsMap={},this._coordsList=[],this._axesMap={},this._axesList=[],this.axisPointerEnabled=!0,this.dimensions=yo,this._initCartesian(t,r,i),this.model=t}return e.prototype.getRect=function(){return this._rect},e.prototype.update=function(t,r){var i=this._axesMap;this._updateScale(t,this.model);function n(o){var s,l=Jt(o),u=l.length;if(u){for(var h=[],f=u-1;f>=0;f--){var d=+l[f],c=o[d],v=c.model,p=c.scale;co(p)&&v.get("alignTicks")&&v.get("interval")==null?h.push(c):(ho(p,v),co(p)&&(s=c))}h.length&&(s||(s=h.pop(),ho(s.scale,s.model)),Y(h,function(_){Ch(_.scale,_.model,s.scale)}))}}n(i.x),n(i.y);var a={};Y(i.x,function(o){gl(i,"y",o,a)}),Y(i.y,function(o){gl(i,"x",o,a)}),this.resize(this.model,r)},e.prototype.resize=function(t,r,i){var n=t.getBoxLayoutParams(),a=!i&&t.get("containLabel"),o=dn(n,{width:r.getWidth(),height:r.getHeight()});this._rect=o;var s=this._axesList;l(),a&&(Y(s,function(u){if(!u.model.get(["axisLabel","inside"])){var h=Pc(u);if(h){var f=u.isHorizontal()?"height":"width",d=u.model.get(["axisLabel","margin"]);o[f]-=h[f]+d,u.position==="top"?o.y+=h.height+d:u.position==="left"&&(o.x+=h.width+d)}}}),l()),Y(this._coordsList,function(u){u.calcAffineTransform()});function l(){Y(s,function(u){var h=u.isHorizontal(),f=h?[0,o.width]:[0,o.height],d=u.inverse?1:0;u.setExtent(f[d],f[1-d]),qv(u,h?o.x:o.y)})}},e.prototype.getAxis=function(t,r){var i=this._axesMap[t];if(i!=null)return i[r||0]},e.prototype.getAxes=function(){return this._axesList.slice()},e.prototype.getCartesian=function(t,r){if(t!=null&&r!=null){var i="x"+t+"y"+r;return this._coordsMap[i]}Go(t)&&(r=t.yAxisIndex,t=t.xAxisIndex);for(var n=0,a=this._coordsList;n<a.length;n++)if(a[n].getAxis("x").index===t||a[n].getAxis("y").index===r)return a[n]},e.prototype.getCartesians=function(){return this._coordsList.slice()},e.prototype.convertToPixel=function(t,r,i){var n=this._findConvertTarget(r);return n.cartesian?n.cartesian.dataToPoint(i):n.axis?n.axis.toGlobalCoord(n.axis.dataToCoord(i)):null},e.prototype.convertFromPixel=function(t,r,i){var n=this._findConvertTarget(r);return n.cartesian?n.cartesian.pointToData(i):n.axis?n.axis.coordToData(n.axis.toLocalCoord(i)):null},e.prototype._findConvertTarget=function(t){var r=t.seriesModel,i=t.xAxisModel||r&&r.getReferringComponents("xAxis",Nr).models[0],n=t.yAxisModel||r&&r.getReferringComponents("yAxis",Nr).models[0],a=t.gridModel,o=this._coordsList,s,l;if(r)s=r.coordinateSystem,Ut(o,s)<0&&(s=null);else if(i&&n)s=this.getCartesian(i.componentIndex,n.componentIndex);else if(i)l=this.getAxis("x",i.componentIndex);else if(n)l=this.getAxis("y",n.componentIndex);else if(a){var u=a.coordinateSystem;u===this&&(s=this._coordsList[0])}return{cartesian:s,axis:l}},e.prototype.containPoint=function(t){var r=this._coordsList[0];if(r)return r.containPoint(t)},e.prototype._initCartesian=function(t,r,i){var n=this,a=this,o={left:!1,right:!1,top:!1,bottom:!1},s={x:{},y:{}},l={x:0,y:0};if(r.eachComponent("xAxis",u("x"),this),r.eachComponent("yAxis",u("y"),this),!l.x||!l.y){this._axesMap={},this._axesList=[];return}this._axesMap=s,Y(s.x,function(h,f){Y(s.y,function(d,c){var v="x"+f+"y"+c,p=new Xv(v);p.master=n,p.model=t,n._coordsMap[v]=p,n._coordsList.push(p),p.addAxis(h),p.addAxis(d)})});function u(h){return function(f,d){if(Ra(f,t)){var c=f.get("position");h==="x"?c!=="top"&&c!=="bottom"&&(c=o.bottom?"top":"bottom"):c!=="left"&&c!=="right"&&(c=o.left?"right":"left"),o[c]=!0;var v=new jv(h,Hu(f),[0,0],f.get("type"),c),p=v.type==="category";v.onBand=p&&f.get("boundaryGap"),v.inverse=f.get("inverse"),f.axis=v,v.model=f,v.grid=a,v.index=d,a._axesList.push(v),s[h][d]=v,l[h]++}}}},e.prototype._updateScale=function(t,r){Y(this._axesList,function(n){if(n.scale.setExtent(1/0,-1/0),n.type==="category"){var a=n.model.get("categorySortInfo");n.scale.setSortInfo(a)}}),t.eachSeries(function(n){if(Ms(n)){var a=Ds(n),o=a.xAxisModel,s=a.yAxisModel;if(!Ra(o,r)||!Ra(s,r))return;var l=this.getCartesian(o.componentIndex,s.componentIndex),u=n.getData(),h=l.getAxis("x"),f=l.getAxis("y");i(u,h),i(u,f)}},this);function i(n,a){Y(Nc(n,a.dim),function(o){a.scale.unionExtentFromData(n,o)})}},e.prototype.getTooltipAxes=function(t){var r=[],i=[];return Y(this.getCartesians(),function(n){var a=t!=null&&t!=="auto"?n.getAxis(t):n.getBaseAxis(),o=n.getOtherAxis(a);Ut(r,a)<0&&r.push(a),Ut(i,o)<0&&i.push(o)}),{baseAxes:r,otherAxes:i}},e.create=function(t,r){var i=[];return t.eachComponent("grid",function(n,a){var o=new e(n,t,r);o.name="grid_"+a,o.resize(n,r,!0),n.coordinateSystem=o,i.push(o)}),t.eachSeries(function(n){if(Ms(n)){var a=Ds(n),o=a.xAxisModel,s=a.yAxisModel,l=o.getCoordSysModel(),u=l.coordinateSystem;n.coordinateSystem=u.getCartesian(o.componentIndex,s.componentIndex)}}),i},e.dimensions=yo,e}();function Ra(e,t){return e.getCoordSysModel()===t}function gl(e,t,r,i){r.getAxesOnZeroOf=function(){return a?[a]:[]};var n=e[t],a,o=r.model,s=o.get(["axisLine","onZero"]),l=o.get(["axisLine","onZeroAxisIndex"]);if(!s)return;if(l!=null)ml(n[l])&&(a=n[l]);else for(var u in n)if(n.hasOwnProperty(u)&&ml(n[u])&&!i[h(n[u])]){a=n[u];break}a&&(i[h(a)]=!0);function h(f){return f.dim+"_"+f.index}}function ml(e){return e&&e.type!=="category"&&e.type!=="time"&&Ic(e)}function qv(e,t){var r=e.getExtent(),i=r[0]+r[1];e.toGlobalCoord=e.dim==="x"?function(n){return n+t}:function(n){return i-n+t},e.toLocalCoord=e.dim==="x"?function(n){return n-t}:function(n){return i-n+t}}var xo=Kt();function Yv(e,t,r,i){var n=r.axis;if(!n.scale.isBlank()){var a=r.getModel("splitArea"),o=a.getModel("areaStyle"),s=o.get("color"),l=i.coordinateSystem.getRect(),u=n.getTicksCoords({tickModel:a,clamp:!0});if(u.length){var h=s.length,f=xo(e).splitAreaColors,d=Yt(),c=0;if(f)for(var v=0;v<u.length;v++){var p=f.get(u[v].tickValue);if(p!=null){c=(p+(h-1)*v)%h;break}}var _=n.toGlobalCoord(u[0].coord),m=o.getAreaStyle();s=Be(s)?s:[s];for(var v=1;v<u.length;v++){var g=n.toGlobalCoord(u[v].coord),y=void 0,x=void 0,w=void 0,T=void 0;n.isHorizontal()?(y=_,x=l.y,w=g-y,T=l.height,_=y+w):(y=l.x,x=_,w=l.width,T=g-x,_=x+T);var b=u[v-1].tickValue;b!=null&&d.set(b,c),t.add(new Xr({anid:b!=null?"area_"+b:null,shape:{x:y,y:x,width:w,height:T},style:He({fill:s[c]},m),autoBatch:!0,silent:!0})),c=(c+1)%h}xo(e).splitAreaColors=d}}}function $v(e){xo(e).splitAreaColors=null}var Kv=["axisLine","axisTickLabel","axisName"],Jv=["splitArea","splitLine","minorSplitLine"],Mh=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r.axisPointerClass="CartesianAxisPointer",r}return t.prototype.render=function(r,i,n,a){this.group.removeAll();var o=this._axisGroup;if(this._axisGroup=new $t,this.group.add(this._axisGroup),!!r.get("show")){var s=r.getCoordSysModel(),l=Rc(s,r),u=new Yu(r,lt({handleAutoShown:function(f){for(var d=s.coordinateSystem.getCartesians(),c=0;c<d.length;c++)if(co(d[c].getOtherAxis(r.axis).scale))return!0;return!1}},l));Y(Kv,u.add,u),this._axisGroup.add(u.getGroup()),Y(Jv,function(f){r.get([f,"show"])&&Qv[f](this,this._axisGroup,r,s)},this);var h=a&&a.type==="changeAxisOrder"&&a.isInitSort;h||Oc(o,this._axisGroup,r),e.prototype.render.call(this,r,i,n,a)}},t.prototype.remove=function(){$v(this)},t.type="cartesianAxis",t}(Bc),Qv={splitLine:function(e,t,r,i){var n=r.axis;if(!n.scale.isBlank()){var a=r.getModel("splitLine"),o=a.getModel("lineStyle"),s=o.get("color"),l=a.get("showMinLine")!==!1,u=a.get("showMaxLine")!==!1;s=Be(s)?s:[s];for(var h=i.coordinateSystem.getRect(),f=n.isHorizontal(),d=0,c=n.getTicksCoords({tickModel:a}),v=[],p=[],_=o.getLineStyle(),m=0;m<c.length;m++){var g=n.toGlobalCoord(c[m].coord);if(!(m===0&&!l||m===c.length-1&&!u)){var y=c[m].tickValue;f?(v[0]=g,v[1]=h.y,p[0]=g,p[1]=h.y+h.height):(v[0]=h.x,v[1]=g,p[0]=h.x+h.width,p[1]=g);var x=d++%s.length,w=new Ps({anid:y!=null?"line_"+y:null,autoBatch:!0,shape:{x1:v[0],y1:v[1],x2:p[0],y2:p[1]},style:He({stroke:s[x]},_),silent:!0});Ns(w.shape,_.lineWidth),t.add(w)}}}},minorSplitLine:function(e,t,r,i){var n=r.axis,a=r.getModel("minorSplitLine"),o=a.getModel("lineStyle"),s=i.coordinateSystem.getRect(),l=n.isHorizontal(),u=n.getMinorTicksCoords();if(u.length)for(var h=[],f=[],d=o.getLineStyle(),c=0;c<u.length;c++)for(var v=0;v<u[c].length;v++){var p=n.toGlobalCoord(u[c][v].coord);l?(h[0]=p,h[1]=s.y,f[0]=p,f[1]=s.y+s.height):(h[0]=s.x,h[1]=p,f[0]=s.x+s.width,f[1]=p);var _=new Ps({anid:"minor_line_"+u[c][v].tickValue,autoBatch:!0,shape:{x1:h[0],y1:h[1],x2:f[0],y2:f[1]},style:d,silent:!0});Ns(_.shape,d.lineWidth),t.add(_)}},splitArea:function(e,t,r,i){Yv(e,t,r,i)}},Dh=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.type="xAxis",t}(Mh),ep=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=Dh.type,r}return t.type="yAxis",t}(Mh),tp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type="grid",r}return t.prototype.render=function(r,i){this.group.removeAll(),r.get("show")&&this.group.add(new Xr({shape:r.coordinateSystem.getRect(),style:He({fill:r.get("backgroundColor")},r.getItemStyle()),silent:!0,z2:-1}))},t.type="grid",t}(Qt),_l={offset:0};function rp(e){e.registerComponentView(tp),e.registerComponentModel(Uv),e.registerCoordinateSystem("cartesian2d",Zv),dl(e,"x",_o,_l),dl(e,"y",_o,_l),e.registerComponentView(Dh),e.registerComponentView(ep),e.registerPreprocessor(function(t){t.xAxis&&t.yAxis&&!t.grid&&(t.grid={})})}function ip(e){e.eachSeriesByType("radar",function(t){var r=t.getData(),i=[],n=t.coordinateSystem;if(n){var a=n.getIndicatorAxes();Y(a,function(o,s){r.each(r.mapDimension(a[s].dim),function(l,u){i[u]=i[u]||[];var h=n.dataToPoint(l,s);i[u][s]=yl(h)?h:xl(n)})}),r.each(function(o){var s=Fc(i[o],function(l){return yl(l)})||xl(n);i[o].push(s.slice()),r.setItemLayout(o,i[o])})}})}function yl(e){return!isNaN(e[0])&&!isNaN(e[1])}function xl(e){return[e.cx,e.cy]}function np(e){var t=e.polar;if(t){Be(t)||(t=[t]);var r=[];Y(t,function(i,n){i.indicator?(i.type&&!i.shape&&(i.shape=i.type),e.radar=e.radar||[],Be(e.radar)||(e.radar=[e.radar]),e.radar.push(i)):r.push(i)}),e.polar=r}Y(e.series,function(i){i&&i.type==="radar"&&i.polarIndex&&(i.radarIndex=i.polarIndex)})}var ap=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.render=function(r,i,n){var a=r.coordinateSystem,o=this.group,s=r.getData(),l=this._data;function u(d,c){var v=d.getItemVisual(c,"symbol")||"circle";if(v!=="none"){var p=Xu(d.getItemVisual(c,"symbolSize")),_=Zi(v,-1,-1,2,2),m=d.getItemVisual(c,"symbolRotate")||0;return _.attr({style:{strokeNoScale:!0},z2:100,scaleX:p[0]/2,scaleY:p[1]/2,rotation:m*Math.PI/180||0}),_}}function h(d,c,v,p,_,m){v.removeAll();for(var g=0;g<c.length-1;g++){var y=u(p,_);y&&(y.__dimIdx=g,d[g]?(y.setPosition(d[g]),Gc[m?"initProps":"updateProps"](y,{x:c[g][0],y:c[g][1]},r,_)):y.setPosition(c[g]),v.add(y))}}function f(d){return we(d,function(c){return[a.cx,a.cy]})}s.diff(l).add(function(d){var c=s.getItemLayout(d);if(c){var v=new $u,p=new Ku,_={shape:{points:c}};v.shape.points=f(c),p.shape.points=f(c),Ct(v,_,r,d),Ct(p,_,r,d);var m=new $t,g=new $t;m.add(p),m.add(v),m.add(g),h(p.shape.points,c,g,s,d,!0),s.setItemGraphicEl(d,m)}}).update(function(d,c){var v=l.getItemGraphicEl(c),p=v.childAt(0),_=v.childAt(1),m=v.childAt(2),g={shape:{points:s.getItemLayout(d)}};g.shape.points&&(h(p.shape.points,g.shape.points,m,s,d,!1),qn(_),qn(p),pt(p,g,r),pt(_,g,r),s.setItemGraphicEl(d,v))}).remove(function(d){o.remove(l.getItemGraphicEl(d))}).execute(),s.eachItemGraphicEl(function(d,c){var v=s.getItemModel(c),p=d.childAt(0),_=d.childAt(1),m=d.childAt(2),g=s.getItemVisual(c,"style"),y=g.fill;o.add(d),p.useStyle(He(v.getModel("lineStyle").getLineStyle(),{fill:"none",stroke:y})),Yi(p,v,"lineStyle"),Yi(_,v,"areaStyle");var x=v.getModel("areaStyle"),w=x.isEmpty()&&x.parentModel.isEmpty();_.ignore=w,Y(["emphasis","select","blur"],function(A){var C=v.getModel([A,"areaStyle"]),D=C.isEmpty()&&C.parentModel.isEmpty();_.ensureState(A).ignore=D&&w}),_.useStyle(He(x.getAreaStyle(),{fill:y,opacity:.7,decal:g.decal}));var T=v.getModel("emphasis"),b=T.getModel("itemStyle").getItemStyle();m.eachChild(function(A){if(A instanceof ha){var C=A.style;A.useStyle(lt({image:C.image,x:C.x,y:C.y,width:C.width,height:C.height},g))}else A.useStyle(g),A.setColor(y),A.style.strokeNoScale=!0;var D=A.ensureState("emphasis");D.style=Vo(b);var L=s.getStore().get(s.getDimensionIndex(A.__dimIdx),c);(L==null||isNaN(L))&&(L=""),fa(A,fn(v),{labelFetcher:s.hostModel,labelDataIndex:c,labelDimIndex:A.__dimIdx,defaultText:L,inheritColor:y,defaultOpacity:g.opacity})}),qi(d,T.get("focus"),T.get("blurScope"),T.get("disabled"))}),this._data=s},t.prototype.remove=function(){this.group.removeAll(),this._data=null},t.type="radar",t}(it),op=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r.hasSymbolVisual=!0,r}return t.prototype.init=function(r){e.prototype.init.apply(this,arguments),this.legendVisualProvider=new zc(Yn(this.getData,this),Yn(this.getRawData,this))},t.prototype.getInitialData=function(r,i){return Uc(this,{generateCoord:"indicator_",generateCoordCount:1/0})},t.prototype.formatTooltip=function(r,i,n){var a=this.getData(),o=this.coordinateSystem,s=o.getIndicatorAxes(),l=this.getData().getName(r),u=l===""?this.name:l,h=Vc(this,r);return Is("section",{header:u,sortBlocks:!0,blocks:we(s,function(f){var d=a.get(a.mapDimension(f.dim),r);return Is("nameValue",{markerType:"subItem",markerColor:h,name:f.name,value:d,sortParam:d})})})},t.prototype.getTooltipPosition=function(r){if(r!=null){for(var i=this.getData(),n=this.coordinateSystem,a=i.getValues(we(n.dimensions,function(u){return i.mapDimension(u)}),r),o=0,s=a.length;o<s;o++)if(!isNaN(a[o])){var l=n.getIndicatorAxes();return n.coordToPoint(l[o].dataToCoord(a[o]),o)}}},t.type="series.radar",t.dependencies=["radar"],t.defaultOption={z:2,colorBy:"data",coordinateSystem:"radar",legendHoverLink:!0,radarIndex:0,lineStyle:{width:2,type:"solid",join:"round"},label:{position:"top"},symbolSize:8},t}(ft),Pi=Lh.value;function Cn(e,t){return He({show:t},e)}var sp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.optionUpdated=function(){var r=this.get("boundaryGap"),i=this.get("splitNumber"),n=this.get("scale"),a=this.get("axisLine"),o=this.get("axisTick"),s=this.get("axisLabel"),l=this.get("axisName"),u=this.get(["axisName","show"]),h=this.get(["axisName","formatter"]),f=this.get("axisNameGap"),d=this.get("triggerEvent"),c=we(this.get("indicator")||[],function(v){v.max!=null&&v.max>0&&!v.min?v.min=0:v.min!=null&&v.min<0&&!v.max&&(v.max=0);var p=l;v.color!=null&&(p=He({color:v.color},l));var _=le(Vo(v),{boundaryGap:r,splitNumber:i,scale:n,axisLine:a,axisTick:o,axisLabel:s,name:v.text,showName:u,nameLocation:"end",nameGap:f,nameTextStyle:p,triggerEvent:d},!1);if(Uo(h)){var m=_.name;_.name=h.replace("{value}",m??"")}else St(h)&&(_.name=h(_.name,_));var g=new zr(_,null,this.ecModel);return un(g,Wo.prototype),g.mainType="radar",g.componentIndex=this.componentIndex,g},this);this._indicatorModels=c},t.prototype.getIndicatorModels=function(){return this._indicatorModels},t.type="radar",t.defaultOption={z:0,center:["50%","50%"],radius:"75%",startAngle:90,axisName:{show:!0},boundaryGap:[0,0],splitNumber:5,axisNameGap:15,scale:!1,shape:"polygon",axisLine:le({lineStyle:{color:"#bbb"}},Pi.axisLine),axisLabel:Cn(Pi.axisLabel,!1),axisTick:Cn(Pi.axisTick,!1),splitLine:Cn(Pi.splitLine,!0),splitArea:Cn(Pi.splitArea,!0),indicator:[]},t}(Rt),lp=["axisLine","axisTickLabel","axisName"],up=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.render=function(r,i,n){var a=this.group;a.removeAll(),this._buildAxes(r),this._buildSplitLineAndArea(r)},t.prototype._buildAxes=function(r){var i=r.coordinateSystem,n=i.getIndicatorAxes(),a=we(n,function(o){var s=o.model.get("showName")?o.name:"",l=new Yu(o.model,{axisName:s,position:[i.cx,i.cy],rotation:o.angle,labelDirection:-1,tickDirection:-1,nameDirection:1});return l});Y(a,function(o){Y(lp,o.add,o),this.group.add(o.getGroup())},this)},t.prototype._buildSplitLineAndArea=function(r){var i=r.coordinateSystem,n=i.getIndicatorAxes();if(!n.length)return;var a=r.get("shape"),o=r.getModel("splitLine"),s=r.getModel("splitArea"),l=o.getModel("lineStyle"),u=s.getModel("areaStyle"),h=o.get("show"),f=s.get("show"),d=l.get("color"),c=u.get("color"),v=Be(d)?d:[d],p=Be(c)?c:[c],_=[],m=[];function g(I,V,Z){var B=Z%V.length;return I[B]=I[B]||[],B}if(a==="circle")for(var y=n[0].getTicksCoords(),x=i.cx,w=i.cy,T=0;T<y.length;T++){if(h){var b=g(_,v,T);_[b].push(new Hc({shape:{cx:x,cy:w,r:y[T].coord}}))}if(f&&T<y.length-1){var b=g(m,p,T);m[b].push(new kc({shape:{cx:x,cy:w,r0:y[T].coord,r:y[T+1].coord}}))}}else for(var A,C=we(n,function(I,V){var Z=I.getTicksCoords();return A=A==null?Z.length-1:Math.min(Z.length-1,A),we(Z,function(B){return i.coordToPoint(B.coord,V)})}),D=[],T=0;T<=A;T++){for(var L=[],M=0;M<n.length;M++)L.push(C[M][T]);if(L[0]&&L.push(L[0].slice()),h){var b=g(_,v,T);_[b].push(new Ku({shape:{points:L}}))}if(f&&D){var b=g(m,p,T-1);m[b].push(new $u({shape:{points:L.concat(D)}}))}D=L.slice().reverse()}var P=l.getLineStyle(),N=u.getAreaStyle();Y(m,function(I,V){this.group.add(Rs(I,{style:He({stroke:"none",fill:p[V%p.length]},N),silent:!0}))},this),Y(_,function(I,V){this.group.add(Rs(I,{style:He({fill:"none",stroke:v[V%v.length]},P),silent:!0}))},this)},t.type="radar",t}(Qt),hp=function(e){me(t,e);function t(r,i,n){var a=e.call(this,r,i,n)||this;return a.type="value",a.angle=0,a.name="",a}return t}(Si),fp=function(){function e(t,r,i){this.dimensions=[],this._model=t,this._indicatorAxes=we(t.getIndicatorModels(),function(n,a){var o="indicator_"+a,s=new hp(o,new fo);return s.name=n.get("name"),s.model=n,n.axis=s,this.dimensions.push(o),s},this),this.resize(t,i)}return e.prototype.getIndicatorAxes=function(){return this._indicatorAxes},e.prototype.dataToPoint=function(t,r){var i=this._indicatorAxes[r];return this.coordToPoint(i.dataToCoord(t),r)},e.prototype.coordToPoint=function(t,r){var i=this._indicatorAxes[r],n=i.angle,a=this.cx+t*Math.cos(n),o=this.cy-t*Math.sin(n);return[a,o]},e.prototype.pointToData=function(t){var r=t[0]-this.cx,i=t[1]-this.cy,n=Math.sqrt(r*r+i*i);r/=n,i/=n;for(var a=Math.atan2(-i,r),o=1/0,s,l=-1,u=0;u<this._indicatorAxes.length;u++){var h=this._indicatorAxes[u],f=Math.abs(a-h.angle);f<o&&(s=h,l=u,o=f)}return[l,+(s&&s.coordToData(n))]},e.prototype.resize=function(t,r){var i=t.get("center"),n=r.getWidth(),a=r.getHeight(),o=Math.min(n,a)/2;this.cx=dr(i[0],n),this.cy=dr(i[1],a),this.startAngle=t.get("startAngle")*Math.PI/180;var s=t.get("radius");(Uo(s)||ci(s))&&(s=[0,s]),this.r0=dr(s[0],o),this.r=dr(s[1],o),Y(this._indicatorAxes,function(l,u){l.setExtent(this.r0,this.r);var h=this.startAngle+u*Math.PI*2/this._indicatorAxes.length;h=Math.atan2(Math.sin(h),Math.cos(h)),l.angle=h},this)},e.prototype.update=function(t,r){var i=this._indicatorAxes,n=this._model;Y(i,function(s){s.scale.setExtent(1/0,-1/0)}),t.eachSeriesByType("radar",function(s,l){if(!(s.get("coordinateSystem")!=="radar"||t.getComponent("radar",s.get("radarIndex"))!==n)){var u=s.getData();Y(i,function(h){h.scale.unionExtentFromData(u,u.mapDimension(h.dim))})}},this);var a=n.get("splitNumber"),o=new fo;o.setExtent(0,a),o.setInterval(1),Y(i,function(s,l){Ch(s.scale,s.model,o)})},e.prototype.convertToPixel=function(t,r,i){return console.warn("Not implemented."),null},e.prototype.convertFromPixel=function(t,r,i){return console.warn("Not implemented."),null},e.prototype.containPoint=function(t){return console.warn("Not implemented."),!1},e.create=function(t,r){var i=[];return t.eachComponent("radar",function(n){var a=new e(n,t,r);i.push(a),n.coordinateSystem=a}),t.eachSeriesByType("radar",function(n){n.get("coordinateSystem")==="radar"&&(n.coordinateSystem=i[n.get("radarIndex")||0])}),i},e.dimensions=[],e}();function cp(e){e.registerCoordinateSystem("radar",fp),e.registerComponentModel(sp),e.registerComponentView(up),e.registerVisual({seriesType:"radar",reset:function(t){var r=t.getData();r.each(function(i){r.setItemVisual(i,"legendIcon","roundRect")}),r.setVisual("legendIcon","roundRect")}})}function dp(e){Ne(cp),e.registerChartView(ap),e.registerSeriesModel(op),e.registerLayout(ip),e.registerProcessor(Wc("radar")),e.registerPreprocessor(np)}var vp={南海诸岛:[32,80],广东:[0,-10],香港:[10,5],澳门:[-10,10],天津:[5,5]};function pp(e,t){if(e==="china"){var r=vp[t.name];if(r){var i=t.getCenter();i[0]+=r[0]/10.5,i[1]+=-r[1]/(10.5/.75),t.setCenter(i)}}}var bt=Kt();function gp(e){var t=e.mainData,r=e.datas;r||(r={main:t},e.datasAttr={main:"data"}),e.datas=e.mainData=null,Ph(t,r,e),Y(r,function(i){Y(t.TRANSFERABLE_METHODS,function(n){i.wrapMethod(n,ui(mp,e))})}),t.wrapMethod("cloneShallow",ui(yp,e)),Y(t.CHANGABLE_METHODS,function(i){t.wrapMethod(i,ui(_p,e))}),Xc(r[t.dataType]===t)}function mp(e,t){if(wp(this)){var r=lt({},bt(this).datas);r[this.dataType]=t,Ph(t,r,e)}else Jo(t,this.dataType,bt(this).mainData,e);return t}function _p(e,t){return e.struct&&e.struct.update(),t}function yp(e,t){return Y(bt(t).datas,function(r,i){r!==t&&Jo(r.cloneShallow(),i,t,e)}),t}function xp(e){var t=bt(this).mainData;return e==null||t==null?t:bt(t).datas[e]}function Tp(){var e=bt(this).mainData;return e==null?[{data:e}]:we(Jt(bt(e).datas),function(t){return{type:t,data:bt(e).datas[t]}})}function wp(e){return bt(e).mainData===e}function Ph(e,t,r){bt(e).datas={},Y(t,function(i,n){Jo(i,n,e,r)})}function Jo(e,t,r,i){bt(r).datas[t]=e,bt(e).mainData=r,e.dataType=t,i.struct&&(e[i.structAttr]=i.struct,i.struct[i.datasAttr[t]]=e),e.getLinkedData=xp,e.getLinkedDataAll=Tp}function Yr(e){return"_EC_"+e}var Sp=function(){function e(t){this.type="graph",this.nodes=[],this.edges=[],this._nodesMap={},this._edgesMap={},this._directed=t||!1}return e.prototype.isDirected=function(){return this._directed},e.prototype.addNode=function(t,r){t=t==null?""+r:""+t;var i=this._nodesMap;if(!i[Yr(t)]){var n=new Pr(t,r);return n.hostGraph=this,this.nodes.push(n),i[Yr(t)]=n,n}},e.prototype.getNodeByIndex=function(t){var r=this.data.getRawIndex(t);return this.nodes[r]},e.prototype.getNodeById=function(t){return this._nodesMap[Yr(t)]},e.prototype.addEdge=function(t,r,i){var n=this._nodesMap,a=this._edgesMap;if(ci(t)&&(t=this.nodes[t]),ci(r)&&(r=this.nodes[r]),t instanceof Pr||(t=n[Yr(t)]),r instanceof Pr||(r=n[Yr(r)]),!(!t||!r)){var o=t.id+"-"+r.id,s=new Nh(t,r,i);return s.hostGraph=this,this._directed&&(t.outEdges.push(s),r.inEdges.push(s)),t.edges.push(s),t!==r&&r.edges.push(s),this.edges.push(s),a[o]=s,s}},e.prototype.getEdgeByIndex=function(t){var r=this.edgeData.getRawIndex(t);return this.edges[r]},e.prototype.getEdge=function(t,r){t instanceof Pr&&(t=t.id),r instanceof Pr&&(r=r.id);var i=this._edgesMap;return this._directed?i[t+"-"+r]:i[t+"-"+r]||i[r+"-"+t]},e.prototype.eachNode=function(t,r){for(var i=this.nodes,n=i.length,a=0;a<n;a++)i[a].dataIndex>=0&&t.call(r,i[a],a)},e.prototype.eachEdge=function(t,r){for(var i=this.edges,n=i.length,a=0;a<n;a++)i[a].dataIndex>=0&&i[a].node1.dataIndex>=0&&i[a].node2.dataIndex>=0&&t.call(r,i[a],a)},e.prototype.breadthFirstTraverse=function(t,r,i,n){if(r instanceof Pr||(r=this._nodesMap[Yr(r)]),!!r){for(var a=i==="out"?"outEdges":i==="in"?"inEdges":"edges",o=0;o<this.nodes.length;o++)this.nodes[o].__visited=!1;if(!t.call(n,r,null))for(var s=[r];s.length;)for(var l=s.shift(),u=l[a],o=0;o<u.length;o++){var h=u[o],f=h.node1===l?h.node2:h.node1;if(!f.__visited){if(t.call(n,f,l))return;s.push(f),f.__visited=!0}}}},e.prototype.update=function(){for(var t=this.data,r=this.edgeData,i=this.nodes,n=this.edges,a=0,o=i.length;a<o;a++)i[a].dataIndex=-1;for(var a=0,o=t.count();a<o;a++)i[t.getRawIndex(a)].dataIndex=a;r.filterSelf(function(s){var l=n[r.getRawIndex(s)];return l.node1.dataIndex>=0&&l.node2.dataIndex>=0});for(var a=0,o=n.length;a<o;a++)n[a].dataIndex=-1;for(var a=0,o=r.count();a<o;a++)n[r.getRawIndex(a)].dataIndex=a},e.prototype.clone=function(){for(var t=new e(this._directed),r=this.nodes,i=this.edges,n=0;n<r.length;n++)t.addNode(r[n].id,r[n].dataIndex);for(var n=0;n<i.length;n++){var a=i[n];t.addEdge(a.node1.id,a.node2.id,a.dataIndex)}return t},e}(),Pr=function(){function e(t,r){this.inEdges=[],this.outEdges=[],this.edges=[],this.dataIndex=-1,this.id=t??"",this.dataIndex=r??-1}return e.prototype.degree=function(){return this.edges.length},e.prototype.inDegree=function(){return this.inEdges.length},e.prototype.outDegree=function(){return this.outEdges.length},e.prototype.getModel=function(t){if(!(this.dataIndex<0)){var r=this.hostGraph,i=r.data.getItemModel(this.dataIndex);return i.getModel(t)}},e.prototype.getAdjacentDataIndices=function(){for(var t={edge:[],node:[]},r=0;r<this.edges.length;r++){var i=this.edges[r];i.dataIndex<0||(t.edge.push(i.dataIndex),t.node.push(i.node1.dataIndex,i.node2.dataIndex))}return t},e.prototype.getTrajectoryDataIndices=function(){for(var t=Yt(),r=Yt(),i=0;i<this.edges.length;i++){var n=this.edges[i];if(!(n.dataIndex<0)){t.set(n.dataIndex,!0);for(var a=[n.node1],o=[n.node2],s=0;s<a.length;){var l=a[s];s++,r.set(l.dataIndex,!0);for(var u=0;u<l.inEdges.length;u++)t.set(l.inEdges[u].dataIndex,!0),a.push(l.inEdges[u].node1)}for(s=0;s<o.length;){var h=o[s];s++,r.set(h.dataIndex,!0);for(var u=0;u<h.outEdges.length;u++)t.set(h.outEdges[u].dataIndex,!0),o.push(h.outEdges[u].node2)}}}return{edge:t.keys(),node:r.keys()}},e}(),Nh=function(){function e(t,r,i){this.dataIndex=-1,this.node1=t,this.node2=r,this.dataIndex=i??-1}return e.prototype.getModel=function(t){if(!(this.dataIndex<0)){var r=this.hostGraph,i=r.edgeData.getItemModel(this.dataIndex);return i.getModel(t)}},e.prototype.getAdjacentDataIndices=function(){return{edge:[this.dataIndex],node:[this.node1.dataIndex,this.node2.dataIndex]}},e.prototype.getTrajectoryDataIndices=function(){var t=Yt(),r=Yt();t.set(this.dataIndex,!0);for(var i=[this.node1],n=[this.node2],a=0;a<i.length;){var o=i[a];a++,r.set(o.dataIndex,!0);for(var s=0;s<o.inEdges.length;s++)t.set(o.inEdges[s].dataIndex,!0),i.push(o.inEdges[s].node1)}for(a=0;a<n.length;){var l=n[a];a++,r.set(l.dataIndex,!0);for(var s=0;s<l.outEdges.length;s++)t.set(l.outEdges[s].dataIndex,!0),n.push(l.outEdges[s].node2)}return{edge:t.keys(),node:r.keys()}},e}();function Ih(e,t){return{getValue:function(r){var i=this[e][t];return i.getStore().get(i.getDimensionIndex(r||"value"),this.dataIndex)},setVisual:function(r,i){this.dataIndex>=0&&this[e][t].setItemVisual(this.dataIndex,r,i)},getVisual:function(r){return this[e][t].getItemVisual(this.dataIndex,r)},setLayout:function(r,i){this.dataIndex>=0&&this[e][t].setItemLayout(this.dataIndex,r,i)},getLayout:function(){return this[e][t].getItemLayout(this.dataIndex)},getGraphicEl:function(){return this[e][t].getItemGraphicEl(this.dataIndex)},getRawIndex:function(){return this[e][t].getRawIndex(this.dataIndex)}}}un(Pr,Ih("hostGraph","data"));un(Nh,Ih("hostGraph","edgeData"));function bp(e,t,r,i){return e&&(e.legacy||e.legacy!==!1&&!r&&!i&&t!=="tspan"&&(t==="text"||ce(e,"text")))}function Ap(e,t,r){var i=e,n,a,o;if(t==="text")o=i;else{o={},ce(i,"text")&&(o.text=i.text),ce(i,"rich")&&(o.rich=i.rich),ce(i,"textFill")&&(o.fill=i.textFill),ce(i,"textStroke")&&(o.stroke=i.textStroke),ce(i,"fontFamily")&&(o.fontFamily=i.fontFamily),ce(i,"fontSize")&&(o.fontSize=i.fontSize),ce(i,"fontStyle")&&(o.fontStyle=i.fontStyle),ce(i,"fontWeight")&&(o.fontWeight=i.fontWeight),a={type:"text",style:o,silent:!0},n={};var s=ce(i,"textPosition");n.position=s?i.textPosition:"inside",ce(i,"textPosition")&&(n.position=i.textPosition),ce(i,"textOffset")&&(n.offset=i.textOffset),ce(i,"textRotation")&&(n.rotation=i.textRotation),ce(i,"textDistance")&&(n.distance=i.textDistance)}return Tl(o,e),Y(o.rich,function(l){Tl(l,l)}),{textConfig:n,textContent:a}}function Tl(e,t){t&&(t.font=t.textFont||t.font,ce(t,"textStrokeWidth")&&(e.lineWidth=t.textStrokeWidth),ce(t,"textAlign")&&(e.align=t.textAlign),ce(t,"textVerticalAlign")&&(e.verticalAlign=t.textVerticalAlign),ce(t,"textLineHeight")&&(e.lineHeight=t.textLineHeight),ce(t,"textWidth")&&(e.width=t.textWidth),ce(t,"textHeight")&&(e.height=t.textHeight),ce(t,"textBackgroundColor")&&(e.backgroundColor=t.textBackgroundColor),ce(t,"textPadding")&&(e.padding=t.textPadding),ce(t,"textBorderColor")&&(e.borderColor=t.textBorderColor),ce(t,"textBorderWidth")&&(e.borderWidth=t.textBorderWidth),ce(t,"textBorderRadius")&&(e.borderRadius=t.textBorderRadius),ce(t,"textBoxShadowColor")&&(e.shadowColor=t.textBoxShadowColor),ce(t,"textBoxShadowBlur")&&(e.shadowBlur=t.textBoxShadowBlur),ce(t,"textBoxShadowOffsetX")&&(e.shadowOffsetX=t.textBoxShadowOffsetX),ce(t,"textBoxShadowOffsetY")&&(e.shadowOffsetY=t.textBoxShadowOffsetY))}var Rh={position:["x","y"],scale:["scaleX","scaleY"],origin:["originX","originY"]},wl=Jt(Rh);eh($i,function(e,t){return e[t]=1,e},{});$i.join(", ");var Kn=["","style","shape","extra"],di=Kt();function Qo(e,t,r,i,n){var a=e+"Animation",o=Qu(e,i,n)||{},s=di(t).userDuring;return o.duration>0&&(o.during=s?Yn(Pp,{el:t,userDuring:s}):null,o.setToFinal=!0,o.scope=e),lt(o,r[a]),o}function Oa(e,t,r,i){i=i||{};var n=i.dataIndex,a=i.isInit,o=i.clearStyle,s=r.isAnimationEnabled(),l=di(e),u=t.style;l.userDuring=t.during;var h={},f={};if(Ip(e,t,f),bl("shape",t,f),bl("extra",t,f),!a&&s&&(Np(e,t,h),Sl("shape",e,t,h),Sl("extra",e,t,h),Rp(e,t,u,h)),f.style=u,Lp(e,f,o),Mp(e,t),s)if(a){var d={};Y(Kn,function(v){var p=v?t[v]:t;p&&p.enterFrom&&(v&&(d[v]=d[v]||{}),lt(v?d[v]:d,p.enterFrom))});var c=Qo("enter",e,t,r,n);c.duration>0&&e.animateFrom(d,c)}else Cp(e,t,n||0,r,h);Oh(e,t),u?e.dirty():e.markRedraw()}function Oh(e,t){for(var r=di(e).leaveToProps,i=0;i<Kn.length;i++){var n=Kn[i],a=n?t[n]:t;a&&a.leaveTo&&(r||(r=di(e).leaveToProps={}),n&&(r[n]=r[n]||{}),lt(n?r[n]:r,a.leaveTo))}}function Ep(e,t,r,i){if(e){var n=e.parent,a=di(e).leaveToProps;if(a){var o=Qo("update",e,t,r,0);o.done=function(){n.remove(e)},e.animateTo(a,o)}else n.remove(e)}}function Fr(e){return e==="all"}function Lp(e,t,r){var i=t.style;if(!e.isGroup&&i){if(r){e.useStyle({});for(var n=e.animators,a=0;a<n.length;a++){var o=n[a];o.targetName==="style"&&o.changeTarget(e.style)}}e.setStyle(i)}t&&(t.style=null,t&&e.attr(t),t.style=i)}function Cp(e,t,r,i,n){if(n){var a=Qo("update",e,t,i,r);a.duration>0&&e.animateFrom(n,a)}}function Mp(e,t){ce(t,"silent")&&(e.silent=t.silent),ce(t,"ignore")&&(e.ignore=t.ignore),e instanceof Ju&&ce(t,"invisible")&&(e.invisible=t.invisible),e instanceof cn&&ce(t,"autoBatch")&&(e.autoBatch=t.autoBatch)}var Ft={},Dp={setTransform:function(e,t){return Ft.el[e]=t,this},getTransform:function(e){return Ft.el[e]},setShape:function(e,t){var r=Ft.el,i=r.shape||(r.shape={});return i[e]=t,r.dirtyShape&&r.dirtyShape(),this},getShape:function(e){var t=Ft.el.shape;if(t)return t[e]},setStyle:function(e,t){var r=Ft.el,i=r.style;return i&&(i[e]=t,r.dirtyStyle&&r.dirtyStyle()),this},getStyle:function(e){var t=Ft.el.style;if(t)return t[e]},setExtra:function(e,t){var r=Ft.el.extra||(Ft.el.extra={});return r[e]=t,this},getExtra:function(e){var t=Ft.el.extra;if(t)return t[e]}};function Pp(){var e=this,t=e.el;if(t){var r=di(t).userDuring,i=e.userDuring;if(r!==i){e.el=e.userDuring=null;return}Ft.el=t,i(Dp)}}function Sl(e,t,r,i){var n=r[e];if(n){var a=t[e],o;if(a){var s=r.transition,l=n.transition;if(l)if(!o&&(o=i[e]={}),Fr(l))lt(o,a);else for(var u=Ho(l),h=0;h<u.length;h++){var f=u[h],d=a[f];o[f]=d}else if(Fr(s)||Ut(s,e)>=0){!o&&(o=i[e]={});for(var c=Jt(a),h=0;h<c.length;h++){var f=c[h],d=a[f];Op(n[f],d)&&(o[f]=d)}}}}}function bl(e,t,r){var i=t[e];if(i)for(var n=r[e]={},a=Jt(i),o=0;o<a.length;o++){var s=a[o];n[s]=jc(i[s])}}function Np(e,t,r){for(var i=t.transition,n=Fr(i)?$i:Ho(i||[]),a=0;a<n.length;a++){var o=n[a];if(!(o==="style"||o==="shape"||o==="extra")){var s=e[o];r[o]=s}}}function Ip(e,t,r){for(var i=0;i<wl.length;i++){var n=wl[i],a=Rh[n],o=t[n];o&&(r[a[0]]=o[0],r[a[1]]=o[1])}for(var i=0;i<$i.length;i++){var s=$i[i];t[s]!=null&&(r[s]=t[s])}}function Rp(e,t,r,i){if(r){var n=e.style,a;if(n){var o=r.transition,s=t.transition;if(o&&!Fr(o)){var l=Ho(o);!a&&(a=i.style={});for(var u=0;u<l.length;u++){var h=l[u],f=n[h];a[h]=f}}else if(e.getAnimationStyleProps&&(Fr(s)||Fr(o)||Ut(s,"style")>=0)){var d=e.getAnimationStyleProps(),c=d?d.style:null;if(c){!a&&(a=i.style={});for(var v=Jt(r),u=0;u<v.length;u++){var h=v[u];if(c[h]){var f=n[h];a[h]=f}}}}}}}function Op(e,t){return Zc(e)?e!==t:e!=null&&isFinite(e)}var Bh=Kt(),Bp=["percent","easing","shape","style","extra"];function Fp(e){e.stopAnimation("keyframe"),e.attr(Bh(e))}function To(e,t,r){if(!(!r.isAnimationEnabled()||!t)){if(Be(t)){Y(t,function(s){To(e,s,r)});return}var i=t.keyframes,n=t.duration;if(r&&n==null){var a=Qu("enter",r,0);n=a&&a.duration}if(!(!i||!n)){var o=Bh(e);Y(Kn,function(s){if(!(s&&!e[s])){var l;i.sort(function(u,h){return u.percent-h.percent}),Y(i,function(u){var h=e.animators,f=s?u[s]:u;if(f){var d=Jt(f);if(s||(d=Zt(d,function(p){return Ut(Bp,p)<0})),!!d.length){l||(l=e.animate(s,t.loop,!0),l.scope="keyframe");for(var c=0;c<h.length;c++)h[c]!==l&&h[c].targetName===l.targetName&&h[c].stopTracks(d);s&&(o[s]=o[s]||{});var v=s?o[s]:o;Y(d,function(p){v[p]=((s?e[s]:e)||{})[p]}),l.whenWithKeys(n*u.percent,f,d,u.easing)}}}),l&&l.delay(t.delay||0).duration(n).start(t.easing)}})}}}function Gp(e){Ne(rp),Ne(qc)}function zp(e,t){var r=e.existing;if(t.id=e.keyInfo.id,!t.type&&r&&(t.type=r.type),t.parentId==null){var i=t.parentOption;i?t.parentId=i.id:r&&(t.parentId=r.parentId)}t.parentOption=null}function Al(e,t){var r;return Y(t,function(i){e[i]!=null&&e[i]!=="auto"&&(r=!0)}),r}function Up(e,t,r){var i=lt({},r),n=e[t],a=r.$action||"merge";a==="merge"?n?(le(n,i,!0),Zu(n,i,{ignoreSize:!0}),$c(r,n),Mn(r,n),Mn(r,n,"shape"),Mn(r,n,"style"),Mn(r,n,"extra"),r.clipPath=n.clipPath):e[t]=i:a==="replace"?e[t]=i:a==="remove"&&n&&(e[t]=null)}var Fh=["transition","enterFrom","leaveTo"],Vp=Fh.concat(["enterAnimation","updateAnimation","leaveAnimation"]);function Mn(e,t,r){if(r&&(!e[r]&&t[r]&&(e[r]={}),e=e[r],t=t[r]),!(!e||!t))for(var i=r?Fh:Vp,n=0;n<i.length;n++){var a=i[n];e[a]==null&&t[a]!=null&&(e[a]=t[a])}}function Hp(e,t){if(e&&(e.hv=t.hv=[Al(t,["left","right"]),Al(t,["top","bottom"])],e.type==="group")){var r=e,i=t;r.width==null&&(r.width=i.width=0),r.height==null&&(r.height=i.height=0)}}var kp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r.preventAutoZ=!0,r}return t.prototype.mergeOption=function(r,i){var n=this.option.elements;this.option.elements=null,e.prototype.mergeOption.call(this,r,i),this.option.elements=n},t.prototype.optionUpdated=function(r,i){var n=this.option,a=(i?n:r).elements,o=n.elements=i?[]:n.elements,s=[];this._flatten(a,s,null);var l=Yc(o,s,"normalMerge"),u=this._elOptionsToUpdate=[];Y(l,function(h,f){var d=h.newOption;d&&(u.push(d),zp(h,d),Up(o,f,d),Hp(o[f],d))},this),n.elements=Zt(o,function(h){return h&&delete h.$action,h!=null})},t.prototype._flatten=function(r,i,n){Y(r,function(a){if(a){n&&(a.parentOption=n),i.push(a);var o=a.children;o&&o.length&&this._flatten(o,i,a),delete a.children}},this)},t.prototype.useElOptionsToUpdate=function(){var r=this._elOptionsToUpdate;return this._elOptionsToUpdate=null,r},t.type="graphic",t.defaultOption={elements:[]},t}(Rt),El={path:null,compoundPath:null,group:$t,image:ha,text:gr},xt=Kt(),Wp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type=t.type,r}return t.prototype.init=function(){this._elMap=Yt()},t.prototype.render=function(r,i,n){r!==this._lastGraphicModel&&this._clear(),this._lastGraphicModel=r,this._updateElements(r),this._relocate(r,n)},t.prototype._updateElements=function(r){var i=r.useElOptionsToUpdate();if(i){var n=this._elMap,a=this.group,o=r.get("z"),s=r.get("zlevel");Y(i,function(l){var u=xn(l.id,null),h=u!=null?n.get(u):null,f=xn(l.parentId,null),d=f!=null?n.get(f):a,c=l.type,v=l.style;c==="text"&&v&&l.hv&&l.hv[1]&&(v.textVerticalAlign=v.textBaseline=v.verticalAlign=v.align=null);var p=l.textContent,_=l.textConfig;if(v&&bp(v,c,!!_,!!p)){var m=Ap(v,c);!_&&m.textConfig&&(_=l.textConfig=m.textConfig),!p&&m.textContent&&(p=m.textContent)}var g=Xp(l),y=l.$action||"merge",x=y==="merge",w=y==="replace";if(x){var T=!h,b=h;T?b=Ll(u,d,l.type,n):(b&&(xt(b).isNew=!1),Fp(b)),b&&(Oa(b,g,r,{isInit:T}),Cl(b,l,o,s))}else if(w){Wn(h,l,n,r);var A=Ll(u,d,l.type,n);A&&(Oa(A,g,r,{isInit:!0}),Cl(A,l,o,s))}else y==="remove"&&(Oh(h,l),Wn(h,l,n,r));var C=n.get(u);if(C&&p)if(x){var D=C.getTextContent();D?D.attr(p):C.setTextContent(new gr(p))}else w&&C.setTextContent(new gr(p));if(C){var L=l.clipPath;if(L){var M=L.type,P=void 0,T=!1;if(x){var N=C.getClipPath();T=!N||xt(N).type!==M,P=T?wo(M):N}else w&&(T=!0,P=wo(M));C.setClipPath(P),Oa(P,L,r,{isInit:T}),To(P,L.keyframeAnimation,r)}var I=xt(C);C.setTextConfig(_),I.option=l,jp(C,r,l),Kc({el:C,componentModel:r,itemName:C.name,itemTooltipOption:l.tooltip}),To(C,l.keyframeAnimation,r)}})}},t.prototype._relocate=function(r,i){for(var n=r.option.elements,a=this.group,o=this._elMap,s=i.getWidth(),l=i.getHeight(),u=["x","y"],h=0;h<n.length;h++){var f=n[h],d=xn(f.id,null),c=d!=null?o.get(d):null;if(!(!c||!c.isGroup)){var v=c.parent,p=v===a,_=xt(c),m=xt(v);_.width=dr(_.option.width,p?s:m.width)||0,_.height=dr(_.option.height,p?l:m.height)||0}}for(var h=n.length-1;h>=0;h--){var f=n[h],d=xn(f.id,null),c=d!=null?o.get(d):null;if(c){var v=c.parent,m=xt(v),g=v===a?{width:s,height:l}:{width:m.width,height:m.height},y={},x=Jc(c,f,g,null,{hv:f.hv,boundingMode:f.bounding},y);if(!xt(c).isNew&&x){for(var w=f.transition,T={},b=0;b<u.length;b++){var A=u[b],C=y[A];w&&(Fr(w)||Ut(w,A)>=0)?T[A]=C:c[A]=C}pt(c,T,r,0)}else c.attr(y)}}},t.prototype._clear=function(){var r=this,i=this._elMap;i.each(function(n){Wn(n,xt(n).option,i,r._lastGraphicModel)}),this._elMap=Yt()},t.prototype.dispose=function(){this._clear()},t.type="graphic",t}(Qt);function wo(e){var t=ce(El,e)?El[e]:ed(e),r=new t({});return xt(r).type=e,r}function Ll(e,t,r,i){var n=wo(r);return t.add(n),i.set(e,n),xt(n).id=e,xt(n).isNew=!0,n}function Wn(e,t,r,i){var n=e&&e.parent;n&&(e.type==="group"&&e.traverse(function(a){Wn(a,t,r,i)}),Ep(e,t,i),r.removeKey(xt(e).id))}function Cl(e,t,r,i){e.isGroup||Y([["cursor",Ju.prototype.cursor],["zlevel",i||0],["z",r||0],["z2",0]],function(n){var a=n[0];ce(t,a)?e[a]=Wu(t[a],n[1]):e[a]==null&&(e[a]=n[1])}),Y(Jt(t),function(n){if(n.indexOf("on")===0){var a=t[n];e[n]=St(a)?a:null}}),ce(t,"draggable")&&(e.draggable=t.draggable),t.name!=null&&(e.name=t.name),t.id!=null&&(e.id=t.id)}function Xp(e){return e=lt({},e),Y(["id","parentId","$action","hv","bounding","textContent","clipPath"].concat(Qc),function(t){delete e[t]}),e}function jp(e,t,r){var i=_t(e).eventData;!e.silent&&!e.ignore&&!i&&(i=_t(e).eventData={componentType:"graphic",componentIndex:t.componentIndex,name:e.name}),i&&(i.info=r.info)}function Zp(e){e.registerComponentModel(kp),e.registerComponentView(Wp),e.registerPreprocessor(function(t){var r=t.graphic;Be(r)?!r[0]||!r[0].elements?t.graphic=[{elements:r}]:t.graphic=[t.graphic[0]]:r&&!r.elements&&(t.graphic=[{elements:[r]}])})}var qp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type="dataset",r}return t.prototype.init=function(r,i,n){e.prototype.init.call(this,r,i,n),this._sourceManager=new td(this),Os(this)},t.prototype.mergeOption=function(r,i){e.prototype.mergeOption.call(this,r,i),Os(this)},t.prototype.optionUpdated=function(){this._sourceManager.dirty()},t.prototype.getSourceManager=function(){return this._sourceManager},t.type="dataset",t.defaultOption={seriesLayoutBy:rd},t}(Rt),Yp=function(e){me(t,e);function t(){var r=e!==null&&e.apply(this,arguments)||this;return r.type="dataset",r}return t.type="dataset",t}(Qt);function $p(e){e.registerComponentModel(qp),e.registerComponentView(Yp)}Ne([th,$p]);Ne(ev);function Ml(e,t,r){typeof t=="object"&&(r=t,t=null);var i=this,n;if(!(e instanceof Function)){n=[];for(var a in e)e.hasOwnProperty(a)&&n.push(a)}var o=function(l){if(i.apply(this,arguments),e instanceof Function?Dl(this,e.call(this,l)):Kp(this,e,n),this.constructor===o)for(var u=o.__initializers__,h=0;h<u.length;h++)u[h].apply(this,arguments)};o.__super__=i,i.__initializers__?o.__initializers__=i.__initializers__.slice():o.__initializers__=[],t&&o.__initializers__.push(t);var s=function(){};return s.prototype=i.prototype,o.prototype=new s,o.prototype.constructor=o,Dl(o.prototype,r),o.extend=i.extend,o.derive=i.extend,o}function Dl(e,t){if(t)for(var r in t)t.hasOwnProperty(r)&&(e[r]=t[r])}function Kp(e,t,r){for(var i=0;i<r.length;i++){var n=r[i];e[n]=t[n]}}const Jp={extend:Ml,derive:Ml};function Qp(e,t){this.action=e,this.context=t}var es={trigger:function(e){if(this.hasOwnProperty("__handlers__")&&this.__handlers__.hasOwnProperty(e)){var t=this.__handlers__[e],r=t.length,i=-1,n=arguments;switch(n.length){case 1:for(;++i<r;)t[i].action.call(t[i].context);return;case 2:for(;++i<r;)t[i].action.call(t[i].context,n[1]);return;case 3:for(;++i<r;)t[i].action.call(t[i].context,n[1],n[2]);return;case 4:for(;++i<r;)t[i].action.call(t[i].context,n[1],n[2],n[3]);return;case 5:for(;++i<r;)t[i].action.call(t[i].context,n[1],n[2],n[3],n[4]);return;default:for(;++i<r;)t[i].action.apply(t[i].context,Array.prototype.slice.call(n,1));return}}},on:function(e,t,r){if(!(!e||!t)){var i=this.__handlers__||(this.__handlers__={});if(!i[e])i[e]=[];else if(this.has(e,t))return;var n=new Qp(t,r||this);return i[e].push(n),this}},once:function(e,t,r){if(!e||!t)return;var i=this;function n(){i.off(e,n),t.apply(this,arguments)}return this.on(e,n,r)},before:function(e,t,r){if(!(!e||!t))return e="before"+e,this.on(e,t,r)},after:function(e,t,r){if(!(!e||!t))return e="after"+e,this.on(e,t,r)},success:function(e,t){return this.once("success",e,t)},error:function(e,t){return this.once("error",e,t)},off:function(e,t){var r=this.__handlers__||(this.__handlers__={});if(!t){r[e]=[];return}if(r[e]){for(var i=r[e],n=[],a=0;a<i.length;a++)t&&i[a].action!==t&&n.push(i[a]);r[e]=n}return this},has:function(e,t){var r=this.__handlers__;if(!r||!r[e])return!1;for(var i=r[e],n=0;n<i.length;n++)if(i[n].action===t)return!0}},eg=0,tg=Array.prototype,rg=tg.forEach,Pe={genGUID:function(){return++eg},relative2absolute:function(e,t){if(!t||e.match(/^\//))return e;for(var r=e.split("/"),i=t.split("/"),n=r[0];n==="."||n==="..";)n===".."&&i.pop(),r.shift(),n=r[0];return i.join("/")+"/"+r.join("/")},extend:function(e,t){if(t)for(var r in t)t.hasOwnProperty(r)&&(e[r]=t[r]);return e},defaults:function(e,t){if(t)for(var r in t)e[r]===void 0&&(e[r]=t[r]);return e},extendWithPropList:function(e,t,r){if(t)for(var i=0;i<r.length;i++){var n=r[i];e[n]=t[n]}return e},defaultsWithPropList:function(e,t,r){if(t)for(var i=0;i<r.length;i++){var n=r[i];e[n]==null&&(e[n]=t[n])}return e},each:function(e,t,r){if(e&&t)if(e.forEach&&e.forEach===rg)e.forEach(t,r);else if(e.length===+e.length)for(var i=0,n=e.length;i<n;i++)t.call(r,e[i],i,e);else for(var a in e)e.hasOwnProperty(a)&&t.call(r,e[a],a,e)},isObject:function(e){return e===Object(e)},isArray:function(e){return Array.isArray(e)},isArrayLike:function(e){return e?e.length===+e.length:!1},clone:function(e){if(Pe.isObject(e)){if(Pe.isArray(e))return e.slice();if(Pe.isArrayLike(e)){for(var t=new e.constructor(e.length),r=0;r<e.length;r++)t[r]=e[r];return t}else return Pe.extend({},e)}else return e}},Qe=function(){this.__uid__=Pe.genGUID()};Qe.__initializers__=[function(e){Pe.extend(this,e)}];Pe.extend(Qe,Jp);Pe.extend(Qe.prototype,es);var Pl=["OES_texture_float","OES_texture_half_float","OES_texture_float_linear","OES_texture_half_float_linear","OES_standard_derivatives","OES_vertex_array_object","OES_element_index_uint","WEBGL_compressed_texture_s3tc","WEBGL_depth_texture","EXT_texture_filter_anisotropic","EXT_shader_texture_lod","WEBGL_draw_buffers","EXT_frag_depth","EXT_sRGB","ANGLE_instanced_arrays"],Nl=["MAX_TEXTURE_SIZE","MAX_CUBE_MAP_TEXTURE_SIZE"];function ig(e){for(var t={},r={},i=0;i<Pl.length;i++){var n=Pl[i];o(n)}for(var i=0;i<Nl.length;i++){var a=Nl[i];r[a]=e.getParameter(e[a])}this.getExtension=function(s){return s in t||o(s),t[s]},this.getParameter=function(s){return r[s]};function o(s){if(e.getExtension){var l=e.getExtension(s);l||(l=e.getExtension("MOZ_"+s)),l||(l=e.getExtension("WEBKIT_"+s)),t[s]=l}}}const F={DEPTH_BUFFER_BIT:256,STENCIL_BUFFER_BIT:1024,COLOR_BUFFER_BIT:16384,POINTS:0,LINES:1,LINE_LOOP:2,LINE_STRIP:3,TRIANGLES:4,TRIANGLE_STRIP:5,TRIANGLE_FAN:6,STREAM_DRAW:35040,STATIC_DRAW:35044,DYNAMIC_DRAW:35048,FRONT:1028,BACK:1029,FRONT_AND_BACK:1032,CW:2304,CCW:2305,BYTE:5120,UNSIGNED_BYTE:5121,SHORT:5122,UNSIGNED_SHORT:5123,INT:5124,UNSIGNED_INT:5125,FLOAT:5126,DEPTH_COMPONENT:6402,ALPHA:6406,RGB:6407,RGBA:6408,LUMINANCE:6409,LUMINANCE_ALPHA:6410,NEAREST:9728,LINEAR:9729,NEAREST_MIPMAP_NEAREST:9984,LINEAR_MIPMAP_NEAREST:9985,NEAREST_MIPMAP_LINEAR:9986,LINEAR_MIPMAP_LINEAR:9987,TEXTURE_2D:3553,TEXTURE_CUBE_MAP:34067,REPEAT:10497,CLAMP_TO_EDGE:33071,MIRRORED_REPEAT:33648,FRAMEBUFFER:36160,RENDERBUFFER:36161,DEPTH_STENCIL:34041,COLOR_ATTACHMENT0:36064,DEPTH_ATTACHMENT:36096,STENCIL_ATTACHMENT:36128,DEPTH_STENCIL_ATTACHMENT:33306};function ng(e){var t=new XMLHttpRequest;t.open("get",e.url),t.responseType=e.responseType||"text",e.onprogress&&(t.onprogress=function(r){if(r.lengthComputable){var i=r.loaded/r.total;e.onprogress(i,r.loaded,r.total)}else e.onprogress(null)}),t.onload=function(r){t.status>=400?e.onerror&&e.onerror():e.onload&&e.onload(t.response)},e.onerror&&(t.onerror=e.onerror),t.send(null)}const ag={get:ng};var Ba,de={};de.supportWebGL=function(){if(Ba==null)try{var e=document.createElement("canvas"),t=e.getContext("webgl")||e.getContext("experimental-webgl");if(!t)throw new Error}catch{Ba=!1}return Ba};de.Int8Array=typeof Int8Array>"u"?Array:Int8Array;de.Uint8Array=typeof Uint8Array>"u"?Array:Uint8Array;de.Uint16Array=typeof Uint16Array>"u"?Array:Uint16Array;de.Uint32Array=typeof Uint32Array>"u"?Array:Uint32Array;de.Int16Array=typeof Int16Array>"u"?Array:Int16Array;de.Float32Array=typeof Float32Array>"u"?Array:Float32Array;de.Float64Array=typeof Float64Array>"u"?Array:Float64Array;var Ir={};typeof window<"u"?Ir=window:typeof global<"u"&&(Ir=global);de.requestAnimationFrame=Ir.requestAnimationFrame||Ir.msRequestAnimationFrame||Ir.mozRequestAnimationFrame||Ir.webkitRequestAnimationFrame||function(e){setTimeout(e,16)};de.createCanvas=function(){return document.createElement("canvas")};de.createImage=function(){return new Ir.Image};de.request={get:ag.get};de.addEventListener=function(e,t,r,i){e.addEventListener(t,r,i)};de.removeEventListener=function(e,t,r){e.removeEventListener(t,r)};var qe=function(){this.head=null,this.tail=null,this._length=0};qe.prototype.insert=function(e){var t=new qe.Entry(e);return this.insertEntry(t),t};qe.prototype.insertAt=function(e,t){if(!(e<0)){for(var r=this.head,i=0;r&&i!=e;)r=r.next,i++;if(r){var n=new qe.Entry(t),a=r.prev;a?(a.next=n,n.prev=a):this.head=n,n.next=r,r.prev=n}else this.insert(t)}};qe.prototype.insertBeforeEntry=function(e,t){var r=new qe.Entry(e),i=t.prev;i?(i.next=r,r.prev=i):this.head=r,r.next=t,t.prev=r,this._length++};qe.prototype.insertEntry=function(e){this.head?(this.tail.next=e,e.prev=this.tail,this.tail=e):this.head=this.tail=e,this._length++};qe.prototype.remove=function(e){var t=e.prev,r=e.next;t?t.next=r:this.head=r,r?r.prev=t:this.tail=t,e.next=e.prev=null,this._length--};qe.prototype.removeAt=function(e){if(!(e<0)){for(var t=this.head,r=0;t&&r!=e;)t=t.next,r++;if(t)return this.remove(t),t.value}};qe.prototype.getHead=function(){if(this.head)return this.head.value};qe.prototype.getTail=function(){if(this.tail)return this.tail.value};qe.prototype.getAt=function(e){if(!(e<0)){for(var t=this.head,r=0;t&&r!=e;)t=t.next,r++;return t.value}};qe.prototype.indexOf=function(e){for(var t=this.head,r=0;t;){if(t.value===e)return r;t=t.next,r++}};qe.prototype.length=function(){return this._length};qe.prototype.isEmpty=function(){return this._length===0};qe.prototype.forEach=function(e,t){for(var r=this.head,i=0,n=typeof t<"u";r;)n?e.call(t,r.value,i):e(r.value,i),r=r.next,i++};qe.prototype.clear=function(){this.tail=this.head=null,this._length=0};qe.Entry=function(e){this.value=e,this.next=null,this.prev=null};var jr=function(e){this._list=new qe,this._map={},this._maxSize=e||10};jr.prototype.setMaxSize=function(e){this._maxSize=e};jr.prototype.put=function(e,t){if(!this._map.hasOwnProperty(e)){var r=this._list.length();if(r>=this._maxSize&&r>0){var i=this._list.head;this._list.remove(i),delete this._map[i.key]}var n=this._list.insert(t);n.key=e,this._map[e]=n}};jr.prototype.get=function(e){var t=this._map[e];if(this._map.hasOwnProperty(e))return t!==this._list.tail&&(this._list.remove(t),this._list.insertEntry(t)),t.value};jr.prototype.remove=function(e){var t=this._map[e];typeof t<"u"&&(delete this._map[e],this._list.remove(t))};jr.prototype.clear=function(){this._list.clear(),this._map={}};var Se={},Il={transparent:[0,0,0,0],aliceblue:[240,248,255,1],antiquewhite:[250,235,215,1],aqua:[0,255,255,1],aquamarine:[127,255,212,1],azure:[240,255,255,1],beige:[245,245,220,1],bisque:[255,228,196,1],black:[0,0,0,1],blanchedalmond:[255,235,205,1],blue:[0,0,255,1],blueviolet:[138,43,226,1],brown:[165,42,42,1],burlywood:[222,184,135,1],cadetblue:[95,158,160,1],chartreuse:[127,255,0,1],chocolate:[210,105,30,1],coral:[255,127,80,1],cornflowerblue:[100,149,237,1],cornsilk:[255,248,220,1],crimson:[220,20,60,1],cyan:[0,255,255,1],darkblue:[0,0,139,1],darkcyan:[0,139,139,1],darkgoldenrod:[184,134,11,1],darkgray:[169,169,169,1],darkgreen:[0,100,0,1],darkgrey:[169,169,169,1],darkkhaki:[189,183,107,1],darkmagenta:[139,0,139,1],darkolivegreen:[85,107,47,1],darkorange:[255,140,0,1],darkorchid:[153,50,204,1],darkred:[139,0,0,1],darksalmon:[233,150,122,1],darkseagreen:[143,188,143,1],darkslateblue:[72,61,139,1],darkslategray:[47,79,79,1],darkslategrey:[47,79,79,1],darkturquoise:[0,206,209,1],darkviolet:[148,0,211,1],deeppink:[255,20,147,1],deepskyblue:[0,191,255,1],dimgray:[105,105,105,1],dimgrey:[105,105,105,1],dodgerblue:[30,144,255,1],firebrick:[178,34,34,1],floralwhite:[255,250,240,1],forestgreen:[34,139,34,1],fuchsia:[255,0,255,1],gainsboro:[220,220,220,1],ghostwhite:[248,248,255,1],gold:[255,215,0,1],goldenrod:[218,165,32,1],gray:[128,128,128,1],green:[0,128,0,1],greenyellow:[173,255,47,1],grey:[128,128,128,1],honeydew:[240,255,240,1],hotpink:[255,105,180,1],indianred:[205,92,92,1],indigo:[75,0,130,1],ivory:[255,255,240,1],khaki:[240,230,140,1],lavender:[230,230,250,1],lavenderblush:[255,240,245,1],lawngreen:[124,252,0,1],lemonchiffon:[255,250,205,1],lightblue:[173,216,230,1],lightcoral:[240,128,128,1],lightcyan:[224,255,255,1],lightgoldenrodyellow:[250,250,210,1],lightgray:[211,211,211,1],lightgreen:[144,238,144,1],lightgrey:[211,211,211,1],lightpink:[255,182,193,1],lightsalmon:[255,160,122,1],lightseagreen:[32,178,170,1],lightskyblue:[135,206,250,1],lightslategray:[119,136,153,1],lightslategrey:[119,136,153,1],lightsteelblue:[176,196,222,1],lightyellow:[255,255,224,1],lime:[0,255,0,1],limegreen:[50,205,50,1],linen:[250,240,230,1],magenta:[255,0,255,1],maroon:[128,0,0,1],mediumaquamarine:[102,205,170,1],mediumblue:[0,0,205,1],mediumorchid:[186,85,211,1],mediumpurple:[147,112,219,1],mediumseagreen:[60,179,113,1],mediumslateblue:[123,104,238,1],mediumspringgreen:[0,250,154,1],mediumturquoise:[72,209,204,1],mediumvioletred:[199,21,133,1],midnightblue:[25,25,112,1],mintcream:[245,255,250,1],mistyrose:[255,228,225,1],moccasin:[255,228,181,1],navajowhite:[255,222,173,1],navy:[0,0,128,1],oldlace:[253,245,230,1],olive:[128,128,0,1],olivedrab:[107,142,35,1],orange:[255,165,0,1],orangered:[255,69,0,1],orchid:[218,112,214,1],palegoldenrod:[238,232,170,1],palegreen:[152,251,152,1],paleturquoise:[175,238,238,1],palevioletred:[219,112,147,1],papayawhip:[255,239,213,1],peachpuff:[255,218,185,1],peru:[205,133,63,1],pink:[255,192,203,1],plum:[221,160,221,1],powderblue:[176,224,230,1],purple:[128,0,128,1],red:[255,0,0,1],rosybrown:[188,143,143,1],royalblue:[65,105,225,1],saddlebrown:[139,69,19,1],salmon:[250,128,114,1],sandybrown:[244,164,96,1],seagreen:[46,139,87,1],seashell:[255,245,238,1],sienna:[160,82,45,1],silver:[192,192,192,1],skyblue:[135,206,235,1],slateblue:[106,90,205,1],slategray:[112,128,144,1],slategrey:[112,128,144,1],snow:[255,250,250,1],springgreen:[0,255,127,1],steelblue:[70,130,180,1],tan:[210,180,140,1],teal:[0,128,128,1],thistle:[216,191,216,1],tomato:[255,99,71,1],turquoise:[64,224,208,1],violet:[238,130,238,1],wheat:[245,222,179,1],white:[255,255,255,1],whitesmoke:[245,245,245,1],yellow:[255,255,0,1],yellowgreen:[154,205,50,1]};function Pt(e){return e=Math.round(e),e<0?0:e>255?255:e}function og(e){return e=Math.round(e),e<0?0:e>360?360:e}function Ji(e){return e<0?0:e>1?1:e}function Fa(e){return e.length&&e.charAt(e.length-1)==="%"?Pt(parseFloat(e)/100*255):Pt(parseInt(e,10))}function vi(e){return e.length&&e.charAt(e.length-1)==="%"?Ji(parseFloat(e)/100):Ji(parseFloat(e))}function Ga(e,t,r){return r<0?r+=1:r>1&&(r-=1),r*6<1?e+(t-e)*r*6:r*2<1?t:r*3<2?e+(t-e)*(2/3-r)*6:e}function vr(e,t,r){return e+(t-e)*r}function Dt(e,t,r,i,n){return e[0]=t,e[1]=r,e[2]=i,e[3]=n,e}function So(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e}var Gh=new jr(20),Dn=null;function $r(e,t){Dn&&So(Dn,t),Dn=Gh.put(e,Dn||t.slice())}Se.parse=function(e,t){if(e){t=t||[];var r=Gh.get(e);if(r)return So(t,r);e=e+"";var i=e.replace(/ /g,"").toLowerCase();if(i in Il)return So(t,Il[i]),$r(e,t),t;if(i.charAt(0)==="#"){if(i.length===4){var n=parseInt(i.substr(1),16);if(!(n>=0&&n<=4095)){Dt(t,0,0,0,1);return}return Dt(t,(n&3840)>>4|(n&3840)>>8,n&240|(n&240)>>4,n&15|(n&15)<<4,1),$r(e,t),t}else if(i.length===7){var n=parseInt(i.substr(1),16);if(!(n>=0&&n<=16777215)){Dt(t,0,0,0,1);return}return Dt(t,(n&16711680)>>16,(n&65280)>>8,n&255,1),$r(e,t),t}return}var a=i.indexOf("("),o=i.indexOf(")");if(a!==-1&&o+1===i.length){var s=i.substr(0,a),l=i.substr(a+1,o-(a+1)).split(","),u=1;switch(s){case"rgba":if(l.length!==4){Dt(t,0,0,0,1);return}u=vi(l.pop());case"rgb":if(l.length!==3){Dt(t,0,0,0,1);return}return Dt(t,Fa(l[0]),Fa(l[1]),Fa(l[2]),u),$r(e,t),t;case"hsla":if(l.length!==4){Dt(t,0,0,0,1);return}return l[3]=vi(l[3]),bo(l,t),$r(e,t),t;case"hsl":if(l.length!==3){Dt(t,0,0,0,1);return}return bo(l,t),$r(e,t),t;default:return}}Dt(t,0,0,0,1)}};Se.parseToFloat=function(e,t){if(t=Se.parse(e,t),!!t)return t[0]/=255,t[1]/=255,t[2]/=255,t};function bo(e,t){var r=(parseFloat(e[0])%360+360)%360/360,i=vi(e[1]),n=vi(e[2]),a=n<=.5?n*(i+1):n+i-n*i,o=n*2-a;return t=t||[],Dt(t,Pt(Ga(o,a,r+1/3)*255),Pt(Ga(o,a,r)*255),Pt(Ga(o,a,r-1/3)*255),1),e.length===4&&(t[3]=e[3]),t}function sg(e){if(e){var t=e[0]/255,r=e[1]/255,i=e[2]/255,n=Math.min(t,r,i),a=Math.max(t,r,i),o=a-n,s=(a+n)/2,l,u;if(o===0)l=0,u=0;else{s<.5?u=o/(a+n):u=o/(2-a-n);var h=((a-t)/6+o/2)/o,f=((a-r)/6+o/2)/o,d=((a-i)/6+o/2)/o;t===a?l=d-f:r===a?l=1/3+h-d:i===a&&(l=2/3+f-h),l<0&&(l+=1),l>1&&(l-=1)}var c=[l*360,u,s];return e[3]!=null&&c.push(e[3]),c}}Se.lift=function(e,t){var r=Se.parse(e);if(r){for(var i=0;i<3;i++)t<0?r[i]=r[i]*(1-t)|0:r[i]=(255-r[i])*t+r[i]|0;return Se.stringify(r,r.length===4?"rgba":"rgb")}};Se.toHex=function(e){var t=Se.parse(e);if(t)return((1<<24)+(t[0]<<16)+(t[1]<<8)+ +t[2]).toString(16).slice(1)};Se.fastLerp=function(e,t,r){if(!(!(t&&t.length)||!(e>=0&&e<=1))){r=r||[];var i=e*(t.length-1),n=Math.floor(i),a=Math.ceil(i),o=t[n],s=t[a],l=i-n;return r[0]=Pt(vr(o[0],s[0],l)),r[1]=Pt(vr(o[1],s[1],l)),r[2]=Pt(vr(o[2],s[2],l)),r[3]=Ji(vr(o[3],s[3],l)),r}};Se.fastMapToColor=Se.fastLerp;Se.lerp=function(e,t,r){if(!(!(t&&t.length)||!(e>=0&&e<=1))){var i=e*(t.length-1),n=Math.floor(i),a=Math.ceil(i),o=Se.parse(t[n]),s=Se.parse(t[a]),l=i-n,u=Se.stringify([Pt(vr(o[0],s[0],l)),Pt(vr(o[1],s[1],l)),Pt(vr(o[2],s[2],l)),Ji(vr(o[3],s[3],l))],"rgba");return r?{color:u,leftIndex:n,rightIndex:a,value:i}:u}};Se.mapToColor=Se.lerp;Se.modifyHSL=function(e,t,r,i){if(e=Se.parse(e),e)return e=sg(e),t!=null&&(e[0]=og(t)),r!=null&&(e[1]=vi(r)),i!=null&&(e[2]=vi(i)),Se.stringify(bo(e),"rgba")};Se.modifyAlpha=function(e,t){if(e=Se.parse(e),e&&t!=null)return e[3]=Ji(t),Se.stringify(e,"rgba")};Se.stringify=function(e,t){if(!(!e||!e.length)){var r=e[0]+","+e[1]+","+e[2];return(t==="rgba"||t==="hsva"||t==="hsla")&&(r+=","+e[3]),t+"("+r+")"}};var lg=Se.parseToFloat,za={};function Rl(e){var t=Object.keys(e);t.sort();for(var r=[],i=0;i<t.length;i++){var n=t[i],a=e[n];a===null?r.push(n):r.push(n+" "+a.toString())}return r.join(`
`)}function ug(e,t,r){r.sort();for(var i=[],n=0;n<r.length;n++){var a=r[n];i.push(a)}var o=Rl(e)+`
`+Rl(t)+`
`+i.join(`
`);if(za[o])return za[o];var s=Pe.genGUID();return za[o]=s,s}var At=Qe.extend(function(){return{name:"",depthTest:!0,depthMask:!0,transparent:!1,blend:null,autoUpdateTextureStatus:!0,uniforms:{},vertexDefines:{},fragmentDefines:{},_textureStatus:{},_enabledUniforms:null}},function(){this.name||(this.name="MATERIAL_"+this.__uid__),this.shader&&this.attachShader(this.shader,!0)},{precision:"highp",setUniform:function(e,t){t===void 0&&console.warn('Uniform value "'+e+'" is undefined');var r=this.uniforms[e];r&&(typeof t=="string"&&(t=lg(t)||t),r.value=t,this.autoUpdateTextureStatus&&r.type==="t"&&(t?this.enableTexture(e):this.disableTexture(e)))},setUniforms:function(e){for(var t in e){var r=e[t];this.setUniform(t,r)}},isUniformEnabled:function(e){return this._enabledUniforms.indexOf(e)>=0},getEnabledUniforms:function(){return this._enabledUniforms},getTextureUniforms:function(){return this._textureUniforms},set:function(e,t){if(typeof e=="object")for(var r in e){var i=e[r];this.setUniform(r,i)}else this.setUniform(e,t)},get:function(e){var t=this.uniforms[e];if(t)return t.value},attachShader:function(e,t){var r=this.uniforms;this.uniforms=e.createUniforms(),this.shader=e;var i=this.uniforms;this._enabledUniforms=Object.keys(i),this._enabledUniforms.sort(),this._textureUniforms=this._enabledUniforms.filter(function(u){var h=this.uniforms[u].type;return h==="t"||h==="tv"},this);var n=this.vertexDefines,a=this.fragmentDefines;if(this.vertexDefines=Pe.clone(e.vertexDefines),this.fragmentDefines=Pe.clone(e.fragmentDefines),t){for(var o in r)i[o]&&(i[o].value=r[o].value);Pe.defaults(this.vertexDefines,n),Pe.defaults(this.fragmentDefines,a)}var s={};for(var l in e.textures)s[l]={shaderType:e.textures[l].shaderType,type:e.textures[l].type,enabled:t&&this._textureStatus[l]?this._textureStatus[l].enabled:!1};this._textureStatus=s,this._programKey=""},clone:function(){var e=new this.constructor({name:this.name,shader:this.shader});for(var t in this.uniforms)e.uniforms[t].value=this.uniforms[t].value;return e.depthTest=this.depthTest,e.depthMask=this.depthMask,e.transparent=this.transparent,e.blend=this.blend,e.vertexDefines=Pe.clone(this.vertexDefines),e.fragmentDefines=Pe.clone(this.fragmentDefines),e.enableTexture(this.getEnabledTextures()),e.precision=this.precision,e},define:function(e,t,r){var i=this.vertexDefines,n=this.fragmentDefines;e!=="vertex"&&e!=="fragment"&&e!=="both"&&arguments.length<3&&(r=t,t=e,e="both"),r=r??null,(e==="vertex"||e==="both")&&i[t]!==r&&(i[t]=r,this._programKey=""),(e==="fragment"||e==="both")&&n[t]!==r&&(n[t]=r,e!=="both"&&(this._programKey=""))},undefine:function(e,t){e!=="vertex"&&e!=="fragment"&&e!=="both"&&arguments.length<2&&(t=e,e="both"),(e==="vertex"||e==="both")&&this.isDefined("vertex",t)&&(delete this.vertexDefines[t],this._programKey=""),(e==="fragment"||e==="both")&&this.isDefined("fragment",t)&&(delete this.fragmentDefines[t],e!=="both"&&(this._programKey=""))},isDefined:function(e,t){switch(e){case"vertex":return this.vertexDefines[t]!==void 0;case"fragment":return this.fragmentDefines[t]!==void 0}},getDefine:function(e,t){switch(e){case"vertex":return this.vertexDefines[t];case"fragment":return this.fragmentDefines[t]}},enableTexture:function(e){if(Array.isArray(e)){for(var t=0;t<e.length;t++)this.enableTexture(e[t]);return}var r=this._textureStatus[e];if(r){var i=r.enabled;i||(r.enabled=!0,this._programKey="")}},enableTexturesAll:function(){var e=this._textureStatus;for(var t in e)e[t].enabled=!0;this._programKey=""},disableTexture:function(e){if(Array.isArray(e)){for(var t=0;t<e.length;t++)this.disableTexture(e[t]);return}var r=this._textureStatus[e];if(r){var i=!r.enabled;i||(r.enabled=!1,this._programKey="")}},disableTexturesAll:function(){var e=this._textureStatus;for(var t in e)e[t].enabled=!1;this._programKey=""},isTextureEnabled:function(e){var t=this._textureStatus;return!!t[e]&&t[e].enabled},getEnabledTextures:function(){var e=[],t=this._textureStatus;for(var r in t)t[r].enabled&&e.push(r);return e},dirtyDefines:function(){this._programKey=""},getProgramKey:function(){return this._programKey||(this._programKey=ug(this.vertexDefines,this.fragmentDefines,this.getEnabledTextures())),this._programKey}}),Xn=1e-6,et=Array,si=Math.random,U={};U.create=function(){var e=new et(2);return e[0]=0,e[1]=0,e};U.clone=function(e){var t=new et(2);return t[0]=e[0],t[1]=e[1],t};U.fromValues=function(e,t){var r=new et(2);return r[0]=e,r[1]=t,r};U.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e};U.set=function(e,t,r){return e[0]=t,e[1]=r,e};U.add=function(e,t,r){return e[0]=t[0]+r[0],e[1]=t[1]+r[1],e};U.subtract=function(e,t,r){return e[0]=t[0]-r[0],e[1]=t[1]-r[1],e};U.sub=U.subtract;U.multiply=function(e,t,r){return e[0]=t[0]*r[0],e[1]=t[1]*r[1],e};U.mul=U.multiply;U.divide=function(e,t,r){return e[0]=t[0]/r[0],e[1]=t[1]/r[1],e};U.div=U.divide;U.min=function(e,t,r){return e[0]=Math.min(t[0],r[0]),e[1]=Math.min(t[1],r[1]),e};U.max=function(e,t,r){return e[0]=Math.max(t[0],r[0]),e[1]=Math.max(t[1],r[1]),e};U.scale=function(e,t,r){return e[0]=t[0]*r,e[1]=t[1]*r,e};U.scaleAndAdd=function(e,t,r,i){return e[0]=t[0]+r[0]*i,e[1]=t[1]+r[1]*i,e};U.distance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1];return Math.sqrt(r*r+i*i)};U.dist=U.distance;U.squaredDistance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1];return r*r+i*i};U.sqrDist=U.squaredDistance;U.length=function(e){var t=e[0],r=e[1];return Math.sqrt(t*t+r*r)};U.len=U.length;U.squaredLength=function(e){var t=e[0],r=e[1];return t*t+r*r};U.sqrLen=U.squaredLength;U.negate=function(e,t){return e[0]=-t[0],e[1]=-t[1],e};U.inverse=function(e,t){return e[0]=1/t[0],e[1]=1/t[1],e};U.normalize=function(e,t){var r=t[0],i=t[1],n=r*r+i*i;return n>0&&(n=1/Math.sqrt(n),e[0]=t[0]*n,e[1]=t[1]*n),e};U.dot=function(e,t){return e[0]*t[0]+e[1]*t[1]};U.cross=function(e,t,r){var i=t[0]*r[1]-t[1]*r[0];return e[0]=e[1]=0,e[2]=i,e};U.lerp=function(e,t,r,i){var n=t[0],a=t[1];return e[0]=n+i*(r[0]-n),e[1]=a+i*(r[1]-a),e};U.random=function(e,t){t=t||1;var r=GLMAT_RANDOM()*2*Math.PI;return e[0]=Math.cos(r)*t,e[1]=Math.sin(r)*t,e};U.transformMat2=function(e,t,r){var i=t[0],n=t[1];return e[0]=r[0]*i+r[2]*n,e[1]=r[1]*i+r[3]*n,e};U.transformMat2d=function(e,t,r){var i=t[0],n=t[1];return e[0]=r[0]*i+r[2]*n+r[4],e[1]=r[1]*i+r[3]*n+r[5],e};U.transformMat3=function(e,t,r){var i=t[0],n=t[1];return e[0]=r[0]*i+r[3]*n+r[6],e[1]=r[1]*i+r[4]*n+r[7],e};U.transformMat4=function(e,t,r){var i=t[0],n=t[1];return e[0]=r[0]*i+r[4]*n+r[12],e[1]=r[1]*i+r[5]*n+r[13],e};U.forEach=function(){var e=U.create();return function(t,r,i,n,a,o){var s,l;for(r||(r=2),i||(i=0),n?l=Math.min(n*r+i,t.length):l=t.length,s=i;s<l;s+=r)e[0]=t[s],e[1]=t[s+1],a(e,e,o),t[s]=e[0],t[s+1]=e[1];return t}}();var te=function(e,t){e=e||0,t=t||0,this.array=U.fromValues(e,t),this._dirty=!0};te.prototype={constructor:te,add:function(e){return U.add(this.array,this.array,e.array),this._dirty=!0,this},set:function(e,t){return this.array[0]=e,this.array[1]=t,this._dirty=!0,this},setArray:function(e){return this.array[0]=e[0],this.array[1]=e[1],this._dirty=!0,this},clone:function(){return new te(this.x,this.y)},copy:function(e){return U.copy(this.array,e.array),this._dirty=!0,this},cross:function(e,t){return U.cross(e.array,this.array,t.array),e._dirty=!0,this},dist:function(e){return U.dist(this.array,e.array)},distance:function(e){return U.distance(this.array,e.array)},div:function(e){return U.div(this.array,this.array,e.array),this._dirty=!0,this},divide:function(e){return U.divide(this.array,this.array,e.array),this._dirty=!0,this},dot:function(e){return U.dot(this.array,e.array)},len:function(){return U.len(this.array)},length:function(){return U.length(this.array)},lerp:function(e,t,r){return U.lerp(this.array,e.array,t.array,r),this._dirty=!0,this},min:function(e){return U.min(this.array,this.array,e.array),this._dirty=!0,this},max:function(e){return U.max(this.array,this.array,e.array),this._dirty=!0,this},mul:function(e){return U.mul(this.array,this.array,e.array),this._dirty=!0,this},multiply:function(e){return U.multiply(this.array,this.array,e.array),this._dirty=!0,this},negate:function(){return U.negate(this.array,this.array),this._dirty=!0,this},normalize:function(){return U.normalize(this.array,this.array),this._dirty=!0,this},random:function(e){return U.random(this.array,e),this._dirty=!0,this},scale:function(e){return U.scale(this.array,this.array,e),this._dirty=!0,this},scaleAndAdd:function(e,t){return U.scaleAndAdd(this.array,this.array,e.array,t),this._dirty=!0,this},sqrDist:function(e){return U.sqrDist(this.array,e.array)},squaredDistance:function(e){return U.squaredDistance(this.array,e.array)},sqrLen:function(){return U.sqrLen(this.array)},squaredLength:function(){return U.squaredLength(this.array)},sub:function(e){return U.sub(this.array,this.array,e.array),this._dirty=!0,this},subtract:function(e){return U.subtract(this.array,this.array,e.array),this._dirty=!0,this},transformMat2:function(e){return U.transformMat2(this.array,this.array,e.array),this._dirty=!0,this},transformMat2d:function(e){return U.transformMat2d(this.array,this.array,e.array),this._dirty=!0,this},transformMat3:function(e){return U.transformMat3(this.array,this.array,e.array),this._dirty=!0,this},transformMat4:function(e){return U.transformMat4(this.array,this.array,e.array),this._dirty=!0,this},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};if(Object.defineProperty){var Ol=te.prototype;Object.defineProperty(Ol,"x",{get:function(){return this.array[0]},set:function(e){this.array[0]=e,this._dirty=!0}}),Object.defineProperty(Ol,"y",{get:function(){return this.array[1]},set:function(e){this.array[1]=e,this._dirty=!0}})}te.add=function(e,t,r){return U.add(e.array,t.array,r.array),e._dirty=!0,e};te.set=function(e,t,r){return U.set(e.array,t,r),e._dirty=!0,e};te.copy=function(e,t){return U.copy(e.array,t.array),e._dirty=!0,e};te.cross=function(e,t,r){return U.cross(e.array,t.array,r.array),e._dirty=!0,e};te.dist=function(e,t){return U.distance(e.array,t.array)};te.distance=te.dist;te.div=function(e,t,r){return U.divide(e.array,t.array,r.array),e._dirty=!0,e};te.divide=te.div;te.dot=function(e,t){return U.dot(e.array,t.array)};te.len=function(e){return U.length(e.array)};te.lerp=function(e,t,r,i){return U.lerp(e.array,t.array,r.array,i),e._dirty=!0,e};te.min=function(e,t,r){return U.min(e.array,t.array,r.array),e._dirty=!0,e};te.max=function(e,t,r){return U.max(e.array,t.array,r.array),e._dirty=!0,e};te.mul=function(e,t,r){return U.multiply(e.array,t.array,r.array),e._dirty=!0,e};te.multiply=te.mul;te.negate=function(e,t){return U.negate(e.array,t.array),e._dirty=!0,e};te.normalize=function(e,t){return U.normalize(e.array,t.array),e._dirty=!0,e};te.random=function(e,t){return U.random(e.array,t),e._dirty=!0,e};te.scale=function(e,t,r){return U.scale(e.array,t.array,r),e._dirty=!0,e};te.scaleAndAdd=function(e,t,r,i){return U.scaleAndAdd(e.array,t.array,r.array,i),e._dirty=!0,e};te.sqrDist=function(e,t){return U.sqrDist(e.array,t.array)};te.squaredDistance=te.sqrDist;te.sqrLen=function(e){return U.sqrLen(e.array)};te.squaredLength=te.sqrLen;te.sub=function(e,t,r){return U.subtract(e.array,t.array,r.array),e._dirty=!0,e};te.subtract=te.sub;te.transformMat2=function(e,t,r){return U.transformMat2(e.array,t.array,r.array),e._dirty=!0,e};te.transformMat2d=function(e,t,r){return U.transformMat2d(e.array,t.array,r.array),e._dirty=!0,e};te.transformMat3=function(e,t,r){return U.transformMat3(e.array,t.array,r.array),e._dirty=!0,e};te.transformMat4=function(e,t,r){return U.transformMat4(e.array,t.array,r.array),e._dirty=!0,e};var Bl=1,Fl=2,Ua=3,Gl={};function hg(e){for(var t=e.split(`
`),r=0,i=t.length;r<i;r++)t[r]=r+1+": "+t[r];return t.join(`
`)}function zl(e,t,r){if(!e.getShaderParameter(t,e.COMPILE_STATUS))return[e.getShaderInfoLog(t),hg(r)].join(`
`)}var Ul=new de.Float32Array(16),fg=Qe.extend({uniformSemantics:{},attributes:{}},function(){this._locations={},this._textureSlot=0,this._program=null},{bind:function(e){this._textureSlot=0,e.gl.useProgram(this._program)},hasUniform:function(e){var t=this._locations[e];return t!=null},useTextureSlot:function(e,t,r){t&&(e.gl.activeTexture(e.gl.TEXTURE0+r),t.isRenderable()?t.bind(e):t.unbind(e))},currentTextureSlot:function(){return this._textureSlot},resetTextureSlot:function(e){this._textureSlot=e||0},takeCurrentTextureSlot:function(e,t){var r=this._textureSlot;return this.useTextureSlot(e,t,r),this._textureSlot++,r},setUniform:function(e,t,r,i){var n=this._locations,a=n[r];if(a==null)return!1;switch(t){case"m4":if(!(i instanceof Float32Array)){for(var o=0;o<i.length;o++)Ul[o]=i[o];i=Ul}e.uniformMatrix4fv(a,!1,i);break;case"2i":e.uniform2i(a,i[0],i[1]);break;case"2f":e.uniform2f(a,i[0],i[1]);break;case"3i":e.uniform3i(a,i[0],i[1],i[2]);break;case"3f":e.uniform3f(a,i[0],i[1],i[2]);break;case"4i":e.uniform4i(a,i[0],i[1],i[2],i[3]);break;case"4f":e.uniform4f(a,i[0],i[1],i[2],i[3]);break;case"1i":e.uniform1i(a,i);break;case"1f":e.uniform1f(a,i);break;case"1fv":e.uniform1fv(a,i);break;case"1iv":e.uniform1iv(a,i);break;case"2iv":e.uniform2iv(a,i);break;case"2fv":e.uniform2fv(a,i);break;case"3iv":e.uniform3iv(a,i);break;case"3fv":e.uniform3fv(a,i);break;case"4iv":e.uniform4iv(a,i);break;case"4fv":e.uniform4fv(a,i);break;case"m2":case"m2v":e.uniformMatrix2fv(a,!1,i);break;case"m3":case"m3v":e.uniformMatrix3fv(a,!1,i);break;case"m4v":if(Array.isArray(i)&&Array.isArray(i[0])){for(var s=new de.Float32Array(i.length*16),l=0,o=0;o<i.length;o++)for(var u=i[o],h=0;h<16;h++)s[l++]=u[h];e.uniformMatrix4fv(a,!1,s)}else e.uniformMatrix4fv(a,!1,i);break}return!0},setUniformOfSemantic:function(e,t,r){var i=this.uniformSemantics[t];return i?this.setUniform(e,i.type,i.symbol,r):!1},enableAttributes:function(e,t,r){var i=e.gl,n=this._program,a=this._locations,o;r?o=r.__enabledAttributeList:o=Gl[e.__uid__],o||(r?o=r.__enabledAttributeList=[]:o=Gl[e.__uid__]=[]);for(var s=[],l=0;l<t.length;l++){var u=t[l];if(!this.attributes[u]){s[l]=-1;continue}var h=a[u];if(h==null){if(h=i.getAttribLocation(n,u),h===-1){s[l]=-1;continue}a[u]=h}s[l]=h,o[h]?o[h]=Fl:o[h]=Bl}for(var l=0;l<o.length;l++)switch(o[l]){case Bl:i.enableVertexAttribArray(l),o[l]=Ua;break;case Fl:o[l]=Ua;break;case Ua:i.disableVertexAttribArray(l),o[l]=0;break}return s},getAttribLocation:function(e,t){var r=this._locations,i=r[t];return i==null&&(i=e.getAttribLocation(this._program,t),r[t]=i),i},buildProgram:function(e,t,r,i){var n=e.createShader(e.VERTEX_SHADER),a=e.createProgram();e.shaderSource(n,r),e.compileShader(n);var o=e.createShader(e.FRAGMENT_SHADER);e.shaderSource(o,i),e.compileShader(o);var s=zl(e,n,r);if(s||(s=zl(e,o,i),s))return s;if(e.attachShader(a,n),e.attachShader(a,o),t.attributeSemantics.POSITION)e.bindAttribLocation(a,0,t.attributeSemantics.POSITION.symbol);else{var l=Object.keys(this.attributes);e.bindAttribLocation(a,0,l[0])}if(e.linkProgram(a),e.deleteShader(n),e.deleteShader(o),this._program=a,this.vertexCode=r,this.fragmentCode=i,!e.getProgramParameter(a,e.LINK_STATUS))return`Could not link program
`+e.getProgramInfoLog(a);for(var u=0;u<t.uniforms.length;u++){var h=t.uniforms[u];this._locations[h]=e.getUniformLocation(a,h)}}}),cg=/for\s*?\(int\s*?_idx_\s*\=\s*([\w-]+)\;\s*_idx_\s*<\s*([\w-]+);\s*_idx_\s*\+\+\s*\)\s*\{\{([\s\S]+?)(?=\}\})\}\}/g;function Vl(e,t,r){function i(o,s,l,u){var h="";isNaN(s)&&(s in t?s=t[s]:s=n[s]),isNaN(l)&&(l in t?l=t[l]:l=n[l]);for(var f=parseInt(s);f<parseInt(l);f++)h+="{"+u.replace(/float\s*\(\s*_idx_\s*\)/g,f.toFixed(1)).replace(/_idx_/g,f)+"}";return h}var n={};for(var a in r)n[a+"_COUNT"]=r[a];return e.replace(cg,i)}function Va(e,t,r){var i=[];if(t)for(var n in t){var a=t[n];a>0&&i.push("#define "+n.toUpperCase()+"_COUNT "+a)}if(r)for(var o=0;o<r.length;o++){var s=r[o];i.push("#define "+s.toUpperCase()+"_ENABLED")}for(var s in e){var l=e[s];l===null?i.push("#define "+s):i.push("#define "+s+" "+l.toString())}return i.join(`
`)}function dg(e){for(var t=[],r=0;r<e.length;r++)t.push("#extension GL_"+e[r]+" : enable");return t.join(`
`)}function vg(e){return["precision",e,"float"].join(" ")+`;
`+["precision",e,"int"].join(" ")+`;
`+["precision",e,"sampler2D"].join(" ")+`;
`}function zh(e){this._renderer=e,this._cache={}}zh.prototype.getProgram=function(e,t,r){var i=this._cache,n=e.isSkinnedMesh&&e.isSkinnedMesh(),a=e.isInstancedMesh&&e.isInstancedMesh(),o="s"+t.shader.shaderID+"m"+t.getProgramKey();r&&(o+="se"+r.getProgramKey(e.lightGroup)),n&&(o+=",sk"+e.joints.length),a&&(o+=",is");var x=i[o];if(x)return x;var s=r?r.getLightsNumbers(e.lightGroup):{},l=this._renderer,u=l.gl,h=t.getEnabledTextures(),f="";if(n){var d={SKINNING:null,JOINT_COUNT:e.joints.length};e.joints.length>l.getMaxJointNumber()&&(d.USE_SKIN_MATRICES_TEXTURE=null),f+=`
`+Va(d)+`
`}a&&(f+=`
#define INSTANCING
`);var c=f+Va(t.vertexDefines,s,h),v=f+Va(t.fragmentDefines,s,h),p=c+`
`+t.shader.vertex,_=["OES_standard_derivatives","EXT_shader_texture_lod"].filter(function(T){return l.getGLExtension(T)!=null});_.indexOf("EXT_shader_texture_lod")>=0&&(v+=`
#define SUPPORT_TEXTURE_LOD`),_.indexOf("OES_standard_derivatives")>=0&&(v+=`
#define SUPPORT_STANDARD_DERIVATIVES`);var m=dg(_)+`
`+vg(t.precision)+`
`+v+`
`+t.shader.fragment,g=Vl(p,t.vertexDefines,s),y=Vl(m,t.fragmentDefines,s),x=new fg;x.uniformSemantics=t.shader.uniformSemantics,x.attributes=t.shader.attributes;var w=x.buildProgram(u,t.shader,g,y);return x.__error=w,i[o]=x,x};var Hl=/uniform\s+(bool|float|int|vec2|vec3|vec4|ivec2|ivec3|ivec4|mat2|mat3|mat4|sampler2D|samplerCube)\s+([\s\S]*?);/g,pg=/attribute\s+(float|int|vec2|vec3|vec4)\s+([\s\S]*?);/g,kl=/#define\s+(\w+)?(\s+[\d-.]+)?\s*;?\s*\n/g,gg={bool:"1i",int:"1i",sampler2D:"t",samplerCube:"t",float:"1f",vec2:"2f",vec3:"3f",vec4:"4f",ivec2:"2i",ivec3:"3i",ivec4:"4i",mat2:"m2",mat3:"m3",mat4:"m4"};function Wt(e){for(var t=[],r=0;r<e;r++)t[r]=0;return t}var Wl={bool:function(){return!0},int:function(){return 0},float:function(){return 0},sampler2D:function(){return null},samplerCube:function(){return null},vec2:function(){return Wt(2)},vec3:function(){return Wt(3)},vec4:function(){return Wt(4)},ivec2:function(){return Wt(2)},ivec3:function(){return Wt(3)},ivec4:function(){return Wt(4)},mat2:function(){return Wt(4)},mat3:function(){return Wt(9)},mat4:function(){return Wt(16)},array:function(){return[]}},Ao=["POSITION","NORMAL","BINORMAL","TANGENT","TEXCOORD","TEXCOORD_0","TEXCOORD_1","COLOR","JOINT","WEIGHT"],Uh=["SKIN_MATRIX","VIEWPORT_SIZE","VIEWPORT","DEVICEPIXELRATIO","WINDOW_SIZE","NEAR","FAR","TIME"],Vh=["WORLD","VIEW","PROJECTION","WORLDVIEW","VIEWPROJECTION","WORLDVIEWPROJECTION","WORLDINVERSE","VIEWINVERSE","PROJECTIONINVERSE","WORLDVIEWINVERSE","VIEWPROJECTIONINVERSE","WORLDVIEWPROJECTIONINVERSE","WORLDTRANSPOSE","VIEWTRANSPOSE","PROJECTIONTRANSPOSE","WORLDVIEWTRANSPOSE","VIEWPROJECTIONTRANSPOSE","WORLDVIEWPROJECTIONTRANSPOSE","WORLDINVERSETRANSPOSE","VIEWINVERSETRANSPOSE","PROJECTIONINVERSETRANSPOSE","WORLDVIEWINVERSETRANSPOSE","VIEWPROJECTIONINVERSETRANSPOSE","WORLDVIEWPROJECTIONINVERSETRANSPOSE"],mg={vec4:4,vec3:3,vec2:2,float:1},Ha={},Hh={};function _g(e,t){var r="vertex:"+e+"fragment:"+t;if(Ha[r])return Ha[r];var i=Pe.genGUID();return Ha[r]=i,Hh[i]={vertex:e,fragment:t},i}function Xl(e){return e.replace(/[ \t]*\/\/.*\n/g,"").replace(/[ \t]*\/\*[\s\S]*?\*\//g,"")}function Kr(){console.error("Wrong uniform/attributes syntax")}function jl(e,t){for(var r=/[,=\(\):]/,i=t.replace(/:\s*\[\s*(.*)\s*\]/g,"="+e+"($1)").replace(/\s+/g,"").split(/(?=[,=\(\):])/g),n=[],a=0;a<i.length;a++)i[a].match(r)?n.push(i[a].charAt(0),i[a].slice(1)):n.push(i[a]);i=n;var o=0,s=1,l=2,u=3,h=4,f=5,d=o,c={},v=null,p;_(i[0]);function _(y){y||Kr();var x=y.match(/\[(.*?)\]/);p=y.replace(/\[(.*?)\]/,""),c[p]={},x&&(c[p].isArray=!0,c[p].arraySize=x[1])}for(var a=1;a<i.length;a++){var m=i[a];if(m){if(m==="="){if(d!==o&&d!==u){Kr();break}d=s;continue}else if(m===":"){d=h;continue}else if(m===","){if(d===l){if(!(v instanceof Array)){Kr();break}v.push(+i[++a])}else d=f;continue}else if(m===")"){c[p].value=new de.Float32Array(v),v=null,d=f;continue}else if(m==="("){if(d!==l){Kr();break}if(!(v instanceof Array)){Kr();break}v.push(+i[++a]);continue}else if(m.indexOf("vec")>=0){if(d!==s&&d!==h){Kr();break}d=l,v=[];continue}else if(d===s){e==="bool"?c[p].value=m==="true":c[p].value=parseFloat(m),v=null;continue}else if(d===h){var g=m;Ao.indexOf(g)>=0||Uh.indexOf(g)>=0||Vh.indexOf(g)>=0?c[p].semantic=g:g==="ignore"||g==="unconfigurable"?c[p].ignore=!0:e==="bool"?c[p].value=g==="true":c[p].value=parseFloat(g);continue}_(m),d=o}}return c}function k(e,t){typeof e=="object"&&(t=e.fragment,e=e.vertex),e=Xl(e),t=Xl(t),this._shaderID=_g(e,t),this._vertexCode=k.parseImport(e),this._fragmentCode=k.parseImport(t),this.attributeSemantics={},this.matrixSemantics={},this.uniformSemantics={},this.matrixSemanticKeys=[],this.uniformTemplates={},this.attributes={},this.textures={},this.vertexDefines={},this.fragmentDefines={},this._parseAttributes(),this._parseUniforms(),this._parseDefines()}k.prototype={constructor:k,createUniforms:function(){var e={};for(var t in this.uniformTemplates){var r=this.uniformTemplates[t];e[t]={type:r.type,value:r.value()}}return e},_parseImport:function(){this._vertexCode=k.parseImport(this.vertex),this._fragmentCode=k.parseImport(this.fragment)},_addSemanticUniform:function(e,t,r){if(Ao.indexOf(r)>=0)this.attributeSemantics[r]={symbol:e,type:t};else if(Vh.indexOf(r)>=0){var i=!1,n=r;r.match(/TRANSPOSE$/)&&(i=!0,n=r.slice(0,-9)),this.matrixSemantics[r]={symbol:e,type:t,isTranspose:i,semanticNoTranspose:n}}else Uh.indexOf(r)>=0&&(this.uniformSemantics[r]={symbol:e,type:t})},_addMaterialUniform:function(e,t,r,i,n,a){a[e]={type:r,value:n?Wl.array:i||Wl[t],semantic:null}},_parseUniforms:function(){var e={},t=this,r="vertex";this._uniformList=[],this._vertexCode=this._vertexCode.replace(Hl,n),r="fragment",this._fragmentCode=this._fragmentCode.replace(Hl,n),t.matrixSemanticKeys=Object.keys(this.matrixSemantics);function i(a){return a!=null?function(){return a}:null}function n(a,o,s){var l=jl(o,s),u=[];for(var h in l){var f=l[h],d=f.semantic,c=h,v=gg[o],p=i(l[h].value);l[h].isArray&&(c+="["+l[h].arraySize+"]",v+="v"),u.push(c),t._uniformList.push(h),f.ignore||((o==="sampler2D"||o==="samplerCube")&&(t.textures[h]={shaderType:r,type:o}),d?t._addSemanticUniform(h,v,d):t._addMaterialUniform(h,o,v,p,l[h].isArray,e))}return u.length>0?"uniform "+o+" "+u.join(",")+`;
`:""}this.uniformTemplates=e},_parseAttributes:function(){var e={},t=this;this._vertexCode=this._vertexCode.replace(pg,r);function r(i,n,a){var o=jl(n,a),s=mg[n]||1,l=[];for(var u in o){var h=o[u].semantic;if(e[u]={type:"float",size:s,semantic:h||null},h){if(Ao.indexOf(h)<0)throw new Error('Unkown semantic "'+h+'"');t.attributeSemantics[h]={symbol:u,type:n}}l.push(u)}return"attribute "+n+" "+l.join(",")+`;
`}this.attributes=e},_parseDefines:function(){var e=this,t="vertex";this._vertexCode=this._vertexCode.replace(kl,r),t="fragment",this._fragmentCode=this._fragmentCode.replace(kl,r);function r(i,n,a){var o=t==="vertex"?e.vertexDefines:e.fragmentDefines;return o[n]||(a==="false"?o[n]=!1:a==="true"?o[n]=!0:o[n]=a?isNaN(parseFloat(a))?a.trim():parseFloat(a):null),""}},clone:function(){var e=Hh[this._shaderID],t=new k(e.vertex,e.fragment);return t}};Object.defineProperty&&(Object.defineProperty(k.prototype,"shaderID",{get:function(){return this._shaderID}}),Object.defineProperty(k.prototype,"vertex",{get:function(){return this._vertexCode}}),Object.defineProperty(k.prototype,"fragment",{get:function(){return this._fragmentCode}}),Object.defineProperty(k.prototype,"uniforms",{get:function(){return this._uniformList}}));var yg=/(@import)\s*([0-9a-zA-Z_\-\.]*)/g;k.parseImport=function(e){return e=e.replace(yg,function(n,r,i){var n=k.source(i);return n?k.parseImport(n):(console.error('Shader chunk "'+i+'" not existed in library'),"")}),e};var xg=/(@export)\s*([0-9a-zA-Z_\-\.]*)\s*\n([\s\S]*?)@end/g;k.import=function(e){e.replace(xg,function(t,r,i,a){var a=a.replace(/(^[\s\t\xa0\u3000]+)|([\u3000\xa0\s\t]+\x24)/g,"");if(a){for(var o=i.split("."),s=k.codes,l=0,u;l<o.length-1;)u=o[l++],s[u]||(s[u]={}),s=s[u];u=o[l],s[u]=a}return a})};k.codes={};k.source=function(e){for(var t=e.split("."),r=k.codes,i=0;r&&i<t.length;){var n=t[i++];r=r[n]}return typeof r!="string"?(console.error('Shader "'+e+'" not existed in library'),""):r};const kh=`@export clay.prez.vertex
uniform mat4 WVP : WORLDVIEWPROJECTION;
attribute vec3 pos : POSITION;
attribute vec2 uv : TEXCOORD_0;
uniform vec2 uvRepeat : [1.0, 1.0];
uniform vec2 uvOffset : [0.0, 0.0];
@import clay.chunk.skinning_header
@import clay.chunk.instancing_header
varying vec2 v_Texcoord;
void main()
{
 vec4 P = vec4(pos, 1.0);
#ifdef SKINNING
 @import clay.chunk.skin_matrix
 P = skinMatrixWS * P;
#endif
#ifdef INSTANCING
 @import clay.chunk.instancing_matrix
 P = instanceMat * P;
#endif
 gl_Position = WVP * P;
 v_Texcoord = uv * uvRepeat + uvOffset;
}
@end
@export clay.prez.fragment
uniform sampler2D alphaMap;
uniform float alphaCutoff: 0.0;
varying vec2 v_Texcoord;
void main()
{
 if (alphaCutoff > 0.0) {
 if (texture2D(alphaMap, v_Texcoord).a <= alphaCutoff) {
 discard;
 }
 }
 gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
@end`;var z={};z.create=function(){var e=new et(16);return e[0]=1,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=1,e[6]=0,e[7]=0,e[8]=0,e[9]=0,e[10]=1,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,e};z.clone=function(e){var t=new et(16);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3],t[4]=e[4],t[5]=e[5],t[6]=e[6],t[7]=e[7],t[8]=e[8],t[9]=e[9],t[10]=e[10],t[11]=e[11],t[12]=e[12],t[13]=e[13],t[14]=e[14],t[15]=e[15],t};z.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e[4]=t[4],e[5]=t[5],e[6]=t[6],e[7]=t[7],e[8]=t[8],e[9]=t[9],e[10]=t[10],e[11]=t[11],e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15],e};z.identity=function(e){return e[0]=1,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=1,e[6]=0,e[7]=0,e[8]=0,e[9]=0,e[10]=1,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,e};z.transpose=function(e,t){if(e===t){var r=t[1],i=t[2],n=t[3],a=t[6],o=t[7],s=t[11];e[1]=t[4],e[2]=t[8],e[3]=t[12],e[4]=r,e[6]=t[9],e[7]=t[13],e[8]=i,e[9]=a,e[11]=t[14],e[12]=n,e[13]=o,e[14]=s}else e[0]=t[0],e[1]=t[4],e[2]=t[8],e[3]=t[12],e[4]=t[1],e[5]=t[5],e[6]=t[9],e[7]=t[13],e[8]=t[2],e[9]=t[6],e[10]=t[10],e[11]=t[14],e[12]=t[3],e[13]=t[7],e[14]=t[11],e[15]=t[15];return e};z.invert=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=t[6],u=t[7],h=t[8],f=t[9],d=t[10],c=t[11],v=t[12],p=t[13],_=t[14],m=t[15],g=r*s-i*o,y=r*l-n*o,x=r*u-a*o,w=i*l-n*s,T=i*u-a*s,b=n*u-a*l,A=h*p-f*v,C=h*_-d*v,D=h*m-c*v,L=f*_-d*p,M=f*m-c*p,P=d*m-c*_,N=g*P-y*M+x*L+w*D-T*C+b*A;return N?(N=1/N,e[0]=(s*P-l*M+u*L)*N,e[1]=(n*M-i*P-a*L)*N,e[2]=(p*b-_*T+m*w)*N,e[3]=(d*T-f*b-c*w)*N,e[4]=(l*D-o*P-u*C)*N,e[5]=(r*P-n*D+a*C)*N,e[6]=(_*x-v*b-m*y)*N,e[7]=(h*b-d*x+c*y)*N,e[8]=(o*M-s*D+u*A)*N,e[9]=(i*D-r*M-a*A)*N,e[10]=(v*T-p*x+m*g)*N,e[11]=(f*x-h*T-c*g)*N,e[12]=(s*C-o*L-l*A)*N,e[13]=(r*L-i*C+n*A)*N,e[14]=(p*y-v*w-_*g)*N,e[15]=(h*w-f*y+d*g)*N,e):null};z.adjoint=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=t[6],u=t[7],h=t[8],f=t[9],d=t[10],c=t[11],v=t[12],p=t[13],_=t[14],m=t[15];return e[0]=s*(d*m-c*_)-f*(l*m-u*_)+p*(l*c-u*d),e[1]=-(i*(d*m-c*_)-f*(n*m-a*_)+p*(n*c-a*d)),e[2]=i*(l*m-u*_)-s*(n*m-a*_)+p*(n*u-a*l),e[3]=-(i*(l*c-u*d)-s*(n*c-a*d)+f*(n*u-a*l)),e[4]=-(o*(d*m-c*_)-h*(l*m-u*_)+v*(l*c-u*d)),e[5]=r*(d*m-c*_)-h*(n*m-a*_)+v*(n*c-a*d),e[6]=-(r*(l*m-u*_)-o*(n*m-a*_)+v*(n*u-a*l)),e[7]=r*(l*c-u*d)-o*(n*c-a*d)+h*(n*u-a*l),e[8]=o*(f*m-c*p)-h*(s*m-u*p)+v*(s*c-u*f),e[9]=-(r*(f*m-c*p)-h*(i*m-a*p)+v*(i*c-a*f)),e[10]=r*(s*m-u*p)-o*(i*m-a*p)+v*(i*u-a*s),e[11]=-(r*(s*c-u*f)-o*(i*c-a*f)+h*(i*u-a*s)),e[12]=-(o*(f*_-d*p)-h*(s*_-l*p)+v*(s*d-l*f)),e[13]=r*(f*_-d*p)-h*(i*_-n*p)+v*(i*d-n*f),e[14]=-(r*(s*_-l*p)-o*(i*_-n*p)+v*(i*l-n*s)),e[15]=r*(s*d-l*f)-o*(i*d-n*f)+h*(i*l-n*s),e};z.determinant=function(e){var t=e[0],r=e[1],i=e[2],n=e[3],a=e[4],o=e[5],s=e[6],l=e[7],u=e[8],h=e[9],f=e[10],d=e[11],c=e[12],v=e[13],p=e[14],_=e[15],m=t*o-r*a,g=t*s-i*a,y=t*l-n*a,x=r*s-i*o,w=r*l-n*o,T=i*l-n*s,b=u*v-h*c,A=u*p-f*c,C=u*_-d*c,D=h*p-f*v,L=h*_-d*v,M=f*_-d*p;return m*M-g*L+y*D+x*C-w*A+T*b};z.multiply=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=t[6],h=t[7],f=t[8],d=t[9],c=t[10],v=t[11],p=t[12],_=t[13],m=t[14],g=t[15],y=r[0],x=r[1],w=r[2],T=r[3];return e[0]=y*i+x*s+w*f+T*p,e[1]=y*n+x*l+w*d+T*_,e[2]=y*a+x*u+w*c+T*m,e[3]=y*o+x*h+w*v+T*g,y=r[4],x=r[5],w=r[6],T=r[7],e[4]=y*i+x*s+w*f+T*p,e[5]=y*n+x*l+w*d+T*_,e[6]=y*a+x*u+w*c+T*m,e[7]=y*o+x*h+w*v+T*g,y=r[8],x=r[9],w=r[10],T=r[11],e[8]=y*i+x*s+w*f+T*p,e[9]=y*n+x*l+w*d+T*_,e[10]=y*a+x*u+w*c+T*m,e[11]=y*o+x*h+w*v+T*g,y=r[12],x=r[13],w=r[14],T=r[15],e[12]=y*i+x*s+w*f+T*p,e[13]=y*n+x*l+w*d+T*_,e[14]=y*a+x*u+w*c+T*m,e[15]=y*o+x*h+w*v+T*g,e};z.multiplyAffine=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[4],s=t[5],l=t[6],u=t[8],h=t[9],f=t[10],d=t[12],c=t[13],v=t[14],p=r[0],_=r[1],m=r[2];return e[0]=p*i+_*o+m*u,e[1]=p*n+_*s+m*h,e[2]=p*a+_*l+m*f,p=r[4],_=r[5],m=r[6],e[4]=p*i+_*o+m*u,e[5]=p*n+_*s+m*h,e[6]=p*a+_*l+m*f,p=r[8],_=r[9],m=r[10],e[8]=p*i+_*o+m*u,e[9]=p*n+_*s+m*h,e[10]=p*a+_*l+m*f,p=r[12],_=r[13],m=r[14],e[12]=p*i+_*o+m*u+d,e[13]=p*n+_*s+m*h+c,e[14]=p*a+_*l+m*f+v,e};z.mul=z.multiply;z.mulAffine=z.multiplyAffine;z.translate=function(e,t,r){var i=r[0],n=r[1],a=r[2],o,s,l,u,h,f,d,c,v,p,_,m;return t===e?(e[12]=t[0]*i+t[4]*n+t[8]*a+t[12],e[13]=t[1]*i+t[5]*n+t[9]*a+t[13],e[14]=t[2]*i+t[6]*n+t[10]*a+t[14],e[15]=t[3]*i+t[7]*n+t[11]*a+t[15]):(o=t[0],s=t[1],l=t[2],u=t[3],h=t[4],f=t[5],d=t[6],c=t[7],v=t[8],p=t[9],_=t[10],m=t[11],e[0]=o,e[1]=s,e[2]=l,e[3]=u,e[4]=h,e[5]=f,e[6]=d,e[7]=c,e[8]=v,e[9]=p,e[10]=_,e[11]=m,e[12]=o*i+h*n+v*a+t[12],e[13]=s*i+f*n+p*a+t[13],e[14]=l*i+d*n+_*a+t[14],e[15]=u*i+c*n+m*a+t[15]),e};z.scale=function(e,t,r){var i=r[0],n=r[1],a=r[2];return e[0]=t[0]*i,e[1]=t[1]*i,e[2]=t[2]*i,e[3]=t[3]*i,e[4]=t[4]*n,e[5]=t[5]*n,e[6]=t[6]*n,e[7]=t[7]*n,e[8]=t[8]*a,e[9]=t[9]*a,e[10]=t[10]*a,e[11]=t[11]*a,e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15],e};z.rotate=function(e,t,r,i){var n=i[0],a=i[1],o=i[2],s=Math.sqrt(n*n+a*a+o*o),l,u,h,f,d,c,v,p,_,m,g,y,x,w,T,b,A,C,D,L,M,P,N,I;return Math.abs(s)<Xn?null:(s=1/s,n*=s,a*=s,o*=s,l=Math.sin(r),u=Math.cos(r),h=1-u,f=t[0],d=t[1],c=t[2],v=t[3],p=t[4],_=t[5],m=t[6],g=t[7],y=t[8],x=t[9],w=t[10],T=t[11],b=n*n*h+u,A=a*n*h+o*l,C=o*n*h-a*l,D=n*a*h-o*l,L=a*a*h+u,M=o*a*h+n*l,P=n*o*h+a*l,N=a*o*h-n*l,I=o*o*h+u,e[0]=f*b+p*A+y*C,e[1]=d*b+_*A+x*C,e[2]=c*b+m*A+w*C,e[3]=v*b+g*A+T*C,e[4]=f*D+p*L+y*M,e[5]=d*D+_*L+x*M,e[6]=c*D+m*L+w*M,e[7]=v*D+g*L+T*M,e[8]=f*P+p*N+y*I,e[9]=d*P+_*N+x*I,e[10]=c*P+m*N+w*I,e[11]=v*P+g*N+T*I,t!==e&&(e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15]),e)};z.rotateX=function(e,t,r){var i=Math.sin(r),n=Math.cos(r),a=t[4],o=t[5],s=t[6],l=t[7],u=t[8],h=t[9],f=t[10],d=t[11];return t!==e&&(e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15]),e[4]=a*n+u*i,e[5]=o*n+h*i,e[6]=s*n+f*i,e[7]=l*n+d*i,e[8]=u*n-a*i,e[9]=h*n-o*i,e[10]=f*n-s*i,e[11]=d*n-l*i,e};z.rotateY=function(e,t,r){var i=Math.sin(r),n=Math.cos(r),a=t[0],o=t[1],s=t[2],l=t[3],u=t[8],h=t[9],f=t[10],d=t[11];return t!==e&&(e[4]=t[4],e[5]=t[5],e[6]=t[6],e[7]=t[7],e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15]),e[0]=a*n-u*i,e[1]=o*n-h*i,e[2]=s*n-f*i,e[3]=l*n-d*i,e[8]=a*i+u*n,e[9]=o*i+h*n,e[10]=s*i+f*n,e[11]=l*i+d*n,e};z.rotateZ=function(e,t,r){var i=Math.sin(r),n=Math.cos(r),a=t[0],o=t[1],s=t[2],l=t[3],u=t[4],h=t[5],f=t[6],d=t[7];return t!==e&&(e[8]=t[8],e[9]=t[9],e[10]=t[10],e[11]=t[11],e[12]=t[12],e[13]=t[13],e[14]=t[14],e[15]=t[15]),e[0]=a*n+u*i,e[1]=o*n+h*i,e[2]=s*n+f*i,e[3]=l*n+d*i,e[4]=u*n-a*i,e[5]=h*n-o*i,e[6]=f*n-s*i,e[7]=d*n-l*i,e};z.fromRotationTranslation=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=i+i,l=n+n,u=a+a,h=i*s,f=i*l,d=i*u,c=n*l,v=n*u,p=a*u,_=o*s,m=o*l,g=o*u;return e[0]=1-(c+p),e[1]=f+g,e[2]=d-m,e[3]=0,e[4]=f-g,e[5]=1-(h+p),e[6]=v+_,e[7]=0,e[8]=d+m,e[9]=v-_,e[10]=1-(h+c),e[11]=0,e[12]=r[0],e[13]=r[1],e[14]=r[2],e[15]=1,e};z.fromQuat=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=r+r,s=i+i,l=n+n,u=r*o,h=i*o,f=i*s,d=n*o,c=n*s,v=n*l,p=a*o,_=a*s,m=a*l;return e[0]=1-f-v,e[1]=h+m,e[2]=d-_,e[3]=0,e[4]=h-m,e[5]=1-u-v,e[6]=c+p,e[7]=0,e[8]=d+_,e[9]=c-p,e[10]=1-u-f,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,e};z.frustum=function(e,t,r,i,n,a,o){var s=1/(r-t),l=1/(n-i),u=1/(a-o);return e[0]=a*2*s,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=a*2*l,e[6]=0,e[7]=0,e[8]=(r+t)*s,e[9]=(n+i)*l,e[10]=(o+a)*u,e[11]=-1,e[12]=0,e[13]=0,e[14]=o*a*2*u,e[15]=0,e};z.perspective=function(e,t,r,i,n){var a=1/Math.tan(t/2),o=1/(i-n);return e[0]=a/r,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=a,e[6]=0,e[7]=0,e[8]=0,e[9]=0,e[10]=(n+i)*o,e[11]=-1,e[12]=0,e[13]=0,e[14]=2*n*i*o,e[15]=0,e};z.ortho=function(e,t,r,i,n,a,o){var s=1/(t-r),l=1/(i-n),u=1/(a-o);return e[0]=-2*s,e[1]=0,e[2]=0,e[3]=0,e[4]=0,e[5]=-2*l,e[6]=0,e[7]=0,e[8]=0,e[9]=0,e[10]=2*u,e[11]=0,e[12]=(t+r)*s,e[13]=(n+i)*l,e[14]=(o+a)*u,e[15]=1,e};z.lookAt=function(e,t,r,i){var n,a,o,s,l,u,h,f,d,c,v=t[0],p=t[1],_=t[2],m=i[0],g=i[1],y=i[2],x=r[0],w=r[1],T=r[2];return Math.abs(v-x)<Xn&&Math.abs(p-w)<Xn&&Math.abs(_-T)<Xn?z.identity(e):(h=v-x,f=p-w,d=_-T,c=1/Math.sqrt(h*h+f*f+d*d),h*=c,f*=c,d*=c,n=g*d-y*f,a=y*h-m*d,o=m*f-g*h,c=Math.sqrt(n*n+a*a+o*o),c?(c=1/c,n*=c,a*=c,o*=c):(n=0,a=0,o=0),s=f*o-d*a,l=d*n-h*o,u=h*a-f*n,c=Math.sqrt(s*s+l*l+u*u),c?(c=1/c,s*=c,l*=c,u*=c):(s=0,l=0,u=0),e[0]=n,e[1]=s,e[2]=h,e[3]=0,e[4]=a,e[5]=l,e[6]=f,e[7]=0,e[8]=o,e[9]=u,e[10]=d,e[11]=0,e[12]=-(n*v+a*p+o*_),e[13]=-(s*v+l*p+u*_),e[14]=-(h*v+f*p+d*_),e[15]=1,e)};z.frob=function(e){return Math.sqrt(Math.pow(e[0],2)+Math.pow(e[1],2)+Math.pow(e[2],2)+Math.pow(e[3],2)+Math.pow(e[4],2)+Math.pow(e[5],2)+Math.pow(e[6],2)+Math.pow(e[7],2)+Math.pow(e[8],2)+Math.pow(e[9],2)+Math.pow(e[10],2)+Math.pow(e[11],2)+Math.pow(e[12],2)+Math.pow(e[13],2)+Math.pow(e[14],2)+Math.pow(e[15],2))};var E={};E.create=function(){var e=new et(3);return e[0]=0,e[1]=0,e[2]=0,e};E.clone=function(e){var t=new et(3);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t};E.fromValues=function(e,t,r){var i=new et(3);return i[0]=e,i[1]=t,i[2]=r,i};E.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e};E.set=function(e,t,r,i){return e[0]=t,e[1]=r,e[2]=i,e};E.add=function(e,t,r){return e[0]=t[0]+r[0],e[1]=t[1]+r[1],e[2]=t[2]+r[2],e};E.subtract=function(e,t,r){return e[0]=t[0]-r[0],e[1]=t[1]-r[1],e[2]=t[2]-r[2],e};E.sub=E.subtract;E.multiply=function(e,t,r){return e[0]=t[0]*r[0],e[1]=t[1]*r[1],e[2]=t[2]*r[2],e};E.mul=E.multiply;E.divide=function(e,t,r){return e[0]=t[0]/r[0],e[1]=t[1]/r[1],e[2]=t[2]/r[2],e};E.div=E.divide;E.min=function(e,t,r){return e[0]=Math.min(t[0],r[0]),e[1]=Math.min(t[1],r[1]),e[2]=Math.min(t[2],r[2]),e};E.max=function(e,t,r){return e[0]=Math.max(t[0],r[0]),e[1]=Math.max(t[1],r[1]),e[2]=Math.max(t[2],r[2]),e};E.scale=function(e,t,r){return e[0]=t[0]*r,e[1]=t[1]*r,e[2]=t[2]*r,e};E.scaleAndAdd=function(e,t,r,i){return e[0]=t[0]+r[0]*i,e[1]=t[1]+r[1]*i,e[2]=t[2]+r[2]*i,e};E.distance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1],n=t[2]-e[2];return Math.sqrt(r*r+i*i+n*n)};E.dist=E.distance;E.squaredDistance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1],n=t[2]-e[2];return r*r+i*i+n*n};E.sqrDist=E.squaredDistance;E.length=function(e){var t=e[0],r=e[1],i=e[2];return Math.sqrt(t*t+r*r+i*i)};E.len=E.length;E.squaredLength=function(e){var t=e[0],r=e[1],i=e[2];return t*t+r*r+i*i};E.sqrLen=E.squaredLength;E.negate=function(e,t){return e[0]=-t[0],e[1]=-t[1],e[2]=-t[2],e};E.inverse=function(e,t){return e[0]=1/t[0],e[1]=1/t[1],e[2]=1/t[2],e};E.normalize=function(e,t){var r=t[0],i=t[1],n=t[2],a=r*r+i*i+n*n;return a>0&&(a=1/Math.sqrt(a),e[0]=t[0]*a,e[1]=t[1]*a,e[2]=t[2]*a),e};E.dot=function(e,t){return e[0]*t[0]+e[1]*t[1]+e[2]*t[2]};E.cross=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=r[0],s=r[1],l=r[2];return e[0]=n*l-a*s,e[1]=a*o-i*l,e[2]=i*s-n*o,e};E.lerp=function(e,t,r,i){var n=t[0],a=t[1],o=t[2];return e[0]=n+i*(r[0]-n),e[1]=a+i*(r[1]-a),e[2]=o+i*(r[2]-o),e};E.random=function(e,t){t=t||1;var r=si()*2*Math.PI,i=si()*2-1,n=Math.sqrt(1-i*i)*t;return e[0]=Math.cos(r)*n,e[1]=Math.sin(r)*n,e[2]=i*t,e};E.transformMat4=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=r[3]*i+r[7]*n+r[11]*a+r[15];return o=o||1,e[0]=(r[0]*i+r[4]*n+r[8]*a+r[12])/o,e[1]=(r[1]*i+r[5]*n+r[9]*a+r[13])/o,e[2]=(r[2]*i+r[6]*n+r[10]*a+r[14])/o,e};E.transformMat3=function(e,t,r){var i=t[0],n=t[1],a=t[2];return e[0]=i*r[0]+n*r[3]+a*r[6],e[1]=i*r[1]+n*r[4]+a*r[7],e[2]=i*r[2]+n*r[5]+a*r[8],e};E.transformQuat=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=r[0],s=r[1],l=r[2],u=r[3],h=u*i+s*a-l*n,f=u*n+l*i-o*a,d=u*a+o*n-s*i,c=-o*i-s*n-l*a;return e[0]=h*u+c*-o+f*-l-d*-s,e[1]=f*u+c*-s+d*-o-h*-l,e[2]=d*u+c*-l+h*-s-f*-o,e};E.rotateX=function(e,t,r,i){var n=[],a=[];return n[0]=t[0]-r[0],n[1]=t[1]-r[1],n[2]=t[2]-r[2],a[0]=n[0],a[1]=n[1]*Math.cos(i)-n[2]*Math.sin(i),a[2]=n[1]*Math.sin(i)+n[2]*Math.cos(i),e[0]=a[0]+r[0],e[1]=a[1]+r[1],e[2]=a[2]+r[2],e};E.rotateY=function(e,t,r,i){var n=[],a=[];return n[0]=t[0]-r[0],n[1]=t[1]-r[1],n[2]=t[2]-r[2],a[0]=n[2]*Math.sin(i)+n[0]*Math.cos(i),a[1]=n[1],a[2]=n[2]*Math.cos(i)-n[0]*Math.sin(i),e[0]=a[0]+r[0],e[1]=a[1]+r[1],e[2]=a[2]+r[2],e};E.rotateZ=function(e,t,r,i){var n=[],a=[];return n[0]=t[0]-r[0],n[1]=t[1]-r[1],n[2]=t[2]-r[2],a[0]=n[0]*Math.cos(i)-n[1]*Math.sin(i),a[1]=n[0]*Math.sin(i)+n[1]*Math.cos(i),a[2]=n[2],e[0]=a[0]+r[0],e[1]=a[1]+r[1],e[2]=a[2]+r[2],e};E.forEach=function(){var e=E.create();return function(t,r,i,n,a,o){var s,l;for(r||(r=3),i||(i=0),n?l=Math.min(n*r+i,t.length):l=t.length,s=i;s<l;s+=r)e[0]=t[s],e[1]=t[s+1],e[2]=t[s+2],a(e,e,o),t[s]=e[0],t[s+1]=e[1],t[s+2]=e[2];return t}}();E.angle=function(e,t){var r=E.fromValues(e[0],e[1],e[2]),i=E.fromValues(t[0],t[1],t[2]);E.normalize(r,r),E.normalize(i,i);var n=E.dot(r,i);return n>1?0:Math.acos(n)};k.import(kh);var Te=z.create,Zl={};function ql(e){return e.material}function Tg(e,t,r){return t.uniforms[r].value}function wg(e,t,r,i){return r!==i}function Sg(e){return!0}function Yl(){}var $l={float:F.FLOAT,byte:F.BYTE,ubyte:F.UNSIGNED_BYTE,short:F.SHORT,ushort:F.UNSIGNED_SHORT};function bg(e,t,r){this.availableAttributes=e,this.availableAttributeSymbols=t,this.indicesBuffer=r,this.vao=null}function Ag(e){var t,r;this.bind=function(i){t||(t=de.createCanvas(),t.width=t.height=1,t.getContext("2d"));var n=i.gl,a=!r;a&&(r=n.createTexture()),n.bindTexture(n.TEXTURE_2D,r),a&&n.texImage2D(n.TEXTURE_2D,0,n.RGBA,n.RGBA,n.UNSIGNED_BYTE,t)},this.unbind=function(i){i.gl.bindTexture(i.gl.TEXTURE_2D,null)},this.isRenderable=function(){return!0}}var Et=Qe.extend(function(){return{canvas:null,_width:100,_height:100,devicePixelRatio:typeof window<"u"&&window.devicePixelRatio||1,clearColor:[0,0,0,0],clearBit:17664,alpha:!0,depth:!0,stencil:!1,antialias:!0,premultipliedAlpha:!0,preserveDrawingBuffer:!1,throwError:!0,gl:null,viewport:{},maxJointNumber:20,__currentFrameBuffer:null,_viewportStack:[],_clearStack:[],_sceneRendering:null}},function(){this.canvas||(this.canvas=de.createCanvas());var e=this.canvas;try{var t={alpha:this.alpha,depth:this.depth,stencil:this.stencil,antialias:this.antialias,premultipliedAlpha:this.premultipliedAlpha,preserveDrawingBuffer:this.preserveDrawingBuffer};if(this.gl=e.getContext("webgl",t)||e.getContext("experimental-webgl",t),!this.gl)throw new Error;this._glinfo=new ig(this.gl),this.gl.targetRenderer&&console.error("Already created a renderer"),this.gl.targetRenderer=this,this.resize()}catch(r){throw"Error creating WebGL Context "+r}this._programMgr=new zh(this),this._placeholderTexture=new Ag},{resize:function(e,t){var r=this.canvas,i=this.devicePixelRatio;e!=null?(r.style&&(r.style.width=e+"px",r.style.height=t+"px"),r.width=e*i,r.height=t*i,this._width=e,this._height=t):(this._width=r.width/i,this._height=r.height/i),this.setViewport(0,0,this._width,this._height)},getWidth:function(){return this._width},getHeight:function(){return this._height},getViewportAspect:function(){var e=this.viewport;return e.width/e.height},setDevicePixelRatio:function(e){this.devicePixelRatio=e,this.resize(this._width,this._height)},getDevicePixelRatio:function(){return this.devicePixelRatio},getGLExtension:function(e){return this._glinfo.getExtension(e)},getGLParameter:function(e){return this._glinfo.getParameter(e)},setViewport:function(e,t,r,i,n){if(typeof e=="object"){var a=e;e=a.x,t=a.y,r=a.width,i=a.height,n=a.devicePixelRatio}n=n||this.devicePixelRatio,this.gl.viewport(e*n,t*n,r*n,i*n),this.viewport={x:e,y:t,width:r,height:i,devicePixelRatio:n}},saveViewport:function(){this._viewportStack.push(this.viewport)},restoreViewport:function(){this._viewportStack.length>0&&this.setViewport(this._viewportStack.pop())},saveClear:function(){this._clearStack.push({clearBit:this.clearBit,clearColor:this.clearColor})},restoreClear:function(){if(this._clearStack.length>0){var e=this._clearStack.pop();this.clearColor=e.clearColor,this.clearBit=e.clearBit}},bindSceneRendering:function(e){this._sceneRendering=e},render:function(e,t,r,i){var n=this.gl,a=this.clearColor;if(this.clearBit){n.colorMask(!0,!0,!0,!0),n.depthMask(!0);var o=this.viewport,s=!1,l=o.devicePixelRatio;(o.width!==this._width||o.height!==this._height||l&&l!==this.devicePixelRatio||o.x||o.y)&&(s=!0,n.enable(n.SCISSOR_TEST),n.scissor(o.x*l,o.y*l,o.width*l,o.height*l)),n.clearColor(a[0],a[1],a[2],a[3]),n.clear(this.clearBit),s&&n.disable(n.SCISSOR_TEST)}if(r||e.update(!1),e.updateLights(),t=t||e.getMainCamera(),!t){console.error("Can't find camera in the scene.");return}t.update();var u=e.updateRenderList(t,!0);this._sceneRendering=e;var h=u.opaque,f=u.transparent,d=e.material;e.trigger("beforerender",this,e,t,u),i?(this.renderPreZ(h,e,t),n.depthFunc(n.LEQUAL)):n.depthFunc(n.LESS);for(var c=Te(),v=E.create(),p=0;p<f.length;p++){var _=f[p];z.multiplyAffine(c,t.viewMatrix.array,_.worldTransform.array),E.transformMat4(v,_.position.array,c),_.__depth=v[2]}this.renderPass(h,t,{getMaterial:function(m){return d||m.material},sortCompare:this.opaqueSortCompare}),this.renderPass(f,t,{getMaterial:function(m){return d||m.material},sortCompare:this.transparentSortCompare}),e.trigger("afterrender",this,e,t,u),this._sceneRendering=null},getProgram:function(e,t,r){return t=t||e.material,this._programMgr.getProgram(e,t,r)},validateProgram:function(e){if(e.__error){var t=e.__error;if(Zl[e.__uid__])return;if(Zl[e.__uid__]=!0,this.throwError)throw new Error(t);this.trigger("error",t)}},updatePrograms:function(e,t,r){var i=r&&r.getMaterial||ql;t=t||null;for(var n=0;n<e.length;n++){var a=e[n],o=i.call(this,a);if(n>0){var s=e[n-1],l=s.joints?s.joints.length:0,u=a.joints?a.joints.length:0;if(u===l&&a.material===s.material&&a.lightGroup===s.lightGroup){a.__program=s.__program;continue}}var h=this._programMgr.getProgram(a,o,t);this.validateProgram(h),a.__program=h}},renderPass:function(e,t,r){this.trigger("beforerenderpass",this,e,t,r),r=r||{},r.getMaterial=r.getMaterial||ql,r.getUniform=r.getUniform||Tg,r.isMaterialChanged=r.isMaterialChanged||wg,r.beforeRender=r.beforeRender||Yl,r.afterRender=r.afterRender||Yl;var i=r.ifRender||Sg;this.updatePrograms(e,this._sceneRendering,r),r.sortCompare&&e.sort(r.sortCompare);var n=this.viewport,a=n.devicePixelRatio,o=[n.x*a,n.y*a,n.width*a,n.height*a],s=this.devicePixelRatio,l=this.__currentFrameBuffer?[this.__currentFrameBuffer.getTextureWidth(),this.__currentFrameBuffer.getTextureHeight()]:[this._width*s,this._height*s],u=[o[2],o[3]],h=Date.now();t?(z.copy(xe.VIEW,t.viewMatrix.array),z.copy(xe.PROJECTION,t.projectionMatrix.array),z.copy(xe.VIEWINVERSE,t.worldTransform.array)):(z.identity(xe.VIEW),z.identity(xe.PROJECTION),z.identity(xe.VIEWINVERSE)),z.multiply(xe.VIEWPROJECTION,xe.PROJECTION,xe.VIEW),z.invert(xe.PROJECTIONINVERSE,xe.PROJECTION),z.invert(xe.VIEWPROJECTIONINVERSE,xe.VIEWPROJECTION);for(var f=this.gl,d=this._sceneRendering,c,v,p,_,m,g,y,x,w,T,b,A,C=null,D=0;D<e.length;D++){var L=e[D],M=L.worldTransform!=null,P;if(i(L)){M&&(P=L.isSkinnedMesh&&L.isSkinnedMesh()?L.offsetMatrix?L.offsetMatrix.array:xe.IDENTITY:L.worldTransform.array);var N=L.geometry,I=r.getMaterial.call(this,L),V=L.__program,Z=I.shader,B=N.__uid__+"-"+V.__uid__,$=B!==T;T=B,M&&(z.copy(xe.WORLD,P),z.multiply(xe.WORLDVIEWPROJECTION,xe.VIEWPROJECTION,P),z.multiplyAffine(xe.WORLDVIEW,xe.VIEW,P),(Z.matrixSemantics.WORLDINVERSE||Z.matrixSemantics.WORLDINVERSETRANSPOSE)&&z.invert(xe.WORLDINVERSE,P),(Z.matrixSemantics.WORLDVIEWINVERSE||Z.matrixSemantics.WORLDVIEWINVERSETRANSPOSE)&&z.invert(xe.WORLDVIEWINVERSE,xe.WORLDVIEW),(Z.matrixSemantics.WORLDVIEWPROJECTIONINVERSE||Z.matrixSemantics.WORLDVIEWPROJECTIONINVERSETRANSPOSE)&&z.invert(xe.WORLDVIEWPROJECTIONINVERSE,xe.WORLDVIEWPROJECTION)),L.beforeRender&&L.beforeRender(this),r.beforeRender.call(this,L,I,c);var q=V!==v;q?(V.bind(this),V.setUniformOfSemantic(f,"VIEWPORT",o),V.setUniformOfSemantic(f,"WINDOW_SIZE",l),t&&(V.setUniformOfSemantic(f,"NEAR",t.near),V.setUniformOfSemantic(f,"FAR",t.far)),V.setUniformOfSemantic(f,"DEVICEPIXELRATIO",a),V.setUniformOfSemantic(f,"TIME",h),V.setUniformOfSemantic(f,"VIEWPORT_SIZE",u),d&&d.setLightUniforms(V,L.lightGroup,this)):V=v,(q||r.isMaterialChanged(L,p,I,c))&&(I.depthTest!==_&&(I.depthTest?f.enable(f.DEPTH_TEST):f.disable(f.DEPTH_TEST),_=I.depthTest),I.depthMask!==m&&(f.depthMask(I.depthMask),m=I.depthMask),I.transparent!==w&&(I.transparent?f.enable(f.BLEND):f.disable(f.BLEND),w=I.transparent),I.transparent&&(I.blend?I.blend(f):(f.blendEquationSeparate(f.FUNC_ADD,f.FUNC_ADD),f.blendFuncSeparate(f.SRC_ALPHA,f.ONE_MINUS_SRC_ALPHA,f.ONE,f.ONE_MINUS_SRC_ALPHA))),A=this._bindMaterial(L,I,V,p||null,c||null,v||null,r.getUniform),c=I);var j=Z.matrixSemanticKeys;if(M)for(var Q=0;Q<j.length;Q++){var ie=j[Q],ae=Z.matrixSemantics[ie],ee=xe[ie];if(ae.isTranspose){var be=xe[ae.semanticNoTranspose];z.transpose(ee,be)}V.setUniform(f,ae.type,ae.symbol,ee)}L.cullFace!==y&&(y=L.cullFace,f.cullFace(y)),L.frontFace!==x&&(x=L.frontFace,f.frontFace(x)),L.culling!==g&&(g=L.culling,g?f.enable(f.CULL_FACE):f.disable(f.CULL_FACE)),this._updateSkeleton(L,V,A),$&&(b=this._bindVAO(C,Z,N,V)),this._renderObject(L,b,V),r.afterRender(this,L),L.afterRender&&L.afterRender(this),v=V,p=L}}this.trigger("afterrenderpass",this,e,t,r)},getMaxJointNumber:function(){return this.maxJointNumber},_updateSkeleton:function(e,t,r){var i=this.gl,n=e.skeleton;if(n)if(n.update(),e.joints.length>this.getMaxJointNumber()){var a=n.getSubSkinMatricesTexture(e.__uid__,e.joints);t.useTextureSlot(this,a,r),t.setUniform(i,"1i","skinMatricesTexture",r),t.setUniform(i,"1f","skinMatricesTextureSize",a.width)}else{var o=n.getSubSkinMatrices(e.__uid__,e.joints);t.setUniformOfSemantic(i,"SKIN_MATRIX",o)}},_renderObject:function(e,t,r){var i=this.gl,n=e.geometry,a=e.mode;a==null&&(a=4);var o=null,s=e.isInstancedMesh&&e.isInstancedMesh();if(s&&(o=this.getGLExtension("ANGLE_instanced_arrays"),!o)){console.warn("Device not support ANGLE_instanced_arrays extension");return}var l;if(s&&(l=this._bindInstancedAttributes(e,r,o)),t.indicesBuffer){var u=this.getGLExtension("OES_element_index_uint"),h=u&&n.indices instanceof Uint32Array,f=h?i.UNSIGNED_INT:i.UNSIGNED_SHORT;s?o.drawElementsInstancedANGLE(a,t.indicesBuffer.count,f,0,e.getInstanceCount()):i.drawElements(a,t.indicesBuffer.count,f,0)}else s?o.drawArraysInstancedANGLE(a,0,n.vertexCount,e.getInstanceCount()):i.drawArrays(a,0,n.vertexCount);if(s)for(var d=0;d<l.length;d++)i.disableVertexAttribArray(l[d])},_bindInstancedAttributes:function(e,t,r){for(var i=this.gl,n=e.getInstancedAttributesBuffers(this),a=[],o=0;o<n.length;o++){var s=n[o],l=t.getAttribLocation(i,s.symbol);if(!(l<0)){var u=$l[s.type]||i.FLOAT;i.enableVertexAttribArray(l),i.bindBuffer(i.ARRAY_BUFFER,s.buffer),i.vertexAttribPointer(l,s.size,u,!1,0,0),r.vertexAttribDivisorANGLE(l,s.divisor),a.push(l)}}return a},_bindMaterial:function(e,t,r,i,n,a,o){for(var s=this.gl,l=a===r,u=r.currentTextureSlot(),h=t.getEnabledUniforms(),f=t.getTextureUniforms(),d=this._placeholderTexture,c=0;c<f.length;c++){var v=f[c],p=o(e,t,v),_=t.uniforms[v].type;if(_==="t"&&p)p.__slot=-1;else if(_==="tv")for(var m=0;m<p.length;m++)p[m]&&(p[m].__slot=-1)}d.__slot=-1;for(var c=0;c<h.length;c++){var v=h[c],g=t.uniforms[v],p=o(e,t,v),_=g.type,y=_==="t";if(y&&(!p||!p.isRenderable())&&(p=d),n&&l){var x=o(i,n,v);if(y&&(!x||!x.isRenderable())&&(x=d),x===p){if(y)r.takeCurrentTextureSlot(this,null);else if(_==="tv"&&p)for(var m=0;m<p.length;m++)r.takeCurrentTextureSlot(this,null);continue}}if(p!=null)if(y)if(p.__slot<0){var w=r.currentTextureSlot(),T=r.setUniform(s,"1i",v,w);T&&(r.takeCurrentTextureSlot(this,p),p.__slot=w)}else r.setUniform(s,"1i",v,p.__slot);else if(Array.isArray(p)){if(p.length===0)continue;if(_==="tv"){if(!r.hasUniform(v))continue;for(var b=[],m=0;m<p.length;m++){var A=p[m];if(A.__slot<0){var w=r.currentTextureSlot();b.push(w),r.takeCurrentTextureSlot(this,A),A.__slot=w}else b.push(A.__slot)}r.setUniform(s,"1iv",v,b)}else r.setUniform(s,g.type,v,p)}else r.setUniform(s,g.type,v,p)}var C=r.currentTextureSlot();return r.resetTextureSlot(u),C},_bindVAO:function(e,t,r,i){var n=!r.dynamic,a=this.gl,o=this.__uid__+"-"+i.__uid__,s=r.__vaoCache[o];if(!s){var l=r.getBufferChunks(this);if(!l||!l.length)return;for(var u=l[0],h=u.attributeBuffers,x=u.indicesBuffer,y=[],f=[],d=0;d<h.length;d++){var c=h[d],v=c.name,p=c.semantic,_;if(p){var m=t.attributeSemantics[p];_=m&&m.symbol}else _=v;_&&i.attributes[_]&&(y.push(c),f.push(_))}s=new bg(y,f,x),n&&(r.__vaoCache[o]=s)}var g=!0;e&&n&&(s.vao==null?s.vao=e.createVertexArrayOES():g=!1,e.bindVertexArrayOES(s.vao));var y=s.availableAttributes,x=s.indicesBuffer;if(g){for(var w=i.enableAttributes(this,s.availableAttributeSymbols,e&&n&&s),d=0;d<y.length;d++){var T=w[d];if(T!==-1){var c=y[d],b=c.buffer,A=c.size,C=$l[c.type]||a.FLOAT;a.bindBuffer(a.ARRAY_BUFFER,b),a.vertexAttribPointer(T,A,C,!1,0,0)}}r.isUseIndices()&&a.bindBuffer(a.ELEMENT_ARRAY_BUFFER,x.buffer)}return s},renderPreZ:function(e,t,r){var i=this.gl,n=this._prezMaterial||new At({shader:new k(k.source("clay.prez.vertex"),k.source("clay.prez.fragment"))});this._prezMaterial=n,i.colorMask(!1,!1,!1,!1),i.depthMask(!0),this.renderPass(e,r,{ifRender:function(a){return!a.ignorePreZ},isMaterialChanged:function(a,o){var s=a.material,l=o.material;return s.get("diffuseMap")!==l.get("diffuseMap")||(s.get("alphaCutoff")||0)!==(l.get("alphaCutoff")||0)},getUniform:function(a,o,s){if(s==="alphaMap")return a.material.get("diffuseMap");if(s==="alphaCutoff"){if(a.material.isDefined("fragment","ALPHA_TEST")&&a.material.get("diffuseMap")){var l=a.material.get("alphaCutoff");return l||0}return 0}else return s==="uvRepeat"?a.material.get("uvRepeat"):s==="uvOffset"?a.material.get("uvOffset"):o.get(s)},getMaterial:function(){return n},sort:this.opaqueSortCompare}),i.colorMask(!0,!0,!0,!0),i.depthMask(!0)},disposeScene:function(e){this.disposeNode(e,!0,!0),e.dispose()},disposeNode:function(e,t,r){e.getParent()&&e.getParent().remove(e);var i={};e.traverse(function(n){var a=n.material;if(n.geometry&&t&&n.geometry.dispose(this),r&&a&&!i[a.__uid__]){for(var o=a.getTextureUniforms(),s=0;s<o.length;s++){var l=o[s],u=a.uniforms[l].value,h=a.uniforms[l].type;if(u){if(h==="t")u.dispose&&u.dispose(this);else if(h==="tv")for(var f=0;f<u.length;f++)u[f]&&u[f].dispose&&u[f].dispose(this)}}i[a.__uid__]=!0}n.dispose&&n.dispose(this)},this)},disposeGeometry:function(e){e.dispose(this)},disposeTexture:function(e){e.dispose(this)},disposeFrameBuffer:function(e){e.dispose(this)},dispose:function(){},screenToNDC:function(e,t,r){r||(r=new te),t=this._height-t;var i=this.viewport,n=r.array;return n[0]=(e-i.x)/i.width,n[0]=n[0]*2-1,n[1]=(t-i.y)/i.height,n[1]=n[1]*2-1,r}});Et.opaqueSortCompare=Et.prototype.opaqueSortCompare=function(e,t){return e.renderOrder===t.renderOrder?e.__program===t.__program?e.material===t.material?e.geometry.__uid__-t.geometry.__uid__:e.material.__uid__-t.material.__uid__:e.__program&&t.__program?e.__program.__uid__-t.__program.__uid__:0:e.renderOrder-t.renderOrder};Et.transparentSortCompare=Et.prototype.transparentSortCompare=function(e,t){return e.renderOrder===t.renderOrder?e.__depth===t.__depth?e.__program===t.__program?e.material===t.material?e.geometry.__uid__-t.geometry.__uid__:e.material.__uid__-t.material.__uid__:e.__program&&t.__program?e.__program.__uid__-t.__program.__uid__:0:e.__depth-t.__depth:e.renderOrder-t.renderOrder};var xe={IDENTITY:Te(),WORLD:Te(),VIEW:Te(),PROJECTION:Te(),WORLDVIEW:Te(),VIEWPROJECTION:Te(),WORLDVIEWPROJECTION:Te(),WORLDINVERSE:Te(),VIEWINVERSE:Te(),PROJECTIONINVERSE:Te(),WORLDVIEWINVERSE:Te(),VIEWPROJECTIONINVERSE:Te(),WORLDVIEWPROJECTIONINVERSE:Te(),WORLDTRANSPOSE:Te(),VIEWTRANSPOSE:Te(),PROJECTIONTRANSPOSE:Te(),WORLDVIEWTRANSPOSE:Te(),VIEWPROJECTIONTRANSPOSE:Te(),WORLDVIEWPROJECTIONTRANSPOSE:Te(),WORLDINVERSETRANSPOSE:Te(),VIEWINVERSETRANSPOSE:Te(),PROJECTIONINVERSETRANSPOSE:Te(),WORLDVIEWINVERSETRANSPOSE:Te(),VIEWPROJECTIONINVERSETRANSPOSE:Te(),WORLDVIEWPROJECTIONINVERSETRANSPOSE:Te()};Et.COLOR_BUFFER_BIT=F.COLOR_BUFFER_BIT;Et.DEPTH_BUFFER_BIT=F.DEPTH_BUFFER_BIT;Et.STENCIL_BUFFER_BIT=F.STENCIL_BUFFER_BIT;var R=function(e,t,r){e=e||0,t=t||0,r=r||0,this.array=E.fromValues(e,t,r),this._dirty=!0};R.prototype={constructor:R,add:function(e){return E.add(this.array,this.array,e.array),this._dirty=!0,this},set:function(e,t,r){return this.array[0]=e,this.array[1]=t,this.array[2]=r,this._dirty=!0,this},setArray:function(e){return this.array[0]=e[0],this.array[1]=e[1],this.array[2]=e[2],this._dirty=!0,this},clone:function(){return new R(this.x,this.y,this.z)},copy:function(e){return E.copy(this.array,e.array),this._dirty=!0,this},cross:function(e,t){return E.cross(this.array,e.array,t.array),this._dirty=!0,this},dist:function(e){return E.dist(this.array,e.array)},distance:function(e){return E.distance(this.array,e.array)},div:function(e){return E.div(this.array,this.array,e.array),this._dirty=!0,this},divide:function(e){return E.divide(this.array,this.array,e.array),this._dirty=!0,this},dot:function(e){return E.dot(this.array,e.array)},len:function(){return E.len(this.array)},length:function(){return E.length(this.array)},lerp:function(e,t,r){return E.lerp(this.array,e.array,t.array,r),this._dirty=!0,this},min:function(e){return E.min(this.array,this.array,e.array),this._dirty=!0,this},max:function(e){return E.max(this.array,this.array,e.array),this._dirty=!0,this},mul:function(e){return E.mul(this.array,this.array,e.array),this._dirty=!0,this},multiply:function(e){return E.multiply(this.array,this.array,e.array),this._dirty=!0,this},negate:function(){return E.negate(this.array,this.array),this._dirty=!0,this},normalize:function(){return E.normalize(this.array,this.array),this._dirty=!0,this},random:function(e){return E.random(this.array,e),this._dirty=!0,this},scale:function(e){return E.scale(this.array,this.array,e),this._dirty=!0,this},scaleAndAdd:function(e,t){return E.scaleAndAdd(this.array,this.array,e.array,t),this._dirty=!0,this},sqrDist:function(e){return E.sqrDist(this.array,e.array)},squaredDistance:function(e){return E.squaredDistance(this.array,e.array)},sqrLen:function(){return E.sqrLen(this.array)},squaredLength:function(){return E.squaredLength(this.array)},sub:function(e){return E.sub(this.array,this.array,e.array),this._dirty=!0,this},subtract:function(e){return E.subtract(this.array,this.array,e.array),this._dirty=!0,this},transformMat3:function(e){return E.transformMat3(this.array,this.array,e.array),this._dirty=!0,this},transformMat4:function(e){return E.transformMat4(this.array,this.array,e.array),this._dirty=!0,this},transformQuat:function(e){return E.transformQuat(this.array,this.array,e.array),this._dirty=!0,this},applyProjection:function(e){var t=this.array;if(e=e.array,e[15]===0){var r=-1/t[2];t[0]=e[0]*t[0]*r,t[1]=e[5]*t[1]*r,t[2]=(e[10]*t[2]+e[14])*r}else t[0]=e[0]*t[0]+e[12],t[1]=e[5]*t[1]+e[13],t[2]=e[10]*t[2]+e[14];return this._dirty=!0,this},eulerFromQuat:function(e,t){R.eulerFromQuat(this,e,t)},eulerFromMat3:function(e,t){R.eulerFromMat3(this,e,t)},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};var Pn=Object.defineProperty;if(Pn){var ka=R.prototype;Pn(ka,"x",{get:function(){return this.array[0]},set:function(e){this.array[0]=e,this._dirty=!0}}),Pn(ka,"y",{get:function(){return this.array[1]},set:function(e){this.array[1]=e,this._dirty=!0}}),Pn(ka,"z",{get:function(){return this.array[2]},set:function(e){this.array[2]=e,this._dirty=!0}})}R.add=function(e,t,r){return E.add(e.array,t.array,r.array),e._dirty=!0,e};R.set=function(e,t,r,i){E.set(e.array,t,r,i),e._dirty=!0};R.copy=function(e,t){return E.copy(e.array,t.array),e._dirty=!0,e};R.cross=function(e,t,r){return E.cross(e.array,t.array,r.array),e._dirty=!0,e};R.dist=function(e,t){return E.distance(e.array,t.array)};R.distance=R.dist;R.div=function(e,t,r){return E.divide(e.array,t.array,r.array),e._dirty=!0,e};R.divide=R.div;R.dot=function(e,t){return E.dot(e.array,t.array)};R.len=function(e){return E.length(e.array)};R.lerp=function(e,t,r,i){return E.lerp(e.array,t.array,r.array,i),e._dirty=!0,e};R.min=function(e,t,r){return E.min(e.array,t.array,r.array),e._dirty=!0,e};R.max=function(e,t,r){return E.max(e.array,t.array,r.array),e._dirty=!0,e};R.mul=function(e,t,r){return E.multiply(e.array,t.array,r.array),e._dirty=!0,e};R.multiply=R.mul;R.negate=function(e,t){return E.negate(e.array,t.array),e._dirty=!0,e};R.normalize=function(e,t){return E.normalize(e.array,t.array),e._dirty=!0,e};R.random=function(e,t){return E.random(e.array,t),e._dirty=!0,e};R.scale=function(e,t,r){return E.scale(e.array,t.array,r),e._dirty=!0,e};R.scaleAndAdd=function(e,t,r,i){return E.scaleAndAdd(e.array,t.array,r.array,i),e._dirty=!0,e};R.sqrDist=function(e,t){return E.sqrDist(e.array,t.array)};R.squaredDistance=R.sqrDist;R.sqrLen=function(e){return E.sqrLen(e.array)};R.squaredLength=R.sqrLen;R.sub=function(e,t,r){return E.subtract(e.array,t.array,r.array),e._dirty=!0,e};R.subtract=R.sub;R.transformMat3=function(e,t,r){return E.transformMat3(e.array,t.array,r.array),e._dirty=!0,e};R.transformMat4=function(e,t,r){return E.transformMat4(e.array,t.array,r.array),e._dirty=!0,e};R.transformQuat=function(e,t,r){return E.transformQuat(e.array,t.array,r.array),e._dirty=!0,e};function Tt(e,t,r){return e<t?t:e>r?r:e}var _e=Math.atan2,wt=Math.asin,Jr=Math.abs;R.eulerFromQuat=function(e,t,d){e._dirty=!0,t=t.array;var i=e.array,n=t[0],a=t[1],o=t[2],s=t[3],l=n*n,u=a*a,h=o*o,f=s*s,d=(d||"XYZ").toUpperCase();switch(d){case"XYZ":i[0]=_e(2*(n*s-a*o),f-l-u+h),i[1]=wt(Tt(2*(n*o+a*s),-1,1)),i[2]=_e(2*(o*s-n*a),f+l-u-h);break;case"YXZ":i[0]=wt(Tt(2*(n*s-a*o),-1,1)),i[1]=_e(2*(n*o+a*s),f-l-u+h),i[2]=_e(2*(n*a+o*s),f-l+u-h);break;case"ZXY":i[0]=wt(Tt(2*(n*s+a*o),-1,1)),i[1]=_e(2*(a*s-o*n),f-l-u+h),i[2]=_e(2*(o*s-n*a),f-l+u-h);break;case"ZYX":i[0]=_e(2*(n*s+o*a),f-l-u+h),i[1]=wt(Tt(2*(a*s-n*o),-1,1)),i[2]=_e(2*(n*a+o*s),f+l-u-h);break;case"YZX":i[0]=_e(2*(n*s-o*a),f-l+u-h),i[1]=_e(2*(a*s-n*o),f+l-u-h),i[2]=wt(Tt(2*(n*a+o*s),-1,1));break;case"XZY":i[0]=_e(2*(n*s+a*o),f-l+u-h),i[1]=_e(2*(n*o+a*s),f+l-u-h),i[2]=wt(Tt(2*(o*s-n*a),-1,1));break;default:console.warn("Unkown order: "+d)}return e};R.eulerFromMat3=function(e,t,v){var i=t.array,n=i[0],a=i[3],o=i[6],s=i[1],l=i[4],u=i[7],h=i[2],f=i[5],d=i[8],c=e.array,v=(v||"XYZ").toUpperCase();switch(v){case"XYZ":c[1]=wt(Tt(o,-1,1)),Jr(o)<.99999?(c[0]=_e(-u,d),c[2]=_e(-a,n)):(c[0]=_e(f,l),c[2]=0);break;case"YXZ":c[0]=wt(-Tt(u,-1,1)),Jr(u)<.99999?(c[1]=_e(o,d),c[2]=_e(s,l)):(c[1]=_e(-h,n),c[2]=0);break;case"ZXY":c[0]=wt(Tt(f,-1,1)),Jr(f)<.99999?(c[1]=_e(-h,d),c[2]=_e(-a,l)):(c[1]=0,c[2]=_e(s,n));break;case"ZYX":c[1]=wt(-Tt(h,-1,1)),Jr(h)<.99999?(c[0]=_e(f,d),c[2]=_e(s,n)):(c[0]=0,c[2]=_e(-a,l));break;case"YZX":c[2]=wt(Tt(s,-1,1)),Jr(s)<.99999?(c[0]=_e(-u,l),c[1]=_e(-h,n)):(c[0]=0,c[1]=_e(o,d));break;case"XZY":c[2]=wt(-Tt(a,-1,1)),Jr(a)<.99999?(c[0]=_e(f,l),c[1]=_e(o,n)):(c[0]=_e(-u,d),c[1]=0);break;default:console.warn("Unkown order: "+v)}return e._dirty=!0,e};Object.defineProperties(R,{POSITIVE_X:{get:function(){return new R(1,0,0)}},NEGATIVE_X:{get:function(){return new R(-1,0,0)}},POSITIVE_Y:{get:function(){return new R(0,1,0)}},NEGATIVE_Y:{get:function(){return new R(0,-1,0)}},POSITIVE_Z:{get:function(){return new R(0,0,1)}},NEGATIVE_Z:{get:function(){return new R(0,0,-1)}},UP:{get:function(){return new R(0,1,0)}},ZERO:{get:function(){return new R}}});var Wa=1e-5,Gr=function(e,t){this.origin=e||new R,this.direction=t||new R};Gr.prototype={constructor:Gr,intersectPlane:function(e,t){var r=e.normal.array,i=e.distance,n=this.origin.array,a=this.direction.array,o=E.dot(r,a);if(o===0)return null;t||(t=new R);var s=(E.dot(r,n)-i)/o;return E.scaleAndAdd(t.array,n,a,-s),t._dirty=!0,t},mirrorAgainstPlane:function(e){var t=E.dot(e.normal.array,this.direction.array);E.scaleAndAdd(this.direction.array,this.direction.array,e.normal.array,-t*2),this.direction._dirty=!0},distanceToPoint:function(){var e=E.create();return function(t){E.sub(e,t,this.origin.array);var r=E.dot(e,this.direction.array);if(r<0)return E.distance(this.origin.array,t);var i=E.lenSquared(e);return Math.sqrt(i-r*r)}}(),intersectSphere:function(){var e=E.create();return function(t,r,i){var n=this.origin.array,a=this.direction.array;t=t.array,E.sub(e,t,n);var o=E.dot(e,a),s=E.squaredLength(e),l=s-o*o,u=r*r;if(!(l>u)){var h=Math.sqrt(u-l),f=o-h,d=o+h;return i||(i=new R),f<0?d<0?null:(E.scaleAndAdd(i.array,n,a,d),i):(E.scaleAndAdd(i.array,n,a,f),i)}}}(),intersectBoundingBox:function(e,t){var r=this.direction.array,i=this.origin.array,n=e.min.array,a=e.max.array,o=1/r[0],s=1/r[1],l=1/r[2],u,h,f,d,c,v;if(o>=0?(u=(n[0]-i[0])*o,h=(a[0]-i[0])*o):(h=(n[0]-i[0])*o,u=(a[0]-i[0])*o),s>=0?(f=(n[1]-i[1])*s,d=(a[1]-i[1])*s):(d=(n[1]-i[1])*s,f=(a[1]-i[1])*s),u>d||f>h||((f>u||u!==u)&&(u=f),(d<h||h!==h)&&(h=d),l>=0?(c=(n[2]-i[2])*l,v=(a[2]-i[2])*l):(v=(n[2]-i[2])*l,c=(a[2]-i[2])*l),u>v||c>h)||((c>u||u!==u)&&(u=c),(v<h||h!==h)&&(h=v),h<0))return null;var p=u>=0?u:h;return t||(t=new R),E.scaleAndAdd(t.array,i,r,p),t},intersectTriangle:function(){var e=E.create(),t=E.create(),r=E.create(),i=E.create();return function(n,a,o,s,l,u){var h=this.direction.array,f=this.origin.array;n=n.array,a=a.array,o=o.array,E.sub(e,a,n),E.sub(t,o,n),E.cross(i,t,h);var d=E.dot(e,i);if(s){if(d>-Wa)return null}else if(d>-Wa&&d<Wa)return null;E.sub(r,f,n);var c=E.dot(i,r)/d;if(c<0||c>1)return null;E.cross(i,e,r);var v=E.dot(h,i)/d;if(v<0||v>1||c+v>1)return null;E.cross(i,e,t);var p=-E.dot(r,i)/d;return p<0?null:(l||(l=new R),u&&R.set(u,1-c-v,c,v),E.scaleAndAdd(l.array,f,h,p),l)}}(),applyTransform:function(e){R.add(this.direction,this.direction,this.origin),R.transformMat4(this.origin,this.origin,e),R.transformMat4(this.direction,this.direction,e),R.sub(this.direction,this.direction,this.origin),R.normalize(this.direction,this.direction)},copy:function(e){R.copy(this.origin,e.origin),R.copy(this.direction,e.direction)},clone:function(){var e=new Gr;return e.copy(this),e}};var G={};G.create=function(){var e=new et(4);return e[0]=0,e[1]=0,e[2]=0,e[3]=0,e};G.clone=function(e){var t=new et(4);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3],t};G.fromValues=function(e,t,r,i){var n=new et(4);return n[0]=e,n[1]=t,n[2]=r,n[3]=i,n};G.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e};G.set=function(e,t,r,i,n){return e[0]=t,e[1]=r,e[2]=i,e[3]=n,e};G.add=function(e,t,r){return e[0]=t[0]+r[0],e[1]=t[1]+r[1],e[2]=t[2]+r[2],e[3]=t[3]+r[3],e};G.subtract=function(e,t,r){return e[0]=t[0]-r[0],e[1]=t[1]-r[1],e[2]=t[2]-r[2],e[3]=t[3]-r[3],e};G.sub=G.subtract;G.multiply=function(e,t,r){return e[0]=t[0]*r[0],e[1]=t[1]*r[1],e[2]=t[2]*r[2],e[3]=t[3]*r[3],e};G.mul=G.multiply;G.divide=function(e,t,r){return e[0]=t[0]/r[0],e[1]=t[1]/r[1],e[2]=t[2]/r[2],e[3]=t[3]/r[3],e};G.div=G.divide;G.min=function(e,t,r){return e[0]=Math.min(t[0],r[0]),e[1]=Math.min(t[1],r[1]),e[2]=Math.min(t[2],r[2]),e[3]=Math.min(t[3],r[3]),e};G.max=function(e,t,r){return e[0]=Math.max(t[0],r[0]),e[1]=Math.max(t[1],r[1]),e[2]=Math.max(t[2],r[2]),e[3]=Math.max(t[3],r[3]),e};G.scale=function(e,t,r){return e[0]=t[0]*r,e[1]=t[1]*r,e[2]=t[2]*r,e[3]=t[3]*r,e};G.scaleAndAdd=function(e,t,r,i){return e[0]=t[0]+r[0]*i,e[1]=t[1]+r[1]*i,e[2]=t[2]+r[2]*i,e[3]=t[3]+r[3]*i,e};G.distance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1],n=t[2]-e[2],a=t[3]-e[3];return Math.sqrt(r*r+i*i+n*n+a*a)};G.dist=G.distance;G.squaredDistance=function(e,t){var r=t[0]-e[0],i=t[1]-e[1],n=t[2]-e[2],a=t[3]-e[3];return r*r+i*i+n*n+a*a};G.sqrDist=G.squaredDistance;G.length=function(e){var t=e[0],r=e[1],i=e[2],n=e[3];return Math.sqrt(t*t+r*r+i*i+n*n)};G.len=G.length;G.squaredLength=function(e){var t=e[0],r=e[1],i=e[2],n=e[3];return t*t+r*r+i*i+n*n};G.sqrLen=G.squaredLength;G.negate=function(e,t){return e[0]=-t[0],e[1]=-t[1],e[2]=-t[2],e[3]=-t[3],e};G.inverse=function(e,t){return e[0]=1/t[0],e[1]=1/t[1],e[2]=1/t[2],e[3]=1/t[3],e};G.normalize=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=r*r+i*i+n*n+a*a;return o>0&&(o=1/Math.sqrt(o),e[0]=t[0]*o,e[1]=t[1]*o,e[2]=t[2]*o,e[3]=t[3]*o),e};G.dot=function(e,t){return e[0]*t[0]+e[1]*t[1]+e[2]*t[2]+e[3]*t[3]};G.lerp=function(e,t,r,i){var n=t[0],a=t[1],o=t[2],s=t[3];return e[0]=n+i*(r[0]-n),e[1]=a+i*(r[1]-a),e[2]=o+i*(r[2]-o),e[3]=s+i*(r[3]-s),e};G.random=function(e,t){return t=t||1,e[0]=si(),e[1]=si(),e[2]=si(),e[3]=si(),G.normalize(e,e),G.scale(e,e,t),e};G.transformMat4=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3];return e[0]=r[0]*i+r[4]*n+r[8]*a+r[12]*o,e[1]=r[1]*i+r[5]*n+r[9]*a+r[13]*o,e[2]=r[2]*i+r[6]*n+r[10]*a+r[14]*o,e[3]=r[3]*i+r[7]*n+r[11]*a+r[15]*o,e};G.transformQuat=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=r[0],s=r[1],l=r[2],u=r[3],h=u*i+s*a-l*n,f=u*n+l*i-o*a,d=u*a+o*n-s*i,c=-o*i-s*n-l*a;return e[0]=h*u+c*-o+f*-l-d*-s,e[1]=f*u+c*-s+d*-o-h*-l,e[2]=d*u+c*-l+h*-s-f*-o,e};G.forEach=function(){var e=G.create();return function(t,r,i,n,a,o){var s,l;for(r||(r=4),i||(i=0),n?l=Math.min(n*r+i,t.length):l=t.length,s=i;s<l;s+=r)e[0]=t[s],e[1]=t[s+1],e[2]=t[s+2],e[3]=t[s+3],a(e,e,o),t[s]=e[0],t[s+1]=e[1],t[s+2]=e[2],t[s+3]=e[3];return t}}();var K={};K.create=function(){var e=new et(9);return e[0]=1,e[1]=0,e[2]=0,e[3]=0,e[4]=1,e[5]=0,e[6]=0,e[7]=0,e[8]=1,e};K.fromMat4=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[4],e[4]=t[5],e[5]=t[6],e[6]=t[8],e[7]=t[9],e[8]=t[10],e};K.clone=function(e){var t=new et(9);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3],t[4]=e[4],t[5]=e[5],t[6]=e[6],t[7]=e[7],t[8]=e[8],t};K.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e[4]=t[4],e[5]=t[5],e[6]=t[6],e[7]=t[7],e[8]=t[8],e};K.identity=function(e){return e[0]=1,e[1]=0,e[2]=0,e[3]=0,e[4]=1,e[5]=0,e[6]=0,e[7]=0,e[8]=1,e};K.transpose=function(e,t){if(e===t){var r=t[1],i=t[2],n=t[5];e[1]=t[3],e[2]=t[6],e[3]=r,e[5]=t[7],e[6]=i,e[7]=n}else e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8];return e};K.invert=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=t[6],u=t[7],h=t[8],f=h*o-s*u,d=-h*a+s*l,c=u*a-o*l,v=r*f+i*d+n*c;return v?(v=1/v,e[0]=f*v,e[1]=(-h*i+n*u)*v,e[2]=(s*i-n*o)*v,e[3]=d*v,e[4]=(h*r-n*l)*v,e[5]=(-s*r+n*a)*v,e[6]=c*v,e[7]=(-u*r+i*l)*v,e[8]=(o*r-i*a)*v,e):null};K.adjoint=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=t[6],u=t[7],h=t[8];return e[0]=o*h-s*u,e[1]=n*u-i*h,e[2]=i*s-n*o,e[3]=s*l-a*h,e[4]=r*h-n*l,e[5]=n*a-r*s,e[6]=a*u-o*l,e[7]=i*l-r*u,e[8]=r*o-i*a,e};K.determinant=function(e){var t=e[0],r=e[1],i=e[2],n=e[3],a=e[4],o=e[5],s=e[6],l=e[7],u=e[8];return t*(u*a-o*l)+r*(-u*n+o*s)+i*(l*n-a*s)};K.multiply=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=t[6],h=t[7],f=t[8],d=r[0],c=r[1],v=r[2],p=r[3],_=r[4],m=r[5],g=r[6],y=r[7],x=r[8];return e[0]=d*i+c*o+v*u,e[1]=d*n+c*s+v*h,e[2]=d*a+c*l+v*f,e[3]=p*i+_*o+m*u,e[4]=p*n+_*s+m*h,e[5]=p*a+_*l+m*f,e[6]=g*i+y*o+x*u,e[7]=g*n+y*s+x*h,e[8]=g*a+y*l+x*f,e};K.mul=K.multiply;K.translate=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=t[6],h=t[7],f=t[8],d=r[0],c=r[1];return e[0]=i,e[1]=n,e[2]=a,e[3]=o,e[4]=s,e[5]=l,e[6]=d*i+c*o+u,e[7]=d*n+c*s+h,e[8]=d*a+c*l+f,e};K.rotate=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=t[6],h=t[7],f=t[8],d=Math.sin(r),c=Math.cos(r);return e[0]=c*i+d*o,e[1]=c*n+d*s,e[2]=c*a+d*l,e[3]=c*o-d*i,e[4]=c*s-d*n,e[5]=c*l-d*a,e[6]=u,e[7]=h,e[8]=f,e};K.scale=function(e,t,r){var i=r[0],n=r[1];return e[0]=i*t[0],e[1]=i*t[1],e[2]=i*t[2],e[3]=n*t[3],e[4]=n*t[4],e[5]=n*t[5],e[6]=t[6],e[7]=t[7],e[8]=t[8],e};K.fromMat2d=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=0,e[3]=t[2],e[4]=t[3],e[5]=0,e[6]=t[4],e[7]=t[5],e[8]=1,e};K.fromQuat=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=r+r,s=i+i,l=n+n,u=r*o,h=i*o,f=i*s,d=n*o,c=n*s,v=n*l,p=a*o,_=a*s,m=a*l;return e[0]=1-f-v,e[3]=h-m,e[6]=d+_,e[1]=h+m,e[4]=1-u-v,e[7]=c-p,e[2]=d-_,e[5]=c+p,e[8]=1-u-f,e};K.normalFromMat4=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=t[6],u=t[7],h=t[8],f=t[9],d=t[10],c=t[11],v=t[12],p=t[13],_=t[14],m=t[15],g=r*s-i*o,y=r*l-n*o,x=r*u-a*o,w=i*l-n*s,T=i*u-a*s,b=n*u-a*l,A=h*p-f*v,C=h*_-d*v,D=h*m-c*v,L=f*_-d*p,M=f*m-c*p,P=d*m-c*_,N=g*P-y*M+x*L+w*D-T*C+b*A;return N?(N=1/N,e[0]=(s*P-l*M+u*L)*N,e[1]=(l*D-o*P-u*C)*N,e[2]=(o*M-s*D+u*A)*N,e[3]=(n*M-i*P-a*L)*N,e[4]=(r*P-n*D+a*C)*N,e[5]=(i*D-r*M-a*A)*N,e[6]=(p*b-_*T+m*w)*N,e[7]=(_*x-v*b-m*y)*N,e[8]=(v*T-p*x+m*g)*N,e):null};K.frob=function(e){return Math.sqrt(Math.pow(e[0],2)+Math.pow(e[1],2)+Math.pow(e[2],2)+Math.pow(e[3],2)+Math.pow(e[4],2)+Math.pow(e[5],2)+Math.pow(e[6],2)+Math.pow(e[7],2)+Math.pow(e[8],2))};var X={};X.create=function(){var e=new et(4);return e[0]=0,e[1]=0,e[2]=0,e[3]=1,e};X.rotationTo=function(){var e=E.create(),t=E.fromValues(1,0,0),r=E.fromValues(0,1,0);return function(i,n,a){var o=E.dot(n,a);return o<-.999999?(E.cross(e,t,n),E.length(e)<1e-6&&E.cross(e,r,n),E.normalize(e,e),X.setAxisAngle(i,e,Math.PI),i):o>.999999?(i[0]=0,i[1]=0,i[2]=0,i[3]=1,i):(E.cross(e,n,a),i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=1+o,X.normalize(i,i))}}();X.setAxes=function(){var e=K.create();return function(t,r,i,n){return e[0]=i[0],e[3]=i[1],e[6]=i[2],e[1]=n[0],e[4]=n[1],e[7]=n[2],e[2]=-r[0],e[5]=-r[1],e[8]=-r[2],X.normalize(t,X.fromMat3(t,e))}}();X.clone=G.clone;X.fromValues=G.fromValues;X.copy=G.copy;X.set=G.set;X.identity=function(e){return e[0]=0,e[1]=0,e[2]=0,e[3]=1,e};X.setAxisAngle=function(e,t,r){r=r*.5;var i=Math.sin(r);return e[0]=i*t[0],e[1]=i*t[1],e[2]=i*t[2],e[3]=Math.cos(r),e};X.add=G.add;X.multiply=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=r[0],l=r[1],u=r[2],h=r[3];return e[0]=i*h+o*s+n*u-a*l,e[1]=n*h+o*l+a*s-i*u,e[2]=a*h+o*u+i*l-n*s,e[3]=o*h-i*s-n*l-a*u,e};X.mul=X.multiply;X.scale=G.scale;X.rotateX=function(e,t,r){r*=.5;var i=t[0],n=t[1],a=t[2],o=t[3],s=Math.sin(r),l=Math.cos(r);return e[0]=i*l+o*s,e[1]=n*l+a*s,e[2]=a*l-n*s,e[3]=o*l-i*s,e};X.rotateY=function(e,t,r){r*=.5;var i=t[0],n=t[1],a=t[2],o=t[3],s=Math.sin(r),l=Math.cos(r);return e[0]=i*l-a*s,e[1]=n*l+o*s,e[2]=a*l+i*s,e[3]=o*l-n*s,e};X.rotateZ=function(e,t,r){r*=.5;var i=t[0],n=t[1],a=t[2],o=t[3],s=Math.sin(r),l=Math.cos(r);return e[0]=i*l+n*s,e[1]=n*l-i*s,e[2]=a*l+o*s,e[3]=o*l-a*s,e};X.calculateW=function(e,t){var r=t[0],i=t[1],n=t[2];return e[0]=r,e[1]=i,e[2]=n,e[3]=Math.sqrt(Math.abs(1-r*r-i*i-n*n)),e};X.dot=G.dot;X.lerp=G.lerp;X.slerp=function(e,t,r,i){var n=t[0],a=t[1],o=t[2],s=t[3],l=r[0],u=r[1],h=r[2],f=r[3],d,c,v,p,_;return c=n*l+a*u+o*h+s*f,c<0&&(c=-c,l=-l,u=-u,h=-h,f=-f),1-c>1e-6?(d=Math.acos(c),v=Math.sin(d),p=Math.sin((1-i)*d)/v,_=Math.sin(i*d)/v):(p=1-i,_=i),e[0]=p*n+_*l,e[1]=p*a+_*u,e[2]=p*o+_*h,e[3]=p*s+_*f,e};X.invert=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=r*r+i*i+n*n+a*a,s=o?1/o:0;return e[0]=-r*s,e[1]=-i*s,e[2]=-n*s,e[3]=a*s,e};X.conjugate=function(e,t){return e[0]=-t[0],e[1]=-t[1],e[2]=-t[2],e[3]=t[3],e};X.length=G.length;X.len=X.length;X.squaredLength=G.squaredLength;X.sqrLen=X.squaredLength;X.normalize=G.normalize;X.fromMat3=function(e,t){var r=t[0]+t[4]+t[8],i;if(r>0)i=Math.sqrt(r+1),e[3]=.5*i,i=.5/i,e[0]=(t[5]-t[7])*i,e[1]=(t[6]-t[2])*i,e[2]=(t[1]-t[3])*i;else{var n=0;t[4]>t[0]&&(n=1),t[8]>t[n*3+n]&&(n=2);var a=(n+1)%3,o=(n+2)%3;i=Math.sqrt(t[n*3+n]-t[a*3+a]-t[o*3+o]+1),e[n]=.5*i,i=.5/i,e[3]=(t[a*3+o]-t[o*3+a])*i,e[a]=(t[a*3+n]+t[n*3+a])*i,e[o]=(t[o*3+n]+t[n*3+o])*i}return e};var W=function(){this._axisX=new R,this._axisY=new R,this._axisZ=new R,this.array=z.create(),this._dirty=!0};W.prototype={constructor:W,setArray:function(e){for(var t=0;t<this.array.length;t++)this.array[t]=e[t];return this._dirty=!0,this},adjoint:function(){return z.adjoint(this.array,this.array),this._dirty=!0,this},clone:function(){return new W().copy(this)},copy:function(e){return z.copy(this.array,e.array),this._dirty=!0,this},determinant:function(){return z.determinant(this.array)},fromQuat:function(e){return z.fromQuat(this.array,e.array),this._dirty=!0,this},fromRotationTranslation:function(e,t){return z.fromRotationTranslation(this.array,e.array,t.array),this._dirty=!0,this},fromMat2d:function(e){return W.fromMat2d(this,e),this},frustum:function(e,t,r,i,n,a){return z.frustum(this.array,e,t,r,i,n,a),this._dirty=!0,this},identity:function(){return z.identity(this.array),this._dirty=!0,this},invert:function(){return z.invert(this.array,this.array),this._dirty=!0,this},lookAt:function(e,t,r){return z.lookAt(this.array,e.array,t.array,r.array),this._dirty=!0,this},mul:function(e){return z.mul(this.array,this.array,e.array),this._dirty=!0,this},mulLeft:function(e){return z.mul(this.array,e.array,this.array),this._dirty=!0,this},multiply:function(e){return z.multiply(this.array,this.array,e.array),this._dirty=!0,this},multiplyLeft:function(e){return z.multiply(this.array,e.array,this.array),this._dirty=!0,this},ortho:function(e,t,r,i,n,a){return z.ortho(this.array,e,t,r,i,n,a),this._dirty=!0,this},perspective:function(e,t,r,i){return z.perspective(this.array,e,t,r,i),this._dirty=!0,this},rotate:function(e,t){return z.rotate(this.array,this.array,e,t.array),this._dirty=!0,this},rotateX:function(e){return z.rotateX(this.array,this.array,e),this._dirty=!0,this},rotateY:function(e){return z.rotateY(this.array,this.array,e),this._dirty=!0,this},rotateZ:function(e){return z.rotateZ(this.array,this.array,e),this._dirty=!0,this},scale:function(e){return z.scale(this.array,this.array,e.array),this._dirty=!0,this},translate:function(e){return z.translate(this.array,this.array,e.array),this._dirty=!0,this},transpose:function(){return z.transpose(this.array,this.array),this._dirty=!0,this},decomposeMatrix:function(){var e=E.create(),t=E.create(),r=E.create(),i=K.create();return function(n,a,o){var s=this.array;E.set(e,s[0],s[1],s[2]),E.set(t,s[4],s[5],s[6]),E.set(r,s[8],s[9],s[10]);var l=E.length(e),u=E.length(t),h=E.length(r),f=this.determinant();f<0&&(l=-l),n&&n.set(l,u,h),o.set(s[12],s[13],s[14]),K.fromMat4(i,s),i[0]/=l,i[1]/=l,i[2]/=l,i[3]/=u,i[4]/=u,i[5]/=u,i[6]/=h,i[7]/=h,i[8]/=h,X.fromMat3(a.array,i),X.normalize(a.array,a.array),a._dirty=!0,o._dirty=!0}}(),toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};var Nn=Object.defineProperty;if(Nn){var Xa=W.prototype;Nn(Xa,"z",{get:function(){var e=this.array;return this._axisZ.set(e[8],e[9],e[10]),this._axisZ},set:function(e){var t=this.array;e=e.array,t[8]=e[0],t[9]=e[1],t[10]=e[2],this._dirty=!0}}),Nn(Xa,"y",{get:function(){var e=this.array;return this._axisY.set(e[4],e[5],e[6]),this._axisY},set:function(e){var t=this.array;e=e.array,t[4]=e[0],t[5]=e[1],t[6]=e[2],this._dirty=!0}}),Nn(Xa,"x",{get:function(){var e=this.array;return this._axisX.set(e[0],e[1],e[2]),this._axisX},set:function(e){var t=this.array;e=e.array,t[0]=e[0],t[1]=e[1],t[2]=e[2],this._dirty=!0}})}W.adjoint=function(e,t){return z.adjoint(e.array,t.array),e._dirty=!0,e};W.copy=function(e,t){return z.copy(e.array,t.array),e._dirty=!0,e};W.determinant=function(e){return z.determinant(e.array)};W.identity=function(e){return z.identity(e.array),e._dirty=!0,e};W.ortho=function(e,t,r,i,n,a,o){return z.ortho(e.array,t,r,i,n,a,o),e._dirty=!0,e};W.perspective=function(e,t,r,i,n){return z.perspective(e.array,t,r,i,n),e._dirty=!0,e};W.lookAt=function(e,t,r,i){return z.lookAt(e.array,t.array,r.array,i.array),e._dirty=!0,e};W.invert=function(e,t){return z.invert(e.array,t.array),e._dirty=!0,e};W.mul=function(e,t,r){return z.mul(e.array,t.array,r.array),e._dirty=!0,e};W.multiply=W.mul;W.fromQuat=function(e,t){return z.fromQuat(e.array,t.array),e._dirty=!0,e};W.fromRotationTranslation=function(e,t,r){return z.fromRotationTranslation(e.array,t.array,r.array),e._dirty=!0,e};W.fromMat2d=function(i,r){i._dirty=!0;var r=r.array,i=i.array;return i[0]=r[0],i[4]=r[2],i[12]=r[4],i[1]=r[1],i[5]=r[3],i[13]=r[5],i};W.rotate=function(e,t,r,i){return z.rotate(e.array,t.array,r,i.array),e._dirty=!0,e};W.rotateX=function(e,t,r){return z.rotateX(e.array,t.array,r),e._dirty=!0,e};W.rotateY=function(e,t,r){return z.rotateY(e.array,t.array,r),e._dirty=!0,e};W.rotateZ=function(e,t,r){return z.rotateZ(e.array,t.array,r),e._dirty=!0,e};W.scale=function(e,t,r){return z.scale(e.array,t.array,r.array),e._dirty=!0,e};W.transpose=function(e,t){return z.transpose(e.array,t.array),e._dirty=!0,e};W.translate=function(e,t,r){return z.translate(e.array,t.array,r.array),e._dirty=!0,e};var pe=function(e,t,r,i){e=e||0,t=t||0,r=r||0,i=i===void 0?1:i,this.array=X.fromValues(e,t,r,i),this._dirty=!0};pe.prototype={constructor:pe,add:function(e){return X.add(this.array,this.array,e.array),this._dirty=!0,this},calculateW:function(){return X.calculateW(this.array,this.array),this._dirty=!0,this},set:function(e,t,r,i){return this.array[0]=e,this.array[1]=t,this.array[2]=r,this.array[3]=i,this._dirty=!0,this},setArray:function(e){return this.array[0]=e[0],this.array[1]=e[1],this.array[2]=e[2],this.array[3]=e[3],this._dirty=!0,this},clone:function(){return new pe(this.x,this.y,this.z,this.w)},conjugate:function(){return X.conjugate(this.array,this.array),this._dirty=!0,this},copy:function(e){return X.copy(this.array,e.array),this._dirty=!0,this},dot:function(e){return X.dot(this.array,e.array)},fromMat3:function(e){return X.fromMat3(this.array,e.array),this._dirty=!0,this},fromMat4:function(){var e=K.create();return function(t){return K.fromMat4(e,t.array),K.transpose(e,e),X.fromMat3(this.array,e),this._dirty=!0,this}}(),identity:function(){return X.identity(this.array),this._dirty=!0,this},invert:function(){return X.invert(this.array,this.array),this._dirty=!0,this},len:function(){return X.len(this.array)},length:function(){return X.length(this.array)},lerp:function(e,t,r){return X.lerp(this.array,e.array,t.array,r),this._dirty=!0,this},mul:function(e){return X.mul(this.array,this.array,e.array),this._dirty=!0,this},mulLeft:function(e){return X.multiply(this.array,e.array,this.array),this._dirty=!0,this},multiply:function(e){return X.multiply(this.array,this.array,e.array),this._dirty=!0,this},multiplyLeft:function(e){return X.multiply(this.array,e.array,this.array),this._dirty=!0,this},normalize:function(){return X.normalize(this.array,this.array),this._dirty=!0,this},rotateX:function(e){return X.rotateX(this.array,this.array,e),this._dirty=!0,this},rotateY:function(e){return X.rotateY(this.array,this.array,e),this._dirty=!0,this},rotateZ:function(e){return X.rotateZ(this.array,this.array,e),this._dirty=!0,this},rotationTo:function(e,t){return X.rotationTo(this.array,e.array,t.array),this._dirty=!0,this},setAxes:function(e,t,r){return X.setAxes(this.array,e.array,t.array,r.array),this._dirty=!0,this},setAxisAngle:function(e,t){return X.setAxisAngle(this.array,e.array,t),this._dirty=!0,this},slerp:function(e,t,r){return X.slerp(this.array,e.array,t.array,r),this._dirty=!0,this},sqrLen:function(){return X.sqrLen(this.array)},squaredLength:function(){return X.squaredLength(this.array)},fromEuler:function(e,t){return pe.fromEuler(this,e,t)},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};var Ni=Object.defineProperty;if(Ni){var In=pe.prototype;Ni(In,"x",{get:function(){return this.array[0]},set:function(e){this.array[0]=e,this._dirty=!0}}),Ni(In,"y",{get:function(){return this.array[1]},set:function(e){this.array[1]=e,this._dirty=!0}}),Ni(In,"z",{get:function(){return this.array[2]},set:function(e){this.array[2]=e,this._dirty=!0}}),Ni(In,"w",{get:function(){return this.array[3]},set:function(e){this.array[3]=e,this._dirty=!0}})}pe.add=function(e,t,r){return X.add(e.array,t.array,r.array),e._dirty=!0,e};pe.set=function(e,t,r,i,n){X.set(e.array,t,r,i,n),e._dirty=!0};pe.copy=function(e,t){return X.copy(e.array,t.array),e._dirty=!0,e};pe.calculateW=function(e,t){return X.calculateW(e.array,t.array),e._dirty=!0,e};pe.conjugate=function(e,t){return X.conjugate(e.array,t.array),e._dirty=!0,e};pe.identity=function(e){return X.identity(e.array),e._dirty=!0,e};pe.invert=function(e,t){return X.invert(e.array,t.array),e._dirty=!0,e};pe.dot=function(e,t){return X.dot(e.array,t.array)};pe.len=function(e){return X.length(e.array)};pe.lerp=function(e,t,r,i){return X.lerp(e.array,t.array,r.array,i),e._dirty=!0,e};pe.slerp=function(e,t,r,i){return X.slerp(e.array,t.array,r.array,i),e._dirty=!0,e};pe.mul=function(e,t,r){return X.multiply(e.array,t.array,r.array),e._dirty=!0,e};pe.multiply=pe.mul;pe.rotateX=function(e,t,r){return X.rotateX(e.array,t.array,r),e._dirty=!0,e};pe.rotateY=function(e,t,r){return X.rotateY(e.array,t.array,r),e._dirty=!0,e};pe.rotateZ=function(e,t,r){return X.rotateZ(e.array,t.array,r),e._dirty=!0,e};pe.setAxisAngle=function(e,t,r){return X.setAxisAngle(e.array,t.array,r),e._dirty=!0,e};pe.normalize=function(e,t){return X.normalize(e.array,t.array),e._dirty=!0,e};pe.sqrLen=function(e){return X.sqrLen(e.array)};pe.squaredLength=pe.sqrLen;pe.fromMat3=function(e,t){return X.fromMat3(e.array,t.array),e._dirty=!0,e};pe.setAxes=function(e,t,r,i){return X.setAxes(e.array,t.array,r.array,i.array),e._dirty=!0,e};pe.rotationTo=function(e,t,r){return X.rotationTo(e.array,t.array,r.array),e._dirty=!0,e};pe.fromEuler=function(e,t,h){e._dirty=!0,t=t.array;var i=e.array,n=Math.cos(t[0]/2),a=Math.cos(t[1]/2),o=Math.cos(t[2]/2),s=Math.sin(t[0]/2),l=Math.sin(t[1]/2),u=Math.sin(t[2]/2),h=(h||"XYZ").toUpperCase();switch(h){case"XYZ":i[0]=s*a*o+n*l*u,i[1]=n*l*o-s*a*u,i[2]=n*a*u+s*l*o,i[3]=n*a*o-s*l*u;break;case"YXZ":i[0]=s*a*o+n*l*u,i[1]=n*l*o-s*a*u,i[2]=n*a*u-s*l*o,i[3]=n*a*o+s*l*u;break;case"ZXY":i[0]=s*a*o-n*l*u,i[1]=n*l*o+s*a*u,i[2]=n*a*u+s*l*o,i[3]=n*a*o-s*l*u;break;case"ZYX":i[0]=s*a*o-n*l*u,i[1]=n*l*o+s*a*u,i[2]=n*a*u-s*l*o,i[3]=n*a*o+s*l*u;break;case"YZX":i[0]=s*a*o+n*l*u,i[1]=n*l*o+s*a*u,i[2]=n*a*u-s*l*o,i[3]=n*a*o-s*l*u;break;case"XZY":i[0]=s*a*o-n*l*u,i[1]=n*l*o-s*a*u,i[2]=n*a*u+s*l*o,i[3]=n*a*o+s*l*u;break}};var lr=E.set,Rn=E.copy,Je=function(e,t){this.min=e||new R(1/0,1/0,1/0),this.max=t||new R(-1/0,-1/0,-1/0),this.vertices=null};Je.prototype={constructor:Je,updateFromVertices:function(e){if(e.length>0){var t=this.min,r=this.max,i=t.array,n=r.array;Rn(i,e[0]),Rn(n,e[0]);for(var a=1;a<e.length;a++){var o=e[a];o[0]<i[0]&&(i[0]=o[0]),o[1]<i[1]&&(i[1]=o[1]),o[2]<i[2]&&(i[2]=o[2]),o[0]>n[0]&&(n[0]=o[0]),o[1]>n[1]&&(n[1]=o[1]),o[2]>n[2]&&(n[2]=o[2])}t._dirty=!0,r._dirty=!0}},union:function(e){var t=this.min,r=this.max;return E.min(t.array,t.array,e.min.array),E.max(r.array,r.array,e.max.array),t._dirty=!0,r._dirty=!0,this},intersection:function(e){var t=this.min,r=this.max;return E.max(t.array,t.array,e.min.array),E.min(r.array,r.array,e.max.array),t._dirty=!0,r._dirty=!0,this},intersectBoundingBox:function(e){var t=this.min.array,r=this.max.array,i=e.min.array,n=e.max.array;return!(t[0]>n[0]||t[1]>n[1]||t[2]>n[2]||r[0]<i[0]||r[1]<i[1]||r[2]<i[2])},containBoundingBox:function(e){var t=this.min.array,r=this.max.array,i=e.min.array,n=e.max.array;return t[0]<=i[0]&&t[1]<=i[1]&&t[2]<=i[2]&&r[0]>=n[0]&&r[1]>=n[1]&&r[2]>=n[2]},containPoint:function(e){var t=this.min.array,r=this.max.array,i=e.array;return t[0]<=i[0]&&t[1]<=i[1]&&t[2]<=i[2]&&r[0]>=i[0]&&r[1]>=i[1]&&r[2]>=i[2]},isFinite:function(){var e=this.min.array,t=this.max.array;return isFinite(e[0])&&isFinite(e[1])&&isFinite(e[2])&&isFinite(t[0])&&isFinite(t[1])&&isFinite(t[2])},applyTransform:function(e){this.transformFrom(this,e)},transformFrom:function(){var e=E.create(),t=E.create(),r=E.create(),i=E.create(),n=E.create(),a=E.create();return function(o,s){var l=o.min.array,u=o.max.array,h=s.array;return e[0]=h[0]*l[0],e[1]=h[1]*l[0],e[2]=h[2]*l[0],t[0]=h[0]*u[0],t[1]=h[1]*u[0],t[2]=h[2]*u[0],r[0]=h[4]*l[1],r[1]=h[5]*l[1],r[2]=h[6]*l[1],i[0]=h[4]*u[1],i[1]=h[5]*u[1],i[2]=h[6]*u[1],n[0]=h[8]*l[2],n[1]=h[9]*l[2],n[2]=h[10]*l[2],a[0]=h[8]*u[2],a[1]=h[9]*u[2],a[2]=h[10]*u[2],l=this.min.array,u=this.max.array,l[0]=Math.min(e[0],t[0])+Math.min(r[0],i[0])+Math.min(n[0],a[0])+h[12],l[1]=Math.min(e[1],t[1])+Math.min(r[1],i[1])+Math.min(n[1],a[1])+h[13],l[2]=Math.min(e[2],t[2])+Math.min(r[2],i[2])+Math.min(n[2],a[2])+h[14],u[0]=Math.max(e[0],t[0])+Math.max(r[0],i[0])+Math.max(n[0],a[0])+h[12],u[1]=Math.max(e[1],t[1])+Math.max(r[1],i[1])+Math.max(n[1],a[1])+h[13],u[2]=Math.max(e[2],t[2])+Math.max(r[2],i[2])+Math.max(n[2],a[2])+h[14],this.min._dirty=!0,this.max._dirty=!0,this}}(),applyProjection:function(e){var t=this.min.array,r=this.max.array,i=e.array,n=t[0],a=t[1],o=t[2],s=r[0],l=r[1],u=t[2],h=r[0],f=r[1],d=r[2];if(i[15]===1)t[0]=i[0]*n+i[12],t[1]=i[5]*a+i[13],r[2]=i[10]*o+i[14],r[0]=i[0]*h+i[12],r[1]=i[5]*f+i[13],t[2]=i[10]*d+i[14];else{var c=-1/o;t[0]=i[0]*n*c,t[1]=i[5]*a*c,r[2]=(i[10]*o+i[14])*c,c=-1/u,r[0]=i[0]*s*c,r[1]=i[5]*l*c,c=-1/d,t[2]=(i[10]*d+i[14])*c}return this.min._dirty=!0,this.max._dirty=!0,this},updateVertices:function(){var e=this.vertices;if(!e){e=[];for(var t=0;t<8;t++)e[t]=E.fromValues(0,0,0);this.vertices=e}var r=this.min.array,i=this.max.array;return lr(e[0],r[0],r[1],r[2]),lr(e[1],r[0],i[1],r[2]),lr(e[2],i[0],r[1],r[2]),lr(e[3],i[0],i[1],r[2]),lr(e[4],r[0],r[1],i[2]),lr(e[5],r[0],i[1],i[2]),lr(e[6],i[0],r[1],i[2]),lr(e[7],i[0],i[1],i[2]),this},copy:function(e){var t=this.min,r=this.max;return Rn(t.array,e.min.array),Rn(r.array,e.max.array),t._dirty=!0,r._dirty=!0,this},clone:function(){var e=new Je;return e.copy(this),e}};var Eg=0,Vt=Qe.extend({name:"",position:null,rotation:null,scale:null,worldTransform:null,localTransform:null,autoUpdateLocalTransform:!0,_parent:null,_scene:null,_needsUpdateWorldTransform:!0,_inIterating:!1,__depth:0},function(){this.name||(this.name=(this.type||"NODE")+"_"+Eg++),this.position||(this.position=new R),this.rotation||(this.rotation=new pe),this.scale||(this.scale=new R(1,1,1)),this.worldTransform=new W,this.localTransform=new W,this._children=[]},{target:null,invisible:!1,isSkinnedMesh:function(){return!1},isRenderable:function(){return!1},setName:function(e){var t=this._scene;if(t){var r=t._nodeRepository;delete r[this.name],r[e]=this}this.name=e},add:function(e){var t=e._parent;if(t!==this){t&&t.remove(e),e._parent=this,this._children.push(e);var r=this._scene;r&&r!==e.scene&&e.traverse(this._addSelfToScene,this),e._needsUpdateWorldTransform=!0}},remove:function(e){var t=this._children,r=t.indexOf(e);r<0||(t.splice(r,1),e._parent=null,this._scene&&e.traverse(this._removeSelfFromScene,this))},removeAll:function(){for(var e=this._children,t=0;t<e.length;t++)e[t]._parent=null,this._scene&&e[t].traverse(this._removeSelfFromScene,this);this._children=[]},getScene:function(){return this._scene},getParent:function(){return this._parent},_removeSelfFromScene:function(e){e._scene.removeFromScene(e),e._scene=null},_addSelfToScene:function(e){this._scene.addToScene(e),e._scene=this._scene},isAncestor:function(e){for(var t=e._parent;t;){if(t===this)return!0;t=t._parent}return!1},children:function(){return this._children.slice()},childAt:function(e){return this._children[e]},getChildByName:function(e){for(var t=this._children,r=0;r<t.length;r++)if(t[r].name===e)return t[r]},getDescendantByName:function(e){for(var t=this._children,r=0;r<t.length;r++){var i=t[r];if(i.name===e)return i;var n=i.getDescendantByName(e);if(n)return n}},queryNode:function(e){if(e){for(var t=e.split("/"),r=this,i=0;i<t.length;i++){var n=t[i];if(n){for(var a=!1,o=r._children,s=0;s<o.length;s++){var l=o[s];if(l.name===n){r=l,a=!0;break}}if(!a)return}}return r}},getPath:function(e){if(!this._parent)return"/";for(var t=this._parent,r=this.name;t._parent&&(r=t.name+"/"+r,t._parent!=e);)t=t._parent;return!t._parent&&e?null:r},traverse:function(e,t){e.call(t,this);for(var r=this._children,i=0,n=r.length;i<n;i++)r[i].traverse(e,t)},eachChild:function(e,t){for(var r=this._children,i=0,n=r.length;i<n;i++){var a=r[i];e.call(t,a,i)}},setLocalTransform:function(e){z.copy(this.localTransform.array,e.array),this.decomposeLocalTransform()},decomposeLocalTransform:function(e){var t=e?null:this.scale;this.localTransform.decomposeMatrix(t,this.rotation,this.position)},setWorldTransform:function(e){z.copy(this.worldTransform.array,e.array),this.decomposeWorldTransform()},decomposeWorldTransform:function(){var e=z.create();return function(t){var r=this.localTransform,i=this.worldTransform;this._parent?(z.invert(e,this._parent.worldTransform.array),z.multiply(r.array,e,i.array)):z.copy(r.array,i.array);var n=t?null:this.scale;r.decomposeMatrix(n,this.rotation,this.position)}}(),transformNeedsUpdate:function(){return this.position._dirty||this.rotation._dirty||this.scale._dirty},updateLocalTransform:function(){var e=this.position,t=this.rotation,r=this.scale;if(this.transformNeedsUpdate()){var i=this.localTransform.array;z.fromRotationTranslation(i,t.array,e.array),z.scale(i,i,r.array),t._dirty=!1,r._dirty=!1,e._dirty=!1,this._needsUpdateWorldTransform=!0}},_updateWorldTransformTopDown:function(){var e=this.localTransform.array,t=this.worldTransform.array;this._parent?z.multiplyAffine(t,this._parent.worldTransform.array,e):z.copy(t,e)},updateWorldTransform:function(){for(var e=this;e&&e.getParent()&&e.getParent().transformNeedsUpdate();)e=e.getParent();e.update()},update:function(e){this.autoUpdateLocalTransform?this.updateLocalTransform():e=!0,(e||this._needsUpdateWorldTransform)&&(this._updateWorldTransformTopDown(),e=!0,this._needsUpdateWorldTransform=!1);for(var t=this._children,r=0,i=t.length;r<i;r++)t[r].update(e)},getBoundingBox:function(){function e(n){return!n.invisible&&n.geometry}var t=new Je,r=new W,i=new W;return function(n,a){return a=a||new Je,this._parent?W.invert(i,this._parent.worldTransform):W.identity(i),this.traverse(function(o){o.geometry&&o.geometry.boundingBox&&(t.copy(o.geometry.boundingBox),W.multiply(r,i,o.worldTransform),t.applyTransform(r),a.union(t))},this,e),a}}(),getWorldPosition:function(e){this.transformNeedsUpdate()&&this.updateWorldTransform();var t=this.worldTransform.array;if(e){var r=e.array;return r[0]=t[12],r[1]=t[13],r[2]=t[14],e}else return new R(t[12],t[13],t[14])},clone:function(){var e=new this.constructor,t=this._children;e.setName(this.name),e.position.copy(this.position),e.rotation.copy(this.rotation),e.scale.copy(this.scale);for(var r=0;r<t.length;r++)e.add(t[r].clone());return e},rotateAround:function(){var e=new R,t=new W;return function(r,i,n){e.copy(this.position).subtract(r);var a=this.localTransform;a.identity(),a.translate(r),a.rotate(n,i),t.fromRotationTranslation(this.rotation,e),a.multiply(t),a.scale(this.scale),this.decomposeLocalTransform(),this._needsUpdateWorldTransform=!0}}(),lookAt:function(){var e=new W;return function(t,r){e.lookAt(this.position,t,r||this.localTransform.y).invert(),this.setLocalTransform(e),this.target=t}}()}),ut=Vt.extend({material:null,geometry:null,mode:F.TRIANGLES,_renderInfo:null},{__program:null,lightGroup:0,renderOrder:0,culling:!0,cullFace:F.BACK,frontFace:F.CCW,frustumCulling:!0,receiveShadow:!0,castShadow:!0,ignorePicking:!1,ignorePreZ:!1,ignoreGBuffer:!1,isRenderable:function(){return this.geometry&&this.material&&this.material.shader&&!this.invisible&&this.geometry.vertexCount>0},beforeRender:function(e){},afterRender:function(e,t){},getBoundingBox:function(e,t){return t=Vt.prototype.getBoundingBox.call(this,e,t),this.geometry&&this.geometry.boundingBox&&t.union(this.geometry.boundingBox),t},clone:function(){var e=["castShadow","receiveShadow","mode","culling","cullFace","frontFace","frustumCulling","renderOrder","lineWidth","ignorePicking","ignorePreZ","ignoreGBuffer"];return function(){var t=Vt.prototype.clone.call(this);t.geometry=this.geometry,t.material=this.material;for(var r=0;r<e.length;r++){var i=e[r];t[i]!==this[i]&&(t[i]=this[i])}return t}}()});ut.POINTS=F.POINTS;ut.LINES=F.LINES;ut.LINE_LOOP=F.LINE_LOOP;ut.LINE_STRIP=F.LINE_STRIP;ut.TRIANGLES=F.TRIANGLES;ut.TRIANGLE_STRIP=F.TRIANGLE_STRIP;ut.TRIANGLE_FAN=F.TRIANGLE_FAN;ut.BACK=F.BACK;ut.FRONT=F.FRONT;ut.FRONT_AND_BACK=F.FRONT_AND_BACK;ut.CW=F.CW;ut.CCW=F.CCW;var ts=Qe.extend({scene:null,camera:null,renderer:null},function(){this._ray=new Gr,this._ndc=new te},{pick:function(e,t,r){var i=this.pickAll(e,t,[],r);return i[0]||null},pickAll:function(e,t,r,i){return this.renderer.screenToNDC(e,t,this._ndc),this.camera.castRay(this._ndc,this._ray),r=r||[],this._intersectNode(this.scene,r,i||!1),r.sort(this._intersectionCompareFunc),r},_intersectNode:function(e,t,r){e instanceof ut&&e.isRenderable()&&(!e.ignorePicking||r)&&(e.mode===F.TRIANGLES&&e.geometry.isUseIndices()||e.geometry.pickByRay||e.geometry.pick)&&this._intersectRenderable(e,t);for(var i=0;i<e._children.length;i++)this._intersectNode(e._children[i],t,r)},_intersectRenderable:function(){var e=new R,t=new R,r=new R,i=new Gr,n=new W;return function(a,o){var s=a.isSkinnedMesh();i.copy(this._ray),W.invert(n,a.worldTransform),s||i.applyTransform(n);var l=a.geometry,u=s?a.skeleton.boundingBox:l.boundingBox;if(!(u&&!i.intersectBoundingBox(u))){if(l.pick){l.pick(this._ndc.x,this._ndc.y,this.renderer,this.camera,a,o);return}else if(l.pickByRay){l.pickByRay(i,a,o);return}var h=a.cullFace===F.BACK&&a.frontFace===F.CCW||a.cullFace===F.FRONT&&a.frontFace===F.CW,f,d=l.indices,c=l.attributes.position,v=l.attributes.weight,p=l.attributes.joint,_,m=[];if(!(!c||!c.value||!d)){if(s){_=a.skeleton.getSubSkinMatrices(a.__uid__,a.joints);for(var g=0;g<a.joints.length;g++){m[g]=m[g]||[];for(var y=0;y<16;y++)m[g][y]=_[g*16+y]}var x=[],w=[],T=[],b=[],A=[],C=l.attributes.skinnedPosition;(!C||!C.value)&&(l.createAttribute("skinnedPosition","f",3),C=l.attributes.skinnedPosition,C.init(l.vertexCount));for(var g=0;g<l.vertexCount;g++){c.get(g,x),v.get(g,w),p.get(g,T),w[3]=1-w[0]-w[1]-w[2],E.set(b,0,0,0);for(var y=0;y<4;y++)T[y]>=0&&w[y]>1e-4&&(E.transformMat4(A,x,m[T[y]]),E.scaleAndAdd(b,b,A,w[y]));C.set(g,b)}}for(var g=0;g<d.length;g+=3){var D=d[g],L=d[g+1],M=d[g+2],P=s?l.attributes.skinnedPosition:c;if(P.get(D,e.array),P.get(L,t.array),P.get(M,r.array),h?f=i.intersectTriangle(e,t,r,a.culling):f=i.intersectTriangle(e,r,t,a.culling),f){var N=new R;s?R.copy(N,f):R.transformMat4(N,f,a.worldTransform),o.push(new ts.Intersection(f,N,a,[D,L,M],g/3,R.dist(N,this._ray.origin)))}}}}}}(),_intersectionCompareFunc:function(e,t){return e.distance-t.distance}});ts.Intersection=function(e,t,r,i,n,a){this.point=e,this.pointWorld=t,this.target=r,this.triangle=i,this.triangleIndex=n,this.distance=a};var Ii="__dt__",pi=function(){this._contextId=0,this._caches=[],this._context={}};pi.prototype={use:function(e,t){var r=this._caches;r[e]||(r[e]={},t&&(r[e]=t())),this._contextId=e,this._context=r[e]},put:function(e,t){this._context[e]=t},get:function(e){return this._context[e]},dirty:function(e){e=e||"";var t=Ii+e;this.put(t,!0)},dirtyAll:function(e){e=e||"";for(var t=Ii+e,r=this._caches,i=0;i<r.length;i++)r[i]&&(r[i][t]=!0)},fresh:function(e){e=e||"";var t=Ii+e;this.put(t,!1)},freshAll:function(e){e=e||"";for(var t=Ii+e,r=this._caches,i=0;i<r.length;i++)r[i]&&(r[i][t]=!1)},isDirty:function(e){e=e||"";var t=Ii+e,r=this._context;return!r.hasOwnProperty(t)||r[t]===!0},deleteContext:function(e){delete this._caches[e],this._context={}},delete:function(e){delete this._context[e]},clearAll:function(){this._caches={}},getContext:function(){return this._context},eachContext:function(e,t){var r=Object.keys(this._caches);r.forEach(function(i){e&&e.call(t,i)})},miss:function(e){return!this._context.hasOwnProperty(e)}};pi.prototype.constructor=pi;var H=Qe.extend({width:512,height:512,type:F.UNSIGNED_BYTE,format:F.RGBA,wrapS:F.REPEAT,wrapT:F.REPEAT,minFilter:F.LINEAR_MIPMAP_LINEAR,magFilter:F.LINEAR,useMipmap:!0,anisotropic:1,flipY:!0,sRGB:!0,unpackAlignment:4,premultiplyAlpha:!1,dynamic:!1,NPOT:!1,__used:0},function(){this._cache=new pi},{getWebGLTexture:function(e){var t=e.gl,r=this._cache;return r.use(e.__uid__),r.miss("webgl_texture")&&r.put("webgl_texture",t.createTexture()),this.dynamic?this.update(e):r.isDirty()&&(this.update(e),r.fresh()),r.get("webgl_texture")},bind:function(){},unbind:function(){},dirty:function(){this._cache&&this._cache.dirtyAll()},update:function(e){},updateCommon:function(e){var t=e.gl;t.pixelStorei(t.UNPACK_FLIP_Y_WEBGL,this.flipY),t.pixelStorei(t.UNPACK_PREMULTIPLY_ALPHA_WEBGL,this.premultiplyAlpha),t.pixelStorei(t.UNPACK_ALIGNMENT,this.unpackAlignment),this.format===F.DEPTH_COMPONENT&&(this.useMipmap=!1);var r=e.getGLExtension("EXT_sRGB");this.format===H.SRGB&&!r&&(this.format=H.RGB),this.format===H.SRGB_ALPHA&&!r&&(this.format=H.RGBA),this.NPOT=!this.isPowerOfTwo()},getAvailableWrapS:function(){return this.NPOT?F.CLAMP_TO_EDGE:this.wrapS},getAvailableWrapT:function(){return this.NPOT?F.CLAMP_TO_EDGE:this.wrapT},getAvailableMinFilter:function(){var e=this.minFilter;return this.NPOT||!this.useMipmap?e===F.NEAREST_MIPMAP_NEAREST||e===F.NEAREST_MIPMAP_LINEAR?F.NEAREST:e===F.LINEAR_MIPMAP_LINEAR||e===F.LINEAR_MIPMAP_NEAREST?F.LINEAR:e:e},getAvailableMagFilter:function(){return this.magFilter},nextHighestPowerOfTwo:function(e){--e;for(var t=1;t<32;t<<=1)e=e|e>>t;return e+1},dispose:function(e){var t=this._cache;t.use(e.__uid__);var r=t.get("webgl_texture");r&&e.gl.deleteTexture(r),t.deleteContext(e.__uid__)},isRenderable:function(){},isPowerOfTwo:function(){}});Object.defineProperty(H.prototype,"width",{get:function(){return this._width},set:function(e){this._width=e}});Object.defineProperty(H.prototype,"height",{get:function(){return this._height},set:function(e){this._height=e}});H.BYTE=F.BYTE;H.UNSIGNED_BYTE=F.UNSIGNED_BYTE;H.SHORT=F.SHORT;H.UNSIGNED_SHORT=F.UNSIGNED_SHORT;H.INT=F.INT;H.UNSIGNED_INT=F.UNSIGNED_INT;H.FLOAT=F.FLOAT;H.HALF_FLOAT=36193;H.UNSIGNED_INT_24_8_WEBGL=34042;H.DEPTH_COMPONENT=F.DEPTH_COMPONENT;H.DEPTH_STENCIL=F.DEPTH_STENCIL;H.ALPHA=F.ALPHA;H.RGB=F.RGB;H.RGBA=F.RGBA;H.LUMINANCE=F.LUMINANCE;H.LUMINANCE_ALPHA=F.LUMINANCE_ALPHA;H.SRGB=35904;H.SRGB_ALPHA=35906;H.COMPRESSED_RGB_S3TC_DXT1_EXT=33776;H.COMPRESSED_RGBA_S3TC_DXT1_EXT=33777;H.COMPRESSED_RGBA_S3TC_DXT3_EXT=33778;H.COMPRESSED_RGBA_S3TC_DXT5_EXT=33779;H.NEAREST=F.NEAREST;H.LINEAR=F.LINEAR;H.NEAREST_MIPMAP_NEAREST=F.NEAREST_MIPMAP_NEAREST;H.LINEAR_MIPMAP_NEAREST=F.LINEAR_MIPMAP_NEAREST;H.NEAREST_MIPMAP_LINEAR=F.NEAREST_MIPMAP_LINEAR;H.LINEAR_MIPMAP_LINEAR=F.LINEAR_MIPMAP_LINEAR;H.REPEAT=F.REPEAT;H.CLAMP_TO_EDGE=F.CLAMP_TO_EDGE;H.MIRRORED_REPEAT=F.MIRRORED_REPEAT;var Xe=ut.extend({skeleton:null,joints:null},function(){this.joints||(this.joints=[])},{offsetMatrix:null,isInstancedMesh:function(){return!1},isSkinnedMesh:function(){return!!(this.skeleton&&this.joints&&this.joints.length>0)},clone:function(){var e=ut.prototype.clone.call(this);return e.skeleton=this.skeleton,this.joints&&(e.joints=this.joints.slice()),e}});Xe.POINTS=F.POINTS;Xe.LINES=F.LINES;Xe.LINE_LOOP=F.LINE_LOOP;Xe.LINE_STRIP=F.LINE_STRIP;Xe.TRIANGLES=F.TRIANGLES;Xe.TRIANGLE_STRIP=F.TRIANGLE_STRIP;Xe.TRIANGLE_FAN=F.TRIANGLE_FAN;Xe.BACK=F.BACK;Xe.FRONT=F.FRONT;Xe.FRONT_AND_BACK=F.FRONT_AND_BACK;Xe.CW=F.CW;Xe.CCW=F.CCW;var pn={};pn.isPowerOfTwo=function(e){return(e&e-1)===0};pn.nextPowerOfTwo=function(e){return e--,e|=e>>1,e|=e>>2,e|=e>>4,e|=e>>8,e|=e>>16,e++,e};pn.nearestPowerOfTwo=function(e){return Math.pow(2,Math.round(Math.log(e)/Math.LN2))};var Kl=pn.isPowerOfTwo;function Jl(e){return Math.pow(2,Math.round(Math.log(e)/Math.LN2))}function Lg(e,t){var r=Jl(e.width),i=Jl(e.height);t=t||document.createElement("canvas"),t.width=r,t.height=i;var n=t.getContext("2d");return n.drawImage(e.image,0,0,r,i),t}var ne=H.extend(function(){return{image:null,pixels:null,mipmaps:[],convertToPOT:!1}},{textureType:"texture2D",update:function(e){var t=e.gl;t.bindTexture(t.TEXTURE_2D,this._cache.get("webgl_texture")),this.updateCommon(e);var r=this.format,i=this.type,n=!!(this.convertToPOT&&!this.mipmaps.length&&this.image&&(this.wrapS===H.REPEAT||this.wrapT===H.REPEAT)&&this.NPOT);t.texParameteri(t.TEXTURE_2D,t.TEXTURE_WRAP_S,n?this.wrapS:this.getAvailableWrapS()),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_WRAP_T,n?this.wrapT:this.getAvailableWrapT()),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_MAG_FILTER,n?this.magFilter:this.getAvailableMagFilter()),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_MIN_FILTER,n?this.minFilter:this.getAvailableMinFilter());var a=e.getGLExtension("EXT_texture_filter_anisotropic");if(a&&this.anisotropic>1&&t.texParameterf(t.TEXTURE_2D,a.TEXTURE_MAX_ANISOTROPY_EXT,this.anisotropic),i===36193){var o=e.getGLExtension("OES_texture_half_float");o||(i=F.FLOAT)}if(this.mipmaps.length)for(var s=this.width,l=this.height,u=0;u<this.mipmaps.length;u++){var h=this.mipmaps[u];this._updateTextureData(t,h,u,s,l,r,i,!1),s/=2,l/=2}else this._updateTextureData(t,this,0,this.width,this.height,r,i,n),this.useMipmap&&(!this.NPOT||n)&&t.generateMipmap(t.TEXTURE_2D);t.bindTexture(t.TEXTURE_2D,null)},_updateTextureData:function(e,t,r,i,n,a,o,s){if(t.image){var l=t.image;s&&(this._potCanvas=Lg(this,this._potCanvas),l=this._potCanvas),e.texImage2D(e.TEXTURE_2D,r,a,a,o,l)}else a<=H.COMPRESSED_RGBA_S3TC_DXT5_EXT&&a>=H.COMPRESSED_RGB_S3TC_DXT1_EXT?e.compressedTexImage2D(e.TEXTURE_2D,r,a,i,n,0,t.pixels):e.texImage2D(e.TEXTURE_2D,r,a,i,n,0,a,o,t.pixels)},generateMipmap:function(e){var t=e.gl;this.useMipmap&&!this.NPOT&&(t.bindTexture(t.TEXTURE_2D,this._cache.get("webgl_texture")),t.generateMipmap(t.TEXTURE_2D))},isPowerOfTwo:function(){return Kl(this.width)&&Kl(this.height)},isRenderable:function(){return this.image?this.image.width>0&&this.image.height>0:!!(this.width&&this.height)},bind:function(e){e.gl.bindTexture(e.gl.TEXTURE_2D,this.getWebGLTexture(e))},unbind:function(e){e.gl.bindTexture(e.gl.TEXTURE_2D,null)},load:function(e,t){var r=de.createImage();t&&(r.crossOrigin=t);var i=this;return r.onload=function(){i.dirty(),i.trigger("success",i)},r.onerror=function(){i.trigger("error",i)},r.src=e,this.image=r,this}});Object.defineProperty(ne.prototype,"width",{get:function(){return this.image?this.image.width:this._width},set:function(e){this.image?console.warn("Texture from image can't set width"):(this._width!==e&&this.dirty(),this._width=e)}});Object.defineProperty(ne.prototype,"height",{get:function(){return this.image?this.image.height:this._height},set:function(e){this.image?console.warn("Texture from image can't set height"):(this._height!==e&&this.dirty(),this._height=e)}});function Wh(e){return{byte:de.Int8Array,ubyte:de.Uint8Array,short:de.Int16Array,ushort:de.Uint16Array}[e]||de.Float32Array}function ja(e){return"attr_"+e}function gi(e,t,r,i){switch(this.name=e,this.type=t,this.size=r,this.semantic=i||"",this.value=null,r){case 1:this.get=function(n){return this.value[n]},this.set=function(n,a){this.value[n]=a},this.copy=function(n,a){this.value[n]=this.value[n]};break;case 2:this.get=function(n,a){var o=this.value;return a[0]=o[n*2],a[1]=o[n*2+1],a},this.set=function(n,a){var o=this.value;o[n*2]=a[0],o[n*2+1]=a[1]},this.copy=function(n,a){var o=this.value;a*=2,n*=2,o[n]=o[a],o[n+1]=o[a+1]};break;case 3:this.get=function(n,a){var o=n*3,s=this.value;return a[0]=s[o],a[1]=s[o+1],a[2]=s[o+2],a},this.set=function(n,a){var o=n*3,s=this.value;s[o]=a[0],s[o+1]=a[1],s[o+2]=a[2]},this.copy=function(n,a){var o=this.value;a*=3,n*=3,o[n]=o[a],o[n+1]=o[a+1],o[n+2]=o[a+2]};break;case 4:this.get=function(n,a){var o=this.value,s=n*4;return a[0]=o[s],a[1]=o[s+1],a[2]=o[s+2],a[3]=o[s+3],a},this.set=function(n,a){var o=this.value,s=n*4;o[s]=a[0],o[s+1]=a[1],o[s+2]=a[2],o[s+3]=a[3]},this.copy=function(n,a){var o=this.value;a*=4,n*=4,o[n]=o[a],o[n+1]=o[a+1],o[n+2]=o[a+2],o[n+3]=o[a+3]}}}gi.prototype.init=function(e){if(!this.value||this.value.length!==e*this.size){var t=Wh(this.type);this.value=new t(e*this.size)}};gi.prototype.fromArray=function(e){var t=Wh(this.type),r;if(e[0]&&e[0].length){var i=0,n=this.size;r=new t(e.length*n);for(var a=0;a<e.length;a++)for(var o=0;o<n;o++)r[i++]=e[a][o]}else r=new t(e);this.value=r};gi.prototype.clone=function(e){var t=new gi(this.name,this.type,this.size,this.semantic);return e&&console.warn("todo"),t};function Xh(e,t,r,i,n){this.name=e,this.type=t,this.buffer=r,this.size=i,this.semantic=n,this.symbol="",this.needsRemove=!1}function jh(e){this.buffer=e,this.count=0}var ht=Qe.extend(function(){return{attributes:{},indices:null,dynamic:!0,_enabledAttributes:null,__used:0}},function(){this._cache=new pi,this._attributeList=Object.keys(this.attributes),this.__vaoCache={}},{mainAttribute:"",pick:null,pickByRay:null,dirty:function(){for(var e=this.getEnabledAttributes(),t=0;t<e.length;t++)this.dirtyAttribute(e[t]);this.dirtyIndices(),this._enabledAttributes=null,this._cache.dirty("any")},dirtyIndices:function(){this._cache.dirtyAll("indices")},dirtyAttribute:function(e){this._cache.dirtyAll(ja(e)),this._cache.dirtyAll("attributes")},getTriangleIndices:function(e,t){if(e<this.triangleCount&&e>=0){t||(t=[]);var r=this.indices;return t[0]=r[e*3],t[1]=r[e*3+1],t[2]=r[e*3+2],t}},setTriangleIndices:function(e,t){var r=this.indices;r[e*3]=t[0],r[e*3+1]=t[1],r[e*3+2]=t[2]},isUseIndices:function(){return!!this.indices},initIndicesFromArray:function(e){var t,r=this.vertexCount>65535?de.Uint32Array:de.Uint16Array;if(e[0]&&e[0].length){var i=0,n=3;t=new r(e.length*n);for(var a=0;a<e.length;a++)for(var o=0;o<n;o++)t[i++]=e[a][o]}else t=new r(e);this.indices=t},createAttribute:function(e,t,r,i){var n=new gi(e,t,r,i);return this.attributes[e]&&this.removeAttribute(e),this.attributes[e]=n,this._attributeList.push(e),n},removeAttribute:function(e){var t=this._attributeList,r=t.indexOf(e);return r>=0?(t.splice(r,1),delete this.attributes[e],!0):!1},getAttribute:function(e){return this.attributes[e]},getEnabledAttributes:function(){var e=this._enabledAttributes,t=this._attributeList;if(e)return e;for(var r=[],i=this.vertexCount,n=0;n<t.length;n++){var a=t[n],o=this.attributes[a];o.value&&o.value.length===i*o.size&&r.push(a)}return this._enabledAttributes=r,r},getBufferChunks:function(e){var t=this._cache;t.use(e.__uid__);var r=t.isDirty("attributes"),i=t.isDirty("indices");if(r||i){this._updateBuffer(e.gl,r,i);for(var n=this.getEnabledAttributes(),a=0;a<n.length;a++)t.fresh(ja(n[a]));t.fresh("attributes"),t.fresh("indices")}return t.fresh("any"),t.get("chunks")},_updateBuffer:function(e,t,r){var i=this._cache,n=i.get("chunks"),a=!1;n||(n=[],n[0]={attributeBuffers:[],indicesBuffer:null},i.put("chunks",n),a=!0);var o=n[0],s=o.attributeBuffers,l=o.indicesBuffer;if(t||a){var u=this.getEnabledAttributes(),h={};if(!a)for(var f=0;f<s.length;f++)h[s[f].name]=s[f];for(var d=0;d<u.length;d++){var c=u[d],v=this.attributes[c],p;a||(p=h[c]);var _;p?_=p.buffer:_=e.createBuffer(),i.isDirty(ja(c))&&(e.bindBuffer(e.ARRAY_BUFFER,_),e.bufferData(e.ARRAY_BUFFER,v.value,this.dynamic?e.DYNAMIC_DRAW:e.STATIC_DRAW)),s[d]=new Xh(c,v.type,_,v.size,v.semantic)}for(var f=d;f<s.length;f++)e.deleteBuffer(s[f].buffer);s.length=d}this.isUseIndices()&&(r||a)&&(l||(l=new jh(e.createBuffer()),o.indicesBuffer=l),l.count=this.indices.length,e.bindBuffer(e.ELEMENT_ARRAY_BUFFER,l.buffer),e.bufferData(e.ELEMENT_ARRAY_BUFFER,this.indices,this.dynamic?e.DYNAMIC_DRAW:e.STATIC_DRAW))},dispose:function(e){var t=this._cache;t.use(e.__uid__);var r=t.get("chunks");if(r)for(var i=0;i<r.length;i++){for(var n=r[i],a=0;a<n.attributeBuffers.length;a++){var o=n.attributeBuffers[a];e.gl.deleteBuffer(o.buffer)}n.indicesBuffer&&e.gl.deleteBuffer(n.indicesBuffer.buffer)}if(this.__vaoCache){var s=e.getGLExtension("OES_vertex_array_object");for(var l in this.__vaoCache){var u=this.__vaoCache[l].vao;u&&s.deleteVertexArrayOES(u)}}this.__vaoCache={},t.deleteContext(e.__uid__)}});Object.defineProperty&&(Object.defineProperty(ht.prototype,"vertexCount",{enumerable:!1,get:function(){var e=this.attributes[this.mainAttribute];return e||(e=this.attributes[this._attributeList[0]]),!e||!e.value?0:e.value.length/e.size}}),Object.defineProperty(ht.prototype,"triangleCount",{enumerable:!1,get:function(){var e=this.indices;return e?e.length/3:0}}));ht.STATIC_DRAW=F.STATIC_DRAW;ht.DYNAMIC_DRAW=F.DYNAMIC_DRAW;ht.STREAM_DRAW=F.STREAM_DRAW;ht.AttributeBuffer=Xh;ht.IndicesBuffer=jh;ht.Attribute=gi;var at=E.create,Qr=E.add,br=E.set,Gt=ht.Attribute,se=ht.extend(function(){return{attributes:{position:new Gt("position","float",3,"POSITION"),texcoord0:new Gt("texcoord0","float",2,"TEXCOORD_0"),texcoord1:new Gt("texcoord1","float",2,"TEXCOORD_1"),normal:new Gt("normal","float",3,"NORMAL"),tangent:new Gt("tangent","float",4,"TANGENT"),color:new Gt("color","float",4,"COLOR"),weight:new Gt("weight","float",3,"WEIGHT"),joint:new Gt("joint","float",4,"JOINT"),barycentric:new Gt("barycentric","float",3,null)},boundingBox:null}},{mainAttribute:"position",updateBoundingBox:function(){var e=this.boundingBox;e||(e=this.boundingBox=new Je);var t=this.attributes.position.value;if(t&&t.length){var r=e.min,i=e.max,n=r.array,a=i.array;E.set(n,t[0],t[1],t[2]),E.set(a,t[0],t[1],t[2]);for(var o=3;o<t.length;){var s=t[o++],l=t[o++],u=t[o++];s<n[0]&&(n[0]=s),l<n[1]&&(n[1]=l),u<n[2]&&(n[2]=u),s>a[0]&&(a[0]=s),l>a[1]&&(a[1]=l),u>a[2]&&(a[2]=u)}r._dirty=!0,i._dirty=!0}},generateVertexNormals:function(){if(this.vertexCount){var e=this.indices,t=this.attributes,r=t.position.value,i=t.normal.value;if(!i||i.length!==r.length)i=t.normal.value=new de.Float32Array(r.length);else for(var n=0;n<i.length;n++)i[n]=0;for(var a=at(),o=at(),s=at(),l=at(),u=at(),h=at(),f=e?e.length:this.vertexCount,d,c,v,p=0;p<f;){e?(d=e[p++],c=e[p++],v=e[p++]):(d=p++,c=p++,v=p++),br(a,r[d*3],r[d*3+1],r[d*3+2]),br(o,r[c*3],r[c*3+1],r[c*3+2]),br(s,r[v*3],r[v*3+1],r[v*3+2]),E.sub(l,a,o),E.sub(u,o,s),E.cross(h,l,u);for(var n=0;n<3;n++)i[d*3+n]=i[d*3+n]+h[n],i[c*3+n]=i[c*3+n]+h[n],i[v*3+n]=i[v*3+n]+h[n]}for(var n=0;n<i.length;)br(h,i[n],i[n+1],i[n+2]),E.normalize(h,h),i[n++]=h[0],i[n++]=h[1],i[n++]=h[2];this.dirty()}},generateFaceNormals:function(){if(this.vertexCount){this.isUniqueVertex()||this.generateUniqueVertex();var e=this.indices,t=this.attributes,r=t.position.value,i=t.normal.value,n=at(),a=at(),o=at(),s=at(),l=at(),u=at();i||(i=t.normal.value=new Float32Array(r.length));for(var h=e?e.length:this.vertexCount,f,d,c,v=0;v<h;){e?(f=e[v++],d=e[v++],c=e[v++]):(f=v++,d=v++,c=v++),br(n,r[f*3],r[f*3+1],r[f*3+2]),br(a,r[d*3],r[d*3+1],r[d*3+2]),br(o,r[c*3],r[c*3+1],r[c*3+2]),E.sub(s,n,a),E.sub(l,a,o),E.cross(u,s,l),E.normalize(u,u);for(var p=0;p<3;p++)i[f*3+p]=u[p],i[d*3+p]=u[p],i[c*3+p]=u[p]}this.dirty()}},generateTangents:function(){if(this.vertexCount){var e=this.vertexCount,t=this.attributes;t.tangent.value||(t.tangent.value=new Float32Array(e*4));var r=t.texcoord0.value,i=t.position.value,n=t.tangent.value,a=t.normal.value;if(!r){console.warn("Geometry without texcoords can't generate tangents.");return}for(var o=[],s=[],l=0;l<e;l++)o[l]=[0,0,0],s[l]=[0,0,0];for(var u=[0,0,0],h=[0,0,0],f=this.indices,d=f?f.length:this.vertexCount,c,v,p,l=0;l<d;){f?(c=f[l++],v=f[l++],p=f[l++]):(c=l++,v=l++,p=l++);var _=r[c*2],m=r[v*2],g=r[p*2],y=r[c*2+1],x=r[v*2+1],w=r[p*2+1],T=i[c*3],b=i[v*3],A=i[p*3],C=i[c*3+1],D=i[v*3+1],L=i[p*3+1],M=i[c*3+2],P=i[v*3+2],N=i[p*3+2],I=b-T,V=A-T,Z=D-C,B=L-C,$=P-M,q=N-M,j=m-_,Q=g-_,ie=x-y,ae=w-y,ee=1/(j*ae-ie*Q);u[0]=(ae*I-ie*V)*ee,u[1]=(ae*Z-ie*B)*ee,u[2]=(ae*$-ie*q)*ee,h[0]=(j*V-Q*I)*ee,h[1]=(j*B-Q*Z)*ee,h[2]=(j*q-Q*$)*ee,Qr(o[c],o[c],u),Qr(o[v],o[v],u),Qr(o[p],o[p],u),Qr(s[c],s[c],h),Qr(s[v],s[v],h),Qr(s[p],s[p],h)}for(var be=at(),Ae=at(),Me=at(),l=0;l<e;l++){Me[0]=a[l*3],Me[1]=a[l*3+1],Me[2]=a[l*3+2];var tt=o[l];E.scale(be,Me,E.dot(Me,tt)),E.sub(be,tt,be),E.normalize(be,be),E.cross(Ae,Me,tt),n[l*4]=be[0],n[l*4+1]=be[1],n[l*4+2]=be[2],n[l*4+3]=E.dot(Ae,s[l])<0?-1:1}this.dirty()}},isUniqueVertex:function(){return this.isUseIndices()?this.vertexCount===this.indices.length:!0},generateUniqueVertex:function(){if(!(!this.vertexCount||!this.indices)){this.indices.length>65535&&(this.indices=new de.Uint32Array(this.indices));for(var e=this.attributes,t=this.indices,r=this.getEnabledAttributes(),i={},n=0;n<r.length;n++){var a=r[n];i[a]=e[a].value,e[a].init(this.indices.length)}for(var o=0,s=0;s<t.length;s++){for(var l=t[s],n=0;n<r.length;n++)for(var a=r[n],u=e[a].value,h=e[a].size,f=0;f<h;f++)u[o*h+f]=i[a][l*h+f];t[s]=o,o++}this.dirty()}},generateBarycentric:function(){if(this.vertexCount){this.isUniqueVertex()||this.generateUniqueVertex();var e=this.attributes,t=e.barycentric.value,r=this.indices;if(!(t&&t.length===r.length*3)){t=e.barycentric.value=new Float32Array(r.length*3);for(var i=0;i<(r?r.length:this.vertexCount/3);)for(var n=0;n<3;n++){var a=r?r[i++]:i*3+n;t[a*3+n]=1}this.dirty()}}},applyTransform:function(e){var t=this.attributes,r=t.position.value,i=t.normal.value,n=t.tangent.value;e=e.array;var a=z.create();z.invert(a,e),z.transpose(a,a);var o=E.transformMat4,s=E.forEach;s(r,3,0,null,o,e),i&&s(i,3,0,null,o,a),n&&s(n,4,0,null,o,a),this.boundingBox&&this.updateBoundingBox()},dispose:function(e){var t=this._cache;t.use(e.__uid__);var r=t.get("chunks");if(r)for(var i=0;i<r.length;i++){for(var n=r[i],a=0;a<n.attributeBuffers.length;a++){var o=n.attributeBuffers[a];e.gl.deleteBuffer(o.buffer)}n.indicesBuffer&&e.gl.deleteBuffer(n.indicesBuffer.buffer)}if(this.__vaoCache){var s=e.getGLExtension("OES_vertex_array_object");for(var l in this.__vaoCache){var u=this.__vaoCache[l].vao;u&&s.deleteVertexArrayOES(u)}}this.__vaoCache={},t.deleteContext(e.__uid__)}});se.STATIC_DRAW=ht.STATIC_DRAW;se.DYNAMIC_DRAW=ht.DYNAMIC_DRAW;se.STREAM_DRAW=ht.STREAM_DRAW;se.AttributeBuffer=ht.AttributeBuffer;se.IndicesBuffer=ht.IndicesBuffer;se.Attribute=Gt;const Cg=`vec3 calcAmbientSHLight(int idx, vec3 N) {
 int offset = 9 * idx;
 return ambientSHLightCoefficients[0]
 + ambientSHLightCoefficients[1] * N.x
 + ambientSHLightCoefficients[2] * N.y
 + ambientSHLightCoefficients[3] * N.z
 + ambientSHLightCoefficients[4] * N.x * N.z
 + ambientSHLightCoefficients[5] * N.z * N.y
 + ambientSHLightCoefficients[6] * N.y * N.x
 + ambientSHLightCoefficients[7] * (3.0 * N.z * N.z - 1.0)
 + ambientSHLightCoefficients[8] * (N.x * N.x - N.y * N.y);
}`;var Mt="uniform vec3 ",Ri="uniform float ",ei="@export clay.header.",ti="@end",Ke=":unconfigurable;";const Mg=[ei+"directional_light",Mt+"directionalLightDirection[DIRECTIONAL_LIGHT_COUNT]"+Ke,Mt+"directionalLightColor[DIRECTIONAL_LIGHT_COUNT]"+Ke,ti,ei+"ambient_light",Mt+"ambientLightColor[AMBIENT_LIGHT_COUNT]"+Ke,ti,ei+"ambient_sh_light",Mt+"ambientSHLightColor[AMBIENT_SH_LIGHT_COUNT]"+Ke,Mt+"ambientSHLightCoefficients[AMBIENT_SH_LIGHT_COUNT * 9]"+Ke,Cg,ti,ei+"ambient_cubemap_light",Mt+"ambientCubemapLightColor[AMBIENT_CUBEMAP_LIGHT_COUNT]"+Ke,"uniform samplerCube ambientCubemapLightCubemap[AMBIENT_CUBEMAP_LIGHT_COUNT]"+Ke,"uniform sampler2D ambientCubemapLightBRDFLookup[AMBIENT_CUBEMAP_LIGHT_COUNT]"+Ke,ti,ei+"point_light",Mt+"pointLightPosition[POINT_LIGHT_COUNT]"+Ke,Ri+"pointLightRange[POINT_LIGHT_COUNT]"+Ke,Mt+"pointLightColor[POINT_LIGHT_COUNT]"+Ke,ti,ei+"spot_light",Mt+"spotLightPosition[SPOT_LIGHT_COUNT]"+Ke,Mt+"spotLightDirection[SPOT_LIGHT_COUNT]"+Ke,Ri+"spotLightRange[SPOT_LIGHT_COUNT]"+Ke,Ri+"spotLightUmbraAngleCosine[SPOT_LIGHT_COUNT]"+Ke,Ri+"spotLightPenumbraAngleCosine[SPOT_LIGHT_COUNT]"+Ke,Ri+"spotLightFalloffFactor[SPOT_LIGHT_COUNT]"+Ke,Mt+"spotLightColor[SPOT_LIGHT_COUNT]"+Ke,ti].join(`
`);k.import(Mg);var It=Vt.extend(function(){return{color:[1,1,1],intensity:1,castShadow:!0,shadowResolution:512,group:0}},{type:"",clone:function(){var e=Vt.prototype.clone.call(this);return e.color=Array.prototype.slice.call(this.color),e.intensity=this.intensity,e.castShadow=this.castShadow,e.shadowResolution=this.shadowResolution,e}}),Wi=function(e,t){this.normal=e||new R(0,1,0),this.distance=t||0};Wi.prototype={constructor:Wi,distanceToPoint:function(e){return E.dot(e.array,this.normal.array)-this.distance},projectPoint:function(e,t){t||(t=new R);var r=this.distanceToPoint(e);return E.scaleAndAdd(t.array,e.array,this.normal.array,-r),t._dirty=!0,t},normalize:function(){var e=1/E.len(this.normal.array);E.scale(this.normal.array,e),this.distance*=e},intersectFrustum:function(e){for(var t=e.vertices,r=this.normal.array,i=E.dot(t[0].array,r)>this.distance,n=1;n<8;n++)if(E.dot(t[n].array,r)>this.distance!=i)return!0},intersectLine:function(){var e=E.create();return function(t,r,i){var n=this.distanceToPoint(t),a=this.distanceToPoint(r);if(n>0&&a>0||n<0&&a<0)return null;var o=this.normal.array,s=this.distance,l=t.array;E.sub(e,r.array,t.array),E.normalize(e,e);var u=E.dot(o,e);if(u===0)return null;i||(i=new R);var h=(E.dot(o,l)-s)/u;return E.scaleAndAdd(i.array,l,e,-h),i._dirty=!0,i}}(),applyTransform:function(){var e=z.create(),t=G.create(),r=G.create();return r[3]=1,function(i){i=i.array,E.scale(r,this.normal.array,this.distance),G.transformMat4(r,r,i),this.distance=E.dot(r,this.normal.array),z.invert(e,i),z.transpose(e,e),t[3]=0,E.copy(t,this.normal.array),G.transformMat4(t,t,e),E.copy(this.normal.array,t)}}(),copy:function(e){E.copy(this.normal.array,e.normal.array),this.normal._dirty=!0,this.distance=e.distance},clone:function(){var e=new Wi;return e.copy(this),e}};var De=E.set,Ql=E.copy,eu=E.transformMat4,Za=Math.min,qa=Math.max,da=function(){this.planes=[];for(var e=0;e<6;e++)this.planes.push(new Wi);this.boundingBox=new Je,this.vertices=[];for(var e=0;e<8;e++)this.vertices[e]=E.fromValues(0,0,0)};da.prototype={setFromProjection:function(e){var t=this.planes,r=e.array,i=r[0],n=r[1],a=r[2],o=r[3],s=r[4],l=r[5],u=r[6],h=r[7],f=r[8],d=r[9],c=r[10],v=r[11],p=r[12],_=r[13],m=r[14],g=r[15];De(t[0].normal.array,o-i,h-s,v-f),t[0].distance=-(g-p),t[0].normalize(),De(t[1].normal.array,o+i,h+s,v+f),t[1].distance=-(g+p),t[1].normalize(),De(t[2].normal.array,o+n,h+l,v+d),t[2].distance=-(g+_),t[2].normalize(),De(t[3].normal.array,o-n,h-l,v-d),t[3].distance=-(g-_),t[3].normalize(),De(t[4].normal.array,o-a,h-u,v-c),t[4].distance=-(g-m),t[4].normalize(),De(t[5].normal.array,o+a,h+u,v+c),t[5].distance=-(g+m),t[5].normalize();var y=this.boundingBox,x=this.vertices;if(g===0){var w=l/i,T=-m/(c-1),b=-m/(c+1),A=-b/l,C=-T/l;y.min.set(-A*w,-A,b),y.max.set(A*w,A,T),De(x[0],-A*w,-A,b),De(x[1],-A*w,A,b),De(x[2],A*w,-A,b),De(x[3],A*w,A,b),De(x[4],-C*w,-C,T),De(x[5],-C*w,C,T),De(x[6],C*w,-C,T),De(x[7],C*w,C,T)}else{var D=(-1-p)/i,L=(1-p)/i,M=(1-_)/l,P=(-1-_)/l,N=(-1-m)/c,I=(1-m)/c;y.min.set(Math.min(D,L),Math.min(P,M),Math.min(I,N)),y.max.set(Math.max(L,D),Math.max(M,P),Math.max(N,I));var V=y.min.array,Z=y.max.array;De(x[0],V[0],V[1],V[2]),De(x[1],V[0],Z[1],V[2]),De(x[2],Z[0],V[1],V[2]),De(x[3],Z[0],Z[1],V[2]),De(x[4],V[0],V[1],Z[2]),De(x[5],V[0],Z[1],Z[2]),De(x[6],Z[0],V[1],Z[2]),De(x[7],Z[0],Z[1],Z[2])}},getTransformedBoundingBox:function(){var e=E.create();return function(t,r){var i=this.vertices,n=r.array,a=t.min,o=t.max,s=a.array,l=o.array,u=i[0];eu(e,u,n),Ql(s,e),Ql(l,e);for(var h=1;h<8;h++)u=i[h],eu(e,u,n),s[0]=Za(e[0],s[0]),s[1]=Za(e[1],s[1]),s[2]=Za(e[2],s[2]),l[0]=qa(e[0],l[0]),l[1]=qa(e[1],l[1]),l[2]=qa(e[2],l[2]);return a._dirty=!0,o._dirty=!0,t}}()};var mi=Vt.extend(function(){return{projectionMatrix:new W,invProjectionMatrix:new W,viewMatrix:new W,frustum:new da}},function(){this.update(!0)},{update:function(e){Vt.prototype.update.call(this,e),W.invert(this.viewMatrix,this.worldTransform),this.updateProjectionMatrix(),W.invert(this.invProjectionMatrix,this.projectionMatrix),this.frustum.setFromProjection(this.projectionMatrix)},setViewMatrix:function(e){W.copy(this.viewMatrix,e),W.invert(this.worldTransform,e),this.decomposeWorldTransform()},decomposeProjectionMatrix:function(){},setProjectionMatrix:function(e){W.copy(this.projectionMatrix,e),W.invert(this.invProjectionMatrix,e),this.decomposeProjectionMatrix()},updateProjectionMatrix:function(){},castRay:function(){var e=G.create();return function(t,r){var i=r!==void 0?r:new Gr,n=t.array[0],a=t.array[1];return G.set(e,n,a,-1,1),G.transformMat4(e,e,this.invProjectionMatrix.array),G.transformMat4(e,e,this.worldTransform.array),E.scale(i.origin.array,e,1/e[3]),G.set(e,n,a,1,1),G.transformMat4(e,e,this.invProjectionMatrix.array),G.transformMat4(e,e,this.worldTransform.array),E.scale(e,e,1/e[3]),E.sub(i.direction.array,e,i.origin.array),E.normalize(i.direction.array,i.direction.array),i.direction._dirty=!0,i.origin._dirty=!0,i}}()}),Dg=z.create(),tu=z.create(),Ya={};function Pg(e){var t=[],r=Object.keys(e);r.sort();for(var i=0;i<r.length;i++){var n=r[i];t.push(n+" "+e[n])}var a=t.join(`
`);if(Ya[a])return Ya[a];var o=Pe.genGUID();return Ya[a]=o,o}function va(){this.opaque=[],this.transparent=[],this._opaqueCount=0,this._transparentCount=0}va.prototype.startCount=function(){this._opaqueCount=0,this._transparentCount=0};va.prototype.add=function(e,t){t?this.transparent[this._transparentCount++]=e:this.opaque[this._opaqueCount++]=e};va.prototype.endCount=function(){this.transparent.length=this._transparentCount,this.opaque.length=this._opaqueCount};var _r=Vt.extend(function(){return{material:null,lights:[],viewBoundingBoxLastFrame:new Je,shadowUniforms:{},_cameraList:[],_lightUniforms:{},_previousLightNumber:{},_lightNumber:{},_lightProgramKeys:{},_nodeRepository:{},_renderLists:new jr(20)}},function(){this._scene=this},{addToScene:function(e){e instanceof mi?(this._cameraList.length>0&&console.warn("Found multiple camera in one scene. Use the fist one."),this._cameraList.push(e)):e instanceof It&&this.lights.push(e),e.name&&(this._nodeRepository[e.name]=e)},removeFromScene:function(e){var t;e instanceof mi?(t=this._cameraList.indexOf(e),t>=0&&this._cameraList.splice(t,1)):e instanceof It&&(t=this.lights.indexOf(e),t>=0&&this.lights.splice(t,1)),e.name&&delete this._nodeRepository[e.name]},getNode:function(e){return this._nodeRepository[e]},setMainCamera:function(e){var t=this._cameraList.indexOf(e);t>=0&&this._cameraList.splice(t,1),this._cameraList.unshift(e)},getMainCamera:function(){return this._cameraList[0]},getLights:function(){return this.lights},updateLights:function(){var e=this.lights;this._previousLightNumber=this._lightNumber;for(var t={},r=0;r<e.length;r++){var i=e[r];if(!i.invisible){var n=i.group;t[n]||(t[n]={}),t[n][i.type]=t[n][i.type]||0,t[n][i.type]++}}this._lightNumber=t;for(var a in t)this._lightProgramKeys[a]=Pg(t[a]);this._updateLightUniforms()},cloneNode:function(e){var t=e.clone(),r={};function i(n,a){r[n.__uid__]=a;for(var o=0;o<n._children.length;o++){var s=n._children[o],l=a._children[o];i(s,l)}}return i(e,t),t.traverse(function(n){n.skeleton&&(n.skeleton=n.skeleton.clone(r)),n.material&&(n.material=n.material.clone())}),t},updateRenderList:function(e,t){var r=e.__uid__,i=this._renderLists.get(r);i||(i=new va,this._renderLists.put(r,i)),i.startCount(),t&&(this.viewBoundingBoxLastFrame.min.set(1/0,1/0,1/0),this.viewBoundingBoxLastFrame.max.set(-1/0,-1/0,-1/0));var n=this.material&&this.material.transparent||!1;return this._doUpdateRenderList(this,e,n,i,t),i.endCount(),i},getRenderList:function(e){return this._renderLists.get(e.__uid__)},_doUpdateRenderList:function(e,t,r,i,n){if(!e.invisible)for(var a=0;a<e._children.length;a++){var o=e._children[a];if(o.isRenderable()){var s=o.isSkinnedMesh()?Dg:o.worldTransform.array,l=o.geometry;z.multiplyAffine(tu,t.viewMatrix.array,s),(n&&!l.boundingBox||!this.isFrustumCulled(o,t,tu))&&i.add(o,o.material.transparent||r)}o._children.length>0&&this._doUpdateRenderList(o,t,r,i,n)}},isFrustumCulled:function(){var e=new Je,t=new W;return function(r,i,n){var a=r.boundingBox;if(a||(r.skeleton&&r.skeleton.boundingBox?a=r.skeleton.boundingBox:a=r.geometry.boundingBox),!a)return!1;if(t.array=n,e.transformFrom(a,t),r.castShadow&&this.viewBoundingBoxLastFrame.union(e),r.frustumCulling){if(!e.intersectBoundingBox(i.frustum.boundingBox))return!0;t.array=i.projectionMatrix.array,e.max.array[2]>0&&e.min.array[2]<0&&(e.max.array[2]=-1e-20),e.applyProjection(t);var o=e.min.array,s=e.max.array;if(s[0]<-1||o[0]>1||s[1]<-1||o[1]>1||s[2]<-1||o[2]>1)return!0}return!1}}(),_updateLightUniforms:function(){var e=this.lights;e.sort(Ng);var t=this._lightUniforms;for(var r in t)for(var i in t[r])t[r][i].value.length=0;for(var n=0;n<e.length;n++){var a=e[n];if(!a.invisible){var r=a.group;for(var i in a.uniformTemplates){var o=a.uniformTemplates[i],s=o.value(a);if(s!=null){t[r]||(t[r]={}),t[r][i]||(t[r][i]={type:"",value:[]});var l=t[r][i];switch(l.type=o.type+"v",o.type){case"1i":case"1f":case"t":l.value.push(s);break;case"2f":case"3f":case"4f":for(var u=0;u<s.length;u++)l.value.push(s[u]);break;default:console.error("Unkown light uniform type "+o.type)}}}}}},getLightGroups:function(){var e=[];for(var t in this._lightNumber)e.push(t);return e},getNumberChangedLightGroups:function(){var e=[];for(var t in this._lightNumber)this.isLightNumberChanged(t)&&e.push(t);return e},isLightNumberChanged:function(e){var t=this._previousLightNumber,r=this._lightNumber;for(var i in r[e])if(!t[e]||r[e][i]!==t[e][i])return!0;for(var i in t[e])if(!r[e]||r[e][i]!==t[e][i])return!0;return!1},getLightsNumbers:function(e){return this._lightNumber[e]},getProgramKey:function(e){return this._lightProgramKeys[e]},setLightUniforms:function(){function e(t,r,i){for(var n in t){var a=t[n];if(a.type==="tv"){if(!r.hasUniform(n))continue;for(var o=[],s=0;s<a.value.length;s++){var l=a.value[s],u=r.takeCurrentTextureSlot(i,l);o.push(u)}r.setUniform(i.gl,"1iv",n,o)}else r.setUniform(i.gl,a.type,n,a.value)}}return function(t,r,i){e(this._lightUniforms[r],t,i),e(this.shadowUniforms,t,i)}}(),dispose:function(){this.material=null,this._opaqueList=[],this._transparentList=[],this.lights=[],this._lightUniforms={},this._lightNumber={},this._nodeRepository={}}});function Ng(e,t){if(t.castShadow&&!e.castShadow)return!0}var On=pn.isPowerOfTwo,Ig=["px","nx","py","ny","pz","nz"],Vr=H.extend(function(){return{image:{px:null,nx:null,py:null,ny:null,pz:null,nz:null},pixels:{px:null,nx:null,py:null,ny:null,pz:null,nz:null},mipmaps:[]}},{textureType:"textureCube",update:function(e){var t=e.gl;t.bindTexture(t.TEXTURE_CUBE_MAP,this._cache.get("webgl_texture")),this.updateCommon(e);var r=this.format,i=this.type;t.texParameteri(t.TEXTURE_CUBE_MAP,t.TEXTURE_WRAP_S,this.getAvailableWrapS()),t.texParameteri(t.TEXTURE_CUBE_MAP,t.TEXTURE_WRAP_T,this.getAvailableWrapT()),t.texParameteri(t.TEXTURE_CUBE_MAP,t.TEXTURE_MAG_FILTER,this.getAvailableMagFilter()),t.texParameteri(t.TEXTURE_CUBE_MAP,t.TEXTURE_MIN_FILTER,this.getAvailableMinFilter());var n=e.getGLExtension("EXT_texture_filter_anisotropic");if(n&&this.anisotropic>1&&t.texParameterf(t.TEXTURE_CUBE_MAP,n.TEXTURE_MAX_ANISOTROPY_EXT,this.anisotropic),i===36193){var a=e.getGLExtension("OES_texture_half_float");a||(i=F.FLOAT)}if(this.mipmaps.length)for(var o=this.width,s=this.height,l=0;l<this.mipmaps.length;l++){var u=this.mipmaps[l];this._updateTextureData(t,u,l,o,s,r,i),o/=2,s/=2}else this._updateTextureData(t,this,0,this.width,this.height,r,i),!this.NPOT&&this.useMipmap&&t.generateMipmap(t.TEXTURE_CUBE_MAP);t.bindTexture(t.TEXTURE_CUBE_MAP,null)},_updateTextureData:function(e,t,r,i,n,a,o){for(var s=0;s<6;s++){var l=Ig[s],u=t.image&&t.image[l];u?e.texImage2D(e.TEXTURE_CUBE_MAP_POSITIVE_X+s,r,a,a,o,u):e.texImage2D(e.TEXTURE_CUBE_MAP_POSITIVE_X+s,r,a,i,n,0,a,o,t.pixels&&t.pixels[l])}},generateMipmap:function(e){var t=e.gl;this.useMipmap&&!this.NPOT&&(t.bindTexture(t.TEXTURE_CUBE_MAP,this._cache.get("webgl_texture")),t.generateMipmap(t.TEXTURE_CUBE_MAP))},bind:function(e){e.gl.bindTexture(e.gl.TEXTURE_CUBE_MAP,this.getWebGLTexture(e))},unbind:function(e){e.gl.bindTexture(e.gl.TEXTURE_CUBE_MAP,null)},isPowerOfTwo:function(){return this.image.px?On(this.image.px.width)&&On(this.image.px.height):On(this.width)&&On(this.height)},isRenderable:function(){return this.image.px?ri(this.image.px)&&ri(this.image.nx)&&ri(this.image.py)&&ri(this.image.ny)&&ri(this.image.pz)&&ri(this.image.nz):!!(this.width&&this.height)},load:function(e,t){var r=0,i=this;return Pe.each(e,function(n,a){var o=de.createImage();t&&(o.crossOrigin=t),o.onload=function(){r--,r===0&&(i.dirty(),i.trigger("success",i))},o.onerror=function(){r--},r++,o.src=n,i.image[a]=o}),this}});Object.defineProperty(Vr.prototype,"width",{get:function(){return this.image&&this.image.px?this.image.px.width:this._width},set:function(e){this.image&&this.image.px?console.warn("Texture from image can't set width"):(this._width!==e&&this.dirty(),this._width=e)}});Object.defineProperty(Vr.prototype,"height",{get:function(){return this.image&&this.image.px?this.image.px.height:this._height},set:function(e){this.image&&this.image.px?console.warn("Texture from image can't set height"):(this._height!==e&&this.dirty(),this._height=e)}});function ri(e){return e.width>0&&e.height>0}var We=mi.extend({fov:50,aspect:1,near:.1,far:2e3},{updateProjectionMatrix:function(){var e=this.fov/180*Math.PI;this.projectionMatrix.perspective(e,this.aspect,this.near,this.far)},decomposeProjectionMatrix:function(){var e=this.projectionMatrix.array,t=Math.atan(1/e[5])*2;this.fov=t/Math.PI*180,this.aspect=e[5]/e[0],this.near=e[14]/(e[10]-1),this.far=e[14]/(e[10]+1)},clone:function(){var e=mi.prototype.clone.call(this);return e.fov=this.fov,e.aspect=this.aspect,e.near=this.near,e.far=this.far,e}}),Bn="framebuffer",jt="renderbuffer",ru=jt+"_width",iu=jt+"_height",$a=jt+"_attached",Ka="depthtexture_attached",Ar=F.FRAMEBUFFER,Oi=F.RENDERBUFFER,Ui=F.DEPTH_ATTACHMENT,Zh=F.COLOR_ATTACHMENT0,Ie=Qe.extend({depthBuffer:!0,viewport:null,_width:0,_height:0,_textures:null,_boundRenderer:null},function(){this._cache=new pi,this._textures={}},{getTextureWidth:function(){return this._width},getTextureHeight:function(){return this._height},bind:function(e){if(e.__currentFrameBuffer){if(e.__currentFrameBuffer===this)return;console.warn("Renderer already bound with another framebuffer. Unbind it first")}e.__currentFrameBuffer=this;var t=e.gl;t.bindFramebuffer(Ar,this._getFrameBufferGL(e)),this._boundRenderer=e;var r=this._cache;r.put("viewport",e.viewport);var i=!1,n,a;for(var o in this._textures){i=!0;var s=this._textures[o];s&&(n=s.texture.width,a=s.texture.height,this._doAttach(e,s.texture,o,s.target))}this._width=n,this._height=a,!i&&this.depthBuffer&&console.error("Must attach texture before bind, or renderbuffer may have incorrect width and height."),this.viewport?e.setViewport(this.viewport):e.setViewport(0,0,n,a,1);var l=r.get("attached_textures");if(l){for(var o in l)if(!this._textures[o]){var u=l[o];this._doDetach(t,o,u)}}if(!r.get(Ka)&&this.depthBuffer){r.miss(jt)&&r.put(jt,t.createRenderbuffer());var h=r.get(jt);(n!==r.get(ru)||a!==r.get(iu))&&(t.bindRenderbuffer(Oi,h),t.renderbufferStorage(Oi,t.DEPTH_COMPONENT16,n,a),r.put(ru,n),r.put(iu,a),t.bindRenderbuffer(Oi,null)),r.get($a)||(t.framebufferRenderbuffer(Ar,Ui,Oi,h),r.put($a,!0))}},unbind:function(e){e.__currentFrameBuffer=null;var t=e.gl;t.bindFramebuffer(Ar,null),this._boundRenderer=null,this._cache.use(e.__uid__);var r=this._cache.get("viewport");r&&e.setViewport(r),this.updateMipmap(e)},updateMipmap:function(e){var t=e.gl;for(var r in this._textures){var i=this._textures[r];if(i){var n=i.texture;if(!n.NPOT&&n.useMipmap&&n.minFilter===H.LINEAR_MIPMAP_LINEAR){var a=n.textureType==="textureCube"?F.TEXTURE_CUBE_MAP:F.TEXTURE_2D;t.bindTexture(a,n.getWebGLTexture(e)),t.generateMipmap(a),t.bindTexture(a,null)}}}},checkStatus:function(e){return e.checkFramebufferStatus(Ar)},_getFrameBufferGL:function(e){var t=this._cache;return t.use(e.__uid__),t.miss(Bn)&&t.put(Bn,e.gl.createFramebuffer()),t.get(Bn)},attach:function(e,t,r){if(!e.width)throw new Error("The texture attached to color buffer is not a valid.");t=t||Zh,r=r||F.TEXTURE_2D;var i=this._boundRenderer,n=i&&i.gl,a;if(n){var o=this._cache;o.use(i.__uid__),a=o.get("attached_textures")}var s=this._textures[t];if(!(s&&s.target===r&&s.texture===e&&a&&a[t]!=null)){var l=!0;i&&(l=this._doAttach(i,e,t,r),this.viewport||i.setViewport(0,0,e.width,e.height,1)),l&&(this._textures[t]=this._textures[t]||{},this._textures[t].texture=e,this._textures[t].target=r)}},_doAttach:function(e,t,r,i){var n=e.gl,a=t.getWebGLTexture(e),o=this._cache.get("attached_textures");if(o&&o[r]){var s=o[r];if(s.texture===t&&s.target===i)return}r=+r;var l=!0;if(r===Ui||r===F.DEPTH_STENCIL_ATTACHMENT){var u=e.getGLExtension("WEBGL_depth_texture");if(u||(console.error("Depth texture is not supported by the browser"),l=!1),t.format!==F.DEPTH_COMPONENT&&t.format!==F.DEPTH_STENCIL&&(console.error("The texture attached to depth buffer is not a valid."),l=!1),l){var h=this._cache.get(jt);h&&(n.framebufferRenderbuffer(Ar,Ui,Oi,null),n.deleteRenderbuffer(h),this._cache.put(jt,!1)),this._cache.put($a,!1),this._cache.put(Ka,!0)}}return n.framebufferTexture2D(Ar,r,i,a,0),o||(o={},this._cache.put("attached_textures",o)),o[r]=o[r]||{},o[r].texture=t,o[r].target=i,l},_doDetach:function(e,t,r){e.framebufferTexture2D(Ar,t,r,null,0);var i=this._cache.get("attached_textures");i&&i[t]&&(i[t]=null),(t===Ui||t===F.DEPTH_STENCIL_ATTACHMENT)&&this._cache.put(Ka,!1)},detach:function(e,t){if(this._textures[e]=null,this._boundRenderer){var r=this._cache;r.use(this._boundRenderer.__uid__),this._doDetach(this._boundRenderer.gl,e,t)}},dispose:function(e){var t=e.gl,r=this._cache;r.use(e.__uid__);var i=r.get(jt);i&&t.deleteRenderbuffer(i);var n=r.get(Bn);n&&t.deleteFramebuffer(n),r.deleteContext(e.__uid__),this._textures={}}});Ie.DEPTH_ATTACHMENT=Ui;Ie.COLOR_ATTACHMENT0=Zh;Ie.STENCIL_ATTACHMENT=F.STENCIL_ATTACHMENT;Ie.DEPTH_STENCIL_ATTACHMENT=F.DEPTH_STENCIL_ATTACHMENT;var Rg=["px","nx","py","ny","pz","nz"],rs=Qe.extend(function(){var e={position:new R,far:1e3,near:.1,texture:null,shadowMapPass:null},t=e._cameras={px:new We({fov:90}),nx:new We({fov:90}),py:new We({fov:90}),ny:new We({fov:90}),pz:new We({fov:90}),nz:new We({fov:90})};return t.px.lookAt(R.POSITIVE_X,R.NEGATIVE_Y),t.nx.lookAt(R.NEGATIVE_X,R.NEGATIVE_Y),t.py.lookAt(R.POSITIVE_Y,R.POSITIVE_Z),t.ny.lookAt(R.NEGATIVE_Y,R.NEGATIVE_Z),t.pz.lookAt(R.POSITIVE_Z,R.NEGATIVE_Y),t.nz.lookAt(R.NEGATIVE_Z,R.NEGATIVE_Y),e._frameBuffer=new Ie,e},{getCamera:function(e){return this._cameras[e]},render:function(e,t,r){var i=e.gl;r||t.update();for(var n=this.texture.width,a=2*Math.atan(n/(n-.5))/Math.PI*180,o=0;o<6;o++){var s=Rg[o],l=this._cameras[s];if(R.copy(l.position,this.position),l.far=this.far,l.near=this.near,l.fov=a,this.shadowMapPass){l.update();var u=t.getBoundingBox();u.applyTransform(l.viewMatrix),t.viewBoundingBoxLastFrame.copy(u),this.shadowMapPass.render(e,t,l,!0)}this._frameBuffer.attach(this.texture,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+o),this._frameBuffer.bind(e),e.render(t,l,!0),this._frameBuffer.unbind(e)}},dispose:function(e){this._frameBuffer.dispose(e)}}),pa=se.extend({dynamic:!1,widthSegments:1,heightSegments:1},function(){this.build()},{build:function(){for(var e=this.heightSegments,t=this.widthSegments,r=this.attributes,i=[],n=[],a=[],o=[],s=0;s<=e;s++)for(var l=s/e,u=0;u<=t;u++){var h=u/t;if(i.push([2*h-1,2*l-1,0]),n&&n.push([h,l]),a&&a.push([0,0,1]),u<t&&s<e){var f=u+s*(t+1);o.push([f,f+1,f+t+1]),o.push([f+t+1,f+1,f+t+2])}}r.position.fromArray(i),r.texcoord0.fromArray(n),r.normal.fromArray(a),this.initIndicesFromArray(o),this.boundingBox=new Je,this.boundingBox.min.set(-1,-1,0),this.boundingBox.max.set(1,1,0)}}),Le=new W,qh=se.extend({dynamic:!1,widthSegments:1,heightSegments:1,depthSegments:1,inside:!1},function(){this.build()},{build:function(){var e={px:ii("px",this.depthSegments,this.heightSegments),nx:ii("nx",this.depthSegments,this.heightSegments),py:ii("py",this.widthSegments,this.depthSegments),ny:ii("ny",this.widthSegments,this.depthSegments),pz:ii("pz",this.widthSegments,this.heightSegments),nz:ii("nz",this.widthSegments,this.heightSegments)},t=["position","texcoord0","normal"],r=0,i=0;for(var n in e)r+=e[n].vertexCount,i+=e[n].indices.length;for(var a=0;a<t.length;a++)this.attributes[t[a]].init(r);this.indices=new de.Uint16Array(i);var o=0,s=0;for(var n in e){for(var l=e[n],a=0;a<t.length;a++)for(var u=t[a],h=l.attributes[u].value,f=l.attributes[u].size,d=u==="normal",c=0;c<h.length;c++){var v=h[c];this.inside&&d&&(v=-v),this.attributes[u].value[c+f*s]=v}for(var p=l.indices.length,c=0;c<l.indices.length;c++)this.indices[c+o]=s+l.indices[this.inside?p-c-1:c];o+=l.indices.length,s+=l.vertexCount}this.boundingBox=new Je,this.boundingBox.max.set(1,1,1),this.boundingBox.min.set(-1,-1,-1)}});function ii(e,t,r){Le.identity();var i=new pa({widthSegments:t,heightSegments:r});switch(e){case"px":W.translate(Le,Le,R.POSITIVE_X),W.rotateY(Le,Le,Math.PI/2);break;case"nx":W.translate(Le,Le,R.NEGATIVE_X),W.rotateY(Le,Le,-Math.PI/2);break;case"py":W.translate(Le,Le,R.POSITIVE_Y),W.rotateX(Le,Le,-Math.PI/2);break;case"ny":W.translate(Le,Le,R.NEGATIVE_Y),W.rotateX(Le,Le,Math.PI/2);break;case"pz":W.translate(Le,Le,R.POSITIVE_Z);break;case"nz":W.translate(Le,Le,R.NEGATIVE_Z),W.rotateY(Le,Le,Math.PI);break}return i.applyTransform(Le),i}const Og=`@export clay.skybox.vertex
#define SHADER_NAME skybox
uniform mat4 world : WORLD;
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
attribute vec3 position : POSITION;
varying vec3 v_WorldPosition;
void main()
{
 v_WorldPosition = (world * vec4(position, 1.0)).xyz;
 gl_Position = worldViewProjection * vec4(position, 1.0);
}
@end
@export clay.skybox.fragment
#define PI 3.1415926
uniform mat4 viewInverse : VIEWINVERSE;
#ifdef EQUIRECTANGULAR
uniform sampler2D environmentMap;
#else
uniform samplerCube environmentMap;
#endif
uniform float lod: 0.0;
varying vec3 v_WorldPosition;
@import clay.util.rgbm
@import clay.util.srgb
@import clay.util.ACES
void main()
{
 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(v_WorldPosition - eyePos);
#ifdef EQUIRECTANGULAR
 float phi = acos(V.y);
 float theta = atan(-V.x, V.z) + PI * 0.5;
 vec2 uv = vec2(theta / 2.0 / PI, phi / PI);
 vec4 texel = decodeHDR(texture2D(environmentMap, fract(uv)));
#else
 #if defined(LOD) || defined(SUPPORT_TEXTURE_LOD)
 vec4 texel = decodeHDR(textureCubeLodEXT(environmentMap, V, lod));
 #else
 vec4 texel = decodeHDR(textureCube(environmentMap, V));
 #endif
#endif
#ifdef SRGB_DECODE
 texel = sRGBToLinear(texel);
#endif
#ifdef TONEMAPPING
 texel.rgb = ACESToneMapping(texel.rgb);
#endif
#ifdef SRGB_ENCODE
 texel = linearTosRGB(texel);
#endif
 gl_FragColor = encodeHDR(vec4(texel.rgb, 1.0));
}
@end`;k.import(Og);var Qi=Xe.extend(function(){var e=new k({vertex:k.source("clay.skybox.vertex"),fragment:k.source("clay.skybox.fragment")}),t=new At({shader:e,depthMask:!1});return{scene:null,geometry:new qh,material:t,environmentMap:null,culling:!1,_dummyCamera:new We}},function(){var e=this.scene;e&&this.attachScene(e),this.environmentMap&&this.setEnvironmentMap(this.environmentMap)},{attachScene:function(e){this.scene&&this.detachScene(),e.skybox=this,this.scene=e,e.on("beforerender",this._beforeRenderScene,this)},detachScene:function(){this.scene&&(this.scene.off("beforerender",this._beforeRenderScene),this.scene.skybox=null),this.scene=null},dispose:function(e){this.detachScene(),this.geometry.dispose(e)},setEnvironmentMap:function(e){e.textureType==="texture2D"?(this.material.define("EQUIRECTANGULAR"),e.minFilter=H.LINEAR):this.material.undefine("EQUIRECTANGULAR"),this.material.set("environmentMap",e)},getEnvironmentMap:function(){return this.material.get("environmentMap")},_beforeRenderScene:function(e,t,r){this.renderSkybox(e,r)},renderSkybox:function(e,t){var r=this._dummyCamera;r.aspect=e.getViewportAspect(),r.fov=t.fov||50,r.updateProjectionMatrix(),W.invert(r.invProjectionMatrix,r.projectionMatrix),r.worldTransform.copy(t.worldTransform),r.viewMatrix.copy(t.viewMatrix),this.position.copy(t.getWorldPosition()),this.update(),e.gl.disable(e.gl.BLEND),this.material.get("lod")>0?this.material.define("fragment","LOD"):this.material.undefine("fragment","LOD"),e.renderPass([this],r)}}),Bg=542327876,Fg=131072,Gg=512,zg=4;function is(e){return e.charCodeAt(0)+(e.charCodeAt(1)<<8)+(e.charCodeAt(2)<<16)+(e.charCodeAt(3)<<24)}var Ug=31,Vg=is("DXT1"),Hg=is("DXT3"),kg=is("DXT5"),Wg=0,Xg=1,jg=2,Zg=3,qg=4,Yg=7,$g=20,Kg=21,Jg=28,Qg={parse:function(e,t){var r=new Int32Array(e,0,Ug);if(r[Wg]!==Bg||!r($g)&zg)return null;var i=r(Kg),n=r[qg],a=r[Zg],o=r[Jg]&Gg,s=r[jg]&Fg,l,u;switch(i){case Vg:l=8,u=H.COMPRESSED_RGB_S3TC_DXT1_EXT;break;case Hg:l=16,u=H.COMPRESSED_RGBA_S3TC_DXT3_EXT;break;case kg:l=16,u=H.COMPRESSED_RGBA_S3TC_DXT5_EXT;break;default:return null}var h=r[Xg]+4,f=o?6:1,d=1;s&&(d=Math.max(1,r[Yg]));for(var c=[],v=0;v<f;v++){var p=n,_=a;c[v]=new ne({width:p,height:_,format:u});for(var m=[],g=0;g<d;g++){var y=Math.max(4,p)/4*Math.max(4,_)/4*l,x=new Uint8Array(e,h,y);h+=y,p*=.5,_*=.5,m[g]=x}c[v].pixels=m[0],s&&(c[v].mipmaps=m)}if(t)t.width=c[0].width,t.height=c[0].height,t.format=c[0].format,t.pixels=c[0].pixels,t.mipmaps=c[0].mipmaps;else return c[0]}},jn=String.fromCharCode,em=8,tm=32767;function rm(e,t,r,i){if(e[3]>0){var n=Math.pow(2,e[3]-128-8+i);t[r+0]=e[0]*n,t[r+1]=e[1]*n,t[r+2]=e[2]*n}else t[r+0]=0,t[r+1]=0,t[r+2]=0;return t[r+3]=1,t}function im(e,t,r){for(var i="",n=t;n<r;n++)i+=jn(e[n]);return i}function nm(e,t){t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3]}function nu(e,t,r,i){for(var n=0,a=0,o=i;o>0;)if(e[a][0]=t[r++],e[a][1]=t[r++],e[a][2]=t[r++],e[a][3]=t[r++],e[a][0]===1&&e[a][1]===1&&e[a][2]===1){for(var s=e[a][3]<<n>>>0;s>0;s--)nm(e[a-1],e[a]),a++,o--;n+=8}else a++,o--,n=0;return r}function am(e,t,r,i){if(i<em|i>tm)return nu(e,t,r,i);var n=t[r++];if(n!=2)return nu(e,t,r-1,i);if(e[0][1]=t[r++],e[0][2]=t[r++],n=t[r++],(e[0][2]<<8>>>0|n)>>>0!==i)return null;for(var n=0;n<4;n++)for(var a=0;a<i;){var o=t[r++];if(o>128){o=(o&127)>>>0;for(var s=t[r++];o--;)e[a++][n]=s}else for(;o--;)e[a++][n]=t[r++]}return r}var om={parseRGBE:function(e,t,r){r==null&&(r=0);var i=new Uint8Array(e),n=i.length;if(im(i,0,2)==="#?"){for(var a=2;a<n&&!(jn(i[a])===`
`&&jn(i[a+1])===`
`);a++);if(!(a>=n)){a+=2;for(var o="";a<n;a++){var s=jn(i[a]);if(s===`
`)break;o+=s}var l=o.split(" "),u=parseInt(l[1]),h=parseInt(l[3]);if(!(!h||!u)){for(var f=a+1,d=[],c=0;c<h;c++){d[c]=[];for(var v=0;v<4;v++)d[c][v]=0}for(var p=new Float32Array(h*u*4),_=0,m=0;m<u;m++){var f=am(d,i,f,h);if(!f)return null;for(var c=0;c<h;c++)rm(d[c],p,_,r),_+=4}return t||(t=new ne),t.width=h,t.height=u,t.pixels=p,t.type=H.FLOAT,t}}}},parseRGBEFromPNG:function(e){}},Ht={loadTexture:function(e,t,r,i){var n;if(typeof t=="function"?(r=t,i=r,t={}):t=t||{},typeof e=="string"){if(e.match(/.hdr$/)||t.fileType==="hdr")return n=new ne({width:0,height:0,sRGB:!1}),Ht._fetchTexture(e,function(a){om.parseRGBE(a,n,t.exposure),n.dirty(),r&&r(n)},i),n;e.match(/.dds$/)||t.fileType==="dds"?(n=new ne({width:0,height:0}),Ht._fetchTexture(e,function(a){Qg.parse(a,n),n.dirty(),r&&r(n)},i)):(n=new ne,n.load(e),n.success(r),n.error(i))}else typeof e=="object"&&typeof e.px<"u"&&(n=new Vr,n.load(e),n.success(r),n.error(i));return n},loadPanorama:function(e,t,r,i,n,a){var o=this;typeof i=="function"?(n=i,a=n,i={}):i=i||{},Ht.loadTexture(t,i,function(s){s.flipY=i.flipY||!1,o.panoramaToCubeMap(e,s,r,i),s.dispose(e),n&&n(r)},a)},panoramaToCubeMap:function(e,t,r,i){var n=new rs,a=new Qi({scene:new _r});return a.setEnvironmentMap(t),i=i||{},i.encodeRGBM&&a.material.define("fragment","RGBM_ENCODE"),r.sRGB=t.sRGB,n.texture=r,n.render(e,a.scene),n.texture=null,n.dispose(e),r},heightToNormal:function(e,t){var r=document.createElement("canvas"),i=r.width=e.width,n=r.height=e.height,a=r.getContext("2d");a.drawImage(e,0,0,i,n),t=t||!1;for(var o=a.getImageData(0,0,i,n),s=a.createImageData(i,n),l=0;l<o.data.length;l+=4){if(t){var u=o.data[l],h=o.data[l+1],f=o.data[l+2],d=Math.abs(u-h)+Math.abs(h-f);if(d>20)return console.warn("Given image is not a height map"),e}var c,v,p,_;l%(i*4)===0?(c=o.data[l],p=o.data[l+4]):l%(i*4)===(i-1)*4?(c=o.data[l-4],p=o.data[l]):(c=o.data[l-4],p=o.data[l+4]),l<i*4?(v=o.data[l],_=o.data[l+i*4]):l>i*(n-1)*4?(v=o.data[l-i*4],_=o.data[l]):(v=o.data[l-i*4],_=o.data[l+i*4]),s.data[l]=c-p+127,s.data[l+1]=v-_+127,s.data[l+2]=255,s.data[l+3]=255}return a.putImageData(s,0,0),r},isHeightImage:function(e,t,r){if(!e||!e.width||!e.height)return!1;var i=document.createElement("canvas"),n=i.getContext("2d"),a=t||32;r=r||20,i.width=i.height=a,n.drawImage(e,0,0,a,a);for(var o=n.getImageData(0,0,a,a),s=0;s<o.data.length;s+=4){var l=o.data[s],u=o.data[s+1],h=o.data[s+2],f=Math.abs(l-u)+Math.abs(u-h);if(f>r)return!1}return!0},_fetchTexture:function(e,t,r){de.request.get({url:e,responseType:"arraybuffer",onload:t,onerror:r})},createChessboard:function(e,t,r,i){e=e||512,t=t||64,r=r||"black",i=i||"white";var n=Math.ceil(e/t),a=document.createElement("canvas");a.width=e,a.height=e;var o=a.getContext("2d");o.fillStyle=i,o.fillRect(0,0,e,e),o.fillStyle=r;for(var s=0;s<n;s++)for(var l=0;l<n;l++){var u=l%2?s%2:s%2-1;u&&o.fillRect(s*t,l*t,t,t)}var h=new ne({image:a,anisotropic:8});return h},createBlank:function(e){var t=document.createElement("canvas");t.width=1,t.height=1;var r=t.getContext("2d");r.fillStyle=e,r.fillRect(0,0,1,1);var i=new ne({image:t});return i}},Eo=["mousedown","mouseup","mousemove","mouseover","mouseout","click","dblclick","contextmenu"];function Lo(e){return"_on"+e}var Co=function(e){var t=this;this._texture=new ne({anisotropic:32,flipY:!1,surface:this,dispose:function(r){t.dispose(),ne.prototype.dispose.call(this,r)}}),Eo.forEach(function(r){this[Lo(r)]=function(i){i.triangle&&this._meshes.forEach(function(n){this.dispatchEvent(r,n,i.triangle,i.point)},this)}},this),this._meshes=[],e&&this.setECharts(e),this.onupdate=null};Co.prototype={constructor:Co,getTexture:function(){return this._texture},setECharts:function(e){this._chart=e;var t=e.getDom();if(!(t instanceof HTMLCanvasElement))console.error("ECharts must init on canvas if it is used as texture."),t=document.createElement("canvas");else{var r=this,i=e.getZr(),n=i.__oldRefreshImmediately||i.refreshImmediately;i.refreshImmediately=function(){n.call(this),r._texture.dirty(),r.onupdate&&r.onupdate()},i.__oldRefreshImmediately=n}this._texture.image=t,this._texture.dirty(),this.onupdate&&this.onupdate()},dispatchEvent:function(){var e=new R,t=new R,r=new R,i=new te,n=new te,a=new te,o=new te,s=new R;return function(l,u,h,f){var d=u.geometry,c=d.attributes.position,v=d.attributes.texcoord0,p=R.dot,_=R.cross;c.get(h[0],e.array),c.get(h[1],t.array),c.get(h[2],r.array),v.get(h[0],i.array),v.get(h[1],n.array),v.get(h[2],a.array),_(s,t,r);var m=p(e,s),g=p(f,s)/m;_(s,r,e);var y=p(f,s)/m;_(s,e,t);var x=p(f,s)/m;te.scale(o,i,g),te.scaleAndAdd(o,o,n,y),te.scaleAndAdd(o,o,a,x);var w=o.x*this._chart.getWidth(),T=o.y*this._chart.getHeight();this._chart.getZr().handler.dispatch(l,{zrX:w,zrY:T})}}(),attachToMesh:function(e){this._meshes.indexOf(e)>=0||(Eo.forEach(function(t){e.on(t,this[Lo(t)],this)},this),this._meshes.push(e))},detachFromMesh:function(e){var t=this._meshes.indexOf(e);t>=0&&this._meshes.splice(t,1),Eo.forEach(function(r){e.off(r,this[Lo(r)])},this)},dispose:function(){this._meshes.forEach(function(e){this.detachFromMesh(e)},this)}};var _i=mi.extend({left:-1,right:1,near:-1,far:1,top:1,bottom:-1},{updateProjectionMatrix:function(){this.projectionMatrix.ortho(this.left,this.right,this.bottom,this.top,this.near,this.far)},decomposeProjectionMatrix:function(){var e=this.projectionMatrix.array;this.left=(-1-e[12])/e[0],this.right=(1-e[12])/e[0],this.top=(1-e[13])/e[5],this.bottom=(-1-e[13])/e[5],this.near=-(-1-e[14])/e[10],this.far=-(1-e[14])/e[10]},clone:function(){var e=mi.prototype.clone.call(this);return e.left=this.left,e.right=this.right,e.near=this.near,e.far=this.far,e.top=this.top,e.bottom=this.bottom,e}});const sm=`
@export clay.compositor.vertex
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
attribute vec3 position : POSITION;
attribute vec2 texcoord : TEXCOORD_0;
varying vec2 v_Texcoord;
void main()
{
 v_Texcoord = texcoord;
 gl_Position = worldViewProjection * vec4(position, 1.0);
}
@end`;k.import(sm);var lm=new pa,au=new Xe({geometry:lm,frustumCulling:!1}),um=new _i,Oe=Qe.extend(function(){return{fragment:"",outputs:null,material:null,blendWithPrevious:!1,clearColor:!1,clearDepth:!0}},function(){var e=new k(k.source("clay.compositor.vertex"),this.fragment),t=new At({shader:e});t.enableTexturesAll(),this.material=t},{setUniform:function(e,t){this.material.setUniform(e,t)},getUniform:function(e){var t=this.material.uniforms[e];if(t)return t.value},attachOutput:function(e,t){this.outputs||(this.outputs={}),t=t||F.COLOR_ATTACHMENT0,this.outputs[t]=e},detachOutput:function(e){for(var t in this.outputs)this.outputs[t]===e&&(this.outputs[t]=null)},bind:function(e,t){if(this.outputs)for(var r in this.outputs){var i=this.outputs[r];i&&t.attach(i,r)}t&&t.bind(e)},unbind:function(e,t){t.unbind(e)},render:function(e,t){var r=e.gl;if(t){this.bind(e,t);var i=e.getGLExtension("EXT_draw_buffers");if(i&&this.outputs){var n=[];for(var a in this.outputs)a=+a,a>=r.COLOR_ATTACHMENT0&&a<=r.COLOR_ATTACHMENT0+8&&n.push(a);i.drawBuffersEXT(n)}}this.trigger("beforerender",this,e);var o=this.clearDepth?r.DEPTH_BUFFER_BIT:0;if(r.depthMask(!0),this.clearColor){o=o|r.COLOR_BUFFER_BIT,r.colorMask(!0,!0,!0,!0);var s=this.clearColor;Array.isArray(s)&&r.clearColor(s[0],s[1],s[2],s[3])}r.clear(o),this.blendWithPrevious?(r.enable(r.BLEND),this.material.transparent=!0):(r.disable(r.BLEND),this.material.transparent=!1),this.renderQuad(e),this.trigger("afterrender",this,e),t&&this.unbind(e,t)},renderQuad:function(e){au.material=this.material,e.renderPass([au],um)},dispose:function(e){}});const hm=`#define SAMPLE_NUMBER 1024
#define PI 3.14159265358979
uniform sampler2D normalDistribution;
uniform vec2 viewportSize : [512, 256];
const vec3 N = vec3(0.0, 0.0, 1.0);
const float fSampleNumber = float(SAMPLE_NUMBER);
vec3 importanceSampleNormal(float i, float roughness, vec3 N) {
 vec3 H = texture2D(normalDistribution, vec2(roughness, i)).rgb;
 vec3 upVector = abs(N.y) > 0.999 ? vec3(1.0, 0.0, 0.0) : vec3(0.0, 1.0, 0.0);
 vec3 tangentX = normalize(cross(N, upVector));
 vec3 tangentZ = cross(N, tangentX);
 return normalize(tangentX * H.x + N * H.y + tangentZ * H.z);
}
float G_Smith(float roughness, float NoV, float NoL) {
 float k = roughness * roughness / 2.0;
 float G1V = NoV / (NoV * (1.0 - k) + k);
 float G1L = NoL / (NoL * (1.0 - k) + k);
 return G1L * G1V;
}
void main() {
 vec2 uv = gl_FragCoord.xy / viewportSize;
 float NoV = uv.x;
 float roughness = uv.y;
 vec3 V;
 V.x = sqrt(1.0 - NoV * NoV);
 V.y = 0.0;
 V.z = NoV;
 float A = 0.0;
 float B = 0.0;
 for (int i = 0; i < SAMPLE_NUMBER; i++) {
 vec3 H = importanceSampleNormal(float(i) / fSampleNumber, roughness, N);
 vec3 L = reflect(-V, H);
 float NoL = clamp(L.z, 0.0, 1.0);
 float NoH = clamp(H.z, 0.0, 1.0);
 float VoH = clamp(dot(V, H), 0.0, 1.0);
 if (NoL > 0.0) {
 float G = G_Smith(roughness, NoV, NoL);
 float G_Vis = G * VoH / (NoH * NoV);
 float Fc = pow(1.0 - VoH, 5.0);
 A += (1.0 - Fc) * G_Vis;
 B += Fc * G_Vis;
 }
 }
 gl_FragColor = vec4(vec2(A, B) / fSampleNumber, 0.0, 1.0);
}
`,fm=`#define SHADER_NAME prefilter
#define SAMPLE_NUMBER 1024
#define PI 3.14159265358979
uniform mat4 viewInverse : VIEWINVERSE;
uniform samplerCube environmentMap;
uniform sampler2D normalDistribution;
uniform float roughness : 0.5;
varying vec2 v_Texcoord;
varying vec3 v_WorldPosition;
@import clay.util.rgbm
vec3 importanceSampleNormal(float i, float roughness, vec3 N) {
 vec3 H = texture2D(normalDistribution, vec2(roughness, i)).rgb;
 vec3 upVector = abs(N.y) > 0.999 ? vec3(1.0, 0.0, 0.0) : vec3(0.0, 1.0, 0.0);
 vec3 tangentX = normalize(cross(N, upVector));
 vec3 tangentZ = cross(N, tangentX);
 return normalize(tangentX * H.x + N * H.y + tangentZ * H.z);
}
void main() {
 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(v_WorldPosition - eyePos);
 vec3 N = V;
 vec3 prefilteredColor = vec3(0.0);
 float totalWeight = 0.0;
 float fMaxSampleNumber = float(SAMPLE_NUMBER);
 for (int i = 0; i < SAMPLE_NUMBER; i++) {
 vec3 H = importanceSampleNormal(float(i) / fMaxSampleNumber, roughness, N);
 vec3 L = reflect(-V, H);
 float NoL = clamp(dot(N, L), 0.0, 1.0);
 if (NoL > 0.0) {
 prefilteredColor += decodeHDR(textureCube(environmentMap, L)).rgb * NoL;
 totalWeight += NoL;
 }
 }
 gl_FragColor = encodeHDR(vec4(prefilteredColor / totalWeight, 1.0));
}
`;var kt={},Ja=["px","nx","py","ny","pz","nz"];kt.prefilterEnvironmentMap=function(e,t,r,i,n){(!n||!i)&&(i=kt.generateNormalDistribution(),n=kt.integrateBRDF(e,i)),r=r||{};var a=r.width||64,o=r.height||64,s=r.type||t.type,l=new Vr({width:a,height:o,type:s,flipY:!1,mipmaps:[]});l.isPowerOfTwo()||console.warn("Width and height must be power of two to enable mipmap.");var u=Math.min(a,o),h=Math.log(u)/Math.log(2)+1,f=new At({shader:new k({vertex:k.source("clay.skybox.vertex"),fragment:fm})});f.set("normalDistribution",i),r.encodeRGBM&&f.define("fragment","RGBM_ENCODE"),r.decodeRGBM&&f.define("fragment","RGBM_DECODE");var d=new _r,c;if(t.textureType==="texture2D"){var v=new Vr({width:a,height:o,type:s===H.FLOAT?H.HALF_FLOAT:s});Ht.panoramaToCubeMap(e,t,v,{encodeRGBM:r.decodeRGBM}),t=v}c=new Qi({scene:d,material:f}),c.material.set("environmentMap",t);var p=new rs({texture:l});r.encodeRGBM&&(s=l.type=H.UNSIGNED_BYTE);for(var _=new ne({width:a,height:o,type:s}),m=new Ie({depthBuffer:!1}),g=de[s===H.UNSIGNED_BYTE?"Uint8Array":"Float32Array"],y=0;y<h;y++){l.mipmaps[y]={pixels:{}},c.material.set("roughness",y/(h-1));for(var x=_.width,w=2*Math.atan(x/(x-.5))/Math.PI*180,T=0;T<Ja.length;T++){var b=new g(_.width*_.height*4);m.attach(_),m.bind(e);var A=p.getCamera(Ja[T]);A.fov=w,e.render(d,A),e.gl.readPixels(0,0,_.width,_.height,H.RGBA,s,b),m.unbind(e),l.mipmaps[y].pixels[Ja[T]]=b}_.width/=2,_.height/=2,_.dirty()}return m.dispose(e),_.dispose(e),c.dispose(e),i.dispose(e),{environmentMap:l,brdfLookup:n,normalDistribution:i,maxMipmapLevel:h}};kt.integrateBRDF=function(e,t){t=t||kt.generateNormalDistribution();var r=new Ie({depthBuffer:!1}),i=new Oe({fragment:hm}),n=new ne({width:512,height:256,type:H.HALF_FLOAT,wrapS:H.CLAMP_TO_EDGE,wrapT:H.CLAMP_TO_EDGE,minFilter:H.NEAREST,magFilter:H.NEAREST,useMipmap:!1});return i.setUniform("normalDistribution",t),i.setUniform("viewportSize",[512,256]),i.attachOutput(n),i.render(e,r),r.dispose(e),n};kt.generateNormalDistribution=function(r,i){for(var r=r||256,i=i||1024,n=new ne({width:r,height:i,type:H.FLOAT,minFilter:H.NEAREST,magFilter:H.NEAREST,wrapS:H.CLAMP_TO_EDGE,wrapT:H.CLAMP_TO_EDGE,useMipmap:!1}),a=new Float32Array(i*r*4),o=[],s=0;s<r;s++){for(var l=s/r,u=l*l,h=0;h<i;h++){var f=(h<<16|h>>>16)>>>0;f=((f&1431655765)<<1|(f&2863311530)>>>1)>>>0,f=((f&858993459)<<2|(f&3435973836)>>>2)>>>0,f=((f&252645135)<<4|(f&4042322160)>>>4)>>>0,f=(((f&16711935)<<8|(f&4278255360)>>>8)>>>0)/4294967296;var d=Math.sqrt((1-f)/(1+(u*u-1)*f));o[h]=d}for(var h=0;h<i;h++){var c=(h*r+s)*4,d=o[h],v=Math.sqrt(1-d*d),p=h/i,_=2*Math.PI*p;a[c]=v*Math.cos(_),a[c+1]=d,a[c+2]=v*Math.sin(_),a[c+3]=1}}return n.pixels=a,n};var cm=It.extend({cubemap:null,castShadow:!1,_normalDistribution:null,_brdfLookup:null},{type:"AMBIENT_CUBEMAP_LIGHT",prefilter:function(e,t){if(!e.getGLExtension("EXT_shader_texture_lod")){console.warn("Device not support textureCubeLodEXT");return}this._brdfLookup||(this._normalDistribution=kt.generateNormalDistribution(),this._brdfLookup=kt.integrateBRDF(e,this._normalDistribution));var r=this.cubemap;if(!r.__prefiltered){var i=kt.prefilterEnvironmentMap(e,r,{encodeRGBM:!0,width:t,height:t},this._normalDistribution,this._brdfLookup);this.cubemap=i.environmentMap,this.cubemap.__prefiltered=!0,r.dispose(e)}},getBRDFLookup:function(){return this._brdfLookup},uniformTemplates:{ambientCubemapLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}},ambientCubemapLightCubemap:{type:"t",value:function(e){return e.cubemap}},ambientCubemapLightBRDFLookup:{type:"t",value:function(e){return e._brdfLookup}}}}),dm=It.extend({castShadow:!1,coefficients:[]},function(){this._coefficientsTmpArr=new de.Float32Array(9*3)},{type:"AMBIENT_SH_LIGHT",uniformTemplates:{ambientSHLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}},ambientSHLightCoefficients:{type:"3f",value:function(e){for(var t=e._coefficientsTmpArr,r=0;r<e.coefficients.length;r++)t[r]=e.coefficients[r];return t}}}}),Yh={},Rr=["px","nx","py","ny","pz","nz"];function vm(e,t){var r=e[0],i=e[1],n=e[2];return t===0?1:t===1?r:t===2?i:t===3?n:t===4?r*n:t===5?i*n:t===6?r*i:t===7?3*n*n-1:r*r-i*i}var pm={px:[2,1,0,-1,-1,1],nx:[2,1,0,1,-1,-1],py:[0,2,1,1,-1,-1],ny:[0,2,1,1,1,1],pz:[0,1,2,-1,-1,-1],nz:[0,1,2,1,-1,1]};function gm(e,t,r,i){for(var n=new de.Float32Array(27),a=E.create(),o=E.create(),s=E.create(),l=0;l<9;l++){for(var u=E.create(),h=0;h<Rr.length;h++){for(var f=t[Rr[h]],d=E.create(),c=0,v=0,p=pm[Rr[h]],_=0;_<i;_++)for(var m=0;m<r;m++){a[0]=m/(r-1)*2-1,a[1]=_/(i-1)*2-1,a[2]=-1,E.normalize(a,a),s[0]=a[p[0]]*p[3],s[1]=a[p[1]]*p[4],s[2]=a[p[2]]*p[5],o[0]=f[v++]/255,o[1]=f[v++]/255,o[2]=f[v++]/255;var g=f[v++]/255*8.12;o[0]*=g,o[1]*=g,o[2]*=g,E.scaleAndAdd(d,d,o,vm(s,l)*-a[2]),c+=-a[2]}E.scaleAndAdd(u,u,d,1/c)}n[l*3]=u[0]/6,n[l*3+1]=u[1]/6,n[l*3+2]=u[2]/6}return n}Yh.projectEnvironmentMap=function(e,t,r){r=r||{},r.lod=r.lod||0;var i,n=new _r,a=64;t.textureType==="texture2D"?i=new Qi({scene:n,environmentMap:t}):(a=t.image&&t.image.px?t.image.px.width:t.width,i=new Qi({scene:n,environmentMap:t}));var o=Math.ceil(a/Math.pow(2,r.lod)),s=Math.ceil(a/Math.pow(2,r.lod)),l=new ne({width:o,height:s}),u=new Ie;i.material.define("fragment","RGBM_ENCODE"),r.decodeRGBM&&i.material.define("fragment","RGBM_DECODE"),i.material.set("lod",r.lod);for(var h=new rs({texture:l}),f={},d=0;d<Rr.length;d++){f[Rr[d]]=new Uint8Array(o*s*4);var c=h.getCamera(Rr[d]);c.fov=90,u.attach(l),u.bind(e),e.render(n,c),e.gl.readPixels(0,0,o,s,H.RGBA,H.UNSIGNED_BYTE,f[Rr[d]]),u.unbind(e)}return i.dispose(e),u.dispose(e),l.dispose(e),gm(e,f,o,s)};var oe={firstNotNull:function(){for(var e=0,t=arguments.length;e<t;e++)if(arguments[e]!=null)return arguments[e]},queryDataIndex:function(e,t){if(t.dataIndexInside!=null)return t.dataIndexInside;if(t.dataIndex!=null)return Be(t.dataIndex)?we(t.dataIndex,function(r){return e.indexOfRawIndex(r)}):e.indexOfRawIndex(t.dataIndex);if(t.name!=null)return Be(t.name)?we(t.name,function(r){return e.indexOfName(r)}):e.indexOfName(t.name)}},mm=se.extend({dynamic:!1,widthSegments:40,heightSegments:20,phiStart:0,phiLength:Math.PI*2,thetaStart:0,thetaLength:Math.PI,radius:1},function(){this.build()},{build:function(){var e=this.heightSegments,t=this.widthSegments,r=this.attributes.position,i=this.attributes.texcoord0,n=this.attributes.normal,a=(t+1)*(e+1);r.init(a),i.init(a),n.init(a);var o=a>65535?Uint32Array:Uint16Array,s=this.indices=new o(t*e*6),l,u,h,f,d,c,v,y=this.radius,p=this.phiStart,_=this.phiLength,m=this.thetaStart,g=this.thetaLength,y=this.radius,x=[],w=[],T=0,b=1/y;for(v=0;v<=e;v++)for(c=0;c<=t;c++)f=c/t,d=v/e,l=-y*Math.cos(p+f*_)*Math.sin(m+d*g),u=y*Math.cos(m+d*g),h=y*Math.sin(p+f*_)*Math.sin(m+d*g),x[0]=l,x[1]=u,x[2]=h,w[0]=f,w[1]=d,r.set(T,x),i.set(T,w),x[0]*=b,x[1]*=b,x[2]*=b,n.set(T,x),T++;var A,C,D,L,M=t+1,P=0;for(v=0;v<e;v++)for(c=0;c<t;c++)C=v*M+c,A=v*M+c+1,L=(v+1)*M+c+1,D=(v+1)*M+c,s[P++]=A,s[P++]=C,s[P++]=L,s[P++]=C,s[P++]=D,s[P++]=L;this.boundingBox=new Je,this.boundingBox.max.set(y,y,y),this.boundingBox.min.set(-y,-y,-y)}}),_m=It.extend({castShadow:!1},{type:"AMBIENT_LIGHT",uniformTemplates:{ambientLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}}}}),ym=It.extend({shadowBias:.001,shadowSlopeScale:2,shadowCascade:1,cascadeSplitLogFactor:.2},{type:"DIRECTIONAL_LIGHT",uniformTemplates:{directionalLightDirection:{type:"3f",value:function(e){return e.__dir=e.__dir||new R,e.__dir.copy(e.worldTransform.z).normalize().negate().array}},directionalLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}}},clone:function(){var e=It.prototype.clone.call(this);return e.shadowBias=this.shadowBias,e.shadowSlopeScale=this.shadowSlopeScale,e}}),xm=It.extend({range:100,castShadow:!1},{type:"POINT_LIGHT",uniformTemplates:{pointLightPosition:{type:"3f",value:function(e){return e.getWorldPosition().array}},pointLightRange:{type:"1f",value:function(e){return e.range}},pointLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}}},clone:function(){var e=It.prototype.clone.call(this);return e.range=this.range,e}}),Tm=It.extend({range:20,umbraAngle:30,penumbraAngle:45,falloffFactor:2,shadowBias:.001,shadowSlopeScale:2},{type:"SPOT_LIGHT",uniformTemplates:{spotLightPosition:{type:"3f",value:function(e){return e.getWorldPosition().array}},spotLightRange:{type:"1f",value:function(e){return e.range}},spotLightUmbraAngleCosine:{type:"1f",value:function(e){return Math.cos(e.umbraAngle*Math.PI/180)}},spotLightPenumbraAngleCosine:{type:"1f",value:function(e){return Math.cos(e.penumbraAngle*Math.PI/180)}},spotLightFalloffFactor:{type:"1f",value:function(e){return e.falloffFactor}},spotLightDirection:{type:"3f",value:function(e){return e.__dir=e.__dir||new R,e.__dir.copy(e.worldTransform.z).negate().array}},spotLightColor:{type:"3f",value:function(e){var t=e.color,r=e.intensity;return[t[0]*r,t[1]*r,t[2]*r]}}},clone:function(){var e=It.prototype.clone.call(this);return e.range=this.range,e.umbraAngle=this.umbraAngle,e.penumbraAngle=this.penumbraAngle,e.falloffFactor=this.falloffFactor,e.shadowBias=this.shadowBias,e.shadowSlopeScale=this.shadowSlopeScale,e}}),he=function(e,t,r,i){e=e||0,t=t||0,r=r||0,i=i||0,this.array=G.fromValues(e,t,r,i),this._dirty=!0};he.prototype={constructor:he,add:function(e){return G.add(this.array,this.array,e.array),this._dirty=!0,this},set:function(e,t,r,i){return this.array[0]=e,this.array[1]=t,this.array[2]=r,this.array[3]=i,this._dirty=!0,this},setArray:function(e){return this.array[0]=e[0],this.array[1]=e[1],this.array[2]=e[2],this.array[3]=e[3],this._dirty=!0,this},clone:function(){return new he(this.x,this.y,this.z,this.w)},copy:function(e){return G.copy(this.array,e.array),this._dirty=!0,this},dist:function(e){return G.dist(this.array,e.array)},distance:function(e){return G.distance(this.array,e.array)},div:function(e){return G.div(this.array,this.array,e.array),this._dirty=!0,this},divide:function(e){return G.divide(this.array,this.array,e.array),this._dirty=!0,this},dot:function(e){return G.dot(this.array,e.array)},len:function(){return G.len(this.array)},length:function(){return G.length(this.array)},lerp:function(e,t,r){return G.lerp(this.array,e.array,t.array,r),this._dirty=!0,this},min:function(e){return G.min(this.array,this.array,e.array),this._dirty=!0,this},max:function(e){return G.max(this.array,this.array,e.array),this._dirty=!0,this},mul:function(e){return G.mul(this.array,this.array,e.array),this._dirty=!0,this},multiply:function(e){return G.multiply(this.array,this.array,e.array),this._dirty=!0,this},negate:function(){return G.negate(this.array,this.array),this._dirty=!0,this},normalize:function(){return G.normalize(this.array,this.array),this._dirty=!0,this},random:function(e){return G.random(this.array,e),this._dirty=!0,this},scale:function(e){return G.scale(this.array,this.array,e),this._dirty=!0,this},scaleAndAdd:function(e,t){return G.scaleAndAdd(this.array,this.array,e.array,t),this._dirty=!0,this},sqrDist:function(e){return G.sqrDist(this.array,e.array)},squaredDistance:function(e){return G.squaredDistance(this.array,e.array)},sqrLen:function(){return G.sqrLen(this.array)},squaredLength:function(){return G.squaredLength(this.array)},sub:function(e){return G.sub(this.array,this.array,e.array),this._dirty=!0,this},subtract:function(e){return G.subtract(this.array,this.array,e.array),this._dirty=!0,this},transformMat4:function(e){return G.transformMat4(this.array,this.array,e.array),this._dirty=!0,this},transformQuat:function(e){return G.transformQuat(this.array,this.array,e.array),this._dirty=!0,this},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};var Bi=Object.defineProperty;if(Bi){var Fn=he.prototype;Bi(Fn,"x",{get:function(){return this.array[0]},set:function(e){this.array[0]=e,this._dirty=!0}}),Bi(Fn,"y",{get:function(){return this.array[1]},set:function(e){this.array[1]=e,this._dirty=!0}}),Bi(Fn,"z",{get:function(){return this.array[2]},set:function(e){this.array[2]=e,this._dirty=!0}}),Bi(Fn,"w",{get:function(){return this.array[3]},set:function(e){this.array[3]=e,this._dirty=!0}})}he.add=function(e,t,r){return G.add(e.array,t.array,r.array),e._dirty=!0,e};he.set=function(e,t,r,i,n){G.set(e.array,t,r,i,n),e._dirty=!0};he.copy=function(e,t){return G.copy(e.array,t.array),e._dirty=!0,e};he.dist=function(e,t){return G.distance(e.array,t.array)};he.distance=he.dist;he.div=function(e,t,r){return G.divide(e.array,t.array,r.array),e._dirty=!0,e};he.divide=he.div;he.dot=function(e,t){return G.dot(e.array,t.array)};he.len=function(e){return G.length(e.array)};he.lerp=function(e,t,r,i){return G.lerp(e.array,t.array,r.array,i),e._dirty=!0,e};he.min=function(e,t,r){return G.min(e.array,t.array,r.array),e._dirty=!0,e};he.max=function(e,t,r){return G.max(e.array,t.array,r.array),e._dirty=!0,e};he.mul=function(e,t,r){return G.multiply(e.array,t.array,r.array),e._dirty=!0,e};he.multiply=he.mul;he.negate=function(e,t){return G.negate(e.array,t.array),e._dirty=!0,e};he.normalize=function(e,t){return G.normalize(e.array,t.array),e._dirty=!0,e};he.random=function(e,t){return G.random(e.array,t),e._dirty=!0,e};he.scale=function(e,t,r){return G.scale(e.array,t.array,r),e._dirty=!0,e};he.scaleAndAdd=function(e,t,r,i){return G.scaleAndAdd(e.array,t.array,r.array,i),e._dirty=!0,e};he.sqrDist=function(e,t){return G.sqrDist(e.array,t.array)};he.squaredDistance=he.sqrDist;he.sqrLen=function(e){return G.sqrLen(e.array)};he.squaredLength=he.sqrLen;he.sub=function(e,t,r){return G.subtract(e.array,t.array,r.array),e._dirty=!0,e};he.subtract=he.sub;he.transformMat4=function(e,t,r){return G.transformMat4(e.array,t.array,r.array),e._dirty=!0,e};he.transformQuat=function(e,t,r){return G.transformQuat(e.array,t.array,r.array),e._dirty=!0,e};var fe={};fe.create=function(){var e=new et(4);return e[0]=1,e[1]=0,e[2]=0,e[3]=1,e};fe.clone=function(e){var t=new et(4);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3],t};fe.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e};fe.identity=function(e){return e[0]=1,e[1]=0,e[2]=0,e[3]=1,e};fe.transpose=function(e,t){if(e===t){var r=t[1];e[1]=t[2],e[2]=r}else e[0]=t[0],e[1]=t[2],e[2]=t[1],e[3]=t[3];return e};fe.invert=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=r*a-n*i;return o?(o=1/o,e[0]=a*o,e[1]=-i*o,e[2]=-n*o,e[3]=r*o,e):null};fe.adjoint=function(e,t){var r=t[0];return e[0]=t[3],e[1]=-t[1],e[2]=-t[2],e[3]=r,e};fe.determinant=function(e){return e[0]*e[3]-e[2]*e[1]};fe.multiply=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=r[0],l=r[1],u=r[2],h=r[3];return e[0]=i*s+a*l,e[1]=n*s+o*l,e[2]=i*u+a*h,e[3]=n*u+o*h,e};fe.mul=fe.multiply;fe.rotate=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=Math.sin(r),l=Math.cos(r);return e[0]=i*l+a*s,e[1]=n*l+o*s,e[2]=i*-s+a*l,e[3]=n*-s+o*l,e};fe.scale=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=r[0],l=r[1];return e[0]=i*s,e[1]=n*s,e[2]=a*l,e[3]=o*l,e};fe.frob=function(e){return Math.sqrt(Math.pow(e[0],2)+Math.pow(e[1],2)+Math.pow(e[2],2)+Math.pow(e[3],2))};fe.LDU=function(e,t,r,i){return e[2]=i[2]/i[0],r[0]=i[0],r[1]=i[1],r[3]=i[3]-e[2]*r[1],[e,t,r]};var st=function(){this.array=fe.create(),this._dirty=!0};st.prototype={constructor:st,setArray:function(e){for(var t=0;t<this.array.length;t++)this.array[t]=e[t];return this._dirty=!0,this},clone:function(){return new st().copy(this)},copy:function(e){return fe.copy(this.array,e.array),this._dirty=!0,this},adjoint:function(){return fe.adjoint(this.array,this.array),this._dirty=!0,this},determinant:function(){return fe.determinant(this.array)},identity:function(){return fe.identity(this.array),this._dirty=!0,this},invert:function(){return fe.invert(this.array,this.array),this._dirty=!0,this},mul:function(e){return fe.mul(this.array,this.array,e.array),this._dirty=!0,this},mulLeft:function(e){return fe.mul(this.array,e.array,this.array),this._dirty=!0,this},multiply:function(e){return fe.multiply(this.array,this.array,e.array),this._dirty=!0,this},multiplyLeft:function(e){return fe.multiply(this.array,e.array,this.array),this._dirty=!0,this},rotate:function(e){return fe.rotate(this.array,this.array,e),this._dirty=!0,this},scale:function(e){return fe.scale(this.array,this.array,e.array),this._dirty=!0,this},transpose:function(){return fe.transpose(this.array,this.array),this._dirty=!0,this},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};st.adjoint=function(e,t){return fe.adjoint(e.array,t.array),e._dirty=!0,e};st.copy=function(e,t){return fe.copy(e.array,t.array),e._dirty=!0,e};st.determinant=function(e){return fe.determinant(e.array)};st.identity=function(e){return fe.identity(e.array),e._dirty=!0,e};st.invert=function(e,t){return fe.invert(e.array,t.array),e._dirty=!0,e};st.mul=function(e,t,r){return fe.mul(e.array,t.array,r.array),e._dirty=!0,e};st.multiply=st.mul;st.rotate=function(e,t,r){return fe.rotate(e.array,t.array,r),e._dirty=!0,e};st.scale=function(e,t,r){return fe.scale(e.array,t.array,r.array),e._dirty=!0,e};st.transpose=function(e,t){return fe.transpose(e.array,t.array),e._dirty=!0,e};var ve={};ve.create=function(){var e=new et(6);return e[0]=1,e[1]=0,e[2]=0,e[3]=1,e[4]=0,e[5]=0,e};ve.clone=function(e){var t=new et(6);return t[0]=e[0],t[1]=e[1],t[2]=e[2],t[3]=e[3],t[4]=e[4],t[5]=e[5],t};ve.copy=function(e,t){return e[0]=t[0],e[1]=t[1],e[2]=t[2],e[3]=t[3],e[4]=t[4],e[5]=t[5],e};ve.identity=function(e){return e[0]=1,e[1]=0,e[2]=0,e[3]=1,e[4]=0,e[5]=0,e};ve.invert=function(e,t){var r=t[0],i=t[1],n=t[2],a=t[3],o=t[4],s=t[5],l=r*a-i*n;return l?(l=1/l,e[0]=a*l,e[1]=-i*l,e[2]=-n*l,e[3]=r*l,e[4]=(n*s-a*o)*l,e[5]=(i*o-r*s)*l,e):null};ve.determinant=function(e){return e[0]*e[3]-e[1]*e[2]};ve.multiply=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=r[0],h=r[1],f=r[2],d=r[3],c=r[4],v=r[5];return e[0]=i*u+a*h,e[1]=n*u+o*h,e[2]=i*f+a*d,e[3]=n*f+o*d,e[4]=i*c+a*v+s,e[5]=n*c+o*v+l,e};ve.mul=ve.multiply;ve.rotate=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=Math.sin(r),h=Math.cos(r);return e[0]=i*h+a*u,e[1]=n*h+o*u,e[2]=i*-u+a*h,e[3]=n*-u+o*h,e[4]=s,e[5]=l,e};ve.scale=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=r[0],h=r[1];return e[0]=i*u,e[1]=n*u,e[2]=a*h,e[3]=o*h,e[4]=s,e[5]=l,e};ve.translate=function(e,t,r){var i=t[0],n=t[1],a=t[2],o=t[3],s=t[4],l=t[5],u=r[0],h=r[1];return e[0]=i,e[1]=n,e[2]=a,e[3]=o,e[4]=i*u+a*h+s,e[5]=n*u+o*h+l,e};ve.frob=function(e){return Math.sqrt(Math.pow(e[0],2)+Math.pow(e[1],2)+Math.pow(e[2],2)+Math.pow(e[3],2)+Math.pow(e[4],2)+Math.pow(e[5],2)+1)};var vt=function(){this.array=ve.create(),this._dirty=!0};vt.prototype={constructor:vt,setArray:function(e){for(var t=0;t<this.array.length;t++)this.array[t]=e[t];return this._dirty=!0,this},clone:function(){return new vt().copy(this)},copy:function(e){return ve.copy(this.array,e.array),this._dirty=!0,this},determinant:function(){return ve.determinant(this.array)},identity:function(){return ve.identity(this.array),this._dirty=!0,this},invert:function(){return ve.invert(this.array,this.array),this._dirty=!0,this},mul:function(e){return ve.mul(this.array,this.array,e.array),this._dirty=!0,this},mulLeft:function(e){return ve.mul(this.array,e.array,this.array),this._dirty=!0,this},multiply:function(e){return ve.multiply(this.array,this.array,e.array),this._dirty=!0,this},multiplyLeft:function(e){return ve.multiply(this.array,e.array,this.array),this._dirty=!0,this},rotate:function(e){return ve.rotate(this.array,this.array,e),this._dirty=!0,this},scale:function(e){return ve.scale(this.array,this.array,e.array),this._dirty=!0,this},translate:function(e){return ve.translate(this.array,this.array,e.array),this._dirty=!0,this},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};vt.copy=function(e,t){return ve.copy(e.array,t.array),e._dirty=!0,e};vt.determinant=function(e){return ve.determinant(e.array)};vt.identity=function(e){return ve.identity(e.array),e._dirty=!0,e};vt.invert=function(e,t){return ve.invert(e.array,t.array),e._dirty=!0,e};vt.mul=function(e,t,r){return ve.mul(e.array,t.array,r.array),e._dirty=!0,e};vt.multiply=vt.mul;vt.rotate=function(e,t,r){return ve.rotate(e.array,t.array,r),e._dirty=!0,e};vt.scale=function(e,t,r){return ve.scale(e.array,t.array,r.array),e._dirty=!0,e};vt.translate=function(e,t,r){return ve.translate(e.array,t.array,r.array),e._dirty=!0,e};var Ue=function(){this.array=K.create(),this._dirty=!0};Ue.prototype={constructor:Ue,setArray:function(e){for(var t=0;t<this.array.length;t++)this.array[t]=e[t];return this._dirty=!0,this},adjoint:function(){return K.adjoint(this.array,this.array),this._dirty=!0,this},clone:function(){return new Ue().copy(this)},copy:function(e){return K.copy(this.array,e.array),this._dirty=!0,this},determinant:function(){return K.determinant(this.array)},fromMat2d:function(e){return K.fromMat2d(this.array,e.array),this._dirty=!0,this},fromMat4:function(e){return K.fromMat4(this.array,e.array),this._dirty=!0,this},fromQuat:function(e){return K.fromQuat(this.array,e.array),this._dirty=!0,this},identity:function(){return K.identity(this.array),this._dirty=!0,this},invert:function(){return K.invert(this.array,this.array),this._dirty=!0,this},mul:function(e){return K.mul(this.array,this.array,e.array),this._dirty=!0,this},mulLeft:function(e){return K.mul(this.array,e.array,this.array),this._dirty=!0,this},multiply:function(e){return K.multiply(this.array,this.array,e.array),this._dirty=!0,this},multiplyLeft:function(e){return K.multiply(this.array,e.array,this.array),this._dirty=!0,this},rotate:function(e){return K.rotate(this.array,this.array,e),this._dirty=!0,this},scale:function(e){return K.scale(this.array,this.array,e.array),this._dirty=!0,this},translate:function(e){return K.translate(this.array,this.array,e.array),this._dirty=!0,this},normalFromMat4:function(e){return K.normalFromMat4(this.array,e.array),this._dirty=!0,this},transpose:function(){return K.transpose(this.array,this.array),this._dirty=!0,this},toString:function(){return"["+Array.prototype.join.call(this.array,",")+"]"},toArray:function(){return Array.prototype.slice.call(this.array)}};Ue.adjoint=function(e,t){return K.adjoint(e.array,t.array),e._dirty=!0,e};Ue.copy=function(e,t){return K.copy(e.array,t.array),e._dirty=!0,e};Ue.determinant=function(e){return K.determinant(e.array)};Ue.identity=function(e){return K.identity(e.array),e._dirty=!0,e};Ue.invert=function(e,t){return K.invert(e.array,t.array),e};Ue.mul=function(e,t,r){return K.mul(e.array,t.array,r.array),e._dirty=!0,e};Ue.multiply=Ue.mul;Ue.fromMat2d=function(e,t){return K.fromMat2d(e.array,t.array),e._dirty=!0,e};Ue.fromMat4=function(e,t){return K.fromMat4(e.array,t.array),e._dirty=!0,e};Ue.fromQuat=function(e,t){return K.fromQuat(e.array,t.array),e._dirty=!0,e};Ue.normalFromMat4=function(e,t){return K.normalFromMat4(e.array,t.array),e._dirty=!0,e};Ue.rotate=function(e,t,r){return K.rotate(e.array,t.array,r),e._dirty=!0,e};Ue.scale=function(e,t,r){return K.scale(e.array,t.array,r.array),e._dirty=!0,e};Ue.transpose=function(e,t){return K.transpose(e.array,t.array),e._dirty=!0,e};Ue.translate=function(e,t,r){return K.translate(e.array,t.array,r.array),e._dirty=!0,e};var wm={_animators:null,getAnimators:function(){return this._animators=this._animators||[],this._animators},animate:function(e,t){this._animators=this._animators||[];var r=this,i;if(e){for(var n=e.split("."),a=r,o=0,s=n.length;o<s;o++)a&&(a=a[n[o]]);a&&(i=a)}else i=r;if(i==null)throw new Error("Target "+e+" not exists");var l=this._animators,u=new id(i,t),h=this;return u.during(function(){h.__zr&&h.__zr.refresh()}).done(function(){var f=l.indexOf(u);f>=0&&l.splice(f,1)}),l.push(u),this.__zr&&this.__zr.animation.addAnimator(u),u},stopAnimation:function(e){this._animators=this._animators||[];for(var t=this._animators,r=t.length,i=0;i<r;i++)t[i].stop(e);return t.length=0,this},addAnimatorsToZr:function(e){if(this._animators)for(var t=0;t<this._animators.length;t++)e.animation.addAnimator(this._animators[t])},removeAnimatorsFromZr:function(e){if(this._animators)for(var t=0;t<this._animators.length;t++)e.animation.removeAnimator(this._animators[t])}};const $h=`
@export clay.util.rand
highp float rand(vec2 uv) {
 const highp float a = 12.9898, b = 78.233, c = 43758.5453;
 highp float dt = dot(uv.xy, vec2(a,b)), sn = mod(dt, 3.141592653589793);
 return fract(sin(sn) * c);
}
@end
@export clay.util.calculate_attenuation
uniform float attenuationFactor : 5.0;
float lightAttenuation(float dist, float range)
{
 float attenuation = 1.0;
 attenuation = dist*dist/(range*range+1.0);
 float att_s = attenuationFactor;
 attenuation = 1.0/(attenuation*att_s+1.0);
 att_s = 1.0/(att_s+1.0);
 attenuation = attenuation - att_s;
 attenuation /= 1.0 - att_s;
 return clamp(attenuation, 0.0, 1.0);
}
@end
@export clay.util.edge_factor
#ifdef SUPPORT_STANDARD_DERIVATIVES
float edgeFactor(float width)
{
 vec3 d = fwidth(v_Barycentric);
 vec3 a3 = smoothstep(vec3(0.0), d * width, v_Barycentric);
 return min(min(a3.x, a3.y), a3.z);
}
#else
float edgeFactor(float width)
{
 return 1.0;
}
#endif
@end
@export clay.util.encode_float
vec4 encodeFloat(const in float depth)
{
 const vec4 bitShifts = vec4(256.0*256.0*256.0, 256.0*256.0, 256.0, 1.0);
 const vec4 bit_mask = vec4(0.0, 1.0/256.0, 1.0/256.0, 1.0/256.0);
 vec4 res = fract(depth * bitShifts);
 res -= res.xxyz * bit_mask;
 return res;
}
@end
@export clay.util.decode_float
float decodeFloat(const in vec4 color)
{
 const vec4 bitShifts = vec4(1.0/(256.0*256.0*256.0), 1.0/(256.0*256.0), 1.0/256.0, 1.0);
 return dot(color, bitShifts);
}
@end
@export clay.util.float
@import clay.util.encode_float
@import clay.util.decode_float
@end
@export clay.util.rgbm_decode
vec3 RGBMDecode(vec4 rgbm, float range) {
 return range * rgbm.rgb * rgbm.a;
}
@end
@export clay.util.rgbm_encode
vec4 RGBMEncode(vec3 color, float range) {
 if (dot(color, color) == 0.0) {
 return vec4(0.0);
 }
 vec4 rgbm;
 color /= range;
 rgbm.a = clamp(max(max(color.r, color.g), max(color.b, 1e-6)), 0.0, 1.0);
 rgbm.a = ceil(rgbm.a * 255.0) / 255.0;
 rgbm.rgb = color / rgbm.a;
 return rgbm;
}
@end
@export clay.util.rgbm
@import clay.util.rgbm_decode
@import clay.util.rgbm_encode
vec4 decodeHDR(vec4 color)
{
#if defined(RGBM_DECODE) || defined(RGBM)
 return vec4(RGBMDecode(color, 8.12), 1.0);
#else
 return color;
#endif
}
vec4 encodeHDR(vec4 color)
{
#if defined(RGBM_ENCODE) || defined(RGBM)
 return RGBMEncode(color.xyz, 8.12);
#else
 return color;
#endif
}
@end
@export clay.util.srgb
vec4 sRGBToLinear(in vec4 value) {
 return vec4(mix(pow(value.rgb * 0.9478672986 + vec3(0.0521327014), vec3(2.4)), value.rgb * 0.0773993808, vec3(lessThanEqual(value.rgb, vec3(0.04045)))), value.w);
}
vec4 linearTosRGB(in vec4 value) {
 return vec4(mix(pow(value.rgb, vec3(0.41666)) * 1.055 - vec3(0.055), value.rgb * 12.92, vec3(lessThanEqual(value.rgb, vec3(0.0031308)))), value.w);
}
@end
@export clay.chunk.skinning_header
#ifdef SKINNING
attribute vec3 weight : WEIGHT;
attribute vec4 joint : JOINT;
#ifdef USE_SKIN_MATRICES_TEXTURE
uniform sampler2D skinMatricesTexture : ignore;
uniform float skinMatricesTextureSize: ignore;
mat4 getSkinMatrix(sampler2D tex, float idx) {
 float j = idx * 4.0;
 float x = mod(j, skinMatricesTextureSize);
 float y = floor(j / skinMatricesTextureSize) + 0.5;
 vec2 scale = vec2(skinMatricesTextureSize);
 return mat4(
 texture2D(tex, vec2(x + 0.5, y) / scale),
 texture2D(tex, vec2(x + 1.5, y) / scale),
 texture2D(tex, vec2(x + 2.5, y) / scale),
 texture2D(tex, vec2(x + 3.5, y) / scale)
 );
}
mat4 getSkinMatrix(float idx) {
 return getSkinMatrix(skinMatricesTexture, idx);
}
#else
uniform mat4 skinMatrix[JOINT_COUNT] : SKIN_MATRIX;
mat4 getSkinMatrix(float idx) {
 return skinMatrix[int(idx)];
}
#endif
#endif
@end
@export clay.chunk.skin_matrix
mat4 skinMatrixWS = getSkinMatrix(joint.x) * weight.x;
if (weight.y > 1e-4)
{
 skinMatrixWS += getSkinMatrix(joint.y) * weight.y;
}
if (weight.z > 1e-4)
{
 skinMatrixWS += getSkinMatrix(joint.z) * weight.z;
}
float weightW = 1.0-weight.x-weight.y-weight.z;
if (weightW > 1e-4)
{
 skinMatrixWS += getSkinMatrix(joint.w) * weightW;
}
@end
@export clay.chunk.instancing_header
#ifdef INSTANCING
attribute vec4 instanceMat1;
attribute vec4 instanceMat2;
attribute vec4 instanceMat3;
#endif
@end
@export clay.chunk.instancing_matrix
mat4 instanceMat = mat4(
 vec4(instanceMat1.xyz, 0.0),
 vec4(instanceMat2.xyz, 0.0),
 vec4(instanceMat3.xyz, 0.0),
 vec4(instanceMat1.w, instanceMat2.w, instanceMat3.w, 1.0)
);
@end
@export clay.util.parallax_correct
vec3 parallaxCorrect(in vec3 dir, in vec3 pos, in vec3 boxMin, in vec3 boxMax) {
 vec3 first = (boxMax - pos) / dir;
 vec3 second = (boxMin - pos) / dir;
 vec3 further = max(first, second);
 float dist = min(further.x, min(further.y, further.z));
 vec3 fixedPos = pos + dir * dist;
 vec3 boxCenter = (boxMax + boxMin) * 0.5;
 return normalize(fixedPos - boxCenter);
}
@end
@export clay.util.clamp_sample
vec4 clampSample(const in sampler2D texture, const in vec2 coord)
{
#ifdef STEREO
 float eye = step(0.5, coord.x) * 0.5;
 vec2 coordClamped = clamp(coord, vec2(eye, 0.0), vec2(0.5 + eye, 1.0));
#else
 vec2 coordClamped = clamp(coord, vec2(0.0), vec2(1.0));
#endif
 return texture2D(texture, coordClamped);
}
@end
@export clay.util.ACES
vec3 ACESToneMapping(vec3 color)
{
 const float A = 2.51;
 const float B = 0.03;
 const float C = 2.43;
 const float D = 0.59;
 const float E = 0.14;
 return (color * (A * color + B)) / (color * (C * color + D) + E);
}
@end`,Sm=`
@export ecgl.common.transformUniforms
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform mat4 worldInverseTranspose : WORLDINVERSETRANSPOSE;
uniform mat4 world : WORLD;
@end

@export ecgl.common.attributes
attribute vec3 position : POSITION;
attribute vec2 texcoord : TEXCOORD_0;
attribute vec3 normal : NORMAL;
@end

@export ecgl.common.uv.header
uniform vec2 uvRepeat : [1.0, 1.0];
uniform vec2 uvOffset : [0.0, 0.0];
uniform vec2 detailUvRepeat : [1.0, 1.0];
uniform vec2 detailUvOffset : [0.0, 0.0];

varying vec2 v_Texcoord;
varying vec2 v_DetailTexcoord;
@end

@export ecgl.common.uv.main
v_Texcoord = texcoord * uvRepeat + uvOffset;
v_DetailTexcoord = texcoord * detailUvRepeat + detailUvOffset;
@end

@export ecgl.common.uv.fragmentHeader
varying vec2 v_Texcoord;
varying vec2 v_DetailTexcoord;
@end


@export ecgl.common.albedo.main

 vec4 albedoTexel = vec4(1.0);
#ifdef DIFFUSEMAP_ENABLED
 albedoTexel = texture2D(diffuseMap, v_Texcoord);
 #ifdef SRGB_DECODE
 albedoTexel = sRGBToLinear(albedoTexel);
 #endif
#endif

#ifdef DETAILMAP_ENABLED
 vec4 detailTexel = texture2D(detailMap, v_DetailTexcoord);
 #ifdef SRGB_DECODE
 detailTexel = sRGBToLinear(detailTexel);
 #endif
 albedoTexel.rgb = mix(albedoTexel.rgb, detailTexel.rgb, detailTexel.a);
 albedoTexel.a = detailTexel.a + (1.0 - detailTexel.a) * albedoTexel.a;
#endif

@end

@export ecgl.common.wireframe.vertexHeader

#ifdef WIREFRAME_QUAD
attribute vec4 barycentric;
varying vec4 v_Barycentric;
#elif defined(WIREFRAME_TRIANGLE)
attribute vec3 barycentric;
varying vec3 v_Barycentric;
#endif

@end

@export ecgl.common.wireframe.vertexMain

#if defined(WIREFRAME_QUAD) || defined(WIREFRAME_TRIANGLE)
 v_Barycentric = barycentric;
#endif

@end


@export ecgl.common.wireframe.fragmentHeader

uniform float wireframeLineWidth : 1;
uniform vec4 wireframeLineColor: [0, 0, 0, 0.5];

#ifdef WIREFRAME_QUAD
varying vec4 v_Barycentric;
float edgeFactor () {
 vec4 d = fwidth(v_Barycentric);
 vec4 a4 = smoothstep(vec4(0.0), d * wireframeLineWidth, v_Barycentric);
 return min(min(min(a4.x, a4.y), a4.z), a4.w);
}
#elif defined(WIREFRAME_TRIANGLE)
varying vec3 v_Barycentric;
float edgeFactor () {
 vec3 d = fwidth(v_Barycentric);
 vec3 a3 = smoothstep(vec3(0.0), d * wireframeLineWidth, v_Barycentric);
 return min(min(a3.x, a3.y), a3.z);
}
#endif

@end


@export ecgl.common.wireframe.fragmentMain

#if defined(WIREFRAME_QUAD) || defined(WIREFRAME_TRIANGLE)
 if (wireframeLineWidth > 0.) {
 vec4 lineColor = wireframeLineColor;
#ifdef SRGB_DECODE
 lineColor = sRGBToLinear(lineColor);
#endif

 gl_FragColor.rgb = mix(gl_FragColor.rgb, lineColor.rgb, (1.0 - edgeFactor()) * lineColor.a);
 }
#endif
@end




@export ecgl.common.bumpMap.header

#ifdef BUMPMAP_ENABLED
uniform sampler2D bumpMap;
uniform float bumpScale : 1.0;


vec3 bumpNormal(vec3 surfPos, vec3 surfNormal, vec3 baseNormal)
{
 vec2 dSTdx = dFdx(v_Texcoord);
 vec2 dSTdy = dFdy(v_Texcoord);

 float Hll = bumpScale * texture2D(bumpMap, v_Texcoord).x;
 float dHx = bumpScale * texture2D(bumpMap, v_Texcoord + dSTdx).x - Hll;
 float dHy = bumpScale * texture2D(bumpMap, v_Texcoord + dSTdy).x - Hll;

 vec3 vSigmaX = dFdx(surfPos);
 vec3 vSigmaY = dFdy(surfPos);
 vec3 vN = surfNormal;

 vec3 R1 = cross(vSigmaY, vN);
 vec3 R2 = cross(vN, vSigmaX);

 float fDet = dot(vSigmaX, R1);

 vec3 vGrad = sign(fDet) * (dHx * R1 + dHy * R2);
 return normalize(abs(fDet) * baseNormal - vGrad);

}
#endif

@end

@export ecgl.common.normalMap.vertexHeader

#ifdef NORMALMAP_ENABLED
attribute vec4 tangent : TANGENT;
varying vec3 v_Tangent;
varying vec3 v_Bitangent;
#endif

@end

@export ecgl.common.normalMap.vertexMain

#ifdef NORMALMAP_ENABLED
 if (dot(tangent, tangent) > 0.0) {
 v_Tangent = normalize((worldInverseTranspose * vec4(tangent.xyz, 0.0)).xyz);
 v_Bitangent = normalize(cross(v_Normal, v_Tangent) * tangent.w);
 }
#endif

@end


@export ecgl.common.normalMap.fragmentHeader

#ifdef NORMALMAP_ENABLED
uniform sampler2D normalMap;
varying vec3 v_Tangent;
varying vec3 v_Bitangent;
#endif

@end

@export ecgl.common.normalMap.fragmentMain
#ifdef NORMALMAP_ENABLED
 if (dot(v_Tangent, v_Tangent) > 0.0) {
 vec3 normalTexel = texture2D(normalMap, v_DetailTexcoord).xyz;
 if (dot(normalTexel, normalTexel) > 0.0) { N = normalTexel * 2.0 - 1.0;
 mat3 tbn = mat3(v_Tangent, v_Bitangent, v_Normal);
 N = normalize(tbn * N);
 }
 }
#endif
@end



@export ecgl.common.vertexAnimation.header

#ifdef VERTEX_ANIMATION
attribute vec3 prevPosition;
attribute vec3 prevNormal;
uniform float percent;
#endif

@end

@export ecgl.common.vertexAnimation.main

#ifdef VERTEX_ANIMATION
 vec3 pos = mix(prevPosition, position, percent);
 vec3 norm = mix(prevNormal, normal, percent);
#else
 vec3 pos = position;
 vec3 norm = normal;
#endif

@end


@export ecgl.common.ssaoMap.header
#ifdef SSAOMAP_ENABLED
uniform sampler2D ssaoMap;
uniform vec4 viewport : VIEWPORT;
#endif
@end

@export ecgl.common.ssaoMap.main
 float ao = 1.0;
#ifdef SSAOMAP_ENABLED
 ao = texture2D(ssaoMap, (gl_FragCoord.xy - viewport.xy) / viewport.zw).r;
#endif
@end




@export ecgl.common.diffuseLayer.header

#if (LAYER_DIFFUSEMAP_COUNT > 0)
uniform float layerDiffuseIntensity[LAYER_DIFFUSEMAP_COUNT];
uniform sampler2D layerDiffuseMap[LAYER_DIFFUSEMAP_COUNT];
#endif

@end

@export ecgl.common.emissiveLayer.header

#if (LAYER_EMISSIVEMAP_COUNT > 0)
uniform float layerEmissionIntensity[LAYER_EMISSIVEMAP_COUNT];
uniform sampler2D layerEmissiveMap[LAYER_EMISSIVEMAP_COUNT];
#endif

@end

@export ecgl.common.layers.header
@import ecgl.common.diffuseLayer.header
@import ecgl.common.emissiveLayer.header
@end

@export ecgl.common.diffuseLayer.main

#if (LAYER_DIFFUSEMAP_COUNT > 0)
 for (int _idx_ = 0; _idx_ < LAYER_DIFFUSEMAP_COUNT; _idx_++) {{
 float intensity = layerDiffuseIntensity[_idx_];
 vec4 texel2 = texture2D(layerDiffuseMap[_idx_], v_Texcoord);
 #ifdef SRGB_DECODE
 texel2 = sRGBToLinear(texel2);
 #endif
 albedoTexel.rgb = mix(albedoTexel.rgb, texel2.rgb * intensity, texel2.a);
 albedoTexel.a = texel2.a + (1.0 - texel2.a) * albedoTexel.a;
 }}
#endif

@end

@export ecgl.common.emissiveLayer.main

#if (LAYER_EMISSIVEMAP_COUNT > 0)
 for (int _idx_ = 0; _idx_ < LAYER_EMISSIVEMAP_COUNT; _idx_++)
 {{
 vec4 texel2 = texture2D(layerEmissiveMap[_idx_], v_Texcoord) * layerEmissionIntensity[_idx_];
 #ifdef SRGB_DECODE
 texel2 = sRGBToLinear(texel2);
 #endif
 float intensity = layerEmissionIntensity[_idx_];
 gl_FragColor.rgb += texel2.rgb * texel2.a * intensity;
 }}
#endif

@end
`,bm=`@export ecgl.color.vertex

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

@import ecgl.common.uv.header

attribute vec2 texcoord : TEXCOORD_0;
attribute vec3 position: POSITION;

@import ecgl.common.wireframe.vertexHeader

#ifdef VERTEX_COLOR
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;
#endif

#ifdef VERTEX_ANIMATION
attribute vec3 prevPosition;
uniform float percent : 1.0;
#endif

#ifdef ATMOSPHERE_ENABLED
attribute vec3 normal: NORMAL;
uniform mat4 worldInverseTranspose : WORLDINVERSETRANSPOSE;
varying vec3 v_Normal;
#endif

void main()
{
#ifdef VERTEX_ANIMATION
 vec3 pos = mix(prevPosition, position, percent);
#else
 vec3 pos = position;
#endif

 gl_Position = worldViewProjection * vec4(pos, 1.0);

 @import ecgl.common.uv.main

#ifdef VERTEX_COLOR
 v_Color = a_Color;
#endif

#ifdef ATMOSPHERE_ENABLED
 v_Normal = normalize((worldInverseTranspose * vec4(normal, 0.0)).xyz);
#endif

 @import ecgl.common.wireframe.vertexMain

}

@end

@export ecgl.color.fragment

#define LAYER_DIFFUSEMAP_COUNT 0
#define LAYER_EMISSIVEMAP_COUNT 0

uniform sampler2D diffuseMap;
uniform sampler2D detailMap;

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

#ifdef ATMOSPHERE_ENABLED
uniform mat4 viewTranspose: VIEWTRANSPOSE;
uniform vec3 glowColor;
uniform float glowPower;
varying vec3 v_Normal;
#endif

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif

@import ecgl.common.layers.header

@import ecgl.common.uv.fragmentHeader

@import ecgl.common.wireframe.fragmentHeader

@import clay.util.srgb

void main()
{
#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(color);
#else
 gl_FragColor = color;
#endif

#ifdef VERTEX_COLOR
 gl_FragColor *= v_Color;
#endif

 @import ecgl.common.albedo.main

 @import ecgl.common.diffuseLayer.main

 gl_FragColor *= albedoTexel;

#ifdef ATMOSPHERE_ENABLED
 float atmoIntensity = pow(1.0 - dot(v_Normal, (viewTranspose * vec4(0.0, 0.0, 1.0, 0.0)).xyz), glowPower);
 gl_FragColor.rgb += glowColor * atmoIntensity;
#endif

 @import ecgl.common.emissiveLayer.main

 @import ecgl.common.wireframe.fragmentMain

}
@end`,Am=`/**
 * http: */

@export ecgl.lambert.vertex

@import ecgl.common.transformUniforms

@import ecgl.common.uv.header


@import ecgl.common.attributes

@import ecgl.common.wireframe.vertexHeader

#ifdef VERTEX_COLOR
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;
#endif


@import ecgl.common.vertexAnimation.header


varying vec3 v_Normal;
varying vec3 v_WorldPosition;

void main()
{
 @import ecgl.common.uv.main

 @import ecgl.common.vertexAnimation.main


 gl_Position = worldViewProjection * vec4(pos, 1.0);

 v_Normal = normalize((worldInverseTranspose * vec4(norm, 0.0)).xyz);
 v_WorldPosition = (world * vec4(pos, 1.0)).xyz;

#ifdef VERTEX_COLOR
 v_Color = a_Color;
#endif

 @import ecgl.common.wireframe.vertexMain
}

@end


@export ecgl.lambert.fragment

#define LAYER_DIFFUSEMAP_COUNT 0
#define LAYER_EMISSIVEMAP_COUNT 0

#define NORMAL_UP_AXIS 1
#define NORMAL_FRONT_AXIS 2

@import ecgl.common.uv.fragmentHeader

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

uniform sampler2D diffuseMap;
uniform sampler2D detailMap;

@import ecgl.common.layers.header

uniform float emissionIntensity: 1.0;

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

uniform mat4 viewInverse : VIEWINVERSE;

#ifdef ATMOSPHERE_ENABLED
uniform mat4 viewTranspose: VIEWTRANSPOSE;
uniform vec3 glowColor;
uniform float glowPower;
#endif

#ifdef AMBIENT_LIGHT_COUNT
@import clay.header.ambient_light
#endif
#ifdef AMBIENT_SH_LIGHT_COUNT
@import clay.header.ambient_sh_light
#endif

#ifdef DIRECTIONAL_LIGHT_COUNT
@import clay.header.directional_light
#endif

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif


@import ecgl.common.ssaoMap.header

@import ecgl.common.bumpMap.header

@import clay.util.srgb

@import ecgl.common.wireframe.fragmentHeader

@import clay.plugin.compute_shadow_map

void main()
{
#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(color);
#else
 gl_FragColor = color;
#endif

#ifdef VERTEX_COLOR
 #ifdef SRGB_DECODE
 gl_FragColor *= sRGBToLinear(v_Color);
 #else
 gl_FragColor *= v_Color;
 #endif
#endif

 @import ecgl.common.albedo.main

 @import ecgl.common.diffuseLayer.main

 gl_FragColor *= albedoTexel;

 vec3 N = v_Normal;
#ifdef DOUBLE_SIDED
 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(eyePos - v_WorldPosition);

 if (dot(N, V) < 0.0) {
 N = -N;
 }
#endif

 float ambientFactor = 1.0;

#ifdef BUMPMAP_ENABLED
 N = bumpNormal(v_WorldPosition, v_Normal, N);
 ambientFactor = dot(v_Normal, N);
#endif

 vec3 N2 = vec3(N.x, N[NORMAL_UP_AXIS], N[NORMAL_FRONT_AXIS]);

 vec3 diffuseColor = vec3(0.0, 0.0, 0.0);

 @import ecgl.common.ssaoMap.main

#ifdef AMBIENT_LIGHT_COUNT
 for(int i = 0; i < AMBIENT_LIGHT_COUNT; i++)
 {
 diffuseColor += ambientLightColor[i] * ambientFactor * ao;
 }
#endif
#ifdef AMBIENT_SH_LIGHT_COUNT
 for(int _idx_ = 0; _idx_ < AMBIENT_SH_LIGHT_COUNT; _idx_++)
 {{
 diffuseColor += calcAmbientSHLight(_idx_, N2) * ambientSHLightColor[_idx_] * ao;
 }}
#endif
#ifdef DIRECTIONAL_LIGHT_COUNT
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 float shadowContribsDir[DIRECTIONAL_LIGHT_COUNT];
 if(shadowEnabled)
 {
 computeShadowOfDirectionalLights(v_WorldPosition, shadowContribsDir);
 }
#endif
 for(int i = 0; i < DIRECTIONAL_LIGHT_COUNT; i++)
 {
 vec3 lightDirection = -directionalLightDirection[i];
 vec3 lightColor = directionalLightColor[i];

 float shadowContrib = 1.0;
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 if (shadowEnabled)
 {
 shadowContrib = shadowContribsDir[i];
 }
#endif

 float ndl = dot(N, normalize(lightDirection)) * shadowContrib;

 diffuseColor += lightColor * clamp(ndl, 0.0, 1.0);
 }
#endif

 gl_FragColor.rgb *= diffuseColor;

#ifdef ATMOSPHERE_ENABLED
 float atmoIntensity = pow(1.0 - dot(v_Normal, (viewTranspose * vec4(0.0, 0.0, 1.0, 0.0)).xyz), glowPower);
 gl_FragColor.rgb += glowColor * atmoIntensity;
#endif

 @import ecgl.common.emissiveLayer.main

 @import ecgl.common.wireframe.fragmentMain
}

@end`,Em=`@export ecgl.realistic.vertex

@import ecgl.common.transformUniforms

@import ecgl.common.uv.header

@import ecgl.common.attributes


@import ecgl.common.wireframe.vertexHeader

#ifdef VERTEX_COLOR
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;
#endif

#ifdef NORMALMAP_ENABLED
attribute vec4 tangent : TANGENT;
varying vec3 v_Tangent;
varying vec3 v_Bitangent;
#endif

@import ecgl.common.vertexAnimation.header

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

void main()
{

 @import ecgl.common.uv.main

 @import ecgl.common.vertexAnimation.main

 gl_Position = worldViewProjection * vec4(pos, 1.0);

 v_Normal = normalize((worldInverseTranspose * vec4(norm, 0.0)).xyz);
 v_WorldPosition = (world * vec4(pos, 1.0)).xyz;

#ifdef VERTEX_COLOR
 v_Color = a_Color;
#endif

#ifdef NORMALMAP_ENABLED
 v_Tangent = normalize((worldInverseTranspose * vec4(tangent.xyz, 0.0)).xyz);
 v_Bitangent = normalize(cross(v_Normal, v_Tangent) * tangent.w);
#endif

 @import ecgl.common.wireframe.vertexMain

}

@end



@export ecgl.realistic.fragment

#define LAYER_DIFFUSEMAP_COUNT 0
#define LAYER_EMISSIVEMAP_COUNT 0
#define PI 3.14159265358979
#define ROUGHNESS_CHANEL 0
#define METALNESS_CHANEL 1

#define NORMAL_UP_AXIS 1
#define NORMAL_FRONT_AXIS 2

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif

@import ecgl.common.uv.fragmentHeader

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

uniform sampler2D diffuseMap;

uniform sampler2D detailMap;
uniform sampler2D metalnessMap;
uniform sampler2D roughnessMap;

@import ecgl.common.layers.header

uniform float emissionIntensity: 1.0;

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

uniform float metalness : 0.0;
uniform float roughness : 0.5;

uniform mat4 viewInverse : VIEWINVERSE;

#ifdef ATMOSPHERE_ENABLED
uniform mat4 viewTranspose: VIEWTRANSPOSE;
uniform vec3 glowColor;
uniform float glowPower;
#endif

#ifdef AMBIENT_LIGHT_COUNT
@import clay.header.ambient_light
#endif

#ifdef AMBIENT_SH_LIGHT_COUNT
@import clay.header.ambient_sh_light
#endif

#ifdef AMBIENT_CUBEMAP_LIGHT_COUNT
@import clay.header.ambient_cubemap_light
#endif

#ifdef DIRECTIONAL_LIGHT_COUNT
@import clay.header.directional_light
#endif

@import ecgl.common.normalMap.fragmentHeader

@import ecgl.common.ssaoMap.header

@import ecgl.common.bumpMap.header

@import clay.util.srgb

@import clay.util.rgbm

@import ecgl.common.wireframe.fragmentHeader

@import clay.plugin.compute_shadow_map

vec3 F_Schlick(float ndv, vec3 spec) {
 return spec + (1.0 - spec) * pow(1.0 - ndv, 5.0);
}

float D_Phong(float g, float ndh) {
 float a = pow(8192.0, g);
 return (a + 2.0) / 8.0 * pow(ndh, a);
}

void main()
{
 vec4 albedoColor = color;

 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(eyePos - v_WorldPosition);
#ifdef VERTEX_COLOR
 #ifdef SRGB_DECODE
 albedoColor *= sRGBToLinear(v_Color);
 #else
 albedoColor *= v_Color;
 #endif
#endif

 @import ecgl.common.albedo.main

 @import ecgl.common.diffuseLayer.main

 albedoColor *= albedoTexel;

 float m = metalness;

#ifdef METALNESSMAP_ENABLED
 float m2 = texture2D(metalnessMap, v_DetailTexcoord)[METALNESS_CHANEL];
 m = clamp(m2 + (m - 0.5) * 2.0, 0.0, 1.0);
#endif

 vec3 baseColor = albedoColor.rgb;
 albedoColor.rgb = baseColor * (1.0 - m);
 vec3 specFactor = mix(vec3(0.04), baseColor, m);

 float g = 1.0 - roughness;

#ifdef ROUGHNESSMAP_ENABLED
 float g2 = 1.0 - texture2D(roughnessMap, v_DetailTexcoord)[ROUGHNESS_CHANEL];
 g = clamp(g2 + (g - 0.5) * 2.0, 0.0, 1.0);
#endif

 vec3 N = v_Normal;

#ifdef DOUBLE_SIDED
 if (dot(N, V) < 0.0) {
 N = -N;
 }
#endif

 float ambientFactor = 1.0;

#ifdef BUMPMAP_ENABLED
 N = bumpNormal(v_WorldPosition, v_Normal, N);
 ambientFactor = dot(v_Normal, N);
#endif

@import ecgl.common.normalMap.fragmentMain

 vec3 N2 = vec3(N.x, N[NORMAL_UP_AXIS], N[NORMAL_FRONT_AXIS]);

 vec3 diffuseTerm = vec3(0.0);
 vec3 specularTerm = vec3(0.0);

 float ndv = clamp(dot(N, V), 0.0, 1.0);
 vec3 fresnelTerm = F_Schlick(ndv, specFactor);

 @import ecgl.common.ssaoMap.main

#ifdef AMBIENT_LIGHT_COUNT
 for(int _idx_ = 0; _idx_ < AMBIENT_LIGHT_COUNT; _idx_++)
 {{
 diffuseTerm += ambientLightColor[_idx_] * ambientFactor * ao;
 }}
#endif

#ifdef AMBIENT_SH_LIGHT_COUNT
 for(int _idx_ = 0; _idx_ < AMBIENT_SH_LIGHT_COUNT; _idx_++)
 {{
 diffuseTerm += calcAmbientSHLight(_idx_, N2) * ambientSHLightColor[_idx_] * ao;
 }}
#endif

#ifdef DIRECTIONAL_LIGHT_COUNT
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 float shadowContribsDir[DIRECTIONAL_LIGHT_COUNT];
 if(shadowEnabled)
 {
 computeShadowOfDirectionalLights(v_WorldPosition, shadowContribsDir);
 }
#endif
 for(int _idx_ = 0; _idx_ < DIRECTIONAL_LIGHT_COUNT; _idx_++)
 {{
 vec3 L = -directionalLightDirection[_idx_];
 vec3 lc = directionalLightColor[_idx_];

 vec3 H = normalize(L + V);
 float ndl = clamp(dot(N, normalize(L)), 0.0, 1.0);
 float ndh = clamp(dot(N, H), 0.0, 1.0);

 float shadowContrib = 1.0;
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 if (shadowEnabled)
 {
 shadowContrib = shadowContribsDir[_idx_];
 }
#endif

 vec3 li = lc * ndl * shadowContrib;

 diffuseTerm += li;
 specularTerm += li * fresnelTerm * D_Phong(g, ndh);
 }}
#endif


#ifdef AMBIENT_CUBEMAP_LIGHT_COUNT
 vec3 L = reflect(-V, N);
 L = vec3(L.x, L[NORMAL_UP_AXIS], L[NORMAL_FRONT_AXIS]);
 float rough2 = clamp(1.0 - g, 0.0, 1.0);
 float bias2 = rough2 * 5.0;
 vec2 brdfParam2 = texture2D(ambientCubemapLightBRDFLookup[0], vec2(rough2, ndv)).xy;
 vec3 envWeight2 = specFactor * brdfParam2.x + brdfParam2.y;
 vec3 envTexel2;
 for(int _idx_ = 0; _idx_ < AMBIENT_CUBEMAP_LIGHT_COUNT; _idx_++)
 {{
 envTexel2 = RGBMDecode(textureCubeLodEXT(ambientCubemapLightCubemap[_idx_], L, bias2), 8.12);
 specularTerm += ambientCubemapLightColor[_idx_] * envTexel2 * envWeight2 * ao;
 }}
#endif

 gl_FragColor.rgb = albedoColor.rgb * diffuseTerm + specularTerm;
 gl_FragColor.a = albedoColor.a;

#ifdef ATMOSPHERE_ENABLED
 float atmoIntensity = pow(1.0 - dot(v_Normal, (viewTranspose * vec4(0.0, 0.0, 1.0, 0.0)).xyz), glowPower);
 gl_FragColor.rgb += glowColor * atmoIntensity;
#endif

#ifdef SRGB_ENCODE
 gl_FragColor = linearTosRGB(gl_FragColor);
#endif

 @import ecgl.common.emissiveLayer.main

 @import ecgl.common.wireframe.fragmentMain
}

@end`,Lm=`@export ecgl.hatching.vertex

@import ecgl.realistic.vertex

@end


@export ecgl.hatching.fragment

#define NORMAL_UP_AXIS 1
#define NORMAL_FRONT_AXIS 2

@import ecgl.common.uv.fragmentHeader

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

uniform vec4 color : [0.0, 0.0, 0.0, 1.0];
uniform vec4 paperColor : [1.0, 1.0, 1.0, 1.0];

uniform mat4 viewInverse : VIEWINVERSE;

#ifdef AMBIENT_LIGHT_COUNT
@import clay.header.ambient_light
#endif
#ifdef AMBIENT_SH_LIGHT_COUNT
@import clay.header.ambient_sh_light
#endif

#ifdef DIRECTIONAL_LIGHT_COUNT
@import clay.header.directional_light
#endif

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif


@import ecgl.common.ssaoMap.header

@import ecgl.common.bumpMap.header

@import clay.util.srgb

@import ecgl.common.wireframe.fragmentHeader

@import clay.plugin.compute_shadow_map

uniform sampler2D hatch1;
uniform sampler2D hatch2;
uniform sampler2D hatch3;
uniform sampler2D hatch4;
uniform sampler2D hatch5;
uniform sampler2D hatch6;

float shade(in float tone) {
 vec4 c = vec4(1. ,1., 1., 1.);
 float step = 1. / 6.;
 vec2 uv = v_DetailTexcoord;
 if (tone <= step / 2.0) {
 c = mix(vec4(0.), texture2D(hatch6, uv), 12. * tone);
 }
 else if (tone <= step) {
 c = mix(texture2D(hatch6, uv), texture2D(hatch5, uv), 6. * tone);
 }
 if(tone > step && tone <= 2. * step){
 c = mix(texture2D(hatch5, uv), texture2D(hatch4, uv) , 6. * (tone - step));
 }
 if(tone > 2. * step && tone <= 3. * step){
 c = mix(texture2D(hatch4, uv), texture2D(hatch3, uv), 6. * (tone - 2. * step));
 }
 if(tone > 3. * step && tone <= 4. * step){
 c = mix(texture2D(hatch3, uv), texture2D(hatch2, uv), 6. * (tone - 3. * step));
 }
 if(tone > 4. * step && tone <= 5. * step){
 c = mix(texture2D(hatch2, uv), texture2D(hatch1, uv), 6. * (tone - 4. * step));
 }
 if(tone > 5. * step){
 c = mix(texture2D(hatch1, uv), vec4(1.), 6. * (tone - 5. * step));
 }

 return c.r;
}

const vec3 w = vec3(0.2125, 0.7154, 0.0721);

void main()
{
#ifdef SRGB_DECODE
 vec4 inkColor = sRGBToLinear(color);
#else
 vec4 inkColor = color;
#endif

#ifdef VERTEX_COLOR
 #ifdef SRGB_DECODE
 inkColor *= sRGBToLinear(v_Color);
 #else
 inkColor *= v_Color;
 #endif
#endif

 vec3 N = v_Normal;
#ifdef DOUBLE_SIDED
 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(eyePos - v_WorldPosition);

 if (dot(N, V) < 0.0) {
 N = -N;
 }
#endif

 float tone = 0.0;

 float ambientFactor = 1.0;

#ifdef BUMPMAP_ENABLED
 N = bumpNormal(v_WorldPosition, v_Normal, N);
 ambientFactor = dot(v_Normal, N);
#endif

 vec3 N2 = vec3(N.x, N[NORMAL_UP_AXIS], N[NORMAL_FRONT_AXIS]);

 @import ecgl.common.ssaoMap.main

#ifdef AMBIENT_LIGHT_COUNT
 for(int i = 0; i < AMBIENT_LIGHT_COUNT; i++)
 {
 tone += dot(ambientLightColor[i], w) * ambientFactor * ao;
 }
#endif
#ifdef AMBIENT_SH_LIGHT_COUNT
 for(int _idx_ = 0; _idx_ < AMBIENT_SH_LIGHT_COUNT; _idx_++)
 {{
 tone += dot(calcAmbientSHLight(_idx_, N2) * ambientSHLightColor[_idx_], w) * ao;
 }}
#endif
#ifdef DIRECTIONAL_LIGHT_COUNT
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 float shadowContribsDir[DIRECTIONAL_LIGHT_COUNT];
 if(shadowEnabled)
 {
 computeShadowOfDirectionalLights(v_WorldPosition, shadowContribsDir);
 }
#endif
 for(int i = 0; i < DIRECTIONAL_LIGHT_COUNT; i++)
 {
 vec3 lightDirection = -directionalLightDirection[i];
 float lightTone = dot(directionalLightColor[i], w);

 float shadowContrib = 1.0;
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 if (shadowEnabled)
 {
 shadowContrib = shadowContribsDir[i];
 }
#endif

 float ndl = dot(N, normalize(lightDirection)) * shadowContrib;

 tone += lightTone * clamp(ndl, 0.0, 1.0);
 }
#endif

 gl_FragColor = mix(inkColor, paperColor, shade(clamp(tone, 0.0, 1.0)));
 }
@end
`,Cm=`@export ecgl.sm.depth.vertex

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

attribute vec3 position : POSITION;
attribute vec2 texcoord : TEXCOORD_0;

#ifdef VERTEX_ANIMATION
attribute vec3 prevPosition;
uniform float percent : 1.0;
#endif

varying vec4 v_ViewPosition;
varying vec2 v_Texcoord;

void main(){

#ifdef VERTEX_ANIMATION
 vec3 pos = mix(prevPosition, position, percent);
#else
 vec3 pos = position;
#endif

 v_ViewPosition = worldViewProjection * vec4(pos, 1.0);
 gl_Position = v_ViewPosition;

 v_Texcoord = texcoord;

}
@end



@export ecgl.sm.depth.fragment

@import clay.sm.depth.fragment

@end`;Object.assign(Vt.prototype,wm);k.import($h);k.import(kh);k.import(Sm);k.import(bm);k.import(Am);k.import(Em);k.import(Lm);k.import(Cm);function Mm(e){return!e||e==="none"}function Kh(e){return e instanceof HTMLCanvasElement||e instanceof HTMLImageElement||e instanceof Image}function Dm(e){return e.getZr&&e.setOption}var Pm=_r.prototype.addToScene,Nm=_r.prototype.removeFromScene;_r.prototype.addToScene=function(e){if(Pm.call(this,e),this.__zr){var t=this.__zr;e.traverse(function(r){r.__zr=t,r.addAnimatorsToZr&&r.addAnimatorsToZr(t)})}};_r.prototype.removeFromScene=function(e){Nm.call(this,e),e.traverse(function(t){var r=t.__zr;t.__zr=null,r&&t.removeAnimatorsFromZr&&t.removeAnimatorsFromZr(r)})};At.prototype.setTextureImage=function(e,t,r,i){if(this.shader){var n=r.getZr(),a=this,o;return a.autoUpdateTextureStatus=!1,a.disableTexture(e),Mm(t)||(o=S.loadTexture(t,r,i,function(s){a.enableTexture(e),n&&n.refresh()}),a.set(e,o)),o}};var S={};S.Renderer=Et;S.Node=Vt;S.Mesh=Xe;S.Shader=k;S.Material=At;S.Texture=H;S.Texture2D=ne;S.Geometry=se;S.SphereGeometry=mm;S.PlaneGeometry=pa;S.CubeGeometry=qh;S.AmbientLight=_m;S.DirectionalLight=ym;S.PointLight=xm;S.SpotLight=Tm;S.PerspectiveCamera=We;S.OrthographicCamera=_i;S.Vector2=te;S.Vector3=R;S.Vector4=he;S.Quaternion=pe;S.Matrix2=st;S.Matrix2d=vt;S.Matrix3=Ue;S.Matrix4=W;S.Plane=Wi;S.Ray=Gr;S.BoundingBox=Je;S.Frustum=da;var Gn=null;function Im(){return Gn!==null||(Gn=Ht.createBlank("rgba(255,255,255,0)").image),Gn}function ou(e){return Math.pow(2,Math.round(Math.log(e)/Math.LN2))}function su(e){if((e.wrapS===H.REPEAT||e.wrapT===H.REPEAT)&&e.image){var t=ou(e.width),r=ou(e.height);if(t!==e.width||r!==e.height){var i=document.createElement("canvas");i.width=t,i.height=r;var n=i.getContext("2d");n.drawImage(e.image,0,0,t,r),e.image=i}}}S.loadTexture=function(e,t,r,i){typeof r=="function"&&(i=r,r={}),r=r||{};for(var n=Object.keys(r).sort(),a="",o=0;o<n.length;o++)a+=n[o]+"_"+r[n[o]]+"_";var s=t.__textureCache=t.__textureCache||new nd(20);if(Dm(e)){var l=e.__textureid__,u=s.get(a+l);if(u)u.texture.surface.setECharts(e),i&&i(u.texture);else{var h=new Co(e);h.onupdate=function(){t.getZr().refresh()},u={texture:h.getTexture()};for(var o=0;o<n.length;o++)u.texture[n[o]]=r[n[o]];l=e.__textureid__||"__ecgl_ec__"+u.texture.__uid__,e.__textureid__=l,s.put(a+l,u),i&&i(u.texture)}return u.texture}else if(Kh(e)){var l=e.__textureid__,u=s.get(a+l);if(!u){u={texture:new S.Texture2D({image:e})};for(var o=0;o<n.length;o++)u.texture[n[o]]=r[n[o]];l=e.__textureid__||"__ecgl_image__"+u.texture.__uid__,e.__textureid__=l,s.put(a+l,u),su(u.texture),i&&i(u.texture)}return u.texture}else{var u=s.get(a+e);if(u)u.callbacks?u.callbacks.push(i):i&&i(u.texture);else if(e.match(/.hdr$|^data:application\/octet-stream/)){u={callbacks:[i]};var f=Ht.loadTexture(e,{exposure:r.exposure,fileType:"hdr"},function(){f.dirty(),u.callbacks.forEach(function(v){v&&v(f)}),u.callbacks=null});u.texture=f,s.put(a+e,u)}else{for(var f=new S.Texture2D({image:new Image}),o=0;o<n.length;o++)f[n[o]]=r[n[o]];u={texture:f,callbacks:[i]};var d=f.image;d.onload=function(){f.image=d,su(f),f.dirty(),u.callbacks.forEach(function(p){p&&p(f)}),u.callbacks=null},d.crossOrigin="Anonymous",d.src=e,f.image=Im(),s.put(a+e,u)}return u.texture}};S.createAmbientCubemap=function(e,t,r,i){e=e||{};var n=e.texture,a=oe.firstNotNull(e.exposure,1),o=new cm({intensity:oe.firstNotNull(e.specularIntensity,1)}),s=new dm({intensity:oe.firstNotNull(e.diffuseIntensity,1),coefficients:[.844,.712,.691,-.037,.083,.167,.343,.288,.299,-.041,-.021,-.009,-.003,-.041,-.064,-.011,-.007,-.004,-.031,.034,.081,-.06,-.049,-.06,.046,.056,.05]});return o.cubemap=S.loadTexture(n,r,{exposure:a},function(){o.cubemap.flipY=!1,o.prefilter(t,32),s.coefficients=Yh.projectEnvironmentMap(t,o.cubemap,{lod:1}),i&&i()}),{specular:o,diffuse:s}};S.createBlankTexture=Ht.createBlank;S.isImage=Kh;S.additiveBlend=function(e){e.blendEquation(e.FUNC_ADD),e.blendFunc(e.SRC_ALPHA,e.ONE)};S.parseColor=function(e,t){return e instanceof Array?(t||(t=[]),t[0]=e[0],t[1]=e[1],t[2]=e[2],e.length>3?t[3]=e[3]:t[3]=1,t):(t=rh(e||"#000",t)||[0,0,0,0],t[0]/=255,t[1]/=255,t[2]/=255,t)};S.directionFromAlphaBeta=function(e,t){var r=e/180*Math.PI+Math.PI/2,i=-t/180*Math.PI+Math.PI/2,n=[],a=Math.sin(r);return n[0]=a*Math.cos(i),n[1]=-Math.cos(r),n[2]=a*Math.sin(i),n};S.getShadowResolution=function(e){var t=1024;switch(e){case"low":t=512;break;case"medium":break;case"high":t=2048;break;case"ultra":t=4096;break}return t};S.COMMON_SHADERS=["lambert","color","realistic","hatching","shadow"];S.createShader=function(e){e==="ecgl.shadow"&&(e="ecgl.displayShadow");var t=k.source(e+".vertex"),r=k.source(e+".fragment");t||console.error("Vertex shader of '%s' not exits",e),r||console.error("Fragment shader of '%s' not exits",e);var i=new k(t,r);return i.name=e,i};S.createMaterial=function(e,t){t instanceof Array||(t=[t]);var r=S.createShader(e),i=new At({shader:r});return t.forEach(function(n){typeof n=="string"&&i.define(n)}),i};S.setMaterialFromModel=function(e,t,r,i){t.autoUpdateTextureStatus=!1;var n=r.getModel(e+"Material"),a=n.get("detailTexture"),o=oe.firstNotNull(n.get("textureTiling"),1),s=oe.firstNotNull(n.get("textureOffset"),0);typeof o=="number"&&(o=[o,o]),typeof s=="number"&&(s=[s,s]);var l=o[0]>1||o[1]>1?S.Texture.REPEAT:S.Texture.CLAMP_TO_EDGE,u={anisotropic:8,wrapS:l,wrapT:l};if(e==="realistic"){var h=n.get("roughness"),f=n.get("metalness");f!=null?isNaN(f)&&(t.setTextureImage("metalnessMap",f,i,u),f=oe.firstNotNull(n.get("metalnessAdjust"),.5)):f=0,h!=null?isNaN(h)&&(t.setTextureImage("roughnessMap",h,i,u),h=oe.firstNotNull(n.get("roughnessAdjust"),.5)):h=.5;var d=n.get("normalTexture");t.setTextureImage("detailMap",a,i,u),t.setTextureImage("normalMap",d,i,u),t.set({roughness:h,metalness:f,detailUvRepeat:o,detailUvOffset:s})}else if(e==="lambert")t.setTextureImage("detailMap",a,i,u),t.set({detailUvRepeat:o,detailUvOffset:s});else if(e==="color")t.setTextureImage("detailMap",a,i,u),t.set({detailUvRepeat:o,detailUvOffset:s});else if(e==="hatching"){var c=n.get("hatchingTextures")||[];c.length<6;for(var v=0;v<6;v++)t.setTextureImage("hatch"+(v+1),c[v],i,{anisotropic:8,wrapS:S.Texture.REPEAT,wrapT:S.Texture.REPEAT});t.set({detailUvRepeat:o,detailUvOffset:s})}};S.updateVertexAnimation=function(e,t,r,i){var n=i.get("animation"),a=i.get("animationDurationUpdate"),o=i.get("animationEasingUpdate"),s=r.shadowDepthMaterial;if(n&&t&&a>0&&t.geometry.vertexCount===r.geometry.vertexCount){r.material.define("vertex","VERTEX_ANIMATION"),r.ignorePreZ=!0,s&&s.define("vertex","VERTEX_ANIMATION");for(var l=0;l<e.length;l++)r.geometry.attributes[e[l][0]].value=t.geometry.attributes[e[l][1]].value;r.geometry.dirty(),r.__percent=0,r.material.set("percent",0),r.stopAnimation(),r.animate().when(a,{__percent:1}).during(function(){r.material.set("percent",r.__percent),s&&s.set("percent",r.__percent)}).done(function(){r.ignorePreZ=!1,r.material.undefine("vertex","VERTEX_ANIMATION"),s&&s.undefine("vertex","VERTEX_ANIMATION")}).start(o)}else r.material.undefine("vertex","VERTEX_ANIMATION"),s&&s.undefine("vertex","VERTEX_ANIMATION")};var ye=function(e,t){this.id=e,this.zr=t;try{this.renderer=new Et({clearBit:0,devicePixelRatio:t.painter.dpr,preserveDrawingBuffer:!0,premultipliedAlpha:!0}),this.renderer.resize(t.painter.getWidth(),t.painter.getHeight())}catch(i){this.renderer=null,this.dom=document.createElement("div"),this.dom.style.cssText="position:absolute; left: 0; top: 0; right: 0; bottom: 0;",this.dom.className="ecgl-nowebgl",this.dom.innerHTML="Sorry, your browser does not support WebGL",console.error(i);return}this.onglobalout=this.onglobalout.bind(this),t.on("globalout",this.onglobalout),this.dom=this.renderer.canvas;var r=this.dom.style;r.position="absolute",r.left="0",r.top="0",this.views=[],this._picking=new ts({renderer:this.renderer}),this._viewsToDispose=[],this._accumulatingId=0,this._zrEventProxy=new Xr({shape:{x:-1,y:-1,width:2,height:2},__isGLToZRProxy:!0}),this._backgroundColor=null,this._disposed=!1};ye.prototype.setUnpainted=function(){};ye.prototype.addView=function(e){if(e.layer!==this){var t=this._viewsToDispose.indexOf(e);t>=0&&this._viewsToDispose.splice(t,1),this.views.push(e),e.layer=this;var r=this.zr;e.scene.traverse(function(i){i.__zr=r,i.addAnimatorsToZr&&i.addAnimatorsToZr(r)})}};function Jh(e){var t=e.__zr;e.__zr=null,t&&e.removeAnimatorsFromZr&&e.removeAnimatorsFromZr(t)}ye.prototype.removeView=function(e){if(e.layer===this){var t=this.views.indexOf(e);t>=0&&(this.views.splice(t,1),e.scene.traverse(Jh,this),e.layer=null,this._viewsToDispose.push(e))}};ye.prototype.removeViewsAll=function(){this.views.forEach(function(e){e.scene.traverse(Jh,this),e.layer=null,this._viewsToDispose.push(e)},this),this.views.length=0};ye.prototype.resize=function(e,t){var r=this.renderer;r.resize(e,t)};ye.prototype.clear=function(){var e=this.renderer.gl,t=this._backgroundColor||[0,0,0,0];e.clearColor(t[0],t[1],t[2],t[3]),e.depthMask(!0),e.colorMask(!0,!0,!0,!0),e.clear(e.DEPTH_BUFFER_BIT|e.COLOR_BUFFER_BIT)};ye.prototype.clearDepth=function(){var e=this.renderer.gl;e.clear(e.DEPTH_BUFFER_BIT)};ye.prototype.clearColor=function(){var e=this.renderer.gl;e.clearColor(0,0,0,0),e.clear(e.COLOR_BUFFER_BIT)};ye.prototype.needsRefresh=function(){this.zr.refresh()};ye.prototype.refresh=function(e){this._backgroundColor=e?S.parseColor(e):[0,0,0,0],this.renderer.clearColor=this._backgroundColor;for(var t=0;t<this.views.length;t++)this.views[t].prepareRender(this.renderer);this._doRender(!1),this._trackAndClean();for(var t=0;t<this._viewsToDispose.length;t++)this._viewsToDispose[t].dispose(this.renderer);this._viewsToDispose.length=0,this._startAccumulating()};ye.prototype.renderToCanvas=function(e){this._startAccumulating(!0),e.drawImage(this.dom,0,0,e.canvas.width,e.canvas.height)};ye.prototype._doRender=function(e){this.clear(),this.renderer.saveViewport();for(var t=0;t<this.views.length;t++)this.views[t].render(this.renderer,e);this.renderer.restoreViewport()};ye.prototype._stopAccumulating=function(){this._accumulatingId=0,clearTimeout(this._accumulatingTimeout)};var Rm=1;ye.prototype._startAccumulating=function(e){var t=this;this._stopAccumulating();for(var r=!1,i=0;i<this.views.length;i++)r=this.views[i].needsAccumulate()||r;if(!r)return;function n(a){if(!(!t._accumulatingId||a!==t._accumulatingId)){for(var o=!0,s=0;s<t.views.length;s++)o=t.views[s].isAccumulateFinished()&&r;o||(t._doRender(!0),e?n(a):vo(function(){n(a)}))}}this._accumulatingId=Rm++,e?n(t._accumulatingId):this._accumulatingTimeout=setTimeout(function(){n(t._accumulatingId)},50)};ye.prototype._trackAndClean=function(){var e=[],t=[];this._textureList&&(Jn(this._textureList),Jn(this._geometriesList));for(var r=0;r<this.views.length;r++)Om(this.views[r].scene,e,t);this._textureList&&(Qn(this.renderer,this._textureList),Qn(this.renderer,this._geometriesList)),this._textureList=e,this._geometriesList=t};function Jn(e){for(var t=0;t<e.length;t++)e[t].__used__=0}function Qn(e,t){for(var r=0;r<t.length;r++)t[r].__used__||t[r].dispose(e)}function zn(e,t){e.__used__=e.__used__||0,e.__used__++,e.__used__===1&&t.push(e)}function Om(e,t,r){var i,n;e.traverse(function(o){if(o.isRenderable()){var s=o.geometry,l=o.material;if(l!==i)for(var u=l.getTextureUniforms(),h=0;h<u.length;h++){var f=u[h],d=l.uniforms[f].value;if(d){if(d instanceof H)zn(d,t);else if(d instanceof Array)for(var c=0;c<d.length;c++)d[c]instanceof H&&zn(d[c],t)}}s!==n&&zn(s,r),i=l,n=s}});for(var a=0;a<e.lights.length;a++)e.lights[a].cubemap&&zn(e.lights[a].cubemap,t)}ye.prototype.dispose=function(){this._disposed||(this._stopAccumulating(),this._textureList&&(Jn(this._textureList),Jn(this._geometriesList),Qn(this.renderer,this._textureList),Qn(this.renderer,this._geometriesList)),this.zr.off("globalout",this.onglobalout),this._disposed=!0)};ye.prototype.onmousedown=function(e){if(!(e.target&&e.target.__isGLToZRProxy)){e=e.event;var t=this.pickObject(e.offsetX,e.offsetY);t&&(this._dispatchEvent("mousedown",e,t),this._dispatchDataEvent("mousedown",e,t)),this._downX=e.offsetX,this._downY=e.offsetY}};ye.prototype.onmousemove=function(e){if(!(e.target&&e.target.__isGLToZRProxy)){e=e.event;var t=this.pickObject(e.offsetX,e.offsetY),r=t&&t.target,i=this._hovered;this._hovered=t,i&&r!==i.target&&(i.relatedTarget=r,this._dispatchEvent("mouseout",e,i),this.zr.setCursorStyle("default")),this._dispatchEvent("mousemove",e,t),t&&(this.zr.setCursorStyle("pointer"),(!i||r!==i.target)&&this._dispatchEvent("mouseover",e,t)),this._dispatchDataEvent("mousemove",e,t)}};ye.prototype.onmouseup=function(e){if(!(e.target&&e.target.__isGLToZRProxy)){e=e.event;var t=this.pickObject(e.offsetX,e.offsetY);t&&(this._dispatchEvent("mouseup",e,t),this._dispatchDataEvent("mouseup",e,t)),this._upX=e.offsetX,this._upY=e.offsetY}};ye.prototype.onclick=ye.prototype.dblclick=function(e){if(!(e.target&&e.target.__isGLToZRProxy)){var t=this._upX-this._downX,r=this._upY-this._downY;if(!(Math.sqrt(t*t+r*r)>20)){e=e.event;var i=this.pickObject(e.offsetX,e.offsetY);i&&(this._dispatchEvent(e.type,e,i),this._dispatchDataEvent(e.type,e,i));var n=this._clickToSetFocusPoint(e);if(n){var a=n.view.setDOFFocusOnPoint(n.distance);a&&this.zr.refresh()}}}};ye.prototype._clickToSetFocusPoint=function(e){for(var t=this.renderer,r=t.viewport,i=this.views.length-1;i>=0;i--){var n=this.views[i];if(n.hasDOF()&&n.containPoint(e.offsetX,e.offsetY)){this._picking.scene=n.scene,this._picking.camera=n.camera,t.viewport=n.viewport;var a=this._picking.pick(e.offsetX,e.offsetY,!0);if(a)return a.view=n,a}}t.viewport=r};ye.prototype.onglobalout=function(e){var t=this._hovered;t&&this._dispatchEvent("mouseout",e,{target:t.target})};ye.prototype.pickObject=function(e,t){for(var r=[],i=this.renderer,n=i.viewport,a=0;a<this.views.length;a++){var o=this.views[a];o.containPoint(e,t)&&(this._picking.scene=o.scene,this._picking.camera=o.camera,i.viewport=o.viewport,this._picking.pickAll(e,t,r))}return i.viewport=n,r.sort(function(s,l){return s.distance-l.distance}),r[0]};ye.prototype._dispatchEvent=function(e,t,r){r||(r={});var i=r.target;for(r.cancelBubble=!1,r.event=t,r.type=e,r.offsetX=t.offsetX,r.offsetY=t.offsetY;i&&(i.trigger(e,r),i=i.getParent(),!r.cancelBubble););this._dispatchToView(e,r)};ye.prototype._dispatchDataEvent=function(e,t,r){var i=r&&r.target,n=i&&i.dataIndex,a=i&&i.seriesIndex,o=i&&i.eventData,s=!1,l=this._zrEventProxy;l.x=t.offsetX,l.y=t.offsetY,l.update();var u={target:l};const h=_t(l);e==="mousemove"&&(n!=null?n!==this._lastDataIndex&&(parseInt(this._lastDataIndex,10)>=0&&(h.dataIndex=this._lastDataIndex,h.seriesIndex=this._lastSeriesIndex,this.zr.handler.dispatchToElement(u,"mouseout",t)),s=!0):o!=null&&o!==this._lastEventData&&(this._lastEventData!=null&&(h.eventData=this._lastEventData,this.zr.handler.dispatchToElement(u,"mouseout",t)),s=!0),this._lastEventData=o,this._lastDataIndex=n,this._lastSeriesIndex=a),h.eventData=o,h.dataIndex=n,h.seriesIndex=a,(o!=null||parseInt(n,10)>=0&&parseInt(a,10)>=0)&&(this.zr.handler.dispatchToElement(u,e,t),s&&this.zr.handler.dispatchToElement(u,"mouseover",t))};ye.prototype._dispatchToView=function(e,t){for(var r=0;r<this.views.length;r++)this.views[r].containPoint(t.offsetX,t.offsetY)&&this.views[r].trigger(e,t)};Object.assign(ye.prototype,es);var Bm=["bar3D","line3D","map3D","scatter3D","surface","lines3D","scatterGL","scatter3D"];function Vi(e,t){if(e&&e[t]&&(e[t].normal||e[t].emphasis)){var r=e[t].normal,i=e[t].emphasis;r&&(e[t]=r),i&&(e.emphasis=e.emphasis||{},e.emphasis[t]=i)}}function Fm(e){Vi(e,"itemStyle"),Vi(e,"lineStyle"),Vi(e,"areaStyle"),Vi(e,"label")}function Un(e){e&&(e instanceof Array||(e=[e]),Y(e,function(t){if(t.axisLabel){var r=t.axisLabel;Object.assign(r,r.textStyle),r.textStyle=null}}))}function Gm(e){Y(e.series,function(t){Ut(Bm,t.type)>=0&&(Fm(t),t.coordinateSystem==="mapbox"&&(t.coordinateSystem="mapbox3D",e.mapbox3D=e.mapbox))}),Un(e.xAxis3D),Un(e.yAxis3D),Un(e.zAxis3D),Un(e.grid3D),Vi(e.geo3D)}function Qh(e){this._layers={},this._zr=e}Qh.prototype.update=function(e,t){var r=this,i=t.getZr();if(!i.getWidth()||!i.getHeight()){console.warn("Dom has no width or height");return}function n(s){i.setSleepAfterStill(0);var l;s.coordinateSystem&&s.coordinateSystem.model,l=s.get("zlevel");var u=r._layers,h=u[l];if(!h){if(h=u[l]=new ye("gl-"+l,i),i.painter.isSingleCanvas()){h.virtual=!0;var f=new ha({z:1e4,style:{image:h.renderer.canvas},silent:!0});h.__hostImage=f,i.add(f)}i.painter.insertLayer(l,h)}return h.__hostImage&&h.__hostImage.setStyle({width:h.renderer.getWidth(),height:h.renderer.getHeight()}),h}function a(s,l){s&&s.traverse(function(u){u.isRenderable&&u.isRenderable()&&(u.ignorePicking=u.$ignorePicking!=null?u.$ignorePicking:l)})}for(var o in this._layers)this._layers[o].removeViewsAll();e.eachComponent(function(s,l){if(s!=="series"){var u=t.getViewOfComponentModel(l),h=l.coordinateSystem;if(u.__ecgl__){var f;if(h){if(!h.viewGL){console.error("Can't find viewGL in coordinateSystem of component "+l.id);return}f=h.viewGL}else{if(!l.viewGL){console.error("Can't find viewGL of component "+l.id);return}f=h.viewGL}var f=h.viewGL,d=n(l);d.addView(f),u.afterRender&&u.afterRender(l,e,t,d),a(u.groupGL,l.get("silent"))}}}),e.eachSeries(function(s){var l=t.getViewOfSeriesModel(s),u=s.coordinateSystem;if(l.__ecgl__){if(u&&!u.viewGL&&!l.viewGL){console.error("Can't find viewGL of series "+l.id);return}var h=u&&u.viewGL||l.viewGL,f=n(s);f.addView(h),l.afterRender&&l.afterRender(s,e,t,f),a(l.groupGL,s.get("silent"))}})};ad(function(e){var t=e.getZr(),r=t.painter.dispose;t.painter.dispose=function(){typeof this.eachOtherLayer=="function"&&this.eachOtherLayer(function(i){i instanceof ye&&i.dispose()}),r.call(this)},t.painter.getRenderedCanvas=function(i){if(i=i||{},this._singleCanvas)return this._layers[0].dom;var n=document.createElement("canvas"),a=i.pixelRatio||this.dpr;n.width=this.getWidth()*a,n.height=this.getHeight()*a;var o=n.getContext("2d");o.dpr=a,o.clearRect(0,0,n.width,n.height),i.backgroundColor&&(o.fillStyle=i.backgroundColor,o.fillRect(0,0,n.width,n.height));var s=this.storage.getDisplayList(!0),l={},u,h=this;function f(p,_){var m=h._zlevelList;p==null&&(p=-1/0);for(var g,y=0;y<m.length;y++){var x=m[y],w=h._layers[x];if(!w.__builtin__&&x>p&&x<_){g=w;break}}g&&g.renderToCanvas&&(o.save(),g.renderToCanvas(o),o.restore())}for(var d={ctx:o},c=0;c<s.length;c++){var v=s[c];v.zlevel!==u&&(f(u,v.zlevel),u=v.zlevel),this._doPaintEl(v,d,!0,null,l)}return f(u,1/0),n}});od(function(e,t){var r=t.getZr(),i=r.__egl=r.__egl||new Qh(r);i.update(e,t)});sd(Gm);const ga={defaultOption:{viewControl:{projection:"perspective",autoRotate:!1,autoRotateDirection:"cw",autoRotateSpeed:10,autoRotateAfterStill:3,damping:.8,rotateSensitivity:1,zoomSensitivity:1,panSensitivity:1,panMouseButton:"middle",rotateMouseButton:"left",distance:150,minDistance:40,maxDistance:400,orthographicSize:150,maxOrthographicSize:400,minOrthographicSize:20,center:[0,0,0],alpha:0,beta:0,minAlpha:-90,maxAlpha:90}},setView:function(e){e=e||{},this.option.viewControl=this.option.viewControl||{},e.alpha!=null&&(this.option.viewControl.alpha=e.alpha),e.beta!=null&&(this.option.viewControl.beta=e.beta),e.distance!=null&&(this.option.viewControl.distance=e.distance),e.center!=null&&(this.option.viewControl.center=e.center)}},bi={defaultOption:{postEffect:{enable:!1,bloom:{enable:!0,intensity:.1},depthOfField:{enable:!1,focalRange:20,focalDistance:50,blurRadius:10,fstop:2.8,quality:"medium"},screenSpaceAmbientOcclusion:{enable:!1,radius:2,quality:"medium",intensity:1},screenSpaceReflection:{enable:!1,quality:"medium",maxRoughness:.8},colorCorrection:{enable:!0,exposure:0,brightness:0,contrast:1,saturation:1,lookupTexture:""},edge:{enable:!1},FXAA:{enable:!1}},temporalSuperSampling:{enable:"auto"}}},Ai={defaultOption:{light:{main:{shadow:!1,shadowQuality:"high",color:"#fff",intensity:1,alpha:0,beta:0},ambient:{color:"#fff",intensity:.2},ambientCubemap:{texture:null,exposure:1,diffuseIntensity:.5,specularIntensity:.5}}}};var ma=Rt.extend({type:"grid3D",dependencies:["xAxis3D","yAxis3D","zAxis3D"],defaultOption:{show:!0,zlevel:-10,left:0,top:0,width:"100%",height:"100%",environment:"auto",boxWidth:100,boxHeight:100,boxDepth:100,axisPointer:{show:!0,lineStyle:{color:"rgba(0, 0, 0, 0.8)",width:1},label:{show:!0,formatter:null,margin:8,textStyle:{fontSize:14,color:"#fff",backgroundColor:"rgba(0,0,0,0.5)",padding:3,borderRadius:3}}},axisLine:{show:!0,lineStyle:{color:"#333",width:2,type:"solid"}},axisTick:{show:!0,inside:!1,length:3,lineStyle:{width:1}},axisLabel:{show:!0,inside:!1,rotate:0,margin:8,textStyle:{fontSize:12}},splitLine:{show:!0,lineStyle:{color:["#ccc"],width:1,type:"solid"}},splitArea:{show:!1,areaStyle:{color:["rgba(250,250,250,0.3)","rgba(200,200,200,0.3)"]}},light:{main:{alpha:30,beta:40},ambient:{intensity:.4}},viewControl:{alpha:20,beta:40,autoRotate:!1,distance:200,minDistance:40,maxDistance:400}}});le(ma.prototype,ga);le(ma.prototype,bi);le(ma.prototype,Ai);var Fi=oe.firstNotNull,lu={left:0,middle:1,right:2};function uu(e){return e instanceof Array||(e=[e,e]),e}var gn=Qe.extend(function(){return{zr:null,viewGL:null,_center:new R,minDistance:.5,maxDistance:1.5,maxOrthographicSize:300,minOrthographicSize:30,minAlpha:-90,maxAlpha:90,minBeta:-1/0,maxBeta:1/0,autoRotateAfterStill:0,autoRotateDirection:"cw",autoRotateSpeed:60,damping:.8,rotateSensitivity:1,zoomSensitivity:1,panSensitivity:1,panMouseButton:"middle",rotateMouseButton:"left",_mode:"rotate",_camera:null,_needsUpdate:!1,_rotating:!1,_phi:0,_theta:0,_mouseX:0,_mouseY:0,_rotateVelocity:new te,_panVelocity:new te,_distance:500,_zoomSpeed:0,_stillTimeout:0,_animators:[]}},function(){["_mouseDownHandler","_mouseWheelHandler","_mouseMoveHandler","_mouseUpHandler","_pinchHandler","_contextMenuHandler","_update"].forEach(function(e){this[e]=this[e].bind(this)},this)},{init:function(){var e=this.zr;e&&(e.on("mousedown",this._mouseDownHandler),e.on("globalout",this._mouseUpHandler),e.on("mousewheel",this._mouseWheelHandler),e.on("pinch",this._pinchHandler),e.animation.on("frame",this._update),e.dom.addEventListener("contextmenu",this._contextMenuHandler))},dispose:function(){var e=this.zr;e&&(e.off("mousedown",this._mouseDownHandler),e.off("mousemove",this._mouseMoveHandler),e.off("mouseup",this._mouseUpHandler),e.off("mousewheel",this._mouseWheelHandler),e.off("pinch",this._pinchHandler),e.off("globalout",this._mouseUpHandler),e.dom.removeEventListener("contextmenu",this._contextMenuHandler),e.animation.off("frame",this._update)),this.stopAllAnimation()},getDistance:function(){return this._distance},setDistance:function(e){this._distance=e,this._needsUpdate=!0},getOrthographicSize:function(){return this._orthoSize},setOrthographicSize:function(e){this._orthoSize=e,this._needsUpdate=!0},getAlpha:function(){return this._theta/Math.PI*180},getBeta:function(){return-this._phi/Math.PI*180},getCenter:function(){return this._center.toArray()},setAlpha:function(e){e=Math.max(Math.min(this.maxAlpha,e),this.minAlpha),this._theta=e/180*Math.PI,this._needsUpdate=!0},setBeta:function(e){e=Math.max(Math.min(this.maxBeta,e),this.minBeta),this._phi=-e/180*Math.PI,this._needsUpdate=!0},setCenter:function(e){this._center.setArray(e)},setViewGL:function(e){this.viewGL=e},getCamera:function(){return this.viewGL.camera},setFromViewControlModel:function(e,t){t=t||{};var r=t.baseDistance||0,i=t.baseOrthoSize||1,n=e.get("projection");n!=="perspective"&&n!=="orthographic"&&n!=="isometric"&&(n="perspective"),this._projection=n,this.viewGL.setProjection(n);var a=e.get("distance")+r,o=e.get("orthographicSize")+i;[["damping",.8],["autoRotate",!1],["autoRotateAfterStill",3],["autoRotateDirection","cw"],["autoRotateSpeed",10],["minDistance",30],["maxDistance",400],["minOrthographicSize",30],["maxOrthographicSize",300],["minAlpha",-90],["maxAlpha",90],["minBeta",-1/0],["maxBeta",1/0],["rotateSensitivity",1],["zoomSensitivity",1],["panSensitivity",1],["panMouseButton","left"],["rotateMouseButton","middle"]].forEach(function(d){this[d[0]]=Fi(e.get(d[0]),d[1])},this),this.minDistance+=r,this.maxDistance+=r,this.minOrthographicSize+=i,this.maxOrthographicSize+=i;var s=e.ecModel,l={};["animation","animationDurationUpdate","animationEasingUpdate"].forEach(function(d){l[d]=Fi(e.get(d),s&&s.get(d))});var u=Fi(t.alpha,e.get("alpha"))||0,h=Fi(t.beta,e.get("beta"))||0,f=Fi(t.center,e.get("center"))||[0,0,0];l.animation&&l.animationDurationUpdate>0&&this._notFirst?this.animateTo({alpha:u,beta:h,center:f,distance:a,orthographicSize:o,easing:l.animationEasingUpdate,duration:l.animationDurationUpdate}):(this.setDistance(a),this.setAlpha(u),this.setBeta(h),this.setCenter(f),this.setOrthographicSize(o)),this._notFirst=!0,this._validateProperties()},_validateProperties:function(){},animateTo:function(e){var t=this.zr,r=this,i={},n={};return e.distance!=null&&(i.distance=this.getDistance(),n.distance=e.distance),e.orthographicSize!=null&&(i.orthographicSize=this.getOrthographicSize(),n.orthographicSize=e.orthographicSize),e.alpha!=null&&(i.alpha=this.getAlpha(),n.alpha=e.alpha),e.beta!=null&&(i.beta=this.getBeta(),n.beta=e.beta),e.center!=null&&(i.center=this.getCenter(),n.center=e.center),this._addAnimator(t.animation.animate(i).when(e.duration||1e3,n).during(function(){i.alpha!=null&&r.setAlpha(i.alpha),i.beta!=null&&r.setBeta(i.beta),i.distance!=null&&r.setDistance(i.distance),i.center!=null&&r.setCenter(i.center),i.orthographicSize!=null&&r.setOrthographicSize(i.orthographicSize),r._needsUpdate=!0})).start(e.easing||"linear")},stopAllAnimation:function(){for(var e=0;e<this._animators.length;e++)this._animators[e].stop();this._animators.length=0},update:function(){this._needsUpdate=!0,this._update(20)},_isAnimating:function(){return this._animators.length>0},_update:function(e){if(this._rotating){var t=(this.autoRotateDirection==="cw"?1:-1)*this.autoRotateSpeed/180*Math.PI;this._phi-=t*e/1e3,this._needsUpdate=!0}else this._rotateVelocity.len()>0&&(this._needsUpdate=!0);(Math.abs(this._zoomSpeed)>.1||this._panVelocity.len()>0)&&(this._needsUpdate=!0),this._needsUpdate&&(e=Math.min(e,50),this._updateDistanceOrSize(e),this._updatePan(e),this._updateRotate(e),this._updateTransform(),this.getCamera().update(),this.zr&&this.zr.refresh(),this.trigger("update"),this._needsUpdate=!1)},_updateRotate:function(e){var t=this._rotateVelocity;this._phi=t.y*e/20+this._phi,this._theta=t.x*e/20+this._theta,this.setAlpha(this.getAlpha()),this.setBeta(this.getBeta()),this._vectorDamping(t,Math.pow(this.damping,e/16))},_updateDistanceOrSize:function(e){this._projection==="perspective"?this._setDistance(this._distance+this._zoomSpeed*e/20):this._setOrthoSize(this._orthoSize+this._zoomSpeed*e/20),this._zoomSpeed*=Math.pow(this.damping,e/16)},_setDistance:function(e){this._distance=Math.max(Math.min(e,this.maxDistance),this.minDistance)},_setOrthoSize:function(e){this._orthoSize=Math.max(Math.min(e,this.maxOrthographicSize),this.minOrthographicSize);var t=this.getCamera(),r=this._orthoSize,i=r/this.viewGL.viewport.height*this.viewGL.viewport.width;t.left=-i/2,t.right=i/2,t.top=r/2,t.bottom=-r/2},_updatePan:function(e){var t=this._panVelocity,r=this._distance,i=this.getCamera(),n=i.worldTransform.y,a=i.worldTransform.x;this._center.scaleAndAdd(a,-t.x*r/200).scaleAndAdd(n,-t.y*r/200),this._vectorDamping(t,0)},_updateTransform:function(){var e=this.getCamera(),t=new R,r=this._theta+Math.PI/2,i=this._phi+Math.PI/2,n=Math.sin(r);t.x=n*Math.cos(i),t.y=-Math.cos(r),t.z=n*Math.sin(i),e.position.copy(this._center).scaleAndAdd(t,this._distance),e.rotation.identity().rotateY(-this._phi).rotateX(-this._theta)},_startCountingStill:function(){clearTimeout(this._stillTimeout);var e=this.autoRotateAfterStill,t=this;!isNaN(e)&&e>0&&(this._stillTimeout=setTimeout(function(){t._rotating=!0},e*1e3))},_vectorDamping:function(e,t){var r=e.len();r=r*t,r<1e-4&&(r=0),e.normalize().scale(r)},_decomposeTransform:function(){if(this.getCamera()){this.getCamera().updateWorldTransform();var e=this.getCamera().worldTransform.z,t=Math.asin(e.y),r=Math.atan2(e.x,e.z);this._theta=t,this._phi=-r,this.setBeta(this.getBeta()),this.setAlpha(this.getAlpha()),this.getCamera().aspect?this._setDistance(this.getCamera().position.dist(this._center)):this._setOrthoSize(this.getCamera().top-this.getCamera().bottom)}},_mouseDownHandler:function(e){if(!e.target&&!this._isAnimating()){var t=e.offsetX,r=e.offsetY;this.viewGL&&!this.viewGL.containPoint(t,r)||(this.zr.on("mousemove",this._mouseMoveHandler),this.zr.on("mouseup",this._mouseUpHandler),e.event.targetTouches?e.event.targetTouches.length===1&&(this._mode="rotate"):e.event.button===lu[this.rotateMouseButton]?this._mode="rotate":e.event.button===lu[this.panMouseButton]?this._mode="pan":this._mode="",this._rotateVelocity.set(0,0),this._rotating=!1,this.autoRotate&&this._startCountingStill(),this._mouseX=e.offsetX,this._mouseY=e.offsetY)}},_mouseMoveHandler:function(e){if(!(e.target&&e.target.__isGLToZRProxy)&&!this._isAnimating()){var t=uu(this.panSensitivity),r=uu(this.rotateSensitivity);this._mode==="rotate"?(this._rotateVelocity.y=(e.offsetX-this._mouseX)/this.zr.getHeight()*2*r[0],this._rotateVelocity.x=(e.offsetY-this._mouseY)/this.zr.getWidth()*2*r[1]):this._mode==="pan"&&(this._panVelocity.x=(e.offsetX-this._mouseX)/this.zr.getWidth()*t[0]*400,this._panVelocity.y=(-e.offsetY+this._mouseY)/this.zr.getHeight()*t[1]*400),this._mouseX=e.offsetX,this._mouseY=e.offsetY,e.event.preventDefault()}},_mouseWheelHandler:function(e){if(!this._isAnimating()){var t=e.event.wheelDelta||-e.event.detail;this._zoomHandler(e,t)}},_pinchHandler:function(e){this._isAnimating()||(this._zoomHandler(e,e.pinchScale>1?1:-1),this._mode="")},_zoomHandler:function(e,t){if(t!==0){var r=e.offsetX,i=e.offsetY;if(!(this.viewGL&&!this.viewGL.containPoint(r,i))){var n;this._projection==="perspective"?n=Math.max(Math.max(Math.min(this._distance-this.minDistance,this.maxDistance-this._distance))/20,.5):n=Math.max(Math.max(Math.min(this._orthoSize-this.minOrthographicSize,this.maxOrthographicSize-this._orthoSize))/20,.5),this._zoomSpeed=(t>0?-1:1)*n*this.zoomSensitivity,this._rotating=!1,this.autoRotate&&this._mode==="rotate"&&this._startCountingStill(),e.event.preventDefault()}}},_mouseUpHandler:function(){this.zr.off("mousemove",this._mouseMoveHandler),this.zr.off("mouseup",this._mouseUpHandler)},_isRightMouseButtonUsed:function(){return this.rotateMouseButton==="right"||this.panMouseButton==="right"},_contextMenuHandler:function(e){this._isRightMouseButtonUsed()&&e.preventDefault()},_addAnimator:function(e){var t=this._animators;return t.push(e),e.done(function(){var r=t.indexOf(e);r>=0&&t.splice(r,1)}),e}});Object.defineProperty(gn.prototype,"autoRotate",{get:function(e){return this._autoRotate},set:function(e){this._autoRotate=e,this._rotating=e}});const mn={convertToDynamicArray:function(e){e&&this.resetOffset();var t=this.attributes;for(var r in t)e||!t[r].value?t[r].value=[]:t[r].value=Array.prototype.slice.call(t[r].value);e||!this.indices?this.indices=[]:this.indices=Array.prototype.slice.call(this.indices)},convertToTypedArray:function(){var e=this.attributes;for(var t in e)e[t].value&&e[t].value.length>0?e[t].value=new Float32Array(e[t].value):e[t].value=null;this.indices&&this.indices.length>0&&(this.indices=this.vertexCount>65535?new Uint32Array(this.indices):new Uint16Array(this.indices)),this.dirty()}},Re={vec2:U,vec3:E,vec4:G,mat3:K,mat4:z};var Qa=Re.vec3,hu=[[0,0],[1,1]],yr=se.extend(function(){return{segmentScale:1,dynamic:!0,useNativeLine:!0,attributes:{position:new se.Attribute("position","float",3,"POSITION"),positionPrev:new se.Attribute("positionPrev","float",3),positionNext:new se.Attribute("positionNext","float",3),prevPositionPrev:new se.Attribute("prevPositionPrev","float",3),prevPosition:new se.Attribute("prevPosition","float",3),prevPositionNext:new se.Attribute("prevPositionNext","float",3),offset:new se.Attribute("offset","float",1),color:new se.Attribute("color","float",4,"COLOR")}}},{resetOffset:function(){this._vertexOffset=0,this._triangleOffset=0,this._itemVertexOffsets=[]},setVertexCount:function(e){var t=this.attributes;this.vertexCount!==e&&(t.position.init(e),t.color.init(e),this.useNativeLine||(t.positionPrev.init(e),t.positionNext.init(e),t.offset.init(e)),e>65535?this.indices instanceof Uint16Array&&(this.indices=new Uint32Array(this.indices)):this.indices instanceof Uint32Array&&(this.indices=new Uint16Array(this.indices)))},setTriangleCount:function(e){this.triangleCount!==e&&(e===0?this.indices=null:this.indices=this.vertexCount>65535?new Uint32Array(e*3):new Uint16Array(e*3))},_getCubicCurveApproxStep:function(e,t,r,i){var n=Qa.dist(e,t)+Qa.dist(r,t)+Qa.dist(i,r),a=1/(n+1)*this.segmentScale;return a},getCubicCurveVertexCount:function(e,t,r,i){var n=this._getCubicCurveApproxStep(e,t,r,i),a=Math.ceil(1/n);return this.useNativeLine?a*2:a*2+2},getCubicCurveTriangleCount:function(e,t,r,i){var n=this._getCubicCurveApproxStep(e,t,r,i),a=Math.ceil(1/n);return this.useNativeLine?0:a*2},getLineVertexCount:function(){return this.getPolylineVertexCount(hu)},getLineTriangleCount:function(){return this.getPolylineTriangleCount(hu)},getPolylineVertexCount:function(e){var t;if(typeof e=="number")t=e;else{var r=typeof e[0]!="number";t=r?e.length:e.length/3}return this.useNativeLine?(t-1)*2:(t-1)*2+2},getPolylineTriangleCount:function(e){var t;if(typeof e=="number")t=e;else{var r=typeof e[0]!="number";t=r?e.length:e.length/3}return this.useNativeLine?0:Math.max(t-1,0)*2},addCubicCurve:function(e,t,r,i,n,a){a==null&&(a=1);for(var o=e[0],s=e[1],l=e[2],u=t[0],h=t[1],f=t[2],d=r[0],c=r[1],v=r[2],p=i[0],_=i[1],m=i[2],g=this._getCubicCurveApproxStep(e,t,r,i),y=g*g,x=y*g,w=3*g,T=3*y,b=6*y,A=6*x,C=o-u*2+d,D=s-h*2+c,L=l-f*2+v,M=(u-d)*3-o+p,P=(h-c)*3-s+_,N=(f-v)*3-l+m,I=o,V=s,Z=l,B=(u-o)*w+C*T+M*x,$=(h-s)*w+D*T+P*x,q=(f-l)*w+L*T+N*x,j=C*b+M*A,Q=D*b+P*A,ie=L*b+N*A,ae=M*A,ee=P*A,be=N*A,Ae=0,Me=0,tt=Math.ceil(1/g),Ye=new Float32Array((tt+1)*3),Ye=[],ke=0,Me=0;Me<tt+1;Me++)Ye[ke++]=I,Ye[ke++]=V,Ye[ke++]=Z,I+=B,V+=$,Z+=q,B+=j,$+=Q,q+=ie,j+=ae,Q+=ee,ie+=be,Ae+=g,Ae>1&&(I=B>0?Math.min(I,p):Math.max(I,p),V=$>0?Math.min(V,_):Math.max(V,_),Z=q>0?Math.min(Z,m):Math.max(Z,m));return this.addPolyline(Ye,n,a)},addLine:function(e,t,r,i){return this.addPolyline([e,t],r,i)},addPolyline:function(e,t,r,i,n){if(e.length){var a=typeof e[0]!="number";if(n==null&&(n=a?e.length:e.length/3),!(n<2)){i==null&&(i=0),r==null&&(r=1),this._itemVertexOffsets.push(this._vertexOffset);var a=typeof e[0]!="number",o=a?typeof t[0]!="number":t.length/4===n,s=this.attributes.position,l=this.attributes.positionPrev,u=this.attributes.positionNext,h=this.attributes.color,f=this.attributes.offset,d=this.indices,c=this._vertexOffset,v,p;r=Math.max(r,.01);for(var _=i;_<n;_++){if(a)v=e[_],o?p=t[_]:p=t;else{var m=_*3;if(v=v||[],v[0]=e[m],v[1]=e[m+1],v[2]=e[m+2],o){var g=_*4;p=p||[],p[0]=t[g],p[1]=t[g+1],p[2]=t[g+2],p[3]=t[g+3]}else p=t}if(this.useNativeLine?_>1&&(s.copy(c,c-1),h.copy(c,c-1),c++):(_<n-1&&(l.set(c+2,v),l.set(c+3,v)),_>0&&(u.set(c-2,v),u.set(c-1,v)),s.set(c,v),s.set(c+1,v),h.set(c,p),h.set(c+1,p),f.set(c,r/2),f.set(c+1,-r/2),c+=2),this.useNativeLine)h.set(c,p),s.set(c,v),c++;else if(_>0){var y=this._triangleOffset*3,d=this.indices;d[y]=c-4,d[y+1]=c-3,d[y+2]=c-2,d[y+3]=c-3,d[y+4]=c-1,d[y+5]=c-2,this._triangleOffset+=2}}if(!this.useNativeLine){var x=this._vertexOffset,w=this._vertexOffset+n*2;l.copy(x,x+2),l.copy(x+1,x+3),u.copy(w-1,w-3),u.copy(w-2,w-4)}return this._vertexOffset=c,this._vertexOffset}}},setItemColor:function(e,t){for(var r=this._itemVertexOffsets[e],i=e<this._itemVertexOffsets.length-1?this._itemVertexOffsets[e+1]:this._vertexOffset,n=r;n<i;n++)this.attributes.color.set(n,t);this.dirty("color")},currentTriangleOffset:function(){return this._triangleOffset},currentVertexOffset:function(){return this._vertexOffset}});He(yr.prototype,mn);function ea(e,t,r,i,n,a,o){this._zr=e,this._x=0,this._y=0,this._rowHeight=0,this.width=i,this.height=n,this.offsetX=t,this.offsetY=r,this.dpr=o,this.gap=a}ea.prototype={constructor:ea,clear:function(){this._x=0,this._y=0,this._rowHeight=0},add:function(e,t,r){var i=e.getBoundingRect();t==null&&(t=i.width),r==null&&(r=i.height),t*=this.dpr,r*=this.dpr,this._fitElement(e,t,r);var n=this._x,a=this._y,o=this.width*this.dpr,s=this.height*this.dpr,l=this.gap;if(n+t+l>o&&(n=this._x=0,a+=this._rowHeight+l,this._y=a,this._rowHeight=0),this._x+=t+l,this._rowHeight=Math.max(this._rowHeight,r),a+r+l>s)return null;e.x+=this.offsetX*this.dpr+n,e.y+=this.offsetY*this.dpr+a,this._zr.add(e);var u=[this.offsetX/this.width,this.offsetY/this.height],h=[[n/o+u[0],a/s+u[1]],[(n+t)/o+u[0],(a+r)/s+u[1]]];return h},_fitElement:function(e,t,r){var i=e.getBoundingRect(),n=t/i.width,a=r/i.height;e.x=-i.x*n,e.y=-i.y*a,e.scaleX=n,e.scaleY=a,e.update()}};function ta(e){e=e||{},e.width=e.width||512,e.height=e.height||512,e.devicePixelRatio=e.devicePixelRatio||1,e.gap=e.gap==null?2:e.gap;var t=document.createElement("canvas");t.width=e.width*e.devicePixelRatio,t.height=e.height*e.devicePixelRatio,this._canvas=t,this._texture=new ne({image:t,flipY:!1});var r=this;this._zr=ld(t);var i=this._zr.refreshImmediately;this._zr.refreshImmediately=function(){i.call(this),r._texture.dirty(),r.onupdate&&r.onupdate()},this._dpr=e.devicePixelRatio,this._coords={},this.onupdate=e.onupdate,this._gap=e.gap,this._textureAtlasNodes=[new ea(this._zr,0,0,e.width,e.height,this._gap,this._dpr)],this._nodeWidth=e.width,this._nodeHeight=e.height,this._currentNodeIdx=0}ta.prototype={clear:function(){for(var e=0;e<this._textureAtlasNodes.length;e++)this._textureAtlasNodes[e].clear();this._currentNodeIdx=0,this._zr.clear(),this._coords={}},getWidth:function(){return this._width},getHeight:function(){return this._height},getTexture:function(){return this._texture},getDevicePixelRatio:function(){return this._dpr},getZr:function(){return this._zr},_getCurrentNode:function(){return this._textureAtlasNodes[this._currentNodeIdx]},_expand:function(){if(this._currentNodeIdx++,this._textureAtlasNodes[this._currentNodeIdx])return this._textureAtlasNodes[this._currentNodeIdx];var e=4096/this._dpr,t=this._textureAtlasNodes,r=t.length,i=r*this._nodeWidth%e,n=Math.floor(r*this._nodeWidth/e)*this._nodeHeight;if(!(n>=e)){var a=(i+this._nodeWidth)*this._dpr,o=(n+this._nodeHeight)*this._dpr;try{this._zr.resize({width:a,height:o})}catch{this._canvas.width=a,this._canvas.height=o}var s=new ea(this._zr,i,n,this._nodeWidth,this._nodeHeight,this._gap,this._dpr);return this._textureAtlasNodes.push(s),s}},add:function(e,t,r){if(this._coords[e.id])return this._coords[e.id];var i=this._getCurrentNode().add(e,t,r);if(!i){var n=this._expand();if(!n)return;i=n.add(e,t,r)}return this._coords[e.id]=i,i},getCoordsScale:function(){var e=this._dpr;return[this._nodeWidth/this._canvas.width*e,this._nodeHeight/this._canvas.height*e]},getCoords:function(e){return this._coords[e]},dispose:function(){this._zr.dispose()}};function mr(){}mr.prototype={constructor:mr,setScene:function(e){this._scene=e,this._skybox&&this._skybox.attachScene(this._scene)},initLight:function(e){this._lightRoot=e,this.mainLight=new S.DirectionalLight({shadowBias:.005}),this.ambientLight=new S.AmbientLight,e.add(this.mainLight),e.add(this.ambientLight)},dispose:function(){this._lightRoot&&(this._lightRoot.remove(this.mainLight),this._lightRoot.remove(this.ambientLight))},updateLight:function(e){var t=this.mainLight,r=this.ambientLight,i=e.getModel("light"),n=i.getModel("main"),a=i.getModel("ambient");t.intensity=n.get("intensity"),r.intensity=a.get("intensity"),t.color=S.parseColor(n.get("color")).slice(0,3),r.color=S.parseColor(a.get("color")).slice(0,3);var o=n.get("alpha")||0,s=n.get("beta")||0;t.position.setArray(S.directionFromAlphaBeta(o,s)),t.lookAt(S.Vector3.ZERO),t.castShadow=n.get("shadow"),t.shadowResolution=S.getShadowResolution(n.get("shadowQuality"))},updateAmbientCubemap:function(e,t,r){var i=t.getModel("light.ambientCubemap"),n=i.get("texture");if(n){this._cubemapLightsCache=this._cubemapLightsCache||{};var a=this._cubemapLightsCache[n];if(!a){var o=this;a=this._cubemapLightsCache[n]=S.createAmbientCubemap(i.option,e,r,function(){o._isSkyboxFromAmbientCubemap&&o._skybox.setEnvironmentMap(a.specular.cubemap),r.getZr().refresh()})}this._lightRoot.add(a.diffuse),this._lightRoot.add(a.specular),this._currentCubemapLights=a}else this._currentCubemapLights&&(this._lightRoot.remove(this._currentCubemapLights.diffuse),this._lightRoot.remove(this._currentCubemapLights.specular),this._currentCubemapLights=null)},updateSkybox:function(e,t,r){var i=t.get("environment"),n=this;function a(){return n._skybox=n._skybox||new Qi,n._skybox}var o=a();if(i&&i!=="none")if(i==="auto")if(this._isSkyboxFromAmbientCubemap=!0,this._currentCubemapLights){var s=this._currentCubemapLights.specular.cubemap;o.setEnvironmentMap(s),this._scene&&o.attachScene(this._scene),o.material.set("lod",3)}else this._skybox&&this._skybox.detachScene();else if(typeof i=="object"&&i.colorStops||typeof i=="string"&&rh(i)){this._isSkyboxFromAmbientCubemap=!1;var l=new S.Texture2D({anisotropic:8,flipY:!1});o.setEnvironmentMap(l);var u=l.image=document.createElement("canvas");u.width=u.height=16;var h=u.getContext("2d"),f=new Xr({shape:{x:0,y:0,width:16,height:16},style:{fill:i}});ih(h,f),o.attachScene(this._scene)}else{this._isSkyboxFromAmbientCubemap=!1;var l=S.loadTexture(i,r,{anisotropic:8,flipY:!1});o.setEnvironmentMap(l),o.attachScene(this._scene)}else this._skybox&&this._skybox.detachScene(this._scene),this._skybox=null;var d=t.coordinateSystem;if(this._skybox)if(d&&d.viewGL&&i!=="auto"&&!(i.match&&i.match(/.hdr$/))){var c=d.viewGL.isLinearSpace()?"define":"undefine";this._skybox.material[c]("fragment","SRGB_DECODE")}else this._skybox.material.undefine("fragment","SRGB_DECODE")}};var Er=Re.vec3,ef=se.extend(function(){return{segmentScale:1,useNativeLine:!0,attributes:{position:new se.Attribute("position","float",3,"POSITION"),normal:new se.Attribute("normal","float",3,"NORMAL"),color:new se.Attribute("color","float",4,"COLOR")}}},{resetOffset:function(){this._vertexOffset=0,this._faceOffset=0},setQuadCount:function(e){var t=this.attributes,r=this.getQuadVertexCount()*e,i=this.getQuadTriangleCount()*e;this.vertexCount!==r&&(t.position.init(r),t.normal.init(r),t.color.init(r)),this.triangleCount!==i&&(this.indices=r>65535?new Uint32Array(i*3):new Uint16Array(i*3))},getQuadVertexCount:function(){return 4},getQuadTriangleCount:function(){return 2},addQuad:function(){var e=Er.create(),t=Er.create(),r=Er.create(),i=[0,3,1,3,2,1];return function(n,a){var o=this.attributes.position,s=this.attributes.normal,l=this.attributes.color;Er.sub(e,n[1],n[0]),Er.sub(t,n[2],n[1]),Er.cross(r,e,t),Er.normalize(r,r);for(var u=0;u<4;u++)o.set(this._vertexOffset+u,n[u]),l.set(this._vertexOffset+u,a),s.set(this._vertexOffset+u,r);for(var h=this._faceOffset*3,u=0;u<6;u++)this.indices[h+u]=i[u]+this._vertexOffset;this._vertexOffset+=4,this._faceOffset+=2}}()});He(ef.prototype,mn);var Mo=oe.firstNotNull,zm={x:0,y:2,z:1};function Um(e,t,r,i){var n=[0,0,0],a=i<0?r.getExtentMin():r.getExtentMax();n[zm[r.dim]]=a,e.position.setArray(n),e.rotation.identity(),t.distance=-Math.abs(a),t.normal.set(0,0,0),r.dim==="x"?(e.rotation.rotateY(i*Math.PI/2),t.normal.x=-i):r.dim==="z"?(e.rotation.rotateX(-i*Math.PI/2),t.normal.y=-i):(i>0&&e.rotation.rotateY(Math.PI),t.normal.z=-i)}function _a(e,t,r){this.rootNode=new S.Node;var i=new S.Mesh({geometry:new yr({useNativeLine:!1}),material:t,castShadow:!1,ignorePicking:!0,$ignorePicking:!0,renderOrder:1}),n=new S.Mesh({geometry:new ef,material:r,castShadow:!1,culling:!1,ignorePicking:!0,$ignorePicking:!0,renderOrder:0});this.rootNode.add(n),this.rootNode.add(i),this.faceInfo=e,this.plane=new S.Plane,this.linesMesh=i,this.quadsMesh=n}_a.prototype.update=function(e,t,r){var i=e.coordinateSystem,n=[i.getAxis(this.faceInfo[0]),i.getAxis(this.faceInfo[1])],a=this.linesMesh.geometry,o=this.quadsMesh.geometry;a.convertToDynamicArray(!0),o.convertToDynamicArray(!0),this._updateSplitLines(a,n,e,r),this._udpateSplitAreas(o,n,e,r),a.convertToTypedArray(),o.convertToTypedArray();var s=i.getAxis(this.faceInfo[2]);Um(this.rootNode,this.plane,s,this.faceInfo[3])};_a.prototype._updateSplitLines=function(e,t,r,i){var n=i.getDevicePixelRatio();t.forEach(function(a,o){var s=a.model,l=t[1-o].getExtent();if(!a.scale.isBlank()){var u=s.getModel("splitLine",r.getModel("splitLine"));if(u.get("show")){var h=u.getModel("lineStyle"),f=h.get("color"),d=Mo(h.get("opacity"),1),c=Mo(h.get("width"),1);f=Be(f)?f:[f];for(var v=a.getTicksCoords({tickModel:u}),p=0,_=0;_<v.length;_++){var m=v[_].coord,g=S.parseColor(f[p%f.length]);g[3]*=d;var y=[0,0,0],x=[0,0,0];y[o]=x[o]=m,y[1-o]=l[0],x[1-o]=l[1],e.addLine(y,x,g,c*n),p++}}}})};_a.prototype._udpateSplitAreas=function(e,t,r,i){t.forEach(function(n,a){var o=n.model,s=t[1-a].getExtent();if(!n.scale.isBlank()){var l=o.getModel("splitArea",r.getModel("splitArea"));if(l.get("show")){var u=l.getModel("areaStyle"),h=u.get("color"),f=Mo(u.get("opacity"),1);h=Be(h)?h:[h];for(var d=n.getTicksCoords({tickModel:l,clamp:!0}),c=0,v=[0,0,0],p=[0,0,0],_=0;_<d.length;_++){var m=d[_].coord,g=[0,0,0],y=[0,0,0];if(g[a]=y[a]=m,g[1-a]=s[0],y[1-a]=s[1],_===0){v=g,p=y;continue}var x=S.parseColor(h[c%h.length]);x[3]*=f,e.addQuad([v,g,y,p],x),v=g,p=y,c++}}}})};var fu=[0,1,2,0,2,3],tf=se.extend(function(){return{attributes:{position:new se.Attribute("position","float",3,"POSITION"),texcoord:new se.Attribute("texcoord","float",2,"TEXCOORD_0"),offset:new se.Attribute("offset","float",2),color:new se.Attribute("color","float",4,"COLOR")}}},{resetOffset:function(){this._vertexOffset=0,this._faceOffset=0},setSpriteCount:function(e){this._spriteCount=e;var t=e*4,r=e*2;this.vertexCount!==t&&(this.attributes.position.init(t),this.attributes.offset.init(t),this.attributes.color.init(t)),this.triangleCount!==r&&(this.indices=t>65535?new Uint32Array(r*3):new Uint16Array(r*3))},setSpriteAlign:function(e,t,r,i,n){r==null&&(r="left"),i==null&&(i="top");var a,o,s,l;switch(n=n||0,r){case"left":a=n,s=t[0]+n;break;case"center":case"middle":a=-t[0]/2,s=t[0]/2;break;case"right":a=-t[0]-n,s=-n;break}switch(i){case"bottom":o=n,l=t[1]+n;break;case"middle":o=-t[1]/2,l=t[1]/2;break;case"top":o=-t[1]-n,l=-n;break}var u=e*4,h=this.attributes.offset;h.set(u,[a,l]),h.set(u+1,[s,l]),h.set(u+2,[s,o]),h.set(u+3,[a,o])},addSprite:function(e,t,r,i,n,a){var o=this._vertexOffset;this.setSprite(this._vertexOffset/4,e,t,r,i,n,a);for(var s=0;s<fu.length;s++)this.indices[this._faceOffset*3+s]=fu[s]+o;return this._faceOffset+=2,this._vertexOffset+=4,o/4},setSprite:function(e,t,r,i,n,a,o){for(var s=e*4,l=this.attributes,u=0;u<4;u++)l.position.set(s+u,t);var h=l.texcoord;h.set(s,[i[0][0],i[0][1]]),h.set(s+1,[i[1][0],i[0][1]]),h.set(s+2,[i[1][0],i[1][1]]),h.set(s+3,[i[0][0],i[1][1]]),this.setSpriteAlign(e,r,n,a,o)}});He(tf.prototype,mn);const Vm=`@export ecgl.labels.vertex

attribute vec3 position: POSITION;
attribute vec2 texcoord: TEXCOORD_0;
attribute vec2 offset;
#ifdef VERTEX_COLOR
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;
#endif

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform vec4 viewport : VIEWPORT;

varying vec2 v_Texcoord;

void main()
{
 vec4 proj = worldViewProjection * vec4(position, 1.0);

 vec2 screen = (proj.xy / abs(proj.w) + 1.0) * 0.5 * viewport.zw;

 screen += offset;

 proj.xy = (screen / viewport.zw - 0.5) * 2.0 * abs(proj.w);
 gl_Position = proj;
#ifdef VERTEX_COLOR
 v_Color = a_Color;
#endif
 v_Texcoord = texcoord;
}
@end


@export ecgl.labels.fragment

uniform vec3 color : [1.0, 1.0, 1.0];
uniform float alpha : 1.0;
uniform sampler2D textureAtlas;
uniform vec2 uvScale: [1.0, 1.0];

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif
varying float v_Miter;

varying vec2 v_Texcoord;

void main()
{
 gl_FragColor = vec4(color, alpha) * texture2D(textureAtlas, v_Texcoord * uvScale);
#ifdef VERTEX_COLOR
 gl_FragColor *= v_Color;
#endif
}

@end`;S.Shader.import(Vm);const ns=S.Mesh.extend(function(){var e=new tf({dynamic:!0}),t=new S.Material({shader:S.createShader("ecgl.labels"),transparent:!0,depthMask:!1});return{geometry:e,material:t,culling:!1,castShadow:!1,ignorePicking:!0}});var Lr=oe.firstNotNull,Cr={x:0,y:2,z:1};function as(e,t){var r=new S.Mesh({geometry:new yr({useNativeLine:!1}),material:t,castShadow:!1,ignorePicking:!0,renderOrder:2}),i=new ns;i.material.depthMask=!1;var n=new S.Node;n.add(r),n.add(i),this.rootNode=n,this.dim=e,this.linesMesh=r,this.labelsMesh=i,this.axisLineCoords=null,this.labelElements=[]}var eo={x:"y",y:"x",z:"y"};as.prototype.update=function(e,t,r){var i=e.coordinateSystem,n=i.getAxis(this.dim),a=this.linesMesh.geometry,o=this.labelsMesh.geometry;a.convertToDynamicArray(!0),o.convertToDynamicArray(!0);var s=n.model,l=n.getExtent(),L=r.getDevicePixelRatio(),u=s.getModel("axisLine",e.getModel("axisLine")),h=s.getModel("axisTick",e.getModel("axisTick")),f=s.getModel("axisLabel",e.getModel("axisLabel")),d=u.get("lineStyle.color");if(u.get("show")){var c=u.getModel("lineStyle"),v=[0,0,0],p=[0,0,0],_=Cr[n.dim];v[_]=l[0],p[_]=l[1],this.axisLineCoords=[v,p];var m=S.parseColor(d),g=Lr(c.get("width"),1),y=Lr(c.get("opacity"),1);m[3]*=y,a.addLine(v,p,m,g*L)}if(h.get("show")){var x=h.getModel("lineStyle"),w=S.parseColor(Lr(x.get("color"),d)),g=Lr(x.get("width"),1);w[3]*=Lr(x.get("opacity"),1);for(var T=n.getTicksCoords(),b=h.get("length"),A=0;A<T.length;A++){var C=T[A].coord,v=[0,0,0],p=[0,0,0],_=Cr[n.dim],D=Cr[eo[n.dim]];v[_]=p[_]=C,p[D]=b,a.addLine(v,p,w,g*L)}}this.labelElements=[];var L=r.getDevicePixelRatio();if(f.get("show"))for(var T=n.getTicksCoords(),M=s.get("data"),P=f.get("margin"),N=n.getViewLabels(),A=0;A<N.length;A++){var I=N[A].tickValue,V=N[A].formattedLabel,Z=N[A].rawLabel,C=n.dataToCoord(I),B=[0,0,0],_=Cr[n.dim],D=Cr[eo[n.dim]];B[_]=B[_]=C,B[D]=P;var $=f;M&&M[I]&&M[I].textStyle&&($=new zr(M[I].textStyle,f,s.ecModel));var q=Lr($.get("color"),d),j=new gr({style:$n($,{text:V,fill:typeof q=="function"?q(n.type==="category"?Z:n.type==="value"?I+"":I,A):q,verticalAlign:"top",align:"left"})}),Q=t.add(j),ie=j.getBoundingRect();o.addSprite(B,[ie.width*L,ie.height*L],Q),this.labelElements.push(j)}if(s.get("name")){var ae=s.getModel("nameTextStyle"),B=[0,0,0],_=Cr[n.dim],D=Cr[eo[n.dim]],ee=Lr(ae.get("color"),d),be=ae.get("borderColor"),g=ae.get("borderWidth");B[_]=B[_]=(l[0]+l[1])/2,B[D]=s.get("nameGap");var j=new gr({style:$n(ae,{text:s.get("name"),fill:ee,stroke:be,lineWidth:g})}),Q=t.add(j),ie=j.getBoundingRect();o.addSprite(B,[ie.width*L,ie.height*L],Q),j.__idx=this.labelElements.length,this.nameLabelElement=j}this.labelsMesh.material.set("textureAtlas",t.getTexture()),this.labelsMesh.material.set("uvScale",t.getCoordsScale()),a.convertToTypedArray(),o.convertToTypedArray()};as.prototype.setSpriteAlign=function(e,t,r){for(var i=r.getDevicePixelRatio(),n=this.labelsMesh.geometry,a=0;a<this.labelElements.length;a++){var o=this.labelElements[a],s=o.getBoundingRect();n.setSpriteAlign(a,[s.width*i,s.height*i],e,t)}var l=this.nameLabelElement;if(l){var s=l.getBoundingRect();n.setSpriteAlign(l.__idx,[s.width*i,s.height*i],e,t),n.dirty()}this.textAlign=e,this.textVerticalAlign=t};const ya=`@export ecgl.lines3D.vertex

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

attribute vec3 position: POSITION;
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;

void main()
{
 gl_Position = worldViewProjection * vec4(position, 1.0);
 v_Color = a_Color;
}

@end

@export ecgl.lines3D.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

varying vec4 v_Color;

@import clay.util.srgb

void main()
{
#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(color * v_Color);
#else
 gl_FragColor = color * v_Color;
#endif
}
@end



@export ecgl.lines3D.clipNear

vec4 clipNear(vec4 p1, vec4 p2) {
 float n = (p1.w - near) / (p1.w - p2.w);
 return vec4(mix(p1.xy, p2.xy, n), -near, near);
}

@end

@export ecgl.lines3D.expandLine
#ifdef VERTEX_ANIMATION
 vec4 prevProj = worldViewProjection * vec4(mix(prevPositionPrev, positionPrev, percent), 1.0);
 vec4 currProj = worldViewProjection * vec4(mix(prevPosition, position, percent), 1.0);
 vec4 nextProj = worldViewProjection * vec4(mix(prevPositionNext, positionNext, percent), 1.0);
#else
 vec4 prevProj = worldViewProjection * vec4(positionPrev, 1.0);
 vec4 currProj = worldViewProjection * vec4(position, 1.0);
 vec4 nextProj = worldViewProjection * vec4(positionNext, 1.0);
#endif

 if (currProj.w < 0.0) {
 if (nextProj.w > 0.0) {
 currProj = clipNear(currProj, nextProj);
 }
 else if (prevProj.w > 0.0) {
 currProj = clipNear(currProj, prevProj);
 }
 }

 vec2 prevScreen = (prevProj.xy / abs(prevProj.w) + 1.0) * 0.5 * viewport.zw;
 vec2 currScreen = (currProj.xy / abs(currProj.w) + 1.0) * 0.5 * viewport.zw;
 vec2 nextScreen = (nextProj.xy / abs(nextProj.w) + 1.0) * 0.5 * viewport.zw;

 vec2 dir;
 float len = offset;
 if (position == positionPrev) {
 dir = normalize(nextScreen - currScreen);
 }
 else if (position == positionNext) {
 dir = normalize(currScreen - prevScreen);
 }
 else {
 vec2 dirA = normalize(currScreen - prevScreen);
 vec2 dirB = normalize(nextScreen - currScreen);

 vec2 tanget = normalize(dirA + dirB);

 float miter = 1.0 / max(dot(tanget, dirA), 0.5);
 len *= miter;
 dir = tanget;
 }

 dir = vec2(-dir.y, dir.x) * len;
 currScreen += dir;

 currProj.xy = (currScreen / viewport.zw - 0.5) * 2.0 * abs(currProj.w);
@end


@export ecgl.meshLines3D.vertex

attribute vec3 position: POSITION;
attribute vec3 positionPrev;
attribute vec3 positionNext;
attribute float offset;
attribute vec4 a_Color : COLOR;

#ifdef VERTEX_ANIMATION
attribute vec3 prevPosition;
attribute vec3 prevPositionPrev;
attribute vec3 prevPositionNext;
uniform float percent : 1.0;
#endif

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform vec4 viewport : VIEWPORT;
uniform float near : NEAR;

varying vec4 v_Color;

@import ecgl.common.wireframe.vertexHeader

@import ecgl.lines3D.clipNear

void main()
{
 @import ecgl.lines3D.expandLine

 gl_Position = currProj;

 v_Color = a_Color;

 @import ecgl.common.wireframe.vertexMain
}
@end


@export ecgl.meshLines3D.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

varying vec4 v_Color;

@import ecgl.common.wireframe.fragmentHeader

@import clay.util.srgb

void main()
{
#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(color * v_Color);
#else
 gl_FragColor = color * v_Color;
#endif

 @import ecgl.common.wireframe.fragmentMain
}

@end`;var cu=oe.firstNotNull;S.Shader.import(ya);var Mr={x:0,y:2,z:1};const Hm=Qt.extend({type:"grid3D",__ecgl__:!0,init:function(e,t){var r=[["y","z","x",-1,"left"],["y","z","x",1,"right"],["x","y","z",-1,"bottom"],["x","y","z",1,"top"],["x","z","y",-1,"far"],["x","z","y",1,"near"]],i=["x","y","z"],n=new S.Material({shader:S.createShader("ecgl.color"),depthMask:!1,transparent:!0}),a=new S.Material({shader:S.createShader("ecgl.meshLines3D"),depthMask:!1,transparent:!0});n.define("fragment","DOUBLE_SIDED"),n.define("both","VERTEX_COLOR"),this.groupGL=new S.Node,this._control=new gn({zr:t.getZr()}),this._control.init(),this._faces=r.map(function(s){var l=new _a(s,a,n);return this.groupGL.add(l.rootNode),l},this),this._axes=i.map(function(s){var l=new as(s,a);return this.groupGL.add(l.rootNode),l},this);var o=t.getDevicePixelRatio();this._axisLabelSurface=new ta({width:256,height:256,devicePixelRatio:o}),this._axisLabelSurface.onupdate=function(){t.getZr().refresh()},this._axisPointerLineMesh=new S.Mesh({geometry:new yr({useNativeLine:!1}),material:a,castShadow:!1,ignorePicking:!0,renderOrder:3}),this.groupGL.add(this._axisPointerLineMesh),this._axisPointerLabelsSurface=new ta({width:128,height:128,devicePixelRatio:o}),this._axisPointerLabelsMesh=new ns({ignorePicking:!0,renderOrder:4,castShadow:!1}),this._axisPointerLabelsMesh.material.set("textureAtlas",this._axisPointerLabelsSurface.getTexture()),this.groupGL.add(this._axisPointerLabelsMesh),this._lightRoot=new S.Node,this._sceneHelper=new mr,this._sceneHelper.initLight(this._lightRoot)},render:function(e,t,r){this._model=e,this._api=r;var i=e.coordinateSystem;i.viewGL.add(this._lightRoot),e.get("show")?i.viewGL.add(this.groupGL):i.viewGL.remove(this.groupGL);var n=this._control;n.setViewGL(i.viewGL);var a=e.getModel("viewControl");n.setFromViewControlModel(a,0),this._axisLabelSurface.clear(),n.off("update"),e.get("show")&&(this._faces.forEach(function(o){o.update(e,t,r)},this),this._axes.forEach(function(o){o.update(e,this._axisLabelSurface,r)},this)),n.on("update",this._onCameraChange.bind(this,e,r),this),this._sceneHelper.setScene(i.viewGL.scene),this._sceneHelper.updateLight(e),i.viewGL.setPostEffect(e.getModel("postEffect"),r),i.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling")),this._initMouseHandler(e)},afterRender:function(e,t,r,i){var n=i.renderer;this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r)},showAxisPointer:function(e,t,r,i){this._doShowAxisPointer(),this._updateAxisPointer(i.value)},hideAxisPointer:function(e,t,r,i){this._doHideAxisPointer()},_initMouseHandler:function(e){var t=e.coordinateSystem,r=t.viewGL;e.get("show")&&e.get("axisPointer.show")?r.on("mousemove",this._updateAxisPointerOnMousePosition,this):r.off("mousemove",this._updateAxisPointerOnMousePosition)},_updateAxisPointerOnMousePosition:function(e){if(!e.target){for(var t=this._model,r=t.coordinateSystem,i=r.viewGL,n=i.castRay(e.offsetX,e.offsetY,new S.Ray),a,o=0;o<this._faces.length;o++){var s=this._faces[o];if(!s.rootNode.invisible){s.plane.normal.dot(i.camera.worldTransform.z)<0&&s.plane.normal.negate();var l=n.intersectPlane(s.plane);if(l){var u=r.getAxis(s.faceInfo[0]),h=r.getAxis(s.faceInfo[1]),f=Mr[s.faceInfo[0]],d=Mr[s.faceInfo[1]];u.contain(l.array[f])&&h.contain(l.array[d])&&(a=l)}}}if(a){var c=r.pointToData(a.array,[],!0);this._updateAxisPointer(c),this._doShowAxisPointer()}else this._doHideAxisPointer()}},_onCameraChange:function(e,t){e.get("show")&&(this._updateFaceVisibility(),this._updateAxisLinePosition());var r=this._control;t.dispatchAction({type:"grid3DChangeCamera",alpha:r.getAlpha(),beta:r.getBeta(),distance:r.getDistance(),center:r.getCenter(),from:this.uid,grid3DId:e.id})},_updateFaceVisibility:function(){var e=this._control.getCamera(),t=new S.Vector3;e.update();for(var r=0;r<this._faces.length/2;r++){for(var i=[],n=0;n<2;n++){var a=this._faces[r*2+n];a.rootNode.getWorldPosition(t),t.transformMat4(e.viewMatrix),i[n]=t.z}var o=i[0]>i[1]?0:1,s=this._faces[r*2+o],l=this._faces[r*2+1-o];s.rootNode.invisible=!0,l.rootNode.invisible=!1}},_updateAxisLinePosition:function(){var e=this._model.coordinateSystem,t=e.getAxis("x"),r=e.getAxis("y"),i=e.getAxis("z"),n=i.getExtentMax(),a=i.getExtentMin(),o=t.getExtentMin(),s=t.getExtentMax(),l=r.getExtentMax(),u=r.getExtentMin(),h=this._axes[0].rootNode,f=this._axes[1].rootNode,d=this._axes[2].rootNode,c=this._faces,v=c[4].rootNode.invisible?u:l,p=c[2].rootNode.invisible?n:a,_=c[0].rootNode.invisible?o:s,m=c[2].rootNode.invisible?n:a,g=c[0].rootNode.invisible?s:o,y=c[4].rootNode.invisible?u:l;h.rotation.identity(),f.rotation.identity(),d.rotation.identity(),c[4].rootNode.invisible&&(this._axes[0].flipped=!0,h.rotation.rotateX(Math.PI)),c[0].rootNode.invisible&&(this._axes[1].flipped=!0,f.rotation.rotateZ(Math.PI)),c[4].rootNode.invisible&&(this._axes[2].flipped=!0,d.rotation.rotateY(Math.PI)),h.position.set(0,p,v),f.position.set(_,m,0),d.position.set(g,0,y),h.update(),f.update(),d.update(),this._updateAxisLabelAlign()},_updateAxisLabelAlign:function(){var e=this._control.getCamera(),t=[new S.Vector4,new S.Vector4],r=new S.Vector4;this.groupGL.getWorldPosition(r),r.w=1,r.transformMat4(e.viewMatrix).transformMat4(e.projectionMatrix),r.x/=r.w,r.y/=r.w,this._axes.forEach(function(i){var n=i.axisLineCoords;i.labelsMesh.geometry;for(var a=0;a<t.length;a++)t[a].setArray(n[a]),t[a].w=1,t[a].transformMat4(i.rootNode.worldTransform).transformMat4(e.viewMatrix).transformMat4(e.projectionMatrix),t[a].x/=t[a].w,t[a].y/=t[a].w;var o=t[1].x-t[0].x,s=t[1].y-t[0].y,l=(t[1].x+t[0].x)/2,u=(t[1].y+t[0].y)/2,h,f;Math.abs(s/o)<.5?(h="center",f=u>r.y?"bottom":"top"):(f="middle",h=l>r.x?"left":"right"),i.setSpriteAlign(h,f,this._api)},this)},_doShowAxisPointer:function(){this._axisPointerLineMesh.invisible&&(this._axisPointerLineMesh.invisible=!1,this._axisPointerLabelsMesh.invisible=!1,this._api.getZr().refresh())},_doHideAxisPointer:function(){this._axisPointerLineMesh.invisible||(this._axisPointerLineMesh.invisible=!0,this._axisPointerLabelsMesh.invisible=!0,this._api.getZr().refresh())},_updateAxisPointer:function(e){var t=this._model.coordinateSystem,r=t.dataToPoint(e),i=this._axisPointerLineMesh,n=i.geometry,a=this._model.getModel("axisPointer"),o=this._api.getDevicePixelRatio();n.convertToDynamicArray(!0);function s(A){return oe.firstNotNull(A.model.get("axisPointer.show"),a.get("show"))}function l(A){var C=A.model.getModel("axisPointer",a),D=C.getModel("lineStyle"),L=S.parseColor(D.get("color")),M=cu(D.get("width"),1),P=cu(D.get("opacity"),1);return L[3]*=P,{color:L,lineWidth:M}}for(var u=0;u<this._faces.length;u++){var h=this._faces[u];if(!h.rootNode.invisible){for(var f=h.faceInfo,d=f[3]<0?t.getAxis(f[2]).getExtentMin():t.getAxis(f[2]).getExtentMax(),c=Mr[f[2]],v=0;v<2;v++){var p=f[v],_=f[1-v],m=t.getAxis(p),g=t.getAxis(_);if(s(m)){var y=[0,0,0],x=[0,0,0],w=Mr[p],T=Mr[_];y[w]=x[w]=r[w],y[c]=x[c]=d,y[T]=g.getExtentMin(),x[T]=g.getExtentMax();var b=l(m);n.addLine(y,x,b.color,b.lineWidth*o)}}if(s(t.getAxis(f[2]))){var y=r.slice(),x=r.slice();x[c]=d;var b=l(t.getAxis(f[2]));n.addLine(y,x,b.color,b.lineWidth*o)}}}n.convertToTypedArray(),this._updateAxisPointerLabelsMesh(e),this._api.getZr().refresh()},_updateAxisPointerLabelsMesh:function(e){var t=this._model,r=this._axisPointerLabelsMesh,i=this._axisPointerLabelsSurface,n=t.coordinateSystem,a=t.getModel("axisPointer");r.geometry.convertToDynamicArray(!0),i.clear();var o={x:"y",y:"x",z:"y"};this._axes.forEach(function(s,l){var u=n.getAxis(s.dim),h=u.model,f=h.getModel("axisPointer",a),d=f.getModel("label"),c=f.get("lineStyle.color");if(!(!d.get("show")||!f.get("show"))){var v=e[l],p=d.get("formatter"),_=u.scale.getLabel({value:v});if(p!=null)_=p(_,e);else if(u.scale.type==="interval"||u.scale.type==="log"){var m=nh(u.scale.getTicks()[0]);_=v.toFixed(m+2)}var g=d.get("color"),y=new gr({style:$n(d,{text:_,fill:g||c,align:"left",verticalAlign:"top"})}),x=i.add(y),w=y.getBoundingRect(),T=this._api.getDevicePixelRatio(),b=s.rootNode.position.toArray(),A=Mr[o[s.dim]];b[A]+=(s.flipped?-1:1)*d.get("margin"),b[Mr[s.dim]]=u.dataToCoord(e[l]),r.geometry.addSprite(b,[w.width*T,w.height*T],x,s.textAlign,s.textVerticalAlign)}},this),i.getZr().refreshImmediately(),r.material.set("uvScale",i.getCoordsScale()),r.geometry.convertToTypedArray()},dispose:function(){this.groupGL.removeAll(),this._control.dispose(),this._axisLabelSurface.dispose(),this._axisPointerLabelsSurface.dispose()}});function en(e){Ko.call(this,e),this.type="cartesian3D",this.dimensions=["x","y","z"],this.size=[0,0,0]}en.prototype={constructor:en,model:null,containPoint:function(e){return this.getAxis("x").contain(e[0])&&this.getAxis("y").contain(e[2])&&this.getAxis("z").contain(e[1])},containData:function(e){return this.getAxis("x").containData(e[0])&&this.getAxis("y").containData(e[1])&&this.getAxis("z").containData(e[2])},dataToPoint:function(e,t,r){return t=t||[],t[0]=this.getAxis("x").dataToCoord(e[0],r),t[2]=this.getAxis("y").dataToCoord(e[1],r),t[1]=this.getAxis("z").dataToCoord(e[2],r),t},pointToData:function(e,t,r){return t=t||[],t[0]=this.getAxis("x").coordToData(e[0],r),t[1]=this.getAxis("y").coordToData(e[2],r),t[2]=this.getAxis("z").coordToData(e[1],r),t}};ah(en,Ko);function ra(e,t,r){Si.call(this,e,t,r)}ra.prototype={constructor:ra,getExtentMin:function(){var e=this._extent;return Math.min(e[0],e[1])},getExtentMax:function(){var e=this._extent;return Math.max(e[0],e[1])},calculateCategoryInterval:function(){return Math.floor(this.scale.count()/8)}};ah(ra,Si);var ia=function(){this._pool={},this._allocatedTextures=[]};ia.prototype={constructor:ia,get:function(e){var t=du(e);this._pool.hasOwnProperty(t)||(this._pool[t]=[]);var r=this._pool[t];if(!r.length){var i=new ne(e);return this._allocatedTextures.push(i),i}return r.pop()},put:function(e){var t=du(e);this._pool.hasOwnProperty(t)||(this._pool[t]=[]);var r=this._pool[t];r.push(e)},clear:function(e){for(var t=0;t<this._allocatedTextures.length;t++)this._allocatedTextures[t].dispose(e);this._pool={},this._allocatedTextures=[]}};var rf={width:512,height:512,type:F.UNSIGNED_BYTE,format:F.RGBA,wrapS:F.CLAMP_TO_EDGE,wrapT:F.CLAMP_TO_EDGE,minFilter:F.LINEAR_MIPMAP_LINEAR,magFilter:F.LINEAR,useMipmap:!0,anisotropic:1,flipY:!0,unpackAlignment:4,premultiplyAlpha:!1},to=Object.keys(rf);function du(e){Pe.defaultsWithPropList(e,rf,to),km(e);for(var t="",r=0;r<to.length;r++){var i=to[r],n=e[i].toString();t+=n}return t}function km(e){var t=Wm(e.width,e.height);e.format===F.DEPTH_COMPONENT&&(e.useMipmap=!1),(!t||!e.useMipmap)&&(e.minFilter==F.NEAREST_MIPMAP_NEAREST||e.minFilter==F.NEAREST_MIPMAP_LINEAR?e.minFilter=F.NEAREST:(e.minFilter==F.LINEAR_MIPMAP_LINEAR||e.minFilter==F.LINEAR_MIPMAP_NEAREST)&&(e.minFilter=F.LINEAR)),t||(e.wrapS=F.CLAMP_TO_EDGE,e.wrapT=F.CLAMP_TO_EDGE)}function Wm(e,t){return(e&e-1)===0&&(t&t-1)===0}const Xm=`@export clay.sm.depth.vertex
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
attribute vec3 position : POSITION;
attribute vec2 texcoord : TEXCOORD_0;
uniform vec2 uvRepeat = vec2(1.0, 1.0);
uniform vec2 uvOffset = vec2(0.0, 0.0);
@import clay.chunk.skinning_header
@import clay.chunk.instancing_header
varying vec4 v_ViewPosition;
varying vec2 v_Texcoord;
void main(){
 vec4 P = vec4(position, 1.0);
#ifdef SKINNING
 @import clay.chunk.skin_matrix
 P = skinMatrixWS * P;
#endif
#ifdef INSTANCING
 @import clay.chunk.instancing_matrix
 P = instanceMat * P;
#endif
 v_ViewPosition = worldViewProjection * P;
 gl_Position = v_ViewPosition;
 v_Texcoord = texcoord * uvRepeat + uvOffset;
}
@end
@export clay.sm.depth.fragment
varying vec4 v_ViewPosition;
varying vec2 v_Texcoord;
uniform float bias : 0.001;
uniform float slopeScale : 1.0;
uniform sampler2D alphaMap;
uniform float alphaCutoff: 0.0;
@import clay.util.encode_float
void main(){
 float depth = v_ViewPosition.z / v_ViewPosition.w;
 if (alphaCutoff > 0.0) {
 if (texture2D(alphaMap, v_Texcoord).a <= alphaCutoff) {
 discard;
 }
 }
#ifdef USE_VSM
 depth = depth * 0.5 + 0.5;
 float moment1 = depth;
 float moment2 = depth * depth;
 #ifdef SUPPORT_STANDARD_DERIVATIVES
 float dx = dFdx(depth);
 float dy = dFdy(depth);
 moment2 += 0.25*(dx*dx+dy*dy);
 #endif
 gl_FragColor = vec4(moment1, moment2, 0.0, 1.0);
#else
 #ifdef SUPPORT_STANDARD_DERIVATIVES
 float dx = dFdx(depth);
 float dy = dFdy(depth);
 depth += sqrt(dx*dx + dy*dy) * slopeScale + bias;
 #else
 depth += bias;
 #endif
 gl_FragColor = encodeFloat(depth * 0.5 + 0.5);
#endif
}
@end
@export clay.sm.debug_depth
uniform sampler2D depthMap;
varying vec2 v_Texcoord;
@import clay.util.decode_float
void main() {
 vec4 tex = texture2D(depthMap, v_Texcoord);
#ifdef USE_VSM
 gl_FragColor = vec4(tex.rgb, 1.0);
#else
 float depth = decodeFloat(tex);
 gl_FragColor = vec4(depth, depth, depth, 1.0);
#endif
}
@end
@export clay.sm.distance.vertex
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform mat4 world : WORLD;
attribute vec3 position : POSITION;
@import clay.chunk.skinning_header
varying vec3 v_WorldPosition;
void main (){
 vec4 P = vec4(position, 1.0);
#ifdef SKINNING
 @import clay.chunk.skin_matrix
 P = skinMatrixWS * P;
#endif
#ifdef INSTANCING
 @import clay.chunk.instancing_matrix
 P = instanceMat * P;
#endif
 gl_Position = worldViewProjection * P;
 v_WorldPosition = (world * P).xyz;
}
@end
@export clay.sm.distance.fragment
uniform vec3 lightPosition;
uniform float range : 100;
varying vec3 v_WorldPosition;
@import clay.util.encode_float
void main(){
 float dist = distance(lightPosition, v_WorldPosition);
#ifdef USE_VSM
 gl_FragColor = vec4(dist, dist * dist, 0.0, 0.0);
#else
 dist = dist / range;
 gl_FragColor = encodeFloat(dist);
#endif
}
@end
@export clay.plugin.shadow_map_common
@import clay.util.decode_float
float tapShadowMap(sampler2D map, vec2 uv, float z){
 vec4 tex = texture2D(map, uv);
 return step(z, decodeFloat(tex) * 2.0 - 1.0);
}
float pcf(sampler2D map, vec2 uv, float z, float textureSize, vec2 scale) {
 float shadowContrib = tapShadowMap(map, uv, z);
 vec2 offset = vec2(1.0 / textureSize) * scale;
#ifdef PCF_KERNEL_SIZE
 for (int _idx_ = 0; _idx_ < PCF_KERNEL_SIZE; _idx_++) {{
 shadowContrib += tapShadowMap(map, uv + offset * pcfKernel[_idx_], z);
 }}
 return shadowContrib / float(PCF_KERNEL_SIZE + 1);
#else
 shadowContrib += tapShadowMap(map, uv+vec2(offset.x, 0.0), z);
 shadowContrib += tapShadowMap(map, uv+vec2(offset.x, offset.y), z);
 shadowContrib += tapShadowMap(map, uv+vec2(-offset.x, offset.y), z);
 shadowContrib += tapShadowMap(map, uv+vec2(0.0, offset.y), z);
 shadowContrib += tapShadowMap(map, uv+vec2(-offset.x, 0.0), z);
 shadowContrib += tapShadowMap(map, uv+vec2(-offset.x, -offset.y), z);
 shadowContrib += tapShadowMap(map, uv+vec2(offset.x, -offset.y), z);
 shadowContrib += tapShadowMap(map, uv+vec2(0.0, -offset.y), z);
 return shadowContrib / 9.0;
#endif
}
float pcf(sampler2D map, vec2 uv, float z, float textureSize) {
 return pcf(map, uv, z, textureSize, vec2(1.0));
}
float chebyshevUpperBound(vec2 moments, float z){
 float p = 0.0;
 z = z * 0.5 + 0.5;
 if (z <= moments.x) {
 p = 1.0;
 }
 float variance = moments.y - moments.x * moments.x;
 variance = max(variance, 0.0000001);
 float mD = moments.x - z;
 float pMax = variance / (variance + mD * mD);
 pMax = clamp((pMax-0.4)/(1.0-0.4), 0.0, 1.0);
 return max(p, pMax);
}
float computeShadowContrib(
 sampler2D map, mat4 lightVPM, vec3 position, float textureSize, vec2 scale, vec2 offset
) {
 vec4 posInLightSpace = lightVPM * vec4(position, 1.0);
 posInLightSpace.xyz /= posInLightSpace.w;
 float z = posInLightSpace.z;
 if(all(greaterThan(posInLightSpace.xyz, vec3(-0.99, -0.99, -1.0))) &&
 all(lessThan(posInLightSpace.xyz, vec3(0.99, 0.99, 1.0)))){
 vec2 uv = (posInLightSpace.xy+1.0) / 2.0;
 #ifdef USE_VSM
 vec2 moments = texture2D(map, uv * scale + offset).xy;
 return chebyshevUpperBound(moments, z);
 #else
 return pcf(map, uv * scale + offset, z, textureSize, scale);
 #endif
 }
 return 1.0;
}
float computeShadowContrib(sampler2D map, mat4 lightVPM, vec3 position, float textureSize) {
 return computeShadowContrib(map, lightVPM, position, textureSize, vec2(1.0), vec2(0.0));
}
float computeShadowContribOmni(samplerCube map, vec3 direction, float range)
{
 float dist = length(direction);
 vec4 shadowTex = textureCube(map, direction);
#ifdef USE_VSM
 vec2 moments = shadowTex.xy;
 float variance = moments.y - moments.x * moments.x;
 float mD = moments.x - dist;
 float p = variance / (variance + mD * mD);
 if(moments.x + 0.001 < dist){
 return clamp(p, 0.0, 1.0);
 }else{
 return 1.0;
 }
#else
 return step(dist, (decodeFloat(shadowTex) + 0.0002) * range);
#endif
}
@end
@export clay.plugin.compute_shadow_map
#if defined(SPOT_LIGHT_SHADOWMAP_COUNT) || defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT) || defined(POINT_LIGHT_SHADOWMAP_COUNT)
#ifdef SPOT_LIGHT_SHADOWMAP_COUNT
uniform sampler2D spotLightShadowMaps[SPOT_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
uniform mat4 spotLightMatrices[SPOT_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
uniform float spotLightShadowMapSizes[SPOT_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
#endif
#ifdef DIRECTIONAL_LIGHT_SHADOWMAP_COUNT
#if defined(SHADOW_CASCADE)
uniform sampler2D directionalLightShadowMaps[1]:unconfigurable;
uniform mat4 directionalLightMatrices[SHADOW_CASCADE]:unconfigurable;
uniform float directionalLightShadowMapSizes[1]:unconfigurable;
uniform float shadowCascadeClipsNear[SHADOW_CASCADE]:unconfigurable;
uniform float shadowCascadeClipsFar[SHADOW_CASCADE]:unconfigurable;
#else
uniform sampler2D directionalLightShadowMaps[DIRECTIONAL_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
uniform mat4 directionalLightMatrices[DIRECTIONAL_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
uniform float directionalLightShadowMapSizes[DIRECTIONAL_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
#endif
#endif
#ifdef POINT_LIGHT_SHADOWMAP_COUNT
uniform samplerCube pointLightShadowMaps[POINT_LIGHT_SHADOWMAP_COUNT]:unconfigurable;
#endif
uniform bool shadowEnabled : true;
#ifdef PCF_KERNEL_SIZE
uniform vec2 pcfKernel[PCF_KERNEL_SIZE];
#endif
@import clay.plugin.shadow_map_common
#if defined(SPOT_LIGHT_SHADOWMAP_COUNT)
void computeShadowOfSpotLights(vec3 position, inout float shadowContribs[SPOT_LIGHT_COUNT] ) {
 float shadowContrib;
 for(int _idx_ = 0; _idx_ < SPOT_LIGHT_SHADOWMAP_COUNT; _idx_++) {{
 shadowContrib = computeShadowContrib(
 spotLightShadowMaps[_idx_], spotLightMatrices[_idx_], position,
 spotLightShadowMapSizes[_idx_]
 );
 shadowContribs[_idx_] = shadowContrib;
 }}
 for(int _idx_ = SPOT_LIGHT_SHADOWMAP_COUNT; _idx_ < SPOT_LIGHT_COUNT; _idx_++){{
 shadowContribs[_idx_] = 1.0;
 }}
}
#endif
#if defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
#ifdef SHADOW_CASCADE
void computeShadowOfDirectionalLights(vec3 position, inout float shadowContribs[DIRECTIONAL_LIGHT_COUNT]){
 float depth = (2.0 * gl_FragCoord.z - gl_DepthRange.near - gl_DepthRange.far)
 / (gl_DepthRange.far - gl_DepthRange.near);
 float shadowContrib;
 shadowContribs[0] = 1.0;
 for (int _idx_ = 0; _idx_ < SHADOW_CASCADE; _idx_++) {{
 if (
 depth >= shadowCascadeClipsNear[_idx_] &&
 depth <= shadowCascadeClipsFar[_idx_]
 ) {
 shadowContrib = computeShadowContrib(
 directionalLightShadowMaps[0], directionalLightMatrices[_idx_], position,
 directionalLightShadowMapSizes[0],
 vec2(1.0 / float(SHADOW_CASCADE), 1.0),
 vec2(float(_idx_) / float(SHADOW_CASCADE), 0.0)
 );
 shadowContribs[0] = shadowContrib;
 }
 }}
 for(int _idx_ = DIRECTIONAL_LIGHT_SHADOWMAP_COUNT; _idx_ < DIRECTIONAL_LIGHT_COUNT; _idx_++) {{
 shadowContribs[_idx_] = 1.0;
 }}
}
#else
void computeShadowOfDirectionalLights(vec3 position, inout float shadowContribs[DIRECTIONAL_LIGHT_COUNT]){
 float shadowContrib;
 for(int _idx_ = 0; _idx_ < DIRECTIONAL_LIGHT_SHADOWMAP_COUNT; _idx_++) {{
 shadowContrib = computeShadowContrib(
 directionalLightShadowMaps[_idx_], directionalLightMatrices[_idx_], position,
 directionalLightShadowMapSizes[_idx_]
 );
 shadowContribs[_idx_] = shadowContrib;
 }}
 for(int _idx_ = DIRECTIONAL_LIGHT_SHADOWMAP_COUNT; _idx_ < DIRECTIONAL_LIGHT_COUNT; _idx_++) {{
 shadowContribs[_idx_] = 1.0;
 }}
}
#endif
#endif
#if defined(POINT_LIGHT_SHADOWMAP_COUNT)
void computeShadowOfPointLights(vec3 position, inout float shadowContribs[POINT_LIGHT_COUNT] ){
 vec3 lightPosition;
 vec3 direction;
 for(int _idx_ = 0; _idx_ < POINT_LIGHT_SHADOWMAP_COUNT; _idx_++) {{
 lightPosition = pointLightPosition[_idx_];
 direction = position - lightPosition;
 shadowContribs[_idx_] = computeShadowContribOmni(pointLightShadowMaps[_idx_], direction, pointLightRange[_idx_]);
 }}
 for(int _idx_ = POINT_LIGHT_SHADOWMAP_COUNT; _idx_ < POINT_LIGHT_COUNT; _idx_++) {{
 shadowContribs[_idx_] = 1.0;
 }}
}
#endif
#endif
@end`;var ur=["px","nx","py","ny","pz","nz"];k.import(Xm);function ro(e,t,r){if(r==="alphaMap")return e.material.get("diffuseMap");if(r==="alphaCutoff"){if(e.material.isDefined("fragment","ALPHA_TEST")&&e.material.get("diffuseMap")){var i=e.material.get("alphaCutoff");return i||0}return 0}else return r==="uvRepeat"?e.material.get("uvRepeat"):r==="uvOffset"?e.material.get("uvOffset"):t.get(r)}function vu(e,t){var r=e.material,i=t.material;return r.get("diffuseMap")!==i.get("diffuseMap")||(r.get("alphaCutoff")||0)!==(i.get("alphaCutoff")||0)}var zt=Qe.extend(function(){return{softShadow:zt.PCF,shadowBlur:1,lightFrustumBias:"auto",kernelPCF:new Float32Array([1,0,1,1,-1,1,0,1,-1,0,-1,-1,1,-1,0,-1]),precision:"highp",_lastRenderNotCastShadow:!1,_frameBuffer:new Ie,_textures:{},_shadowMapNumber:{POINT_LIGHT:0,DIRECTIONAL_LIGHT:0,SPOT_LIGHT:0},_depthMaterials:{},_distanceMaterials:{},_receivers:[],_lightsCastShadow:[],_lightCameras:{},_lightMaterials:{},_texturePool:new ia}},function(){this._gaussianPassH=new Oe({fragment:k.source("clay.compositor.gaussian_blur")}),this._gaussianPassV=new Oe({fragment:k.source("clay.compositor.gaussian_blur")}),this._gaussianPassH.setUniform("blurSize",this.shadowBlur),this._gaussianPassH.setUniform("blurDir",0),this._gaussianPassV.setUniform("blurSize",this.shadowBlur),this._gaussianPassV.setUniform("blurDir",1),this._outputDepthPass=new Oe({fragment:k.source("clay.sm.debug_depth")})},{render:function(e,t,r,i){r||(r=t.getMainCamera()),this.trigger("beforerender",this,e,t,r),this._renderShadowPass(e,t,r,i),this.trigger("afterrender",this,e,t,r)},renderDebug:function(e,t){e.saveClear();var r=e.viewport,i=0,n=0,a=t||r.width/4,o=a;this.softShadow===zt.VSM?this._outputDepthPass.material.define("fragment","USE_VSM"):this._outputDepthPass.material.undefine("fragment","USE_VSM");for(var s in this._textures){var l=this._textures[s];e.setViewport(i,n,a*l.width/l.height,o),this._outputDepthPass.setUniform("depthMap",l),this._outputDepthPass.render(e),i+=a*l.width/l.height}e.setViewport(r),e.restoreClear()},_updateReceivers:function(e,t){if(t.receiveShadow?(this._receivers.push(t),t.material.set("shadowEnabled",1),t.material.set("pcfKernel",this.kernelPCF)):t.material.set("shadowEnabled",0),this.softShadow===zt.VSM)t.material.define("fragment","USE_VSM"),t.material.undefine("fragment","PCF_KERNEL_SIZE");else{t.material.undefine("fragment","USE_VSM");var r=this.kernelPCF;r&&r.length?t.material.define("fragment","PCF_KERNEL_SIZE",r.length/2):t.material.undefine("fragment","PCF_KERNEL_SIZE")}},_update:function(e,t){var r=this;t.traverse(function(a){a.isRenderable()&&r._updateReceivers(e,a)});for(var i=0;i<t.lights.length;i++){var n=t.lights[i];n.castShadow&&!n.invisible&&this._lightsCastShadow.push(n)}},_renderShadowPass:function(e,t,r,i){for(var n in this._shadowMapNumber)this._shadowMapNumber[n]=0;this._lightsCastShadow.length=0,this._receivers.length=0;var a=e.gl;if(i||t.update(),r&&r.update(),t.updateLights(),this._update(e,t),!this._lightsCastShadow.length&&this._lastRenderNotCastShadow)return;this._lastRenderNotCastShadow=this._lightsCastShadow===0,a.enable(a.DEPTH_TEST),a.depthMask(!0),a.disable(a.BLEND),a.clearColor(1,1,1,1);for(var o=[],s=[],l=[],u=[],h=[],f=[],d,c=0;c<this._lightsCastShadow.length;c++){var v=this._lightsCastShadow[c];if(v.type==="DIRECTIONAL_LIGHT"){if(d){console.warn("Only one direectional light supported with shadow cascade");continue}if(v.shadowCascade>4){console.warn("Support at most 4 cascade");continue}v.shadowCascade>1&&(d=v),this.renderDirectionalLightShadow(e,t,r,v,h,u,l)}else v.type==="SPOT_LIGHT"?this.renderSpotLightShadow(e,t,v,s,o):v.type==="POINT_LIGHT"&&this.renderPointLightShadow(e,t,v,f);this._shadowMapNumber[v.type]++}for(var p in this._shadowMapNumber)for(var _=this._shadowMapNumber[p],m=p+"_SHADOWMAP_COUNT",c=0;c<this._receivers.length;c++){var g=this._receivers[c],y=g.material;y.fragmentDefines[m]!==_&&(_>0?y.define("fragment",m,_):y.isDefined("fragment",m)&&y.undefine("fragment",m))}for(var c=0;c<this._receivers.length;c++){var g=this._receivers[c],y=g.material;d?y.define("fragment","SHADOW_CASCADE",d.shadowCascade):y.undefine("fragment","SHADOW_CASCADE")}var x=t.shadowUniforms;function w(D){return D.height}if(l.length>0){var T=l.map(w);if(x.directionalLightShadowMaps={value:l,type:"tv"},x.directionalLightMatrices={value:u,type:"m4v"},x.directionalLightShadowMapSizes={value:T,type:"1fv"},d){var b=h.slice(),A=h.slice();b.pop(),A.shift(),b.reverse(),A.reverse(),u.reverse(),x.shadowCascadeClipsNear={value:b,type:"1fv"},x.shadowCascadeClipsFar={value:A,type:"1fv"}}}if(o.length>0){var C=o.map(w),x=t.shadowUniforms;x.spotLightShadowMaps={value:o,type:"tv"},x.spotLightMatrices={value:s,type:"m4v"},x.spotLightShadowMapSizes={value:C,type:"1fv"}}f.length>0&&(x.pointLightShadowMaps={value:f,type:"tv"})},renderDirectionalLightShadow:function(){var e=new da,t=new W,r=new Je,i=new W,n=new W,a=new W,o=new W;return function(s,l,u,h,f,d,c){var v=this._getDepthMaterial(h),p={getMaterial:function(ie){return ie.shadowDepthMaterial||v},isMaterialChanged:vu,getUniform:ro,ifRender:function(ie){return ie.castShadow},sortCompare:Et.opaqueSortCompare};if(!l.viewBoundingBoxLastFrame.isFinite()){var _=l.getBoundingBox();l.viewBoundingBoxLastFrame.copy(_).applyTransform(u.viewMatrix)}var m=Math.min(-l.viewBoundingBoxLastFrame.min.z,u.far),g=Math.max(-l.viewBoundingBoxLastFrame.max.z,u.near),y=this._getDirectionalLightCamera(h,l,u),x=a.array;o.copy(y.projectionMatrix),z.invert(n.array,y.worldTransform.array),z.multiply(n.array,n.array,u.worldTransform.array),z.multiply(x,o.array,n.array);for(var w=[],T=u instanceof We,b=(u.near+u.far)/(u.near-u.far),A=2*u.near*u.far/(u.near-u.far),C=0;C<=h.shadowCascade;C++){var D=g*Math.pow(m/g,C/h.shadowCascade),L=g+(m-g)*C/h.shadowCascade,M=D*h.cascadeSplitLogFactor+L*(1-h.cascadeSplitLogFactor);w.push(M),f.push(-(-M*b+A)/-M)}var P=this._getTexture(h,h.shadowCascade);c.push(P);var N=s.viewport,I=s.gl;this._frameBuffer.attach(P),this._frameBuffer.bind(s),I.clear(I.COLOR_BUFFER_BIT|I.DEPTH_BUFFER_BIT);for(var C=0;C<h.shadowCascade;C++){var V=w[C],Z=w[C+1];T?z.perspective(t.array,u.fov/180*Math.PI,u.aspect,V,Z):z.ortho(t.array,u.left,u.right,u.bottom,u.top,V,Z),e.setFromProjection(t),e.getTransformedBoundingBox(r,n),r.applyProjection(o);var B=r.min.array,$=r.max.array;B[0]=Math.max(B[0],-1),B[1]=Math.max(B[1],-1),$[0]=Math.min($[0],1),$[1]=Math.min($[1],1),i.ortho(B[0],$[0],B[1],$[1],1,-1),y.projectionMatrix.multiplyLeft(i);var q=h.shadowResolution||512;s.setViewport((h.shadowCascade-C-1)*q,0,q,q,1);var j=l.updateRenderList(y);s.renderPass(j.opaque,y,p),this.softShadow===zt.VSM&&this._gaussianFilter(s,P,P.width);var Q=new W;Q.copy(y.viewMatrix).multiplyLeft(y.projectionMatrix),d.push(Q.array),y.projectionMatrix.copy(o)}this._frameBuffer.unbind(s),s.setViewport(N)}}(),renderSpotLightShadow:function(e,t,r,i,n){var a=this._getTexture(r),o=this._getSpotLightCamera(r),s=e.gl;this._frameBuffer.attach(a),this._frameBuffer.bind(e),s.clear(s.COLOR_BUFFER_BIT|s.DEPTH_BUFFER_BIT);var l=this._getDepthMaterial(r),u={getMaterial:function(d){return d.shadowDepthMaterial||l},isMaterialChanged:vu,getUniform:ro,ifRender:function(d){return d.castShadow},sortCompare:Et.opaqueSortCompare},h=t.updateRenderList(o);e.renderPass(h.opaque,o,u),this._frameBuffer.unbind(e),this.softShadow===zt.VSM&&this._gaussianFilter(e,a,a.width);var f=new W;f.copy(o.worldTransform).invert().multiplyLeft(o.projectionMatrix),n.push(a),i.push(f.array)},renderPointLightShadow:function(e,t,r,i){var n=this._getTexture(r),a=e.gl;i.push(n);var o=this._getDepthMaterial(r),s={getMaterial:function(g){return g.shadowDepthMaterial||o},getUniform:ro,sortCompare:Et.opaqueSortCompare},l={px:[],py:[],pz:[],nx:[],ny:[],nz:[]},u=new Je,h=r.getWorldPosition().array,f=new Je,d=r.range;f.min.setArray(h),f.max.setArray(h);var c=new R(d,d,d);f.max.add(c),f.min.sub(c);var v={px:!1,py:!1,pz:!1,nx:!1,ny:!1,nz:!1};t.traverse(function(g){if(g.isRenderable()&&g.castShadow){var y=g.geometry;if(!y.boundingBox){for(var x=0;x<ur.length;x++)l[ur[x]].push(g);return}if(u.transformFrom(y.boundingBox,g.worldTransform),!u.intersectBoundingBox(f))return;u.updateVertices();for(var x=0;x<ur.length;x++)v[ur[x]]=!1;for(var x=0;x<8;x++){var w=u.vertices[x],T=w[0]-h[0],b=w[1]-h[1],A=w[2]-h[2],C=Math.abs(T),D=Math.abs(b),L=Math.abs(A);C>D?C>L?v[T>0?"px":"nx"]=!0:v[A>0?"pz":"nz"]=!0:D>L?v[b>0?"py":"ny"]=!0:v[A>0?"pz":"nz"]=!0}for(var x=0;x<ur.length;x++)v[ur[x]]&&l[ur[x]].push(g)}});for(var p=0;p<6;p++){var _=ur[p],m=this._getPointLightCamera(r,_);this._frameBuffer.attach(n,a.COLOR_ATTACHMENT0,a.TEXTURE_CUBE_MAP_POSITIVE_X+p),this._frameBuffer.bind(e),a.clear(a.COLOR_BUFFER_BIT|a.DEPTH_BUFFER_BIT),e.renderPass(l[_],m,s)}this._frameBuffer.unbind(e)},_getDepthMaterial:function(e){var t=this._lightMaterials[e.__uid__],r=e.type==="POINT_LIGHT";if(!t){var i=r?"clay.sm.distance.":"clay.sm.depth.";t=new At({precision:this.precision,shader:new k(k.source(i+"vertex"),k.source(i+"fragment"))}),this._lightMaterials[e.__uid__]=t}return e.shadowSlopeScale!=null&&t.setUniform("slopeScale",e.shadowSlopeScale),e.shadowBias!=null&&t.setUniform("bias",e.shadowBias),this.softShadow===zt.VSM?t.define("fragment","USE_VSM"):t.undefine("fragment","USE_VSM"),r&&(t.set("lightPosition",e.getWorldPosition().array),t.set("range",e.range)),t},_gaussianFilter:function(e,t,r){var i={width:r,height:r,type:H.FLOAT},n=this._texturePool.get(i);this._frameBuffer.attach(n),this._frameBuffer.bind(e),this._gaussianPassH.setUniform("texture",t),this._gaussianPassH.setUniform("textureWidth",r),this._gaussianPassH.render(e),this._frameBuffer.attach(t),this._gaussianPassV.setUniform("texture",n),this._gaussianPassV.setUniform("textureHeight",r),this._gaussianPassV.render(e),this._frameBuffer.unbind(e),this._texturePool.put(n)},_getTexture:function(e,t){var r=e.__uid__,i=this._textures[r],n=e.shadowResolution||512;return t=t||1,i||(e.type==="POINT_LIGHT"?i=new Vr:i=new ne,i.width=n*t,i.height=n,this.softShadow===zt.VSM?(i.type=H.FLOAT,i.anisotropic=4):(i.minFilter=F.NEAREST,i.magFilter=F.NEAREST,i.useMipmap=!1),this._textures[r]=i),i},_getPointLightCamera:function(e,t){this._lightCameras.point||(this._lightCameras.point={px:new We,nx:new We,py:new We,ny:new We,pz:new We,nz:new We});var r=this._lightCameras.point[t];switch(r.far=e.range,r.fov=90,r.position.set(0,0,0),t){case"px":r.lookAt(R.POSITIVE_X,R.NEGATIVE_Y);break;case"nx":r.lookAt(R.NEGATIVE_X,R.NEGATIVE_Y);break;case"py":r.lookAt(R.POSITIVE_Y,R.POSITIVE_Z);break;case"ny":r.lookAt(R.NEGATIVE_Y,R.NEGATIVE_Z);break;case"pz":r.lookAt(R.POSITIVE_Z,R.NEGATIVE_Y);break;case"nz":r.lookAt(R.NEGATIVE_Z,R.NEGATIVE_Y);break}return e.getWorldPosition(r.position),r.update(),r},_getDirectionalLightCamera:function(){var e=new W,t=new Je,r=new Je;return function(i,n,a){this._lightCameras.directional||(this._lightCameras.directional=new _i);var o=this._lightCameras.directional;t.copy(n.viewBoundingBoxLastFrame),t.intersection(a.frustum.boundingBox),o.position.copy(t.min).add(t.max).scale(.5).transformMat4(a.worldTransform),o.rotation.copy(i.rotation),o.scale.copy(i.scale),o.updateWorldTransform(),W.invert(e,o.worldTransform),W.multiply(e,e,a.worldTransform),r.copy(t).applyTransform(e);var s=r.min.array,l=r.max.array;return o.position.set((s[0]+l[0])/2,(s[1]+l[1])/2,l[2]).transformMat4(o.worldTransform),o.near=0,o.far=-s[2]+l[2],isNaN(this.lightFrustumBias)?o.far*=4:o.far+=this.lightFrustumBias,o.left=s[0],o.right=l[0],o.top=l[1],o.bottom=s[1],o.update(!0),o}}(),_getSpotLightCamera:function(e){this._lightCameras.spot||(this._lightCameras.spot=new We);var t=this._lightCameras.spot;return t.fov=e.penumbraAngle*2,t.far=e.range,t.worldTransform.copy(e.worldTransform),t.updateProjectionMatrix(),z.invert(t.viewMatrix.array,t.worldTransform.array),t},dispose:function(e){var t=e.gl||e;this._frameBuffer&&this._frameBuffer.dispose(t);for(var r in this._textures)this._textures[r].dispose(t);this._texturePool.clear(e.gl),this._depthMaterials={},this._distanceMaterials={},this._textures={},this._lightCameras={},this._shadowMapNumber={POINT_LIGHT:0,DIRECTIONAL_LIGHT:0,SPOT_LIGHT:0},this._meshMaterials={};for(var i=0;i<this._receivers.length;i++){var n=this._receivers[i];if(n.material){var a=n.material;a.undefine("fragment","POINT_LIGHT_SHADOW_COUNT"),a.undefine("fragment","DIRECTIONAL_LIGHT_SHADOW_COUNT"),a.undefine("fragment","AMBIENT_LIGHT_SHADOW_COUNT"),a.set("shadowEnabled",0)}}this._receivers=[],this._lightsCastShadow=[]}});zt.VSM=1;zt.PCF=2;var tn=Qe.extend(function(){return{name:"",inputLinks:{},outputLinks:{},_prevOutputTextures:{},_outputTextures:{},_outputReferences:{},_rendering:!1,_rendered:!1,_compositor:null}},{updateParameter:function(e,t){var r=this.outputs[e],i=r.parameters,n=r._parametersCopy;if(n||(n=r._parametersCopy={}),i)for(var a in i)a!=="width"&&a!=="height"&&(n[a]=i[a]);var o,s;return i.width instanceof Function?o=i.width.call(this,t):o=i.width,i.height instanceof Function?s=i.height.call(this,t):s=i.height,(n.width!==o||n.height!==s)&&this._outputTextures[e]&&this._outputTextures[e].dispose(t.gl),n.width=o,n.height=s,n},setParameter:function(e,t){},getParameter:function(e){},setParameters:function(e){for(var t in e)this.setParameter(t,e[t])},render:function(){},getOutput:function(e,t){if(t==null)return t=e,this._outputTextures[t];var r=this.outputs[t];if(r)return this._rendered?r.outputLastFrame?this._prevOutputTextures[t]:this._outputTextures[t]:this._rendering?(this._prevOutputTextures[t]||(this._prevOutputTextures[t]=this._compositor.allocateTexture(r.parameters||{})),this._prevOutputTextures[t]):(this.render(e),this._outputTextures[t])},removeReference:function(e){if(this._outputReferences[e]--,this._outputReferences[e]===0){var t=this.outputs[e];t.keepLastFrame?(this._prevOutputTextures[e]&&this._compositor.releaseTexture(this._prevOutputTextures[e]),this._prevOutputTextures[e]=this._outputTextures[e]):this._compositor.releaseTexture(this._outputTextures[e])}},link:function(e,t,r){this.inputLinks[e]={node:t,pin:r},t.outputLinks[r]||(t.outputLinks[r]=[]),t.outputLinks[r].push({node:this,pin:e}),this.pass.material.enableTexture(e)},clear:function(){this.inputLinks={},this.outputLinks={}},updateReference:function(e){if(!this._rendering){this._rendering=!0;for(var t in this.inputLinks){var r=this.inputLinks[t];r.node.updateReference(r.pin)}this._rendering=!1}e&&this._outputReferences[e]++},beforeFrame:function(){this._rendered=!1;for(var e in this.outputLinks)this._outputReferences[e]=0},afterFrame:function(){for(var e in this.outputLinks)if(this._outputReferences[e]>0){var t=this.outputs[e];t.keepLastFrame?(this._prevOutputTextures[e]&&this._compositor.releaseTexture(this._prevOutputTextures[e]),this._prevOutputTextures[e]=this._outputTextures[e]):this._compositor.releaseTexture(this._outputTextures[e])}}}),pu=Qe.extend(function(){return{nodes:[]}},{dirty:function(){this._dirty=!0},addNode:function(e){this.nodes.indexOf(e)>=0||(this.nodes.push(e),this._dirty=!0)},removeNode:function(e){typeof e=="string"&&(e=this.getNodeByName(e));var t=this.nodes.indexOf(e);t>=0&&(this.nodes.splice(t,1),this._dirty=!0)},getNodeByName:function(e){for(var t=0;t<this.nodes.length;t++)if(this.nodes[t].name===e)return this.nodes[t]},update:function(){for(var e=0;e<this.nodes.length;e++)this.nodes[e].clear();for(var e=0;e<this.nodes.length;e++){var t=this.nodes[e];if(t.inputs){for(var r in t.inputs)if(t.inputs[r]){if(t.pass&&!t.pass.material.isUniformEnabled(r)){console.warn("Pin "+t.name+"."+r+" not used.");continue}var i=t.inputs[r],n=this.findPin(i);n?t.link(r,n.node,n.pin):console.warn(typeof i=="string"?"Node "+i+" not exist":"Pin of "+i.node+"."+i.pin+" not exist")}}}},findPin:function(e){var t;if((typeof e=="string"||e instanceof tn)&&(e={node:e}),typeof e.node=="string")for(var r=0;r<this.nodes.length;r++){var i=this.nodes[r];i.name===e.node&&(t=i)}else t=e.node;if(t){var n=e.pin;if(n||t.outputs&&(n=Object.keys(t.outputs)[0]),t.outputs[n])return{node:t,pin:n}}}}),jm=pu.extend(function(){return{_outputs:[],_texturePool:new ia,_frameBuffer:new Ie({depthBuffer:!1})}},{addNode:function(e){pu.prototype.addNode.call(this,e),e._compositor=this},render:function(e,t){if(this._dirty){this.update(),this._dirty=!1,this._outputs.length=0;for(var r=0;r<this.nodes.length;r++)this.nodes[r].outputs||this._outputs.push(this.nodes[r])}for(var r=0;r<this.nodes.length;r++)this.nodes[r].beforeFrame();for(var r=0;r<this._outputs.length;r++)this._outputs[r].updateReference();for(var r=0;r<this._outputs.length;r++)this._outputs[r].render(e,t);for(var r=0;r<this.nodes.length;r++)this.nodes[r].afterFrame()},allocateTexture:function(e){return this._texturePool.get(e)},releaseTexture:function(e){this._texturePool.put(e)},getFrameBuffer:function(){return this._frameBuffer},dispose:function(e){this._texturePool.clear(e)}}),Zm=tn.extend({name:"scene",scene:null,camera:null,autoUpdateScene:!0,preZ:!1},function(){this.frameBuffer=new Ie},{render:function(e){this._rendering=!0;var t=e.gl;this.trigger("beforerender");var r;if(!this.outputs)r=e.render(this.scene,this.camera,!this.autoUpdateScene,this.preZ);else{var i=this.frameBuffer;for(var n in this.outputs){var a=this.updateParameter(n,e),o=this.outputs[n],s=this._compositor.allocateTexture(a);this._outputTextures[n]=s;var l=o.attachment||t.COLOR_ATTACHMENT0;typeof l=="string"&&(l=t[l]),i.attach(s,l)}i.bind(e);var u=e.getGLExtension("EXT_draw_buffers");if(u){var h=[];for(var l in this.outputs)l=parseInt(l),l>=t.COLOR_ATTACHMENT0&&l<=t.COLOR_ATTACHMENT0+8&&h.push(l);u.drawBuffersEXT(h)}e.saveClear(),e.clearBit=F.DEPTH_BUFFER_BIT|F.COLOR_BUFFER_BIT,r=e.render(this.scene,this.camera,!this.autoUpdateScene,this.preZ),e.restoreClear(),i.unbind(e)}this.trigger("afterrender",r),this._rendering=!1,this._rendered=!0}}),qm=tn.extend(function(){return{texture:null,outputs:{color:{}}}},function(){},{getOutput:function(e,t){return this.texture},beforeFrame:function(){},afterFrame:function(){}}),Ym=tn.extend(function(){return{name:"",inputs:{},outputs:null,shader:"",inputLinks:{},outputLinks:{},pass:null,_prevOutputTextures:{},_outputTextures:{},_outputReferences:{},_rendering:!1,_rendered:!1,_compositor:null}},function(){var e=new Oe({fragment:this.shader});this.pass=e},{render:function(e,t){this.trigger("beforerender",e),this._rendering=!0;var r=e.gl;for(var i in this.inputLinks){var n=this.inputLinks[i],a=n.node.getOutput(e,n.pin);this.pass.setUniform(i,a)}if(!this.outputs)this.pass.outputs=null,this._compositor.getFrameBuffer().unbind(e),this.pass.render(e,t);else{this.pass.outputs={};var o={};for(var s in this.outputs){var l=this.updateParameter(s,e);isNaN(l.width)&&this.updateParameter(s,e);var u=this.outputs[s],h=this._compositor.allocateTexture(l);this._outputTextures[s]=h;var f=u.attachment||r.COLOR_ATTACHMENT0;typeof f=="string"&&(f=r[f]),o[f]=h}this._compositor.getFrameBuffer().bind(e);for(var f in o)this._compositor.getFrameBuffer().attach(o[f],f);this.pass.render(e),this._compositor.getFrameBuffer().updateMipmap(e)}for(var i in this.inputLinks){var n=this.inputLinks[i];n.node.removeReference(n.pin)}this._rendering=!1,this._rendered=!0,this.trigger("afterrender",e)},updateParameter:function(e,t){var r=this.outputs[e],i=r.parameters,n=r._parametersCopy;if(n||(n=r._parametersCopy={}),i)for(var a in i)a!=="width"&&a!=="height"&&(n[a]=i[a]);var o,s;return typeof i.width=="function"?o=i.width.call(this,t):o=i.width,typeof i.height=="function"?s=i.height.call(this,t):s=i.height,o=Math.ceil(o),s=Math.ceil(s),(n.width!==o||n.height!==s)&&this._outputTextures[e]&&this._outputTextures[e].dispose(t),n.width=o,n.height=s,n},setParameter:function(e,t){this.pass.setUniform(e,t)},getParameter:function(e){return this.pass.getUniform(e)},setParameters:function(e){for(var t in e)this.setParameter(t,e[t])},define:function(e,t){this.pass.material.define("fragment",e,t)},undefine:function(e){this.pass.material.undefine("fragment",e)},removeReference:function(e){if(this._outputReferences[e]--,this._outputReferences[e]===0){var t=this.outputs[e];t.keepLastFrame?(this._prevOutputTextures[e]&&this._compositor.releaseTexture(this._prevOutputTextures[e]),this._prevOutputTextures[e]=this._outputTextures[e]):this._compositor.releaseTexture(this._outputTextures[e])}},clear:function(){tn.prototype.clear.call(this),this.pass.material.disableTexturesAll()}});const $m=`@export clay.compositor.coloradjust
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float brightness : 0.0;
uniform float contrast : 1.0;
uniform float exposure : 0.0;
uniform float gamma : 1.0;
uniform float saturation : 1.0;
const vec3 w = vec3(0.2125, 0.7154, 0.0721);
void main()
{
 vec4 tex = texture2D( texture, v_Texcoord);
 vec3 color = clamp(tex.rgb + vec3(brightness), 0.0, 1.0);
 color = clamp( (color-vec3(0.5))*contrast+vec3(0.5), 0.0, 1.0);
 color = clamp( color * pow(2.0, exposure), 0.0, 1.0);
 color = clamp( pow(color, vec3(gamma)), 0.0, 1.0);
 float luminance = dot( color, w );
 color = mix(vec3(luminance), color, saturation);
 gl_FragColor = vec4(color, tex.a);
}
@end
@export clay.compositor.brightness
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float brightness : 0.0;
void main()
{
 vec4 tex = texture2D( texture, v_Texcoord);
 vec3 color = tex.rgb + vec3(brightness);
 gl_FragColor = vec4(color, tex.a);
}
@end
@export clay.compositor.contrast
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float contrast : 1.0;
void main()
{
 vec4 tex = texture2D( texture, v_Texcoord);
 vec3 color = (tex.rgb-vec3(0.5))*contrast+vec3(0.5);
 gl_FragColor = vec4(color, tex.a);
}
@end
@export clay.compositor.exposure
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float exposure : 0.0;
void main()
{
 vec4 tex = texture2D(texture, v_Texcoord);
 vec3 color = tex.rgb * pow(2.0, exposure);
 gl_FragColor = vec4(color, tex.a);
}
@end
@export clay.compositor.gamma
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float gamma : 1.0;
void main()
{
 vec4 tex = texture2D(texture, v_Texcoord);
 vec3 color = pow(tex.rgb, vec3(gamma));
 gl_FragColor = vec4(color, tex.a);
}
@end
@export clay.compositor.saturation
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float saturation : 1.0;
const vec3 w = vec3(0.2125, 0.7154, 0.0721);
void main()
{
 vec4 tex = texture2D(texture, v_Texcoord);
 vec3 color = tex.rgb;
 float luminance = dot(color, w);
 color = mix(vec3(luminance), color, saturation);
 gl_FragColor = vec4(color, tex.a);
}
@end`,nf=`@export clay.compositor.kernel.gaussian_9
float gaussianKernel[9];
gaussianKernel[0] = 0.07;
gaussianKernel[1] = 0.09;
gaussianKernel[2] = 0.12;
gaussianKernel[3] = 0.14;
gaussianKernel[4] = 0.16;
gaussianKernel[5] = 0.14;
gaussianKernel[6] = 0.12;
gaussianKernel[7] = 0.09;
gaussianKernel[8] = 0.07;
@end
@export clay.compositor.kernel.gaussian_13
float gaussianKernel[13];
gaussianKernel[0] = 0.02;
gaussianKernel[1] = 0.03;
gaussianKernel[2] = 0.06;
gaussianKernel[3] = 0.08;
gaussianKernel[4] = 0.11;
gaussianKernel[5] = 0.13;
gaussianKernel[6] = 0.14;
gaussianKernel[7] = 0.13;
gaussianKernel[8] = 0.11;
gaussianKernel[9] = 0.08;
gaussianKernel[10] = 0.06;
gaussianKernel[11] = 0.03;
gaussianKernel[12] = 0.02;
@end
@export clay.compositor.gaussian_blur
#define SHADER_NAME gaussian_blur
uniform sampler2D texture;varying vec2 v_Texcoord;
uniform float blurSize : 2.0;
uniform vec2 textureSize : [512.0, 512.0];
uniform float blurDir : 0.0;
@import clay.util.rgbm
@import clay.util.clamp_sample
void main (void)
{
 @import clay.compositor.kernel.gaussian_9
 vec2 off = blurSize / textureSize;
 off *= vec2(1.0 - blurDir, blurDir);
 vec4 sum = vec4(0.0);
 float weightAll = 0.0;
 for (int i = 0; i < 9; i++) {
 float w = gaussianKernel[i];
 vec4 texel = decodeHDR(clampSample(texture, v_Texcoord + float(i - 4) * off));
 sum += texel * w;
 weightAll += w;
 }
 gl_FragColor = encodeHDR(sum / max(weightAll, 0.01));
}
@end
`,Km=`@export clay.compositor.hdr.log_lum
varying vec2 v_Texcoord;
uniform sampler2D texture;
const vec3 w = vec3(0.2125, 0.7154, 0.0721);
@import clay.util.rgbm
void main()
{
 vec4 tex = decodeHDR(texture2D(texture, v_Texcoord));
 float luminance = dot(tex.rgb, w);
 luminance = log(luminance + 0.001);
 gl_FragColor = encodeHDR(vec4(vec3(luminance), 1.0));
}
@end
@export clay.compositor.hdr.lum_adaption
varying vec2 v_Texcoord;
uniform sampler2D adaptedLum;
uniform sampler2D currentLum;
uniform float frameTime : 0.02;
@import clay.util.rgbm
void main()
{
 float fAdaptedLum = decodeHDR(texture2D(adaptedLum, vec2(0.5, 0.5))).r;
 float fCurrentLum = exp(encodeHDR(texture2D(currentLum, vec2(0.5, 0.5))).r);
 fAdaptedLum += (fCurrentLum - fAdaptedLum) * (1.0 - pow(0.98, 30.0 * frameTime));
 gl_FragColor = encodeHDR(vec4(vec3(fAdaptedLum), 1.0));
}
@end
@export clay.compositor.lum
varying vec2 v_Texcoord;
uniform sampler2D texture;
const vec3 w = vec3(0.2125, 0.7154, 0.0721);
void main()
{
 vec4 tex = texture2D( texture, v_Texcoord );
 float luminance = dot(tex.rgb, w);
 gl_FragColor = vec4(vec3(luminance), 1.0);
}
@end`,af=`
@export clay.compositor.lut
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform sampler2D lookup;
void main()
{
 vec4 tex = texture2D(texture, v_Texcoord);
 float blueColor = tex.b * 63.0;
 vec2 quad1;
 quad1.y = floor(floor(blueColor) / 8.0);
 quad1.x = floor(blueColor) - (quad1.y * 8.0);
 vec2 quad2;
 quad2.y = floor(ceil(blueColor) / 8.0);
 quad2.x = ceil(blueColor) - (quad2.y * 8.0);
 vec2 texPos1;
 texPos1.x = (quad1.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * tex.r);
 texPos1.y = (quad1.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * tex.g);
 vec2 texPos2;
 texPos2.x = (quad2.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * tex.r);
 texPos2.y = (quad2.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * tex.g);
 vec4 newColor1 = texture2D(lookup, texPos1);
 vec4 newColor2 = texture2D(lookup, texPos2);
 vec4 newColor = mix(newColor1, newColor2, fract(blueColor));
 gl_FragColor = vec4(newColor.rgb, tex.w);
}
@end`,Jm=`@export clay.compositor.vignette
#define OUTPUT_ALPHA
varying vec2 v_Texcoord;
uniform sampler2D texture;
uniform float darkness: 1;
uniform float offset: 1;
@import clay.util.rgbm
void main()
{
 vec4 texel = decodeHDR(texture2D(texture, v_Texcoord));
 gl_FragColor.rgb = texel.rgb;
 vec2 uv = (v_Texcoord - vec2(0.5)) * vec2(offset);
 gl_FragColor = encodeHDR(vec4(mix(texel.rgb, vec3(1.0 - darkness), dot(uv, uv)), texel.a));
}
@end`,of=`@export clay.compositor.output
#define OUTPUT_ALPHA
varying vec2 v_Texcoord;
uniform sampler2D texture;
@import clay.util.rgbm
void main()
{
 vec4 tex = decodeHDR(texture2D(texture, v_Texcoord));
 gl_FragColor.rgb = tex.rgb;
#ifdef OUTPUT_ALPHA
 gl_FragColor.a = tex.a;
#else
 gl_FragColor.a = 1.0;
#endif
 gl_FragColor = encodeHDR(gl_FragColor);
#ifdef PREMULTIPLY_ALPHA
 gl_FragColor.rgb *= gl_FragColor.a;
#endif
}
@end`,sf=`@export clay.compositor.bright
uniform sampler2D texture;
uniform float threshold : 1;
uniform float scale : 1.0;
uniform vec2 textureSize: [512, 512];
varying vec2 v_Texcoord;
const vec3 lumWeight = vec3(0.2125, 0.7154, 0.0721);
@import clay.util.rgbm
vec4 median(vec4 a, vec4 b, vec4 c)
{
 return a + b + c - min(min(a, b), c) - max(max(a, b), c);
}
void main()
{
 vec4 texel = decodeHDR(texture2D(texture, v_Texcoord));
#ifdef ANTI_FLICKER
 vec3 d = 1.0 / textureSize.xyx * vec3(1.0, 1.0, 0.0);
 vec4 s1 = decodeHDR(texture2D(texture, v_Texcoord - d.xz));
 vec4 s2 = decodeHDR(texture2D(texture, v_Texcoord + d.xz));
 vec4 s3 = decodeHDR(texture2D(texture, v_Texcoord - d.zy));
 vec4 s4 = decodeHDR(texture2D(texture, v_Texcoord + d.zy));
 texel = median(median(texel, s1, s2), s3, s4);
#endif
 float lum = dot(texel.rgb , lumWeight);
 vec4 color;
 if (lum > threshold && texel.a > 0.0)
 {
 color = vec4(texel.rgb * scale, texel.a * scale);
 }
 else
 {
 color = vec4(0.0);
 }
 gl_FragColor = encodeHDR(color);
}
@end
`,lf=`@export clay.compositor.downsample
uniform sampler2D texture;
uniform vec2 textureSize : [512, 512];
varying vec2 v_Texcoord;
@import clay.util.rgbm
float brightness(vec3 c)
{
 return max(max(c.r, c.g), c.b);
}
@import clay.util.clamp_sample
void main()
{
 vec4 d = vec4(-1.0, -1.0, 1.0, 1.0) / textureSize.xyxy;
#ifdef ANTI_FLICKER
 vec3 s1 = decodeHDR(clampSample(texture, v_Texcoord + d.xy)).rgb;
 vec3 s2 = decodeHDR(clampSample(texture, v_Texcoord + d.zy)).rgb;
 vec3 s3 = decodeHDR(clampSample(texture, v_Texcoord + d.xw)).rgb;
 vec3 s4 = decodeHDR(clampSample(texture, v_Texcoord + d.zw)).rgb;
 float s1w = 1.0 / (brightness(s1) + 1.0);
 float s2w = 1.0 / (brightness(s2) + 1.0);
 float s3w = 1.0 / (brightness(s3) + 1.0);
 float s4w = 1.0 / (brightness(s4) + 1.0);
 float oneDivideSum = 1.0 / (s1w + s2w + s3w + s4w);
 vec4 color = vec4(
 (s1 * s1w + s2 * s2w + s3 * s3w + s4 * s4w) * oneDivideSum,
 1.0
 );
#else
 vec4 color = decodeHDR(clampSample(texture, v_Texcoord + d.xy));
 color += decodeHDR(clampSample(texture, v_Texcoord + d.zy));
 color += decodeHDR(clampSample(texture, v_Texcoord + d.xw));
 color += decodeHDR(clampSample(texture, v_Texcoord + d.zw));
 color *= 0.25;
#endif
 gl_FragColor = encodeHDR(color);
}
@end`,uf=`
@export clay.compositor.upsample
#define HIGH_QUALITY
uniform sampler2D texture;
uniform vec2 textureSize : [512, 512];
uniform float sampleScale: 0.5;
varying vec2 v_Texcoord;
@import clay.util.rgbm
@import clay.util.clamp_sample
void main()
{
#ifdef HIGH_QUALITY
 vec4 d = vec4(1.0, 1.0, -1.0, 0.0) / textureSize.xyxy * sampleScale;
 vec4 s;
 s = decodeHDR(clampSample(texture, v_Texcoord - d.xy));
 s += decodeHDR(clampSample(texture, v_Texcoord - d.wy)) * 2.0;
 s += decodeHDR(clampSample(texture, v_Texcoord - d.zy));
 s += decodeHDR(clampSample(texture, v_Texcoord + d.zw)) * 2.0;
 s += decodeHDR(clampSample(texture, v_Texcoord )) * 4.0;
 s += decodeHDR(clampSample(texture, v_Texcoord + d.xw)) * 2.0;
 s += decodeHDR(clampSample(texture, v_Texcoord + d.zy));
 s += decodeHDR(clampSample(texture, v_Texcoord + d.wy)) * 2.0;
 s += decodeHDR(clampSample(texture, v_Texcoord + d.xy));
 gl_FragColor = encodeHDR(s / 16.0);
#else
 vec4 d = vec4(-1.0, -1.0, +1.0, +1.0) / textureSize.xyxy;
 vec4 s;
 s = decodeHDR(clampSample(texture, v_Texcoord + d.xy));
 s += decodeHDR(clampSample(texture, v_Texcoord + d.zy));
 s += decodeHDR(clampSample(texture, v_Texcoord + d.xw));
 s += decodeHDR(clampSample(texture, v_Texcoord + d.zw));
 gl_FragColor = encodeHDR(s / 4.0);
#endif
}
@end`,hf=`@export clay.compositor.hdr.composite
#define TONEMAPPING
uniform sampler2D texture;
#ifdef BLOOM_ENABLED
uniform sampler2D bloom;
#endif
#ifdef LENSFLARE_ENABLED
uniform sampler2D lensflare;
uniform sampler2D lensdirt;
#endif
#ifdef LUM_ENABLED
uniform sampler2D lum;
#endif
#ifdef LUT_ENABLED
uniform sampler2D lut;
#endif
#ifdef COLOR_CORRECTION
uniform float brightness : 0.0;
uniform float contrast : 1.0;
uniform float saturation : 1.0;
#endif
#ifdef VIGNETTE
uniform float vignetteDarkness: 1.0;
uniform float vignetteOffset: 1.0;
#endif
uniform float exposure : 1.0;
uniform float bloomIntensity : 0.25;
uniform float lensflareIntensity : 1;
varying vec2 v_Texcoord;
@import clay.util.srgb
vec3 ACESToneMapping(vec3 color)
{
 const float A = 2.51;
 const float B = 0.03;
 const float C = 2.43;
 const float D = 0.59;
 const float E = 0.14;
 return (color * (A * color + B)) / (color * (C * color + D) + E);
}
float eyeAdaption(float fLum)
{
 return mix(0.2, fLum, 0.5);
}
#ifdef LUT_ENABLED
vec3 lutTransform(vec3 color) {
 float blueColor = color.b * 63.0;
 vec2 quad1;
 quad1.y = floor(floor(blueColor) / 8.0);
 quad1.x = floor(blueColor) - (quad1.y * 8.0);
 vec2 quad2;
 quad2.y = floor(ceil(blueColor) / 8.0);
 quad2.x = ceil(blueColor) - (quad2.y * 8.0);
 vec2 texPos1;
 texPos1.x = (quad1.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * color.r);
 texPos1.y = (quad1.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * color.g);
 vec2 texPos2;
 texPos2.x = (quad2.x * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * color.r);
 texPos2.y = (quad2.y * 0.125) + 0.5/512.0 + ((0.125 - 1.0/512.0) * color.g);
 vec4 newColor1 = texture2D(lut, texPos1);
 vec4 newColor2 = texture2D(lut, texPos2);
 vec4 newColor = mix(newColor1, newColor2, fract(blueColor));
 return newColor.rgb;
}
#endif
@import clay.util.rgbm
void main()
{
 vec4 texel = vec4(0.0);
 vec4 originalTexel = vec4(0.0);
#ifdef TEXTURE_ENABLED
 texel = decodeHDR(texture2D(texture, v_Texcoord));
 originalTexel = texel;
#endif
#ifdef BLOOM_ENABLED
 vec4 bloomTexel = decodeHDR(texture2D(bloom, v_Texcoord));
 texel.rgb += bloomTexel.rgb * bloomIntensity;
 texel.a += bloomTexel.a * bloomIntensity;
#endif
#ifdef LENSFLARE_ENABLED
 texel += decodeHDR(texture2D(lensflare, v_Texcoord)) * texture2D(lensdirt, v_Texcoord) * lensflareIntensity;
#endif
 texel.a = min(texel.a, 1.0);
#ifdef LUM_ENABLED
 float fLum = texture2D(lum, vec2(0.5, 0.5)).r;
 float adaptedLumDest = 3.0 / (max(0.1, 1.0 + 10.0*eyeAdaption(fLum)));
 float exposureBias = adaptedLumDest * exposure;
#else
 float exposureBias = exposure;
#endif
#ifdef TONEMAPPING
 texel.rgb *= exposureBias;
 texel.rgb = ACESToneMapping(texel.rgb);
#endif
 texel = linearTosRGB(texel);
#ifdef LUT_ENABLED
 texel.rgb = lutTransform(clamp(texel.rgb,vec3(0.0),vec3(1.0)));
#endif
#ifdef COLOR_CORRECTION
 texel.rgb = clamp(texel.rgb + vec3(brightness), 0.0, 1.0);
 texel.rgb = clamp((texel.rgb - vec3(0.5))*contrast+vec3(0.5), 0.0, 1.0);
 float lum = dot(texel.rgb, vec3(0.2125, 0.7154, 0.0721));
 texel.rgb = mix(vec3(lum), texel.rgb, saturation);
#endif
#ifdef VIGNETTE
 vec2 uv = (v_Texcoord - vec2(0.5)) * vec2(vignetteOffset);
 texel.rgb = mix(texel.rgb, vec3(1.0 - vignetteDarkness), dot(uv, uv));
#endif
 gl_FragColor = encodeHDR(texel);
#ifdef DEBUG
 #if DEBUG == 1
 gl_FragColor = encodeHDR(decodeHDR(texture2D(texture, v_Texcoord)));
 #elif DEBUG == 2
 gl_FragColor = encodeHDR(decodeHDR(texture2D(bloom, v_Texcoord)) * bloomIntensity);
 #elif DEBUG == 3
 gl_FragColor = encodeHDR(decodeHDR(texture2D(lensflare, v_Texcoord) * lensflareIntensity));
 #endif
#endif
 if (originalTexel.a <= 0.01 && gl_FragColor.a > 1e-5) {
 gl_FragColor.a = dot(gl_FragColor.rgb, vec3(0.2125, 0.7154, 0.0721));
 }
#ifdef PREMULTIPLY_ALPHA
 gl_FragColor.rgb *= gl_FragColor.a;
#endif
}
@end`,Qm=`@export clay.compositor.lensflare
#define SAMPLE_NUMBER 8
uniform sampler2D texture;
uniform sampler2D lenscolor;
uniform vec2 textureSize : [512, 512];
uniform float dispersal : 0.3;
uniform float haloWidth : 0.4;
uniform float distortion : 1.0;
varying vec2 v_Texcoord;
@import clay.util.rgbm
vec4 textureDistorted(
 in vec2 texcoord,
 in vec2 direction,
 in vec3 distortion
) {
 return vec4(
 decodeHDR(texture2D(texture, texcoord + direction * distortion.r)).r,
 decodeHDR(texture2D(texture, texcoord + direction * distortion.g)).g,
 decodeHDR(texture2D(texture, texcoord + direction * distortion.b)).b,
 1.0
 );
}
void main()
{
 vec2 texcoord = -v_Texcoord + vec2(1.0); vec2 textureOffset = 1.0 / textureSize;
 vec2 ghostVec = (vec2(0.5) - texcoord) * dispersal;
 vec2 haloVec = normalize(ghostVec) * haloWidth;
 vec3 distortion = vec3(-textureOffset.x * distortion, 0.0, textureOffset.x * distortion);
 vec4 result = vec4(0.0);
 for (int i = 0; i < SAMPLE_NUMBER; i++)
 {
 vec2 offset = fract(texcoord + ghostVec * float(i));
 float weight = length(vec2(0.5) - offset) / length(vec2(0.5));
 weight = pow(1.0 - weight, 10.0);
 result += textureDistorted(offset, normalize(ghostVec), distortion) * weight;
 }
 result *= texture2D(lenscolor, vec2(length(vec2(0.5) - texcoord)) / length(vec2(0.5)));
 float weight = length(vec2(0.5) - fract(texcoord + haloVec)) / length(vec2(0.5));
 weight = pow(1.0 - weight, 10.0);
 vec2 offset = fract(texcoord + haloVec);
 result += textureDistorted(offset, normalize(ghostVec), distortion) * weight;
 gl_FragColor = result;
}
@end`,ff=`@export clay.compositor.blend
#define SHADER_NAME blend
#ifdef TEXTURE1_ENABLED
uniform sampler2D texture1;
uniform float weight1 : 1.0;
#endif
#ifdef TEXTURE2_ENABLED
uniform sampler2D texture2;
uniform float weight2 : 1.0;
#endif
#ifdef TEXTURE3_ENABLED
uniform sampler2D texture3;
uniform float weight3 : 1.0;
#endif
#ifdef TEXTURE4_ENABLED
uniform sampler2D texture4;
uniform float weight4 : 1.0;
#endif
#ifdef TEXTURE5_ENABLED
uniform sampler2D texture5;
uniform float weight5 : 1.0;
#endif
#ifdef TEXTURE6_ENABLED
uniform sampler2D texture6;
uniform float weight6 : 1.0;
#endif
varying vec2 v_Texcoord;
@import clay.util.rgbm
void main()
{
 vec4 tex = vec4(0.0);
#ifdef TEXTURE1_ENABLED
 tex += decodeHDR(texture2D(texture1, v_Texcoord)) * weight1;
#endif
#ifdef TEXTURE2_ENABLED
 tex += decodeHDR(texture2D(texture2, v_Texcoord)) * weight2;
#endif
#ifdef TEXTURE3_ENABLED
 tex += decodeHDR(texture2D(texture3, v_Texcoord)) * weight3;
#endif
#ifdef TEXTURE4_ENABLED
 tex += decodeHDR(texture2D(texture4, v_Texcoord)) * weight4;
#endif
#ifdef TEXTURE5_ENABLED
 tex += decodeHDR(texture2D(texture5, v_Texcoord)) * weight5;
#endif
#ifdef TEXTURE6_ENABLED
 tex += decodeHDR(texture2D(texture6, v_Texcoord)) * weight6;
#endif
 gl_FragColor = encodeHDR(tex);
}
@end`,cf=`@export clay.compositor.fxaa
uniform sampler2D texture;
uniform vec4 viewport : VIEWPORT;
varying vec2 v_Texcoord;
#define FXAA_REDUCE_MIN (1.0/128.0)
#define FXAA_REDUCE_MUL (1.0/8.0)
#define FXAA_SPAN_MAX 8.0
@import clay.util.rgbm
void main()
{
 vec2 resolution = 1.0 / viewport.zw;
 vec3 rgbNW = decodeHDR( texture2D( texture, ( gl_FragCoord.xy + vec2( -1.0, -1.0 ) ) * resolution ) ).xyz;
 vec3 rgbNE = decodeHDR( texture2D( texture, ( gl_FragCoord.xy + vec2( 1.0, -1.0 ) ) * resolution ) ).xyz;
 vec3 rgbSW = decodeHDR( texture2D( texture, ( gl_FragCoord.xy + vec2( -1.0, 1.0 ) ) * resolution ) ).xyz;
 vec3 rgbSE = decodeHDR( texture2D( texture, ( gl_FragCoord.xy + vec2( 1.0, 1.0 ) ) * resolution ) ).xyz;
 vec4 rgbaM = decodeHDR( texture2D( texture, gl_FragCoord.xy * resolution ) );
 vec3 rgbM = rgbaM.xyz;
 float opacity = rgbaM.w;
 vec3 luma = vec3( 0.299, 0.587, 0.114 );
 float lumaNW = dot( rgbNW, luma );
 float lumaNE = dot( rgbNE, luma );
 float lumaSW = dot( rgbSW, luma );
 float lumaSE = dot( rgbSE, luma );
 float lumaM = dot( rgbM, luma );
 float lumaMin = min( lumaM, min( min( lumaNW, lumaNE ), min( lumaSW, lumaSE ) ) );
 float lumaMax = max( lumaM, max( max( lumaNW, lumaNE) , max( lumaSW, lumaSE ) ) );
 vec2 dir;
 dir.x = -((lumaNW + lumaNE) - (lumaSW + lumaSE));
 dir.y = ((lumaNW + lumaSW) - (lumaNE + lumaSE));
 float dirReduce = max( ( lumaNW + lumaNE + lumaSW + lumaSE ) * ( 0.25 * FXAA_REDUCE_MUL ), FXAA_REDUCE_MIN );
 float rcpDirMin = 1.0 / ( min( abs( dir.x ), abs( dir.y ) ) + dirReduce );
 dir = min( vec2( FXAA_SPAN_MAX, FXAA_SPAN_MAX),
 max( vec2(-FXAA_SPAN_MAX, -FXAA_SPAN_MAX),
 dir * rcpDirMin)) * resolution;
 vec3 rgbA = decodeHDR( texture2D( texture, gl_FragCoord.xy * resolution + dir * ( 1.0 / 3.0 - 0.5 ) ) ).xyz;
 rgbA += decodeHDR( texture2D( texture, gl_FragCoord.xy * resolution + dir * ( 2.0 / 3.0 - 0.5 ) ) ).xyz;
 rgbA *= 0.5;
 vec3 rgbB = decodeHDR( texture2D( texture, gl_FragCoord.xy * resolution + dir * -0.5 ) ).xyz;
 rgbB += decodeHDR( texture2D( texture, gl_FragCoord.xy * resolution + dir * 0.5 ) ).xyz;
 rgbB *= 0.25;
 rgbB += rgbA * 0.5;
 float lumaB = dot( rgbB, luma );
 if ( ( lumaB < lumaMin ) || ( lumaB > lumaMax ) )
 {
 gl_FragColor = vec4( rgbA, opacity );
 }
 else {
 gl_FragColor = vec4( rgbB, opacity );
 }
}
@end`;function e_(e){e.import($m),e.import(nf),e.import(Km),e.import(af),e.import(Jm),e.import(of),e.import(sf),e.import(lf),e.import(uf),e.import(hf),e.import(Qm),e.import(ff),e.import(cf)}e_(k);var t_=/^#source\((.*?)\)/;function r_(e,t){var r=new jm;t=t||{};var i={textures:{},parameters:{}},n=function(s,l){for(var u=0;u<e.nodes.length;u++){var h=e.nodes[u],f=i_(h,i,t);f&&r.addNode(f)}};for(var a in e.parameters){var o=e.parameters[a];i.parameters[a]=os(o)}return o_(e,i,t,function(s){i.textures=s,n()}),r}function i_(e,t,r){var i=e.type||"filter",n,a,o;if(i==="filter"){var s=e.shader.trim(),l=t_.exec(s);if(l?n=k.source(l[1].trim()):s.charAt(0)==="#"&&(n=t.shaders[s.substr(1)]),n||(n=s),!n)return}if(e.inputs){a={};for(var u in e.inputs)typeof e.inputs[u]=="string"?a[u]=e.inputs[u]:a[u]={node:e.inputs[u].node,pin:e.inputs[u].pin}}if(e.outputs){o={};for(var u in e.outputs){var h=e.outputs[u];o[u]={},h.attachment!=null&&(o[u].attachment=h.attachment),h.keepLastFrame!=null&&(o[u].keepLastFrame=h.keepLastFrame),h.outputLastFrame!=null&&(o[u].outputLastFrame=h.outputLastFrame),h.parameters&&(o[u].parameters=os(h.parameters))}}var f;if(i==="scene"?f=new Zm({name:e.name,scene:r.scene,camera:r.camera,outputs:o}):i==="texture"?f=new qm({name:e.name,outputs:o}):f=new Ym({name:e.name,shader:n,inputs:a,outputs:o}),f){if(e.parameters)for(var u in e.parameters){var d=e.parameters[u];typeof d=="string"?(d=d.trim(),d.charAt(0)==="#"?d=t.textures[d.substr(1)]:f.on("beforerender",s_(u,df(d)))):typeof d=="function"&&f.on("beforerender",d),f.setParameter(u,d)}if(e.defines&&f.pass)for(var u in e.defines){var d=e.defines[u];f.pass.material.define("fragment",u,d)}}return f}function n_(e,t){return e}function a_(e,t){return t}function os(e){var t={};if(!e)return t;["type","minFilter","magFilter","wrapS","wrapT","flipY","useMipmap"].forEach(function(i){var n=e[i];n!=null&&(typeof n=="string"&&(n=H[n]),t[i]=n)});var r=e.scale||1;return["width","height"].forEach(function(i){if(e[i]!=null){var n=e[i];typeof n=="string"?(n=n.trim(),t[i]=l_(i,df(n),r)):t[i]=n}}),t.width||(t.width=n_),t.height||(t.height=a_),e.useMipmap!=null&&(t.useMipmap=e.useMipmap),t}function o_(e,t,r,i){if(!e.textures){i({});return}var n={},a=0,o=!1,s=r.textureRootPath;Pe.each(e.textures,function(l,u){var h,f=l.path,d=os(l.parameters);if(Array.isArray(f)&&f.length===6)s&&(f=f.map(function(c){return Pe.relative2absolute(c,s)})),h=new Vr(d);else if(typeof f=="string")s&&(f=Pe.relative2absolute(f,s)),h=new ne(d);else return;h.load(f),a++,h.once("success",function(){n[u]=h,a--,a===0&&(i(n),o=!0)})}),a===0&&!o&&i(n)}function s_(e,t){return function(r){var i=r.getDevicePixelRatio(),n=r.getWidth(),a=r.getHeight(),o=t(n,a,i);this.setParameter(e,o)}}function l_(e,t,r){return r=r||1,function(i){var n=i.getDevicePixelRatio(),a=i.getWidth()*r,o=i.getHeight()*r;return t(a,o,n)}}function df(e){var t=/^expr\((.*)\)$/.exec(e);if(t)try{var r=new Function("width","height","dpr","return "+t[1]);return r(1,1),r}catch{throw new Error("Invalid expression.")}}function yi(e,t){for(var r=0,i=1/t,n=e;n>0;)r=r+i*(n%t),n=Math.floor(n/t),i=i/t;return r}const u_=`@export ecgl.ssao.estimate

uniform sampler2D depthTex;

uniform sampler2D normalTex;

uniform sampler2D noiseTex;

uniform vec2 depthTexSize;

uniform vec2 noiseTexSize;

uniform mat4 projection;

uniform mat4 projectionInv;

uniform mat4 viewInverseTranspose;

uniform vec3 kernel[KERNEL_SIZE];

uniform float radius : 1;

uniform float power : 1;

uniform float bias: 1e-2;

uniform float intensity: 1.0;

varying vec2 v_Texcoord;

float ssaoEstimator(in vec3 originPos, in mat3 kernelBasis) {
 float occlusion = 0.0;

 for (int i = 0; i < KERNEL_SIZE; i++) {
 vec3 samplePos = kernel[i];
#ifdef NORMALTEX_ENABLED
 samplePos = kernelBasis * samplePos;
#endif
 samplePos = samplePos * radius + originPos;

 vec4 texCoord = projection * vec4(samplePos, 1.0);
 texCoord.xy /= texCoord.w;

 vec4 depthTexel = texture2D(depthTex, texCoord.xy * 0.5 + 0.5);

 float sampleDepth = depthTexel.r * 2.0 - 1.0;
 if (projection[3][3] == 0.0) {
 sampleDepth = projection[3][2] / (sampleDepth * projection[2][3] - projection[2][2]);
 }
 else {
 sampleDepth = (sampleDepth - projection[3][2]) / projection[2][2];
 }
 
 float rangeCheck = smoothstep(0.0, 1.0, radius / abs(originPos.z - sampleDepth));
 occlusion += rangeCheck * step(samplePos.z, sampleDepth - bias);
 }
#ifdef NORMALTEX_ENABLED
 occlusion = 1.0 - occlusion / float(KERNEL_SIZE);
#else
 occlusion = 1.0 - clamp((occlusion / float(KERNEL_SIZE) - 0.6) * 2.5, 0.0, 1.0);
#endif
 return pow(occlusion, power);
}

void main()
{

 vec4 depthTexel = texture2D(depthTex, v_Texcoord);

#ifdef NORMALTEX_ENABLED
 vec4 tex = texture2D(normalTex, v_Texcoord);
 if (dot(tex.rgb, tex.rgb) == 0.0) {
 gl_FragColor = vec4(1.0);
 return;
 }
 vec3 N = tex.rgb * 2.0 - 1.0;
 N = (viewInverseTranspose * vec4(N, 0.0)).xyz;

 vec2 noiseTexCoord = depthTexSize / vec2(noiseTexSize) * v_Texcoord;
 vec3 rvec = texture2D(noiseTex, noiseTexCoord).rgb * 2.0 - 1.0;
 vec3 T = normalize(rvec - N * dot(rvec, N));
 vec3 BT = normalize(cross(N, T));
 mat3 kernelBasis = mat3(T, BT, N);
#else
 if (depthTexel.r > 0.99999) {
 gl_FragColor = vec4(1.0);
 return;
 }
 mat3 kernelBasis;
#endif

 float z = depthTexel.r * 2.0 - 1.0;

 vec4 projectedPos = vec4(v_Texcoord * 2.0 - 1.0, z, 1.0);
 vec4 p4 = projectionInv * projectedPos;

 vec3 position = p4.xyz / p4.w;

 float ao = ssaoEstimator(position, kernelBasis);
 ao = clamp(1.0 - (1.0 - ao) * intensity, 0.0, 1.0);
 gl_FragColor = vec4(vec3(ao), 1.0);
}

@end


@export ecgl.ssao.blur
#define SHADER_NAME SSAO_BLUR

uniform sampler2D ssaoTexture;

#ifdef NORMALTEX_ENABLED
uniform sampler2D normalTex;
#endif

varying vec2 v_Texcoord;

uniform vec2 textureSize;
uniform float blurSize : 1.0;

uniform int direction: 0.0;

#ifdef DEPTHTEX_ENABLED
uniform sampler2D depthTex;
uniform mat4 projection;
uniform float depthRange : 0.5;

float getLinearDepth(vec2 coord)
{
 float depth = texture2D(depthTex, coord).r * 2.0 - 1.0;
 return projection[3][2] / (depth * projection[2][3] - projection[2][2]);
}
#endif

void main()
{
 float kernel[5];
 kernel[0] = 0.122581;
 kernel[1] = 0.233062;
 kernel[2] = 0.288713;
 kernel[3] = 0.233062;
 kernel[4] = 0.122581;

 vec2 off = vec2(0.0);
 if (direction == 0) {
 off[0] = blurSize / textureSize.x;
 }
 else {
 off[1] = blurSize / textureSize.y;
 }

 vec2 coord = v_Texcoord;

 float sum = 0.0;
 float weightAll = 0.0;

#ifdef NORMALTEX_ENABLED
 vec3 centerNormal = texture2D(normalTex, v_Texcoord).rgb * 2.0 - 1.0;
#endif
#if defined(DEPTHTEX_ENABLED)
 float centerDepth = getLinearDepth(v_Texcoord);
#endif

 for (int i = 0; i < 5; i++) {
 vec2 coord = clamp(v_Texcoord + vec2(float(i) - 2.0) * off, vec2(0.0), vec2(1.0));

 float w = kernel[i];
#ifdef NORMALTEX_ENABLED
 vec3 normal = texture2D(normalTex, coord).rgb * 2.0 - 1.0;
 w *= clamp(dot(normal, centerNormal), 0.0, 1.0);
#endif
#ifdef DEPTHTEX_ENABLED
 float d = getLinearDepth(coord);
 w *= (1.0 - smoothstep(abs(centerDepth - d) / depthRange, 0.0, 1.0));
#endif

 weightAll += w;
 sum += texture2D(ssaoTexture, coord).r * w;
 }

 gl_FragColor = vec4(vec3(sum / weightAll), 1.0);
}

@end
`;k.import(u_);function vf(e){for(var t=new Uint8Array(e*e*4),r=0,i=new R,n=0;n<e;n++)for(var a=0;a<e;a++)i.set(Math.random()*2-1,Math.random()*2-1,0).normalize(),t[r++]=(i.x*.5+.5)*255,t[r++]=(i.y*.5+.5)*255,t[r++]=0,t[r++]=255;return t}function gu(e){return new ne({pixels:vf(e),wrapS:H.REPEAT,wrapT:H.REPEAT,width:e,height:e})}function h_(e,t,r){var i=new Float32Array(e*3);t=t||0;for(var n=0;n<e;n++){var a=yi(n+t,2)*(r?1:2)*Math.PI,o=yi(n+t,3)*Math.PI,s=Math.random(),l=Math.cos(a)*Math.sin(o)*s,u=Math.cos(o)*s,h=Math.sin(a)*Math.sin(o)*s;i[n*3]=l,i[n*3+1]=u,i[n*3+2]=h}return i}function er(e){e=e||{},this._ssaoPass=new Oe({fragment:k.source("ecgl.ssao.estimate")}),this._blurPass=new Oe({fragment:k.source("ecgl.ssao.blur")}),this._framebuffer=new Ie({depthBuffer:!1}),this._ssaoTexture=new ne,this._blurTexture=new ne,this._blurTexture2=new ne,this._depthTex=e.depthTexture,this._normalTex=e.normalTexture,this.setNoiseSize(4),this.setKernelSize(e.kernelSize||12),e.radius!=null&&this.setParameter("radius",e.radius),e.power!=null&&this.setParameter("power",e.power),this._normalTex||(this._ssaoPass.material.disableTexture("normalTex"),this._blurPass.material.disableTexture("normalTex")),this._depthTex||this._blurPass.material.disableTexture("depthTex"),this._blurPass.material.setUniform("normalTex",this._normalTex),this._blurPass.material.setUniform("depthTex",this._depthTex)}er.prototype.setDepthTexture=function(e){this._depthTex=e};er.prototype.setNormalTexture=function(e){this._normalTex=e,this._ssaoPass.material[e?"enableTexture":"disableTexture"]("normalTex"),this.setKernelSize(this._kernelSize)};er.prototype.update=function(e,t,r){var i=e.getWidth(),n=e.getHeight(),a=this._ssaoPass,o=this._blurPass;a.setUniform("kernel",this._kernels[r%this._kernels.length]),a.setUniform("depthTex",this._depthTex),this._normalTex!=null&&a.setUniform("normalTex",this._normalTex),a.setUniform("depthTexSize",[this._depthTex.width,this._depthTex.height]);var s=new W;W.transpose(s,t.worldTransform),a.setUniform("projection",t.projectionMatrix.array),a.setUniform("projectionInv",t.invProjectionMatrix.array),a.setUniform("viewInverseTranspose",s.array);var l=this._ssaoTexture,u=this._blurTexture,h=this._blurTexture2;l.width=i/2,l.height=n/2,u.width=i,u.height=n,h.width=i,h.height=n,this._framebuffer.attach(l),this._framebuffer.bind(e),e.gl.clearColor(1,1,1,1),e.gl.clear(e.gl.COLOR_BUFFER_BIT),a.render(e),o.setUniform("textureSize",[i/2,n/2]),o.setUniform("projection",t.projectionMatrix.array),this._framebuffer.attach(u),o.setUniform("direction",0),o.setUniform("ssaoTexture",l),o.render(e),this._framebuffer.attach(h),o.setUniform("textureSize",[i,n]),o.setUniform("direction",1),o.setUniform("ssaoTexture",u),o.render(e),this._framebuffer.unbind(e);var f=e.clearColor;e.gl.clearColor(f[0],f[1],f[2],f[3])};er.prototype.getTargetTexture=function(){return this._blurTexture2};er.prototype.setParameter=function(e,t){e==="noiseTexSize"?this.setNoiseSize(t):e==="kernelSize"?this.setKernelSize(t):e==="intensity"?this._ssaoPass.material.set("intensity",t):this._ssaoPass.setUniform(e,t)};er.prototype.setKernelSize=function(e){this._kernelSize=e,this._ssaoPass.material.define("fragment","KERNEL_SIZE",e),this._kernels=this._kernels||[];for(var t=0;t<30;t++)this._kernels[t]=h_(e,t*e,!!this._normalTex)};er.prototype.setNoiseSize=function(e){var t=this._ssaoPass.getUniform("noiseTex");t?(t.data=vf(e),t.width=t.height=e,t.dirty()):(t=gu(e),this._ssaoPass.setUniform("noiseTex",gu(e))),this._ssaoPass.setUniform("noiseTexSize",[e,e])};er.prototype.dispose=function(e){this._blurTexture.dispose(e),this._ssaoTexture.dispose(e),this._blurTexture2.dispose(e)};const f_=`@export ecgl.ssr.main

#define SHADER_NAME SSR
#define MAX_ITERATION 20;
#define SAMPLE_PER_FRAME 5;
#define TOTAL_SAMPLES 128;

uniform sampler2D sourceTexture;
uniform sampler2D gBufferTexture1;
uniform sampler2D gBufferTexture2;
uniform sampler2D gBufferTexture3;
uniform samplerCube specularCubemap;
uniform float specularIntensity: 1;

uniform mat4 projection;
uniform mat4 projectionInv;
uniform mat4 toViewSpace;
uniform mat4 toWorldSpace;

uniform float maxRayDistance: 200;

uniform float pixelStride: 16;
uniform float pixelStrideZCutoff: 50; 
uniform float screenEdgeFadeStart: 0.9; 
uniform float eyeFadeStart : 0.2; uniform float eyeFadeEnd: 0.8; 
uniform float minGlossiness: 0.2; uniform float zThicknessThreshold: 1;

uniform float nearZ;
uniform vec2 viewportSize : VIEWPORT_SIZE;

uniform float jitterOffset: 0;

varying vec2 v_Texcoord;

#ifdef DEPTH_DECODE
@import clay.util.decode_float
#endif

#ifdef PHYSICALLY_CORRECT
uniform sampler2D normalDistribution;
uniform float sampleOffset: 0;
uniform vec2 normalDistributionSize;

vec3 transformNormal(vec3 H, vec3 N) {
 vec3 upVector = N.y > 0.999 ? vec3(1.0, 0.0, 0.0) : vec3(0.0, 1.0, 0.0);
 vec3 tangentX = normalize(cross(N, upVector));
 vec3 tangentZ = cross(N, tangentX);
 return normalize(tangentX * H.x + N * H.y + tangentZ * H.z);
}
vec3 importanceSampleNormalGGX(float i, float roughness, vec3 N) {
 float p = fract((i + sampleOffset) / float(TOTAL_SAMPLES));
 vec3 H = texture2D(normalDistribution,vec2(roughness, p)).rgb;
 return transformNormal(H, N);
}
float G_Smith(float g, float ndv, float ndl) {
 float roughness = 1.0 - g;
 float k = roughness * roughness / 2.0;
 float G1V = ndv / (ndv * (1.0 - k) + k);
 float G1L = ndl / (ndl * (1.0 - k) + k);
 return G1L * G1V;
}
vec3 F_Schlick(float ndv, vec3 spec) {
 return spec + (1.0 - spec) * pow(1.0 - ndv, 5.0);
}
#endif

float fetchDepth(sampler2D depthTexture, vec2 uv)
{
 vec4 depthTexel = texture2D(depthTexture, uv);
 return depthTexel.r * 2.0 - 1.0;
}

float linearDepth(float depth)
{
 if (projection[3][3] == 0.0) {
 return projection[3][2] / (depth * projection[2][3] - projection[2][2]);
 }
 else {
 return (depth - projection[3][2]) / projection[2][2];
 }
}

bool rayIntersectDepth(float rayZNear, float rayZFar, vec2 hitPixel)
{
 if (rayZFar > rayZNear)
 {
 float t = rayZFar; rayZFar = rayZNear; rayZNear = t;
 }
 float cameraZ = linearDepth(fetchDepth(gBufferTexture2, hitPixel));
 return rayZFar <= cameraZ && rayZNear >= cameraZ - zThicknessThreshold;
}


bool traceScreenSpaceRay(
 vec3 rayOrigin, vec3 rayDir, float jitter,
 out vec2 hitPixel, out vec3 hitPoint, out float iterationCount
)
{
 float rayLength = ((rayOrigin.z + rayDir.z * maxRayDistance) > -nearZ)
 ? (-nearZ - rayOrigin.z) / rayDir.z : maxRayDistance;

 vec3 rayEnd = rayOrigin + rayDir * rayLength;

 vec4 H0 = projection * vec4(rayOrigin, 1.0);
 vec4 H1 = projection * vec4(rayEnd, 1.0);

 float k0 = 1.0 / H0.w, k1 = 1.0 / H1.w;

 vec3 Q0 = rayOrigin * k0, Q1 = rayEnd * k1;

 vec2 P0 = (H0.xy * k0 * 0.5 + 0.5) * viewportSize;
 vec2 P1 = (H1.xy * k1 * 0.5 + 0.5) * viewportSize;

 P1 += dot(P1 - P0, P1 - P0) < 0.0001 ? 0.01 : 0.0;
 vec2 delta = P1 - P0;

 bool permute = false;
 if (abs(delta.x) < abs(delta.y)) {
 permute = true;
 delta = delta.yx;
 P0 = P0.yx;
 P1 = P1.yx;
 }
 float stepDir = sign(delta.x);
 float invdx = stepDir / delta.x;

 vec3 dQ = (Q1 - Q0) * invdx;
 float dk = (k1 - k0) * invdx;

 vec2 dP = vec2(stepDir, delta.y * invdx);

 float strideScaler = 1.0 - min(1.0, -rayOrigin.z / pixelStrideZCutoff);
 float pixStride = 1.0 + strideScaler * pixelStride;

 dP *= pixStride; dQ *= pixStride; dk *= pixStride;

 vec4 pqk = vec4(P0, Q0.z, k0);
 vec4 dPQK = vec4(dP, dQ.z, dk);

 pqk += dPQK * jitter;
 float rayZFar = (dPQK.z * 0.5 + pqk.z) / (dPQK.w * 0.5 + pqk.w);
 float rayZNear;

 bool intersect = false;

 vec2 texelSize = 1.0 / viewportSize;

 iterationCount = 0.0;

 for (int i = 0; i < MAX_ITERATION; i++)
 {
 pqk += dPQK;

 rayZNear = rayZFar;
 rayZFar = (dPQK.z * 0.5 + pqk.z) / (dPQK.w * 0.5 + pqk.w);

 hitPixel = permute ? pqk.yx : pqk.xy;
 hitPixel *= texelSize;

 intersect = rayIntersectDepth(rayZNear, rayZFar, hitPixel);

 iterationCount += 1.0;

 dPQK *= 1.2;

 if (intersect) {
 break;
 }
 }

 Q0.xy += dQ.xy * iterationCount;
 Q0.z = pqk.z;
 hitPoint = Q0 / pqk.w;

 return intersect;
}

float calculateAlpha(
 float iterationCount, float reflectivity,
 vec2 hitPixel, vec3 hitPoint, float dist, vec3 rayDir
)
{
 float alpha = clamp(reflectivity, 0.0, 1.0);
 alpha *= 1.0 - (iterationCount / float(MAX_ITERATION));
 vec2 hitPixelNDC = hitPixel * 2.0 - 1.0;
 float maxDimension = min(1.0, max(abs(hitPixelNDC.x), abs(hitPixelNDC.y)));
 alpha *= 1.0 - max(0.0, maxDimension - screenEdgeFadeStart) / (1.0 - screenEdgeFadeStart);

 float _eyeFadeStart = eyeFadeStart;
 float _eyeFadeEnd = eyeFadeEnd;
 if (_eyeFadeStart > _eyeFadeEnd) {
 float tmp = _eyeFadeEnd;
 _eyeFadeEnd = _eyeFadeStart;
 _eyeFadeStart = tmp;
 }

 float eyeDir = clamp(rayDir.z, _eyeFadeStart, _eyeFadeEnd);
 alpha *= 1.0 - (eyeDir - _eyeFadeStart) / (_eyeFadeEnd - _eyeFadeStart);

 alpha *= 1.0 - clamp(dist / maxRayDistance, 0.0, 1.0);

 return alpha;
}

@import clay.util.rand

@import clay.util.rgbm

void main()
{
 vec4 normalAndGloss = texture2D(gBufferTexture1, v_Texcoord);

 if (dot(normalAndGloss.rgb, vec3(1.0)) == 0.0) {
 discard;
 }

 float g = normalAndGloss.a;
#if !defined(PHYSICALLY_CORRECT)
 if (g <= minGlossiness) {
 discard;
 }
#endif

 float reflectivity = (g - minGlossiness) / (1.0 - minGlossiness);

 vec3 N = normalize(normalAndGloss.rgb * 2.0 - 1.0);
 N = normalize((toViewSpace * vec4(N, 0.0)).xyz);

 vec4 projectedPos = vec4(v_Texcoord * 2.0 - 1.0, fetchDepth(gBufferTexture2, v_Texcoord), 1.0);
 vec4 pos = projectionInv * projectedPos;
 vec3 rayOrigin = pos.xyz / pos.w;
 vec3 V = -normalize(rayOrigin);

 float ndv = clamp(dot(N, V), 0.0, 1.0);
 float iterationCount;
 float jitter = rand(fract(v_Texcoord + jitterOffset));

#ifdef PHYSICALLY_CORRECT
 vec4 color = vec4(vec3(0.0), 1.0);
 vec4 albedoMetalness = texture2D(gBufferTexture3, v_Texcoord);
 vec3 albedo = albedoMetalness.rgb;
 float m = albedoMetalness.a;
 vec3 diffuseColor = albedo * (1.0 - m);
 vec3 spec = mix(vec3(0.04), albedo, m);

 float jitter2 = rand(fract(v_Texcoord)) * float(TOTAL_SAMPLES);

 for (int i = 0; i < SAMPLE_PER_FRAME; i++) {
 vec3 H = importanceSampleNormalGGX(float(i) + jitter2, 1.0 - g, N);
 vec3 rayDir = normalize(reflect(-V, H));
#else
 vec3 rayDir = normalize(reflect(-V, N));
#endif
 vec2 hitPixel;
 vec3 hitPoint;

 bool intersect = traceScreenSpaceRay(rayOrigin, rayDir, jitter, hitPixel, hitPoint, iterationCount);

 float dist = distance(rayOrigin, hitPoint);

 vec3 hitNormal = texture2D(gBufferTexture1, hitPixel).rgb * 2.0 - 1.0;
 hitNormal = normalize((toViewSpace * vec4(hitNormal, 0.0)).xyz);
#ifdef PHYSICALLY_CORRECT
 float ndl = clamp(dot(N, rayDir), 0.0, 1.0);
 float vdh = clamp(dot(V, H), 0.0, 1.0);
 float ndh = clamp(dot(N, H), 0.0, 1.0);
 vec3 litTexel = vec3(0.0);
 if (dot(hitNormal, rayDir) < 0.0 && intersect) {
 litTexel = texture2D(sourceTexture, hitPixel).rgb;
 litTexel *= pow(clamp(1.0 - dist / 200.0, 0.0, 1.0), 3.0);

 }
 else {
 #ifdef SPECULARCUBEMAP_ENABLED
 vec3 rayDirW = normalize(toWorldSpace * vec4(rayDir, 0.0)).rgb;
 litTexel = RGBMDecode(textureCubeLodEXT(specularCubemap, rayDirW, 0.0), 8.12).rgb * specularIntensity;
#endif
 }
 color.rgb += ndl * litTexel * (
 F_Schlick(ndl, spec) * G_Smith(g, ndv, ndl) * vdh / (ndh * ndv + 0.001)
 );
 }
 color.rgb /= float(SAMPLE_PER_FRAME);
#else
 #if !defined(SPECULARCUBEMAP_ENABLED)
 if (dot(hitNormal, rayDir) >= 0.0) {
 discard;
 }
 if (!intersect) {
 discard;
 }
#endif
 float alpha = clamp(calculateAlpha(iterationCount, reflectivity, hitPixel, hitPoint, dist, rayDir), 0.0, 1.0);
 vec4 color = texture2D(sourceTexture, hitPixel);
 color.rgb *= alpha;

#ifdef SPECULARCUBEMAP_ENABLED
 vec3 rayDirW = normalize(toWorldSpace * vec4(rayDir, 0.0)).rgb;
 alpha = alpha * (intersect ? 1.0 : 0.0);
 float bias = (1.0 -g) * 5.0;
 color.rgb += (1.0 - alpha)
 * RGBMDecode(textureCubeLodEXT(specularCubemap, rayDirW, bias), 8.12).rgb
 * specularIntensity;
#endif

#endif

 gl_FragColor = encodeHDR(color);
}
@end

@export ecgl.ssr.blur

uniform sampler2D texture;
uniform sampler2D gBufferTexture1;
uniform sampler2D gBufferTexture2;
uniform mat4 projection;
uniform float depthRange : 0.05;

varying vec2 v_Texcoord;

uniform vec2 textureSize;
uniform float blurSize : 1.0;

#ifdef BLEND
 #ifdef SSAOTEX_ENABLED
uniform sampler2D ssaoTex;
 #endif
uniform sampler2D sourceTexture;
#endif

float getLinearDepth(vec2 coord)
{
 float depth = texture2D(gBufferTexture2, coord).r * 2.0 - 1.0;
 return projection[3][2] / (depth * projection[2][3] - projection[2][2]);
}

@import clay.util.rgbm


void main()
{
 @import clay.compositor.kernel.gaussian_9

 vec4 centerNTexel = texture2D(gBufferTexture1, v_Texcoord);
 float g = centerNTexel.a;
 float maxBlurSize = clamp(1.0 - g, 0.0, 1.0) * blurSize;
#ifdef VERTICAL
 vec2 off = vec2(0.0, maxBlurSize / textureSize.y);
#else
 vec2 off = vec2(maxBlurSize / textureSize.x, 0.0);
#endif

 vec2 coord = v_Texcoord;

 vec4 sum = vec4(0.0);
 float weightAll = 0.0;

 vec3 cN = centerNTexel.rgb * 2.0 - 1.0;
 float cD = getLinearDepth(v_Texcoord);
 for (int i = 0; i < 9; i++) {
 vec2 coord = clamp((float(i) - 4.0) * off + v_Texcoord, vec2(0.0), vec2(1.0));
 float w = gaussianKernel[i]
 * clamp(dot(cN, texture2D(gBufferTexture1, coord).rgb * 2.0 - 1.0), 0.0, 1.0);
 float d = getLinearDepth(coord);
 w *= (1.0 - smoothstep(abs(cD - d) / depthRange, 0.0, 1.0));

 weightAll += w;
 sum += decodeHDR(texture2D(texture, coord)) * w;
 }

#ifdef BLEND
 float aoFactor = 1.0;
 #ifdef SSAOTEX_ENABLED
 aoFactor = texture2D(ssaoTex, v_Texcoord).r;
 #endif
 gl_FragColor = encodeHDR(
 sum / weightAll * aoFactor + decodeHDR(texture2D(sourceTexture, v_Texcoord))
 );
#else
 gl_FragColor = encodeHDR(sum / weightAll);
#endif
}

@end`;k.import(f_);function tr(e){e=e||{},this._ssrPass=new Oe({fragment:k.source("ecgl.ssr.main"),clearColor:[0,0,0,0]}),this._blurPass1=new Oe({fragment:k.source("ecgl.ssr.blur"),clearColor:[0,0,0,0]}),this._blurPass2=new Oe({fragment:k.source("ecgl.ssr.blur"),clearColor:[0,0,0,0]}),this._blendPass=new Oe({fragment:k.source("clay.compositor.blend")}),this._blendPass.material.disableTexturesAll(),this._blendPass.material.enableTexture(["texture1","texture2"]),this._ssrPass.setUniform("gBufferTexture1",e.normalTexture),this._ssrPass.setUniform("gBufferTexture2",e.depthTexture),this._blurPass1.setUniform("gBufferTexture1",e.normalTexture),this._blurPass1.setUniform("gBufferTexture2",e.depthTexture),this._blurPass2.setUniform("gBufferTexture1",e.normalTexture),this._blurPass2.setUniform("gBufferTexture2",e.depthTexture),this._blurPass2.material.define("fragment","VERTICAL"),this._blurPass2.material.define("fragment","BLEND"),this._ssrTexture=new ne({type:H.HALF_FLOAT}),this._texture2=new ne({type:H.HALF_FLOAT}),this._texture3=new ne({type:H.HALF_FLOAT}),this._prevTexture=new ne({type:H.HALF_FLOAT}),this._currentTexture=new ne({type:H.HALF_FLOAT}),this._frameBuffer=new Ie({depthBuffer:!1}),this._normalDistribution=null,this._totalSamples=256,this._samplePerFrame=4,this._ssrPass.material.define("fragment","SAMPLE_PER_FRAME",this._samplePerFrame),this._ssrPass.material.define("fragment","TOTAL_SAMPLES",this._totalSamples),this._downScale=1}tr.prototype.setAmbientCubemap=function(e,t){this._ssrPass.material.set("specularCubemap",e),this._ssrPass.material.set("specularIntensity",t);var r=e&&t;this._ssrPass.material[r?"enableTexture":"disableTexture"]("specularCubemap")};tr.prototype.update=function(e,t,r,i){var n=e.getWidth(),a=e.getHeight(),o=this._ssrTexture,s=this._texture2,l=this._texture3;o.width=this._prevTexture.width=this._currentTexture.width=n/this._downScale,o.height=this._prevTexture.height=this._currentTexture.height=a/this._downScale,s.width=l.width=n,s.height=l.height=a;var u=this._frameBuffer,h=this._ssrPass,f=this._blurPass1,d=this._blurPass2,c=this._blendPass,v=new W,p=new W;W.transpose(v,t.worldTransform),W.transpose(p,t.viewMatrix),h.setUniform("sourceTexture",r),h.setUniform("projection",t.projectionMatrix.array),h.setUniform("projectionInv",t.invProjectionMatrix.array),h.setUniform("toViewSpace",v.array),h.setUniform("toWorldSpace",p.array),h.setUniform("nearZ",t.near);var _=i/this._totalSamples*this._samplePerFrame;if(h.setUniform("jitterOffset",_),h.setUniform("sampleOffset",i*this._samplePerFrame),f.setUniform("textureSize",[o.width,o.height]),d.setUniform("textureSize",[n,a]),d.setUniform("sourceTexture",r),f.setUniform("projection",t.projectionMatrix.array),d.setUniform("projection",t.projectionMatrix.array),u.attach(o),u.bind(e),h.render(e),this._physicallyCorrect&&(u.attach(this._currentTexture),c.setUniform("texture1",this._prevTexture),c.setUniform("texture2",o),c.material.set({weight1:i>=1?.95:0,weight2:i>=1?.05:1}),c.render(e)),u.attach(s),f.setUniform("texture",this._physicallyCorrect?this._currentTexture:o),f.render(e),u.attach(l),d.setUniform("texture",s),d.render(e),u.unbind(e),this._physicallyCorrect){var m=this._prevTexture;this._prevTexture=this._currentTexture,this._currentTexture=m}};tr.prototype.getTargetTexture=function(){return this._texture3};tr.prototype.setParameter=function(e,t){e==="maxIteration"?this._ssrPass.material.define("fragment","MAX_ITERATION",t):this._ssrPass.setUniform(e,t)};tr.prototype.setPhysicallyCorrect=function(e){e?(this._normalDistribution||(this._normalDistribution=kt.generateNormalDistribution(64,this._totalSamples)),this._ssrPass.material.define("fragment","PHYSICALLY_CORRECT"),this._ssrPass.material.set("normalDistribution",this._normalDistribution),this._ssrPass.material.set("normalDistributionSize",[64,this._totalSamples])):this._ssrPass.material.undefine("fragment","PHYSICALLY_CORRECT"),this._physicallyCorrect=e};tr.prototype.setSSAOTexture=function(e){var t=this._blurPass2;e?(t.material.enableTexture("ssaoTex"),t.material.set("ssaoTex",e)):t.material.disableTexture("ssaoTex")};tr.prototype.isFinished=function(e){return this._physicallyCorrect?e>this._totalSamples/this._samplePerFrame:!0};tr.prototype.dispose=function(e){this._ssrTexture.dispose(e),this._texture2.dispose(e),this._texture3.dispose(e),this._prevTexture.dispose(e),this._currentTexture.dispose(e),this._frameBuffer.dispose(e)};const mu=[0,0,-.321585265978,-.154972575841,.458126042375,.188473391593,.842080129861,.527766490688,.147304551086,-.659453822776,-.331943915203,-.940619700594,.0479226680259,.54812163202,.701581552186,-.709825561388,-.295436780218,.940589268233,-.901489676764,.237713156085,.973570876096,-.109899459384,-.866792314779,-.451805525005,.330975007087,.800048655954,-.344275183665,.381779221166,-.386139432542,-.437418421534,-.576478634965,-.0148463392551,.385798197415,-.262426961053,-.666302061145,.682427250835,-.628010632582,-.732836215494,.10163141741,-.987658134403,.711995289051,-.320024291314,.0296005138058,.950296523438,.0130612307608,-.351024443122,-.879596633704,-.10478487883,.435712737232,.504254490347,.779203817497,.206477676721,.388264289969,-.896736162545,-.153106280781,-.629203242522,-.245517550697,.657969239148,.126830499058,.26862328493,-.634888119007,-.302301223431,.617074219636,.779817204925],c_=`@export ecgl.normal.vertex

@import ecgl.common.transformUniforms

@import ecgl.common.uv.header

@import ecgl.common.attributes

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

@import ecgl.common.normalMap.vertexHeader

@import ecgl.common.vertexAnimation.header

void main()
{

 @import ecgl.common.vertexAnimation.main

 @import ecgl.common.uv.main

 v_Normal = normalize((worldInverseTranspose * vec4(normal, 0.0)).xyz);
 v_WorldPosition = (world * vec4(pos, 1.0)).xyz;

 @import ecgl.common.normalMap.vertexMain

 gl_Position = worldViewProjection * vec4(pos, 1.0);

}


@end


@export ecgl.normal.fragment

#define ROUGHNESS_CHANEL 0

uniform bool useBumpMap;
uniform bool useRoughnessMap;
uniform bool doubleSide;
uniform float roughness;

@import ecgl.common.uv.fragmentHeader

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

uniform mat4 viewInverse : VIEWINVERSE;

@import ecgl.common.normalMap.fragmentHeader
@import ecgl.common.bumpMap.header

uniform sampler2D roughnessMap;

void main()
{
 vec3 N = v_Normal;
 
 bool flipNormal = false;
 if (doubleSide) {
 vec3 eyePos = viewInverse[3].xyz;
 vec3 V = normalize(eyePos - v_WorldPosition);

 if (dot(N, V) < 0.0) {
 flipNormal = true;
 }
 }

 @import ecgl.common.normalMap.fragmentMain

 if (useBumpMap) {
 N = bumpNormal(v_WorldPosition, v_Normal, N);
 }

 float g = 1.0 - roughness;

 if (useRoughnessMap) {
 float g2 = 1.0 - texture2D(roughnessMap, v_DetailTexcoord)[ROUGHNESS_CHANEL];
 g = clamp(g2 + (g - 0.5) * 2.0, 0.0, 1.0);
 }

 if (flipNormal) {
 N = -N;
 }

 gl_FragColor.rgb = (N.xyz + 1.0) * 0.5;
 gl_FragColor.a = g;
}
@end`;k.import(c_);function io(e,t,r,i,n){var a=e.gl;t.setUniform(a,"1i",r,n),a.activeTexture(a.TEXTURE0+n),i.isRenderable()?i.bind(e):i.unbind(e)}function d_(e,t,r,i,n){var a,o,s,l,u=e.gl;return function(h,f,d){if(!(l&&l.material===h.material)){var c=h.material,v=h.__program,p=c.get("roughness");p==null&&(p=1);var _=c.get("normalMap")||t,m=c.get("roughnessMap"),g=c.get("bumpMap"),y=c.get("uvRepeat"),x=c.get("uvOffset"),w=c.get("detailUvRepeat"),T=c.get("detailUvOffset"),b=!!g&&c.isTextureEnabled("bumpMap"),A=!!m&&c.isTextureEnabled("roughnessMap"),C=c.isDefined("fragment","DOUBLE_SIDED");g=g||r,m=m||i,d!==f?(f.set("normalMap",_),f.set("bumpMap",g),f.set("roughnessMap",m),f.set("useBumpMap",b),f.set("useRoughnessMap",A),f.set("doubleSide",C),y!=null&&f.set("uvRepeat",y),x!=null&&f.set("uvOffset",x),w!=null&&f.set("detailUvRepeat",w),T!=null&&f.set("detailUvOffset",T),f.set("roughness",p)):(v.setUniform(u,"1f","roughness",p),a!==_&&io(e,v,"normalMap",_,0),o!==g&&g&&io(e,v,"bumpMap",g,1),s!==m&&m&&io(e,v,"roughnessMap",m,2),y!=null&&v.setUniform(u,"2f","uvRepeat",y),x!=null&&v.setUniform(u,"2f","uvOffset",x),w!=null&&v.setUniform(u,"2f","detailUvRepeat",w),T!=null&&v.setUniform(u,"2f","detailUvOffset",T),v.setUniform(u,"1i","useBumpMap",+b),v.setUniform(u,"1i","useRoughnessMap",+A),v.setUniform(u,"1i","doubleSide",+C)),a=_,o=g,s=m,l=h}}}function Ei(e){this._depthTex=new ne({format:H.DEPTH_COMPONENT,type:H.UNSIGNED_INT}),this._normalTex=new ne({type:H.HALF_FLOAT}),this._framebuffer=new Ie,this._framebuffer.attach(this._normalTex),this._framebuffer.attach(this._depthTex,Ie.DEPTH_ATTACHMENT),this._normalMaterial=new At({shader:new k(k.source("ecgl.normal.vertex"),k.source("ecgl.normal.fragment"))}),this._normalMaterial.enableTexture(["normalMap","bumpMap","roughnessMap"]),this._defaultNormalMap=Ht.createBlank("#000"),this._defaultBumpMap=Ht.createBlank("#000"),this._defaultRoughessMap=Ht.createBlank("#000"),this._debugPass=new Oe({fragment:k.source("clay.compositor.output")}),this._debugPass.setUniform("texture",this._normalTex),this._debugPass.material.undefine("fragment","OUTPUT_ALPHA")}Ei.prototype.getDepthTexture=function(){return this._depthTex};Ei.prototype.getNormalTexture=function(){return this._normalTex};Ei.prototype.update=function(e,t,r){var i=e.getWidth(),n=e.getHeight(),a=this._depthTex,o=this._normalTex,s=this._normalMaterial;a.width=i,a.height=n,o.width=i,o.height=n;var l=t.getRenderList(r).opaque;this._framebuffer.bind(e),e.gl.clearColor(0,0,0,0),e.gl.clear(e.gl.COLOR_BUFFER_BIT|e.gl.DEPTH_BUFFER_BIT),e.gl.disable(e.gl.BLEND),e.renderPass(l,r,{getMaterial:function(){return s},ifRender:function(u){return u.renderNormal},beforeRender:d_(e,this._defaultNormalMap,this._defaultBumpMap,this._defaultRoughessMap,this._normalMaterial),sort:e.opaqueSortCompare}),this._framebuffer.unbind(e)};Ei.prototype.renderDebug=function(e){this._debugPass.render(e)};Ei.prototype.dispose=function(e){this._depthTex.dispose(e),this._normalTex.dispose(e)};function _n(e){e=e||{},this._edgePass=new Oe({fragment:k.source("ecgl.edge")}),this._edgePass.setUniform("normalTexture",e.normalTexture),this._edgePass.setUniform("depthTexture",e.depthTexture),this._targetTexture=new ne({type:H.HALF_FLOAT}),this._frameBuffer=new Ie,this._frameBuffer.attach(this._targetTexture)}_n.prototype.update=function(e,t,r,i){var n=e.getWidth(),a=e.getHeight(),o=this._targetTexture;o.width=n,o.height=a;var s=this._frameBuffer;s.bind(e),this._edgePass.setUniform("projectionInv",t.invProjectionMatrix.array),this._edgePass.setUniform("textureSize",[n,a]),this._edgePass.setUniform("texture",r),this._edgePass.render(e),s.unbind(e)};_n.prototype.getTargetTexture=function(){return this._targetTexture};_n.prototype.setParameter=function(e,t){this._edgePass.setUniform(e,t)};_n.prototype.dispose=function(e){this._targetTexture.dispose(e),this._frameBuffer.dispose(e)};const v_={nodes:[{name:"source",type:"texture",outputs:{color:{}}},{name:"source_half",shader:"#source(clay.compositor.downsample)",inputs:{texture:"source"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 2)",height:"expr(height * 1.0 / 2)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0, height * 1.0] )"}},{name:"bright",shader:"#source(clay.compositor.bright)",inputs:{texture:"source_half"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 2)",height:"expr(height * 1.0 / 2)",type:"HALF_FLOAT"}}},parameters:{threshold:2,scale:4,textureSize:"expr([width * 1.0 / 2, height / 2])"}},{name:"bright_downsample_4",shader:"#source(clay.compositor.downsample)",inputs:{texture:"bright"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 4)",height:"expr(height * 1.0 / 4)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0 / 2, height / 2] )"}},{name:"bright_downsample_8",shader:"#source(clay.compositor.downsample)",inputs:{texture:"bright_downsample_4"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 8)",height:"expr(height * 1.0 / 8)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0 / 4, height / 4] )"}},{name:"bright_downsample_16",shader:"#source(clay.compositor.downsample)",inputs:{texture:"bright_downsample_8"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 16)",height:"expr(height * 1.0 / 16)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0 / 8, height / 8] )"}},{name:"bright_downsample_32",shader:"#source(clay.compositor.downsample)",inputs:{texture:"bright_downsample_16"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 32)",height:"expr(height * 1.0 / 32)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0 / 16, height / 16] )"}},{name:"bright_upsample_16_blur_h",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_downsample_32"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 16)",height:"expr(height * 1.0 / 16)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:0,textureSize:"expr( [width * 1.0 / 32, height / 32] )"}},{name:"bright_upsample_16_blur_v",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_upsample_16_blur_h"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 16)",height:"expr(height * 1.0 / 16)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:1,textureSize:"expr( [width * 1.0 / 16, height * 1.0 / 16] )"}},{name:"bright_upsample_8_blur_h",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_downsample_16"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 8)",height:"expr(height * 1.0 / 8)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:0,textureSize:"expr( [width * 1.0 / 16, height * 1.0 / 16] )"}},{name:"bright_upsample_8_blur_v",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_upsample_8_blur_h"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 8)",height:"expr(height * 1.0 / 8)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:1,textureSize:"expr( [width * 1.0 / 8, height * 1.0 / 8] )"}},{name:"bright_upsample_8_blend",shader:"#source(clay.compositor.blend)",inputs:{texture1:"bright_upsample_8_blur_v",texture2:"bright_upsample_16_blur_v"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 8)",height:"expr(height * 1.0 / 8)",type:"HALF_FLOAT"}}},parameters:{weight1:.3,weight2:.7}},{name:"bright_upsample_4_blur_h",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_downsample_8"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 4)",height:"expr(height * 1.0 / 4)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:0,textureSize:"expr( [width * 1.0 / 8, height * 1.0 / 8] )"}},{name:"bright_upsample_4_blur_v",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_upsample_4_blur_h"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 4)",height:"expr(height * 1.0 / 4)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:1,textureSize:"expr( [width * 1.0 / 4, height * 1.0 / 4] )"}},{name:"bright_upsample_4_blend",shader:"#source(clay.compositor.blend)",inputs:{texture1:"bright_upsample_4_blur_v",texture2:"bright_upsample_8_blend"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 4)",height:"expr(height * 1.0 / 4)",type:"HALF_FLOAT"}}},parameters:{weight1:.3,weight2:.7}},{name:"bright_upsample_2_blur_h",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_downsample_4"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 2)",height:"expr(height * 1.0 / 2)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:0,textureSize:"expr( [width * 1.0 / 4, height * 1.0 / 4] )"}},{name:"bright_upsample_2_blur_v",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_upsample_2_blur_h"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 2)",height:"expr(height * 1.0 / 2)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:1,textureSize:"expr( [width * 1.0 / 2, height * 1.0 / 2] )"}},{name:"bright_upsample_2_blend",shader:"#source(clay.compositor.blend)",inputs:{texture1:"bright_upsample_2_blur_v",texture2:"bright_upsample_4_blend"},outputs:{color:{parameters:{width:"expr(width * 1.0 / 2)",height:"expr(height * 1.0 / 2)",type:"HALF_FLOAT"}}},parameters:{weight1:.3,weight2:.7}},{name:"bright_upsample_full_blur_h",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:0,textureSize:"expr( [width * 1.0 / 2, height * 1.0 / 2] )"}},{name:"bright_upsample_full_blur_v",shader:"#source(clay.compositor.gaussian_blur)",inputs:{texture:"bright_upsample_full_blur_h"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}},parameters:{blurSize:1,blurDir:1,textureSize:"expr( [width * 1.0, height * 1.0] )"}},{name:"bloom_composite",shader:"#source(clay.compositor.blend)",inputs:{texture1:"bright_upsample_full_blur_v",texture2:"bright_upsample_2_blend"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}},parameters:{weight1:.3,weight2:.7}},{name:"coc",shader:"#source(ecgl.dof.coc)",outputs:{color:{parameters:{minFilter:"NEAREST",magFilter:"NEAREST",width:"expr(width * 1.0)",height:"expr(height * 1.0)"}}},parameters:{focalDist:50,focalRange:30}},{name:"dof_far_blur",shader:"#source(ecgl.dof.diskBlur)",inputs:{texture:"source",coc:"coc"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0, height * 1.0] )"}},{name:"dof_near_blur",shader:"#source(ecgl.dof.diskBlur)",inputs:{texture:"source",coc:"coc"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}},parameters:{textureSize:"expr( [width * 1.0, height * 1.0] )"},defines:{BLUR_NEARFIELD:null}},{name:"dof_coc_blur",shader:"#source(ecgl.dof.diskBlur)",inputs:{texture:"coc"},outputs:{color:{parameters:{minFilter:"NEAREST",magFilter:"NEAREST",width:"expr(width * 1.0)",height:"expr(height * 1.0)"}}},parameters:{textureSize:"expr( [width * 1.0, height * 1.0] )"},defines:{BLUR_COC:null}},{name:"dof_composite",shader:"#source(ecgl.dof.composite)",inputs:{original:"source",blurred:"dof_far_blur",nearfield:"dof_near_blur",coc:"coc",nearcoc:"dof_coc_blur"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)",type:"HALF_FLOAT"}}}},{name:"composite",shader:"#source(clay.compositor.hdr.composite)",inputs:{texture:"source",bloom:"bloom_composite"},outputs:{color:{parameters:{width:"expr(width * 1.0)",height:"expr(height * 1.0)"}}},defines:{}},{name:"FXAA",shader:"#source(clay.compositor.fxaa)",inputs:{texture:"composite"}}]},p_=`@export ecgl.dof.coc

uniform sampler2D depth;

uniform float zNear: 0.1;
uniform float zFar: 2000;

uniform float focalDistance: 3;
uniform float focalRange: 1;
uniform float focalLength: 30;
uniform float fstop: 2.8;

varying vec2 v_Texcoord;

@import clay.util.encode_float

void main()
{
 float z = texture2D(depth, v_Texcoord).r * 2.0 - 1.0;

 float dist = 2.0 * zNear * zFar / (zFar + zNear - z * (zFar - zNear));

 float aperture = focalLength / fstop;

 float coc;

 float uppper = focalDistance + focalRange;
 float lower = focalDistance - focalRange;
 if (dist <= uppper && dist >= lower) {
 coc = 0.5;
 }
 else {
 float focalAdjusted = dist > uppper ? uppper : lower;

 coc = abs(aperture * (focalLength * (dist - focalAdjusted)) / (dist * (focalAdjusted - focalLength)));
 coc = clamp(coc, 0.0, 2.0) / 2.00001;

 if (dist < lower) {
 coc = -coc;
 }
 coc = coc * 0.5 + 0.5;
 }

 gl_FragColor = encodeFloat(coc);
}
@end


@export ecgl.dof.composite

#define DEBUG 0

uniform sampler2D original;
uniform sampler2D blurred;
uniform sampler2D nearfield;
uniform sampler2D coc;
uniform sampler2D nearcoc;
varying vec2 v_Texcoord;

@import clay.util.rgbm
@import clay.util.float

void main()
{
 vec4 blurredColor = texture2D(blurred, v_Texcoord);
 vec4 originalColor = texture2D(original, v_Texcoord);

 float fCoc = decodeFloat(texture2D(coc, v_Texcoord));

 fCoc = abs(fCoc * 2.0 - 1.0);

 float weight = smoothstep(0.0, 1.0, fCoc);
 
#ifdef NEARFIELD_ENABLED
 vec4 nearfieldColor = texture2D(nearfield, v_Texcoord);
 float fNearCoc = decodeFloat(texture2D(nearcoc, v_Texcoord));
 fNearCoc = abs(fNearCoc * 2.0 - 1.0);

 gl_FragColor = encodeHDR(
 mix(
 nearfieldColor, mix(originalColor, blurredColor, weight),
 pow(1.0 - fNearCoc, 4.0)
 )
 );
#else
 gl_FragColor = encodeHDR(mix(originalColor, blurredColor, weight));
#endif

}

@end



@export ecgl.dof.diskBlur

#define POISSON_KERNEL_SIZE 16;

uniform sampler2D texture;
uniform sampler2D coc;
varying vec2 v_Texcoord;

uniform float blurRadius : 10.0;
uniform vec2 textureSize : [512.0, 512.0];

uniform vec2 poissonKernel[POISSON_KERNEL_SIZE];

uniform float percent;

float nrand(const in vec2 n) {
 return fract(sin(dot(n.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

@import clay.util.rgbm
@import clay.util.float


void main()
{
 vec2 offset = blurRadius / textureSize;

 float rnd = 6.28318 * nrand(v_Texcoord + 0.07 * percent );
 float cosa = cos(rnd);
 float sina = sin(rnd);
 vec4 basis = vec4(cosa, -sina, sina, cosa);

#if !defined(BLUR_NEARFIELD) && !defined(BLUR_COC)
 offset *= abs(decodeFloat(texture2D(coc, v_Texcoord)) * 2.0 - 1.0);
#endif

#ifdef BLUR_COC
 float cocSum = 0.0;
#else
 vec4 color = vec4(0.0);
#endif


 float weightSum = 0.0;

 for (int i = 0; i < POISSON_KERNEL_SIZE; i++) {
 vec2 ofs = poissonKernel[i];

 ofs = vec2(dot(ofs, basis.xy), dot(ofs, basis.zw));

 vec2 uv = v_Texcoord + ofs * offset;
 vec4 texel = texture2D(texture, uv);

 float w = 1.0;
#ifdef BLUR_COC
 float fCoc = decodeFloat(texel) * 2.0 - 1.0;
 cocSum += clamp(fCoc, -1.0, 0.0) * w;
#else
 texel = texel;
 #if !defined(BLUR_NEARFIELD)
 float fCoc = decodeFloat(texture2D(coc, uv)) * 2.0 - 1.0;
 w *= abs(fCoc);
 #endif
 texel.rgb *= texel.a;
 color += texel * w;
#endif

 weightSum += w;
 }

#ifdef BLUR_COC
 gl_FragColor = encodeFloat(clamp(cocSum / weightSum, -1.0, 0.0) * 0.5 + 0.5);
#else
 color /= weightSum;
 color.rgb /= (color.a + 0.0001);
 gl_FragColor = color;
#endif
}

@end`,g_=`@export ecgl.edge

uniform sampler2D texture;

uniform sampler2D normalTexture;
uniform sampler2D depthTexture;

uniform mat4 projectionInv;

uniform vec2 textureSize;

uniform vec4 edgeColor: [0,0,0,0.8];

varying vec2 v_Texcoord;

vec3 packColor(vec2 coord) {
 float z = texture2D(depthTexture, coord).r * 2.0 - 1.0;
 vec4 p = vec4(v_Texcoord * 2.0 - 1.0, z, 1.0);
 vec4 p4 = projectionInv * p;

 return vec3(
 texture2D(normalTexture, coord).rg,
 -p4.z / p4.w / 5.0
 );
}

void main() {
 vec2 cc = v_Texcoord;
 vec3 center = packColor(cc);

 float size = clamp(1.0 - (center.z - 10.0) / 100.0, 0.0, 1.0) * 0.5;
 float dx = size / textureSize.x;
 float dy = size / textureSize.y;

 vec2 coord;
 vec3 topLeft = packColor(cc+vec2(-dx, -dy));
 vec3 top = packColor(cc+vec2(0.0, -dy));
 vec3 topRight = packColor(cc+vec2(dx, -dy));
 vec3 left = packColor(cc+vec2(-dx, 0.0));
 vec3 right = packColor(cc+vec2(dx, 0.0));
 vec3 bottomLeft = packColor(cc+vec2(-dx, dy));
 vec3 bottom = packColor(cc+vec2(0.0, dy));
 vec3 bottomRight = packColor(cc+vec2(dx, dy));

 vec3 v = -topLeft-2.0*top-topRight+bottomLeft+2.0*bottom+bottomRight;
 vec3 h = -bottomLeft-2.0*left-topLeft+bottomRight+2.0*right+topRight;

 float edge = sqrt(dot(h, h) + dot(v, v));

 edge = smoothstep(0.8, 1.0, edge);

 gl_FragColor = mix(texture2D(texture, v_Texcoord), vec4(edgeColor.rgb, 1.0), edgeColor.a * edge);
}
@end`;k.import(nf);k.import(af);k.import(of);k.import(sf);k.import(lf);k.import(uf);k.import(hf);k.import(ff);k.import(cf);k.import(p_);k.import(g_);function pf(e,t){return{color:{parameters:{width:e,height:t}}}}var ss=["composite","FXAA"];function ue(){this._width,this._height,this._dpr,this._sourceTexture=new ne({type:H.HALF_FLOAT}),this._depthTexture=new ne({format:H.DEPTH_COMPONENT,type:H.UNSIGNED_INT}),this._framebuffer=new Ie,this._framebuffer.attach(this._sourceTexture),this._framebuffer.attach(this._depthTexture,Ie.DEPTH_ATTACHMENT),this._normalPass=new Ei,this._compositor=r_(v_);var e=this._compositor.getNodeByName("source");e.texture=this._sourceTexture;var t=this._compositor.getNodeByName("coc");this._sourceNode=e,this._cocNode=t,this._compositeNode=this._compositor.getNodeByName("composite"),this._fxaaNode=this._compositor.getNodeByName("FXAA"),this._dofBlurNodes=["dof_far_blur","dof_near_blur","dof_coc_blur"].map(function(i){return this._compositor.getNodeByName(i)},this),this._dofBlurKernel=0,this._dofBlurKernelSize=new Float32Array(0),this._finalNodesChain=ss.map(function(i){return this._compositor.getNodeByName(i)},this);var r={normalTexture:this._normalPass.getNormalTexture(),depthTexture:this._normalPass.getDepthTexture()};this._ssaoPass=new er(r),this._ssrPass=new tr(r),this._edgePass=new _n(r)}ue.prototype.resize=function(i,n,r){r=r||1;var i=i*r,n=n*r,a=this._sourceTexture,o=this._depthTexture;a.width=i,a.height=n,o.width=i,o.height=n;var s={getWidth:function(){return i},getHeight:function(){return n},getDevicePixelRatio:function(){return r}};function l(u,h){if(typeof u[h]=="function"){var f=u[h].__original||u[h];u[h]=function(d){return f.call(this,s)},u[h].__original=f}}this._compositor.nodes.forEach(function(u){for(var h in u.outputs){var f=u.outputs[h].parameters;f&&(l(f,"width"),l(f,"height"))}for(var d in u.parameters)l(u.parameters,d)}),this._width=i,this._height=n,this._dpr=r};ue.prototype.getWidth=function(){return this._width};ue.prototype.getHeight=function(){return this._height};ue.prototype._ifRenderNormalPass=function(){return this._enableSSAO||this._enableEdge||this._enableSSR};ue.prototype._getPrevNode=function(e){for(var t=ss.indexOf(e.name)-1,r=this._finalNodesChain[t];r&&!this._compositor.getNodeByName(r.name);)t-=1,r=this._finalNodesChain[t];return r};ue.prototype._getNextNode=function(e){for(var t=ss.indexOf(e.name)+1,r=this._finalNodesChain[t];r&&!this._compositor.getNodeByName(r.name);)t+=1,r=this._finalNodesChain[t];return r};ue.prototype._addChainNode=function(e){var t=this._getPrevNode(e),r=this._getNextNode(e);t&&(e.inputs.texture=t.name,r?(e.outputs=pf(this.getWidth.bind(this),this.getHeight.bind(this)),r.inputs.texture=e.name):e.outputs=null,this._compositor.addNode(e))};ue.prototype._removeChainNode=function(e){var t=this._getPrevNode(e),r=this._getNextNode(e);t&&(r?(t.outputs=pf(this.getWidth.bind(this),this.getHeight.bind(this)),r.inputs.texture=t.name):t.outputs=null,this._compositor.removeNode(e))};ue.prototype.updateNormal=function(e,t,r,i){this._ifRenderNormalPass()&&this._normalPass.update(e,t,r)};ue.prototype.updateSSAO=function(e,t,r,i){this._ssaoPass.update(e,r,i)};ue.prototype.enableSSAO=function(){this._enableSSAO=!0};ue.prototype.disableSSAO=function(){this._enableSSAO=!1};ue.prototype.enableSSR=function(){this._enableSSR=!0};ue.prototype.disableSSR=function(){this._enableSSR=!1};ue.prototype.getSSAOTexture=function(){return this._ssaoPass.getTargetTexture()};ue.prototype.getSourceFrameBuffer=function(){return this._framebuffer};ue.prototype.getSourceTexture=function(){return this._sourceTexture};ue.prototype.disableFXAA=function(){this._removeChainNode(this._fxaaNode)};ue.prototype.enableFXAA=function(){this._addChainNode(this._fxaaNode)};ue.prototype.enableBloom=function(){this._compositeNode.inputs.bloom="bloom_composite",this._compositor.dirty()};ue.prototype.disableBloom=function(){this._compositeNode.inputs.bloom=null,this._compositor.dirty()};ue.prototype.enableDOF=function(){this._compositeNode.inputs.texture="dof_composite",this._compositor.dirty()};ue.prototype.disableDOF=function(){this._compositeNode.inputs.texture="source",this._compositor.dirty()};ue.prototype.enableColorCorrection=function(){this._compositeNode.define("COLOR_CORRECTION"),this._enableColorCorrection=!0};ue.prototype.disableColorCorrection=function(){this._compositeNode.undefine("COLOR_CORRECTION"),this._enableColorCorrection=!1};ue.prototype.enableEdge=function(){this._enableEdge=!0};ue.prototype.disableEdge=function(){this._enableEdge=!1};ue.prototype.setBloomIntensity=function(e){this._compositeNode.setParameter("bloomIntensity",e)};ue.prototype.setSSAOParameter=function(e,t){switch(e){case"quality":var r={low:6,medium:12,high:32,ultra:62}[t]||12;this._ssaoPass.setParameter("kernelSize",r);break;case"radius":this._ssaoPass.setParameter(e,t),this._ssaoPass.setParameter("bias",t/200);break;case"intensity":this._ssaoPass.setParameter(e,t);break}};ue.prototype.setDOFParameter=function(e,t){switch(e){case"focalDistance":case"focalRange":case"fstop":this._cocNode.setParameter(e,t);break;case"blurRadius":for(var r=0;r<this._dofBlurNodes.length;r++)this._dofBlurNodes[r].setParameter("blurRadius",t);break;case"quality":var i={low:4,medium:8,high:16,ultra:32}[t]||8;this._dofBlurKernelSize=i;for(var r=0;r<this._dofBlurNodes.length;r++)this._dofBlurNodes[r].pass.material.define("POISSON_KERNEL_SIZE",i);this._dofBlurKernel=new Float32Array(i*2);break}};ue.prototype.setSSRParameter=function(e,t){if(t!=null)switch(e){case"quality":var r={low:10,medium:15,high:30,ultra:80}[t]||20,i={low:32,medium:16,high:8,ultra:4}[t]||16;this._ssrPass.setParameter("maxIteration",r),this._ssrPass.setParameter("pixelStride",i);break;case"maxRoughness":this._ssrPass.setParameter("minGlossiness",Math.max(Math.min(1-t,1),0));break;case"physical":this.setPhysicallyCorrectSSR(t);break;default:console.warn("Unkown SSR parameter "+e)}};ue.prototype.setPhysicallyCorrectSSR=function(e){this._ssrPass.setPhysicallyCorrect(e)};ue.prototype.setEdgeColor=function(e){var t=S.parseColor(e);this._edgePass.setParameter("edgeColor",t)};ue.prototype.setExposure=function(e){this._compositeNode.setParameter("exposure",Math.pow(2,e))};ue.prototype.setColorLookupTexture=function(e,t){this._compositeNode.pass.material.setTextureImage("lut",this._enableColorCorrection?e:"none",t,{minFilter:S.Texture.NEAREST,magFilter:S.Texture.NEAREST,flipY:!1})};ue.prototype.setColorCorrection=function(e,t){this._compositeNode.setParameter(e,t)};ue.prototype.isSSREnabled=function(){return this._enableSSR};ue.prototype.composite=function(e,t,r,i,n){var a=this._sourceTexture,o=a;this._enableEdge&&(this._edgePass.update(e,r,a,n),a=o=this._edgePass.getTargetTexture()),this._enableSSR&&(this._ssrPass.update(e,r,a,n),o=this._ssrPass.getTargetTexture(),this._ssrPass.setSSAOTexture(this._enableSSAO?this._ssaoPass.getTargetTexture():null)),this._sourceNode.texture=o,this._cocNode.setParameter("depth",this._depthTexture);for(var s=this._dofBlurKernel,l=this._dofBlurKernelSize,u=Math.floor(mu.length/2/l),h=n%u,f=0;f<l*2;f++)s[f]=mu[f+h*l*2];for(var f=0;f<this._dofBlurNodes.length;f++)this._dofBlurNodes[f].setParameter("percent",n/30),this._dofBlurNodes[f].setParameter("poissonKernel",s);this._cocNode.setParameter("zNear",r.near),this._cocNode.setParameter("zFar",r.far),this._compositor.render(e,i)};ue.prototype.dispose=function(e){this._sourceTexture.dispose(e),this._depthTexture.dispose(e),this._framebuffer.dispose(e),this._compositor.dispose(e),this._normalPass.dispose(e),this._ssaoPass.dispose(e)};function Do(e){for(var t=[],r=0;r<30;r++)t.push([yi(r,2),yi(r,3)]);this._haltonSequence=t,this._frame=0,this._sourceTex=new ne,this._sourceFb=new Ie,this._sourceFb.attach(this._sourceTex),this._prevFrameTex=new ne,this._outputTex=new ne;var i=this._blendPass=new Oe({fragment:k.source("clay.compositor.blend")});i.material.disableTexturesAll(),i.material.enableTexture(["texture1","texture2"]),this._blendFb=new Ie({depthBuffer:!1}),this._outputPass=new Oe({fragment:k.source("clay.compositor.output"),blendWithPrevious:!0}),this._outputPass.material.define("fragment","OUTPUT_ALPHA"),this._outputPass.material.blend=function(n){n.blendEquationSeparate(n.FUNC_ADD,n.FUNC_ADD),n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA)}}Do.prototype={constructor:Do,jitterProjection:function(e,t){var r=e.viewport,i=r.devicePixelRatio||e.getDevicePixelRatio(),n=r.width*i,a=r.height*i,o=this._haltonSequence[this._frame%this._haltonSequence.length],s=new W;s.array[12]=(o[0]*2-1)/n,s.array[13]=(o[1]*2-1)/a,W.mul(t.projectionMatrix,s,t.projectionMatrix),W.invert(t.invProjectionMatrix,t.projectionMatrix)},resetFrame:function(){this._frame=0},getFrame:function(){return this._frame},getSourceFrameBuffer:function(){return this._sourceFb},getOutputTexture:function(){return this._outputTex},resize:function(e,t){this._prevFrameTex.width=e,this._prevFrameTex.height=t,this._outputTex.width=e,this._outputTex.height=t,this._sourceTex.width=e,this._sourceTex.height=t,this._prevFrameTex.dirty(),this._outputTex.dirty(),this._sourceTex.dirty()},isFinished:function(){return this._frame>=this._haltonSequence.length},render:function(e,t,r){var i=this._blendPass;this._frame===0?(i.setUniform("weight1",0),i.setUniform("weight2",1)):(i.setUniform("weight1",.9),i.setUniform("weight2",.1)),i.setUniform("texture1",this._prevFrameTex),i.setUniform("texture2",t||this._sourceTex),this._blendFb.attach(this._outputTex),this._blendFb.bind(e),i.render(e),this._blendFb.unbind(e),r||(this._outputPass.setUniform("texture",this._outputTex),this._outputPass.render(e));var n=this._prevFrameTex;this._prevFrameTex=this._outputTex,this._outputTex=n,this._frame++},dispose:function(e){this._sourceFb.dispose(e),this._blendFb.dispose(e),this._prevFrameTex.dispose(e),this._outputTex.dispose(e),this._sourceTex.dispose(e),this._outputPass.dispose(e),this._blendPass.dispose(e)}};function ge(e){e=e||"perspective",this.layer=null,this.scene=new _r,this.rootNode=this.scene,this.viewport={x:0,y:0,width:0,height:0},this.setProjection(e),this._compositor=new ue,this._temporalSS=new Do,this._shadowMapPass=new zt;for(var t=[],r=0,i=0;i<30;i++){for(var n=[],a=0;a<6;a++)n.push(yi(r,2)*4-2),n.push(yi(r,3)*4-2),r++;t.push(n)}this._pcfKernels=t,this.scene.on("beforerender",function(o,s,l){this.needsTemporalSS()&&this._temporalSS.jitterProjection(o,l)},this)}ge.prototype.setProjection=function(e){var t=this.camera;t&&t.update(),e==="perspective"?this.camera instanceof We||(this.camera=new We,t&&this.camera.setLocalTransform(t.localTransform)):this.camera instanceof _i||(this.camera=new _i,t&&this.camera.setLocalTransform(t.localTransform)),this.camera.near=.1,this.camera.far=2e3};ge.prototype.setViewport=function(e,t,r,i,n){this.camera instanceof We&&(this.camera.aspect=r/i),n=n||1,this.viewport.x=e,this.viewport.y=t,this.viewport.width=r,this.viewport.height=i,this.viewport.devicePixelRatio=n,this._compositor.resize(r*n,i*n),this._temporalSS.resize(r*n,i*n)};ge.prototype.containPoint=function(e,t){var r=this.viewport,i=this.layer.renderer.getHeight();return t=i-t,e>=r.x&&t>=r.y&&e<=r.x+r.width&&t<=r.y+r.height};var _u=new te;ge.prototype.castRay=function(e,t,r){var i=this.layer.renderer,n=i.viewport;return i.viewport=this.viewport,i.screenToNDC(e,t,_u),this.camera.castRay(_u,r),i.viewport=n,r};ge.prototype.prepareRender=function(){this.scene.update(),this.camera.update(),this.scene.updateLights();var e=this.scene.updateRenderList(this.camera);this._needsSortProgressively=!1;for(var t=0;t<e.transparent.length;t++){var r=e.transparent[t],i=r.geometry;i.needsSortVerticesProgressively&&i.needsSortVerticesProgressively()&&(this._needsSortProgressively=!0),i.needsSortTrianglesProgressively&&i.needsSortTrianglesProgressively()&&(this._needsSortProgressively=!0)}this._frame=0,this._temporalSS.resetFrame()};ge.prototype.render=function(e,t){this._doRender(e,t,this._frame),this._frame++};ge.prototype.needsAccumulate=function(){return this.needsTemporalSS()||this._needsSortProgressively};ge.prototype.needsTemporalSS=function(){var e=this._enableTemporalSS;return e==="auto"&&(e=this._enablePostEffect),e};ge.prototype.hasDOF=function(){return this._enableDOF};ge.prototype.isAccumulateFinished=function(){return this.needsTemporalSS()?this._temporalSS.isFinished():this._frame>30};ge.prototype._doRender=function(e,t,r){var i=this.scene,n=this.camera;r=r||0,this._updateTransparent(e,i,n,r),t||(this._shadowMapPass.kernelPCF=this._pcfKernels[0],this._shadowMapPass.render(e,i,n,!0)),this._updateShadowPCFKernel(r);var a=e.clearColor;if(e.gl.clearColor(a[0],a[1],a[2],a[3]),this._enablePostEffect&&(this.needsTemporalSS()&&this._temporalSS.jitterProjection(e,n),this._compositor.updateNormal(e,i,n,this._temporalSS.getFrame())),this._updateSSAO(e,i,n,this._temporalSS.getFrame()),this._enablePostEffect){var o=this._compositor.getSourceFrameBuffer();o.bind(e),e.gl.clear(e.gl.DEPTH_BUFFER_BIT|e.gl.COLOR_BUFFER_BIT),e.render(i,n,!0,!0),o.unbind(e),this.needsTemporalSS()&&t?(this._compositor.composite(e,i,n,this._temporalSS.getSourceFrameBuffer(),this._temporalSS.getFrame()),e.setViewport(this.viewport),this._temporalSS.render(e)):(e.setViewport(this.viewport),this._compositor.composite(e,i,n,null,0))}else if(this.needsTemporalSS()&&t){var o=this._temporalSS.getSourceFrameBuffer();o.bind(e),e.saveClear(),e.clearBit=e.gl.DEPTH_BUFFER_BIT|e.gl.COLOR_BUFFER_BIT,e.render(i,n,!0,!0),e.restoreClear(),o.unbind(e),e.setViewport(this.viewport),this._temporalSS.render(e)}else e.setViewport(this.viewport),e.render(i,n,!0,!0)};ge.prototype._updateTransparent=function(e,t,r,i){for(var n=new R,a=new W,o=r.getWorldPosition(),s=t.getRenderList(r).transparent,l=0;l<s.length;l++){var u=s[l],h=u.geometry;W.invert(a,u.worldTransform),R.transformMat4(n,o,a),h.needsSortTriangles&&h.needsSortTriangles()&&h.doSortTriangles(n,i),h.needsSortVertices&&h.needsSortVertices()&&h.doSortVertices(n,i)}};ge.prototype._updateSSAO=function(e,t,r){var i=this._enableSSAO&&this._enablePostEffect;i&&this._compositor.updateSSAO(e,t,r,this._temporalSS.getFrame());for(var n=t.getRenderList(r),a=0;a<n.opaque.length;a++){var o=n.opaque[a];o.renderNormal&&o.material[i?"enableTexture":"disableTexture"]("ssaoMap"),i&&o.material.set("ssaoMap",this._compositor.getSSAOTexture())}};ge.prototype._updateShadowPCFKernel=function(e){for(var t=this._pcfKernels[e%this._pcfKernels.length],r=this.scene.getRenderList(this.camera),i=r.opaque,n=0;n<i.length;n++)i[n].receiveShadow&&(i[n].material.set("pcfKernel",t),i[n].material.define("fragment","PCF_KERNEL_SIZE",t.length/2))};ge.prototype.dispose=function(e){this._compositor.dispose(e.gl),this._temporalSS.dispose(e.gl),this._shadowMapPass.dispose(e)};ge.prototype.setPostEffect=function(e,t){var r=this._compositor;this._enablePostEffect=e.get("enable");var i=e.getModel("bloom"),n=e.getModel("edge"),a=e.getModel("DOF",e.getModel("depthOfField")),o=e.getModel("SSAO",e.getModel("screenSpaceAmbientOcclusion")),s=e.getModel("SSR",e.getModel("screenSpaceReflection")),l=e.getModel("FXAA"),u=e.getModel("colorCorrection");i.get("enable")?r.enableBloom():r.disableBloom(),a.get("enable")?r.enableDOF():r.disableDOF(),s.get("enable")?r.enableSSR():r.disableSSR(),u.get("enable")?r.enableColorCorrection():r.disableColorCorrection(),n.get("enable")?r.enableEdge():r.disableEdge(),l.get("enable")?r.enableFXAA():r.disableFXAA(),this._enableDOF=a.get("enable"),this._enableSSAO=o.get("enable"),this._enableSSAO?r.enableSSAO():r.disableSSAO(),r.setBloomIntensity(i.get("intensity")),r.setEdgeColor(n.get("color")),r.setColorLookupTexture(u.get("lookupTexture"),t),r.setExposure(u.get("exposure")),["radius","quality","intensity"].forEach(function(h){r.setSSAOParameter(h,o.get(h))}),["quality","maxRoughness","physical"].forEach(function(h){r.setSSRParameter(h,s.get(h))}),["quality","focalDistance","focalRange","blurRadius","fstop"].forEach(function(h){r.setDOFParameter(h,a.get(h))}),["brightness","contrast","saturation"].forEach(function(h){r.setColorCorrection(h,u.get(h))})};ge.prototype.setDOFFocusOnPoint=function(e){if(this._enablePostEffect)return e>this.camera.far||e<this.camera.near?void 0:(this._compositor.setDOFParameter("focalDistance",e),!0)};ge.prototype.setTemporalSuperSampling=function(e){this._enableTemporalSS=e.get("enable")};ge.prototype.isLinearSpace=function(){return this._enablePostEffect};ge.prototype.setRootNode=function(e){if(this.rootNode!==e){for(var t=this.rootNode.children(),r=0;r<t.length;r++)e.add(t[r]);e!==this.scene&&this.scene.add(e),this.rootNode=e}};ge.prototype.add=function(e){this.rootNode.add(e)};ge.prototype.remove=function(e){this.rootNode.remove(e)};ge.prototype.removeAll=function(e){this.rootNode.removeAll(e)};Object.assign(ge.prototype,es);function m_(e,t){var r=e.getBoxLayoutParams(),i=dn(r,{width:t.getWidth(),height:t.getHeight()});i.y=t.getHeight()-i.y-i.height,this.viewGL.setViewport(i.x,i.y,i.width,i.height,t.getDevicePixelRatio());var n=e.get("boxWidth"),a=e.get("boxHeight"),o=e.get("boxDepth");this.getAxis("x").setExtent(-n/2,n/2),this.getAxis("y").setExtent(o/2,-o/2),this.getAxis("z").setExtent(-a/2,a/2),this.size=[n,a,o]}function __(e,t){var r={};function i(n,a){r[n]=r[n]||[1/0,-1/0],r[n][0]=Math.min(a[0],r[n][0]),r[n][1]=Math.max(a[1],r[n][1])}e.eachSeries(function(n){if(n.coordinateSystem===this){var a=n.getData();["x","y","z"].forEach(function(o){a.mapDimensionsAll(o,!0).forEach(function(s){i(o,a.getDataExtent(s,!0))})})}},this),["xAxis3D","yAxis3D","zAxis3D"].forEach(function(n){e.eachComponent(n,function(a){var o=n.charAt(0),s=a.getReferringComponents("grid3D").models[0],l=s.coordinateSystem;if(l===this){var u=l.getAxis(o);if(!u){var h=jo(r[o]||[1/0,-1/0],a);u=new ra(o,h),u.type=a.get("type");var f=u.type==="category";u.onBand=f&&a.get("boundaryGap"),u.inverse=a.get("inverse"),a.axis=u,u.model=a,u.getLabelModel=function(){return a.getModel("axisLabel",s.getModel("axisLabel"))},u.getTickModel=function(){return a.getModel("axisTick",s.getModel("axisTick"))},l.addAxis(u)}}},this)},this),this.resize(this.model,t)}var y_={dimensions:en.prototype.dimensions,create:function(e,t){var r=[];e.eachComponent("grid3D",function(a){a.__viewGL=a.__viewGL||new ge;var o=new en;o.model=a,o.viewGL=a.__viewGL,a.coordinateSystem=o,r.push(o),o.resize=m_,o.update=__});var i=["xAxis3D","yAxis3D","zAxis3D"];function n(a,o){return i.map(function(s){var l=a.getReferringComponents(s).models[0];return l==null&&(l=o.getComponent(s)),l})}return e.eachSeries(function(a){if(a.get("coordinateSystem")==="cartesian3D"){var o=a.getReferringComponents("grid3D").models[0];if(o==null){var s=n(a,e),o=s[0].getCoordSysModel();s.forEach(function(h){h.getCoordSysModel()})}var l=o.coordinateSystem;a.coordinateSystem=l}}),r}},gf=Rt.extend({type:"cartesian3DAxis",axis:null,getCoordSysModel:function(){return this.ecModel.queryComponents({mainType:"grid3D",index:this.option.gridIndex,id:this.option.gridId})[0]}});Od(gf);var mf={show:!0,grid3DIndex:0,inverse:!1,name:"",nameLocation:"middle",nameTextStyle:{fontSize:16},nameGap:20,axisPointer:{},axisLine:{},axisTick:{},axisLabel:{},splitArea:{}},x_=le({boundaryGap:!0,axisTick:{alignWithLabel:!1,interval:"auto"},axisLabel:{interval:"auto"},axisPointer:{label:{show:!1}}},mf),ls=le({boundaryGap:[0,0],splitNumber:5,axisPointer:{label:{}}},mf),T_=He({scale:!0,min:"dataMin",max:"dataMax"},ls),_f=He({logBase:10},ls);_f.scale=!0;const w_={categoryAxis3D:x_,valueAxis3D:ls,timeAxis3D:T_,logAxis3D:_f};var S_=["value","category","time","log"];function b_(e,t,r,i,n){S_.forEach(function(a){var o=r.extend({type:t+"Axis3D."+a,__ordinalMeta:null,mergeDefaultAndTheme:function(s,l){var u=l.getTheme();le(s,u.get(a+"Axis3D")),le(s,this.getDefaultOption()),s.type=i(t,s)},optionUpdated:function(){var s=this.option;s.type==="category"&&(this.__ordinalMeta=qu.createByAxisModel(this))},getCategories:function(){if(this.option.type==="category")return this.__ordinalMeta.categories},getOrdinalMeta:function(){return this.__ordinalMeta},defaultOption:le(Vo(w_[a+"Axis3D"]),n||{},!0)});e.registerComponentModel(o)}),e.registerSubTypeDefaulter(t+"Axis3D",ui(i,t))}function A_(e,t){return t.type||(t.data?"category":"value")}function E_(e){e.registerComponentModel(ma),e.registerComponentView(Hm),e.registerCoordinateSystem("grid3D",y_),["x","y","z"].forEach(function(t){b_(e,t,gf,A_,{name:t.toUpperCase()});const r=e.ComponentView.extend({type:t+"Axis3D"});e.registerComponentView(r)}),e.registerAction({type:"grid3DChangeCamera",event:"grid3dcamerachanged",update:"series:updateCamera"},function(t,r){r.eachComponent({mainType:"grid3D",query:t},function(i){i.setView(t)})}),e.registerAction({type:"grid3DShowAxisPointer",event:"grid3dshowaxispointer",update:"grid3D:showAxisPointer"},function(t,r){}),e.registerAction({type:"grid3DHideAxisPointer",event:"grid3dhideaxispointer",update:"grid3D:hideAxisPointer"},function(t,r){})}Ne(E_);const Li={defaultOption:{shading:null,realisticMaterial:{textureTiling:1,textureOffset:0,detailTexture:null},lambertMaterial:{textureTiling:1,textureOffset:0,detailTexture:null},colorMaterial:{textureTiling:1,textureOffset:0,detailTexture:null},hatchingMaterial:{textureTiling:1,textureOffset:0,paperColor:"#fff"}}},yf={getFilledRegions:function(e,t){var r=(e||[]).slice(),i;if(typeof t=="string"?(t=po(t),i=t&&t.geoJson):t&&t.features&&(i=t),!i)return[];for(var n={},a=i.features,o=0;o<r.length;o++)n[r[o].name]=r[o];for(var o=0;o<a.length;o++){var s=a[o].properties.name;n[s]||r.push({name:s})}return r},defaultOption:{show:!0,zlevel:-10,map:"",left:0,top:0,width:"100%",height:"100%",boxWidth:100,boxHeight:10,boxDepth:"auto",regionHeight:3,environment:"auto",groundPlane:{show:!1,color:"#aaa"},shading:"lambert",light:{main:{alpha:40,beta:30}},viewControl:{alpha:40,beta:0,distance:100,orthographicSize:60,minAlpha:5,minBeta:-80,maxBeta:80},label:{show:!1,distance:2,textStyle:{fontSize:20,color:"#000",backgroundColor:"rgba(255,255,255,0.7)",padding:3,borderRadius:4}},itemStyle:{color:"#fff",borderWidth:0,borderColor:"#333"},emphasis:{itemStyle:{color:"#639fc0"},label:{show:!0}}}};var Ci=Rt.extend({type:"geo3D",layoutMode:"box",coordinateSystem:null,optionUpdated:function(){var e=this.option;e.regions=this.getFilledRegions(e.regions,e.map);var t=vn(e.data||[],{coordDimensions:["value"],encodeDefine:this.get("encode"),dimensionsDefine:this.get("dimensions")}),r=new Nt(t,this);r.initData(e.regions);var i={};r.each(function(n){var a=r.getName(n),o=r.getItemModel(n);i[a]=o}),this._regionModelMap=i,this._data=r},getData:function(){return this._data},getRegionModel:function(e){var t=this.getData().getName(e);return this._regionModelMap[t]||new zr(null,this)},getRegionPolygonCoords:function(e){var t=this.getData().getName(e),r=this.coordinateSystem.getRegion(t);return r?r.geometries:[]},getFormattedLabel:function(e,t){var r=this._data.getName(e),i=this.getRegionModel(e),n=i.get(t==="normal"?["label","formatter"]:["emphasis","label","formatter"]);n==null&&(n=i.get(["label","formatter"]));var a={name:r};if(typeof n=="function")return a.status=t,n(a);if(typeof n=="string"){var o=a.seriesName;return n.replace("{a}",o??"")}else return r},defaultOption:{regions:[]}});le(Ci.prototype,yf);le(Ci.prototype,ga);le(Ci.prototype,bi);le(Ci.prototype,Ai);le(Ci.prototype,Li);function xf(e,t,r){r=r||2;var i=t&&t.length,n=i?t[0]*r:e.length,a=Tf(e,0,n,r,!0),o=[];if(!a)return o;var s,l,u,h,f,d,c;if(i&&(a=P_(e,t,a,r)),e.length>80*r){s=u=e[0],l=h=e[1];for(var v=r;v<n;v+=r)f=e[v],d=e[v+1],f<s&&(s=f),d<l&&(l=d),f>u&&(u=f),d>h&&(h=d);c=Math.max(u-s,h-l)}return nn(a,o,r,s,l,c),o}function Tf(e,t,r,i,n){var a,o;if(n===Io(e,t,r,i)>0)for(a=t;a<r;a+=i)o=yu(a,e[a],e[a+1],o);else for(a=r-i;a>=t;a-=i)o=yu(a,e[a],e[a+1],o);return o&&Or(o,o.next)&&(on(o),o=o.next),o}function rn(e,t){if(!e)return e;t||(t=e);var r=e,i;do if(i=!1,!r.steiner&&(Or(r,r.next)||ot(r.prev,r,r.next)===0)){if(on(r),r=t=r.prev,r===r.next)return null;i=!0}else r=r.next;while(i||r!==t);return t}function nn(e,t,r,i,n,a,o){if(e){!o&&a&&O_(e,i,n,a);for(var s=e,l,u;e.prev!==e.next;){if(l=e.prev,u=e.next,a?C_(e,i,n,a):L_(e)){t.push(l.i/r),t.push(e.i/r),t.push(u.i/r),on(e),e=u.next,s=u.next;continue}if(e=u,e===s){o?o===1?(e=M_(e,t,r),nn(e,t,r,i,n,a,2)):o===2&&D_(e,t,r,i,n,a):nn(rn(e),t,r,i,n,a,1);break}}}}function L_(e){var t=e.prev,r=e,i=e.next;if(ot(t,r,i)>=0)return!1;for(var n=e.next.next;n!==e.prev;){if(na(t.x,t.y,r.x,r.y,i.x,i.y,n.x,n.y)&&ot(n.prev,n,n.next)>=0)return!1;n=n.next}return!0}function C_(e,t,r,i){var n=e.prev,a=e,o=e.next;if(ot(n,a,o)>=0)return!1;for(var s=n.x<a.x?n.x<o.x?n.x:o.x:a.x<o.x?a.x:o.x,l=n.y<a.y?n.y<o.y?n.y:o.y:a.y<o.y?a.y:o.y,u=n.x>a.x?n.x>o.x?n.x:o.x:a.x>o.x?a.x:o.x,h=n.y>a.y?n.y>o.y?n.y:o.y:a.y>o.y?a.y:o.y,f=Po(s,l,t,r,i),d=Po(u,h,t,r,i),c=e.nextZ;c&&c.z<=d;){if(c!==e.prev&&c!==e.next&&na(n.x,n.y,a.x,a.y,o.x,o.y,c.x,c.y)&&ot(c.prev,c,c.next)>=0)return!1;c=c.nextZ}for(c=e.prevZ;c&&c.z>=f;){if(c!==e.prev&&c!==e.next&&na(n.x,n.y,a.x,a.y,o.x,o.y,c.x,c.y)&&ot(c.prev,c,c.next)>=0)return!1;c=c.prevZ}return!0}function M_(e,t,r){var i=e;do{var n=i.prev,a=i.next.next;!Or(n,a)&&wf(n,i,i.next,a)&&an(n,a)&&an(a,n)&&(t.push(n.i/r),t.push(i.i/r),t.push(a.i/r),on(i),on(i.next),i=e=a),i=i.next}while(i!==e);return i}function D_(e,t,r,i,n,a){var o=e;do{for(var s=o.next.next;s!==o.prev;){if(o.i!==s.i&&G_(o,s)){var l=Sf(o,s);o=rn(o,o.next),l=rn(l,l.next),nn(o,t,r,i,n,a),nn(l,t,r,i,n,a);return}s=s.next}o=o.next}while(o!==e)}function P_(e,t,r,i){var n=[],a,o,s,l,u;for(a=0,o=t.length;a<o;a++)s=t[a]*i,l=a<o-1?t[a+1]*i:e.length,u=Tf(e,s,l,i,!1),u===u.next&&(u.steiner=!0),n.push(F_(u));for(n.sort(N_),a=0;a<n.length;a++)I_(n[a],r),r=rn(r,r.next);return r}function N_(e,t){return e.x-t.x}function I_(e,t){if(t=R_(e,t),t){var r=Sf(t,e);rn(r,r.next)}}function R_(e,t){var r=t,i=e.x,n=e.y,a=-1/0,o;do{if(n<=r.y&&n>=r.next.y&&r.next.y!==r.y){var s=r.x+(n-r.y)*(r.next.x-r.x)/(r.next.y-r.y);if(s<=i&&s>a){if(a=s,s===i){if(n===r.y)return r;if(n===r.next.y)return r.next}o=r.x<r.next.x?r:r.next}}r=r.next}while(r!==t);if(!o)return null;if(i===a)return o.prev;var l=o,u=o.x,h=o.y,f=1/0,d;for(r=o.next;r!==l;)i>=r.x&&r.x>=u&&i!==r.x&&na(n<h?i:a,n,u,h,n<h?a:i,n,r.x,r.y)&&(d=Math.abs(n-r.y)/(i-r.x),(d<f||d===f&&r.x>o.x)&&an(r,e)&&(o=r,f=d)),r=r.next;return o}function O_(e,t,r,i){var n=e;do n.z===null&&(n.z=Po(n.x,n.y,t,r,i)),n.prevZ=n.prev,n.nextZ=n.next,n=n.next;while(n!==e);n.prevZ.nextZ=null,n.prevZ=null,B_(n)}function B_(e){var t,r,i,n,a,o,s,l,u=1;do{for(r=e,e=null,a=null,o=0;r;){for(o++,i=r,s=0,t=0;t<u&&(s++,i=i.nextZ,!!i);t++);for(l=u;s>0||l>0&&i;)s!==0&&(l===0||!i||r.z<=i.z)?(n=r,r=r.nextZ,s--):(n=i,i=i.nextZ,l--),a?a.nextZ=n:e=n,n.prevZ=a,a=n;r=i}a.nextZ=null,u*=2}while(o>1);return e}function Po(e,t,r,i,n){return e=32767*(e-r)/n,t=32767*(t-i)/n,e=(e|e<<8)&16711935,e=(e|e<<4)&252645135,e=(e|e<<2)&858993459,e=(e|e<<1)&1431655765,t=(t|t<<8)&16711935,t=(t|t<<4)&252645135,t=(t|t<<2)&858993459,t=(t|t<<1)&1431655765,e|t<<1}function F_(e){var t=e,r=e;do t.x<r.x&&(r=t),t=t.next;while(t!==e);return r}function na(e,t,r,i,n,a,o,s){return(n-o)*(t-s)-(e-o)*(a-s)>=0&&(e-o)*(i-s)-(r-o)*(t-s)>=0&&(r-o)*(a-s)-(n-o)*(i-s)>=0}function G_(e,t){return e.next.i!==t.i&&e.prev.i!==t.i&&!z_(e,t)&&an(e,t)&&an(t,e)&&U_(e,t)}function ot(e,t,r){return(t.y-e.y)*(r.x-t.x)-(t.x-e.x)*(r.y-t.y)}function Or(e,t){return e.x===t.x&&e.y===t.y}function wf(e,t,r,i){return Or(e,t)&&Or(r,i)||Or(e,i)&&Or(r,t)?!0:ot(e,t,r)>0!=ot(e,t,i)>0&&ot(r,i,e)>0!=ot(r,i,t)>0}function z_(e,t){var r=e;do{if(r.i!==e.i&&r.next.i!==e.i&&r.i!==t.i&&r.next.i!==t.i&&wf(r,r.next,e,t))return!0;r=r.next}while(r!==e);return!1}function an(e,t){return ot(e.prev,e,e.next)<0?ot(e,t,e.next)>=0&&ot(e,e.prev,t)>=0:ot(e,t,e.prev)<0||ot(e,e.next,t)<0}function U_(e,t){var r=e,i=!1,n=(e.x+t.x)/2,a=(e.y+t.y)/2;do r.y>a!=r.next.y>a&&r.next.y!==r.y&&n<(r.next.x-r.x)*(a-r.y)/(r.next.y-r.y)+r.x&&(i=!i),r=r.next;while(r!==e);return i}function Sf(e,t){var r=new No(e.i,e.x,e.y),i=new No(t.i,t.x,t.y),n=e.next,a=t.prev;return e.next=t,t.prev=e,r.next=n,n.prev=r,i.next=r,r.prev=i,a.next=i,i.prev=a,i}function yu(e,t,r,i){var n=new No(e,t,r);return i?(n.next=i.next,n.prev=i,i.next.prev=n,i.next=n):(n.prev=n,n.next=n),n}function on(e){e.next.prev=e.prev,e.prev.next=e.next,e.prevZ&&(e.prevZ.nextZ=e.nextZ),e.nextZ&&(e.nextZ.prevZ=e.prevZ)}function No(e,t,r){this.i=e,this.x=t,this.y=r,this.prev=null,this.next=null,this.z=null,this.prevZ=null,this.nextZ=null,this.steiner=!1}xf.deviation=function(e,t,r,i){var n=t&&t.length,a=n?t[0]*r:e.length,o=Math.abs(Io(e,0,a,r));if(n)for(var s=0,l=t.length;s<l;s++){var u=t[s]*r,h=s<l-1?t[s+1]*r:e.length;o-=Math.abs(Io(e,u,h,r))}var f=0;for(s=0;s<i.length;s+=3){var d=i[s]*r,c=i[s+1]*r,v=i[s+2]*r;f+=Math.abs((e[d]-e[v])*(e[c+1]-e[d+1])-(e[d]-e[c])*(e[v+1]-e[d+1]))}return o===0&&f===0?0:Math.abs((f-o)/o)};function Io(e,t,r,i){for(var n=0,a=t,o=r-i;a<r;a+=i)n+=(e[o]-e[a])*(e[a+1]+e[o+1]),o=a;return n}function no(e,t,r){var i=e[t];e[t]=e[r],e[r]=i}function bf(e,t,r,i,n){var a=r,o=e[t];no(e,t,i);for(var s=r;s<i;s++)n(e[s],o)<0&&(no(e,s,a),a++);return no(e,i,a),a}function aa(e,t,r,i){if(r<i){var n=Math.floor((r+i)/2),a=bf(e,n,r,i,t);aa(e,t,r,a-1),aa(e,t,a+1,i)}}function xi(){this._parts=[]}xi.prototype.step=function(e,t,r){var i=e.length;if(r===0){this._parts=[],this._sorted=!1;var n=Math.floor(i/2);this._parts.push({pivot:n,left:0,right:i-1}),this._currentSortPartIdx=0}if(!this._sorted){var a=this._parts;if(a.length===0)return this._sorted=!0,!0;if(a.length<512){for(var o=0;o<a.length;o++)a[o].pivot=bf(e,a[o].pivot,a[o].left,a[o].right,t);for(var s=[],o=0;o<a.length;o++){var l=a[o].left,u=a[o].pivot-1;u>l&&s.push({pivot:Math.floor((u+l)/2),left:l,right:u});var l=a[o].pivot+1,u=a[o].right;u>l&&s.push({pivot:Math.floor((u+l)/2),left:l,right:u})}a=this._parts=s}else for(var o=0;o<Math.floor(a.length/10);o++){var h=a.length-1-this._currentSortPartIdx;if(aa(e,t,a[h].left,a[h].right),this._currentSortPartIdx++,this._currentSortPartIdx===a.length)return this._sorted=!0,!0}return!1}};xi.sort=aa;var hi=Re.vec3,xu=hi.create(),Tu=hi.create(),wu=hi.create();const us={needsSortTriangles:function(){return this.indices&&this.sortTriangles},needsSortTrianglesProgressively:function(){return this.needsSortTriangles()&&this.triangleCount>=2e4},doSortTriangles:function(e,t){var r=this.indices;if(t===0){var i=this.attributes.position,e=e.array;(!this._triangleZList||this._triangleZList.length!==this.triangleCount)&&(this._triangleZList=new Float32Array(this.triangleCount),this._sortedTriangleIndices=new Uint32Array(this.triangleCount),this._indicesTmp=new r.constructor(r.length),this._triangleZListTmp=new Float32Array(this.triangleCount));for(var n=0,a,o=0;o<r.length;){i.get(r[o++],xu),i.get(r[o++],Tu),i.get(r[o++],wu);var s=hi.sqrDist(xu,e),l=hi.sqrDist(Tu,e),u=hi.sqrDist(wu,e),h=Math.min(s,l);h=Math.min(h,u),o===3?(a=h,h=0):h=h-a,this._triangleZList[n++]=h}}for(var f=this._sortedTriangleIndices,o=0;o<f.length;o++)f[o]=o;if(this.triangleCount<2e4)t===0&&this._simpleSort(!0);else for(var o=0;o<3;o++)this._progressiveQuickSort(t*3+o);for(var d=this._indicesTmp,c=this._triangleZListTmp,v=this._triangleZList,o=0;o<this.triangleCount;o++){var p=f[o]*3,_=o*3;d[_++]=r[p++],d[_++]=r[p++],d[_]=r[p],c[o]=v[f[o]]}var m=this._indicesTmp;this._indicesTmp=this.indices,this.indices=m;var m=this._triangleZListTmp;this._triangleZListTmp=this._triangleZList,this._triangleZList=m,this.dirtyIndices()},_simpleSort:function(e){var t=this._triangleZList,r=this._sortedTriangleIndices;function i(n,a){return t[a]-t[n]}e?Array.prototype.sort.call(r,i):xi.sort(r,i,0,r.length-1)},_progressiveQuickSort:function(e){var t=this._triangleZList,r=this._sortedTriangleIndices;this._quickSort=this._quickSort||new xi,this._quickSort.step(r,function(i,n){return t[n]-t[i]},e)}};function V_(e){const t=e.getVisual("style");if(t){const r=e.getVisual("drawType");return t[r]}}function H_(e){return e.getVisual("style").opacity}function Ze(e,t){const r=e.getItemVisual(t,"style");if(r){const i=e.getVisual("drawType");return r[i]}}function je(e,t){const r=e.getItemVisual(t,"style");return r&&r.opacity}var Af=1,Ef=2;function rr(e,t,r){this._labelsMesh=new ns,this._labelTextureSurface=new ta({width:512,height:512,devicePixelRatio:r.getDevicePixelRatio(),onupdate:function(){r.getZr().refresh()}}),this._api=r,this._labelsMesh.material.set("textureAtlas",this._labelTextureSurface.getTexture())}rr.prototype.getLabelPosition=function(e,t,r){return[0,0,0]};rr.prototype.getLabelDistance=function(e,t,r){return 0};rr.prototype.getMesh=function(){return this._labelsMesh};rr.prototype.updateData=function(e,t,r){t==null&&(t=0),r==null&&(r=e.count()),(!this._labelsVisibilitiesBits||this._labelsVisibilitiesBits.length!==r-t)&&(this._labelsVisibilitiesBits=new Uint8Array(r-t));for(var i=["label","show"],n=["emphasis","label","show"],a=t;a<r;a++){var o=e.getItemModel(a),s=o.get(i),l=o.get(n);l==null&&(l=s);var u=(s?Af:0)|(l?Ef:0);this._labelsVisibilitiesBits[a-t]=u}this._start=t,this._end=r,this._data=e};rr.prototype.updateLabels=function(e){if(this._data){e=e||[];for(var t=e.length>0,r={},i=0;i<e.length;i++)r[e[i]]=!0;this._labelsMesh.geometry.convertToDynamicArray(!0),this._labelTextureSurface.clear();for(var n=["label"],a=["emphasis","label"],o=this._data.hostModel,s=this._data,l=o.getModel(n),u=o.getModel(a,l),h={left:"right",right:"left",top:"center",bottom:"center"},f={left:"middle",right:"middle",top:"bottom",bottom:"top"},d=this._start;d<this._end;d++){var c=!1;t&&r[d]&&(c=!0);var v=this._labelsVisibilitiesBits[d-this._start]&(c?Ef:Af);if(v){var p=s.getItemModel(d),_=p.getModel(c?a:n,c?u:l),m=_.get("distance")||0,g=_.get("position"),y=this._api.getDevicePixelRatio(),x=o.getFormattedLabel(d,c?"emphasis":"normal");if(x==null||x==="")return;var w=new gr({style:$n(_,{text:x,fill:_.get("color")||Ze(s,d)||"#000",align:"left",verticalAlign:"top",opacity:oe.firstNotNull(_.get("opacity"),je(s,d),1)})}),T=w.getBoundingRect(),b=1.2;T.height*=b;var A=this._labelTextureSurface.add(w),C=h[g]||"center",D=f[g]||"bottom";this._labelsMesh.geometry.addSprite(this.getLabelPosition(d,g,m),[T.width*y,T.height*y],A,C,D,this.getLabelDistance(d,g,m)*y)}}this._labelsMesh.material.set("uvScale",this._labelTextureSurface.getCoordsScale()),this._labelTextureSurface.getZr().refreshImmediately(),this._labelsMesh.geometry.convertToTypedArray(),this._labelsMesh.geometry.dirty()}};rr.prototype.dispose=function(){this._labelTextureSurface.dispose()};var ct=Re.vec3;S.Shader.import(ya);function Ti(e){this.rootNode=new S.Node,this._triangulationResults={},this._shadersMap=S.COMMON_SHADERS.filter(function(r){return r!=="shadow"}).reduce(function(r,i){return r[i]=S.createShader("ecgl."+i),r},{}),this._linesShader=S.createShader("ecgl.meshLines3D");var t={};S.COMMON_SHADERS.forEach(function(r){t[r]=new S.Material({shader:S.createShader("ecgl."+r)})}),this._groundMaterials=t,this._groundMesh=new S.Mesh({geometry:new S.PlaneGeometry({dynamic:!0}),castShadow:!1,renderNormal:!0,$ignorePicking:!0}),this._groundMesh.rotation.rotateX(-Math.PI/2),this._labelsBuilder=new rr(512,512,e),this._labelsBuilder.getMesh().renderOrder=100,this._labelsBuilder.getMesh().material.depthTest=!1,this.rootNode.add(this._labelsBuilder.getMesh()),this._initMeshes(),this._api=e}Ti.prototype={constructor:Ti,extrudeY:!0,update:function(e,t,r,i,n){var a=e.getData();i==null&&(i=0),n==null&&(n=a.count()),this._startIndex=i,this._endIndex=n-1,this._triangulation(e,i,n);var o=this._getShader(e.get("shading"));this._prepareMesh(e,o,r,i,n),this.rootNode.updateWorldTransform(),this._updateRegionMesh(e,r,i,n);var s=e.coordinateSystem;s.type==="geo3D"&&this._updateGroundPlane(e,s,r);var l=this;this._labelsBuilder.updateData(a,i,n),this._labelsBuilder.getLabelPosition=function(u,h,f){var d=a.getName(u),c,v=f;if(s.type==="geo3D"){var p=s.getRegion(d);if(!p)return[NaN,NaN,NaN];c=p.getCenter();var _=s.dataToPoint([c[0],c[1],v]);return _}else var m=l._triangulationResults[u-l._startIndex],c=l.extrudeY?[(m.max[0]+m.min[0])/2,m.max[1]+v,(m.max[2]+m.min[2])/2]:[(m.max[0]+m.min[0])/2,(m.max[1]+m.min[1])/2,m.max[2]+v]},this._data=a,this._labelsBuilder.updateLabels(),this._updateDebugWireframe(e),this._lastHoverDataIndex=0},_initMeshes:function(){var e=this;function t(){var n=new S.Mesh({name:"Polygon",material:new S.Material({shader:e._shadersMap.lambert}),geometry:new S.Geometry({sortTriangles:!0,dynamic:!0}),culling:!1,ignorePicking:!0,renderNormal:!0});return Object.assign(n.geometry,us),n}var r=t(),i=new S.Mesh({material:new S.Material({shader:this._linesShader}),castShadow:!1,ignorePicking:!0,$ignorePicking:!0,geometry:new yr({useNativeLine:!1})});this.rootNode.add(r),this.rootNode.add(i),r.material.define("both","VERTEX_COLOR"),r.material.define("fragment","DOUBLE_SIDED"),this._polygonMesh=r,this._linesMesh=i,this.rootNode.add(this._groundMesh)},_getShader:function(e){var t=this._shadersMap[e];return t||(t=this._shadersMap.lambert),t.__shading=e,t},_prepareMesh:function(e,t,r,i,n){for(var a=0,o=0,s=0,l=0,u=i;u<n;u++){var h=this._getRegionPolygonInfo(u),f=this._getRegionLinesInfo(u,e,this._linesMesh.geometry);a+=h.vertexCount,o+=h.triangleCount,s+=f.vertexCount,l+=f.triangleCount}var d=this._polygonMesh,c=d.geometry;["position","normal","texcoord0","color"].forEach(function(v){c.attributes[v].init(a)}),c.indices=a>65535?new Uint32Array(o*3):new Uint16Array(o*3),d.material.shader!==t&&d.material.attachShader(t,!0),S.setMaterialFromModel(t.__shading,d.material,e,r),s>0&&(this._linesMesh.geometry.resetOffset(),this._linesMesh.geometry.setVertexCount(s),this._linesMesh.geometry.setTriangleCount(l)),this._dataIndexOfVertex=new Uint32Array(a),this._vertexRangeOfDataIndex=new Uint32Array((n-i)*2)},_updateRegionMesh:function(e,t,r,i){for(var n=e.getData(),a=0,o=0,s=!1,T=this._polygonMesh,l=this._linesMesh,u=r;u<i;u++){var h=e.getRegionModel(u),f=h.getModel("itemStyle"),d=oe.firstNotNull(Ze(n,u),f.get("color"),"#fff"),c=oe.firstNotNull(je(n,u),f.get("opacity"),1),v=S.parseColor(d),p=S.parseColor(f.get("borderColor"));v[3]*=c,p[3]*=c;var _=v[3]<.99;T.material.set("color",[1,1,1,1]),s=s||_;for(var m=oe.firstNotNull(h.get("height",!0),e.get("regionHeight")),g=this._updatePolygonGeometry(e,T.geometry,u,m,a,o,v),y=a;y<g.vertexOffset;y++)this._dataIndexOfVertex[y]=u;this._vertexRangeOfDataIndex[(u-r)*2]=a,this._vertexRangeOfDataIndex[(u-r)*2+1]=g.vertexOffset,a=g.vertexOffset,o=g.triangleOffset;var x=f.get("borderWidth"),w=x>0;w&&(x*=t.getDevicePixelRatio(),this._updateLinesGeometry(l.geometry,e,u,m,x,e.coordinateSystem.transform)),l.invisible=!w,l.material.set({color:p})}var T=this._polygonMesh;T.material.transparent=s,T.material.depthMask=!s,T.geometry.updateBoundingBox(),T.frontFace=this.extrudeY?S.Mesh.CCW:S.Mesh.CW,T.material.get("normalMap")&&T.geometry.generateTangents(),T.seriesIndex=e.seriesIndex,T.on("mousemove",this._onmousemove,this),T.on("mouseout",this._onmouseout,this)},_updateDebugWireframe:function(e){var t=e.getModel("debug.wireframe");if(t.get("show")){var r=S.parseColor(t.get("lineStyle.color")||"rgba(0,0,0,0.5)"),i=oe.firstNotNull(t.get("lineStyle.width"),1),n=this._polygonMesh;n.geometry.generateBarycentric(),n.material.define("both","WIREFRAME_TRIANGLE"),n.material.set("wireframeLineColor",r),n.material.set("wireframeLineWidth",i)}},_onmousemove:function(e){var t=this._dataIndexOfVertex[e.triangle[0]];t==null&&(t=-1),t!==this._lastHoverDataIndex&&(this.downplay(this._lastHoverDataIndex),this.highlight(t),this._labelsBuilder.updateLabels([t])),this._lastHoverDataIndex=t,this._polygonMesh.dataIndex=t},_onmouseout:function(e){e.target&&(this.downplay(this._lastHoverDataIndex),this._lastHoverDataIndex=-1,this._polygonMesh.dataIndex=-1),this._labelsBuilder.updateLabels([])},_updateGroundPlane:function(e,t,r){var i=e.getModel("groundPlane",e);if(this._groundMesh.invisible=!i.get("show",!0),!this._groundMesh.invisible){var n=e.get("shading"),a=this._groundMaterials[n];a||(a=this._groundMaterials.lambert),S.setMaterialFromModel(n,a,i,r),a.get("normalMap")&&this._groundMesh.geometry.generateTangents(),this._groundMesh.material=a,this._groundMesh.material.set("color",S.parseColor(i.get("color"))),this._groundMesh.scale.set(t.size[0],t.size[2],1)}},_triangulation:function(e,t,r){this._triangulationResults=[];for(var i=[1/0,1/0,1/0],n=[-1/0,-1/0,-1/0],a=e.coordinateSystem,o=t;o<r;o++){for(var s=[],l=e.getRegionPolygonCoords(o),u=0;u<l.length;u++){var h=l[u].exterior,f=l[u].interiors,d=[],c=[];if(!(h.length<3)){for(var v=0,p=0;p<h.length;p++){var _=h[p];d[v++]=_[0],d[v++]=_[1]}for(var p=0;p<f.length;p++)if(!(f[p].length<3)){for(var m=d.length/2,g=0;g<f[p].length;g++){var _=f[p][g];d.push(_[0]),d.push(_[1])}c.push(m)}for(var y=xf(d,c),x=new Float64Array(d.length/2*3),w=[],T=[1/0,1/0,1/0],b=[-1/0,-1/0,-1/0],A=0,p=0;p<d.length;)ct.set(w,d[p++],0,d[p++]),a&&a.transform&&ct.transformMat4(w,w,a.transform),ct.min(T,T,w),ct.max(b,b,w),x[A++]=w[0],x[A++]=w[1],x[A++]=w[2];ct.min(i,i,T),ct.max(n,n,b),s.push({points:x,indices:y,min:T,max:b})}}this._triangulationResults.push(s)}this._geoBoundingBox=[i,n]},_getRegionPolygonInfo:function(e){for(var t=this._triangulationResults[e-this._startIndex],r=0,i=0,n=0;n<t.length;n++)r+=t[n].points.length/3,i+=t[n].indices.length/3;var a=r*2+r*4,o=i*2+r*2;return{vertexCount:a,triangleCount:o}},_updatePolygonGeometry:function(e,t,r,i,n,a,o){var s=e.get("projectUVOnGround"),l=t.attributes.position,u=t.attributes.normal,h=t.attributes.texcoord0,f=t.attributes.color,d=this._triangulationResults[r-this._startIndex],c=f.value&&o,v=t.indices,p=this.extrudeY?1:2,_=this.extrudeY?2:1,m=[this.rootNode.worldTransform.x.len(),this.rootNode.worldTransform.y.len(),this.rootNode.worldTransform.z.len()],g=ct.mul([],this._geoBoundingBox[0],m),y=ct.mul([],this._geoBoundingBox[1],m),x=Math.max(y[0]-g[0],y[2]-g[2]);function w(Me,tt,Ye){for(var ke=Me.points,Di=ke.length,Fe=[],Ot=[],rt=0;rt<Di;rt+=3)Fe[0]=ke[rt],Fe[p]=tt,Fe[_]=ke[rt+2],Ot[0]=(ke[rt]*m[0]-g[0])/x,Ot[1]=(ke[rt+2]*m[_]-g[2])/x,l.set(n,Fe),c&&f.set(n,o),h.set(n++,Ot)}function T(Me,tt,Ye){var ke=n;w(Me,tt);for(var Di=Me.indices.length,Fe=0;Fe<Di;Fe++)v[a*3+Fe]=Me.indices[Fe]+ke;a+=Me.indices.length/3}for(var b=this.extrudeY?[0,1,0]:[0,0,1],A=ct.negate([],b),C=0;C<d.length;C++){var D=n,L=d[C];T(L,0),T(L,i);for(var M=L.points.length/3,P=0;P<M;P++)u.set(D+P,A),u.set(D+P+M,b);for(var N=[0,3,1,1,3,2],I=[[],[],[],[]],V=[],Z=[],B=[],$=[],q=0,P=0;P<M;P++){for(var j=(P+1)%M,Q=(L.points[j*3]-L.points[P*3])*m[0],ie=(L.points[j*3+2]-L.points[P*3+2])*m[_],ae=Math.sqrt(Q*Q+ie*ie),ee=0;ee<4;ee++){var be=ee===0||ee===3,Ae=(be?P:j)*3;I[ee][0]=L.points[Ae],I[ee][p]=ee>1?i:0,I[ee][_]=L.points[Ae+2],l.set(n+ee,I[ee]),s?($[0]=(L.points[Ae]*m[0]-g[0])/x,$[1]=(L.points[Ae+2]*m[_]-g[_])/x):($[0]=(be?q:q+ae)/x,$[1]=(I[ee][p]*m[p]-g[p])/x),h.set(n+ee,$)}ct.sub(V,I[1],I[0]),ct.sub(Z,I[3],I[0]),ct.cross(B,V,Z),ct.normalize(B,B);for(var ee=0;ee<4;ee++)u.set(n+ee,B),c&&f.set(n+ee,o);for(var ee=0;ee<6;ee++)v[a*3+ee]=N[ee]+n;n+=4,a+=2,q+=ae}}return t.dirty(),{vertexOffset:n,triangleOffset:a}},_getRegionLinesInfo:function(e,t,r){var i=0,n=0,a=t.getRegionModel(e),o=a.getModel("itemStyle"),s=o.get("borderWidth");if(s>0){var l=t.getRegionPolygonCoords(e);l.forEach(function(u){var h=u.exterior,f=u.interiors;i+=r.getPolylineVertexCount(h),n+=r.getPolylineTriangleCount(h);for(var d=0;d<f.length;d++)i+=r.getPolylineVertexCount(f[d]),n+=r.getPolylineTriangleCount(f[d])},this)}return{vertexCount:i,triangleCount:n}},_updateLinesGeometry:function(e,t,r,i,n,a){function o(u){for(var h=new Float64Array(u.length*3),f=0,d=[],c=0;c<u.length;c++)d[0]=u[c][0],d[1]=i+.1,d[2]=u[c][1],a&&ct.transformMat4(d,d,a),h[f++]=d[0],h[f++]=d[1],h[f++]=d[2];return h}var s=[1,1,1,1],l=t.getRegionPolygonCoords(r);l.forEach(function(u){var h=u.exterior,f=u.interiors;e.addPolyline(o(h),s,n);for(var d=0;d<f.length;d++)e.addPolyline(o(f[d]),s,n)})},highlight:function(e){var t=this._data;if(t){var r=t.getItemModel(e),i=r.getModel(["emphasis","itemStyle"]),n=i.get("color"),a=oe.firstNotNull(i.get("opacity"),je(t,e),1);if(n==null){var o=Ze(t,e);n=ko(o,-.4)}a==null&&(a=je(t,e));var s=S.parseColor(n);s[3]*=a,this._setColorOfDataIndex(t,e,s)}},downplay:function(e){var t=this._data;if(t){var r=t.getItemModel(e),i=oe.firstNotNull(Ze(t,e),r.get(["itemStyle","color"]),"#fff"),n=oe.firstNotNull(je(t,e),r.get(["itemStyle","opacity"]),1),a=S.parseColor(i);a[3]*=n,this._setColorOfDataIndex(t,e,a)}},dispose:function(){this._labelsBuilder.dispose()},_setColorOfDataIndex:function(e,t,r){if(!(t<this._startIndex&&t>this._endIndex)){t-=this._startIndex;for(var i=this._vertexRangeOfDataIndex[t*2];i<this._vertexRangeOfDataIndex[t*2+1];i++)this._polygonMesh.geometry.attributes.color.set(i,r);this._polygonMesh.geometry.dirty(),this._api.getZr().refresh()}}};const k_=Qt.extend({type:"geo3D",__ecgl__:!0,init:function(e,t){this._geo3DBuilder=new Ti(t),this.groupGL=new S.Node,this._lightRoot=new S.Node,this._sceneHelper=new mr(this._lightRoot),this._sceneHelper.initLight(this._lightRoot),this._control=new gn({zr:t.getZr()}),this._control.init()},render:function(e,t,r){this.groupGL.add(this._geo3DBuilder.rootNode);var i=e.coordinateSystem;if(!(!i||!i.viewGL)){i.viewGL.add(this._lightRoot),e.get("show")?i.viewGL.add(this.groupGL):i.viewGL.remove(this.groupGL);var n=this._control;n.setViewGL(i.viewGL);var a=e.getModel("viewControl");n.setFromViewControlModel(a,0),this._sceneHelper.setScene(i.viewGL.scene),this._sceneHelper.updateLight(e),i.viewGL.setPostEffect(e.getModel("postEffect"),r),i.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling")),this._geo3DBuilder.update(e,t,r,0,e.getData().count());var o=i.viewGL.isLinearSpace()?"define":"undefine";this._geo3DBuilder.rootNode.traverse(function(s){s.material&&s.material[o]("fragment","SRGB_DECODE")}),n.off("update"),n.on("update",function(){r.dispatchAction({type:"geo3DChangeCamera",alpha:n.getAlpha(),beta:n.getBeta(),distance:n.getDistance(),center:n.getCenter(),from:this.uid,geo3DId:e.id})}),n.update()}},afterRender:function(e,t,r,i){var n=i.renderer;this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r)},dispose:function(){this._control.dispose(),this._geo3DBuilder.dispose()}});var W_={Russia:[100,60],"United States":[-99,38],"United States of America":[-99,38]};function X_(e,t){if(e==="world"){var r=W_[t.name];if(r){var i=[r[0],r[1]];t.setCenter(i)}}}var j_=Re.vec3,li=Re.mat4,Z_=[pp,X_];function oa(e,t,r,i,n){this.name=e,this.map=t,this.regionHeight=0,this.regions=[],this._nameCoordMap={},this.loadGeoJson(r,i,n),this.transform=li.identity(new Float64Array(16)),this.invTransform=li.identity(new Float64Array(16)),this.extrudeY=!0,this.altitudeAxis}oa.prototype={constructor:oa,type:"geo3D",dimensions:["lng","lat","alt"],containPoint:function(){},loadGeoJson:function(e,t,r){var i=js||js;try{this.regions=e?i(e):[]}catch(u){throw`Invalid geoJson format
`+u}t=t||{},r=r||{};for(var n=this.regions,a={},o=0;o<n.length;o++){var s=n[o].name;s=r[s]||s,n[o].name=s,a[s]=n[o],this.addGeoCoord(s,n[o].getCenter());var l=t[s];l&&n[o].transformTo(l.left,l.top,l.width,l.height)}this._regionsMap=a,this._geoRect=null,Z_.forEach(function(u){u(this)},this)},getGeoBoundingRect:function(){if(this._geoRect)return this._geoRect;for(var e,t=this.regions,r=0;r<t.length;r++){var i=t[r].getBoundingRect();e=e||i.clone(),e.union(i)}return this._geoRect=e||new Ur(0,0,0,0)},addGeoCoord:function(e,t){this._nameCoordMap[e]=t},getRegion:function(e){return this._regionsMap[e]},getRegionByCoord:function(e){for(var t=this.regions,r=0;r<t.length;r++)if(t[r].contain(e))return t[r]},setSize:function(e,t,r){this.size=[e,t,r];var i=this.getGeoBoundingRect(),n=e/i.width,a=-r/i.height,o=-e/2-i.x*n,s=r/2-i.y*a,l=this.extrudeY?[o,0,s]:[o,s,0],u=this.extrudeY?[n,1,a]:[n,a,1],h=this.transform;li.identity(h),li.translate(h,h,l),li.scale(h,h,u),li.invert(this.invTransform,h)},dataToPoint:function(e,t){t=t||[];var r=this.extrudeY?1:2,i=this.extrudeY?2:1,n=e[2];return isNaN(n)&&(n=0),t[0]=e[0],t[i]=e[1],this.altitudeAxis?t[r]=this.altitudeAxis.dataToCoord(n):t[r]=0,t[r]+=this.regionHeight,j_.transformMat4(t,t,this.transform),t},pointToData:function(e,t){}};function q_(e,t){var r=e.getBoxLayoutParams(),i=dn(r,{width:t.getWidth(),height:t.getHeight()});i.y=t.getHeight()-i.y-i.height,this.viewGL.setViewport(i.x,i.y,i.width,i.height,t.getDevicePixelRatio());var n=this.getGeoBoundingRect(),a=n.width/n.height*(e.get("aspectScale")||.75),o=e.get("boxWidth"),s=e.get("boxDepth"),l=e.get("boxHeight");l==null&&(l=5),isNaN(o)&&isNaN(s)&&(o=100),isNaN(s)?s=o/a:isNaN(o)&&(o=s/a),this.setSize(o,l,s),this.regionHeight=e.get("regionHeight"),this.altitudeAxis&&this.altitudeAxis.setExtent(0,Math.max(l-this.regionHeight,0))}function Y_(e,t){var r=[1/0,-1/0];if(e.eachSeries(function(n){if(n.coordinateSystem===this&&n.type!=="series.map3D"){var a=n.getData(),o=n.coordDimToDataDim("alt"),s=o&&o[0];if(s){var l=a.getDataExtent(s,!0);r[0]=Math.min(r[0],l[0]),r[1]=Math.max(r[1],l[1])}}},this),r&&isFinite(r[1]-r[0])){var i=jo(r,{type:"value",min:"dataMin",max:"dataMax"});this.altitudeAxis=new Si("altitude",i),this.resize(this.model,t)}}var Su=0,hs={dimensions:oa.prototype.dimensions,create:function(e,t){var r=[];if(!po)throw new Error("geo3D component depends on geo component");function i(n,a){var o=hs.createGeo3D(n);n.__viewGL=n.__viewGL||new ge,o.viewGL=n.__viewGL,n.coordinateSystem=o,o.model=n,r.push(o),o.resize=q_,o.resize(n,t),o.update=Y_}return e.eachComponent("geo3D",function(n,a){i(n)}),e.eachSeriesByType("map3D",function(n,a){var o=n.get("coordinateSystem");o==null&&(o="geo3D"),o==="geo3D"&&i(n)}),e.eachSeries(function(n){if(n.get("coordinateSystem")==="geo3D"){if(n.type==="series.map3D")return;var a=n.getReferringComponents("geo3D").models[0];if(a||(a=e.getComponent("geo3D")),!a)throw new Error('geo "'+oe.firstNotNull(n.get("geo3DIndex"),n.get("geo3DId"),0)+'" not found');n.coordinateSystem=a.coordinateSystem}}),r},createGeo3D:function(e){var t=e.get("map"),r;return typeof t=="string"?(r=t,t=po(t)):t&&t.features&&(t={geoJson:t}),r==null&&(r="GEO_ANONYMOUS_"+Su++),new oa(r+Su++,r,t&&t.geoJson,t&&t.specialAreas,e.get("nameMap"))}};function Lf(e){e.registerComponentModel(Ci),e.registerComponentView(k_),e.registerAction({type:"geo3DChangeCamera",event:"geo3dcamerachanged",update:"series:updateCamera"},function(t,r){r.eachComponent({mainType:"geo3D",query:t},function(i){i.setView(t)})}),e.registerCoordinateSystem("geo3D",hs)}Ne(Lf);function bu(e,t){e.id=e.id||e.name||t+""}var Hr=Rt.extend({type:"globe",layoutMode:"box",coordinateSystem:null,init:function(){Hr.superApply(this,"init",arguments),Y(this.option.layers,function(e,t){le(e,this.defaultLayerOption),bu(e,t)},this)},mergeOption:function(e){var t=this.option.layers;this.option.layers=null,Hr.superApply(this,"mergeOption",arguments);function r(o){return eh(o,function(s,l,u){return bu(l,u),s[l.id]=l,s},{})}if(t&&t.length){var i=r(e.layers),n=r(t);for(var a in i)n[a]?le(n[a],i[a],!0):t.push(e.layers[a]);this.option.layers=t}Y(this.option.layers,function(o){le(o,this.defaultLayerOption)},this)},optionUpdated:function(){this.updateDisplacementHash()},defaultLayerOption:{show:!0,type:"overlay"},defaultOption:{show:!0,zlevel:-10,left:0,top:0,width:"100%",height:"100%",environment:"auto",baseColor:"#fff",baseTexture:"",heightTexture:"",displacementTexture:"",displacementScale:0,displacementQuality:"medium",globeRadius:100,globeOuterRadius:150,shading:"lambert",light:{main:{time:""}},atmosphere:{show:!1,offset:5,color:"#ffffff",glowPower:6,innerGlowPower:2},viewControl:{autoRotate:!0,panSensitivity:0,targetCoord:null},layers:[]},setDisplacementData:function(e,t,r){this.displacementData=e,this.displacementWidth=t,this.displacementHeight=r},getDisplacementTexture:function(){return this.get("displacementTexture")||this.get("heightTexture")},getDisplacemenScale:function(){var e=this.getDisplacementTexture(),t=this.get("displacementScale");return(!e||e==="none")&&(t=0),t},hasDisplacement:function(){return this.getDisplacemenScale()>0},_displacementChanged:!0,_displacementScale:0,updateDisplacementHash:function(){var e=this.getDisplacementTexture(),t=this.getDisplacemenScale();this._displacementChanged=this._displacementTexture!==e||this._displacementScale!==t,this._displacementTexture=e,this._displacementScale=t},isDisplacementChanged:function(){return this._displacementChanged}});le(Hr.prototype,ga);le(Hr.prototype,bi);le(Hr.prototype,Ai);le(Hr.prototype,Li);var Cf=Math.PI,Lt=Math.sin,qt=Math.cos,Mf=Math.tan,Df=Math.asin,Pf=Math.atan2,kr=Cf/180,$_=1e3*60*60*24,K_=2440588,J_=2451545;function Q_(e){return e.valueOf()/$_-.5+K_}function e0(e){return Q_(e)-J_}var sa=kr*23.4397;function t0(e,t){return Pf(Lt(e)*qt(sa)-Mf(t)*Lt(sa),qt(e))}function r0(e,t){return Df(Lt(t)*qt(sa)+qt(t)*Lt(sa)*Lt(e))}function i0(e,t,r){return Pf(Lt(e),qt(e)*Lt(t)-Mf(r)*qt(t))}function n0(e,t,r){return Df(Lt(t)*Lt(r)+qt(t)*qt(r)*qt(e))}function a0(e,t){return kr*(280.16+360.9856235*e)-t}function o0(e){return kr*(357.5291+.98560028*e)}function s0(e){var t=kr*(1.9148*Lt(e)+.02*Lt(2*e)+3e-4*Lt(3*e)),r=kr*102.9372;return e+t+r+Cf}function l0(e){var t=o0(e),r=s0(t);return{dec:r0(r,0),ra:t0(r,0)}}var Nf={};Nf.getPosition=function(e,t,r){var i=kr*-r,n=kr*t,a=e0(e),o=l0(a),s=a0(a,i)-o.ra;return{azimuth:i0(s,n,o.dec),altitude:n0(s,n,o.dec)}};const u0=`@export ecgl.atmosphere.vertex
attribute vec3 position: POSITION;
attribute vec3 normal : NORMAL;
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform mat4 normalMatrix : WORLDINVERSETRANSPOSE;

varying vec3 v_Normal;

void main() {
 v_Normal = normalize((normalMatrix * vec4(normal, 0.0)).xyz);
 gl_Position = worldViewProjection * vec4(position, 1.0);
}
@end


@export ecgl.atmosphere.fragment
uniform mat4 viewTranspose: VIEWTRANSPOSE;
uniform float glowPower;
uniform vec3 glowColor;

varying vec3 v_Normal;

void main() {
 float intensity = pow(1.0 - dot(v_Normal, (viewTranspose * vec4(0.0, 0.0, 1.0, 0.0)).xyz), glowPower);
 gl_FragColor = vec4(glowColor, intensity * intensity);
}
@end`;S.Shader.import($h);S.Shader.import(u0);const h0=Qt.extend({type:"globe",__ecgl__:!0,_displacementScale:0,init:function(e,t){this.groupGL=new S.Node,this._sphereGeometry=new S.SphereGeometry({widthSegments:200,heightSegments:100,dynamic:!0}),this._overlayGeometry=new S.SphereGeometry({widthSegments:80,heightSegments:40}),this._planeGeometry=new S.PlaneGeometry,this._earthMesh=new S.Mesh({renderNormal:!0}),this._atmosphereMesh=new S.Mesh,this._atmosphereGeometry=new S.SphereGeometry({widthSegments:80,heightSegments:40}),this._atmosphereMaterial=new S.Material({shader:new S.Shader(S.Shader.source("ecgl.atmosphere.vertex"),S.Shader.source("ecgl.atmosphere.fragment")),transparent:!0}),this._atmosphereMesh.geometry=this._atmosphereGeometry,this._atmosphereMesh.material=this._atmosphereMaterial,this._atmosphereMesh.frontFace=S.Mesh.CW,this._lightRoot=new S.Node,this._sceneHelper=new mr,this._sceneHelper.initLight(this._lightRoot),this.groupGL.add(this._atmosphereMesh),this.groupGL.add(this._earthMesh),this._control=new gn({zr:t.getZr()}),this._control.init(),this._layerMeshes={}},render:function(e,t,r){var i=e.coordinateSystem,n=e.get("shading");i.viewGL.add(this._lightRoot),e.get("show")?i.viewGL.add(this.groupGL):i.viewGL.remove(this.groupGL),this._sceneHelper.setScene(i.viewGL.scene),i.viewGL.setPostEffect(e.getModel("postEffect"),r),i.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling"));var a=this._earthMesh;a.geometry=this._sphereGeometry;var o="ecgl."+n;(!a.material||a.material.shader.name!==o)&&(a.material=S.createMaterial(o)),S.setMaterialFromModel(n,a.material,e,r),["roughnessMap","metalnessMap","detailMap","normalMap"].forEach(function(f){var d=a.material.get(f);d&&(d.flipY=!1)}),a.material.set("color",S.parseColor(e.get("baseColor")));var s=i.radius*.99;if(a.scale.set(s,s,s),e.get("atmosphere.show")){a.material.define("both","ATMOSPHERE_ENABLED"),this._atmosphereMesh.invisible=!1,this._atmosphereMaterial.setUniforms({glowPower:e.get("atmosphere.glowPower")||6,glowColor:e.get("atmosphere.color")||"#ffffff"}),a.material.setUniforms({glowPower:e.get("atmosphere.innerGlowPower")||2,glowColor:e.get("atmosphere.color")||"#ffffff"});var l=e.get("atmosphere.offset")||5;this._atmosphereMesh.scale.set(s+l,s+l,s+l)}else a.material.undefine("both","ATMOSPHERE_ENABLED"),this._atmosphereMesh.invisible=!0;var u=a.material.setTextureImage("diffuseMap",e.get("baseTexture"),r,{flipY:!1,anisotropic:8});u&&u.surface&&u.surface.attachToMesh(a);var h=a.material.setTextureImage("bumpMap",e.get("heightTexture"),r,{flipY:!1,anisotropic:8});h&&h.surface&&h.surface.attachToMesh(a),a.material[e.get("postEffect.enable")?"define":"undefine"]("fragment","SRGB_DECODE"),this._updateLight(e,r),this._displaceVertices(e,r),this._updateViewControl(e,r),this._updateLayers(e,r)},afterRender:function(e,t,r,i){var n=i.renderer;this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r)},_updateLayers:function(e,t){var r=e.coordinateSystem,i=e.get("layers"),n=r.radius,a=[],o=[],s=[],l=[];Y(i,function(c){var v=new zr(c),p=v.get("type"),_=S.loadTexture(v.get("texture"),t,{flipY:!1,anisotropic:8});if(_.surface&&_.surface.attachToMesh(this._earthMesh),p==="blend"){var m=v.get("blendTo"),g=oe.firstNotNull(v.get("intensity"),1);m==="emission"?(s.push(_),l.push(g)):(a.push(_),o.push(g))}else{var y=v.get("id"),x=this._layerMeshes[y];x||(x=this._layerMeshes[y]=new S.Mesh({geometry:this._overlayGeometry,castShadow:!1,ignorePicking:!0}));var w=v.get("shading");w==="lambert"?(x.material=x.__lambertMaterial||new S.Material({autoUpdateTextureStatus:!1,shader:S.createShader("ecgl.lambert"),transparent:!0,depthMask:!1}),x.__lambertMaterial=x.material):(x.material=x.__colorMaterial||new S.Material({autoUpdateTextureStatus:!1,shader:S.createShader("ecgl.color"),transparent:!0,depthMask:!1}),x.__colorMaterial=x.material),x.material.enableTexture("diffuseMap");var T=v.get("distance"),b=n+(T??r.radius/100);x.scale.set(b,b,b),n=b;var A=this._blankTexture||(this._blankTexture=S.createBlankTexture("rgba(255, 255, 255, 0)"));x.material.set("diffuseMap",A),S.loadTexture(v.get("texture"),t,{flipY:!1,anisotropic:8},function(C){C.surface&&C.surface.attachToMesh(x),x.material.set("diffuseMap",C),t.getZr().refresh()}),v.get("show")?this.groupGL.add(x):this.groupGL.remove(x)}},this);var u=this._earthMesh.material;u.define("fragment","LAYER_DIFFUSEMAP_COUNT",a.length),u.define("fragment","LAYER_EMISSIVEMAP_COUNT",s.length),u.set("layerDiffuseMap",a),u.set("layerDiffuseIntensity",o),u.set("layerEmissiveMap",s),u.set("layerEmissionIntensity",l);var h=e.getModel("debug.wireframe");if(h.get("show")){u.define("both","WIREFRAME_TRIANGLE");var f=S.parseColor(h.get("lineStyle.color")||"rgba(0,0,0,0.5)"),d=oe.firstNotNull(h.get("lineStyle.width"),1);u.set("wireframeLineWidth",d),u.set("wireframeLineColor",f)}else u.undefine("both","WIREFRAME_TRIANGLE")},_updateViewControl:function(e,t){var r=e.coordinateSystem,i=e.getModel("viewControl");r.viewGL.camera;var n=this;function a(){return{type:"globeChangeCamera",alpha:o.getAlpha(),beta:o.getBeta(),distance:o.getDistance()-r.radius,center:o.getCenter(),from:n.uid,globeId:e.id}}var o=this._control;o.setViewGL(r.viewGL);var s=i.get("targetCoord"),l,u;s!=null&&(u=s[0]+90,l=s[1]),o.setFromViewControlModel(i,{baseDistance:r.radius,alpha:l,beta:u}),o.off("update"),o.on("update",function(){t.dispatchAction(a())})},_displaceVertices:function(e,t){var r=e.get("displacementQuality"),i=e.get("debug.wireframe.show"),n=e.coordinateSystem;if(!(!e.isDisplacementChanged()&&r===this._displacementQuality&&i===this._showDebugWireframe)){this._displacementQuality=r,this._showDebugWireframe=i;var a=this._sphereGeometry,o={low:100,medium:200,high:400,ultra:800}[r]||200,s=o/2;(a.widthSegments!==o||i)&&(a.widthSegments=o,a.heightSegments=s,a.build()),this._doDisplaceVertices(a,n),i&&a.generateBarycentric()}},_doDisplaceVertices:function(e,t){var r=e.attributes.position.value,i=e.attributes.texcoord0.value,n=e.__originalPosition;(!n||n.length!==r.length)&&(n=new Float32Array(r.length),n.set(r),e.__originalPosition=n);for(var a=t.displacementWidth,o=t.displacementHeight,s=t.displacementData,l=0;l<e.vertexCount;l++){var u=l*3,h=l*2,f=n[u+1],d=n[u+2],c=n[u+3],v=i[h++],p=i[h++],_=Math.round(v*(a-1)),m=Math.round(p*(o-1)),g=m*a+_,y=s?s[g]:0;r[u+1]=f+f*y,r[u+2]=d+d*y,r[u+3]=c+c*y}e.generateVertexNormals(),e.dirty(),e.updateBoundingBox()},_updateLight:function(e,t){var r=this._earthMesh;this._sceneHelper.updateLight(e);var i=this._sceneHelper.mainLight,n=e.get("light.main.time")||new Date,a=Nf.getPosition(ud(n),0,0),o=Math.cos(a.altitude);i.position.y=-o*Math.cos(a.azimuth),i.position.x=Math.sin(a.altitude),i.position.z=o*Math.sin(a.azimuth),i.lookAt(r.getWorldPosition())},dispose:function(e,t){this.groupGL.removeAll(),this._control.dispose()}});var f0=Re.vec3;function la(e){this.radius=e,this.viewGL=null,this.altitudeAxis,this.displacementData=null,this.displacementWidth,this.displacementHeight}la.prototype={constructor:la,dimensions:["lng","lat","alt"],type:"globe",containPoint:function(){},setDisplacementData:function(e,t,r){this.displacementData=e,this.displacementWidth=t,this.displacementHeight=r},_getDisplacementScale:function(e,t){var r=(e+180)/360*(this.displacementWidth-1),i=(90-t)/180*(this.displacementHeight-1),n=Math.round(r)+Math.round(i)*this.displacementWidth;return this.displacementData[n]},dataToPoint:function(e,t){var r=e[0],i=e[1],n=e[2]||0,a=this.radius;this.displacementData&&(a*=1+this._getDisplacementScale(r,i)),this.altitudeAxis&&(a+=this.altitudeAxis.dataToCoord(n)),r=r*Math.PI/180,i=i*Math.PI/180;var o=Math.cos(i)*a;return t=t||[],t[0]=-o*Math.cos(r+Math.PI),t[1]=Math.sin(i)*a,t[2]=o*Math.sin(r+Math.PI),t},pointToData:function(e,t){var r=e[0],i=e[1],n=e[2],a=f0.len(e);r/=a,i/=a,n/=a;var o=Math.asin(i),s=Math.atan2(n,-r);s<0&&(s=Math.PI*2+s);var l=o*180/Math.PI,u=s*180/Math.PI-180;return t=t||[],t[0]=u,t[1]=l,t[2]=a-this.radius,this.altitudeAxis&&(t[2]=this.altitudeAxis.coordToData(t[2])),t}};function c0(e,t){var r=document.createElement("canvas"),i=r.getContext("2d"),n=e.width,a=e.height;r.width=n,r.height=a,i.drawImage(e,0,0,n,a);for(var o=i.getImageData(0,0,n,a).data,s=new Float32Array(o.length/4),l=0;l<o.length/4;l++){var u=o[l*4];s[l]=u/255*t}return{data:s,width:n,height:a}}function d0(e,t){var r=e.getBoxLayoutParams(),i=dn(r,{width:t.getWidth(),height:t.getHeight()});i.y=t.getHeight()-i.y-i.height,this.viewGL.setViewport(i.x,i.y,i.width,i.height,t.getDevicePixelRatio()),this.radius=e.get("globeRadius");var n=e.get("globeOuterRadius");this.altitudeAxis&&this.altitudeAxis.setExtent(0,n-this.radius)}function v0(e,t){var r=[1/0,-1/0];if(e.eachSeries(function(n){if(n.coordinateSystem===this){var a=n.getData(),o=n.coordDimToDataDim("alt"),s=o&&o[0];if(s){var l=a.getDataExtent(s,!0);r[0]=Math.min(r[0],l[0]),r[1]=Math.max(r[1],l[1])}}},this),r&&isFinite(r[1]-r[0])){var i=jo(r,{type:"value",min:"dataMin",max:"dataMax"});this.altitudeAxis=new Si("altitude",i),this.resize(this.model,t)}}var p0={dimensions:la.prototype.dimensions,create:function(e,t){var r=[];return e.eachComponent("globe",function(i){i.__viewGL=i.__viewGL||new ge;var n=new la;n.viewGL=i.__viewGL,i.coordinateSystem=n,n.model=i,r.push(n),n.resize=d0,n.resize(i,t),n.update=v0}),e.eachSeries(function(i){if(i.get("coordinateSystem")==="globe"){var n=i.getReferringComponents("globe").models[0];if(n||(n=e.getComponent("globe")),!n)throw new Error('globe "'+oe.firstNotNull(i.get("globe3DIndex"),i.get("globe3DId"),0)+'" not found');var a=n.coordinateSystem;i.coordinateSystem=a}}),e.eachComponent("globe",function(i,n){var a=i.coordinateSystem,o=i.getDisplacementTexture(),s=i.getDisplacemenScale();if(i.isDisplacementChanged()){if(i.hasDisplacement()){var l=!0;S.loadTexture(o,t,function(u){var h=u.image,f=c0(h,s);i.setDisplacementData(f.data,f.width,f.height),l||t.dispatchAction({type:"globeUpdateDisplacment"})}),l=!1}else a.setDisplacementData(null,0,0);a.setDisplacementData(i.displacementData,i.displacementWidth,i.displacementHeight)}}),r}};function g0(e){e.registerComponentModel(Hr),e.registerComponentView(h0),e.registerCoordinateSystem("globe",p0),e.registerAction({type:"globeChangeCamera",event:"globecamerachanged",update:"series:updateCamera"},function(t,r){r.eachComponent({mainType:"globe",query:t},function(i){i.setView(t)})}),e.registerAction({type:"globeUpdateDisplacment",event:"globedisplacementupdated",update:"update"},function(t,r){})}Ne(g0);var Au=["zoom","center","pitch","bearing"],fs=Rt.extend({type:"mapbox3D",layoutMode:"box",coordinateSystem:null,defaultOption:{zlevel:-10,style:"mapbox://styles/mapbox/light-v9",center:[0,0],zoom:0,pitch:0,bearing:0,light:{main:{alpha:20,beta:30}},altitudeScale:1,boxHeight:"auto"},getMapboxCameraOption:function(){var e=this;return Au.reduce(function(t,r){return t[r]=e.get(r),t},{})},setMapboxCameraOption:function(e){e!=null&&Au.forEach(function(t){e[t]!=null&&(this.option[t]=e[t])},this)},getMapbox:function(){return this._mapbox},setMapbox:function(e){this._mapbox=e}});le(fs.prototype,bi);le(fs.prototype,Ai);function xr(e,t){if(this.id=e,this.zr=t,this.dom=document.createElement("div"),this.dom.style.cssText="position:absolute;left:0;right:0;top:0;bottom:0;",!mapboxgl)throw new Error("Mapbox GL library must be included. See https://www.mapbox.com/mapbox-gl-js/api/");this._mapbox=new mapboxgl.Map({container:this.dom}),this._initEvents()}xr.prototype.setUnpainted=function(){};xr.prototype.resize=function(){this._mapbox.resize()};xr.prototype.getMapbox=function(){return this._mapbox};xr.prototype.clear=function(){};xr.prototype.refresh=function(){this._mapbox.resize()};var If=["mousedown","mouseup","click","dblclick","mousemove","mousewheel","wheel","touchstart","touchend","touchmove","touchcancel"];xr.prototype._initEvents=function(){var e=this._mapbox.getCanvasContainer();this._handlers=this._handlers||{contextmenu:function(t){return t.preventDefault(),!1}},If.forEach(function(t){this._handlers[t]=function(r){var i={};for(var n in r)i[n]=r[n];i.bubbles=!1;var a=new r.constructor(r.type,i);e.dispatchEvent(a)},this.zr.dom.addEventListener(t,this._handlers[t])},this),this.zr.dom.addEventListener("contextmenu",this._handlers.contextmenu)};xr.prototype.dispose=function(){If.forEach(function(e){this.zr.dom.removeEventListener(e,this._handlers[e])},this)};const Rf=`
@export ecgl.displayShadow.vertex

@import ecgl.common.transformUniforms

@import ecgl.common.uv.header

@import ecgl.common.attributes

varying vec3 v_WorldPosition;

varying vec3 v_Normal;

void main()
{
 @import ecgl.common.uv.main
 v_Normal = normalize((worldInverseTranspose * vec4(normal, 0.0)).xyz);

 v_WorldPosition = (world * vec4(position, 1.0)).xyz;
 gl_Position = worldViewProjection * vec4(position, 1.0);
}

@end


@export ecgl.displayShadow.fragment

@import ecgl.common.uv.fragmentHeader

varying vec3 v_Normal;
varying vec3 v_WorldPosition;

uniform float roughness: 0.2;

#ifdef DIRECTIONAL_LIGHT_COUNT
@import clay.header.directional_light
#endif

@import ecgl.common.ssaoMap.header

@import clay.plugin.compute_shadow_map

void main()
{
 float shadow = 1.0;

 @import ecgl.common.ssaoMap.main

#if defined(DIRECTIONAL_LIGHT_COUNT) && defined(DIRECTIONAL_LIGHT_SHADOWMAP_COUNT)
 float shadowContribsDir[DIRECTIONAL_LIGHT_COUNT];
 if(shadowEnabled)
 {
 computeShadowOfDirectionalLights(v_WorldPosition, shadowContribsDir);
 }
 for (int i = 0; i < DIRECTIONAL_LIGHT_COUNT; i++) {
 shadow = min(shadow, shadowContribsDir[i] * 0.5 + 0.5);
 }
#endif

 shadow *= 0.5 + ao * 0.5;
 shadow = clamp(shadow, 0.0, 1.0);

 gl_FragColor = vec4(vec3(0.0), 1.0 - shadow);
}

@end`;S.Shader.import(Rf);const m0=Qt.extend({type:"mapbox3D",__ecgl__:!0,init:function(e,t){var r=t.getZr();this._zrLayer=new xr("mapbox3D",r),r.painter.insertLayer(-1e3,this._zrLayer),this._lightRoot=new S.Node,this._sceneHelper=new mr(this._lightRoot),this._sceneHelper.initLight(this._lightRoot);var i=this._zrLayer.getMapbox(),n=this._dispatchInteractAction.bind(this,t,i);["zoom","rotate","drag","pitch","rotate","move"].forEach(function(a){i.on(a,n)}),this._groundMesh=new S.Mesh({geometry:new S.PlaneGeometry,material:new S.Material({shader:new S.Shader({vertex:S.Shader.source("ecgl.displayShadow.vertex"),fragment:S.Shader.source("ecgl.displayShadow.fragment")}),depthMask:!1}),renderOrder:-100,culling:!1,castShadow:!1,$ignorePicking:!0,renderNormal:!0})},render:function(e,t,r){var i=this._zrLayer.getMapbox(),n=e.get("style"),a=JSON.stringify(n);a!==this._oldStyleStr&&n&&i.setStyle(n),this._oldStyleStr=a,i.setCenter(e.get("center")),i.setZoom(e.get("zoom")),i.setPitch(e.get("pitch")),i.setBearing(e.get("bearing")),e.setMapbox(i);var o=e.coordinateSystem;o.viewGL.scene.add(this._lightRoot),o.viewGL.add(this._groundMesh),this._updateGroundMesh(),this._sceneHelper.setScene(o.viewGL.scene),this._sceneHelper.updateLight(e),o.viewGL.setPostEffect(e.getModel("postEffect"),r),o.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling")),this._mapbox3DModel=e},afterRender:function(e,t,r,i){var n=i.renderer;this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r),e.coordinateSystem.viewGL.scene.traverse(function(a){a.material&&(a.material.define("fragment","NORMAL_UP_AXIS",2),a.material.define("fragment","NORMAL_FRONT_AXIS",1))})},updateCamera:function(e,t,r,i){e.coordinateSystem.setCameraOption(i),this._updateGroundMesh(),r.getZr().refresh()},_dispatchInteractAction:function(e,t,r){e.dispatchAction({type:"mapbox3DChangeCamera",pitch:t.getPitch(),zoom:t.getZoom(),center:t.getCenter().toArray(),bearing:t.getBearing(),mapbox3DId:this._mapbox3DModel&&this._mapbox3DModel.id})},_updateGroundMesh:function(){if(this._mapbox3DModel){var e=this._mapbox3DModel.coordinateSystem,t=e.dataToPoint(e.center);this._groundMesh.position.set(t[0],t[1],-.001);var r=new S.Plane(new S.Vector3(0,0,1),0),i=e.viewGL.camera.castRay(new S.Vector2(-1,-1)),n=e.viewGL.camera.castRay(new S.Vector2(1,1)),a=i.intersectPlane(r),o=n.intersectPlane(r),s=a.dist(o)/e.viewGL.rootNode.scale.x;this._groundMesh.scale.set(s,s,1)}},dispose:function(e,t){this._zrLayer&&this._zrLayer.dispose(),t.getZr().painter.delLayer(-1e3)}});var hr=Re.mat4,Gi=512,ao=.6435011087932844,dt=Math.PI,ni=1/10;function wi(){this.width=0,this.height=0,this.altitudeScale=1,this.boxHeight="auto",this.altitudeExtent,this.bearing=0,this.pitch=0,this.center=[0,0],this._origin,this.zoom=0,this._initialZoom,this.maxPitch=60,this.zoomOffset=0}wi.prototype={constructor:wi,dimensions:["lng","lat","alt"],containPoint:function(){},setCameraOption:function(e){this.bearing=e.bearing,this.pitch=e.pitch,this.center=e.center,this.zoom=e.zoom,this._origin||(this._origin=this.projectOnTileWithScale(this.center,Gi)),this._initialZoom==null&&(this._initialZoom=this.zoom),this.updateTransform()},updateTransform:function(){if(this.height){var e=.5/Math.tan(ao/2)*this.height*ni,t=Math.max(Math.min(this.pitch,this.maxPitch),0)/180*Math.PI,r=ao/2,i=Math.PI/2+t,n=Math.sin(r)*e/Math.sin(Math.PI-i-r),a=Math.cos(Math.PI/2-t)*n+e,o=a*1.1;this.pitch>50&&(o=1e3);var s=[];hr.perspective(s,ao,this.width/this.height,1,o),this.viewGL.camera.projectionMatrix.setArray(s),this.viewGL.camera.decomposeProjectionMatrix();var s=hr.identity([]),l=this.dataToPoint(this.center);hr.scale(s,s,[1,-1,1]),hr.translate(s,s,[0,0,-e]),hr.rotateX(s,s,t),hr.rotateZ(s,s,-this.bearing/180*Math.PI),hr.translate(s,s,[-l[0]*this.getScale()*ni,-l[1]*this.getScale()*ni,0]),this.viewGL.camera.viewMatrix.array=s;var u=[];hr.invert(u,s),this.viewGL.camera.worldTransform.array=u,this.viewGL.camera.decomposeWorldTransform();var h=Gi*this.getScale(),f;if(this.altitudeExtent&&!isNaN(this.boxHeight)){var d=this.altitudeExtent[1]-this.altitudeExtent[0];f=this.boxHeight/d*this.getScale()/Math.pow(2,this._initialZoom-this.zoomOffset)}else f=h/(2*Math.PI*6378e3*Math.abs(Math.cos(this.center[1]*(Math.PI/180))))*this.altitudeScale*ni;this.viewGL.rootNode.scale.set(this.getScale()*ni,this.getScale()*ni,f)}},getScale:function(){return Math.pow(2,this.zoom-this.zoomOffset)},projectOnTile:function(e,t){return this.projectOnTileWithScale(e,this.getScale()*Gi,t)},projectOnTileWithScale:function(e,t,r){var i=e[0],n=e[1],a=i*dt/180,o=n*dt/180,s=t*(a+dt)/(2*dt),l=t*(dt-Math.log(Math.tan(dt/4+o*.5)))/(2*dt);return r=r||[],r[0]=s,r[1]=l,r},unprojectFromTile:function(e,t){return this.unprojectOnTileWithScale(e,this.getScale()*Gi,t)},unprojectOnTileWithScale:function(e,t,r){var i=e[0],n=e[1],a=i/t*(2*dt)-dt,o=2*(Math.atan(Math.exp(dt-n/t*(2*dt)))-dt/4);return r=r||[],r[0]=a*180/dt,r[1]=o*180/dt,r},dataToPoint:function(e,t){return t=this.projectOnTileWithScale(e,Gi,t),t[0]-=this._origin[0],t[1]-=this._origin[1],t[2]=isNaN(e[2])?0:e[2],isNaN(e[2])||(t[2]=e[2],this.altitudeExtent&&(t[2]-=this.altitudeExtent[0])),t}};function sn(){wi.apply(this,arguments)}sn.prototype=new wi;sn.prototype.constructor=sn;sn.prototype.type="mapbox3D";function Of(e,t,r){function i(a,o){var s=o.getWidth(),l=o.getHeight(),u=o.getDevicePixelRatio();this.viewGL.setViewport(0,0,s,l,u),this.width=s,this.height=l,this.altitudeScale=a.get("altitudeScale"),this.boxHeight=a.get("boxHeight")}function n(a,o){if(this.model.get("boxHeight")!=="auto"){var s=[1/0,-1/0];a.eachSeries(function(l){if(l.coordinateSystem===this){var u=l.getData(),h=l.coordDimToDataDim("alt")[0];if(h){var f=u.getDataExtent(h,!0);s[0]=Math.min(s[0],f[0]),s[1]=Math.max(s[1],f[1])}}},this),s&&isFinite(s[1]-s[0])&&(this.altitudeExtent=s)}}return{dimensions:t.prototype.dimensions,create:function(a,o){var s=[];return a.eachComponent(e,function(l){var u=l.__viewGL;u||(u=l.__viewGL=new ge,u.setRootNode(new S.Node));var h=new t;h.viewGL=l.__viewGL,h.resize=i,h.resize(l,o),s.push(h),l.coordinateSystem=h,h.model=l,h.update=n}),a.eachSeries(function(l){if(l.get("coordinateSystem")===e){var u=l.getReferringComponents(e).models[0];if(u||(u=a.getComponent(e)),!u)throw new Error(e+' "'+oe.firstNotNull(l.get(e+"Index"),l.get(e+"Id"),0)+'" not found');l.coordinateSystem=u.coordinateSystem}}),r&&r(s,a,o),s}}}var _0=Of("mapbox3D",sn,function(e){e.forEach(function(t){t.setCameraOption(t.model.getMapboxCameraOption())})});function y0(e){e.registerComponentModel(fs),e.registerComponentView(m0),e.registerCoordinateSystem("mapbox3D",_0),e.registerAction({type:"mapbox3DChangeCamera",event:"mapbox3dcamerachanged",update:"mapbox3D:updateCamera"},function(t,r){r.eachComponent({mainType:"mapbox3D",query:t},function(i){i.setMapboxCameraOption(t)})})}Ne(y0);var Eu=["zoom","center","pitch","bearing"],cs=Rt.extend({type:"maptalks3D",layoutMode:"box",coordinateSystem:null,defaultOption:{zlevel:-10,urlTemplate:"http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",attribution:'&copy; <a href="http://osm.org">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/">CARTO</a>',center:[0,0],zoom:0,pitch:0,bearing:0,light:{main:{alpha:20,beta:30}},altitudeScale:1,boxHeight:"auto"},getMaptalksCameraOption:function(){var e=this;return Eu.reduce(function(t,r){return t[r]=e.get(r),t},{})},setMaptalksCameraOption:function(e){e!=null&&Eu.forEach(function(t){e[t]!=null&&(this.option[t]=e[t])},this)},getMaptalks:function(){return this._maptalks},setMaptalks:function(e){this._maptalks=e}});le(cs.prototype,bi);le(cs.prototype,Ai);function Tr(e,t,r,i){if(this.id=e,this.zr=t,this.dom=document.createElement("div"),this.dom.style.cssText="position:absolute;left:0;right:0;top:0;bottom:0;",!maptalks)throw new Error("Maptalks library must be included. See https://maptalks.org");this._maptalks=new maptalks.Map(this.dom,{center:r,zoom:i,doubleClickZoom:!1,fog:!1}),this._initEvents()}Tr.prototype.setUnpainted=function(){};Tr.prototype.resize=function(){this._maptalks.checkSize()};Tr.prototype.getMaptalks=function(){return this._maptalks};Tr.prototype.clear=function(){};Tr.prototype.refresh=function(){this._maptalks.checkSize()};var Bf=["mousedown","mouseup","click","dblclick","mousemove","mousewheel","DOMMouseScroll","touchstart","touchend","touchmove","touchcancel"];Tr.prototype._initEvents=function(){var e=this.dom;this._handlers=this._handlers||{contextmenu:function(t){return t.preventDefault(),!1}},Bf.forEach(function(t){this._handlers[t]=function(r){var i={};for(var n in r)i[n]=r[n];i.bubbles=!1;var a=new r.constructor(r.type,i);t==="mousewheel"||t==="DOMMouseScroll"?e.dispatchEvent(a):e.firstElementChild.dispatchEvent(a)},this.zr.dom.addEventListener(t,this._handlers[t])},this),this.zr.dom.addEventListener("contextmenu",this._handlers.contextmenu)};Tr.prototype.dispose=function(){Bf.forEach(function(e){this.zr.dom.removeEventListener(e,this._handlers[e])},this),this._maptalks.remove()};S.Shader.import(Rf);const x0=Qt.extend({type:"maptalks3D",__ecgl__:!0,init:function(e,t){this._groundMesh=new S.Mesh({geometry:new S.PlaneGeometry,material:new S.Material({shader:new S.Shader({vertex:S.Shader.source("ecgl.displayShadow.vertex"),fragment:S.Shader.source("ecgl.displayShadow.fragment")}),depthMask:!1}),renderOrder:-100,culling:!1,castShadow:!1,$ignorePicking:!0,renderNormal:!0})},_initMaptalksLayer:function(e,t){var r=t.getZr();this._zrLayer=new Tr("maptalks3D",r,e.get("center"),e.get("zoom")),r.painter.insertLayer(-1e3,this._zrLayer),this._lightRoot=new S.Node,this._sceneHelper=new mr(this._lightRoot),this._sceneHelper.initLight(this._lightRoot);var i=this._zrLayer.getMaptalks(),n=this._dispatchInteractAction.bind(this,t,i);["zoomend","zooming","zoomstart","dragrotating","pitch","pitchend","movestart","moving","moveend","resize","touchstart","touchmove","touchend","animating"].forEach(function(a){i.on(a,n)})},render:function(e,t,r){this._zrLayer||this._initMaptalksLayer(e,r);var i=this._zrLayer.getMaptalks(),n=e.get("urlTemplate"),a=i.getBaseLayer();n!==this._oldUrlTemplate&&(a?a.setOptions({urlTemplate:n,attribution:e.get("attribution")}):(a=new maptalks.TileLayer("maptalks-echarts-gl-baselayer",{urlTemplate:n,subdomains:["a","b","c"],attribution:e.get("attribution")}),i.setBaseLayer(a))),this._oldUrlTemplate=n,i.setCenter(e.get("center")),i.setZoom(e.get("zoom"),{animation:!1}),i.setPitch(e.get("pitch")),i.setBearing(e.get("bearing")),e.setMaptalks(i);var o=e.coordinateSystem;o.viewGL.scene.add(this._lightRoot),o.viewGL.add(this._groundMesh),this._updateGroundMesh(),this._sceneHelper.setScene(o.viewGL.scene),this._sceneHelper.updateLight(e),o.viewGL.setPostEffect(e.getModel("postEffect"),r),o.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling")),this._maptalks3DModel=e},afterRender:function(e,t,r,i){var n=i.renderer;this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r),e.coordinateSystem.viewGL.scene.traverse(function(a){a.material&&(a.material.define("fragment","NORMAL_UP_AXIS",2),a.material.define("fragment","NORMAL_FRONT_AXIS",1))})},updateCamera:function(e,t,r,i){e.coordinateSystem.setCameraOption(i),this._updateGroundMesh(),r.getZr().refresh()},_dispatchInteractAction:function(e,t,r){e.dispatchAction({type:"maptalks3DChangeCamera",pitch:t.getPitch(),zoom:w0(t.getResolution())+1,center:t.getCenter().toArray(),bearing:t.getBearing(),maptalks3DId:this._maptalks3DModel&&this._maptalks3DModel.id})},_updateGroundMesh:function(){if(this._maptalks3DModel){var e=this._maptalks3DModel.coordinateSystem,t=e.dataToPoint(e.center);this._groundMesh.position.set(t[0],t[1],-.001);var r=new S.Plane(new S.Vector3(0,0,1),0),i=e.viewGL.camera.castRay(new S.Vector2(-1,-1)),n=e.viewGL.camera.castRay(new S.Vector2(1,1)),a=i.intersectPlane(r),o=n.intersectPlane(r),s=a.dist(o)/e.viewGL.rootNode.scale.x;this._groundMesh.scale.set(s,s,1)}},dispose:function(e,t){this._zrLayer&&this._zrLayer.dispose(),t.getZr().painter.delLayer(-1e3)}}),T0=2*6378137*Math.PI/(256*Math.pow(2,20));function w0(e){return 19-Math.log(e/T0)/Math.LN2}function ln(){wi.apply(this,arguments),this.maxPitch=85,this.zoomOffset=1}ln.prototype=new wi;ln.prototype.constructor=ln;ln.prototype.type="maptalks3D";var S0=Of("maptalks3D",ln,function(e){e.forEach(function(t){t.setCameraOption(t.model.getMaptalksCameraOption())})});function b0(e){e.registerComponentModel(cs),e.registerComponentView(x0),e.registerCoordinateSystem("maptalks3D",S0),e.registerAction({type:"maptalks3DChangeCamera",event:"maptalks3dcamerachanged",update:"maptalks3D:updateCamera"},function(t,r){r.eachComponent({mainType:"maptalks3D",query:t},function(i){i.setMaptalksCameraOption(t)})})}Ne(b0);var A0=Re.vec3,E0=Xo.isDimensionStacked;function L0(e){var t=e[0],r=e[1];return!(t>0&&r>0||t<0&&r<0)}function C0(e,t){var r=e.getData(),i=e.get("barSize");if(i==null){var n=t.size,a,o,s=t.getAxis("x"),l=t.getAxis("y");s.type==="category"?a=s.getBandWidth()*.7:a=Math.round(n[0]/Math.sqrt(r.count()))*.6,l.type==="category"?o=l.getBandWidth()*.7:o=Math.round(n[1]/Math.sqrt(r.count()))*.6,i=[a,o]}else Be(i)||(i=[i,i]);var u=t.getAxis("z").scale.getExtent(),h=L0(u),f=["x","y","z"].map(function(v){return e.coordDimToDataDim(v)[0]}),d=E0(r,f[2]),c=d?r.getCalculationInfo("stackResultDimension"):f[2];r.each(f,function(v,p,_,m){var g=r.get(c,m),y=d?g-_:h?0:u[0],x=t.dataToPoint([v,p,y]),w=t.dataToPoint([v,p,g]),T=A0.dist(x,w),b=[0,w[1]<x[1]?-1:1,0];Math.abs(T)===0&&(T=.1);var A=[i[0],T,i[1]];r.setItemLayout(m,[x,b,A])}),r.setLayout("orient",[1,0,0])}function ds(e,t,r){for(var i=e.getDataExtent(t),n=e.getDataExtent(r),a=i[1]-i[0]||i[0],o=n[1]-n[0]||n[0],s=50,l=new Uint8Array(s*s),u=0;u<e.count();u++){var h=e.get(t,u),f=e.get(r,u),d=Math.floor((h-i[0])/a*(s-1)),c=Math.floor((f-n[0])/o*(s-1)),v=c*s+d;l[v]=l[v]||1}for(var p=0,u=0;u<l.length;u++)l[u]&&p++;return p/l.length}var Lu=Re.vec3,M0=Xo.isDimensionStacked;function D0(e,t){var r=e.getData(),i=e.get("minHeight")||0,n=e.get("barSize"),a=["lng","lat","alt"].map(function(u){return e.coordDimToDataDim(u)[0]});if(n==null){var o=t.radius*Math.PI,s=ds(r,a[0],a[1]);n=[o/Math.sqrt(r.count()/s),o/Math.sqrt(r.count()/s)]}else Be(n)||(n=[n,n]);var l=vs(r,a);r.each(a,function(u,h,f,d){var c=r.get(l.dimension,d),v=l.isStacked?c-f:t.altitudeAxis.scale.getExtent()[0],p=Math.max(t.altitudeAxis.dataToCoord(f),i),_=t.dataToPoint([u,h,v]),m=t.dataToPoint([u,h,c]),g=Lu.sub([],m,_);Lu.normalize(g,g);var y=[n[0],p,n[1]];r.setItemLayout(d,[_,g,y])}),r.setLayout("orient",R.UP.array)}function P0(e,t){var r=e.getData(),i=e.get("barSize"),n=e.get("minHeight")||0,a=["lng","lat","alt"].map(function(h){return e.coordDimToDataDim(h)[0]});if(i==null){var o=Math.min(t.size[0],t.size[2]),s=ds(r,a[0],a[1]);i=[o/Math.sqrt(r.count()/s),o/Math.sqrt(r.count()/s)]}else Be(i)||(i=[i,i]);var l=[0,1,0],u=vs(r,a);r.each(a,function(h,f,d,c){var v=r.get(u.dimension,c),p=u.isStacked?v-d:t.altitudeAxis.scale.getExtent()[0],_=Math.max(t.altitudeAxis.dataToCoord(d),n),m=t.dataToPoint([h,f,p]),g=[i[0],_,i[1]];r.setItemLayout(c,[m,l,g])}),r.setLayout("orient",[1,0,0])}function N0(e,t){var r=e.getData(),i=e.coordDimToDataDim("lng")[0],n=e.coordDimToDataDim("lat")[0],a=e.coordDimToDataDim("alt")[0],o=e.get("barSize"),s=e.get("minHeight")||0;if(o==null){var l=r.getDataExtent(i),u=r.getDataExtent(n),h=t.dataToPoint([l[0],u[0]]),f=t.dataToPoint([l[1],u[1]]),d=Math.min(Math.abs(h[0]-f[0]),Math.abs(h[1]-f[1]))||1,c=ds(r,i,n);o=[d/Math.sqrt(r.count()/c),d/Math.sqrt(r.count()/c)]}else Be(o)||(o=[o,o]),o[0]/=t.getScale()/16,o[1]/=t.getScale()/16;var v=[0,0,1],p=[i,n,a],_=vs(r,p);r.each(p,function(m,g,y,x){var w=r.get(_.dimension,x),T=_.isStacked?w-y:0,b=t.dataToPoint([m,g,T]),A=t.dataToPoint([m,g,w]),C=Math.max(A[2]-b[2],s),D=[o[0],C,o[1]];r.setItemLayout(x,[b,v,D])}),r.setLayout("orient",[1,0,0])}function vs(e,t){var r=M0(e,t[2]);return{dimension:r?e.getCalculationInfo("stackResultDimension"):t[2],isStacked:r}}function I0(e){e.registerLayout(function(t,r){t.eachSeriesByType("bar3D",function(i){var n=i.coordinateSystem,a=n&&n.type;a==="globe"?D0(i,n):a==="cartesian3D"?C0(i,n):a==="geo3D"?P0(i,n):(a==="mapbox3D"||a==="maptalks3D")&&N0(i,n)})})}var wr={};wr.getFormattedLabel=function(e,t,r,i,n){r=r||"normal";var a=e.getData(i),o=a.getItemModel(t),s=e.getDataParams(t,i);n!=null&&s.value instanceof Array&&(s.value=s.value[n]);var l=o.get(r==="normal"?["label","formatter"]:["emphasis","label","formatter"]);l==null&&(l=o.get(["label","formatter"]));var u;return typeof l=="function"?(s.status=r,u=l(s)):typeof l=="string"&&(u=hd(l,s)),u};wr.normalizeToArray=function(e){return e instanceof Array?e:e==null?[]:[e]};function R0(e,t){var r=[];return Y(e.dimensions,function(i){var n=e.getDimensionInfo(i),a=n.otherDims,o=a[t];o!=null&&o!==!1&&(r[o]=n.name)}),r}function yn(e,t,r){function i(f){var d=[],c=R0(n,"tooltip");c.length?Y(c,function(p){v(n.get(p,t),p)}):Y(f,v);function v(p,_){var m=n.getDimensionInfo(_);if(!(!m||m.otherDims.tooltip===!1)){var g=m.type,y="- "+(m.tooltipName||m.name)+": "+(g==="ordinal"?p+"":g==="time"?cd("yyyy/MM/dd hh:mm:ss",p):Bs(p));y&&d.push(oi(y))}}return"<br/>"+d.join("<br/>")}var n=e.getData(),a=e.getRawValue(t),o=Be(a)?i(a):oi(Bs(a)),s=n.getName(t),l=Ze(n,t);Go(l)&&l.colorStops&&(l=(l.colorStops[0]||{}).color),l=l||"transparent";var u=fd(l),h=e.name;return h==="\0-"&&(h=""),h=h?oi(h)+"<br/>":"",h+u+(s?oi(s)+": "+o:o)}function xa(e,t,r){r=r||e.getSource();var i=t||oh(e.get("coordinateSystem"))||["x","y","z"],n=vn(r,{dimensionsDefine:r.dimensionsDefine||e.get("dimensions"),encodeDefine:r.encodeDefine||e.get("encode"),coordDimensions:i.map(function(s){var l=e.getReferringComponents(s+"Axis3D").models[0];return{type:l&&l.get("type")==="category"?"ordinal":"float",name:s}})});e.get("coordinateSystem")==="cartesian3D"&&n.forEach(function(s){if(i.indexOf(s.coordDim)>=0){var l=e.getReferringComponents(s.coordDim+"Axis3D").models[0];l&&l.get("type")==="category"&&(s.ordinalMeta=l.getOrdinalMeta())}});var a=Xo.enableDataStack(e,n,{byIndex:!0,stackedCoordDimension:"z"}),o=new Nt(n,e);return o.setCalculationInfo(a),o.initData(r),o}var Ff=ft.extend({type:"series.bar3D",dependencies:["globe"],visualStyleAccessPathvisu:"itemStyle",getInitialData:function(e,t){return xa(this)},getFormattedLabel:function(e,t,r,i){var n=wr.getFormattedLabel(this,e,t,r,i);return n==null&&(n=this.getData().get("z",e)),n},formatTooltip:function(e){return yn(this,e)},defaultOption:{coordinateSystem:"cartesian3D",globeIndex:0,grid3DIndex:0,zlevel:-10,bevelSize:0,bevelSmoothness:2,onGridPlane:"xy",shading:"color",minHeight:0,itemStyle:{opacity:1},label:{show:!1,distance:2,textStyle:{fontSize:14,color:"#000",backgroundColor:"rgba(255,255,255,0.7)",padding:3,borderRadius:3}},emphasis:{label:{show:!0}},animationDurationUpdate:500}});le(Ff.prototype,Li);var Ce=Re.vec3,O0=Re.mat3,ps=se.extend(function(){return{attributes:{position:new se.Attribute("position","float",3,"POSITION"),normal:new se.Attribute("normal","float",3,"NORMAL"),color:new se.Attribute("color","float",4,"COLOR"),prevPosition:new se.Attribute("prevPosition","float",3),prevNormal:new se.Attribute("prevNormal","float",3)},dynamic:!0,enableNormal:!1,bevelSize:1,bevelSegments:0,_dataIndices:null,_vertexOffset:0,_triangleOffset:0}},{resetOffset:function(){this._vertexOffset=0,this._triangleOffset=0},setBarCount:function(e){var t=this.enableNormal,r=this.getBarVertexCount()*e,i=this.getBarTriangleCount()*e;this.vertexCount!==r&&(this.attributes.position.init(r),t?this.attributes.normal.init(r):this.attributes.normal.value=null,this.attributes.color.init(r)),this.triangleCount!==i&&(this.indices=r>65535?new Uint32Array(i*3):new Uint16Array(i*3),this._dataIndices=new Uint32Array(r))},getBarVertexCount:function(){var e=this.bevelSize>0?this.bevelSegments:0;return e>0?this._getBevelBarVertexCount(e):this.enableNormal?24:8},getBarTriangleCount:function(){var e=this.bevelSize>0?this.bevelSegments:0;return e>0?this._getBevelBarTriangleCount(e):12},_getBevelBarVertexCount:function(e){return(e+1)*4*(e+1)*2},_getBevelBarTriangleCount:function(e){var t=e*4+3,r=e*2+1;return(t+1)*r*2+4},setColor:function(e,t){for(var r=this.getBarVertexCount(),i=r*e,n=r*(e+1),a=i;a<n;a++)this.attributes.color.set(a,t);this.dirtyAttribute("color")},getDataIndexOfVertex:function(e){return this._dataIndices?this._dataIndices[e]:null},addBar:function(){for(var e=Ce.create,t=Ce.scaleAndAdd,r=e(),i=e(),n=e(),a=e(),o=e(),s=e(),l=e(),u=[],h=[],f=0;f<8;f++)u[f]=e();for(var d=[[0,1,5,4],[2,3,7,6],[4,5,6,7],[3,2,1,0],[0,4,7,3],[1,2,6,5]],c=[0,1,2,0,2,3],v=[],f=0;f<d.length;f++)for(var p=d[f],_=0;_<2;_++){for(var m=[],g=0;g<3;g++)m.push(p[c[_*3+g]]);v.push(m)}return function(y,x,w,T,b,A){var C=this._vertexOffset;if(this.bevelSize>0&&this.bevelSegments>0)this._addBevelBar(y,x,w,T,this.bevelSize,this.bevelSegments,b);else{Ce.copy(n,x),Ce.normalize(n,n),Ce.cross(a,w,n),Ce.normalize(a,a),Ce.cross(i,n,a),Ce.normalize(a,a),Ce.negate(o,i),Ce.negate(s,n),Ce.negate(l,a),t(u[0],y,i,T[0]/2),t(u[0],u[0],a,T[2]/2),t(u[1],y,i,T[0]/2),t(u[1],u[1],l,T[2]/2),t(u[2],y,o,T[0]/2),t(u[2],u[2],l,T[2]/2),t(u[3],y,o,T[0]/2),t(u[3],u[3],a,T[2]/2),t(r,y,n,T[1]),t(u[4],r,i,T[0]/2),t(u[4],u[4],a,T[2]/2),t(u[5],r,i,T[0]/2),t(u[5],u[5],l,T[2]/2),t(u[6],r,o,T[0]/2),t(u[6],u[6],l,T[2]/2),t(u[7],r,o,T[0]/2),t(u[7],u[7],a,T[2]/2);var D=this.attributes;if(this.enableNormal){h[0]=i,h[1]=o,h[2]=n,h[3]=s,h[4]=a,h[5]=l;for(var L=this._vertexOffset,M=0;M<d.length;M++){for(var P=this._triangleOffset*3,N=0;N<6;N++)this.indices[P++]=L+c[N];L+=4,this._triangleOffset+=2}for(var M=0;M<d.length;M++)for(var I=h[M],N=0;N<4;N++){var V=d[M][N];D.position.set(this._vertexOffset,u[V]),D.normal.set(this._vertexOffset,I),D.color.set(this._vertexOffset++,b)}}else{for(var M=0;M<v.length;M++){for(var P=this._triangleOffset*3,N=0;N<3;N++)this.indices[P+N]=v[M][N]+this._vertexOffset;this._triangleOffset++}for(var M=0;M<u.length;M++)D.position.set(this._vertexOffset,u[M]),D.color.set(this._vertexOffset++,b)}}for(var Z=this._vertexOffset,M=C;M<Z;M++)this._dataIndices[M]=A}}(),_addBevelBar:function(){var e=Ce.create(),t=Ce.create(),r=Ce.create(),i=O0.create(),n=[],a=[1,-1,-1,1],o=[1,1,-1,-1],s=[2,0];return function(l,u,h,f,d,c,v){Ce.copy(t,u),Ce.normalize(t,t),Ce.cross(r,h,t),Ce.normalize(r,r),Ce.cross(e,t,r),Ce.normalize(r,r),i[0]=e[0],i[1]=e[1],i[2]=e[2],i[3]=t[0],i[4]=t[1],i[5]=t[2],i[6]=r[0],i[7]=r[1],i[8]=r[2],d=Math.min(f[0],f[2])/2*d;for(var p=0;p<3;p++)n[p]=Math.max(f[p]-d*2,0);for(var _=(f[0]-n[0])/2,m=(f[1]-n[1])/2,g=(f[2]-n[2])/2,y=[],x=[],w=this._vertexOffset,T=[],p=0;p<2;p++){T[p]=T[p]=[];for(var b=0;b<=c;b++)for(var A=0;A<4;A++){(b===0&&p===0||p===1&&b===c)&&T[p].push(w);for(var C=0;C<=c;C++){var D=C/c*Math.PI/2+Math.PI/2*A,L=b/c*Math.PI/2+Math.PI/2*p;x[0]=_*Math.cos(D)*Math.sin(L),x[1]=m*Math.cos(L),x[2]=g*Math.sin(D)*Math.sin(L),y[0]=x[0]+a[A]*n[0]/2,y[1]=x[1]+m+s[p]*n[1]/2,y[2]=x[2]+o[A]*n[2]/2,Math.abs(_-m)<1e-6&&Math.abs(m-g)<1e-6||(x[0]/=_*_,x[1]/=m*m,x[2]/=g*g),Ce.normalize(x,x),Ce.transformMat3(y,y,i),Ce.transformMat3(x,x,i),Ce.add(y,y,l),this.attributes.position.set(w,y),this.enableNormal&&this.attributes.normal.set(w,x),this.attributes.color.set(w,v),w++}}}for(var M=c*4+3,P=c*2+1,N=M+1,A=0;A<P;A++)for(var p=0;p<=M;p++){var I=A*N+p+this._vertexOffset,V=A*N+(p+1)%N+this._vertexOffset,Z=(A+1)*N+(p+1)%N+this._vertexOffset,B=(A+1)*N+p+this._vertexOffset;this.setTriangleIndices(this._triangleOffset++,[Z,I,V]),this.setTriangleIndices(this._triangleOffset++,[Z,B,I])}this.setTriangleIndices(this._triangleOffset++,[T[0][0],T[0][2],T[0][1]]),this.setTriangleIndices(this._triangleOffset++,[T[0][0],T[0][3],T[0][2]]),this.setTriangleIndices(this._triangleOffset++,[T[1][0],T[1][1],T[1][2]]),this.setTriangleIndices(this._triangleOffset++,[T[1][0],T[1][2],T[1][3]]),this._vertexOffset=w}}()});He(ps.prototype,mn);He(ps.prototype,us);var B0=Re.vec3;const F0=it.extend({type:"bar3D",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this._api=t,this._labelsBuilder=new rr(256,256,t);var r=this;this._labelsBuilder.getLabelPosition=function(i,n,a){if(r._data){var o=r._data.getItemLayout(i),s=o[0],l=o[1],u=o[2][1];return B0.scaleAndAdd([],s,l,a+u)}else return[0,0]},this._labelsBuilder.getMesh().renderOrder=100},render:function(e,t,r){var i=this._prevBarMesh;this._prevBarMesh=this._barMesh,this._barMesh=i,this._barMesh||(this._barMesh=new S.Mesh({geometry:new ps,shadowDepthMaterial:new S.Material({shader:new S.Shader(S.Shader.source("ecgl.sm.depth.vertex"),S.Shader.source("ecgl.sm.depth.fragment"))}),culling:e.coordinateSystem.type==="cartesian3D",renderOrder:10,renderNormal:!0})),this.groupGL.remove(this._prevBarMesh),this.groupGL.add(this._barMesh),this.groupGL.add(this._labelsBuilder.getMesh());var n=e.coordinateSystem;if(this._doRender(e,r),n&&n.viewGL){n.viewGL.add(this.groupGL);var a=n.viewGL.isLinearSpace()?"define":"undefine";this._barMesh.material[a]("fragment","SRGB_DECODE")}this._data=e.getData(),this._labelsBuilder.updateData(this._data),this._labelsBuilder.updateLabels(),this._updateAnimation(e)},_updateAnimation:function(e){S.updateVertexAnimation([["prevPosition","position"],["prevNormal","normal"]],this._prevBarMesh,this._barMesh,e)},_doRender:function(e,t){var r=e.getData(),i=e.get("shading"),n=i!=="color",a=this,o=this._barMesh,s="ecgl."+i;(!o.material||o.material.shader.name!==s)&&(o.material=S.createMaterial(s,["VERTEX_COLOR"])),S.setMaterialFromModel(i,o.material,e,t),o.geometry.enableNormal=n,o.geometry.resetOffset();var l=e.get("bevelSize"),u=e.get("bevelSmoothness");o.geometry.bevelSegments=u,o.geometry.bevelSize=l;var h=[],f=new Float32Array(r.count()*4),d=0,_=0,c=!1;r.each(function(g){if(r.hasValue(g)){var y=Ze(r,g),x=je(r,g);x==null&&(x=1),S.parseColor(y,h),h[3]*=x,f[d++]=h[0],f[d++]=h[1],f[d++]=h[2],f[d++]=h[3],h[3]>0&&(_++,h[3]<.99&&(c=!0))}}),o.geometry.setBarCount(_);var v=r.getLayout("orient"),p=this._barIndexOfData=new Int32Array(r.count()),_=0;r.each(function(g){if(!r.hasValue(g)){p[g]=-1;return}var y=r.getItemLayout(g),x=y[0],w=y[1],T=y[2],b=g*4;h[0]=f[b++],h[1]=f[b++],h[2]=f[b++],h[3]=f[b++],h[3]>0&&(a._barMesh.geometry.addBar(x,w,v,T,h,g),p[g]=_++)}),o.geometry.dirty(),o.geometry.updateBoundingBox();var m=o.material;m.transparent=c,m.depthMask=!c,o.geometry.sortTriangles=c,this._initHandler(e,t)},_initHandler:function(e,t){var r=e.getData(),i=this._barMesh,n=e.coordinateSystem.type==="cartesian3D";i.seriesIndex=e.seriesIndex;var a=-1;i.off("mousemove"),i.off("mouseout"),i.on("mousemove",function(o){var s=i.geometry.getDataIndexOfVertex(o.triangle[0]);s!==a&&(this._downplay(a),this._highlight(s),this._labelsBuilder.updateLabels([s]),n&&t.dispatchAction({type:"grid3DShowAxisPointer",value:[r.get("x",s),r.get("y",s),r.get("z",s,!0)]})),a=s,i.dataIndex=s},this),i.on("mouseout",function(o){this._downplay(a),this._labelsBuilder.updateLabels(),a=-1,i.dataIndex=-1,n&&t.dispatchAction({type:"grid3DHideAxisPointer"})},this)},_highlight:function(e){var t=this._data;if(t){var r=this._barIndexOfData[e];if(!(r<0)){var i=t.getItemModel(e),n=i.getModel("emphasis.itemStyle"),a=n.get("color"),o=n.get("opacity");if(a==null){var s=Ze(t,e);a=ko(s,-.4)}o==null&&(o=je(t,e));var l=S.parseColor(a);l[3]*=o,this._barMesh.geometry.setColor(r,l),this._api.getZr().refresh()}}},_downplay:function(e){var t=this._data;if(t){var r=this._barIndexOfData[e];if(!(r<0)){var i=Ze(t,e),n=je(t,e),a=S.parseColor(i);a[3]*=n,this._barMesh.geometry.setColor(r,a),this._api.getZr().refresh()}}},highlight:function(e,t,r,i){this._toggleStatus("highlight",e,t,r,i)},downplay:function(e,t,r,i){this._toggleStatus("downplay",e,t,r,i)},_toggleStatus:function(e,t,r,i,n){var a=t.getData(),o=oe.queryDataIndex(a,n),s=this;o!=null?Y(wr.normalizeToArray(o),function(l){e==="highlight"?this._highlight(l):this._downplay(l)},this):a.each(function(l){e==="highlight"?s._highlight(l):s._downplay(l)})},remove:function(){this.groupGL.removeAll()},dispose:function(){this._labelsBuilder.dispose(),this.groupGL.removeAll()}});function G0(e){e.registerChartView(F0),e.registerSeriesModel(Ff),I0(e),e.registerProcessor(function(t,r){t.eachSeriesByType("bar3d",function(i){var n=i.getData();n.filterSelf(function(a){return n.hasValue(a)})})})}Ne(G0);var z0=ft.extend({type:"series.line3D",dependencies:["grid3D"],visualStyleAccessPath:"lineStyle",visualDrawType:"stroke",getInitialData:function(e,t){return xa(this)},formatTooltip:function(e){return yn(this,e)},defaultOption:{coordinateSystem:"cartesian3D",zlevel:-10,grid3DIndex:0,lineStyle:{width:2},animationDurationUpdate:500}}),U0=Re.vec3;S.Shader.import(ya);const V0=it.extend({type:"line3D",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this._api=t},render:function(e,t,r){var i=this._prevLine3DMesh;this._prevLine3DMesh=this._line3DMesh,this._line3DMesh=i,this._line3DMesh||(this._line3DMesh=new S.Mesh({geometry:new yr({useNativeLine:!1,sortTriangles:!0}),material:new S.Material({shader:S.createShader("ecgl.meshLines3D")}),renderOrder:10}),this._line3DMesh.geometry.pick=this._pick.bind(this)),this.groupGL.remove(this._prevLine3DMesh),this.groupGL.add(this._line3DMesh);var n=e.coordinateSystem;if(n&&n.viewGL){n.viewGL.add(this.groupGL);var a=n.viewGL.isLinearSpace()?"define":"undefine";this._line3DMesh.material[a]("fragment","SRGB_DECODE")}this._doRender(e,r),this._data=e.getData(),this._camera=n.viewGL.camera,this.updateCamera(),this._updateAnimation(e)},updateCamera:function(){this._updateNDCPosition()},_doRender:function(e,t){var r=e.getData(),i=this._line3DMesh;i.geometry.resetOffset();var n=r.getLayout("points"),a=[],o=new Float32Array(n.length/3*4),s=0,l=!1;r.each(function(f){var d=Ze(r,f),c=je(r,f);c==null&&(c=1),S.parseColor(d,a),a[3]*=c,o[s++]=a[0],o[s++]=a[1],o[s++]=a[2],o[s++]=a[3],a[3]<.99&&(l=!0)}),i.geometry.setVertexCount(i.geometry.getPolylineVertexCount(n)),i.geometry.setTriangleCount(i.geometry.getPolylineTriangleCount(n)),i.geometry.addPolyline(n,o,oe.firstNotNull(e.get("lineStyle.width"),1)),i.geometry.dirty(),i.geometry.updateBoundingBox();var u=i.material;u.transparent=l,u.depthMask=!l;var h=e.getModel("debug.wireframe");h.get("show")?(i.geometry.createAttribute("barycentric","float",3),i.geometry.generateBarycentric(),i.material.set("both","WIREFRAME_TRIANGLE"),i.material.set("wireframeLineColor",S.parseColor(h.get("lineStyle.color")||"rgba(0,0,0,0.5)")),i.material.set("wireframeLineWidth",oe.firstNotNull(h.get("lineStyle.width"),1))):i.material.set("both","WIREFRAME_TRIANGLE"),this._points=n,this._initHandler(e,t)},_updateAnimation:function(e){S.updateVertexAnimation([["prevPosition","position"],["prevPositionPrev","positionPrev"],["prevPositionNext","positionNext"]],this._prevLine3DMesh,this._line3DMesh,e)},_initHandler:function(e,t){var r=e.getData(),i=e.coordinateSystem,n=this._line3DMesh,a=-1;n.seriesIndex=e.seriesIndex,n.off("mousemove"),n.off("mouseout"),n.on("mousemove",function(o){var s=i.pointToData(o.point.array),l=r.indicesOfNearest("x",s[0])[0];l!==a&&(t.dispatchAction({type:"grid3DShowAxisPointer",value:[r.get("x",l),r.get("y",l),r.get("z",l)]}),n.dataIndex=l),a=l},this),n.on("mouseout",function(o){a=-1,n.dataIndex=-1,t.dispatchAction({type:"grid3DHideAxisPointer"})},this)},_updateNDCPosition:function(){var e=new W,t=this._camera;W.multiply(e,t.projectionMatrix,t.viewMatrix);var r=this._positionNDC,i=this._points,n=i.length/3;(!r||r.length/2!==n)&&(r=this._positionNDC=new Float32Array(n*2));for(var a=[],o=0;o<n;o++){var s=o*3,l=o*2;a[0]=i[s],a[1]=i[s+1],a[2]=i[s+2],a[3]=1,U0.transformMat4(a,a,e.array),r[l]=a[0]/a[3],r[l+1]=a[1]/a[3]}},_pick:function(e,t,r,i,n,a){var o=this._positionNDC,s=this._data.hostModel,l=s.get("lineStyle.width"),u=-1,h=r.viewport.width,f=r.viewport.height,d=h*.5,c=f*.5;e=(e+1)*d,t=(t+1)*c;for(var v=1;v<o.length/2;v++){var p=(o[(v-1)*2]+1)*d,_=(o[(v-1)*2+1]+1)*c,m=(o[v*2]+1)*d,g=(o[v*2+1]+1)*c;if(dd(p,_,m,g,l,e,t)){var y=(p-e)*(p-e)+(_-t)*(_-t),x=(m-e)*(m-e)+(g-t)*(g-t);u=y<x?v-1:v}}if(u>=0){var w=u*3,T=new R(this._points[w],this._points[w+1],this._points[w+2]);a.push({dataIndex:u,point:T,pointWorld:T.clone(),target:this._line3DMesh,distance:this._camera.getWorldPosition().dist(T)})}},remove:function(){this.groupGL.removeAll()},dispose:function(){this.groupGL.removeAll()}});function H0(e){e.registerChartView(V0),e.registerSeriesModel(z0),e.registerLayout(function(t,r){t.eachSeriesByType("line3D",function(i){var n=i.getData(),a=i.coordinateSystem;if(a){if(a.type!=="cartesian3D")return;var o=new Float32Array(n.count()*3),s=[],l=[],u=a.dimensions,h=u.map(function(f){return i.coordDimToDataDim(f)[0]});a&&n.each(h,function(f,d,c,v){s[0]=f,s[1]=d,s[2]=c,a.dataToPoint(s,l),o[v*3]=l[0],o[v*3+1]=l[1],o[v*3+2]=l[2]}),n.setLayout("points",o)}})})}Ne(H0);const k0=ft.extend({type:"series.scatter3D",dependencies:["globe","grid3D","geo3D"],visualStyleAccessPath:"itemStyle",hasSymbolVisual:!0,getInitialData:function(e,t){return xa(this)},getFormattedLabel:function(e,t,r,i){var n=wr.getFormattedLabel(this,e,t,r,i);if(n==null){var a=this.getData(),o=a.dimensions[a.dimensions.length-1];n=a.get(o,e)}return n},formatTooltip:function(e){return yn(this,e)},defaultOption:{coordinateSystem:"cartesian3D",zlevel:-10,progressive:1e5,progressiveThreshold:1e5,grid3DIndex:0,globeIndex:0,symbol:"circle",symbolSize:10,blendMode:"source-over",label:{show:!1,position:"right",distance:5,textStyle:{fontSize:14,color:"#000",backgroundColor:"rgba(255,255,255,0.7)",padding:3,borderRadius:3}},itemStyle:{opacity:.8},emphasis:{label:{show:!0}},animationDurationUpdate:500}});function oo(e,i,r){var i=i||document.createElement("canvas");i.width=e,i.height=e;var n=i.getContext("2d");return r&&r(n),i}function W0(e,t,r,i){Be(t)||(t=[t,t]);var n=ua.getMarginByStyle(r,i),a=t[0]+n.left+n.right,o=t[1]+n.top+n.bottom,s=Zi(e,0,0,t[0],t[1]),l=Math.max(a,o);s.x=n.left,s.y=n.top,a>o?s.y+=(l-o)/2:s.x+=(l-a)/2;var u=s.getBoundingRect();return s.x-=u.x,s.y-=u.y,s.setStyle(r),s.update(),s.__size=l,s}function X0(e,t,r){var i=t.width,n=t.height,a=e.canvas.width,o=e.canvas.height,s=i/a,l=n/o;function u(m){return m<128?1:-1}function h(m,g){var y=1/0;m=Math.floor(m*s),g=Math.floor(g*l);for(var x=g*i+m,w=t.data[x*4],T=u(w),b=Math.max(g-r,0);b<Math.min(g+r,n);b++)for(var A=Math.max(m-r,0);A<Math.min(m+r,i);A++){var x=b*i+A,C=t.data[x*4],D=u(C),L=A-m,M=b-g;if(T!==D){var P=L*L+M*M;P<y&&(y=P)}}return T*Math.sqrt(y)}for(var f=e.createImageData(a,o),d=0;d<o;d++)for(var c=0;c<a;c++){var v=h(c,d),p=v/r*.5+.5,_=(d*a+c)*4;f.data[_++]=(1-p)*255,f.data[_++]=(1-p)*255,f.data[_++]=(1-p)*255,f.data[_++]=255}return f}var ua={getMarginByStyle:function(e){var t=e.minMargin||0,r=0;e.stroke&&e.stroke!=="none"&&(r=e.lineWidth==null?1:e.lineWidth);var i=e.shadowBlur||0,n=e.shadowOffsetX||0,a=e.shadowOffsetY||0,o={};return o.left=Math.max(r/2,-n+i,t),o.right=Math.max(r/2,n+i,t),o.top=Math.max(r/2,-a+i,t),o.bottom=Math.max(r/2,a+i,t),o},createSymbolSprite:function(e,t,r,i){var n=W0(e,t,r),a=ua.getMarginByStyle(r);return{image:oo(n.__size,i,function(o){ih(o,n)}),margin:a}},createSDFFromCanvas:function(e,t,r,i){return oo(t,i,function(n){var a=e.getContext("2d"),o=a.getImageData(0,0,e.width,e.height);n.putImageData(X0(n,o,r),0,0)})},createSimpleSprite:function(e,t){return oo(e,t,function(r){var i=e/2;r.beginPath(),r.arc(i,i,60,0,Math.PI*2,!1),r.closePath();var n=r.createRadialGradient(i,i,0,i,i,i);n.addColorStop(0,"rgba(255, 255, 255, 1)"),n.addColorStop(.5,"rgba(255, 255, 255, 0.5)"),n.addColorStop(1,"rgba(255, 255, 255, 0)"),r.fillStyle=n,r.fill()})}},Cu=Re.vec3;const j0={needsSortVertices:function(){return this.sortVertices},needsSortVerticesProgressively:function(){return this.needsSortVertices()&&this.vertexCount>=2e4},doSortVertices:function(e,t){var r=this.indices,i=Cu.create();if(!r){r=this.indices=this.vertexCount>65535?new Uint32Array(this.vertexCount):new Uint16Array(this.vertexCount);for(var n=0;n<r.length;n++)r[n]=n}if(t===0){var a=this.attributes.position,e=e.array,o=0;(!this._zList||this._zList.length!==this.vertexCount)&&(this._zList=new Float32Array(this.vertexCount));for(var s,n=0;n<this.vertexCount;n++){a.get(n,i);var l=Cu.sqrDist(i,e);isNaN(l)&&(l=1e7,o++),n===0?(s=l,l=0):l=l-s,this._zList[n]=l}this._noneCount=o}if(this.vertexCount<2e4)t===0&&this._simpleSort(this._noneCount/this.vertexCount>.05);else for(var n=0;n<3;n++)this._progressiveQuickSort(t*3+n);this.dirtyIndices()},_simpleSort:function(e){var t=this._zList,r=this.indices;function i(n,a){return t[a]-t[n]}e?Array.prototype.sort.call(r,i):xi.sort(r,i,0,r.length-1)},_progressiveQuickSort:function(e){var t=this._zList,r=this.indices;this._quickSort=this._quickSort||new xi,this._quickSort.step(r,function(i,n){return t[n]-t[i]},e)}},Z0=`@export ecgl.sdfSprite.vertex

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform float elapsedTime : 0;

attribute vec3 position : POSITION;

#ifdef VERTEX_SIZE
attribute float size;
#else
uniform float u_Size;
#endif

#ifdef VERTEX_COLOR
attribute vec4 a_FillColor: COLOR;
varying vec4 v_Color;
#endif

#ifdef VERTEX_ANIMATION
attribute vec3 prevPosition;
attribute float prevSize;
uniform float percent : 1.0;
#endif


#ifdef POSITIONTEXTURE_ENABLED
uniform sampler2D positionTexture;
#endif

varying float v_Size;

void main()
{

#ifdef POSITIONTEXTURE_ENABLED
 gl_Position = worldViewProjection * vec4(texture2D(positionTexture, position.xy).xy, -10.0, 1.0);
#else

 #ifdef VERTEX_ANIMATION
 vec3 pos = mix(prevPosition, position, percent);
 #else
 vec3 pos = position;
 #endif
 gl_Position = worldViewProjection * vec4(pos, 1.0);
#endif

#ifdef VERTEX_SIZE
#ifdef VERTEX_ANIMATION
 v_Size = mix(prevSize, size, percent);
#else
 v_Size = size;
#endif
#else
 v_Size = u_Size;
#endif

#ifdef VERTEX_COLOR
 v_Color = a_FillColor;
 #endif

 gl_PointSize = v_Size;
}

@end

@export ecgl.sdfSprite.fragment

uniform vec4 color: [1, 1, 1, 1];
uniform vec4 strokeColor: [1, 1, 1, 1];
uniform float smoothing: 0.07;

uniform float lineWidth: 0.0;

#ifdef VERTEX_COLOR
varying vec4 v_Color;
#endif

varying float v_Size;

uniform sampler2D sprite;

@import clay.util.srgb

void main()
{
 gl_FragColor = color;

 vec4 _strokeColor = strokeColor;

#ifdef VERTEX_COLOR
 gl_FragColor *= v_Color;
 #endif

#ifdef SPRITE_ENABLED
 float d = texture2D(sprite, gl_PointCoord).r;
 gl_FragColor.a *= smoothstep(0.5 - smoothing, 0.5 + smoothing, d);

 if (lineWidth > 0.0) {
 float sLineWidth = lineWidth / 2.0;

 float outlineMaxValue0 = 0.5 + sLineWidth;
 float outlineMaxValue1 = 0.5 + sLineWidth + smoothing;
 float outlineMinValue0 = 0.5 - sLineWidth - smoothing;
 float outlineMinValue1 = 0.5 - sLineWidth;

 if (d <= outlineMaxValue1 && d >= outlineMinValue0) {
 float a = _strokeColor.a;
 if (d <= outlineMinValue1) {
 a = a * smoothstep(outlineMinValue0, outlineMinValue1, d);
 }
 else {
 a = a * smoothstep(outlineMaxValue1, outlineMaxValue0, d);
 }
 gl_FragColor.rgb = mix(gl_FragColor.rgb * gl_FragColor.a, _strokeColor.rgb, a);
 gl_FragColor.a = gl_FragColor.a * (1.0 - a) + a;
 }
 }
#endif

#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(gl_FragColor);
#endif
}
@end`;var so=Re.vec4;S.Shader.import(Z0);var q0=S.Mesh.extend(function(){var e=new S.Geometry({dynamic:!0,attributes:{color:new S.Geometry.Attribute("color","float",4,"COLOR"),position:new S.Geometry.Attribute("position","float",3,"POSITION"),size:new S.Geometry.Attribute("size","float",1),prevPosition:new S.Geometry.Attribute("prevPosition","float",3),prevSize:new S.Geometry.Attribute("prevSize","float",1)}});Object.assign(e,j0);var t=new S.Material({shader:S.createShader("ecgl.sdfSprite"),transparent:!0,depthMask:!1});t.enableTexture("sprite"),t.define("both","VERTEX_COLOR"),t.define("both","VERTEX_SIZE");var r=new S.Texture2D({image:document.createElement("canvas"),flipY:!1});return t.set("sprite",r),e.pick=this._pick.bind(this),{geometry:e,material:t,mode:S.Mesh.POINTS,sizeScale:1}},{_pick:function(e,t,r,i,n,a){var o=this._positionNDC;if(o)for(var s=r.viewport,l=2/s.width,u=2/s.height,h=this.geometry.vertexCount-1;h>=0;h--){var f;this.geometry.indices?f=this.geometry.indices[h]:f=h;var d=o[f*2],c=o[f*2+1],v=this.geometry.attributes.size.get(f)/this.sizeScale,p=v/2;if(e>d-p*l&&e<d+p*l&&t>c-p*u&&t<c+p*u){var _=new S.Vector3,m=new S.Vector3;this.geometry.attributes.position.get(f,_.array),S.Vector3.transformMat4(m,_,this.worldTransform),a.push({vertexIndex:f,point:_,pointWorld:m,target:this,distance:m.distance(i.getWorldPosition())})}}},updateNDCPosition:function(e,t,r){var i=this._positionNDC,n=this.geometry;(!i||i.length/2!==n.vertexCount)&&(i=this._positionNDC=new Float32Array(n.vertexCount*2));for(var a=so.create(),o=0;o<n.vertexCount;o++)n.attributes.position.get(o,a),a[3]=1,so.transformMat4(a,a,e.array),so.scale(a,a,1/a[3]),i[o*2]=a[0],i[o*2+1]=a[1]}}),Mu=20,Du=-10;function Y0(e,t){return e&&t&&e[0]===t[0]&&e[1]===t[1]}function Wr(e,t){this.rootNode=new S.Node,this.is2D=e,this._labelsBuilder=new rr(256,256,t),this._labelsBuilder.getMesh().renderOrder=100,this.rootNode.add(this._labelsBuilder.getMesh()),this._api=t,this._spriteImageCanvas=document.createElement("canvas"),this._startDataIndex=0,this._endDataIndex=0,this._sizeScale=1}Wr.prototype={constructor:Wr,highlightOnMouseover:!0,update:function(e,t,r,i,n){var a=this._prevMesh;this._prevMesh=this._mesh,this._mesh=a;var o=e.getData();if(i==null&&(i=0),n==null&&(n=o.count()),this._startDataIndex=i,this._endDataIndex=n-1,!this._mesh){var s=this._prevMesh&&this._prevMesh.material;this._mesh=new q0({renderOrder:10,frustumCulling:!1}),s&&(this._mesh.material=s)}var s=this._mesh.material,l=this._mesh.geometry,u=l.attributes;this.rootNode.remove(this._prevMesh),this.rootNode.add(this._mesh),this._setPositionTextureToMesh(this._mesh,this._positionTexture);var h=this._getSymbolInfo(e,i,n),f=r.getDevicePixelRatio(),d=e.getModel("itemStyle").getItemStyle(),c=e.get("large"),v=1;h.maxSize>2?(v=this._updateSymbolSprite(e,d,h,f),s.enableTexture("sprite")):s.disableTexture("sprite"),u.position.init(n-i);var p=[];if(c){s.undefine("VERTEX_SIZE"),s.undefine("VERTEX_COLOR");var _=V_(o),m=H_(o);S.parseColor(_,p),p[3]*=m,s.set({color:p,u_Size:h.maxSize*this._sizeScale})}else s.set({color:[1,1,1,1]}),s.define("VERTEX_SIZE"),s.define("VERTEX_COLOR"),u.size.init(n-i),u.color.init(n-i),this._originalOpacity=new Float32Array(n-i);for(var g=o.getLayout("points"),y=u.position.value,x=0;x<n-i;x++){var w=x*3,T=x*2;if(this.is2D?(y[w]=g[T],y[w+1]=g[T+1],y[w+2]=Du):(y[w]=g[w],y[w+1]=g[w+1],y[w+2]=g[w+2]),!c){var _=Ze(o,x),m=je(o,x);S.parseColor(_,p),p[3]*=m,u.color.set(x,p),p[3]<.99;var b=o.getItemVisual(x,"symbolSize");b=b instanceof Array?Math.max(b[0],b[1]):b,isNaN(b)&&(b=0),u.size.value[x]=b*v*this._sizeScale,this._originalOpacity[x]=p[3]}}this._mesh.sizeScale=v,l.updateBoundingBox(),l.dirty(),this._updateMaterial(e,d);var A=e.coordinateSystem;if(A&&A.viewGL){var C=A.viewGL.isLinearSpace()?"define":"undefine";s[C]("fragment","SRGB_DECODE")}c||this._updateLabelBuilder(e,i,n),this._updateHandler(e,t,r),this._updateAnimation(e),this._api=r},getPointsMesh:function(){return this._mesh},updateLabels:function(e){this._labelsBuilder.updateLabels(e)},hideLabels:function(){this.rootNode.remove(this._labelsBuilder.getMesh())},showLabels:function(){this.rootNode.add(this._labelsBuilder.getMesh())},dispose:function(){this._labelsBuilder.dispose()},_updateSymbolSprite:function(e,t,r,i){r.maxSize=Math.min(r.maxSize*2,200);var n=[];return r.aspect>1?(n[0]=r.maxSize,n[1]=r.maxSize/r.aspect):(n[1]=r.maxSize,n[0]=r.maxSize*r.aspect),n[0]=n[0]||1,n[1]=n[1]||1,(this._symbolType!==r.type||!Y0(this._symbolSize,n)||this._lineWidth!==t.lineWidth)&&(ua.createSymbolSprite(r.type,n,{fill:"#fff",lineWidth:t.lineWidth,stroke:"transparent",shadowColor:"transparent",minMargin:Math.min(n[0]/2,10)},this._spriteImageCanvas),ua.createSDFFromCanvas(this._spriteImageCanvas,Math.min(this._spriteImageCanvas.width,32),Mu,this._mesh.material.get("sprite").image),this._symbolType=r.type,this._symbolSize=n,this._lineWidth=t.lineWidth),this._spriteImageCanvas.width/r.maxSize*i},_updateMaterial:function(e,t){var r=e.get("blendMode")==="lighter"?S.additiveBlend:null,i=this._mesh.material;i.blend=r,i.set("lineWidth",t.lineWidth/Mu);var n=S.parseColor(t.stroke);i.set("strokeColor",n),i.transparent=!0,i.depthMask=!1,i.depthTest=!this.is2D,i.sortVertices=!this.is2D},_updateLabelBuilder:function(e,o,r){var i=e.getData(),n=this._mesh.geometry,a=n.attributes.position.value,o=this._startDataIndex,s=this._mesh.sizeScale;this._labelsBuilder.updateData(i,o,r),this._labelsBuilder.getLabelPosition=function(l,u,h){var f=(l-o)*3;return[a[f],a[f+1],a[f+2]]},this._labelsBuilder.getLabelDistance=function(l,u,h){var f=n.attributes.size.get(l-o)/s;return f/2+h},this._labelsBuilder.updateLabels()},_updateAnimation:function(e){S.updateVertexAnimation([["prevPosition","position"],["prevSize","size"]],this._prevMesh,this._mesh,e)},_updateHandler:function(e,t,r){var i=e.getData(),n=this._mesh,a=this,o=-1,s=e.coordinateSystem&&e.coordinateSystem.type==="cartesian3D",l;s&&(l=e.coordinateSystem.model),n.seriesIndex=e.seriesIndex,n.off("mousemove"),n.off("mouseout"),n.on("mousemove",function(u){var h=u.vertexIndex+a._startDataIndex;h!==o&&(this.highlightOnMouseover&&(this.downplay(i,o),this.highlight(i,h),this._labelsBuilder.updateLabels([h])),s&&r.dispatchAction({type:"grid3DShowAxisPointer",value:[i.get(e.coordDimToDataDim("x")[0],h),i.get(e.coordDimToDataDim("y")[0],h),i.get(e.coordDimToDataDim("z")[0],h)],grid3DIndex:l.componentIndex})),n.dataIndex=h,o=h},this),n.on("mouseout",function(u){var h=u.vertexIndex+a._startDataIndex;this.highlightOnMouseover&&(this.downplay(i,h),this._labelsBuilder.updateLabels()),o=-1,n.dataIndex=-1,s&&r.dispatchAction({type:"grid3DHideAxisPointer",grid3DIndex:l.componentIndex})},this)},updateLayout:function(e,t,r){var i=e.getData();if(this._mesh){var n=this._mesh.geometry.attributes.position.value,a=i.getLayout("points");if(this.is2D)for(var o=0;o<a.length/2;o++){var s=o*3,l=o*2;n[s]=a[l],n[s+1]=a[l+1],n[s+2]=Du}else for(var o=0;o<a.length;o++)n[o]=a[o];this._mesh.geometry.dirty(),r.getZr().refresh()}},updateView:function(e){if(this._mesh){var t=new W;W.mul(t,e.viewMatrix,this._mesh.worldTransform),W.mul(t,e.projectionMatrix,t),this._mesh.updateNDCPosition(t,this.is2D,this._api)}},highlight:function(e,t){if(!(t>this._endDataIndex||t<this._startDataIndex)){var r=e.getItemModel(t),i=r.getModel("emphasis.itemStyle"),n=i.get("color"),a=i.get("opacity");if(n==null){var o=Ze(e,t);n=ko(o,-.4)}a==null&&(a=je(e,t));var s=S.parseColor(n);s[3]*=a,this._mesh.geometry.attributes.color.set(t-this._startDataIndex,s),this._mesh.geometry.dirtyAttribute("color"),this._api.getZr().refresh()}},downplay:function(e,t){if(!(t>this._endDataIndex||t<this._startDataIndex)){var r=Ze(e,t),i=je(e,t),n=S.parseColor(r);n[3]*=i,this._mesh.geometry.attributes.color.set(t-this._startDataIndex,n),this._mesh.geometry.dirtyAttribute("color"),this._api.getZr().refresh()}},fadeOutAll:function(e){if(this._originalOpacity){for(var t=this._mesh.geometry,r=0;r<t.vertexCount;r++){var i=this._originalOpacity[r]*e;t.attributes.color.value[r*4+3]=i}t.dirtyAttribute("color"),this._api.getZr().refresh()}},fadeInAll:function(){this.fadeOutAll(1)},setPositionTexture:function(e){this._mesh&&this._setPositionTextureToMesh(this._mesh,e),this._positionTexture=e},removePositionTexture:function(){this._positionTexture=null,this._mesh&&this._setPositionTextureToMesh(this._mesh,null)},setSizeScale:function(e){if(e!==this._sizeScale){if(this._mesh){var t=this._mesh.material.get("u_Size");this._mesh.material.set("u_Size",t/this._sizeScale*e);var r=this._mesh.geometry.attributes;if(r.size.value)for(var i=0;i<r.size.value.length;i++)r.size.value[i]=r.size.value[i]/this._sizeScale*e}this._sizeScale=e}},_setPositionTextureToMesh:function(e,t){t&&e.material.set("positionTexture",t),e.material[t?"enableTexture":"disableTexture"]("positionTexture")},_getSymbolInfo:function(e,t,r){if(e.get("large")){var i=oe.firstNotNull(e.get("symbolSize"),1),s,a;return i instanceof Array?(s=Math.max(i[0],i[1]),a=i[0]/i[1]):(s=i,a=1),{maxSize:i,type:e.get("symbol"),aspect:a}}for(var n=e.getData(),a,o=n.getItemVisual(0,"symbol")||"circle",s=0,l=t;l<r;l++){var i=n.getItemVisual(l,"symbolSize"),u=n.getItemVisual(l,"symbol"),h;if(i instanceof Array)h=i[0]/i[1],s=Math.max(Math.max(i[0],i[1]),s);else{if(isNaN(i))continue;h=1,s=Math.max(i,s)}o=u,a=h}return{maxSize:s,type:o,aspect:a}}};const $0=it.extend({type:"scatter3D",hasSymbolVisual:!0,__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this._pointsBuilderList=[],this._currentStep=0},render:function(e,t,r){if(this.groupGL.removeAll(),!!e.getData().count()){var i=e.coordinateSystem;if(i&&i.viewGL){i.viewGL.add(this.groupGL),this._camera=i.viewGL.camera;var n=this._pointsBuilderList[0];n||(n=this._pointsBuilderList[0]=new Wr(!1,r)),this._pointsBuilderList.length=1,this.groupGL.add(n.rootNode),n.update(e,t,r),n.updateView(i.viewGL.camera)}}},incrementalPrepareRender:function(e,t,r){var i=e.coordinateSystem;i&&i.viewGL&&(i.viewGL.add(this.groupGL),this._camera=i.viewGL.camera),this.groupGL.removeAll(),this._currentStep=0},incrementalRender:function(e,t,r,i){if(!(e.end<=e.start)){var n=this._pointsBuilderList[this._currentStep];n||(n=new Wr(!1,i),this._pointsBuilderList[this._currentStep]=n),this.groupGL.add(n.rootNode),n.update(t,r,i,e.start,e.end),n.updateView(t.coordinateSystem.viewGL.camera),this._currentStep++}},updateCamera:function(){this._pointsBuilderList.forEach(function(e){e.updateView(this._camera)},this)},highlight:function(e,t,r,i){this._toggleStatus("highlight",e,t,r,i)},downplay:function(e,t,r,i){this._toggleStatus("downplay",e,t,r,i)},_toggleStatus:function(e,t,r,i,n){var a=t.getData(),o=oe.queryDataIndex(a,n),s=e==="highlight";o!=null?Y(wr.normalizeToArray(o),function(l){for(var u=0;u<this._pointsBuilderList.length;u++){var h=this._pointsBuilderList[u];s?h.highlight(a,l):h.downplay(a,l)}},this):a.each(function(l){for(var u=0;u<this._pointsBuilderList.length;u++){var h=this._pointsBuilderList[u];s?h.highlight(a,l):h.downplay(a,l)}})},dispose:function(){this._pointsBuilderList.forEach(function(e){e.dispose()}),this.groupGL.removeAll()},remove:function(){this.groupGL.removeAll()}});function K0(e){e.registerChartView($0),e.registerSeriesModel(k0),e.registerLayout({seriesType:"scatter3D",reset:function(t){var r=t.coordinateSystem;if(r){var i=r.dimensions;if(i.length<3)return;var n=i.map(function(s){return t.coordDimToDataDim(s)[0]}),a=[],o=[];return{progress:function(s,l){for(var u=new Float32Array((s.end-s.start)*3),h=s.start;h<s.end;h++){var f=(h-s.start)*3;a[0]=l.get(n[0],h),a[1]=l.get(n[1],h),a[2]=l.get(n[2],h),r.dataToPoint(a,o),u[f]=o[0],u[f+1]=o[1],u[f+2]=o[2]}l.setLayout("points",u)}}}}})}Ne(K0);var ze=Re.vec3,Pu=Re.vec2,Xt=ze.normalize,Vn=ze.cross,Nu=ze.sub,lo=ze.add,pr=ze.create,fr=pr(),yt=pr(),cr=pr(),zi=pr(),Iu=[],Ru=[];function J0(e,t){Pu.copy(Iu,e[0]),Pu.copy(Ru,e[1]);var r=[],i=r[0]=pr(),n=r[1]=pr(),a=r[2]=pr(),o=r[3]=pr();t.dataToPoint(Iu,i),t.dataToPoint(Ru,o),Xt(fr,i),Nu(yt,o,i),Xt(yt,yt),Vn(cr,yt,fr),Xt(cr,cr),Vn(yt,fr,cr),lo(n,fr,yt),Xt(n,n),Xt(fr,o),Nu(yt,i,o),Xt(yt,yt),Vn(cr,yt,fr),Xt(cr,cr),Vn(yt,fr,cr),lo(a,fr,yt),Xt(a,a),lo(zi,i,o),Xt(zi,zi);var s=ze.dot(i,zi),l=ze.dot(zi,n),u=(Math.max(ze.len(i),ze.len(o))-s)/l*2;return ze.scaleAndAdd(n,i,n,u),ze.scaleAndAdd(a,o,a,u),r}function Q0(e,t,r){var i=[],n=i[0]=ze.create(),a=i[1]=ze.create(),o=i[2]=ze.create(),s=i[3]=ze.create();t.dataToPoint(e[0],n),t.dataToPoint(e[1],s);var l=ze.dist(n,s);return ze.lerp(a,n,s,.3),ze.lerp(o,n,s,.3),ze.scaleAndAdd(a,a,r,Math.min(l*.1,10)),ze.scaleAndAdd(o,o,r,Math.min(l*.1,10)),i}function Gf(e,t){for(var r=new Float32Array(e.length*3),i=0,n=[],a=0;a<e.length;a++)t.dataToPoint(e[a],n),r[i++]=n[0],r[i++]=n[1],r[i++]=n[2];return r}function zf(e){var t=[];return e.each(function(r){var i=e.getItemModel(r),n=i.option instanceof Array?i.option:i.getShallow("coords",!0);t.push(n)}),{coordsList:t}}function ey(e,t){var r=e.getData(),i=e.get("polyline");r.setLayout("lineType",i?"polyline":"cubicBezier");var n=zf(r);r.each(function(a){var o=n.coordsList[a],s=i?Gf:J0;r.setItemLayout(a,s(o,t))})}function Ou(e,t,r){var i=e.getData(),n=e.get("polyline"),a=zf(i);i.setLayout("lineType",n?"polyline":"cubicBezier"),i.each(function(o){var s=a.coordsList[o],l=n?Gf(s,t):Q0(s,t,r);i.setItemLayout(o,l)})}function ty(e,t){e.eachSeriesByType("lines3D",function(r){var i=r.coordinateSystem;i.type==="globe"?ey(r,i):i.type==="geo3D"?Ou(r,i,[0,1,0]):(i.type==="mapbox3D"||i.type==="maptalks3D")&&Ou(r,i,[0,0,1])})}const ry=ft.extend({type:"series.lines3D",dependencies:["globe"],visualStyleAccessPath:"lineStyle",visualDrawType:"stroke",getInitialData:function(e,t){var r=new Nt(["value"],this);return r.hasItemOption=!1,r.initData(e.data,[],function(i,n,a,o){if(i instanceof Array)return NaN;r.hasItemOption=!0;var s=i.value;if(s!=null)return s instanceof Array?s[o]:s}),r},defaultOption:{coordinateSystem:"globe",globeIndex:0,geo3DIndex:0,zlevel:-10,polyline:!1,effect:{show:!1,period:4,trailWidth:4,trailLength:.2,spotIntensity:6},silent:!0,blendMode:"source-over",lineStyle:{width:1,opacity:.5}}}),iy=`@export ecgl.trail2.vertex
attribute vec3 position: POSITION;
attribute vec3 positionPrev;
attribute vec3 positionNext;
attribute float offset;
attribute float dist;
attribute float distAll;
attribute float start;

attribute vec4 a_Color : COLOR;

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform vec4 viewport : VIEWPORT;
uniform float near : NEAR;

uniform float speed : 0;
uniform float trailLength: 0.3;
uniform float time;
uniform float period: 1000;

uniform float spotSize: 1;

varying vec4 v_Color;
varying float v_Percent;
varying float v_SpotPercent;

@import ecgl.common.wireframe.vertexHeader

@import ecgl.lines3D.clipNear

void main()
{
 @import ecgl.lines3D.expandLine

 gl_Position = currProj;

 v_Color = a_Color;

 @import ecgl.common.wireframe.vertexMain

#ifdef CONSTANT_SPEED
 float t = mod((speed * time + start) / distAll, 1. + trailLength) - trailLength;
#else
 float t = mod((time + start) / period, 1. + trailLength) - trailLength;
#endif

 float trailLen = distAll * trailLength;

 v_Percent = (dist - t * distAll) / trailLen;

 v_SpotPercent = spotSize / distAll;

 }
@end


@export ecgl.trail2.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];
uniform float spotIntensity: 5;

varying vec4 v_Color;
varying float v_Percent;
varying float v_SpotPercent;

@import ecgl.common.wireframe.fragmentHeader

@import clay.util.srgb

void main()
{
 if (v_Percent > 1.0 || v_Percent < 0.0) {
 discard;
 }

 float fade = v_Percent;

#ifdef SRGB_DECODE
 gl_FragColor = sRGBToLinear(color * v_Color);
#else
 gl_FragColor = color * v_Color;
#endif

 @import ecgl.common.wireframe.fragmentMain

 if (v_Percent > (1.0 - v_SpotPercent)) {
 gl_FragColor.rgb *= spotIntensity;
 }

 gl_FragColor.a *= fade;
}

@end`;var Bu=Re.vec3;function ny(e){return e>0?1:-1}S.Shader.import(iy);const ay=S.Mesh.extend(function(){var e=new S.Material({shader:new S.Shader(S.Shader.source("ecgl.trail2.vertex"),S.Shader.source("ecgl.trail2.fragment")),transparent:!0,depthMask:!1}),t=new yr({dynamic:!0});return t.createAttribute("dist","float",1),t.createAttribute("distAll","float",1),t.createAttribute("start","float",1),{geometry:t,material:e,culling:!1,$ignorePicking:!0}},{updateData:function(e,t,r){var i=e.hostModel,n=this.geometry,a=i.getModel("effect"),o=a.get("trailWidth")*t.getDevicePixelRatio(),s=a.get("trailLength"),l=i.get("effect.constantSpeed"),u=i.get("effect.period")*1e3,h=l!=null;h?this.material.set("speed",l/1e3):this.material.set("period",u),this.material[h?"define":"undefine"]("vertex","CONSTANT_SPEED");var f=i.get("polyline");n.trailLength=s,this.material.set("trailLength",s),n.resetOffset(),["position","positionPrev","positionNext"].forEach(function(b){n.attributes[b].value=r.attributes[b].value});var d=["dist","distAll","start","offset","color"];d.forEach(function(b){n.attributes[b].init(n.vertexCount)}),n.indices=r.indices;var c=[],v=a.get("trailColor"),p=a.get("trailOpacity"),_=v!=null,m=p!=null;this.updateWorldTransform();var g=this.worldTransform.x.len(),y=this.worldTransform.y.len(),x=this.worldTransform.z.len(),w=0,T=0;e.each(function(b){var A=e.getItemLayout(b),C=m?p:je(e,b),D=Ze(e,b);C==null&&(C=1),c=S.parseColor(_?v:D,c),c[3]*=C;for(var L=f?r.getPolylineVertexCount(A):r.getCubicCurveVertexCount(A[0],A[1],A[2],A[3]),M=0,P=[],N=[],I=w;I<w+L;I++)n.attributes.position.get(I,P),P[0]*=g,P[1]*=y,P[2]*=x,I>w&&(M+=Bu.dist(P,N)),n.attributes.dist.set(I,M),Bu.copy(N,P);T=Math.max(T,M);for(var V=Math.random()*(h?M:u),I=w;I<w+L;I++)n.attributes.distAll.set(I,M),n.attributes.start.set(I,V),n.attributes.offset.set(I,ny(r.attributes.offset.get(I))*o/2),n.attributes.color.set(I,c);w+=L}),this.material.set("spotSize",T*.1*s),this.material.set("spotIntensity",a.get("spotIntensity")),n.dirty()},setAnimationTime:function(e){this.material.set("time",e)}});S.Shader.import(ya);function oy(e){return e.radius!=null?e.radius:e.size!=null?Math.max(e.size[0],e.size[1],e.size[2]):100}const sy=it.extend({type:"lines3D",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this._meshLinesMaterial=new S.Material({shader:S.createShader("ecgl.meshLines3D"),transparent:!0,depthMask:!1}),this._linesMesh=new S.Mesh({geometry:new yr,material:this._meshLinesMaterial,$ignorePicking:!0}),this._trailMesh=new ay},render:function(e,t,r){this.groupGL.add(this._linesMesh);var i=e.coordinateSystem,n=e.getData();if(i&&i.viewGL){var a=i.viewGL;a.add(this.groupGL),this._updateLines(e,t,r);var o=i.viewGL.isLinearSpace()?"define":"undefine";this._linesMesh.material[o]("fragment","SRGB_DECODE"),this._trailMesh.material[o]("fragment","SRGB_DECODE")}var s=this._trailMesh;if(s.stopAnimation(),e.get("effect.show")){this.groupGL.add(s),s.updateData(n,r,this._linesMesh.geometry),s.__time=s.__time||0;var l=3600*1e3;this._curveEffectsAnimator=s.animate("",{loop:!0}).when(l,{__time:l}).during(function(){s.setAnimationTime(s.__time)}).start()}else this.groupGL.remove(s),this._curveEffectsAnimator=null;this._linesMesh.material.blend=this._trailMesh.material.blend=e.get("blendMode")==="lighter"?S.additiveBlend:null},pauseEffect:function(){this._curveEffectsAnimator&&this._curveEffectsAnimator.pause()},resumeEffect:function(){this._curveEffectsAnimator&&this._curveEffectsAnimator.resume()},toggleEffect:function(){var e=this._curveEffectsAnimator;e&&(e.isPaused()?e.resume():e.pause())},_updateLines:function(e,t,r){var i=e.getData(),n=e.coordinateSystem,a=this._linesMesh.geometry,o=e.get("polyline");a.expandLine=!0;var s=oy(n);a.segmentScale=s/20;var l="lineStyle.width".split("."),u=r.getDevicePixelRatio();i.each(function(c){var v=i.getItemModel(c),p=v.get(l);p==null&&(p=1),i.setItemVisual(c,"lineWidth",p)}),a.useNativeLine=!1;var h=0,f=0;i.each(function(c){var v=i.getItemLayout(c);o?(h+=a.getPolylineVertexCount(v),f+=a.getPolylineTriangleCount(v)):(h+=a.getCubicCurveVertexCount(v[0],v[1],v[2],v[3]),f+=a.getCubicCurveTriangleCount(v[0],v[1],v[2],v[3]))}),a.setVertexCount(h),a.setTriangleCount(f),a.resetOffset();var d=[];i.each(function(c){var v=i.getItemLayout(c),p=Ze(i,c),_=je(i,c),m=i.getItemVisual(c,"lineWidth")*u;_==null&&(_=1),d=S.parseColor(p,d),d[3]*=_,o?a.addPolyline(v,d,m):a.addCubicCurve(v[0],v[1],v[2],v[3],d,m)}),a.dirty()},remove:function(){this.groupGL.removeAll()},dispose:function(){this.groupGL.removeAll()}});function ly(e){e.registerChartView(sy),e.registerSeriesModel(ry),e.registerLayout(ty),e.registerAction({type:"lines3DPauseEffect",event:"lines3deffectpaused",update:"series.lines3D:pauseEffect"},function(){}),e.registerAction({type:"lines3DResumeEffect",event:"lines3deffectresumed",update:"series.lines3D:resumeEffect"},function(){}),e.registerAction({type:"lines3DToggleEffect",event:"lines3deffectchanged",update:"series.lines3D:toggleEffect"},function(){})}Ne(ly);function Fu(e,t){for(var r=[],i=0;i<t.length;i++)r.push(e.dataToPoint(t[i]));return r}var Uf=ft.extend({type:"series.polygons3D",getRegionModel:function(e){return this.getData().getItemModel(e)},getRegionPolygonCoords:function(e){var t=this.coordinateSystem,r=this.getData().getItemModel(e),i=r.option instanceof Array?r.option:r.getShallow("coords");r.get("multiPolygon")||(i=[i]);for(var n=[],a=0;a<i.length;a++){for(var o=[],s=1;s<i[a].length;s++)o.push(Fu(t,i[a][s]));n.push({exterior:Fu(t,i[a][0]),interiors:o})}return n},getInitialData:function(e){var t=new Nt(["value"],this);return t.hasItemOption=!1,t.initData(e.data,[],function(r,i,n,a){if(r instanceof Array)return NaN;t.hasItemOption=!0;var o=r.value;if(o!=null)return o instanceof Array?o[a]:o}),t},defaultOption:{show:!0,data:null,multiPolygon:!1,progressiveThreshold:1e3,progressive:1e3,zlevel:-10,label:{show:!1,distance:2,textStyle:{fontSize:20,color:"#000",backgroundColor:"rgba(255,255,255,0.7)",padding:3,borderRadius:4}},itemStyle:{color:"#fff",borderWidth:0,borderColor:"#333"},emphasis:{itemStyle:{color:"#639fc0"},label:{show:!0}}}});le(Uf.prototype,Li);const uy=it.extend({type:"polygons3D",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this._geo3DBuilderList=[],this._currentStep=0},render:function(e,t,r){this.groupGL.removeAll();var i=e.coordinateSystem;i&&i.viewGL&&i.viewGL.add(this.groupGL);var n=this._geo3DBuilderList[0];n||(n=new Ti(r),n.extrudeY=i.type!=="mapbox3D"&&i.type!=="maptalks3D",this._geo3DBuilderList[0]=n),this._updateShaderDefines(i,n),n.update(e,t,r),this._geo3DBuilderList.length=1,this.groupGL.add(n.rootNode)},incrementalPrepareRender:function(e,t,r){this.groupGL.removeAll();var i=e.coordinateSystem;i&&i.viewGL&&i.viewGL.add(this.groupGL),this._currentStep=0},incrementalRender:function(e,t,r,i){var n=this._geo3DBuilderList[this._currentStep],a=t.coordinateSystem;n||(n=new Ti(i),n.extrudeY=a.type!=="mapbox3D"&&a.type!=="maptalks3D",this._geo3DBuilderList[this._currentStep]=n),n.update(t,r,i,e.start,e.end),this.groupGL.add(n.rootNode),this._updateShaderDefines(a,n),this._currentStep++},_updateShaderDefines:function(e,t){var r=e.viewGL.isLinearSpace()?"define":"undefine";t.rootNode.traverse(function(i){i.material&&(i.material[r]("fragment","SRGB_DECODE"),(e.type==="mapbox3D"||e.type==="maptalks3D")&&(i.material.define("fragment","NORMAL_UP_AXIS",2),i.material.define("fragment","NORMAL_FRONT_AXIS",1)))})},remove:function(){this.groupGL.removeAll()},dispose:function(){this.groupGL.removeAll(),this._geo3DBuilderList.forEach(function(e){e.dispose()})}});function hy(e){e.registerChartView(uy),e.registerSeriesModel(Uf)}Ne(hy);var Vf=ft.extend({type:"series.surface",dependencies:["globe","grid3D","geo3D"],visualStyleAccessPath:"itemStyle",formatTooltip:function(e){return yn(this,e)},getInitialData:function(e,t){var r=e.data;function i(Z){return!(isNaN(Z.min)||isNaN(Z.max)||isNaN(Z.step))}function n(Z){var B=nh;return Math.max(B(Z.min),B(Z.max),B(Z.step))+1}if(!r)if(e.parametric){var x=e.parametricEquation||{},w=x.u||{},T=x.v||{};["u","v"].forEach(function(B){i(x[B])}),["x","y","z"].forEach(function(B){x[B]});var b=Math.floor((w.max+w.step-w.min)/w.step),A=Math.floor((T.max+T.step-T.min)/T.step);r=new Float32Array(b*A*5);for(var C=n(w),D=n(T),d=0,c=0;c<A;c++)for(var v=0;v<b;v++){var L=v*w.step+w.min,M=c*T.step+T.min,P=mt(Math.min(L,w.max),C),N=mt(Math.min(M,T.max),D),p=x.x(P,N),_=x.y(P,N),y=x.z(P,N);r[d++]=p,r[d++]=_,r[d++]=y,r[d++]=P,r[d++]=N}}else{var a=e.equation||{},o=a.x||{},s=a.y||{};if(["x","y"].forEach(function(Z){i(a[Z])}),typeof a.z!="function")return;var l=Math.floor((o.max+o.step-o.min)/o.step),u=Math.floor((s.max+s.step-s.min)/s.step);r=new Float32Array(l*u*3);for(var h=n(o),f=n(s),d=0,c=0;c<u;c++)for(var v=0;v<l;v++){var p=v*o.step+o.min,_=c*s.step+s.min,m=mt(Math.min(p,o.max),h),g=mt(Math.min(_,s.max),f),y=a.z(m,g);r[d++]=m,r[d++]=g,r[d++]=y}}var I=["x","y","z"];e.parametric&&I.push("u","v");var V=xa(this,I,r);return V},defaultOption:{coordinateSystem:"cartesian3D",zlevel:-10,grid3DIndex:0,shading:"lambert",parametric:!1,wireframe:{show:!0,lineStyle:{color:"rgba(0,0,0,0.5)",width:1}},equation:{x:{min:-1,max:1,step:.1},y:{min:-1,max:1,step:.1},z:null},parametricEquation:{u:{min:-1,max:1,step:.1},v:{min:-1,max:1,step:.1},x:null,y:null,z:null},dataShape:null,itemStyle:{},animationDurationUpdate:500}});le(Vf.prototype,Li);var Dr=Re.vec3;function fy(e){return isNaN(e[0])||isNaN(e[1])||isNaN(e[2])}const cy=it.extend({type:"surface",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node},render:function(e,t,r){var i=this._prevSurfaceMesh;this._prevSurfaceMesh=this._surfaceMesh,this._surfaceMesh=i,this._surfaceMesh||(this._surfaceMesh=this._createSurfaceMesh()),this.groupGL.remove(this._prevSurfaceMesh),this.groupGL.add(this._surfaceMesh);var n=e.coordinateSystem,a=e.get("shading"),o=e.getData(),s="ecgl."+a;if((!this._surfaceMesh.material||this._surfaceMesh.material.shader.name!==s)&&(this._surfaceMesh.material=S.createMaterial(s,["VERTEX_COLOR","DOUBLE_SIDED"])),S.setMaterialFromModel(a,this._surfaceMesh.material,e,r),n&&n.viewGL){n.viewGL.add(this.groupGL);var l=n.viewGL.isLinearSpace()?"define":"undefine";this._surfaceMesh.material[l]("fragment","SRGB_DECODE")}var u=e.get("parametric"),h=e.get("dataShape");h||(h=this._getDataShape(o,u));var f=e.getModel("wireframe"),d=f.get("lineStyle.width"),c=f.get("show")&&d>0;this._updateSurfaceMesh(this._surfaceMesh,e,h,c);var v=this._surfaceMesh.material;c?(v.define("WIREFRAME_QUAD"),v.set("wireframeLineWidth",d),v.set("wireframeLineColor",S.parseColor(f.get("lineStyle.color")))):v.undefine("WIREFRAME_QUAD"),this._initHandler(e,r),this._updateAnimation(e)},_updateAnimation:function(e){S.updateVertexAnimation([["prevPosition","position"],["prevNormal","normal"]],this._prevSurfaceMesh,this._surfaceMesh,e)},_createSurfaceMesh:function(){var e=new S.Mesh({geometry:new S.Geometry({dynamic:!0,sortTriangles:!0}),shadowDepthMaterial:new S.Material({shader:new S.Shader(S.Shader.source("ecgl.sm.depth.vertex"),S.Shader.source("ecgl.sm.depth.fragment"))}),culling:!1,renderOrder:10,renderNormal:!0});return e.geometry.createAttribute("barycentric","float",4),e.geometry.createAttribute("prevPosition","float",3),e.geometry.createAttribute("prevNormal","float",3),Object.assign(e.geometry,us),e},_initHandler:function(e,t){var r=e.getData(),i=this._surfaceMesh,n=e.coordinateSystem;function a(s,l){for(var u=1/0,h=-1,f=[],d=0;d<s.length;d++){i.geometry.attributes.position.get(s[d],f);var c=Dr.dist(l.array,f);c<u&&(u=c,h=s[d])}return h}i.seriesIndex=e.seriesIndex;var o=-1;i.off("mousemove"),i.off("mouseout"),i.on("mousemove",function(s){var l=a(s.triangle,s.point);if(l>=0){var u=[];i.geometry.attributes.position.get(l,u);for(var h=n.pointToData(u),f=1/0,d=-1,c=[],v=0;v<r.count();v++){c[0]=r.get("x",v),c[1]=r.get("y",v),c[2]=r.get("z",v);var p=Dr.squaredDistance(c,h);p<f&&(d=v,f=p)}d!==o&&t.dispatchAction({type:"grid3DShowAxisPointer",value:h}),o=d,i.dataIndex=d}else i.dataIndex=-1},this),i.on("mouseout",function(s){o=-1,i.dataIndex=-1,t.dispatchAction({type:"grid3DHideAxisPointer"})},this)},_updateSurfaceMesh:function(e,t,r,i){var n=e.geometry,a=t.getData(),o=a.getLayout("points"),s=0;a.each(function(Fe){a.hasValue(Fe)||s++});var l=s||i,u=n.attributes.position,h=n.attributes.normal,f=n.attributes.texcoord0,d=n.attributes.barycentric,c=n.attributes.color,v=r[0],p=r[1],_=t.get("shading"),m=_!=="color";if(l){var g=(v-1)*(p-1)*4;u.init(g),i&&d.init(g)}else u.value=new Float32Array(o);c.init(n.vertexCount),f.init(n.vertexCount);var y=[0,3,1,1,3,2],x=[[1,1,0,0],[0,1,0,1],[1,0,0,1],[1,0,1,0]],w=n.indices=new(n.vertexCount>65535?Uint32Array:Uint16Array)((v-1)*(p-1)*6),T=function(Fe,Ot,rt){rt[1]=Fe*p+Ot,rt[0]=Fe*p+Ot+1,rt[3]=(Fe+1)*p+Ot+1,rt[2]=(Fe+1)*p+Ot},b=!1;if(l){var A=[],C=[],D=0;m?h.init(n.vertexCount):h.value=null;for(var L=[[],[],[]],M=[],P=[],N=Dr.create(),I=function(Fe,Ot,rt){var Ta=Ot*3;return rt[0]=Fe[Ta],rt[1]=Fe[Ta+1],rt[2]=Fe[Ta+2],rt},V=new Float32Array(o.length),Z=new Float32Array(o.length/3*4),B=0;B<a.count();B++)if(a.hasValue(B)){var Ye=S.parseColor(Ze(a,B)),$=je(a,B);$!=null&&(Ye[3]*=$),Ye[3]<.99&&(b=!0);for(var q=0;q<4;q++)Z[B*4+q]=Ye[q]}for(var j=[1e7,1e7,1e7],B=0;B<v-1;B++)for(var Q=0;Q<p-1;Q++){var ie=B*(p-1)+Q,ae=ie*4;T(B,Q,A);for(var ee=!1,q=0;q<4;q++)I(o,A[q],C),fy(C)&&(ee=!0);for(var q=0;q<4;q++)ee?u.set(ae+q,j):(I(o,A[q],C),u.set(ae+q,C)),i&&d.set(ae+q,x[q]);for(var q=0;q<6;q++)w[D++]=y[q]+ae;if(m&&!ee)for(var q=0;q<2;q++){for(var be=q*3,Ae=0;Ae<3;Ae++){var Me=A[y[be]+Ae];I(o,Me,L[Ae])}Dr.sub(M,L[0],L[1]),Dr.sub(P,L[1],L[2]),Dr.cross(N,M,P);for(var Ae=0;Ae<3;Ae++){var tt=A[y[be]+Ae]*3;V[tt]=V[tt]+N[0],V[tt+1]=V[tt+1]+N[1],V[tt+2]=V[tt+2]+N[2]}}}if(m)for(var B=0;B<V.length/3;B++)I(V,B,N),Dr.normalize(N,N),V[B*3]=N[0],V[B*3+1]=N[1],V[B*3+2]=N[2];for(var Ye=[],ke=[],B=0;B<v-1;B++)for(var Q=0;Q<p-1;Q++){var ie=B*(p-1)+Q,ae=ie*4;T(B,Q,A);for(var q=0;q<4;q++){for(var Ae=0;Ae<4;Ae++)Ye[Ae]=Z[A[q]*4+Ae];c.set(ae+q,Ye),m&&(I(V,A[q],N),h.set(ae+q,N));var Me=A[q];ke[0]=Me%p/(p-1),ke[1]=Math.floor(Me/p)/(v-1),f.set(ae+q,ke)}ie++}}else{for(var ke=[],B=0;B<a.count();B++){ke[0]=B%p/(p-1),ke[1]=Math.floor(B/p)/(v-1);var Ye=S.parseColor(Ze(a,B)),$=je(a,B);$!=null&&(Ye[3]*=$),Ye[3]<.99&&(b=!0),c.set(B,Ye),f.set(B,ke)}for(var A=[],Di=0,B=0;B<v-1;B++)for(var Q=0;Q<p-1;Q++){T(B,Q,A);for(var q=0;q<6;q++)w[Di++]=A[y[q]]}m?n.generateVertexNormals():h.value=null}e.material.get("normalMap")&&n.generateTangents(),n.updateBoundingBox(),n.dirty(),e.material.transparent=b,e.material.depthMask=!b},_getDataShape:function(e,t){for(var r=-1/0,i=0,n=0,a=!1,o=t?"u":"x",s=e.count(),l=0;l<s;l++){var u=e.get(o,l);u<r&&(n=0,i++),r=u,n++}if((!i||n===1)&&(a=!0),!a)return[i+1,n];for(var h=Math.floor(Math.sqrt(s));h>0;){if(Math.floor(s/h)===s/h)return[h,s/h];h--}return h=Math.floor(Math.sqrt(s)),[h,h]},dispose:function(){this.groupGL.removeAll()},remove:function(){this.groupGL.removeAll()}});function dy(e){e.registerChartView(cy),e.registerSeriesModel(Vf),e.registerLayout(function(t,r){t.eachSeriesByType("surface",function(i){var n=i.coordinateSystem;!n||n.type;var a=i.getData(),o=new Float32Array(3*a.count()),s=[NaN,NaN,NaN];if(n&&n.type==="cartesian3D"){var l=n.dimensions,u=l.map(function(h){return i.coordDimToDataDim(h)[0]});a.each(u,function(h,f,d,c){var v;a.hasValue(c)?v=n.dataToPoint([h,f,d]):v=s,o[c*3]=v[0],o[c*3+1]=v[1],o[c*3+2]=v[2]})}a.setLayout("points",o)})})}Ne(dy);function Gu(e,t){for(var r=[],i=0;i<t.length;i++)r.push(e.dataToPoint(t[i]));return r}var Mi=ft.extend({type:"series.map3D",layoutMode:"box",coordinateSystem:null,visualStyleAccessPath:"itemStyle",optionUpdated:function(e){var t=this.get("coordinateSystem");t==null||t==="geo3D"||(this.get("groundPlane.show")&&(this.option.groundPlane.show=!1),this._geo=null)},getInitialData:function(e){e.data=this.getFilledRegions(e.data,e.map);var t=vn(e.data,{coordDimensions:["value"]}),r=new Nt(t,this);r.initData(e.data);var i={};return r.each(function(n){var a=r.getName(n),o=r.getItemModel(n);i[a]=o}),this._regionModelMap=i,r},formatTooltip:function(e){return yn(this,e)},getRegionModel:function(e){var t=this.getData().getName(e);return this._regionModelMap[t]||new zr(null,this)},getRegionPolygonCoords:function(e){var t=this.coordinateSystem,r=this.getData().getName(e);if(t.transform){var i=t.getRegion(r);return i?i.geometries:[]}else{this._geo||(this._geo=hs.createGeo3D(this));for(var i=this._geo.getRegion(r),n=[],a=0;a<i.geometries.length;a++){var o=i.geometries[a],s=[],l=Gu(t,o.exterior);if(s&&s.length)for(var u=0;u<o.interiors.length;u++)s.push(Gu(t,s[u]));n.push({interiors:s,exterior:l})}return n}},getFormattedLabel:function(e,t){var r=wr.getFormattedLabel(this,e,t);return r==null&&(r=this.getData().getName(e)),r},defaultOption:{coordinateSystem:"geo3D",data:null}});le(Mi.prototype,yf);le(Mi.prototype,ga);le(Mi.prototype,bi);le(Mi.prototype,Ai);le(Mi.prototype,Li);const vy=it.extend({type:"map3D",__ecgl__:!0,init:function(e,t){this._geo3DBuilder=new Ti(t),this.groupGL=new S.Node},render:function(e,t,r){var i=e.coordinateSystem;if(!(!i||!i.viewGL)){if(this.groupGL.add(this._geo3DBuilder.rootNode),i.viewGL.add(this.groupGL),i.type==="geo3D"){this._sceneHelper||(this._sceneHelper=new mr,this._sceneHelper.initLight(this.groupGL)),this._sceneHelper.setScene(i.viewGL.scene),this._sceneHelper.updateLight(e),i.viewGL.setPostEffect(e.getModel("postEffect"),r),i.viewGL.setTemporalSuperSampling(e.getModel("temporalSuperSampling"));var n=this._control;n||(n=this._control=new gn({zr:r.getZr()}),this._control.init());var a=e.getModel("viewControl");n.setViewGL(i.viewGL),n.setFromViewControlModel(a,0),n.off("update"),n.on("update",function(){r.dispatchAction({type:"map3DChangeCamera",alpha:n.getAlpha(),beta:n.getBeta(),distance:n.getDistance(),from:this.uid,map3DId:e.id})}),this._geo3DBuilder.extrudeY=!0}else this._control&&(this._control.dispose(),this._control=null),this._sceneHelper&&(this._sceneHelper.dispose(),this._sceneHelper=null),e.getData().getLayout("geo3D"),this._geo3DBuilder.extrudeY=!1;this._geo3DBuilder.update(e,t,r,0,e.getData().count());var o=i.viewGL.isLinearSpace()?"define":"undefine";this._geo3DBuilder.rootNode.traverse(function(s){s.material&&s.material[o]("fragment","SRGB_DECODE")})}},afterRender:function(e,t,r,i){var n=i.renderer,a=e.coordinateSystem;a&&a.type==="geo3D"&&(this._sceneHelper.updateAmbientCubemap(n,e,r),this._sceneHelper.updateSkybox(n,e,r))},dispose:function(){this.groupGL.removeAll(),this._control.dispose(),this._geo3DBuilder.dispose()}});function py(e){Lf(e),e.registerChartView(vy),e.registerSeriesModel(Mi),e.registerAction({type:"map3DChangeCamera",event:"map3dcamerachanged",update:"series:updateCamera"},function(t,r){r.eachComponent({mainType:"series",subType:"map3D",query:t},function(i){i.setView(t)})})}Ne(py);const gy=ft.extend({type:"series.scatterGL",dependencies:["grid","polar","geo","singleAxis"],visualStyleAccessPath:"itemStyle",hasSymbolVisual:!0,getInitialData:function(){return Rd(this)},defaultOption:{coordinateSystem:"cartesian2d",zlevel:10,progressive:1e5,progressiveThreshold:1e5,large:!1,symbol:"circle",symbolSize:10,zoomScale:0,blendMode:"source-over",itemStyle:{opacity:.8},postEffect:{enable:!1,colorCorrection:{exposure:0,brightness:0,contrast:1,saturation:1,enable:!0}}}});function ir(e){this.viewGL=e}ir.prototype.reset=function(e,t){this._updateCamera(t.getWidth(),t.getHeight(),t.getDevicePixelRatio()),this._viewTransform=vd(),this.updateTransform(e,t)};ir.prototype.updateTransform=function(e,t){var r=e.coordinateSystem;r.getRoamTransform&&(Bo(this._viewTransform,r.getRoamTransform()),this._setCameraTransform(this._viewTransform),t.getZr().refresh())};ir.prototype.dataToPoint=function(e,t,r){r=e.dataToPoint(t,null,r);var i=this._viewTransform;i&&fi(r,r,i)};ir.prototype.removeTransformInPoint=function(e){return this._viewTransform&&fi(e,e,this._viewTransform),e};ir.prototype.getZoom=function(){if(this._viewTransform){var e=this._viewTransform;return 1/Math.max(Math.sqrt(e[0]*e[0]+e[1]*e[1]),Math.sqrt(e[2]*e[2]+e[3]*e[3]))}return 1};ir.prototype._setCameraTransform=function(e){var t=this.viewGL.camera;t.position.set(e[4],e[5],0),t.scale.set(Math.sqrt(e[0]*e[0]+e[1]*e[1]),Math.sqrt(e[2]*e[2]+e[3]*e[3]),1)};ir.prototype._updateCamera=function(e,t,r){this.viewGL.setViewport(0,0,e,t,r);var i=this.viewGL.camera;i.left=i.top=0,i.bottom=t,i.right=e,i.near=0,i.far=100};const my=it.extend({type:"scatterGL",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this.viewGL=new ge("orthographic"),this.viewGL.add(this.groupGL),this._pointsBuilderList=[],this._currentStep=0,this._sizeScale=1,this._glViewHelper=new ir(this.viewGL)},render:function(e,t,r){if(this.groupGL.removeAll(),this._glViewHelper.reset(e,r),!!e.getData().count()){var i=this._pointsBuilderList[0];i||(i=this._pointsBuilderList[0]=new Wr(!0,r)),this._pointsBuilderList.length=1,this.groupGL.add(i.rootNode),this._removeTransformInPoints(e.getData().getLayout("points")),i.update(e,t,r),this.viewGL.setPostEffect(e.getModel("postEffect"),r)}},incrementalPrepareRender:function(e,t,r){this.groupGL.removeAll(),this._glViewHelper.reset(e,r),this._currentStep=0,this.viewGL.setPostEffect(e.getModel("postEffect"),r)},incrementalRender:function(e,t,r,i){if(!(e.end<=e.start)){var n=this._pointsBuilderList[this._currentStep];n||(n=new Wr(!0,i),this._pointsBuilderList[this._currentStep]=n),this.groupGL.add(n.rootNode),this._removeTransformInPoints(t.getData().getLayout("points")),n.setSizeScale(this._sizeScale),n.update(t,r,i,e.start,e.end),i.getZr().refresh(),this._currentStep++}},updateTransform:function(e,t,r){if(e.coordinateSystem.getRoamTransform){this._glViewHelper.updateTransform(e,r);var i=this._glViewHelper.getZoom(),n=Math.max((e.get("zoomScale")||0)*(i-1)+1,0);this._sizeScale=n,this._pointsBuilderList.forEach(function(a){a.setSizeScale(n)})}},_removeTransformInPoints:function(e){if(e)for(var t=[],r=0;r<e.length;r+=2)t[0]=e[r],t[1]=e[r+1],this._glViewHelper.removeTransformInPoint(t),e[r]=t[0],e[r+1]=t[1]},dispose:function(){this.groupGL.removeAll(),this._pointsBuilderList.forEach(function(e){e.dispose()})},remove:function(){this.groupGL.removeAll()}});function _y(e){e.registerChartView(my),e.registerSeriesModel(gy),e.registerLayout({seriesType:"scatterGL",reset:function(t){var r=t.coordinateSystem,i=t.getData(),n;if(r){var a=r.dimensions.map(function(s){return i.mapDimension(s)}).slice(0,2),o=[];a.length===1?n=function(s){for(var l=new Float32Array((s.end-s.start)*2),u=s.start;u<s.end;u++){var h=(u-s.start)*2,f=i.get(a[0],u),d=r.dataToPoint(f);l[h]=d[0],l[h+1]=d[1]}i.setLayout("points",l)}:a.length===2&&(n=function(s){for(var l=new Float32Array((s.end-s.start)*2),u=s.start;u<s.end;u++){var h=(u-s.start)*2,f=i.get(a[0],u),d=i.get(a[1],u);o[0]=f,o[1]=d,o=r.dataToPoint(o),l[h]=o[0],l[h+1]=o[1]}i.setLayout("points",l)})}return{progress:n}}})}Ne(_y);function yy(e,t,r,i,n){for(var a=new Sp(i),o=0;o<e.length;o++)a.addNode(oe.firstNotNull(e[o].id,e[o].name,o),o);for(var s=[],l=[],u=0,o=0;o<t.length;o++){var h=t[o],f=h.source,d=h.target;a.addEdge(f,d,u)&&(l.push(h),s.push(oe.firstNotNull(h.id,f+" > "+d)),u++)}var c,v=vn(e,{coordDimensions:["value"]});c=new Nt(v,r),c.initData(e);var p=new Nt(["value"],r);return p.initData(l,s),n&&n(c,p),gp({mainData:c,struct:a,structAttr:"graph",datas:{node:c,edge:p},datasAttr:{node:"data",edge:"edgeData"}}),a.update(),a}var Hi=ft.extend({type:"series.graphGL",visualStyleAccessPath:"itemStyle",hasSymbolVisual:!0,init:function(e){Hi.superApply(this,"init",arguments),this.legendDataProvider=function(){return this._categoriesData},this._updateCategoriesData()},mergeOption:function(e){Hi.superApply(this,"mergeOption",arguments),this._updateCategoriesData()},getFormattedLabel:function(e,t,r,i){var n=wr.getFormattedLabel(this,e,t,r,i);if(n==null){var a=this.getData(),o=a.dimensions[a.dimensions.length-1];n=a.get(o,e)}return n},getInitialData:function(e,t){var r=e.edges||e.links||[],i=e.data||e.nodes||[],n=this;if(i&&r)return yy(i,r,this,!0,a).data;function a(o,s){o.wrapMethod("getItemModel",function(f){const d=n._categoriesModels,c=f.getShallow("category"),v=d[c];return v&&(v.parentModel=f.parentModel,f.parentModel=v),f});const l=t.getModel([]).getModel;function u(f,d){const c=l.call(this,f,d);return c.resolveParentPath=h,c}s.wrapMethod("getItemModel",function(f){return f.resolveParentPath=h,f.getModel=u,f});function h(f){if(f&&(f[0]==="label"||f[1]==="label")){const d=f.slice();return f[0]==="label"?d[0]="edgeLabel":f[1]==="label"&&(d[1]="edgeLabel"),d}return f}}},getGraph:function(){return this.getData().graph},getEdgeData:function(){return this.getGraph().edgeData},getCategoriesData:function(){return this._categoriesData},formatTooltip:function(e,t,r){if(r==="edge"){var i=this.getData(),n=this.getDataParams(e,r),a=i.graph.getEdgeByIndex(e),o=i.getName(a.node1.dataIndex),s=i.getName(a.node2.dataIndex),l=[];return o!=null&&l.push(o),s!=null&&l.push(s),l=oi(l.join(" > ")),n.value&&(l+=" : "+oi(n.value)),l}else return Hi.superApply(this,"formatTooltip",arguments)},_updateCategoriesData:function(){var e=(this.option.categories||[]).map(function(r){return r.value!=null?r:Object.assign({value:0},r)}),t=new Nt(["value"],this);t.initData(e),this._categoriesData=t,this._categoriesModels=t.mapArray(function(r){return t.getItemModel(r,!0)})},setView:function(e){e.zoom!=null&&(this.option.zoom=e.zoom),e.offset!=null&&(this.option.offset=e.offset)},setNodePosition:function(e){for(var t=0;t<e.length/2;t++){var r=e[t*2],i=e[t*2+1],n=this.getData().getRawDataItem(t);n.x=r,n.y=i}},isAnimationEnabled:function(){return Hi.superCall(this,"isAnimationEnabled")&&!(this.get("layout")==="force"&&this.get("force.layoutAnimation"))},defaultOption:{zlevel:10,z:2,legendHoverLink:!0,layout:"forceAtlas2",forceAtlas2:{initLayout:null,GPU:!0,steps:1,maxSteps:1e3,repulsionByDegree:!0,linLogMode:!1,strongGravityMode:!1,gravity:1,edgeWeightInfluence:1,edgeWeight:[1,4],nodeWeight:[1,4],preventOverlap:!1,gravityCenter:null},focusNodeAdjacency:!0,focusNodeAdjacencyOn:"mouseover",left:"center",top:"center",symbol:"circle",symbolSize:5,roam:!1,center:null,zoom:1,label:{show:!1,formatter:"{b}",position:"right",distance:5,textStyle:{fontSize:14}},itemStyle:{},lineStyle:{color:"#aaa",width:1,opacity:.5},emphasis:{label:{show:!0}},animation:!1}}),Ge=Re.vec2,zu=[[0,0],[1,1]],gs=se.extend(function(){return{segmentScale:4,dynamic:!0,useNativeLine:!0,attributes:{position:new se.Attribute("position","float",2,"POSITION"),normal:new se.Attribute("normal","float",2),offset:new se.Attribute("offset","float",1),color:new se.Attribute("color","float",4,"COLOR")}}},{resetOffset:function(){this._vertexOffset=0,this._faceOffset=0,this._itemVertexOffsets=[]},setVertexCount:function(e){var t=this.attributes;this.vertexCount!==e&&(t.position.init(e),t.color.init(e),this.useNativeLine||(t.offset.init(e),t.normal.init(e)),e>65535?this.indices instanceof Uint16Array&&(this.indices=new Uint32Array(this.indices)):this.indices instanceof Uint32Array&&(this.indices=new Uint16Array(this.indices)))},setTriangleCount:function(e){this.triangleCount!==e&&(e===0?this.indices=null:this.indices=this.vertexCount>65535?new Uint32Array(e*3):new Uint16Array(e*3))},_getCubicCurveApproxStep:function(e,t,r,i){var n=Ge.dist(e,t)+Ge.dist(r,t)+Ge.dist(i,r),a=1/(n+1)*this.segmentScale;return a},getCubicCurveVertexCount:function(e,t,r,i){var n=this._getCubicCurveApproxStep(e,t,r,i),a=Math.ceil(1/n);return this.useNativeLine?a*2:a*2+2},getCubicCurveTriangleCount:function(e,t,r,i){var n=this._getCubicCurveApproxStep(e,t,r,i),a=Math.ceil(1/n);return this.useNativeLine?0:a*2},getLineVertexCount:function(){return this.getPolylineVertexCount(zu)},getLineTriangleCount:function(){return this.getPolylineTriangleCount(zu)},getPolylineVertexCount:function(e){var t;if(typeof e=="number")t=e;else{var r=typeof e[0]!="number";t=r?e.length:e.length/2}return this.useNativeLine?(t-1)*2:(t-1)*2+2},getPolylineTriangleCount:function(e){var t;if(typeof e=="number")t=e;else{var r=typeof e[0]!="number";t=r?e.length:e.length/2}return this.useNativeLine?0:(t-1)*2},addCubicCurve:function(e,t,r,i,n,a){a==null&&(a=1);for(var o=e[0],s=e[1],l=t[0],u=t[1],h=r[0],f=r[1],d=i[0],c=i[1],v=this._getCubicCurveApproxStep(e,t,r,i),p=v*v,_=p*v,m=3*v,g=3*p,y=6*p,x=6*_,w=o-l*2+h,T=s-u*2+f,b=(l-h)*3-o+d,A=(u-f)*3-s+c,C=o,D=s,L=(l-o)*m+w*g+b*_,M=(u-s)*m+T*g+A*_,P=w*y+b*x,N=T*y+A*x,I=b*x,V=A*x,Z=0,B=0,$=Math.ceil(1/v),q=new Float32Array(($+1)*3),q=[],j=0,B=0;B<$+1;B++)q[j++]=C,q[j++]=D,C+=L,D+=M,L+=P,M+=N,P+=I,N+=V,Z+=v,Z>1&&(C=L>0?Math.min(C,d):Math.max(C,d),D=M>0?Math.min(D,c):Math.max(D,c));this.addPolyline(q,n,a)},addLine:function(e,t,r,i){this.addPolyline([e,t],r,i)},addPolyline:function(){var e=Ge.create(),t=Ge.create(),r=Ge.create(),i=Ge.create(),n=[],a=[],o=[];return function(s,l,u,h,f){if(s.length){var d=typeof s[0]!="number";if(f==null&&(f=d?s.length:s.length/2),!(f<2)){h==null&&(h=0),u==null&&(u=1),this._itemVertexOffsets.push(this._vertexOffset);for(var c=d?typeof l[0]!="number":l.length/4===f,v=this.attributes.position,p=this.attributes.color,_=this.attributes.offset,m=this.attributes.normal,g=this.indices,y=this._vertexOffset,x,w=0;w<f;w++){if(d)n=s[w+h],c?x=l[w+h]:x=l;else{var T=w*2+h;if(n=n||[],n[0]=s[T],n[1]=s[T+1],c){var b=w*4+h;x=x||[],x[0]=l[b],x[1]=l[b+1],x[2]=l[b+2],x[3]=l[b+3]}else x=l}if(this.useNativeLine)w>1&&(v.copy(y,y-1),p.copy(y,y-1),y++);else{var A;if(w<f-1){if(d)Ge.copy(a,s[w+1]);else{var T=(w+1)*2+h;a=a||[],a[0]=s[T],a[1]=s[T+1]}if(w>0){Ge.sub(e,n,o),Ge.sub(t,a,n),Ge.normalize(e,e),Ge.normalize(t,t),Ge.add(i,e,t),Ge.normalize(i,i);var C=u/2*Math.min(1/Ge.dot(e,i),2);r[0]=-i[1],r[1]=i[0],A=C}else Ge.sub(e,a,n),Ge.normalize(e,e),r[0]=-e[1],r[1]=e[0],A=u/2}else Ge.sub(e,n,o),Ge.normalize(e,e),r[0]=-e[1],r[1]=e[0],A=u/2;m.set(y,r),m.set(y+1,r),_.set(y,A),_.set(y+1,-A),Ge.copy(o,n),v.set(y,n),v.set(y+1,n),p.set(y,x),p.set(y+1,x),y+=2}if(this.useNativeLine)p.set(y,x),v.set(y,n),y++;else if(w>0){var D=this._faceOffset*3,g=this.indices;g[D]=y-4,g[D+1]=y-3,g[D+2]=y-2,g[D+3]=y-3,g[D+4]=y-1,g[D+5]=y-2,this._faceOffset+=2}}this._vertexOffset=y}}}}(),setItemColor:function(e,t){for(var r=this._itemVertexOffsets[e],i=e<this._itemVertexOffsets.length-1?this._itemVertexOffsets[e+1]:this._vertexOffset,n=r;n<i;n++)this.attributes.color.set(n,t);this.dirty("color")}});He(gs.prototype,mn);const xy=`@export ecgl.forceAtlas2.updateNodeRepulsion

#define NODE_COUNT 0

uniform sampler2D positionTex;

uniform vec2 textureSize;
uniform float gravity;
uniform float scaling;
uniform vec2 gravityCenter;

uniform bool strongGravityMode;
uniform bool preventOverlap;

varying vec2 v_Texcoord;

void main() {

 vec4 n0 = texture2D(positionTex, v_Texcoord);

 vec2 force = vec2(0.0);
 for (int i = 0; i < NODE_COUNT; i++) {
 vec2 uv = vec2(
 mod(float(i), textureSize.x) / (textureSize.x - 1.0),
 floor(float(i) / textureSize.x) / (textureSize.y - 1.0)
 );
 vec4 n1 = texture2D(positionTex, uv);

 vec2 dir = n0.xy - n1.xy;
 float d2 = dot(dir, dir);

 if (d2 > 0.0) {
 float factor = 0.0;
 if (preventOverlap) {
 float d = sqrt(d2);
 d = d - n0.w - n1.w;
 if (d > 0.0) {
 factor = scaling * n0.z * n1.z / (d * d);
 }
 else if (d < 0.0) {
 factor = scaling * 100.0 * n0.z * n1.z;
 }
 }
 else {
 factor = scaling * n0.z * n1.z / d2;
 }
 force += dir * factor;
 }
 }

 vec2 dir = gravityCenter - n0.xy;
 float d = 1.0;
 if (!strongGravityMode) {
 d = length(dir);
 }

 force += dir * n0.z * gravity / (d + 1.0);

 gl_FragColor = vec4(force, 0.0, 1.0);
}
@end

@export ecgl.forceAtlas2.updateEdgeAttraction.vertex

attribute vec2 node1;
attribute vec2 node2;
attribute float weight;

uniform sampler2D positionTex;
uniform float edgeWeightInfluence;
uniform bool preventOverlap;
uniform bool linLogMode;

uniform vec2 windowSize: WINDOW_SIZE;

varying vec2 v_Force;

void main() {

 vec4 n0 = texture2D(positionTex, node1);
 vec4 n1 = texture2D(positionTex, node2);

 vec2 dir = n1.xy - n0.xy;
 float d = length(dir);
 float w;
 if (edgeWeightInfluence == 0.0) {
 w = 1.0;
 }
 else if (edgeWeightInfluence == 1.0) {
 w = weight;
 }
 else {
 w = pow(weight, edgeWeightInfluence);
 }
 vec2 offset = vec2(1.0 / windowSize.x, 1.0 / windowSize.y);
 vec2 scale = vec2((windowSize.x - 1.0) / windowSize.x, (windowSize.y - 1.0) / windowSize.y);
 vec2 pos = node1 * scale * 2.0 - 1.0;
 gl_Position = vec4(pos + offset, 0.0, 1.0);
 gl_PointSize = 1.0;

 float factor;
 if (preventOverlap) {
 d = d - n1.w - n0.w;
 }
 if (d <= 0.0) {
 v_Force = vec2(0.0);
 return;
 }

 if (linLogMode) {
 factor = w * log(d) / d;
 }
 else {
 factor = w;
 }
 v_Force = dir * factor;
}
@end

@export ecgl.forceAtlas2.updateEdgeAttraction.fragment

varying vec2 v_Force;

void main() {
 gl_FragColor = vec4(v_Force, 0.0, 0.0);
}
@end

@export ecgl.forceAtlas2.calcWeightedSum.vertex

attribute vec2 node;

varying vec2 v_NodeUv;

void main() {

 v_NodeUv = node;
 gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
 gl_PointSize = 1.0;
}
@end

@export ecgl.forceAtlas2.calcWeightedSum.fragment

varying vec2 v_NodeUv;

uniform sampler2D positionTex;
uniform sampler2D forceTex;
uniform sampler2D forcePrevTex;

void main() {
 vec2 force = texture2D(forceTex, v_NodeUv).rg;
 vec2 forcePrev = texture2D(forcePrevTex, v_NodeUv).rg;

 float mass = texture2D(positionTex, v_NodeUv).z;
 float swing = length(force - forcePrev) * mass;
 float traction = length(force + forcePrev) * 0.5 * mass;

 gl_FragColor = vec4(swing, traction, 0.0, 0.0);
}
@end

@export ecgl.forceAtlas2.calcGlobalSpeed

uniform sampler2D globalSpeedPrevTex;
uniform sampler2D weightedSumTex;
uniform float jitterTolerence;

void main() {
 vec2 weightedSum = texture2D(weightedSumTex, vec2(0.5)).xy;
 float prevGlobalSpeed = texture2D(globalSpeedPrevTex, vec2(0.5)).x;
 float globalSpeed = jitterTolerence * jitterTolerence
 * weightedSum.y / weightedSum.x;
 if (prevGlobalSpeed > 0.0) {
 globalSpeed = min(globalSpeed / prevGlobalSpeed, 1.5) * prevGlobalSpeed;
 }
 gl_FragColor = vec4(globalSpeed, 0.0, 0.0, 1.0);
}
@end

@export ecgl.forceAtlas2.updatePosition

uniform sampler2D forceTex;
uniform sampler2D forcePrevTex;
uniform sampler2D positionTex;
uniform sampler2D globalSpeedTex;

varying vec2 v_Texcoord;

void main() {
 vec2 force = texture2D(forceTex, v_Texcoord).xy;
 vec2 forcePrev = texture2D(forcePrevTex, v_Texcoord).xy;
 vec4 node = texture2D(positionTex, v_Texcoord);

 float globalSpeed = texture2D(globalSpeedTex, vec2(0.5)).r;
 float swing = length(force - forcePrev);
 float speed = 0.1 * globalSpeed / (0.1 + globalSpeed * sqrt(swing));

 float df = length(force);
 if (df > 0.0) {
 speed = min(df * speed, 10.0) / df;

 gl_FragColor = vec4(node.xy + speed * force, node.zw);
 }
 else {
 gl_FragColor = node;
 }
}
@end

@export ecgl.forceAtlas2.edges.vertex
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

attribute vec2 node;
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;

uniform sampler2D positionTex;

void main()
{
 gl_Position = worldViewProjection * vec4(
 texture2D(positionTex, node).xy, -10.0, 1.0
 );
 v_Color = a_Color;
}
@end

@export ecgl.forceAtlas2.edges.fragment
uniform vec4 color : [1.0, 1.0, 1.0, 1.0];
varying vec4 v_Color;
void main() {
 gl_FragColor = color * v_Color;
}
@end`;S.Shader.import(xy);var uo={repulsionByDegree:!0,linLogMode:!1,strongGravityMode:!1,gravity:1,scaling:1,edgeWeightInfluence:1,jitterTolerence:.1,preventOverlap:!1,dissuadeHubs:!1,gravityCenter:null};function Ve(e){var t={type:S.Texture.FLOAT,minFilter:S.Texture.NEAREST,magFilter:S.Texture.NEAREST};this._positionSourceTex=new S.Texture2D(t),this._positionSourceTex.flipY=!1,this._positionTex=new S.Texture2D(t),this._positionPrevTex=new S.Texture2D(t),this._forceTex=new S.Texture2D(t),this._forcePrevTex=new S.Texture2D(t),this._weightedSumTex=new S.Texture2D(t),this._weightedSumTex.width=this._weightedSumTex.height=1,this._globalSpeedTex=new S.Texture2D(t),this._globalSpeedPrevTex=new S.Texture2D(t),this._globalSpeedTex.width=this._globalSpeedTex.height=1,this._globalSpeedPrevTex.width=this._globalSpeedPrevTex.height=1,this._nodeRepulsionPass=new Oe({fragment:S.Shader.source("ecgl.forceAtlas2.updateNodeRepulsion")}),this._positionPass=new Oe({fragment:S.Shader.source("ecgl.forceAtlas2.updatePosition")}),this._globalSpeedPass=new Oe({fragment:S.Shader.source("ecgl.forceAtlas2.calcGlobalSpeed")}),this._copyPass=new Oe({fragment:S.Shader.source("clay.compositor.output")});var r=function(i){i.blendEquation(i.FUNC_ADD),i.blendFunc(i.ONE,i.ONE)};this._edgeForceMesh=new S.Mesh({geometry:new S.Geometry({attributes:{node1:new S.Geometry.Attribute("node1","float",2),node2:new S.Geometry.Attribute("node2","float",2),weight:new S.Geometry.Attribute("weight","float",1)},dynamic:!0,mainAttribute:"node1"}),material:new S.Material({transparent:!0,shader:S.createShader("ecgl.forceAtlas2.updateEdgeAttraction"),blend:r,depthMask:!1,depthText:!1}),mode:S.Mesh.POINTS}),this._weightedSumMesh=new S.Mesh({geometry:new S.Geometry({attributes:{node:new S.Geometry.Attribute("node","float",2)},dynamic:!0,mainAttribute:"node"}),material:new S.Material({transparent:!0,shader:S.createShader("ecgl.forceAtlas2.calcWeightedSum"),blend:r,depthMask:!1,depthText:!1}),mode:S.Mesh.POINTS}),this._framebuffer=new Ie({depthBuffer:!1}),this._dummyCamera=new S.OrthographicCamera({left:-1,right:1,top:1,bottom:-1,near:0,far:100}),this._globalSpeed=0}Ve.prototype.updateOption=function(e){for(var t in uo)this[t]=uo[t];var r=this._nodes.length;if(r>5e4?this.jitterTolerence=10:r>5e3?this.jitterTolerence=1:this.jitterTolerence=.1,r>100?this.scaling=2:this.scaling=10,e)for(var t in uo)e[t]!=null&&(this[t]=e[t]);if(this.repulsionByDegree)for(var i=this._positionSourceTex.pixels,n=0;n<this._nodes.length;n++)i[n*4+2]=(this._nodes[n].degree||0)+1};Ve.prototype._updateGravityCenter=function(e){var t=this._nodes,r=this._edges;if(this.gravityCenter)this._gravityCenter=this.gravityCenter;else{for(var i=[1/0,1/0],n=[-1/0,-1/0],a=0;a<t.length;a++)i[0]=Math.min(t[a].x,i[0]),i[1]=Math.min(t[a].y,i[1]),n[0]=Math.max(t[a].x,n[0]),n[1]=Math.max(t[a].y,n[1]);this._gravityCenter=[(i[0]+n[0])*.5,(i[1]+n[1])*.5]}for(var a=0;a<r.length;a++){var o=r[a].node1,s=r[a].node2;t[o].degree=(t[o].degree||0)+1,t[s].degree=(t[s].degree||0)+1}};Ve.prototype.initData=function(e,t){this._nodes=e,this._edges=t,this._updateGravityCenter();var r=Math.ceil(Math.sqrt(e.length)),i=r,n=new Float32Array(r*i*4);this._resize(r,i);for(var a=0,o=0;o<e.length;o++){var s=e[o];n[a++]=s.x||0,n[a++]=s.y||0,n[a++]=s.mass||1,n[a++]=s.size||1}this._positionSourceTex.pixels=n;var l=this._edgeForceMesh.geometry,u=t.length;l.attributes.node1.init(u*2),l.attributes.node2.init(u*2),l.attributes.weight.init(u*2);for(var h=[],o=0;o<t.length;o++){var f=l.attributes,d=t[o].weight;d==null&&(d=1),f.node1.set(o,this.getNodeUV(t[o].node1,h)),f.node2.set(o,this.getNodeUV(t[o].node2,h)),f.weight.set(o,d),f.node1.set(o+u,this.getNodeUV(t[o].node2,h)),f.node2.set(o+u,this.getNodeUV(t[o].node1,h)),f.weight.set(o+u,d)}var c=this._weightedSumMesh.geometry;c.attributes.node.init(e.length);for(var o=0;o<e.length;o++)c.attributes.node.set(o,this.getNodeUV(o,h));l.dirty(),c.dirty(),this._nodeRepulsionPass.material.define("fragment","NODE_COUNT",e.length),this._nodeRepulsionPass.material.setUniform("textureSize",[r,i]),this._inited=!1,this._frame=0};Ve.prototype.getNodes=function(){return this._nodes};Ve.prototype.getEdges=function(){return this._edges};Ve.prototype.step=function(e){this._inited||(this._initFromSource(e),this._inited=!0),this._frame++,this._framebuffer.attach(this._forceTex),this._framebuffer.bind(e);var t=this._nodeRepulsionPass;t.setUniform("strongGravityMode",this.strongGravityMode),t.setUniform("gravity",this.gravity),t.setUniform("gravityCenter",this._gravityCenter),t.setUniform("scaling",this.scaling),t.setUniform("preventOverlap",this.preventOverlap),t.setUniform("positionTex",this._positionPrevTex),t.render(e);var r=this._edgeForceMesh;r.material.set("linLogMode",this.linLogMode),r.material.set("edgeWeightInfluence",this.edgeWeightInfluence),r.material.set("preventOverlap",this.preventOverlap),r.material.set("positionTex",this._positionPrevTex),e.gl.enable(e.gl.BLEND),e.renderPass([r],this._dummyCamera),this._framebuffer.attach(this._weightedSumTex),e.gl.clearColor(0,0,0,0),e.gl.clear(e.gl.COLOR_BUFFER_BIT),e.gl.enable(e.gl.BLEND);var i=this._weightedSumMesh;i.material.set("positionTex",this._positionPrevTex),i.material.set("forceTex",this._forceTex),i.material.set("forcePrevTex",this._forcePrevTex),e.renderPass([i],this._dummyCamera),this._framebuffer.attach(this._globalSpeedTex);var n=this._globalSpeedPass;n.setUniform("globalSpeedPrevTex",this._globalSpeedPrevTex),n.setUniform("weightedSumTex",this._weightedSumTex),n.setUniform("jitterTolerence",this.jitterTolerence),e.gl.disable(e.gl.BLEND),n.render(e);var a=this._positionPass;this._framebuffer.attach(this._positionTex),a.setUniform("globalSpeedTex",this._globalSpeedTex),a.setUniform("positionTex",this._positionPrevTex),a.setUniform("forceTex",this._forceTex),a.setUniform("forcePrevTex",this._forcePrevTex),a.render(e),this._framebuffer.unbind(e),this._swapTexture()};Ve.prototype.update=function(e,t,r){t==null&&(t=1),t=Math.max(t,1);for(var i=0;i<t;i++)this.step(e);r&&r()};Ve.prototype.getNodePositionTexture=function(){return this._inited?this._positionPrevTex:this._positionSourceTex};Ve.prototype.getNodeUV=function(e,t){t=t||[];var r=this._positionTex.width,i=this._positionTex.height;return t[0]=e%r/(r-1),t[1]=Math.floor(e/r)/(i-1)||0,t};Ve.prototype.getNodePosition=function(e,t){var r=this._positionArr,i=this._positionTex.width,n=this._positionTex.height,a=i*n;(!r||r.length!==a*4)&&(r=this._positionArr=new Float32Array(a*4)),this._framebuffer.bind(e),this._framebuffer.attach(this._positionPrevTex),e.gl.readPixels(0,0,i,n,e.gl.RGBA,e.gl.FLOAT,r),this._framebuffer.unbind(e),t||(t=new Float32Array(this._nodes.length*2));for(var o=0;o<this._nodes.length;o++)t[o*2]=r[o*4],t[o*2+1]=r[o*4+1];return t};Ve.prototype.getTextureData=function(e,t){var r=this["_"+t+"Tex"],i=r.width,n=r.height;this._framebuffer.bind(e),this._framebuffer.attach(r);var a=new Float32Array(i*n*4);return e.gl.readPixels(0,0,i,n,e.gl.RGBA,e.gl.FLOAT,a),this._framebuffer.unbind(e),a};Ve.prototype.getTextureSize=function(){return{width:this._positionTex.width,height:this._positionTex.height}};Ve.prototype.isFinished=function(e){return this._frame>e};Ve.prototype._swapTexture=function(){var e=this._positionPrevTex;this._positionPrevTex=this._positionTex,this._positionTex=e;var e=this._forcePrevTex;this._forcePrevTex=this._forceTex,this._forceTex=e;var e=this._globalSpeedPrevTex;this._globalSpeedPrevTex=this._globalSpeedTex,this._globalSpeedTex=e};Ve.prototype._initFromSource=function(e){this._framebuffer.attach(this._positionPrevTex),this._framebuffer.bind(e),this._copyPass.setUniform("texture",this._positionSourceTex),this._copyPass.render(e),e.gl.clearColor(0,0,0,0),this._framebuffer.attach(this._forcePrevTex),e.gl.clear(e.gl.COLOR_BUFFER_BIT),this._framebuffer.attach(this._globalSpeedPrevTex),e.gl.clear(e.gl.COLOR_BUFFER_BIT),this._framebuffer.unbind(e)};Ve.prototype._resize=function(e,t){["_positionSourceTex","_positionTex","_positionPrevTex","_forceTex","_forcePrevTex"].forEach(function(r){this[r].width=e,this[r].height=t,this[r].dirty()},this)};Ve.prototype.dispose=function(e){this._framebuffer.dispose(e),this._copyPass.dispose(e),this._nodeRepulsionPass.dispose(e),this._positionPass.dispose(e),this._globalSpeedPass.dispose(e),this._edgeForceMesh.geometry.dispose(e),this._weightedSumMesh.geometry.dispose(e),this._positionSourceTex.dispose(e),this._positionTex.dispose(e),this._positionPrevTex.dispose(e),this._forceTex.dispose(e),this._forcePrevTex.dispose(e),this._weightedSumTex.dispose(e),this._globalSpeedTex.dispose(e),this._globalSpeedPrevTex.dispose(e)};function Ty(){var e={create:function(){return new Float32Array(2)},dist:function(l,u){var h=u[0]-l[0],f=u[1]-l[1];return Math.sqrt(h*h+f*f)},len:function(l){var u=l[0],h=l[1];return Math.sqrt(u*u+h*h)},scaleAndAdd:function(l,u,h,f){return l[0]=u[0]+h[0]*f,l[1]=u[1]+h[1]*f,l},scale:function(l,u,h){return l[0]=u[0]*h,l[1]=u[1]*h,l},add:function(l,u,h){return l[0]=u[0]+h[0],l[1]=u[1]+h[1],l},sub:function(l,u,h){return l[0]=u[0]-h[0],l[1]=u[1]-h[1],l},normalize:function(l,u){var h=u[0],f=u[1],d=h*h+f*f;return d>0&&(d=1/Math.sqrt(d),l[0]=u[0]*d,l[1]=u[1]*d),l},negate:function(l,u){return l[0]=-u[0],l[1]=-u[1],l},copy:function(l,u){return l[0]=u[0],l[1]=u[1],l},set:function(l,u,h){return l[0]=u,l[1]=h,l}};function t(){this.subRegions=[],this.nSubRegions=0,this.node=null,this.mass=0,this.centerOfMass=null,this.bbox=new Float32Array(4),this.size=0}var r=t.prototype;r.beforeUpdate=function(){for(var l=0;l<this.nSubRegions;l++)this.subRegions[l].beforeUpdate();this.mass=0,this.centerOfMass&&(this.centerOfMass[0]=0,this.centerOfMass[1]=0),this.nSubRegions=0,this.node=null},r.afterUpdate=function(){this.subRegions.length=this.nSubRegions;for(var l=0;l<this.nSubRegions;l++)this.subRegions[l].afterUpdate()},r.addNode=function(l){if(this.nSubRegions===0)if(this.node==null){this.node=l;return}else this._addNodeToSubRegion(this.node),this.node=null;this._addNodeToSubRegion(l),this._updateCenterOfMass(l)},r.findSubRegion=function(l,u){for(var h=0;h<this.nSubRegions;h++){var f=this.subRegions[h];if(f.contain(l,u))return f}},r.contain=function(l,u){return this.bbox[0]<=l&&this.bbox[2]>=l&&this.bbox[1]<=u&&this.bbox[3]>=u},r.setBBox=function(l,u,h,f){this.bbox[0]=l,this.bbox[1]=u,this.bbox[2]=h,this.bbox[3]=f,this.size=(h-l+f-u)/2},r._newSubRegion=function(){var l=this.subRegions[this.nSubRegions];return l||(l=new t,this.subRegions[this.nSubRegions]=l),this.nSubRegions++,l},r._addNodeToSubRegion=function(l){var u=this.findSubRegion(l.position[0],l.position[1]),h=this.bbox;if(!u){var f=(h[0]+h[2])/2,d=(h[1]+h[3])/2,c=(h[2]-h[0])/2,v=(h[3]-h[1])/2,p=l.position[0]>=f?1:0,_=l.position[1]>=d?1:0,u=this._newSubRegion();u.setBBox(p*c+h[0],_*v+h[1],(p+1)*c+h[0],(_+1)*v+h[1])}u.addNode(l)},r._updateCenterOfMass=function(l){this.centerOfMass==null&&(this.centerOfMass=new Float32Array(2));var u=this.centerOfMass[0]*this.mass,h=this.centerOfMass[1]*this.mass;u+=l.position[0]*l.mass,h+=l.position[1]*l.mass,this.mass+=l.mass,this.centerOfMass[0]=u/this.mass,this.centerOfMass[1]=h/this.mass};function i(){this.position=new Float32Array(2),this.force=e.create(),this.forcePrev=e.create(),this.mass=1,this.inDegree=0,this.outDegree=0}function n(l,u){this.source=l,this.target=u,this.weight=1}function a(){this.autoSettings=!0,this.barnesHutOptimize=!0,this.barnesHutTheta=1.5,this.repulsionByDegree=!0,this.linLogMode=!1,this.strongGravityMode=!1,this.gravity=1,this.scaling=1,this.edgeWeightInfluence=1,this.jitterTolerence=.1,this.preventOverlap=!1,this.dissuadeHubs=!1,this.rootRegion=new t,this.rootRegion.centerOfMass=e.create(),this.nodes=[],this.edges=[],this.bbox=new Float32Array(4),this.gravityCenter=null,this._massArr=null,this._swingingArr=null,this._sizeArr=null,this._globalSpeed=0}var o=a.prototype;o.initNodes=function(l,u,h){var f=u.length;this.nodes.length=0;for(var d=typeof h<"u",c=0;c<f;c++){var v=new i;v.position[0]=l[c*2],v.position[1]=l[c*2+1],v.mass=u[c],d&&(v.size=h[c]),this.nodes.push(v)}this._massArr=u,this._swingingArr=new Float32Array(f),d&&(this._sizeArr=h)},o.initEdges=function(l,u){var h=l.length/2;this.edges.length=0;for(var f=0;f<h;f++){var d=l[f*2],c=l[f*2+1],v=this.nodes[d],p=this.nodes[c];if(!v||!p){console.error("Node not exists, try initNodes before initEdges");return}v.outDegree++,p.inDegree++;var _=new n(v,p);u&&(_.weight=u[f]),this.edges.push(_)}},o.updateSettings=function(){if(this.repulsionByDegree)for(var l=0;l<this.nodes.length;l++){var u=this.nodes[l];u.mass=u.inDegree+u.outDegree+1}else for(var l=0;l<this.nodes.length;l++){var u=this.nodes[l];u.mass=this._massArr[l]}},o.update=function(){var l=this.nodes.length;if(this.updateSettings(),this.updateBBox(),this.barnesHutOptimize){this.rootRegion.setBBox(this.bbox[0],this.bbox[1],this.bbox[2],this.bbox[3]),this.rootRegion.beforeUpdate();for(var u=0;u<l;u++)this.rootRegion.addNode(this.nodes[u]);this.rootRegion.afterUpdate()}for(var u=0;u<l;u++){var h=this.nodes[u];e.copy(h.forcePrev,h.force),e.set(h.force,0,0)}for(var u=0;u<l;u++){var f=this.nodes[u];if(this.barnesHutOptimize)this.applyRegionToNodeRepulsion(this.rootRegion,f);else for(var d=u+1;d<l;d++){var c=this.nodes[d];this.applyNodeToNodeRepulsion(f,c,!1)}this.gravity>0&&(this.strongGravityMode?this.applyNodeStrongGravity(f):this.applyNodeGravity(f))}for(var u=0;u<this.edges.length;u++)this.applyEdgeAttraction(this.edges[u]);for(var v=0,p=0,_=e.create(),u=0;u<l;u++){var h=this.nodes[u],m=e.dist(h.force,h.forcePrev);v+=m*h.mass,e.add(_,h.force,h.forcePrev);var g=e.len(_)*.5;p+=g*h.mass,this._swingingArr[u]=m}var y=this.jitterTolerence*this.jitterTolerence*p/v;this._globalSpeed>0&&(y=Math.min(y/this._globalSpeed,1.5)*this._globalSpeed),this._globalSpeed=y;for(var u=0;u<l;u++){var h=this.nodes[u],m=this._swingingArr[u],x=.1*y/(1+y*Math.sqrt(m)),w=e.len(h.force);w>0&&(x=Math.min(w*x,10)/w,e.scaleAndAdd(h.position,h.position,h.force,x))}},o.applyRegionToNodeRepulsion=function(){var l=e.create();return function(h,f){if(h.node)this.applyNodeToNodeRepulsion(h.node,f,!0);else{e.sub(l,f.position,h.centerOfMass);var d=l[0]*l[0]+l[1]*l[1];if(d>this.barnesHutTheta*h.size*h.size){var c=this.scaling*f.mass*h.mass/d;e.scaleAndAdd(f.force,f.force,l,c)}else for(var v=0;v<h.nSubRegions;v++)this.applyRegionToNodeRepulsion(h.subRegions[v],f)}}}(),o.applyNodeToNodeRepulsion=function(){var l=e.create();return function(h,f,d){if(h!=f){e.sub(l,h.position,f.position);var c=l[0]*l[0]+l[1]*l[1];if(c!==0){var v;if(this.preventOverlap){var p=Math.sqrt(c);if(p=p-h.size-f.size,p>0)v=this.scaling*h.mass*f.mass/(p*p);else if(p<0)v=this.scaling*100*h.mass*f.mass;else return}else v=this.scaling*h.mass*f.mass/c;e.scaleAndAdd(h.force,h.force,l,v),e.scaleAndAdd(f.force,f.force,l,-v)}}}}(),o.applyEdgeAttraction=function(){var l=e.create();return function(h){var f=h.source,d=h.target;e.sub(l,f.position,d.position);var c=e.len(l),v;this.edgeWeightInfluence===0?v=1:this.edgeWeightInfluence===1?v=h.weight:v=Math.pow(h.weight,this.edgeWeightInfluence);var p;this.preventOverlap&&(c=c-f.size-d.size,c<=0)||(this.linLogMode?p=-v*Math.log(c+1)/(c+1):p=-v,e.scaleAndAdd(f.force,f.force,l,p),e.scaleAndAdd(d.force,d.force,l,-p))}}(),o.applyNodeGravity=function(){var l=e.create();return function(u){e.sub(l,this.gravityCenter,u.position);var h=e.len(l);e.scaleAndAdd(u.force,u.force,l,this.gravity*u.mass/(h+1))}}(),o.applyNodeStrongGravity=function(){var l=e.create();return function(u){e.sub(l,this.gravityCenter,u.position),e.scaleAndAdd(u.force,u.force,l,this.gravity*u.mass)}}(),o.updateBBox=function(){for(var l=1/0,u=1/0,h=-1/0,f=-1/0,d=0;d<this.nodes.length;d++){var c=this.nodes[d].position;l=Math.min(l,c[0]),u=Math.min(u,c[1]),h=Math.max(h,c[0]),f=Math.max(f,c[1])}this.bbox[0]=l,this.bbox[1]=u,this.bbox[2]=h,this.bbox[3]=f},o.getGlobalSpeed=function(){return this._globalSpeed};var s=null;self.onmessage=function(l){switch(l.data.cmd){case"init":s=new a,s.initNodes(l.data.nodesPosition,l.data.nodesMass,l.data.nodesSize),s.initEdges(l.data.edges,l.data.edgesWeight);break;case"updateConfig":if(s)for(var u in l.data.config)s[u]=l.data.config[u];break;case"update":var h=l.data.steps;if(s){for(var f=0;f<h;f++)s.update();for(var d=s.nodes.length,c=new Float32Array(d*2),f=0;f<d;f++){var v=s.nodes[f];c[f*2]=v.position[0],c[f*2+1]=v.position[1]}self.postMessage({buffer:c.buffer,globalSpeed:s.getGlobalSpeed()},[c.buffer])}else{var p=new Float32Array;self.postMessage({buffer:p.buffer,globalSpeed:s.getGlobalSpeed()},[p.buffer])}break}}}var ki=Ty.toString();ki=ki.slice(ki.indexOf("{")+1,ki.lastIndexOf("}"));var Xi={barnesHutOptimize:!0,barnesHutTheta:1.5,repulsionByDegree:!0,linLogMode:!1,strongGravityMode:!1,gravity:1,scaling:1,edgeWeightInfluence:1,jitterTolerence:.1,preventOverlap:!1,dissuadeHubs:!1,gravityCenter:null},gt=function(e){for(var t in Xi)this[t]=Xi[t];if(e)for(var t in e)this[t]=e[t];this._nodes=[],this._edges=[],this._disposed=!1,this._positionTex=new ne({type:H.FLOAT,flipY:!1,minFilter:H.NEAREST,magFilter:H.NEAREST})};gt.prototype.initData=function(e,t){var r=new Blob([ki]),i=window.URL.createObjectURL(r);this._worker=new Worker(i),this._worker.onmessage=this._$onupdate.bind(this),this._nodes=e,this._edges=t,this._frame=0;for(var n=e.length,a=t.length,o=new Float32Array(n*2),s=new Float32Array(n),l=new Float32Array(n),u=new Float32Array(a*2),h=new Float32Array(a),f=0;f<e.length;f++){var d=e[f];o[f*2]=d.x,o[f*2+1]=d.y,s[f]=d.mass==null?1:d.mass,l[f]=d.size==null?1:d.size}for(var f=0;f<t.length;f++){var c=t[f],v=c.node1,p=c.node2;u[f*2]=v,u[f*2+1]=p,h[f]=c.weight==null?1:c.weight}var _=Math.ceil(Math.sqrt(e.length)),m=_,g=new Float32Array(_*m*4),y=this._positionTex;y.width=_,y.height=m,y.pixels=g,this._worker.postMessage({cmd:"init",nodesPosition:o,nodesMass:s,nodesSize:l,edges:u,edgesWeight:h}),this._globalSpeed=1/0};gt.prototype.updateOption=function(e){var t={};for(var r in Xi)t[r]=Xi[r];var i=this._nodes,n=this._edges,a=i.length;if(a>5e4?t.jitterTolerence=10:a>5e3?t.jitterTolerence=1:t.jitterTolerence=.1,a>100?t.scaling=2:t.scaling=10,a>1e3?t.barnesHutOptimize=!0:t.barnesHutOptimize=!1,e)for(var r in Xi)e[r]!=null&&(t[r]=e[r]);if(!t.gravityCenter){for(var o=[1/0,1/0],s=[-1/0,-1/0],l=0;l<i.length;l++)o[0]=Math.min(i[l].x,o[0]),o[1]=Math.min(i[l].y,o[1]),s[0]=Math.max(i[l].x,s[0]),s[1]=Math.max(i[l].y,s[1]);t.gravityCenter=[(o[0]+s[0])*.5,(o[1]+s[1])*.5]}for(var l=0;l<n.length;l++){var u=n[l].node1,h=n[l].node2;i[u].degree=(i[u].degree||0)+1,i[h].degree=(i[h].degree||0)+1}this._worker&&this._worker.postMessage({cmd:"updateConfig",config:t})};gt.prototype.update=function(e,t,r){t==null&&(t=1),t=Math.max(t,1),this._frame+=t,this._onupdate=r,this._worker&&this._worker.postMessage({cmd:"update",steps:Math.round(t)})};gt.prototype._$onupdate=function(e){if(!this._disposed){var t=new Float32Array(e.data.buffer);this._globalSpeed=e.data.globalSpeed,this._positionArr=t,this._updateTexture(t),this._onupdate&&this._onupdate()}};gt.prototype.getNodePositionTexture=function(){return this._positionTex};gt.prototype.getNodeUV=function(e,t){t=t||[];var r=this._positionTex.width,i=this._positionTex.height;return t[0]=e%r/(r-1),t[1]=Math.floor(e/r)/(i-1),t};gt.prototype.getNodes=function(){return this._nodes};gt.prototype.getEdges=function(){return this._edges};gt.prototype.isFinished=function(e){return this._frame>e};gt.prototype.getNodePosition=function(e,t){if(t||(t=new Float32Array(this._nodes.length*2)),this._positionArr)for(var r=0;r<this._positionArr.length;r++)t[r]=this._positionArr[r];return t};gt.prototype._updateTexture=function(e){for(var t=this._positionTex.pixels,r=0,i=0;i<e.length;)t[r++]=e[i++],t[r++]=e[i++],t[r++]=1,t[r++]=1;this._positionTex.dirty()};gt.prototype.dispose=function(e){this._disposed=!0,this._worker=null};var wy=Qe.extend(function(){return{zr:null,viewGL:null,minZoom:.2,maxZoom:5,_needsUpdate:!1,_dx:0,_dy:0,_zoom:1}},function(){this._mouseDownHandler=this._mouseDownHandler.bind(this),this._mouseWheelHandler=this._mouseWheelHandler.bind(this),this._mouseMoveHandler=this._mouseMoveHandler.bind(this),this._mouseUpHandler=this._mouseUpHandler.bind(this),this._update=this._update.bind(this)},{init:function(){var e=this.zr;e.on("mousedown",this._mouseDownHandler),e.on("mousewheel",this._mouseWheelHandler),e.on("globalout",this._mouseUpHandler),e.animation.on("frame",this._update)},setTarget:function(e){this._target=e},setZoom:function(e){this._zoom=Math.max(Math.min(e,this.maxZoom),this.minZoom),this._needsUpdate=!0},setOffset:function(e){this._dx=e[0],this._dy=e[1],this._needsUpdate=!0},getZoom:function(){return this._zoom},getOffset:function(){return[this._dx,this._dy]},_update:function(){if(this._target&&this._needsUpdate){var e=this._target,t=this._zoom;e.position.x=this._dx,e.position.y=this._dy,e.scale.set(t,t,t),this.zr.refresh(),this._needsUpdate=!1,this.trigger("update")}},_mouseDownHandler:function(e){if(!e.target){var t=e.offsetX,r=e.offsetY;if(!(this.viewGL&&!this.viewGL.containPoint(t,r))){this.zr.on("mousemove",this._mouseMoveHandler),this.zr.on("mouseup",this._mouseUpHandler);var i=this._convertPos(t,r);this._x=i.x,this._y=i.y}}},_convertPos:function(e,t){var r=this.viewGL.camera,i=this.viewGL.viewport;return{x:(e-i.x)/i.width*(r.right-r.left)+r.left,y:(t-i.y)/i.height*(r.bottom-r.top)+r.top}},_mouseMoveHandler:function(e){var t=this._convertPos(e.offsetX,e.offsetY);this._dx+=t.x-this._x,this._dy+=t.y-this._y,this._x=t.x,this._y=t.y,this._needsUpdate=!0},_mouseUpHandler:function(e){this.zr.off("mousemove",this._mouseMoveHandler),this.zr.off("mouseup",this._mouseUpHandler)},_mouseWheelHandler:function(e){e=e.event;var t=e.wheelDelta||-e.detail;if(t!==0){var r=e.offsetX,i=e.offsetY;if(!(this.viewGL&&!this.viewGL.containPoint(r,i))){var n=t>0?1.1:.9,a=Math.max(Math.min(this._zoom*n,this.maxZoom),this.minZoom);n=a/this._zoom;var o=this._convertPos(r,i),s=(o.x-this._dx)*(n-1),l=(o.y-this._dy)*(n-1);this._dx-=s,this._dy-=l,this._zoom=a,this._needsUpdate=!0}}},dispose:function(){var e=this.zr;e.off("mousedown",this._mouseDownHandler),e.off("mousemove",this._mouseMoveHandler),e.off("mouseup",this._mouseUpHandler),e.off("mousewheel",this._mouseWheelHandler),e.off("globalout",this._mouseUpHandler),e.animation.off("frame",this._update)}});const Sy=`@export ecgl.lines2D.vertex

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

attribute vec2 position: POSITION;
attribute vec4 a_Color : COLOR;
varying vec4 v_Color;

#ifdef POSITIONTEXTURE_ENABLED
uniform sampler2D positionTexture;
#endif

void main()
{
 gl_Position = worldViewProjection * vec4(position, -10.0, 1.0);

 v_Color = a_Color;
}

@end

@export ecgl.lines2D.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

varying vec4 v_Color;

void main()
{
 gl_FragColor = color * v_Color;
}
@end


@export ecgl.meshLines2D.vertex

attribute vec2 position: POSITION;
attribute vec2 normal;
attribute float offset;
attribute vec4 a_Color : COLOR;

uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;
uniform vec4 viewport : VIEWPORT;

varying vec4 v_Color;
varying float v_Miter;

void main()
{
 vec4 p2 = worldViewProjection * vec4(position + normal, -10.0, 1.0);
 gl_Position = worldViewProjection * vec4(position, -10.0, 1.0);

 p2.xy /= p2.w;
 gl_Position.xy /= gl_Position.w;

 vec2 N = normalize(p2.xy - gl_Position.xy);
 gl_Position.xy += N * offset / viewport.zw * 2.0;

 gl_Position.xy *= gl_Position.w;

 v_Color = a_Color;
}
@end


@export ecgl.meshLines2D.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];

varying vec4 v_Color;
varying float v_Miter;

void main()
{
 gl_FragColor = color * v_Color;
}

@end`;var Hn=Re.vec2;S.Shader.import(Sy);var by=1;const Ay=it.extend({type:"graphGL",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this.viewGL=new ge("orthographic"),this.viewGL.camera.left=this.viewGL.camera.right=0,this.viewGL.add(this.groupGL),this._pointsBuilder=new Wr(!0,t),this._forceEdgesMesh=new S.Mesh({material:new S.Material({shader:S.createShader("ecgl.forceAtlas2.edges"),transparent:!0,depthMask:!1,depthTest:!1}),$ignorePicking:!0,geometry:new S.Geometry({attributes:{node:new S.Geometry.Attribute("node","float",2),color:new S.Geometry.Attribute("color","float",4,"COLOR")},dynamic:!0,mainAttribute:"node"}),renderOrder:-1,mode:S.Mesh.LINES}),this._edgesMesh=new S.Mesh({material:new S.Material({shader:S.createShader("ecgl.meshLines2D"),transparent:!0,depthMask:!1,depthTest:!1}),$ignorePicking:!0,geometry:new gs({useNativeLine:!1,dynamic:!0}),renderOrder:-1,culling:!1}),this._layoutId=0,this._control=new wy({zr:t.getZr(),viewGL:this.viewGL}),this._control.setTarget(this.groupGL),this._control.init(),this._clickHandler=this._clickHandler.bind(this)},render:function(e,t,r){this.groupGL.add(this._pointsBuilder.rootNode),this._model=e,this._api=r,this._initLayout(e,t,r),this._pointsBuilder.update(e,t,r),this._forceLayoutInstance instanceof Ve||this.groupGL.remove(this._forceEdgesMesh),this._updateCamera(e,r),this._control.off("update"),this._control.on("update",function(){r.dispatchAction({type:"graphGLRoam",seriesId:e.id,zoom:this._control.getZoom(),offset:this._control.getOffset()}),this._pointsBuilder.updateView(this.viewGL.camera)},this),this._control.setZoom(oe.firstNotNull(e.get("zoom"),1)),this._control.setOffset(e.get("offset")||[0,0]);var i=this._pointsBuilder.getPointsMesh();if(i.off("mousemove",this._mousemoveHandler),i.off("mouseout",this._mouseOutHandler,this),r.getZr().off("click",this._clickHandler),this._pointsBuilder.highlightOnMouseover=!0,e.get("focusNodeAdjacency")){var n=e.get("focusNodeAdjacencyOn");n==="click"?r.getZr().on("click",this._clickHandler):n==="mouseover"&&(i.on("mousemove",this._mousemoveHandler,this),i.on("mouseout",this._mouseOutHandler,this),this._pointsBuilder.highlightOnMouseover=!1)}this._lastMouseOverDataIndex=-1},_clickHandler:function(e){if(!this._layouting){var t=this._pointsBuilder.getPointsMesh().dataIndex;t>=0?this._api.dispatchAction({type:"graphGLFocusNodeAdjacency",seriesId:this._model.id,dataIndex:t}):this._api.dispatchAction({type:"graphGLUnfocusNodeAdjacency",seriesId:this._model.id})}},_mousemoveHandler:function(e){if(!this._layouting){var t=this._pointsBuilder.getPointsMesh().dataIndex;t>=0?t!==this._lastMouseOverDataIndex&&this._api.dispatchAction({type:"graphGLFocusNodeAdjacency",seriesId:this._model.id,dataIndex:t}):this._mouseOutHandler(e),this._lastMouseOverDataIndex=t}},_mouseOutHandler:function(e){this._layouting||(this._api.dispatchAction({type:"graphGLUnfocusNodeAdjacency",seriesId:this._model.id}),this._lastMouseOverDataIndex=-1)},_updateForceEdgesGeometry:function(e,t){var r=this._forceEdgesMesh.geometry,i=t.getEdgeData(),n=0,a=this._forceLayoutInstance,o=i.count()*2;r.attributes.node.init(o),r.attributes.color.init(o),i.each(function(s){var l=e[s];r.attributes.node.set(n,a.getNodeUV(l.node1)),r.attributes.node.set(n+1,a.getNodeUV(l.node2));var u=Ze(i,l.dataIndex),h=S.parseColor(u);h[3]*=oe.firstNotNull(je(i,l.dataIndex),1),r.attributes.color.set(n,h),r.attributes.color.set(n+1,h),n+=2}),r.dirty()},_updateMeshLinesGeometry:function(){var t=this._model.getEdgeData(),e=this._edgesMesh.geometry,t=this._model.getEdgeData(),r=this._model.getData().getLayout("points");e.resetOffset(),e.setVertexCount(t.count()*e.getLineVertexCount()),e.setTriangleCount(t.count()*e.getLineTriangleCount());var i=[],n=[],a=["lineStyle","width"];this._originalEdgeColors=new Float32Array(t.count()*4),this._edgeIndicesMap=new Float32Array(t.count()),t.each(function(o){var s=t.graph.getEdgeByIndex(o),l=s.node1.dataIndex*2,u=s.node2.dataIndex*2;i[0]=r[l],i[1]=r[l+1],n[0]=r[u],n[1]=r[u+1];var h=Ze(t,s.dataIndex),f=S.parseColor(h);f[3]*=oe.firstNotNull(je(t,s.dataIndex),1);var d=t.getItemModel(s.dataIndex),c=oe.firstNotNull(d.get(a),1)*this._api.getDevicePixelRatio();e.addLine(i,n,f,c);for(var v=0;v<4;v++)this._originalEdgeColors[s.dataIndex*4+v]=f[v];this._edgeIndicesMap[s.dataIndex]=o},this),e.dirty()},_updateForceNodesGeometry:function(e){for(var t=this._pointsBuilder.getPointsMesh(),r=[],i=0;i<e.count();i++)this._forceLayoutInstance.getNodeUV(i,r),t.geometry.attributes.position.set(i,r);t.geometry.dirty("position")},_initLayout:function(e,t,r){var i=e.get("layout"),n=e.getGraph(),a=e.getBoxLayoutParams(),o=dn(a,{width:r.getWidth(),height:r.getHeight()});i==="force"&&(i="forceAtlas2"),this.stopLayout(e,t,r,{beforeLayout:!0});var s=e.getData(),l=e.getData();if(i==="forceAtlas2"){var u=e.getModel("forceAtlas2"),h=this._forceLayoutInstance,f=[],d=[],c=s.getDataExtent("value"),v=l.getDataExtent("value"),p=oe.firstNotNull(u.get("edgeWeight"),1),_=oe.firstNotNull(u.get("nodeWeight"),1);typeof p=="number"&&(p=[p,p]),typeof _=="number"&&(_=[_,_]);var m=0,g={},y=new Float32Array(s.count()*2);if(n.eachNode(function(w){var T=w.dataIndex,b=s.get("value",T),A,C;if(s.hasItemOption){var D=s.getItemModel(T);A=D.get("x"),C=D.get("y")}A==null&&(A=o.x+Math.random()*o.width,C=o.y+Math.random()*o.height),y[m*2]=A,y[m*2+1]=C,g[w.id]=m++;var L=Zn(b,c,_);isNaN(L)&&(isNaN(_[0])?L=1:L=_[0]),f.push({x:A,y:C,mass:L,size:s.getItemVisual(T,"symbolSize")})}),s.setLayout("points",y),n.eachEdge(function(w){var T=w.dataIndex,b=s.get("value",T),A=Zn(b,v,p);isNaN(A)&&(isNaN(p[0])?A=1:A=p[0]),d.push({node1:g[w.node1.id],node2:g[w.node2.id],weight:A,dataIndex:T})}),!h){var x=u.get("GPU");this._forceLayoutInstance&&(x&&!(this._forceLayoutInstance instanceof Ve)||!x&&!(this._forceLayoutInstance instanceof gt))&&(this._forceLayoutInstanceToDispose=this._forceLayoutInstance),h=this._forceLayoutInstance=x?new Ve:new gt}h.initData(f,d),h.updateOption(u.option),this._updateForceEdgesGeometry(h.getEdges(),e),this._updatePositionTexture(),r.dispatchAction({type:"graphGLStartLayout",from:this.uid})}else{var y=new Float32Array(s.count()*2),m=0;n.eachNode(function(b){var A=b.dataIndex,C,D;if(s.hasItemOption){var L=s.getItemModel(A);C=L.get("x"),D=L.get("y")}y[m++]=C,y[m++]=D}),s.setLayout("points",y),this._updateAfterLayout(e,t,r)}},_updatePositionTexture:function(){var e=this._forceLayoutInstance.getNodePositionTexture();this._pointsBuilder.setPositionTexture(e),this._forceEdgesMesh.material.set("positionTex",e)},startLayout:function(e,t,a,i){if(!(i&&i.from!=null&&i.from!==this.uid)){var n=this.viewGL,a=this._api,o=this._forceLayoutInstance,s=this._model.getData(),l=this._model.getModel("forceAtlas2");if(o&&(this.groupGL.remove(this._edgesMesh),this.groupGL.add(this._forceEdgesMesh),!!this._forceLayoutInstance)){this._updateForceNodesGeometry(e.getData()),this._pointsBuilder.hideLabels();var u=this,h=this._layoutId=by++,f=l.getShallow("maxSteps"),d=l.getShallow("steps"),c=0,v=Math.max(d*2,20),p=function(_){if(_===u._layoutId){if(o.isFinished(f)){a.dispatchAction({type:"graphGLStopLayout",from:u.uid}),a.dispatchAction({type:"graphGLFinishLayout",points:s.getLayout("points"),from:u.uid});return}o.update(n.layer.renderer,d,function(){u._updatePositionTexture(),c+=d,c>=v&&(u._syncNodePosition(e),c=0),a.getZr().refresh(),vo(function(){p(_)})})}};vo(function(){u._forceLayoutInstanceToDispose&&(u._forceLayoutInstanceToDispose.dispose(n.layer.renderer),u._forceLayoutInstanceToDispose=null),p(h)}),this._layouting=!0}}},stopLayout:function(e,t,r,i){i&&i.from!=null&&i.from!==this.uid||(this._layoutId=0,this.groupGL.remove(this._forceEdgesMesh),this.groupGL.add(this._edgesMesh),this._forceLayoutInstance&&this.viewGL.layer&&(i&&i.beforeLayout||(this._syncNodePosition(e),this._updateAfterLayout(e,t,r)),this._api.getZr().refresh(),this._layouting=!1))},_syncNodePosition:function(e){var t=this._forceLayoutInstance.getNodePosition(this.viewGL.layer.renderer);e.getData().setLayout("points",t),e.setNodePosition(t)},_updateAfterLayout:function(e,t,r){this._updateMeshLinesGeometry(),this._pointsBuilder.removePositionTexture(),this._pointsBuilder.updateLayout(e,t,r),this._pointsBuilder.updateView(this.viewGL.camera),this._pointsBuilder.updateLabels(),this._pointsBuilder.showLabels()},focusNodeAdjacency:function(e,t,r,i){var n=this._model.getData();this._downplayAll();var a=i.dataIndex,o=n.graph,s=[],l=o.getNodeByIndex(a);s.push(l),l.edges.forEach(function(h){h.dataIndex<0||(h.node1!==l&&s.push(h.node1),h.node2!==l&&s.push(h.node2))},this),this._pointsBuilder.fadeOutAll(.05),this._fadeOutEdgesAll(.05),s.forEach(function(h){this._pointsBuilder.highlight(n,h.dataIndex)},this),this._pointsBuilder.updateLabels(s.map(function(h){return h.dataIndex}));var u=[];l.edges.forEach(function(h){h.dataIndex>=0&&(this._highlightEdge(h.dataIndex),u.push(h))},this),this._focusNodes=s,this._focusEdges=u},unfocusNodeAdjacency:function(e,t,r,i){this._downplayAll(),this._pointsBuilder.fadeInAll(),this._fadeInEdgesAll(),this._pointsBuilder.updateLabels()},_highlightEdge:function(e){var t=this._model.getEdgeData().getItemModel(e),r=S.parseColor(t.get("emphasis.lineStyle.color")||t.get("lineStyle.color")),i=oe.firstNotNull(t.get("emphasis.lineStyle.opacity"),t.get("lineStyle.opacity"),1);r[3]*=i,this._edgesMesh.geometry.setItemColor(this._edgeIndicesMap[e],r)},_downplayAll:function(){this._focusNodes&&this._focusNodes.forEach(function(e){this._pointsBuilder.downplay(this._model.getData(),e.dataIndex)},this),this._focusEdges&&this._focusEdges.forEach(function(e){this._downplayEdge(e.dataIndex)},this)},_downplayEdge:function(e){var t=this._getColor(e,[]);this._edgesMesh.geometry.setItemColor(this._edgeIndicesMap[e],t)},_setEdgeFade:function(){var e=[];return function(t,r){this._getColor(t,e),e[3]*=r,this._edgesMesh.geometry.setItemColor(this._edgeIndicesMap[t],e)}}(),_getColor:function(e,t){for(var r=0;r<4;r++)t[r]=this._originalEdgeColors[e*4+r];return t},_fadeOutEdgesAll:function(e){var t=this._model.getData().graph;t.eachEdge(function(r){this._setEdgeFade(r.dataIndex,e)},this)},_fadeInEdgesAll:function(){this._fadeOutEdgesAll(1)},_updateCamera:function(e,t){this.viewGL.setViewport(0,0,t.getWidth(),t.getHeight(),t.getDevicePixelRatio());for(var r=this.viewGL.camera,i=e.getData(),n=i.getLayout("points"),a=Hn.create(1/0,1/0),o=Hn.create(-1/0,-1/0),s=[],l=0;l<n.length;)s[0]=n[l++],s[1]=n[l++],Hn.min(a,a,s),Hn.max(o,o,s);var u=(o[1]+a[1])/2,h=(o[0]+a[0])/2;if(!(h>r.left&&h<r.right&&u<r.bottom&&u>r.top)){var f=Math.max(o[0]-a[0],10),d=f/t.getWidth()*t.getHeight();f*=1.4,d*=1.4,a[0]-=f*.2,r.left=a[0],r.top=u-d/2,r.bottom=u+d/2,r.right=f+a[0],r.near=0,r.far=100}},dispose:function(){var e=this.viewGL.layer.renderer;this._forceLayoutInstance&&this._forceLayoutInstance.dispose(e),this.groupGL.removeAll(),this._layoutId=-1,this._pointsBuilder.dispose()},remove:function(){this.groupGL.removeAll(),this._control.dispose()}});function kn(e){return e instanceof Array||(e=[e,e]),e}function Ey(e){e.registerChartView(Ay),e.registerSeriesModel(Hi),e.registerVisual(function(r){const i={};r.eachSeriesByType("graphGL",function(n){var a=n.getCategoriesData(),o=n.getData(),s={};a.each(function(l){var u=a.getName(l);s["ec-"+u]=l;var h=a.getItemModel(l),f=h.getModel("itemStyle").getItemStyle();f.fill||(f.fill=n.getColorFromPalette(u,i)),a.setItemVisual(l,"style",f);var d=["symbol","symbolSize","symbolKeepAspect"];for(let v=0;v<d.length;v++){var c=h.getShallow(d[v],!0);c!=null&&a.setItemVisual(l,d[v],c)}}),a.count()&&o.each(function(l){var u=o.getItemModel(l);let h=u.getShallow("category");if(h!=null){typeof h=="string"&&(h=s["ec-"+h]);var f=a.getItemVisual(h,"style"),d=o.ensureUniqueItemVisual(l,"style");lt(d,f);var c=["symbol","symbolSize","symbolKeepAspect"];for(let v=0;v<c.length;v++)o.setItemVisual(l,c[v],a.getItemVisual(h,c[v]))}})})}),e.registerVisual(function(r){r.eachSeriesByType("graphGL",function(i){var n=i.getGraph(),a=i.getEdgeData(),o=kn(i.get("edgeSymbol")),s=kn(i.get("edgeSymbolSize"));a.setVisual("drawType","stroke"),a.setVisual("fromSymbol",o&&o[0]),a.setVisual("toSymbol",o&&o[1]),a.setVisual("fromSymbolSize",s&&s[0]),a.setVisual("toSymbolSize",s&&s[1]),a.setVisual("style",i.getModel("lineStyle").getLineStyle()),a.each(function(l){var u=a.getItemModel(l),h=n.getEdgeByIndex(l),f=kn(u.getShallow("symbol",!0)),d=kn(u.getShallow("symbolSize",!0)),c=u.getModel("lineStyle").getLineStyle(),v=a.ensureUniqueItemVisual(l,"style");switch(lt(v,c),v.stroke){case"source":{var p=h.node1.getVisual("style");v.stroke=p&&p.fill;break}case"target":{var p=h.node2.getVisual("style");v.stroke=p&&p.fill;break}}f[0]&&h.setVisual("fromSymbol",f[0]),f[1]&&h.setVisual("toSymbol",f[1]),d[0]&&h.setVisual("fromSymbolSize",d[0]),d[1]&&h.setVisual("toSymbolSize",d[1])})})}),e.registerAction({type:"graphGLRoam",event:"graphglroam",update:"series.graphGL:roam"},function(r,i){i.eachComponent({mainType:"series",query:r},function(n){n.setView(r)})});function t(){}e.registerAction({type:"graphGLStartLayout",event:"graphgllayoutstarted",update:"series.graphGL:startLayout"},t),e.registerAction({type:"graphGLStopLayout",event:"graphgllayoutstopped",update:"series.graphGL:stopLayout"},t),e.registerAction({type:"graphGLFocusNodeAdjacency",event:"graphGLFocusNodeAdjacency",update:"series.graphGL:focusNodeAdjacency"},t),e.registerAction({type:"graphGLUnfocusNodeAdjacency",event:"graphGLUnfocusNodeAdjacency",update:"series.graphGL:unfocusNodeAdjacency"},t)}Ne(Ey);const Ly=ft.extend({type:"series.flowGL",dependencies:["geo","grid","bmap"],visualStyleAccessPath:"itemStyle",getInitialData:function(e,t){var r=this.get("coordinateSystem"),i=r==="geo"?["lng","lat"]:oh(r)||["x","y"];i.push("vx","vy");var n=vn(this.getSource(),{coordDimensions:i,encodeDefine:this.get("encode"),dimensionsDefine:this.get("dimensions")}),a=new Nt(n,this);return a.initData(this.getSource()),a},defaultOption:{coordinateSystem:"cartesian2d",zlevel:10,supersampling:1,particleType:"point",particleDensity:128,particleSize:1,particleSpeed:1,particleTrail:2,colorTexture:null,gridWidth:"auto",gridHeight:"auto",itemStyle:{color:"#fff",opacity:.8}}});var Cy=se.extend(function(){return{dynamic:!0,attributes:{position:new se.Attribute("position","float",3,"POSITION")}}},{resetOffset:function(){this._vertexOffset=0,this._faceOffset=0},setLineCount:function(e){var t=this.attributes,r=4*e,i=2*e;this.vertexCount!==r&&t.position.init(r),this.triangleCount!==i&&(i===0?this.indices=null:this.indices=this.vertexCount>65535?new Uint32Array(i*3):new Uint16Array(i*3))},addLine:function(e){var t=this._vertexOffset;this.attributes.position.set(t,[e[0],e[1],1]),this.attributes.position.set(t+1,[e[0],e[1],-1]),this.attributes.position.set(t+2,[e[0],e[1],2]),this.attributes.position.set(t+3,[e[0],e[1],-2]),this.setTriangleIndices(this._faceOffset++,[t,t+1,t+2]),this.setTriangleIndices(this._faceOffset++,[t+1,t+2,t+3]),this._vertexOffset+=4}});const My=`@export ecgl.vfParticle.particle.fragment

uniform sampler2D particleTexture;
uniform sampler2D spawnTexture;
uniform sampler2D velocityTexture;

uniform float deltaTime;
uniform float elapsedTime;

uniform float speedScaling : 1.0;

uniform vec2 textureSize;
uniform vec4 region : [0, 0, 1, 1];
uniform float firstFrameTime;

varying vec2 v_Texcoord;


void main()
{
 vec4 p = texture2D(particleTexture, v_Texcoord);
 bool spawn = false;
 if (p.w <= 0.0) {
 p = texture2D(spawnTexture, fract(v_Texcoord + elapsedTime / 10.0));
 p.w -= firstFrameTime;
 spawn = true;
 }
 vec2 v = texture2D(velocityTexture, fract(p.xy * region.zw + region.xy)).xy;
 v = (v - 0.5) * 2.0;
 p.z = length(v);
 p.xy += v * deltaTime / 10.0 * speedScaling;
 p.w -= deltaTime;

 if (spawn || p.xy != fract(p.xy)) {
 p.z = 0.0;
 }
 p.xy = fract(p.xy);

 gl_FragColor = p;
}
@end

@export ecgl.vfParticle.renderPoints.vertex

#define PI 3.1415926

attribute vec2 texcoord : TEXCOORD_0;

uniform sampler2D particleTexture;
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

uniform float size : 1.0;

varying float v_Mag;
varying vec2 v_Uv;

void main()
{
 vec4 p = texture2D(particleTexture, texcoord);

 if (p.w > 0.0 && p.z > 1e-5) {
 gl_Position = worldViewProjection * vec4(p.xy * 2.0 - 1.0, 0.0, 1.0);
 }
 else {
 gl_Position = vec4(100000.0, 100000.0, 100000.0, 1.0);
 }

 v_Mag = p.z;
 v_Uv = p.xy;

 gl_PointSize = size;
}

@end

@export ecgl.vfParticle.renderPoints.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];
uniform sampler2D gradientTexture;
uniform sampler2D colorTexture;
uniform sampler2D spriteTexture;

varying float v_Mag;
varying vec2 v_Uv;

void main()
{
 gl_FragColor = color;
#ifdef SPRITETEXTURE_ENABLED
 gl_FragColor *= texture2D(spriteTexture, gl_PointCoord);
 if (color.a == 0.0) {
 discard;
 }
#endif
#ifdef GRADIENTTEXTURE_ENABLED
 gl_FragColor *= texture2D(gradientTexture, vec2(v_Mag, 0.5));
#endif
#ifdef COLORTEXTURE_ENABLED
 gl_FragColor *= texture2D(colorTexture, v_Uv);
#endif
}

@end

@export ecgl.vfParticle.renderLines.vertex

#define PI 3.1415926

attribute vec3 position : POSITION;

uniform sampler2D particleTexture;
uniform sampler2D prevParticleTexture;

uniform float size : 1.0;
uniform vec4 vp: VIEWPORT;
uniform mat4 worldViewProjection : WORLDVIEWPROJECTION;

varying float v_Mag;
varying vec2 v_Uv;

@import clay.util.rand

void main()
{
 vec4 p = texture2D(particleTexture, position.xy);
 vec4 p2 = texture2D(prevParticleTexture, position.xy);

 p.xy = p.xy * 2.0 - 1.0;
 p2.xy = p2.xy * 2.0 - 1.0;

 if (p.w > 0.0 && p.z > 1e-5) {
 vec2 dir = normalize(p.xy - p2.xy);
 vec2 norm = vec2(dir.y / vp.z, -dir.x / vp.w) * sign(position.z) * size;
 if (abs(position.z) == 2.0) {
 gl_Position = vec4(p.xy + norm, 0.0, 1.0);
 v_Uv = p.xy;
 v_Mag = p.z;
 }
 else {
 gl_Position = vec4(p2.xy + norm, 0.0, 1.0);
 v_Mag = p2.z;
 v_Uv = p2.xy;
 }
 gl_Position = worldViewProjection * gl_Position;
 }
 else {
 gl_Position = vec4(100000.0, 100000.0, 100000.0, 1.0);
 }
}

@end

@export ecgl.vfParticle.renderLines.fragment

uniform vec4 color : [1.0, 1.0, 1.0, 1.0];
uniform sampler2D gradientTexture;
uniform sampler2D colorTexture;

varying float v_Mag;
varying vec2 v_Uv;

void main()
{
 gl_FragColor = color;
 #ifdef GRADIENTTEXTURE_ENABLED
 gl_FragColor *= texture2D(gradientTexture, vec2(v_Mag, 0.5));
#endif
#ifdef COLORTEXTURE_ENABLED
 gl_FragColor *= texture2D(colorTexture, v_Uv);
#endif
}

@end
`;k.import(My);function Dy(e){var t=document.createElement("canvas");t.width=t.height=e;var r=t.getContext("2d");return r.fillStyle="#fff",r.arc(e/2,e/2,e/2,0,Math.PI*2),r.fill(),t}var Ro=function(){this.motionBlurFactor=.99,this.vectorFieldTexture=new ne({type:H.FLOAT,flipY:!1}),this.particleLife=[5,20],this._particleType="point",this._particleSize=1,this.particleColor=[1,1,1,1],this.particleSpeedScaling=1,this._thisFrameTexture=null,this._particlePass=null,this._spawnTexture=null,this._particleTexture0=null,this._particleTexture1=null,this._particlePointsMesh=null,this._surfaceFrameBuffer=null,this._elapsedTime=0,this._scene=null,this._camera=null,this._lastFrameTexture=null,this._supersampling=1,this._downsampleTextures=[],this._width=512,this._height=512,this.init()};Ro.prototype={constructor:Ro,init:function(){var e={type:H.FLOAT,minFilter:H.NEAREST,magFilter:H.NEAREST,useMipmap:!1};this._spawnTexture=new ne(e),this._particleTexture0=new ne(e),this._particleTexture1=new ne(e),this._frameBuffer=new Ie({depthBuffer:!1}),this._particlePass=new Oe({fragment:k.source("ecgl.vfParticle.particle.fragment")}),this._particlePass.setUniform("velocityTexture",this.vectorFieldTexture),this._particlePass.setUniform("spawnTexture",this._spawnTexture),this._downsamplePass=new Oe({fragment:k.source("clay.compositor.downsample")});var t=new Xe({renderOrder:10,material:new At({shader:new k(k.source("ecgl.vfParticle.renderPoints.vertex"),k.source("ecgl.vfParticle.renderPoints.fragment"))}),mode:Xe.POINTS,geometry:new se({dynamic:!0,mainAttribute:"texcoord0"})}),r=new Xe({renderOrder:10,material:new At({shader:new k(k.source("ecgl.vfParticle.renderLines.vertex"),k.source("ecgl.vfParticle.renderLines.fragment"))}),geometry:new Cy,culling:!1}),i=new Xe({material:new At({shader:new k(k.source("ecgl.color.vertex"),k.source("ecgl.color.fragment"))}),geometry:new pa});i.material.enableTexture("diffuseMap"),this._particlePointsMesh=t,this._particleLinesMesh=r,this._lastFrameFullQuadMesh=i,this._camera=new _i,this._thisFrameTexture=new ne,this._lastFrameTexture=new ne},setParticleDensity:function(e,t){for(var r=e*t,i=new Float32Array(r*4),n=0,a=this.particleLife,o=0;o<e;o++)for(var s=0;s<t;s++,n++){i[n*4]=Math.random(),i[n*4+1]=Math.random(),i[n*4+2]=Math.random();var l=(a[1]-a[0])*Math.random()+a[0];i[n*4+3]=l}this._particleType==="line"?this._setLineGeometry(e,t):this._setPointsGeometry(e,t),this._spawnTexture.width=e,this._spawnTexture.height=t,this._spawnTexture.pixels=i,this._particleTexture0.width=this._particleTexture1.width=e,this._particleTexture0.height=this._particleTexture1.height=t,this._particlePass.setUniform("textureSize",[e,t])},_setPointsGeometry:function(e,t){var r=e*t,i=this._particlePointsMesh.geometry,n=i.attributes;n.texcoord0.init(r);for(var a=0,o=0;o<e;o++)for(var s=0;s<t;s++,a++)n.texcoord0.value[a*2]=o/e,n.texcoord0.value[a*2+1]=s/t;i.dirty()},_setLineGeometry:function(e,t){var r=e*t,i=this._getParticleMesh().geometry;i.setLineCount(r),i.resetOffset();for(var n=0;n<e;n++)for(var a=0;a<t;a++)i.addLine([n/e,a/t]);i.dirty()},_getParticleMesh:function(){return this._particleType==="line"?this._particleLinesMesh:this._particlePointsMesh},update:function(e,t,r,i){var n=this._getParticleMesh(),a=this._frameBuffer,o=this._particlePass;i&&this._updateDownsampleTextures(e,t),n.material.set("size",this._particleSize*this._supersampling),n.material.set("color",this.particleColor),o.setUniform("speedScaling",this.particleSpeedScaling),a.attach(this._particleTexture1),o.setUniform("firstFrameTime",i?(this.particleLife[1]+this.particleLife[0])/2:0),o.setUniform("particleTexture",this._particleTexture0),o.setUniform("deltaTime",r),o.setUniform("elapsedTime",this._elapsedTime),o.render(e,a),n.material.set("particleTexture",this._particleTexture1),n.material.set("prevParticleTexture",this._particleTexture0),a.attach(this._thisFrameTexture),a.bind(e),e.gl.clear(e.gl.DEPTH_BUFFER_BIT|e.gl.COLOR_BUFFER_BIT);var s=this._lastFrameFullQuadMesh;s.material.set("diffuseMap",this._lastFrameTexture),s.material.set("color",[1,1,1,this.motionBlurFactor]),this._camera.update(!0),e.renderPass([s,n],this._camera),a.unbind(e),this._downsample(e),this._swapTexture(),this._elapsedTime+=r},_downsample:function(e){var t=this._downsampleTextures;if(t.length!==0)for(var r=0,i=this._thisFrameTexture,n=t[r];n;)this._frameBuffer.attach(n),this._downsamplePass.setUniform("texture",i),this._downsamplePass.setUniform("textureSize",[i.width,i.height]),this._downsamplePass.render(e,this._frameBuffer),i=n,n=t[++r]},getSurfaceTexture:function(){var e=this._downsampleTextures;return e.length>0?e[e.length-1]:this._lastFrameTexture},setRegion:function(e){this._particlePass.setUniform("region",e)},resize:function(e,t){this._lastFrameTexture.width=e*this._supersampling,this._lastFrameTexture.height=t*this._supersampling,this._thisFrameTexture.width=e*this._supersampling,this._thisFrameTexture.height=t*this._supersampling,this._width=e,this._height=t},setParticleSize:function(e){var t=this._getParticleMesh();if(e<=2){t.material.disableTexture("spriteTexture"),t.material.transparent=!1;return}this._spriteTexture||(this._spriteTexture=new ne),(!this._spriteTexture.image||this._spriteTexture.image.width!==e)&&(this._spriteTexture.image=Dy(e),this._spriteTexture.dirty()),t.material.transparent=!0,t.material.enableTexture("spriteTexture"),t.material.set("spriteTexture",this._spriteTexture),this._particleSize=e},setGradientTexture:function(e){var t=this._getParticleMesh().material;t[e?"enableTexture":"disableTexture"]("gradientTexture"),t.setUniform("gradientTexture",e)},setColorTextureImage:function(e,t){var r=this._getParticleMesh().material;r.setTextureImage("colorTexture",e,t,{flipY:!0})},setParticleType:function(e){this._particleType=e},clearFrame:function(e){var t=this._frameBuffer;t.attach(this._lastFrameTexture),t.bind(e),e.gl.clear(e.gl.DEPTH_BUFFER_BIT|e.gl.COLOR_BUFFER_BIT),t.unbind(e)},setSupersampling:function(e){this._supersampling=e,this.resize(this._width,this._height)},_updateDownsampleTextures:function(e,t){for(var r=this._downsampleTextures,i=Math.max(Math.floor(Math.log(this._supersampling/t.getDevicePixelRatio())/Math.log(2)),0),n=2,a=this._width*this._supersampling,o=this._height*this._supersampling,s=0;s<i;s++)r[s]=r[s]||new ne,r[s].width=a/n,r[s].height=o/n,n*=2;for(;s<r.length;s++)r[s].dispose(e);r.length=i},_swapTexture:function(){var e=this._particleTexture0;this._particleTexture0=this._particleTexture1,this._particleTexture1=e;var e=this._thisFrameTexture;this._thisFrameTexture=this._lastFrameTexture,this._lastFrameTexture=e},dispose:function(e){e.disposeFrameBuffer(this._frameBuffer),e.disposeTexture(this.vectorFieldTexture),e.disposeTexture(this._spawnTexture),e.disposeTexture(this._particleTexture0),e.disposeTexture(this._particleTexture1),e.disposeTexture(this._thisFrameTexture),e.disposeTexture(this._lastFrameTexture),e.disposeGeometry(this._particleLinesMesh.geometry),e.disposeGeometry(this._particlePointsMesh.geometry),e.disposeGeometry(this._lastFrameFullQuadMesh.geometry),this._spriteTexture&&e.disposeTexture(this._spriteTexture),this._particlePass.dispose(e),this._downsamplePass.dispose(e),this._downsampleTextures.forEach(function(t){t.dispose(e)})}};const Py=it.extend({type:"flowGL",__ecgl__:!0,init:function(e,t){this.viewGL=new ge("orthographic"),this.groupGL=new S.Node,this.viewGL.add(this.groupGL),this._particleSurface=new Ro;var r=new S.Mesh({geometry:new S.PlaneGeometry,material:new S.Material({shader:new S.Shader({vertex:S.Shader.source("ecgl.color.vertex"),fragment:S.Shader.source("ecgl.color.fragment")}),transparent:!0})});r.material.enableTexture("diffuseMap"),this.groupGL.add(r),this._planeMesh=r},render:function(e,t,r){var i=this._particleSurface;i.setParticleType(e.get("particleType")),i.setSupersampling(e.get("supersampling")),this._updateData(e,r),this._updateCamera(r.getWidth(),r.getHeight(),r.getDevicePixelRatio());var n=oe.firstNotNull(e.get("particleDensity"),128);i.setParticleDensity(n,n);var a=this._planeMesh,o=+new Date,s=this,l=!0;a.__percent=0,a.stopAnimation(),a.animate("",{loop:!0}).when(1e5,{__percent:1}).during(function(){var f=+new Date,d=Math.min(f-o,20);o=o+d,s._renderer&&(i.update(s._renderer,r,d/1e3,l),a.material.set("diffuseMap",i.getSurfaceTexture())),l=!1}).start();var u=e.getModel("itemStyle"),h=S.parseColor(u.get("color"));h[3]*=oe.firstNotNull(u.get("opacity"),1),a.material.set("color",h),i.setColorTextureImage(e.get("colorTexture"),r),i.setParticleSize(e.get("particleSize")),i.particleSpeedScaling=e.get("particleSpeed"),i.motionBlurFactor=1-Math.pow(.1,e.get("particleTrail"))},updateTransform:function(e,t,r){this._updateData(e,r)},afterRender:function(e,t,r,i){var n=i.renderer;this._renderer=n},_updateData:function(e,t){var r=e.coordinateSystem,i=r.dimensions.map(function(g){return e.coordDimToDataDim(g)[0]}),n=e.getData(),a=n.getDataExtent(i[0]),o=n.getDataExtent(i[1]),s=e.get("gridWidth"),l=e.get("gridHeight");if(s==null||s==="auto"){var u=(a[1]-a[0])/(o[1]-o[0]);s=Math.round(Math.sqrt(u*n.count()))}(l==null||l==="auto")&&(l=Math.ceil(n.count()/s));var h=this._particleSurface.vectorFieldTexture,f=h.pixels;if(!f||f.length!==l*s*4)f=h.pixels=new Float32Array(s*l*4);else for(var d=0;d<f.length;d++)f[d]=0;var c=0,v=1/0,p=new Float32Array(n.count()*2),_=0,m=[[1/0,1/0],[-1/0,-1/0]];n.each([i[0],i[1],"vx","vy"],function(g,y,x,w){var T=r.dataToPoint([g,y]);p[_++]=T[0],p[_++]=T[1],m[0][0]=Math.min(T[0],m[0][0]),m[0][1]=Math.min(T[1],m[0][1]),m[1][0]=Math.max(T[0],m[1][0]),m[1][1]=Math.max(T[1],m[1][1]);var b=Math.sqrt(x*x+w*w);c=Math.max(c,b),v=Math.min(v,b)}),n.each(["vx","vy"],function(g,y,x){var w=Math.round((p[x*2]-m[0][0])/(m[1][0]-m[0][0])*(s-1)),T=l-1-Math.round((p[x*2+1]-m[0][1])/(m[1][1]-m[0][1])*(l-1)),b=(T*s+w)*4;f[b]=g/c*.5+.5,f[b+1]=y/c*.5+.5,f[b+3]=1}),h.width=s,h.height=l,e.get("coordinateSystem")==="bmap"&&this._fillEmptyPixels(h),h.dirty(),this._updatePlanePosition(m[0],m[1],e,t),this._updateGradientTexture(n.getVisual("visualMeta"),[v,c])},_fillEmptyPixels:function(e){var t=e.pixels,r=e.width,i=e.height;function n(p,_,m){p=Math.max(Math.min(p,r-1),0),_=Math.max(Math.min(_,i-1),0);var g=(_*(r-1)+p)*4;return t[g+3]===0?!1:(m[0]=t[g],m[1]=t[g+1],!0)}function a(p,_,m){m[0]=p[0]+_[0],m[1]=p[1]+_[1]}for(var o=[],s=[],l=[],u=[],h=[],f=0,d=0;d<i;d++)for(var c=0;c<r;c++){var v=(d*(r-1)+c)*4;t[v+3]===0&&(f=o[0]=o[1]=0,n(c-1,d,s)&&(f++,a(s,o,o)),n(c+1,d,l)&&(f++,a(l,o,o)),n(c,d-1,u)&&(f++,a(u,o,o)),n(c,d+1,h)&&(f++,a(h,o,o)),o[0]/=f,o[1]/=f,t[v]=o[0],t[v+1]=o[1]),t[v+3]=1}},_updateGradientTexture:function(e,t){if(!e||!e.length){this._particleSurface.setGradientTexture(null);return}this._gradientTexture=this._gradientTexture||new S.Texture2D({image:document.createElement("canvas")});var r=this._gradientTexture,i=r.image;i.width=200,i.height=1;var n=i.getContext("2d"),a=n.createLinearGradient(0,.5,i.width,.5);e[0].stops.forEach(function(o){var s;t[1]===t[0]?s=0:(s=o.value/t[1],s=Math.min(Math.max(s,0),1)),a.addColorStop(s,o.color)}),n.fillStyle=a,n.fillRect(0,0,i.width,i.height),r.dirty(),this._particleSurface.setGradientTexture(this._gradientTexture)},_updatePlanePosition:function(e,t,r,i){var n=this._limitInViewportAndFullFill(e,t,r,i);e=n.leftTop,t=n.rightBottom,this._particleSurface.setRegion(n.region),this._planeMesh.position.set((e[0]+t[0])/2,i.getHeight()-(e[1]+t[1])/2,0);var a=t[0]-e[0],o=t[1]-e[1];this._planeMesh.scale.set(a/2,o/2,1),this._particleSurface.resize(Math.max(Math.min(a,2048),1),Math.max(Math.min(o,2048),1)),this._renderer&&this._particleSurface.clearFrame(this._renderer)},_limitInViewportAndFullFill:function(e,t,r,i){var n=[Math.max(e[0],0),Math.max(e[1],0)],a=[Math.min(t[0],i.getWidth()),Math.min(t[1],i.getHeight())];if(r.get("coordinateSystem")==="bmap"){var o=r.getData().getDataExtent(r.coordDimToDataDim("lng")[0]),s=Math.floor(o[1]-o[0])>=359;s&&(n[0]>0&&(n[0]=0),a[0]<i.getWidth()&&(a[0]=i.getWidth()))}var l=t[0]-e[0],u=t[1]-e[1],h=a[0]-n[0],f=a[1]-n[1],d=[(n[0]-e[0])/l,1-f/u-(n[1]-e[1])/u,h/l,f/u];return{leftTop:n,rightBottom:a,region:d}},_updateCamera:function(e,t,r){this.viewGL.setViewport(0,0,e,t,r);var i=this.viewGL.camera;i.left=i.bottom=0,i.top=t,i.right=e,i.near=0,i.far=100,i.position.z=10},remove:function(){this._planeMesh.stopAnimation(),this.groupGL.removeAll()},dispose:function(){this._renderer&&this._particleSurface.dispose(this._renderer),this.groupGL.removeAll()}});function Ny(e){e.registerChartView(Py),e.registerSeriesModel(Ly)}Ne(Ny);var Oo=ft.extend({type:"series.linesGL",dependencies:["grid","geo"],visualStyleAccessPath:"lineStyle",visualDrawType:"stroke",streamEnabled:!0,init:function(e){var t=this._processFlatCoordsArray(e.data);this._flatCoords=t.flatCoords,this._flatCoordsOffset=t.flatCoordsOffset,t.flatCoords&&(e.data=new Float32Array(t.count)),Oo.superApply(this,"init",arguments)},mergeOption:function(e){var t=this._processFlatCoordsArray(e.data);this._flatCoords=t.flatCoords,this._flatCoordsOffset=t.flatCoordsOffset,t.flatCoords&&(e.data=new Float32Array(t.count)),Oo.superApply(this,"mergeOption",arguments)},appendData:function(e){var t=this._processFlatCoordsArray(e.data);t.flatCoords&&(this._flatCoords?(this._flatCoords=Fs(this._flatCoords,t.flatCoords),this._flatCoordsOffset=Fs(this._flatCoordsOffset,t.flatCoordsOffset)):(this._flatCoords=t.flatCoords,this._flatCoordsOffset=t.flatCoordsOffset),e.data=new Float32Array(t.count)),this.getRawData().appendData(e.data)},_getCoordsFromItemModel:function(e){var t=this.getData().getItemModel(e),r=t.option instanceof Array?t.option:t.getShallow("coords");return r},getLineCoordsCount:function(e){return this._flatCoordsOffset?this._flatCoordsOffset[e*2+1]:this._getCoordsFromItemModel(e).length},getLineCoords:function(e,t){if(this._flatCoordsOffset){for(var r=this._flatCoordsOffset[e*2],i=this._flatCoordsOffset[e*2+1],n=0;n<i;n++)t[n]=t[n]||[],t[n][0]=this._flatCoords[r+n*2],t[n][1]=this._flatCoords[r+n*2+1];return i}else{for(var a=this._getCoordsFromItemModel(e),n=0;n<a.length;n++)t[n]=t[n]||[],t[n][0]=a[n][0],t[n][1]=a[n][1];return a.length}},_processFlatCoordsArray:function(e){var t=0;if(this._flatCoords&&(t=this._flatCoords.length),typeof e[0]=="number"){for(var r=e.length,i=new Uint32Array(r),n=new Float64Array(r),a=0,o=0,s=0,l=0;l<r;){s++;var u=e[l++];i[o++]=a+t,i[o++]=u;for(var h=0;h<u;h++){var f=e[l++],d=e[l++];n[a++]=f,n[a++]=d}}return{flatCoordsOffset:new Uint32Array(i.buffer,0,o),flatCoords:n,count:s}}return{flatCoordsOffset:null,flatCoords:null,count:e.length}},getInitialData:function(e,t){var r=new Nt(["value"],this);return r.hasItemOption=!1,r.initData(e.data,[],function(i,n,a,o){if(i instanceof Array)return NaN;r.hasItemOption=!0;var s=i.value;if(s!=null)return s instanceof Array?s[o]:s}),r},defaultOption:{coordinateSystem:"geo",zlevel:10,progressive:1e4,progressiveThreshold:5e4,blendMode:"source-over",lineStyle:{opacity:.8},postEffect:{enable:!1,colorCorrection:{exposure:0,brightness:0,contrast:1,saturation:1,enable:!0}}}});const Iy=it.extend({type:"linesGL",__ecgl__:!0,init:function(e,t){this.groupGL=new S.Node,this.viewGL=new ge("orthographic"),this.viewGL.add(this.groupGL),this._glViewHelper=new ir(this.viewGL),this._nativeLinesShader=S.createShader("ecgl.lines3D"),this._meshLinesShader=S.createShader("ecgl.meshLines3D"),this._linesMeshes=[],this._currentStep=0},render:function(e,t,r){this.groupGL.removeAll(),this._glViewHelper.reset(e,r);var i=this._linesMeshes[0];i||(i=this._linesMeshes[0]=this._createLinesMesh(e)),this._linesMeshes.length=1,this.groupGL.add(i),this._updateLinesMesh(e,i,0,e.getData().count()),this.viewGL.setPostEffect(e.getModel("postEffect"),r)},incrementalPrepareRender:function(e,t,r){this.groupGL.removeAll(),this._glViewHelper.reset(e,r),this._currentStep=0,this.viewGL.setPostEffect(e.getModel("postEffect"),r)},incrementalRender:function(e,t,r,i){var n=this._linesMeshes[this._currentStep];n||(n=this._createLinesMesh(t),this._linesMeshes[this._currentStep]=n),this._updateLinesMesh(t,n,e.start,e.end),this.groupGL.add(n),i.getZr().refresh(),this._currentStep++},updateTransform:function(e,t,r){e.coordinateSystem.getRoamTransform&&this._glViewHelper.updateTransform(e,r)},_createLinesMesh:function(e){var t=new S.Mesh({$ignorePicking:!0,material:new S.Material({shader:S.createShader("ecgl.lines3D"),transparent:!0,depthMask:!1,depthTest:!1}),geometry:new gs({segmentScale:10,useNativeLine:!0,dynamic:!1}),mode:S.Mesh.LINES,culling:!1});return t},_updateLinesMesh:function(e,t,r,i){var n=e.getData();t.material.blend=e.get("blendMode")==="lighter"?S.additiveBlend:null;var a=e.get("lineStyle.curveness")||0,o=e.get("polyline"),s=t.geometry,l=e.coordinateSystem,u=oe.firstNotNull(e.get("lineStyle.width"),1);u>1?(t.material.shader!==this._meshLinesShader&&t.material.attachShader(this._meshLinesShader),t.mode=S.Mesh.TRIANGLES):(t.material.shader!==this._nativeLinesShader&&t.material.attachShader(this._nativeLinesShader),t.mode=S.Mesh.LINES),r=r||0,i=i||n.count(),s.resetOffset();var h=0,f=0,d=[],c=[],v=[],p=[],_=[],m=.3,g=.7;function y(){c[0]=d[0]*g+p[0]*m-(d[1]-p[1])*a,c[1]=d[1]*g+p[1]*m-(p[0]-d[0])*a,v[0]=d[0]*m+p[0]*g-(d[1]-p[1])*a,v[1]=d[1]*m+p[1]*g-(p[0]-d[0])*a}if(o||a!==0)for(var x=r;x<i;x++)if(o){var w=e.getLineCoordsCount(x);h+=s.getPolylineVertexCount(w),f+=s.getPolylineTriangleCount(w)}else e.getLineCoords(x,_),this._glViewHelper.dataToPoint(l,_[0],d),this._glViewHelper.dataToPoint(l,_[1],p),y(),h+=s.getCubicCurveVertexCount(d,c,v,p),f+=s.getCubicCurveTriangleCount(d,c,v,p);else{var T=i-r;h+=T*s.getLineVertexCount(),f+=T*s.getLineVertexCount()}s.setVertexCount(h),s.setTriangleCount(f);for(var b=r,A=[],x=r;x<i;x++){S.parseColor(Ze(n,b),A);var C=oe.firstNotNull(je(n,b),1);A[3]*=C;for(var w=e.getLineCoords(x,_),D=0;D<w;D++)this._glViewHelper.dataToPoint(l,_[D],_[D]);o?s.addPolyline(_,A,u,0,w):a!==0?(d=_[0],p=_[1],y(),s.addCubicCurve(d,c,v,p,A,u)):s.addPolyline(_,A,u,0,2),b++}},dispose:function(){this.groupGL.removeAll()},remove:function(){this.groupGL.removeAll()}});function Ry(e){e.registerChartView(Iy),e.registerSeriesModel(Oo)}Ne(Ry);const Oy={class:"home"},By={class:"stat-info"},Fy={class:"stat-value"},Gy={class:"stat-info"},zy={class:"stat-value"},Uy={class:"stat-info"},Vy={class:"stat-value"},Hy={class:"stat-info"},ky={class:"stat-value"},Wy={class:"stat-info"},Xy={class:"stat-value"},jy={class:"stat-info"},Zy={class:"stat-value"},qy={class:"stat-info"},Yy={class:"stat-value"},$y={class:"stat-info"},Ky={class:"stat-value"},Jy={class:"stat-info"},Qy={class:"stat-value"},ex={class:"today-overview-card"},tx={class:"overview-content"},rx={class:"overview-column"},ix={class:"overview-item"},nx={class:"overview-item-icon word-icon"},ax={class:"overview-item-info"},ox={class:"overview-value"},sx={class:"overview-item"},lx={class:"overview-item-icon question-icon"},ux={class:"overview-item-info"},hx={class:"overview-value"},fx={class:"overview-item"},cx={class:"overview-item-icon word-accuracy-icon"},dx={class:"overview-item-info"},vx={class:"overview-value"},px={class:"overview-item"},gx={class:"overview-item-icon question-accuracy-icon"},mx={class:"overview-item-info"},_x={class:"overview-value"},yx={class:"overview-column"},xx={class:"overview-item"},Tx={class:"overview-item-icon word-icon"},wx={class:"overview-item-info"},Sx={class:"overview-value"},bx={class:"overview-item"},Ax={class:"overview-item-icon question-icon"},Ex={class:"overview-item-info"},Lx={class:"overview-value"},Cx={class:"overview-item"},Mx={class:"overview-item-icon word-accuracy-icon"},Dx={class:"overview-item-info"},Px={class:"overview-value"},Nx={class:"overview-item"},Ix={class:"overview-item-icon question-accuracy-icon"},Rx={class:"overview-item-info"},Ox={class:"overview-value"},Bx={class:"card-header-modern"},Fx={key:0,class:"chart-container"},Gx={class:"card-header-modern"},zx={class:"question-count"},Ux={class:"difficulty-bars"},Vx={class:"diff-label"},Hx={class:"diff-count"},kx={class:"error-tags"},Wx={class:"practice-count"},Xx={class:"card-header-modern"},jx={class:"curve-tabs"},Zx={key:0,class:"chart-container"},qx={__name:"Home",setup(e){Ne([th,pd,zv,bv,dp,gd,md,_d,Gp,Zp]);const t=wn({total_questions:0,total_subjects:0,total_error_books:0,active_days:0,difficulty_distribution:{},error_type_distribution:{},by_subject:[],word_stats:{total_words:0,reviewed_words:0,total_reviews:0,accuracy:0},word_accuracy_curve:[],question_accuracy_curve:[]}),r=wn(""),i=wn({yesterday_word_review_count:0,yesterday_question_review_count:0,yesterday_word_accuracy:0,yesterday_question_accuracy:0,today_word_review_count:0,today_question_review_count:0,today_word_accuracy:0,today_question_accuracy:0}),n=wn("month"),a=(m,g)=>g?Math.round(m/g*100):0,o=m=>["","#67c23a","#85ce61","#e6a23c","#f56c6c","#f56c6c"][m]||"#909399",s=(m,g)=>{const y=parseInt(m.replace("#",""),16),x=Math.min(255,Math.max(0,(y>>16)+g)),w=Math.min(255,Math.max(0,(y>>8&255)+g)),T=Math.min(255,Math.max(0,(y&255)+g));return"#"+(x<<16|w<<8|T).toString(16).padStart(6,"0")},l=m=>({计算:"danger",概念:"warning",审题:"info",粗心:"success",其他:""})[m]||"",u=m=>m?Object.fromEntries(Object.entries(m).sort((g,y)=>y[1]-g[1]).slice(0,3)):{},h=Sr(()=>t.value.word_accuracy_curve&&t.value.word_accuracy_curve.length>0),f=Sr(()=>{const m=t.value.by_subject||[];if(!r.value&&m.length>0){const y=m.find(x=>x.subject_name.includes("数学"));r.value=y?y.subject_id:m[0].subject_id}const g=m.find(y=>y.subject_id===r.value);return(g==null?void 0:g.error_type_counts)||{}}),d=Sr(()=>Object.keys(f.value).length>0),c=Sr(()=>{const m=f.value;if(!Object.keys(m).length)return{};const g=["#5470c6","#91cc75","#fac858","#ee6666","#73c0de","#3ba272","#fc8452","#9a60b4","#ea7ccc"],y=Object.entries(m).sort((w,T)=>T[1]-w[1]),x=y.reduce((w,[,T])=>w+T,0);return{tooltip:{trigger:"item",formatter:"{b}: {c} ({d}%)"},legend:{orient:"vertical",right:16,top:"center",itemWidth:14,itemHeight:14,itemGap:16,textStyle:{color:"#606266",fontSize:14,lineHeight:24},formatter:w=>{const T=y.find(([A])=>A===w);if(!T)return w;const b=(T[1]/x*100).toFixed(1);return`${w}  ${T[1]}  ${b}%`}},series:[{type:"pie",radius:["30%","70%"],center:["35%","50%"],avoidLabelOverlap:!0,itemStyle:{borderRadius:6,borderColor:"#fff",borderWidth:2,shadowBlur:20,shadowColor:"rgba(0, 0, 0, 0.15)"},label:{show:!1},emphasis:{scaleSize:8,itemStyle:{shadowBlur:20,shadowColor:"rgba(0, 0, 0, 0.3)"}},labelLine:{show:!1},data:y.map(([w,T],b)=>({name:w,value:T,itemStyle:{color:{type:"linear",x:0,y:0,x2:1,y2:1,colorStops:[{offset:0,color:g[b%g.length]},{offset:1,color:s(g[b%g.length],-30)}]}}}))}]}}),v=Sr(()=>t.value.by_subject||[]),p=Sr(()=>{const m=t.value.word_accuracy_curve||[];if(!m.length)return[];const g=new Date,y=n.value;let x=null;if(y==="week")x=new Date(g.getTime()-7*24*60*60*1e3);else if(y==="month")x=new Date(g.getTime()-30*24*60*60*1e3);else if(y==="3months")x=new Date(g.getTime()-90*24*60*60*1e3);else if(y==="halfyear")x=new Date(g.getTime()-180*24*60*60*1e3);else return m;return m.filter(w=>new Date(w.date)>=x)}),_=Sr(()=>{const m=p.value,g=t.value.question_accuracy_curve||[],y=[...new Set([...m.map(T=>T.date),...g.map(T=>T.date)])].sort();if(!y.length)return{};const x=new Map(m.map(T=>[T.date,T.accuracy])),w=new Map(g.map(T=>[T.date,T.accuracy]));return{tooltip:{trigger:"axis",formatter:function(T){let b=T[0].name+"<br/>";return T.forEach(A=>{A.value!==null&&(b+='<span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:'+A.color+'"></span>',b+=A.seriesName+": "+A.value+"%<br/>")}),b}},legend:{data:["单词正确率","错题正确率"],bottom:0},grid:{left:"3%",right:"4%",bottom:"15%",top:"10px",containLabel:!0},xAxis:{type:"category",data:y},yAxis:{type:"value",name:"正确率%",min:0,max:100,axisLabel:{formatter:"{value}%"}},series:[{name:"单词正确率",type:"line",smooth:!0,connectNulls:!0,symbol:"circle",symbolSize:8,lineStyle:{color:"#67c23a",width:2},itemStyle:{color:"#67c23a"},areaStyle:{color:{type:"linear",x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:"rgba(103, 194, 58, 0.25)"},{offset:1,color:"rgba(103, 194, 58, 0.05)"}]}},data:y.map(T=>x.get(T)??null)},{name:"错题正确率",type:"line",smooth:!0,connectNulls:!0,symbol:"circle",symbolSize:8,lineStyle:{color:"#409eff",width:2},itemStyle:{color:"#409eff"},areaStyle:{color:{type:"linear",x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:"rgba(64, 158, 255, 0.25)"},{offset:1,color:"rgba(64, 158, 255, 0.05)"}]}},data:y.map(T=>w.get(T)??null)}]}});return yd(async()=>{try{const{data:m}=await kf.getSummary();t.value=m}catch(m){console.error("获取统计失败:",m)}try{const m=await Wf.getOverview();i.value=m.data}catch(m){console.error("获取学习概览失败:",m)}}),(m,g)=>{const y=$e("el-col"),x=$e("el-row"),w=$e("Reading"),T=$e("el-icon"),b=$e("Document"),A=$e("CircleCheck"),C=$e("SuccessFilled"),D=$e("el-option"),L=$e("el-select"),M=$e("el-empty"),P=$e("el-card"),N=$e("el-button"),I=$e("el-table-column"),V=$e("el-tag"),Z=$e("el-progress"),B=$e("el-table"),$=$e("el-radio-button"),q=$e("el-radio-group");return Bt(),Zr("div",Oy,[J(x,{gutter:24},{default:re(()=>[J(y,{span:8},{default:re(()=>[O("div",{class:"stat-card stat-card-red",onClick:g[0]||(g[0]=j=>m.$router.push("/questions"))},[g[13]||(g[13]=O("div",{class:"stat-glow"},null,-1)),g[14]||(g[14]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:xd,class:"stat-icon-img"})],-1)),O("div",By,[O("div",Fy,Ee(t.value.total_questions),1),g[12]||(g[12]=O("div",{class:"stat-label"},"错题总数",-1))])])]),_:1}),J(y,{span:8},{default:re(()=>[O("div",{class:"stat-card stat-card-orange",onClick:g[1]||(g[1]=j=>m.$router.push("/questions"))},[g[16]||(g[16]=O("div",{class:"stat-glow"},null,-1)),g[17]||(g[17]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Td,class:"stat-icon-img"})],-1)),O("div",Gy,[O("div",zy,Ee(t.value.total_subjects),1),g[15]||(g[15]=O("div",{class:"stat-label"},"学科数量",-1))])])]),_:1}),J(y,{span:8},{default:re(()=>[O("div",{class:"stat-card stat-card-yellow",onClick:g[2]||(g[2]=j=>m.$router.push("/management"))},[g[19]||(g[19]=O("div",{class:"stat-glow"},null,-1)),g[20]||(g[20]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:wd,class:"stat-icon-img"})],-1)),O("div",Uy,[O("div",Vy,Ee(t.value.active_days||0),1),g[18]||(g[18]=O("div",{class:"stat-label"},"活跃学习天数",-1))])])]),_:1})]),_:1}),J(x,{gutter:24,style:{"margin-top":"24px"}},{default:re(()=>[J(y,{span:8},{default:re(()=>[O("div",{class:"stat-card stat-card-green",onClick:g[3]||(g[3]=j=>m.$router.push("/questions"))},[g[22]||(g[22]=O("div",{class:"stat-glow"},null,-1)),g[23]||(g[23]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Us,class:"stat-icon-img"})],-1)),O("div",Hy,[O("div",ky,Ee(t.value.to_review_questions||0),1),g[21]||(g[21]=O("div",{class:"stat-label"},"待复习(错题)",-1))])])]),_:1}),J(y,{span:8},{default:re(()=>{var j;return[O("div",{class:"stat-card stat-card-cyan",onClick:g[4]||(g[4]=Q=>m.$router.push("/words"))},[g[25]||(g[25]=O("div",{class:"stat-glow"},null,-1)),g[26]||(g[26]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Us,class:"stat-icon-img"})],-1)),O("div",Wy,[O("div",Xy,Ee(((j=t.value.word_stats)==null?void 0:j.to_review_count)||0),1),g[24]||(g[24]=O("div",{class:"stat-label"},"待复习(单词)",-1))])])]}),_:1}),J(y,{span:8},{default:re(()=>{var j;return[O("div",{class:"stat-card stat-card-blue",onClick:g[5]||(g[5]=Q=>m.$router.push("/words"))},[g[28]||(g[28]=O("div",{class:"stat-glow"},null,-1)),g[29]||(g[29]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Sd,class:"stat-icon-img"})],-1)),O("div",jy,[O("div",Zy,Ee(((j=t.value.word_stats)==null?void 0:j.total_reviews)||0),1),g[27]||(g[27]=O("div",{class:"stat-label"},"复习次数",-1))])])]}),_:1})]),_:1}),J(x,{gutter:24,style:{"margin-top":"24px"}},{default:re(()=>[J(y,{span:8},{default:re(()=>{var j;return[O("div",{class:"stat-card stat-card-indigo",onClick:g[6]||(g[6]=Q=>m.$router.push("/words"))},[g[31]||(g[31]=O("div",{class:"stat-glow"},null,-1)),g[32]||(g[32]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:bd,class:"stat-icon-img"})],-1)),O("div",qy,[O("div",Yy,Ee(((j=t.value.word_stats)==null?void 0:j.total_words)||0),1),g[30]||(g[30]=O("div",{class:"stat-label"},"单词总数",-1))])])]}),_:1}),J(y,{span:8},{default:re(()=>{var j;return[O("div",{class:"stat-card stat-card-violet",onClick:g[7]||(g[7]=Q=>m.$router.push("/words"))},[g[34]||(g[34]=O("div",{class:"stat-glow"},null,-1)),g[35]||(g[35]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Ad,class:"stat-icon-img"})],-1)),O("div",$y,[O("div",Ky,Ee(((j=t.value.word_stats)==null?void 0:j.reviewed_words)||0),1),g[33]||(g[33]=O("div",{class:"stat-label"},"已复习单词",-1))])])]}),_:1}),J(y,{span:8},{default:re(()=>{var j;return[O("div",{class:"stat-card stat-card-purple",onClick:g[8]||(g[8]=Q=>m.$router.push("/words"))},[g[37]||(g[37]=O("div",{class:"stat-glow"},null,-1)),g[38]||(g[38]=O("div",{class:"stat-icon-wrapper"},[O("img",{src:Ed,class:"stat-icon-img"})],-1)),O("div",Jy,[O("div",Qy,Ee(((j=t.value.word_stats)==null?void 0:j.accuracy)||0)+"%",1),g[36]||(g[36]=O("div",{class:"stat-label"},"单词正确率",-1))])])]}),_:1})]),_:1}),J(x,{gutter:24,style:{"margin-top":"24px"}},{default:re(()=>[J(y,{span:12},{default:re(()=>[O("div",ex,[g[49]||(g[49]=O("div",{class:"today-card-header"},[O("span",{class:"today-title"},"学习概览")],-1)),O("div",tx,[O("div",rx,[g[43]||(g[43]=O("div",{class:"overview-column-header"},"昨日",-1)),O("div",ix,[O("div",nx,[J(T,null,{default:re(()=>[J(w)]),_:1})]),O("div",ax,[O("div",ox,Ee(i.value.yesterday_word_review_count),1),g[39]||(g[39]=O("div",{class:"overview-label"},"复习单词",-1))])]),O("div",sx,[O("div",lx,[J(T,null,{default:re(()=>[J(b)]),_:1})]),O("div",ux,[O("div",hx,Ee(i.value.yesterday_question_review_count),1),g[40]||(g[40]=O("div",{class:"overview-label"},"复习错题",-1))])]),O("div",fx,[O("div",cx,[J(T,null,{default:re(()=>[J(A)]),_:1})]),O("div",dx,[O("div",vx,Ee(i.value.yesterday_word_accuracy)+"%",1),g[41]||(g[41]=O("div",{class:"overview-label"},"单词正确率",-1))])]),O("div",px,[O("div",gx,[J(T,null,{default:re(()=>[J(C)]),_:1})]),O("div",mx,[O("div",_x,Ee(i.value.yesterday_question_accuracy)+"%",1),g[42]||(g[42]=O("div",{class:"overview-label"},"错题正确率",-1))])])]),O("div",yx,[g[48]||(g[48]=O("div",{class:"overview-column-header today-header"},"今日",-1)),O("div",xx,[O("div",Tx,[J(T,null,{default:re(()=>[J(w)]),_:1})]),O("div",wx,[O("div",Sx,Ee(i.value.today_word_review_count),1),g[44]||(g[44]=O("div",{class:"overview-label"},"复习单词",-1))])]),O("div",bx,[O("div",Ax,[J(T,null,{default:re(()=>[J(b)]),_:1})]),O("div",Ex,[O("div",Lx,Ee(i.value.today_question_review_count),1),g[45]||(g[45]=O("div",{class:"overview-label"},"复习错题",-1))])]),O("div",Cx,[O("div",Mx,[J(T,null,{default:re(()=>[J(A)]),_:1})]),O("div",Dx,[O("div",Px,Ee(i.value.today_word_accuracy)+"%",1),g[46]||(g[46]=O("div",{class:"overview-label"},"单词正确率",-1))])]),O("div",Nx,[O("div",Ix,[J(T,null,{default:re(()=>[J(C)]),_:1})]),O("div",Rx,[O("div",Ox,Ee(i.value.today_question_accuracy)+"%",1),g[47]||(g[47]=O("div",{class:"overview-label"},"错题正确率",-1))])])])])])]),_:1}),J(y,{span:12},{default:re(()=>[J(P,{class:"chart-card",shadow:"hover"},{header:re(()=>[O("div",Bx,[g[50]||(g[50]=O("span",{class:"header-title"},"错误类型分布",-1)),J(L,{modelValue:r.value,"onUpdate:modelValue":g[9]||(g[9]=j=>r.value=j),placeholder:"选择学科",size:"small",style:{width:"140px"}},{default:re(()=>[(Bt(!0),Zr(Sa,null,ba(t.value.by_subject,j=>(Bt(),Tn(D,{key:j.subject_id,label:j.subject_name,value:j.subject_id},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])])]),default:re(()=>[d.value?(Bt(),Zr("div",Fx,[J(zs(Gs),{option:c.value,autoresize:"",style:{height:"280px"}},null,8,["option"])])):(Bt(),Tn(M,{key:1,description:"暂无数据"}))]),_:1})]),_:1})]),_:1}),J(x,{gutter:24,style:{"margin-top":"24px"}},{default:re(()=>[J(y,{span:12},{default:re(()=>[J(P,{class:"subject-table-card",shadow:"hover"},{header:re(()=>[O("div",Gx,[g[52]||(g[52]=O("span",{class:"header-title"},"学科详细数据",-1)),J(N,{type:"primary",size:"small",onClick:g[10]||(g[10]=j=>m.$router.push("/questions"))},{default:re(()=>[...g[51]||(g[51]=[nr("查看全部",-1)])]),_:1})])]),default:re(()=>[J(B,{data:v.value,stripe:"",style:{width:"100%"}},{default:re(()=>[J(I,{type:"index",label:"#",width:"60",align:"center"}),J(I,{prop:"subject_name",label:"学科",width:"80"},{default:re(({row:j})=>[J(V,{type:"primary",plain:""},{default:re(()=>[nr(Ee(j.subject_name),1)]),_:2},1024)]),_:1}),J(I,{label:"错题数",width:"70",align:"center"},{default:re(({row:j})=>[O("span",zx,Ee(j.question_count),1)]),_:1}),J(I,{label:"难度分布","min-width":"240"},{default:re(({row:j})=>[O("div",Ux,[(Bt(),Zr(Sa,null,ba(5,Q=>{var ie,ae;return O("div",{key:Q,class:"diff-bar-item"},[O("span",Vx,"难度"+Ee(Q),1),J(Z,{percentage:a(((ie=j.difficulty_distribution)==null?void 0:ie[Q])||0,j.question_count),"stroke-width":8,color:o(Q),"show-text":!1,style:{flex:"1"}},null,8,["percentage","color"]),O("span",Hx,Ee(((ae=j.difficulty_distribution)==null?void 0:ae[Q])||0),1)])}),64))])]),_:1}),J(I,{label:"主要错误类型","min-width":"180"},{default:re(({row:j})=>[O("div",kx,[(Bt(!0),Zr(Sa,null,ba(u(j.error_type_counts),(Q,ie)=>(Bt(),Tn(V,{key:ie,type:l(ie),size:"small",style:{"margin-right":"4px"}},{default:re(()=>[nr(Ee(ie)+" "+Ee(Q),1)]),_:2},1032,["type"]))),128))])]),_:1}),J(I,{prop:"practice_count",label:"练习次数",width:"120",align:"center"},{default:re(({row:j})=>[O("span",Wx,Ee(j.practice_count||0),1)]),_:1})]),_:1},8,["data"])]),_:1})]),_:1}),J(y,{span:12},{default:re(()=>[J(P,{class:"chart-card",shadow:"hover"},{header:re(()=>[O("div",Xx,[g[58]||(g[58]=O("span",{class:"header-title"},"准确率曲线",-1)),O("div",jx,[J(q,{modelValue:n.value,"onUpdate:modelValue":g[11]||(g[11]=j=>n.value=j),size:"small"},{default:re(()=>[J($,{label:"week"},{default:re(()=>[...g[53]||(g[53]=[nr("最近一周",-1)])]),_:1}),J($,{label:"month"},{default:re(()=>[...g[54]||(g[54]=[nr("最近一月",-1)])]),_:1}),J($,{label:"3months"},{default:re(()=>[...g[55]||(g[55]=[nr("最近3月",-1)])]),_:1}),J($,{label:"halfyear"},{default:re(()=>[...g[56]||(g[56]=[nr("最近半年",-1)])]),_:1}),J($,{label:"all"},{default:re(()=>[...g[57]||(g[57]=[nr("全部",-1)])]),_:1})]),_:1},8,["modelValue"])])])]),default:re(()=>[h.value?(Bt(),Zr("div",Zx,[J(zs(Gs),{option:_.value,autoresize:"",style:{height:"300px"}},null,8,["option"])])):(Bt(),Tn(M,{key:1,description:"暂无准确率数据"}))]),_:1})]),_:1})]),_:1})])}}},Jx=Hf(qx,[["__scopeId","data-v-91983b12"]]);export{Jx as default};
