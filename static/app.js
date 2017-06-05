'use strict';

document.addEventListener("DOMContentLoaded", function(){
    var canvas, ctx, px=0, py=0, mx=0, my=0, drawing=false, drawingTimeout;

    // retrieve canvas and its drawing context
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");

    // setup drawing params
    ctx.lineWidth = 5;
    ctx.fillStyle = "black";
    ctx.lineCap = "round";

    // setup event listeners
    canvas.addEventListener("mousemove", onMouseMove, false);
    canvas.addEventListener("mouseup", onMouseUp, false);
    canvas.addEventListener("mousedown", onMouseDown, false);
    canvas.addEventListener("mouseout", onMouseOut, false);

    function onMouseDown(){
        drawing = true;
        drawingStarted();
    }

    function onMouseUp(){
        drawing = false;
        drawingFinished();
    }

    function onMouseOut(){
        drawing = false;
        drawingFinished();
    }


    function onMouseMove(e){
        // save old position
        px = mx;
        py = my;

        // get current position
        mx = e.clientX - canvas.offsetLeft;
        my = e.clientY - canvas.offsetTop;

        // draw line from prev position to current
        if (drawing){
            drawLine(ctx, px, py, mx, my);
        }
    }

    function drawLine(ctx, ax, ay, bx, by){
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.stroke();
    }

    function clear(){
        // clear canvas after sending digit
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function drawingStarted() {
        // clear timeout to prevent clearing canvas when drawing is resumed
        clearTimeout(drawingTimeout);
    }

    function drawingFinished(){
        clearTimeout(drawingTimeout);
        drawingTimeout = setTimeout(function(){
            sendImage();
            clear();
        }, 1000);
    }

    function sendImage(){
        var image = canvas.toDataURL('image/png');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload/');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send(image);

        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4) {
            // TODO: handle response and error properly
            if (xhr.status === 200) {
              console.log(xhr.responseText);
            } else {
              console.log('Error: ' + xhr.status);
            }
          }
        }
    }
});