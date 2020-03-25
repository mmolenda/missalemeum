

$window.on("load", function () {


    /**
     *
     * Globals
     *
     **/

    let urlPart = "votive";

    /**
     *
     * Functions
     *
     **/

    adaptSectionColumns();

    let ploader = new ProperContentLoader(config.properEndpoint, config.lang + '/' + urlPart, function() {
        markSidebarItemActive(getResourceId());
    });

    function init() {
        let resourceId = getResourceId();
        if (resourceId === undefined) {
            resourceId = $("li.sidebar-item").first().find("a").attr("href");
            setResourceId()
        }
        ploader.load(resourceId);
    }

    init();

    function getResourceId() {
        if (selectedResource === undefined) {
            let splitUrl = window.location.href.split("?")[0].split("/").reverse();
            if (splitUrl[0] !== urlPart) {
                selectedResource = splitUrl[0];
            }
        }
        return selectedResource;
    }

    /**
     *
     * Bindings
     *
     **/

    $(document).on('click', '#sidebar ul li a' , function(event) {
        event.preventDefault();
        setResourceId(event.currentTarget.href.split("/").pop());
        ploader.load(getResourceId());
    });

    window.onpopstate = function(event){
        setResourceId(event.target.location.href.split("/").reverse()[0]);
        ploader.load(getResourceId(), true);
    };

    $window.on("resize", function(){
        adaptSectionColumns();
    });

    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this.id);
    });

    /**
     * filter out the elements in the sidebar;
     * start filtering from 3 characters on;
     * show all elements on empty input
     **/
    $searchInput.on("input", function () {
        filterSidebarItems($(this).val(), function() {markSidebarItemActive(getResourceId())});
    });

    /**
     * X button in the search input clears current search
     **/
    //
    $("#search-clear").on("click", function () {
        $searchInput.val("").trigger("input");
    });


    $("#print").on("click", function () {
        printContent($templateContentPrint, $loadedContent.html());
    });
});
