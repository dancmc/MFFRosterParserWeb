/**
 * Created by Daniel on 21/04/2017.
 */

// Found out that web workers don't have canvas/image elements

$("#test").click(function () {

        var code = "self.onmessage= function (e) {\
        var base64url = e.data;\
        var image  = new Image();\
        image.onload = function(){\
            self.postMessage(this.width);\
        };\
        image.src = base64url}"

        var blob = new Blob([code], {type: 'application/javascript'});

        var reader = new FileReader();


        reader.onload = function (event) {
            var worker = new Worker(URL.createObjectURL(blob));
            worker.onmessage = function (event) {
                console.log(event.data);
                worker.terminate();
            };

            var base64url = event.target.result;
            worker.postMessage(base64url);
        };

        var images = Array.from(document.getElementById('images').files);
        reader.readAsDataURL(images[0])


    }
);

function ss() {
    self.onmessage= function (e) {
        var base64url = e.data;
        var image  = new Image();

        image.onload = function(){
            self.postMessage(this.width);
        };
        image.src = base64url
    }
}