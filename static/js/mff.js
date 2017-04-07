



$("#image_submit").submit(function (event) {
    event.preventDefault();
    var formData = new FormData($("#image_submit")[0]);


    $.ajax({
        url : $(this).attr("action"),
        type: 'POST',
        data: formData,
        //async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (returndata) {

            var json = JSON.parse(returndata);

            // getting list of images
            var images= Object.keys(json.successful[0]);
            // set base64 url as src and append
            var image = new Image();
            image.src = images[0];
            document.body.appendChild(image);

            // get the corresponding json string
            var para = document.createElement("p");
            para.appendChild(document.createTextNode(json.successful[0][images[0]]));
            document.body.appendChild(para);
        }
    });
});