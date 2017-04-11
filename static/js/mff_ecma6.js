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