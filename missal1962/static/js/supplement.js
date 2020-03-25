

$window.on("load", function () {
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

    function getResourceId() {
        if (selectedResource === undefined) {
            return extractResourceId(window.location.href);
        }
        return selectedResource;
    }

    function extractResourceId(url) {
        let splitUrl = url.split("/").reverse();
        if (splitUrl.length > 5) {
            return splitUrl[1] + "/" + splitUrl[0];
        }
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
        $.getJSON(config.supplementEndpoint + resourceId, function(data) {
            $loadedContent.empty();
            window.scrollTo(0, 0);
            title = data.title;
            let description = data.body;
            $(renderTemplate($templateContent, {
                title: title,
                description: description
            })).appendTo($loadedContent);
        }).done(function() {
            loadedResource = resourceId;
            if (historyReplace === true) {
                window.history.replaceState({resourceId: resourceId}, '', '/' + config.lang + '/' + resourceId);
            } else {
                window.history.pushState({resourceId: resourceId}, '', '/' + config.lang + '/' + resourceId);
            }
            document.title = title + " | " + "Missale Meum";
            markSidebarItemActive(resourceId);
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
        }).fail(function() {
            alert(config.translation.cannotLoadMessage);
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
        setResourceId(extractResourceId(event.currentTarget.href));
        loadContent(getResourceId());
    });

    window.onpopstate = function(event){
        setResourceId(extractResourceId(event.target.location.href));
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
