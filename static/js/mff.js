var totalcount
var currentcount;
var formData;
var preferredWidth = 1400;

function append_formdata(blob) {
    formData.append('file', blob)
    currentcount++

    if (totalcount === currentcount) {
        sub(formData)
    }
}

function resizeInCanvas(img, ext) {

    var ratio = preferredWidth / img.width;
    var canvas = document.createElement("CANVAS");

    canvas.width = img.width * ratio;
    console.log(canvas.width)
    canvas.height = img.height * ratio;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(function (blob) {
        append_formdata(blob)
    }, ext, 0.80);

}


$("#image_submit").submit(function (event) {
    event.preventDefault();
    // the first element of a form contains all the
    formData = new FormData();
    currentcount = 0

    // var formData1 = new FormData($("#image_submit")[0]);
    // var images = formData1.getAll('file');
    var images = document.getElementById('images').files
    totalcount = images.length


    for (var i = 0; i < totalcount; i++) {
        (function () {
            var reader = new FileReader();
            var blob = images[i]
            var img = new Image();
            var ext = blob.type

            img.onload = function () {
                if (img.width > preferredWidth) {
                    resizeInCanvas(this, ext)
                } else {
                    append_formdata(blob)
                }
            };

            reader.onload = function (event) {
                img.src = event.target.result
            }
            reader.readAsDataURL(blob)
        })()
    }


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

            var json = JSON.parse(returndata);
            console.log(json)

            // getting list of single image
            var images = Object.keys(json.successful[0]);
            // set base64 url as src and append
            var image = new Image();
            image.src = images[0];
            $("#result_div").append(image);

            // get the corresponding json string
            // images[0] is both the imagedataurl and the key
            var span = document.createElement("span");
            span.innerHTML = "Total time taken : " + json.time_taken + "\n" + json.successful[0][images[0]];
            $("#result_div").append(span);
        }
    });
}