function LoadJS(id, fileUrl) {
    var scriptTag = document.getElementById(id);
    var oHead = document.getElementsByTagName('HEAD').item(0);
    var oScript = document.createElement("script");
    if (scriptTag) oHead.removeChild(scriptTag);
    oScript.type = "text/javascript";
    oScript.src = fileUrl;
    oHead.appendChild(oScript);
}
function LoadCSS(id, fileUrl) {
    var scriptTag = document.getElementById(id);
    var oHead = document.getElementsByTagName('HEAD').item(0);
    var oScript = document.createElement("link");
    if (scriptTag) oHead.removeChild(scriptTag);
    oScript.type = "text/css";
    oScript.href = fileUrl;
    oScript.rel = "stylesheet"
    oHead.appendChild(oScript);
}
$(function () {
    var Vdiv = $("<div style='position:fixed; left:10%; bottom:10%;'></div>");
    var MAIZI_STATIC = "http://127.0.0.1:8000/static/";
    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:8000/plus/recommend_video/",
        data: {"url": location.href, "html": document.getElementsByTagName('html')[0].innerHTML},
        success: function (va) {
            LoadCSS("", MAIZI_STATIC + "css/video-js.css")
            Vdiv.html(va)
            $("body").append(Vdiv);
            LoadJS("", MAIZI_STATIC+"js/video.js")
        },
        dataType: "html"
    });
})