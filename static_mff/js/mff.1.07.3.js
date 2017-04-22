// use this file if not using npm or using ecmascript 5



function compressAll(mode) {
    var formData = new FormData();
    var images = Array.from(document.getElementById('images').files);

    if (images.length === 0) {
        const resultdiv = $("#result_div");
        resultdiv.empty();
        resultdiv.append("<h3>Please select 1 or more images</h3>");
    }

    var Compress = new ImageCompressor();
    Compress.imagesToResizedBlobs(images, {
        "maxSize": 0.1,
        "resize": true,
        "speed": 4,
        "log": true
    }, function (resultArray) {
        resultArray.forEach(function (item) {
            console.log("Compressed by " +item.compression+ "%");
            formData.append("file", item.blob);
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
                var json = JSON.parse(returndata);
                console.log(json);
                var resultdiv = $("#result_div");
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

                        var gearname_span = $("<p><b>" + dup.gear_name + "</b></p>");
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
                            var succjson_span = $("<p>" + succ[base64] + "</p>");

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