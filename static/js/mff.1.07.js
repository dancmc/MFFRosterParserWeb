// use this file if not using npm or using ecmascript 5

var totalcount
var currentcount;
var formData;

function append_formdata(blob) {
    formData.append('file', blob)
    currentcount++

    if (totalcount === currentcount) {
        sub(formData)
    }
}

function defaultFor(arg, val) {
    return typeof arg !== 'undefined' ? arg : val;
}

function Picture(dataurl, base64string, mime, size, time, width, height) {
    this.dataurl = dataurl;
    this.base64string = base64string;
    this.mime = mime;
    this.size = size;
    this.time = time;
    this.width = width;
    this.height = height;
}

function imagesToResizedDataUrl(fileArray, options, callback) {

    var totalcount = fileArray.length;
    var resultArray = [];


    fileArray.forEach(function(file) {

            var reader = new FileReader();
            var img = new Image();
            var mime = file.type;
            var startTime = new Date().getTime();

            img.onload = function () {
                var maxWidth = defaultFor(options["maxWidth"], 99999);
                var maxHeight = defaultFor(options["maxHeight"], 99999);
                var maxSize = defaultFor(options["maxSize"], 99);
                var minQuality = defaultFor(options["minQuality"], 10)/100.0;
                var speed = defaultFor(options["speed"], 1);
                var resize = defaultFor(options["resize"], false);


                var canvas = document.createElement("CANVAS");
                var currentQuality = 0.9;
                var decrement = 0.8/speed;

                //resize img first
                var ratio = Math.min(Math.min(maxWidth / img.width, maxHeight / img.height), 1.0);
                var ratioception = 0.9;

                canvas.width = img.width * ratio;
                canvas.height = img.height * ratio;

                var ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                var dataUrl = canvas.toDataURL('image/jpeg', currentQuality);
                var imgFileSize = (dataUrl.length - 22) * 3 / 4 / 1024 / 1024;

                console.log(imgFileSize);

                while (imgFileSize > maxSize && currentQuality > minQuality) {
                    currentQuality -= decrement;
                    dataUrl = canvas.toDataURL('image/jpeg', currentQuality);
                    imgFileSize = (dataUrl.length - 22) * 3 / 4 / 1024 / 1024;
                }
                console.log(currentQuality+" "+imgFileSize);

                while ((imgFileSize > maxSize && resize && ratioception > 0.1)) {
                    canvas.width = img.width * ratio * ratioception;
                    canvas.height = img.height * ratio * ratioception;
                    currentQuality = 1.0;
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                    while (imgFileSize > maxSize && currentQuality > 0.1) {
                        currentQuality -= decrement;
                        dataUrl = canvas.toDataURL('image/jpeg', currentQuality);
                        imgFileSize = (dataUrl.length - 22) * 3 / 4 / 1024 / 1024;
                    }

                    ratioception -= 0.1;
                }


                resultArray.push(new Picture(dataUrl, dataUrl.split(",")[1], mime, imgFileSize, new Date().getTime()-startTime, canvas.width, canvas.height));
                if (resultArray.length === totalcount) {
                    callback(resultArray);
                }
            };

            reader.onload = function (event) {
                img.src = event.target.result;
            };
            reader.readAsDataURL(file)
    });
}

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type: mime});
}

function compressAll(mode) {
    var formData = new FormData();
    var images = Array.from(document.getElementById('images').files);

    if (images.length === 0) {
        const resultdiv = $("#result_div");
        resultdiv.empty();
        resultdiv.append("<h3>Please select 1 or more images</h3>");
    }

    imagesToResizedDataUrl(images, {
        "maxSize" : 0.1,
        "resize": true,
        "speed" : 4
    }, function(resultArray){
        resultArray.forEach(function(item){
            formData.append("file", dataURLtoBlob(item.dataurl));
            console.log("Took "+item.time+"ms, Size is "+item.size+" MB")
        });
        formData.append("mode", mode);
        sub(formData, mode);

    })
}


$("#submit_multi").click(function () {
        compressAll("multi")
    }
);

$("#submit_single").click(function () {
        compressAll("single")
    }
);

function sub(formData, mode) {

    $.ajax({
            url: "/mff/ocr",
            type: 'POST',
            data: formData,
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            // enctype:"base64",
            success: function (returndata) {
                const json = JSON.parse(returndata);
                console.log(json);
                const resultdiv = $("#result_div");
                resultdiv.empty();

                if (mode === "multi") {

                    // show total time taken & file info
                    const time = $("<div>Request took " + json.time_taken + "  seconds</div>");
                    resultdiv.append(time);
                    $('<p />').text('Total files sent : ' + json.number_total_files).appendTo(resultdiv);
                    $('<p />').text('Invalid files : ' + json.number_invalid_files).appendTo(resultdiv);
                    $('<p />').text('Successes : ' + json.successful.length).appendTo(resultdiv);
                    $('<p />').text('Failures : ' + json.failures.length).appendTo(resultdiv);
                    $('<p />').text('Ambiguous gears : ' + json.duplicate_gears.length).appendTo(resultdiv);

                    //========== asking about ambiguous gears ============
                    if (json.duplicate_gears.length > 0) {
                        resultdiv.append("<h2>Please choose</h2>");
                    }
                    json.duplicate_gears.forEach(function (dup) {
                        var newdiv = $('<div />');

                        var image = new Image();
                        image.src = dup.thumbnail_base64;

                        var list = $('<select />');
                        for (var charalias in dup.char_list) {
                            var option = document.createElement("option");
                            option.value = charalias;
                            option.text = charalias + " : " + dup.char_list[charalias];
                            list.append(option)
                        }

                        var gearname_span = $("<br><p><b>" + dup.gear_name + "</b></p></br>");
                        var gearjson_span = $("<br><p>" + dup.gear_json + "</p></br>");

                        newdiv.append(image);
                        newdiv.append(gearname_span);
                        newdiv.append(list);
                        newdiv.append(gearjson_span);
                        resultdiv.append(newdiv)
                    });

                    //========== showing successes =======================
                    if (json.successful.length > 0) {
                        resultdiv.append("<h2>Successes</h2>");
                    }
                    json.successful.forEach(function (succ) {
                        for (var base64 in succ) {
                            var newdiv = $('<div />');

                            var image = new Image();
                            image.src = base64;
                            var succjson_span = $("<br><p>" + succ[base64] + "</p></br>");

                            newdiv.append(image);
                            newdiv.append(succjson_span);
                            resultdiv.append(newdiv);
                        }
                    });

                    //========== showing failures ========================
                    if (json.failures.length > 0) {
                        resultdiv.append("<h2>Failures</h2>");
                    }
                    json.failures.forEach(function (base64) {
                        var newdiv = $('<div />');

                        var image = new Image();
                        image.src = base64;
                        newdiv.append(image);
                        newdiv.append($('<p />'))
                        resultdiv.append(newdiv);
                    });
                } else if (mode === "single") {
                    $('<p />').text(returndata).appendTo(resultdiv);
                }

            }
        }
    )
}