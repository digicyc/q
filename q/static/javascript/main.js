require(["jquery",
         "slides.min.jquery",
         "backbone-0.9.1",
         "backbone-tastypie-0.1"
        ],
    function($) {
        function loadCss(url) {
            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = url;
            link.media = "all";
            document.getElementsByTagName("head")[0].appendChild(link);
        }
        loadCss("/font/stylesheet.css");


    }
);