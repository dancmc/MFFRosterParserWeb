(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
const Compress = require('compress.js')
const compress = new Compress()


$("#image_submit").submit(function (event) {
    event.preventDefault();

    console.log("hi")
    var formData = new FormData();
    var images = [...document.getElementById('images').files]

    console.log(images)
    compress.compress(images, {
        size: 0.2, // the max size in MB, defaults to 2MB
        quality: 0.85, // the quality of the image, max is 1,
        maxWidth: 2000, // the max width of the output image, defaults to 1920px
        maxHeight: 1920, // the max height of the output image, defaults to 1920px
        resize: true, // defaults to true, set false if you do not want to resize the image width and height
    }).then((data) => {
        // returns an array of compressed images
        data.forEach(function (item, index) {
            // const img1 = item
            const base64str = item.data
            const imgExt = item.ext
            const file = Compress.convertBase64ToFile(base64str, imgExt)
            console.log(item.elapsedTimeInSeconds)
            formData.append("file", file)
        })
        sub(formData)
    })

});

function sub(formData) {
    // }
    $.ajax({
        url: "/mff/ocr",
        type: 'POST',
        data: formData,
        //async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (returndata) {

            const json = JSON.parse(returndata);

            const resultdiv = $("#result_div");
            resultdiv.empty();

            // show total time taken & file info
            const time = $("<div>Request took " + json.time_taken + "  seconds</div>");
            resultdiv.append(time);
            $('<p />').text('Total files sent : '+ json.number_total_files).appendTo(resultdiv);
            $('<p />').text('Invalid files : '+ json.number_invalid_files).appendTo(resultdiv);
            $('<p />').text('Successes : '+ json.successful.length).appendTo(resultdiv);
            $('<p />').text('Failures : '+ json.failures.length).appendTo(resultdiv);
            $('<p />').text('Ambiguous gears : '+ json.duplicate_gears.length).appendTo(resultdiv);

            //========== asking about ambiguous gears ============
            if(json.duplicate_gears.length >0) {
                resultdiv.append("<h2>Please choose</h2>");
            }
            json.duplicate_gears.forEach(function (dup) {
                let newdiv = $('<div />');

                let image = new Image();
                image.src = dup.thumbnail_base64;

                let list = $('<select />');
                for (let charalias in dup.char_list) {
                    let option = document.createElement("option");
                    option.value = charalias;
                    option.text = charalias + " : " +dup.char_list[charalias];
                    list.append(option)
                }

                let gearname_span = $("<br><p><b>" + dup.gear_name + "</b></p></br>");
                let gearjson_span = $("<br><p>" + dup.gear_json + "</p></br>");

                newdiv.append(image);
                newdiv.append(gearname_span);
                newdiv.append(list);
                newdiv.append(gearjson_span);
                resultdiv.append(newdiv)
            });

            //========== showing successes =======================
            if(json.successful.length >0) {
                resultdiv.append("<h2>Successes</h2>");
            }
            json.successful.forEach(function (succ) {
                for(let base64 in succ){
                    let newdiv = $('<div />');

                    let image = new Image();
                    image.src = base64;
                    let succjson_span = $("<br><p>" + succ[base64] + "</p></br>");

                    newdiv.append(image);
                    newdiv.append(succjson_span);
                    resultdiv.append(newdiv);
                }
            });

            //========== showing failures ========================
            if(json.failures.length >0) {
                resultdiv.append("<h2>Failures</h2>");
            }
            json.failures.forEach(function (base64) {
                    let newdiv = $('<div />');

                    let image = new Image();
                    image.src = base64;
                    newdiv.append(image);
                    newdiv.append($('<p />'))
                    resultdiv.append(newdiv);
            });


        }
    });
}
},{"compress.js":2}],2:[function(require,module,exports){
!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.Compress=e():t.Compress=e()}(this,function(){return function(t){function e(i){if(n[i])return n[i].exports;var r=n[i]={exports:{},id:i,loaded:!1};return t[i].call(r.exports,r,r.exports,e),r.loaded=!0,r.exports}var n={};return e.m=t,e.c=n,e.p="",e(0)}([function(t,e,n){var i,r,a;!function(o,u){r=[t,n(1),n(2),n(3),n(4),n(5)],i=u,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t,e,n,i,r,a){"use strict";function o(t){return t&&t.__esModule?t:{default:t}}function u(t){if(Array.isArray(t)){for(var e=0,n=Array(t.length);e<t.length;e++)n[e]=t[e];return n}return Array.from(t)}function s(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}var f=o(e),d=o(n),l=o(i),c=o(r),h=o(a),p=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),v=function(){function t(){s(this,t)}return p(t,[{key:"attach",value:function(t,e){var n=this;return new Promise(function(i,r){var a=document.querySelector(t);a.setAttribute("accept","image/*"),a.addEventListener("change",function(t){var r=n.compress([].concat(u(t.target.files)),e);i(r)},!1)})}},{key:"compress",value:function(t,e){function n(t,e){var n=new h.default(e);return n.start=performance.now(),n.alt=t.name,n.ext=t.type,n.startSize=t.size,l.default.load(t).then(i(n))}function i(t){return function(e){return c.default.load(e).then(function(e){if(t.startWidth=e.naturalWidth,t.startHeight=e.naturalHeight,t.resize){var n=c.default.resize(t.maxWidth,t.maxHeight)(e.naturalWidth,e.naturalHeight),i=n.width,r=n.height;t.endWidth=i,t.endHeight=r}else t.endWidth=e.naturalWidth,t.endHeight=e.naturalHeight;return d.default.imageToCanvas(t.endWidth,t.endHeight)(e)}).then(function(e){return t.iterations=1,t.base64prefix=f.default.prefix(t.ext),r(e,t.startSize,t.quality,t.size,t.minQuality,t.iterations)}).then(function(e){return t.finalSize=f.default.size(e),f.default.data(e)}).then(function(e){t.end=performance.now();var n=t.end-t.start;return{data:e,prefix:t.base64prefix,elapsedTimeInSeconds:n/1e3,alt:t.alt,initialSizeInMb:d.default.size(t.startSize).MB,endSizeInMb:d.default.size(t.finalSize).MB,ext:t.ext,quality:t.quality,endWidthInPx:t.endWidth,endHeightInPx:t.endHeight,initialWidthInPx:t.startWidth,initialHeightInPx:t.startHeight,sizeReducedInPercent:(t.startSize-t.finalSize)/t.startSize*100,iterations:t.iterations}})}}function r(t,e){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1,i=arguments[3],a=arguments.length>4&&void 0!==arguments[4]?arguments[4]:1,o=arguments[5],u=d.default.canvasToBase64(t,n),s=f.default.size(u);return o+=1,s>i?r(t,s,n-.1,i,a,o):n>a?r(t,s,n-.1,i,a,o):n<.5?u:u}return Promise.all(t.map(function(t){return n(t,e)}))}}],[{key:"convertBase64ToFile",value:function(t,e){return d.default.base64ToFile(t,e)}}]),t}();t.exports=v})},function(t,e,n){var i,r,a;!function(n,o){r=[e],i=o,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var e=function(t){var e=t.replace(/^data:image\/\w+;base64,/,"").length;return(e-814)/1.37},n=function(t){return t.split(";")[0].match(/jpeg|png|gif/)[0]},i=function(t){return t.replace(/^data:image\/\w+;base64,/,"")},r=function(t){return"data:"+t+";base64,"};t.default={size:e,mime:n,data:i,prefix:r}})},function(t,e,n){var i,r,a;!function(n,o){r=[e],i=o,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var e=function(t){for(var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"image/jpeg",n=window.atob(t),i=[],r=0;r<n.length;r++)i[r]=n.charCodeAt(r);return new window.Blob([new Uint8Array(i)],{type:e})},n=function(t,e){var n=document.createElement("canvas");return n.width=t,n.height=e,function(t){var e=n.getContext("2d");return e.drawImage(t,0,0,n.width,n.height),n}},i=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:.75,n=t.toDataURL("image/jpeg",e);return n},r=function(t){return{KB:t/1e3,MB:t/1e6}};t.default={base64ToFile:e,imageToCanvas:n,canvasToBase64:i,size:r}})},function(t,e,n){var i,r,a;!function(n,o){r=[e],i=o,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var e=function(t){return new Promise(function(e,n){var i=new FileReader;i.addEventListener("load",function(t){e(t.target.result)},!1),i.addEventListener("error",function(t){n(t)},!1),i.readAsDataURL(t)})};t.default={load:e}})},function(t,e,n){var i,r,a;!function(n,o){r=[e],i=o,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var e=function(t){return new Promise(function(e,n){var i=new Image;i.addEventListener("load",function(){e(i)},!1),i.addEventListener("error",function(t){n(t)},!1),i.src=t})},n=function(t,e){return function(n,i){if(!t&&!e)return{width:n,height:i};var r=Math.min(n,t),a=Math.min(i,e);if(r){var o=n/r,u=i/o;return{width:r,height:u}}var s=i/a,f=n/s;return{width:f,height:a}}};t.default={load:e,resize:n}})},function(t,e,n){var i,r,a;!function(n,o){r=[e],i=o,a="function"==typeof i?i.apply(e,r):i,!(void 0!==a&&(t.exports=a))}(this,function(t){"use strict";function e(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}Object.defineProperty(t,"__esModule",{value:!0});var n=function t(n){var i=n.quality,r=void 0===i?.75:i,a=n.size,o=void 0===a?2:a,u=n.maxWidth,s=void 0===u?1920:u,f=n.maxHeight,d=void 0===f?1920:f,l=n.resize,c=void 0===l||l;e(this,t),this.start=performance.now(),this.end=null,this.alt=null,this.ext=null,this.startSize=null,this.startWidth=null,this.startHeight=null,this.size=1e3*o*1e3,this.endSize=null,this.endWidth=null,this.endHeight=null,this.iterations=0,this.base64prefix=null,this.quality=r,this.resize=c,this.maxWidth=s,this.maxHeight=d};t.default=n})}])});

},{}]},{},[1]);
