

$(window).on("load", function () {


    /**
     *
     * Globals
     *
    **/

    const $templateContentIntro = $("#template-content-intro").text();
    const $templateContentPrint = $("#template-content-print").text();
    const $sidebarAndContent = $("#sidebar, #content");
    const $searchInput = $("input#search-input");

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
            markSidebarItemActive(date);
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
        filterSidebarItems($(this).val(), function() {markSidebarItemActive(getDate())});
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
