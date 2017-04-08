import {Compress} from 'bundle'

$("#image_submit").submit(function (event) {
    event.preventDefault();

    var formData = new FormData();
    var images = [...document.getElementById('images').files]

    console.log(images)
    Compress.compress(images, {
        size: 0.1, // the max size in MB, defaults to 2MB
        quality: 0.75, // the quality of the image, max is 1,
        maxWidth: 1280, // the max width of the output image, defaults to 1920px
        maxHeight: 1280, // the max height of the output image, defaults to 1920px
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

            var json = JSON.parse(returndata);

            // getting list of single image
            var images = Object.keys(json.successful[0]);
            // set base64 url as src and append
            var image = new Image();
            image.src = images[0];
            document.body.appendChild(image);

            // get the corresponding json string
            // images[0] is both the imagedataurl and the key
            var para = document.createElement("p");
            para.appendChild(document.createTextNode("Total time taken : " + json.time_taken + "\n" + json.successful[0][images[0]]));
            document.body.appendChild(para);
        }
    });
}