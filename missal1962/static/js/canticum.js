

$(window).on("load", function () {


    /**
     *
     * Globals
     *
    **/

    const $templateContentIntro = $("#template-content-intro").text();
    const $templateContentPrint = $("#template-content-print").text();

    const $sidebar = $("nav#sidebar");
    const $sidebarAndContent = $("#sidebar, #content");
    const $searchInput = $("input#search-input");
    const $sidebarTools = $("div#sidebar-tools");

    let loadedProperDate;
    let selectedDate;

    /**
     *
     * Functions
     *
     **/

    function setDate(date) {
        selectedDate = date;
    }

    function getDate() {
        if (selectedDate === undefined) {
            let url = window.location.href.replace(/#.*/, "");
            selectedDate = url.split('/').reverse()[0];
        }
        return selectedDate;
    }

    /**
      * Obtain a proper for the given `date` through AJAX call and populate
      * the main element with Bootstrap grid.
      * Once populated, mark corresponding element in the sidebar as active and select given date in the datepicker.
     **/
    function loadProper(date, historyReplace = false) {
        if (loadedProperDate === getDate()) {
            return;
        }
        showLoader();
        let title;
        $.getJSON(config.canticumEndpoint + date, function(data) {
            $loadedContent.empty();
            window.scrollTo(0, 0);
            title = data.title;
            let description = data.body;
            $(renderTemplate($templateContentIntro, {
                title: title,
                description: description.split("\n").join("<br />")
            })).appendTo($loadedContent);
        }).done(function() {
            loadedProperDate = date;
            if (historyReplace === true) {
                window.history.replaceState({date: date}, '', '/canticum/' + date);
            } else {
                window.history.pushState({date: date}, '', '/canticum/' + date);
            }
            document.title = title + " | " + "Mszał Rzymski";
            toggleSidebarItem(date);
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
        }).fail(function() {
            alert(cannotLoadMessage);
        }).always(function() {
            hideLoader();
        });
    }

    /**
      * Mark sidebar element for given `date` as active. If an element is not present, reload the sidebar
      * with the data for proper year.
     **/
    function toggleSidebarItem(date) {
        function markItemActive(date) {
            $sidebar.find("li.sidebar-item").removeClass("active");
            let newActive = $("li#sidebar-item-" + date);
            newActive.addClass("active");

            let itemPosition = newActive.position().top;
            let sidebarPosition = Math.abs($sidebar.find("ul").position().top);

            if ((itemPosition > $sidebar.height() * 0.6) || itemPosition < $sidebarTools.height() * 1.5) {
                $sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
            }
        }
        markItemActive(date);
    }

    /**
      *
      * Bindings
      *
     **/

    $(document).on('click', '#sidebar ul li a' , function(event) {
        event.preventDefault();
        setDate(event.currentTarget.href.split("/").pop());
        loadProper(getDate());
    });

    window.onpopstate = function(event){
        setDate(event.target.location.href.split("/").reverse()[0]);
        loadProper(getDate(), true);
    };

    /**
     * filter out the elements in the sidebar;
     * start filtering from 3 characters on;
     * show all elements on empty input
     **/
    $searchInput.on("input", function () {
        let searchString = $(this).val();
        if (searchString === "") {
            let itemsAll = $sidebar.find("li.sidebar-item");
            itemsAll.show();
            toggleSidebarItem(getDate());
        } else if (searchString.length > 2) {
            let itemsAll = $sidebar.find("li.sidebar-item");
            itemsAll.hide();
            $('li.sidebar-item div:contains("' + searchString + '")').parent().parent().show("fast");
        }
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
