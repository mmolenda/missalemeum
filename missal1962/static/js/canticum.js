

$(window).on("load", function () {


    /**
     *
     * Globals
     *
    **/

    const $templateContent = $("#template-content").text();
    const $templateContentPrint = $("#template-content-print").text();
    const $sidebarAndContent = $("#sidebar, #content");
    const $searchInput = $("input#search-input");

    let urlPart = "canticum";
    let loadedResource;
    let selectedResource;

    /**
     *
     * Functions
     *
     **/

    function init() {
        let resourceId = getResourceId();
        if (resourceId === undefined) {
            resourceId = $("li.sidebar-item").first().find("a").attr("href");
            setResourceId()
        }
        loadContent(resourceId);
    }

    init();

    function setResourceId(resourceId) {
        selectedResource = resourceId;
    }

    function getResourceId() {
        if (selectedResource === undefined) {
            let splitUrl = window.location.href.split("/").reverse();
            if (splitUrl[0] !== urlPart) {
                selectedResource = splitUrl[0];
            }
        }
        return selectedResource;
    }

    /**
      * Obtain content for the given `resourceId` through AJAX call and populate the main element with Bootstrap grid.
      * Once populated, mark corresponding element in the sidebar as active.
     **/
    function loadContent(resourceId, historyReplace = false) {
        if (loadedResource === resourceId) {
            return;
        }
        loader.show();
        let title;
        $.getJSON(config.canticumEndpoint + resourceId, function(data) {
            $loadedContent.empty();
            window.scrollTo(0, 0);
            title = data.title;
            let description = data.body;
            $(renderTemplate($templateContent, {
                title: title,
                description: description.split("\n").join("<br />")
            })).appendTo($loadedContent);
        }).done(function() {
            loadedResource = resourceId;
            if (historyReplace === true) {
                window.history.replaceState({resourceId: resourceId}, '', '/' + urlPart + '/' + resourceId);
            } else {
                window.history.pushState({resourceId: resourceId}, '', '/' + urlPart + '/' + resourceId);
            }
            document.title = title + " | " + "Mszał Rzymski";
            markSidebarItemActive(resourceId);
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
        }).fail(function() {
            alert(cannotLoadMessage);
        }).always(function() {
            loader.hide();
        });
    }

    /**
      *
      * Bindings
      *
     **/

    $(document).on('click', '#sidebar ul li a' , function(event) {
        event.preventDefault();
        setResourceId(event.currentTarget.href.split("/").pop());
        loadContent(getResourceId());
    });

    window.onpopstate = function(event){
        setResourceId(event.target.location.href.split("/").reverse()[0]);
        loadContent(getResourceId(), true);
    };

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
